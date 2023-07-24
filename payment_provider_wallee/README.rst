==============
Payment Wallee
==============

This module adds implementation of Wallee as payment provider.

Wallee portal configuration
===========================

In the Wallee portal, you must create an `Application User` in
Account > Users > Application Users.

- You will need to keep its `User ID` and `Authentication Key` to do the settings
  on Odoo.

- You will need to assign a `User Role` for the newly created User to your `Space`.

In the Wallee portal, you must configure a `Webhook` for Wallee to notify Odoo
of transactions update in Space > Connect > Webhooks.

- You will need to create a `Webhook URL` to your Odoo instance with the suffix
  `payment/wallee/webhook` (e.g. https://myodooinstance.example.com/payment/wallee/webhook)

- You will need to create a `Webhook Listener` to the `Webhook URL` for the
  `Transaction` Entity.


Odoo configuration
==================

Go to Accounting > Configuration > Payment Providers and enable Wallee. You
then need to define following credentials:

- Wallee Space ID
- Wallee Application User ID
- Wallee Application User Auth Key

You can then proceed with the configuration and use Wallee as a payment provider.

Roadmap / Issues
================

* Cannot define supported payment icons according to currency (i.e. wallee offers postfinance and twint only for transactions in CHF, and wallee offers only visa + mastercard for other currencies. However you can set only a list of payment icons unrelated to the currency that will be displayed on the website)
* Payment Authorizations (for recurring transaction) or Payment Tokens (for registering card details) are not implemented
* The module actually seems to handle single transactions well but requires more functional testing, and probably some unit tests.
