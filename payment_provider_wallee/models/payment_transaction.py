# Copyright 2021 Camptocamp SA
import logging

from wallee.models import (
    CriteriaOperator,
    EntityQuery,
    EntityQueryFilter,
    EntityQueryFilterType,
    LineItem,
    LineItemType,
    TransactionCompletion,
    TransactionCreate,
    TransactionState,
)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    @api.model
    def _get_redirect_url(self):
        return (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            + "/payment/status"
        )

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code == "wallee":
            wallee_config = (
                self.env["payment.provider"].sudo()._wallee_get_configuration()
            )
            line_items = []
            for order_line in self.sale_order_ids.order_line:
                line_items.append(self._prepare_line_item_from_order_line(order_line))
            # TODO: Improve transaction creation?
            redirect_url = self._get_redirect_url()
            transaction = TransactionCreate(
                line_items=line_items,
                auto_confirmation_enabled=True,
                currency=self.sale_order_ids.currency_id.name,
                success_url=redirect_url,
                failed_url=redirect_url,
            )
            transaction_service = wallee_config.get("transaction_service")
            transaction_create = transaction_service.create(
                space_id=wallee_config.get("space_id"), transaction=transaction
            )
            self.provider_reference = str(transaction_create.id)
            transaction_payment_page_service = wallee_config.get(
                "transaction_payment_page_service"
            )
            payment_page_url = transaction_payment_page_service.payment_page_url(
                space_id=wallee_config.get("space_id"), id=transaction_create.id
            )
            res["api_url"] = payment_page_url
        return res

    # TODO: Improve to consider different types?
    def _prepare_line_item_from_order_line(self, order_line):
        return LineItem(
            # Truncate string to 150 characters due to wallee limitation
            name=order_line.name[:150],
            unique_id=str(order_line.id),
            # sku="red-t-shirt-123",
            quantity=order_line.product_uom_qty,
            amount_including_tax=order_line.price_total,
            type=LineItemType.PRODUCT,
        )

    def get_wallee_transaction_state(self, transaction_id):
        wallee_config = self.env["payment.provider"].sudo()._wallee_get_configuration()
        transaction_service = wallee_config.get("transaction_service")
        entity_query_filter = EntityQueryFilter(
            field_name="id",
            value=transaction_id,
            type=EntityQueryFilterType.LEAF,
            operator=CriteriaOperator.EQUALS,
        )
        entity_query = EntityQuery(filter=entity_query_filter)
        transaction = transaction_service.search(
            space_id=wallee_config.get("space_id"), query=entity_query
        )
        if transaction:
            return transaction[0].state
        else:
            raise ValidationError(
                "Wallee: "
                + _("Cannot get tx state for transaction %s") % transaction_id
            )

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "wallee":
            return tx
        entity_id = notification_data.get("entityId")
        tx = self.search(
            [("provider_reference", "=", entity_id), ("provider_code", "=", "wallee")]
        )
        if not tx:
            raise ValidationError(
                "Wallee: " + _("No transaction found matching reference %s.", entity_id)
            )
        # TODO: Check validity?
        webhook_space_id = notification_data.get("spaceId")
        config_space_id = (
            self.env["payment.provider"]
            .sudo()
            ._wallee_get_configuration()
            .get("space_id")
        )
        if webhook_space_id != config_space_id:
            raise ValidationError(
                "Wallee: "
                + _(
                    "Webhook call for spaceId %s doesn't match payment provider's stateId %s."
                )
                % (webhook_space_id, config_space_id)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != "wallee":
            return
        transaction_number = notification_data.get("entityId")
        transaction_state = self.get_wallee_transaction_state(transaction_number)
        _logger.info(
            "Wallee transaction {} state: {}".format(
                transaction_number, transaction_state
            )
        )
        # TODO refactor using constant mapping?
        if transaction_state in (TransactionState.PENDING, TransactionState.CONFIRMED):
            self._set_pending()
        elif transaction_state in (
            TransactionState.PROCESSING,
            TransactionState.AUTHORIZED,
        ):
            # TODO: Check if must be handled?
            pass
            # self._set_authorized()
        elif transaction_state in (
            TransactionState.FULFILL,
            TransactionState.COMPLETED,
        ):
            self._set_done()
        elif transaction_state in (
            TransactionState.FAILED,
            TransactionState.VOIDED,
            TransactionState.DECLINE,
        ):
            self._set_canceled()
        else:
            self._set_error(
                "Wallee: " + _("Invalid transaction state %s.") % transaction_state
            )
