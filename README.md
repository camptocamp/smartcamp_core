# Camptocamp Smartcamp OCA core addons

This repository contains the private fork of OCA addons that are supported by Camptocamp.
If a customer wants an addons that is not in the present repositry a request must be done via the suggestion box.

That is a full fork as we want to control the evolution of addons to avoid breacking changes in smartcamp projet.

Smartcampt projects are to be deployed only on the Odoo SH paltform.

Fixes done on this repository are meant if possible to be ported to official OCA Repository

# Extracting addons into repository

Update script extract_addons.py and change:

 * ODOO_SERIE
 * ADDONS_TO_EXTRACT
 * OCA_PROJECTS

and then run:
``` bash
 python3 script/extract_addons.py /home/nbessi/project/smartcamp_core/
 ```
 The script only uses standard lib so no dependencies. It takes as argument
 the path where you want to extract the addons.
 The script will override existing folder blindly.