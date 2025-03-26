# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Carrier Restrict Connection",
    "summary": "Restrict carrier connection using picking types",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-delivery-carrier",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "stock_delivery",
    ],
    "data": [
        "views/stock_picking_views.xml",
    ],
}
