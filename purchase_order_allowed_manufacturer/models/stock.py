# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    manufacturer_id = fields.Many2one(comodel_name="manufacturer.line",
                                      string="Manufacturer")


class StockQuant(models.Model):
    _inherit = "stock.quant"

    manufacturer_id = fields.Many2one(comodel_name='manufacturer.line',
                                      string="Manufacturer",
                                      related="lot_id.manufacturer_id",
                                      store=True)
