# Copyright 2021 Camptocamp SA
import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WalleeController(http.Controller):
    @http.route("/payment/wallee/webhook", type="json", auth="public")
    def wallee_webhook(self, **data):
        webhook_data = request.get_json_data()
        if webhook_data.get("listenerEntityTechnicalName") == "Transaction":
            _logger.info(
                "entering _handle_feedback_data with data:\n%s",
                pprint.pformat(webhook_data),
            )
            request.env["payment.transaction"].sudo()._handle_notification_data(
                "wallee", webhook_data
            )
            # Redirect to payment status page is actually done by wallee
            #  TransactionCreate configuration
            return request.redirect("/payment/status")
        else:
            _logger.warning(
                "Webhook call to /payment/wallee/webhook using unsupported webhook listener entity with data\n%s",
                pprint.pformat(webhook_data),
            )
