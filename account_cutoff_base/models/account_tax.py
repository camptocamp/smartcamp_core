# Copyright 2013-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    account_accrued_revenue_id = fields.Many2one(
        comodel_name="account.account",
        string="Accrued Revenue Tax Account",
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
    )
    account_accrued_expense_id = fields.Many2one(
        comodel_name="account.account",
        string="Accrued Expense Tax Account",
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
    )
