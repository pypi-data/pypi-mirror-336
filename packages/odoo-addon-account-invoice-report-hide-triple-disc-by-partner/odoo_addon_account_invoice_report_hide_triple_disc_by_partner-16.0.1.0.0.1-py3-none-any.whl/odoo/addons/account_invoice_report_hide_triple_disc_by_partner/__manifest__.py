# Copyright 2025 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Report Hide Triple Disc. by Partner",
    "summary": "Do not show triple discount in invoices",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://github.com/sygel-technology/sy-account-invoice-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_invoice_triple_discount",
        "account_invoice_report_hide_discounts_by_partner",
    ],
    "data": ["reports/report_invoice.xml"],
}
