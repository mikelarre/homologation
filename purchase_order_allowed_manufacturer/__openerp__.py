# -*- coding: utf-8 -*-
# © Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Allowed manufacturer products on purchase order",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "purchase_order_allowed_product",
        "stock",
    ],
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Odoo Community Association (OCA)",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Purchase",
    "summary": "",
    "data": [
        "security/ir.model.access.csv",
        "wizard/stock_transfer_details_view.xml",
        "views/product_supplierinfo_view.xml",
        "views/purchase_order_view.xml",
        "views/stock_view.xml",
    ],
    "installable": True,
}
