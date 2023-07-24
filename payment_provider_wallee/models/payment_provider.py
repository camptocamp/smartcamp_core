# Copyright 2021 Camptocamp SA
from wallee import Configuration
from wallee.api import (
    TransactionCompletionServiceApi,
    TransactionPaymentPageServiceApi,
    TransactionServiceApi,
)

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("wallee", "Wallee")], ondelete={"wallee": "set default"}
    )
    wallee_space_id = fields.Integer(
        string="Wallee space ID",
        required_if_provider="wallee",
        groups="base.group_system",
    )
    wallee_application_user_id = fields.Integer(
        string="Wallee Application User ID",
        required_if_provider="wallee",
        groups="base.group_system",
    )
    wallee_application_user_auth_key = fields.Char(
        required_if_provider="wallee", groups="base.group_system"
    )

    @api.model
    def _wallee_get_configuration(self):
        wallee = self.env.ref("payment_provider_wallee.payment_provider_wallee")
        config = Configuration(
            user_id=wallee.wallee_application_user_id,
            api_secret=wallee.wallee_application_user_auth_key,
        )
        transaction_service = TransactionServiceApi(configuration=config)
        transaction_payment_page_service = TransactionPaymentPageServiceApi(
            configuration=config
        )
        transaction_completion_service = TransactionCompletionServiceApi(
            configuration=config
        )
        return {
            "transaction_service": transaction_service,
            "transaction_payment_page_service": transaction_payment_page_service,
            "transaction_completion_service": transaction_completion_service,
            "space_id": wallee.wallee_space_id,
        }
