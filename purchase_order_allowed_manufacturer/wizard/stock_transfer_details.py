# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class TransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    manufacturer_id = fields.Many2one(comodel_name="manufacturer.line",
                                      string='Manufacturer')
    possible_manufacturer_ids = fields.Many2many(
        comodel_name="manufacturer.line",
        compute="_compute_possible_manufacturers",
        string="Possible manufacturer")

    @api.multi
    @api.depends("transfer_id.picking_id.move_lines")
    def _compute_possible_manufacturers(self):
        for record in self:
            moves = record.transfer_id.picking_id.move_lines.filtered(
                lambda x: x.product_id == record.product_id)
            purchase_line = moves.mapped("purchase_line_id")[:1]
            record.possible_manufacturer_ids = \
                purchase_line.order_manufacturer_ids


class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        super(StockTransferDetails, self).do_detailed_transfer()
        for line in self.item_ids:
            line.lot_id.manufacturer_id = line.manufacturer_id
