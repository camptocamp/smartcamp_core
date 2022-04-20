# Quick and dirty script to manually get some addons all OCA addons
# To remove once module analysis install on all our instances
from pathlib import Path
import os
import tempfile
import shutil
import argparse

ODOO_SERIE = "15.0"
ADDONS_TO_EXTRACT = {
    # repo: (addon1, addon2, ...)
    "bank-statement-import": (
        "account_bank_statement_import_transfer_move",
    ),
    "account-closing": (
        "account_cutoff_accrual_picking",
        "account_cutoff_base",
        "account_invoice_start_end_dates",
    ),
    "account-financial-reporting": (
        "account_financial_report",
    ),
    "bank-statement-import": (
        "account_statement_import",
        "account_statement_import_camt",
        "account_statement_import_camt54",
        # still not migrated to v14 and to be account_statement_import_transfer_move
        # "account_bank_statement_import_transfer_move",
    ),
    "reporting-engine": (
        "bi_sql_editor",
        "report_wkhtmltopdf_param",
        "report_xlsx",
    ),
    "server-ux": (
        "date_range",
        "mass_editing",
    ),
    "social": (
        "mail_outbound_static",
    ),
    "mis-builder": (
        "mis_builder",
        "mis_builder_budget",
    ),
    "server-tools": (
        "sql_request_abstract",
    ),
    "web": (
        "web_advanced_search",
    ),
}

def get_parser():
    parser = argparse.ArgumentParser(
        description="Fetch OCA addons to put in smartcamp"
    )
    parser.add_argument(
        "destination_path", type=Path, help="Folder to gather the addons"
    )
    parser.add_argument(
        "--repo-whitelist", default="",
        help="Comma separated list of repos to fetch. "
        "Useful when you want to add new addons or refresh only a few."
    )
    return parser


def fetch_addons(odoo_serie, addons_to_extract, destination_path):
    addons_control = []
    for addons_group in addons_to_extract.values():
        addons_control.extend(list(addons_group))
    with tempfile.TemporaryDirectory() as fp:
        for repo, addons in addons_to_extract.items():
            repo_path = Path(fp, repo)
            command = "git clone --depth=1 --branch={} --single-branch ssh://git@github.com/oca/{}.git {}".format(
                odoo_serie, repo, repo_path
            )
            os.system(command)
            for addon in addons:
                addon_path = repo_path / addon
                if addon_path.is_dir():
                    # I prefer to use shutil instead on Pathlib replace
                    print("Getting {} from repo {}".format(addon, repo))
                    if (destination_path / addon).is_dir():
                        shutil.rmtree(str(destination_path / addon))
                    shutil.move(str(addon_path), str(destination_path))
                    addons_control.remove(addon)
    if addons_control:
        print(
            "The following addons were not found: ",
            ", ".join(addons_control)
        )

def main(serie, addons_to_extract):
    parser = get_parser()
    arguments = parser.parse_args()
    destination_path = arguments.destination_path
    if not destination_path.is_dir():
        raise ValueError("The destination path must be an existing directory")

    repo_whitelist = [x.strip() for x in (arguments.repo_whitelist or "").split(",") if x.strip()]
    if repo_whitelist:
        addons_to_extract = {k: v for k,v in addons_to_extract.items() if k in repo_whitelist}
        print("Updating only repo(s): ", repo_whitelist)
    fetch_addons(serie, addons_to_extract, destination_path)


if __name__ == "__main__":  # pragma: no cover
    serie = ODOO_SERIE
    addons_to_extract = ADDONS_TO_EXTRACT.copy()
    main(serie, addons_to_extract)
