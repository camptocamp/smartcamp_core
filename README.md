# Camptocamp Smartcamp OCA core addons

This repository contains the private fork of OCA addons that are supported by Camptocamp.
If a customer wants an addon that is not in the present repositry a request must be done via the suggestion box.

That is a full fork as we want to control the evolution of addons to avoid breaking changes in Smartcamp projet.

Smartcamp projects are to be deployed only on the Odoo SH platform.

Fixes done on this repository should be ported to official OCA Repositories.

# Extracting addons into repository

Update script extract_addons.py and change:

 * ODOO_SERIE
 * ADDONS_TO_EXTRACT

and then run:

```bash
python3 script/extract_addons.py /path/to/local/checkout/of/smartcamp_core/
```

To add/refresh only some repo use `--repo-whitelist repo1, repo2, repo3`.

The script only uses standard lib so no dependencies.
It takes as argument the path where you want to extract the addons.
The script will override existing folder blindly.
