# Copyright 2021 Camptocamp SA
{
    "name": "Payment Provider: Wallee",
    "summary": "A Swiss payment provider.",
    "version": "16.0.1.0.0",
    "category": "Accounting/Payment Providers",
    "website": "https://www.camptocamp.com",
    "author": "Camptocamp",
    "license": "OPL-1",
    "installable": True,
    "external_dependencies": {"python": ["wallee"]},
    "depends": ["payment"],
    "data": [
        "views/payment_provider.xml",
        "views/payment_provider_wallee_template.xml",
        "data/payment_provider.xml",
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
