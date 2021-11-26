# Quick and dirty script to manually get some addons all OCA addons
# To remove once module analysis install on all our instances
from pathlib import Path
import os
import tempfile
import shutil
import argparse

ODOO_SERIE = "14.0"

OCA_PROJECTS = (
    "account-analytic",
    "account-budgeting",
    "account-closing",
    "account-consolidation",
    "account-financial-reporting",
    "account-financial-tools",
    "account-fiscal-rule",
    "account-invoice-reporting",
    "account-invoicing",
    "account-payment",
    "account-reconcile",
    "bank-payment",
    "bank-statement-import",
    "business-requirement",
    "carrier-delivery",
    "commission",
    "community-data-files",
    "connector-accountedge",
    "connector-cmis",
    "connector-ecommerce",
    "connector-infor",
    "connector-jira",
    "connector-lengow",
    "connector-lims",
    "connector-magento",
    "connector-odoo2odoo",
    "connector-prestashop",
    "connector-redmine",
    "connector-sage",
    "connector-salesforce",
    "connector-spscommerce",
    "connector-woocommerce",
    "connector",
    "contract",
    "credit-control",
    "crm",
    "currency",
    "data-protection",
    "ddmrp",
    "department",
    "dms",
    "e-commerce",
    "edi",
    "event",
    "field-service",
    "fleet",
    "geospatial",
    "hr-attendance",
    "hr-expense",
    "hr-holidays",
    "hr",
    "infrastructure-dns",
    "interface-github",
    "intrastat",
    "iot",
    "knowledge",
    # "l10n-argentina",
    # "l10n-austria",
    # "l10n-belarus",
    # "l10n-belgium",
    # "l10n-brazil",
    # "l10n-cambodia",
    # "l10n-canada",
    # "l10n-chile",
    # "l10n-china",
    # "l10n-colombia",
    # "l10n-costa-rica",
    # "l10n-croatia",
    # "l10n-ecuador",
    # "l10n-estonia",
    # "l10n-ethiopia",
    # "l10n-finland",
    "l10n-france",
    "l10n-germany",
    # "l10n-greece",
    # "l10n-india",
    # "l10n-indonesia",
    # "l10n-iran",
    # "l10n-ireland",
    # "l10n-italy",
    # "l10n-japan",
    # "l10n-luxemburg",
    # "l10n-macedonia",
    # "l10n-mexico",
    # "l10n-morocco",
    # "l10n-netherlands",
    # "l10n-norway",
    # "l10n-peru",
    # "l10n-poland",
    # "l10n-portugal",
    # "l10n-romania",
    # "l10n-russia",
    # "l10n-slovenia",
    # "l10n-spain",
    "l10n-switzerland",
    # "l10n-taiwan",
    # "l10n-thailand",
    # "l10n-turkey",
    # "l10n-united-kingdom",
    # "l10n-uruguay",
    # "l10n-usa",
    # "l10n-venezuela",
    # "l10n-vietnam",
    "management-system",
    "manufacture-reporting",
    "manufacture",
    "margin-analysis",
    "mis-builder",
    "multi-company",
    "operating-unit",
    "partner-contact",
    "pms",
    "product-attribute",
    "product-kitting",
    "product-pack",
    "product-variant",
    "program",
    "project-agile",
    "project-reporting",
    "project-service",
    "purchase-reporting",
    "purchase-workflow",
    "queue",
    "report-print-send",
    "reporting-engine",
    "rest-framework",
    "rma",
    "sale-financial",
    "sale-reporting",
    "sale-workflow",
    "search-engine",
    "server-auth",
    "server-backend",
    "server-brand",
    "server-env",
    "server-tools",
    "server-ux",
    "social",
    "stock-logistics-barcode",
    "stock-logistics-reporting",
    "stock-logistics-tracking",
    "stock-logistics-warehouse",
    "stock-logistics-workflow",
    "storage",
    "survey",
    "timesheet",
    "vertical-association",
    "vertical-construction",
    "vertical-edition",
    "vertical-education",
    "vertical-hotel",
    "vertical-isp",
    "vertical-medical",
    "vertical-ngo",
    "vertical-realstate",
    "vertical-travel",
    "web",
    "webhook",
    "webkit-tools",
    "website-cms",
    "website",
    "wms",
)

ADDONS_TO_EXTRACT = (
    "account_bank_statement_import_transfer_move",
    "account_cutoff_accrual_picking",
    "account_cutoff_base",
    "account_invoice_start_end_dates",
    "account_financial_report",
    "account_statement_import",
    "account_statement_import_camt",
    "account_statement_import_camt54",
    "bi_sql_editor",
    "date_range",
    "mass_editing",
    "mail_outbound_static",
    "mis_builder",
    "mis_builder_budget",
    "report_wkhtmltopdf_param",
    "report_xlsx",
    "sql_request_abstract",
    "web_advanced_search",
)

parser = argparse.ArgumentParser(
    description="Fetch OCA addons to put in smartcampt"
)
parser.add_argument(
    "destination_path", type=Path, help="Folder to gather the addons"
)
arguments = parser.parse_args()
destination_path = arguments.destination_path
if not destination_path.is_dir():
    raise ValueError("The destination path must be an existing directory")
addons_control = list(ADDONS_TO_EXTRACT)
with tempfile.TemporaryDirectory() as fp:
    for project in OCA_PROJECTS:
        project_path = Path(fp, project)
        command = "git clone --depth=1 --branch={} ssh://git@github.com/oca/{}.git {}".format(
            ODOO_SERIE, project, project_path
        )
        os.system(command)
        for addon in ADDONS_TO_EXTRACT:
            addon_path = project_path / addon
            if addon_path.is_dir():
                # I prefer to use shutil instead on Pathlib replace
                print("getting {} from project {}".format(addon, project))
                if (destination_path / addon).is_dir():
                    shutil.rmtree(str(destination_path / addon))
                shutil.move(str(addon_path), str(destination_path))
                addons_control.remove(addon)

if addons_control:
    print(
        "the following addons where not found: {}".format(
            ", ".join(addons_control)
        )
    )
