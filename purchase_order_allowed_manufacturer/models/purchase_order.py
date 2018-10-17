# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    order_manufacturer_ids = fields.Many2many(comodel_name="manufacturer.line",
                                              string="Manufacturers")
    manufacturer_ids = fields.Many2many(comodel_name="manufacturer.line",
                                        string="Manufacturers",
                                        compute="_compute_manufacturers")

    @api.multi
    @api.depends("product_id.seller_ids")
    def _compute_manufacturers(self):
        for record in self:
            supplier_id = record.product_id.seller_ids.filtered(
                lambda x: x.name.id == record.partner_id.id)
            record.manufacturer_ids = supplier_id.manufacturer_ids.filtered(
                lambda x: x.approved)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('only_allowed_products', 'partner_id')
    def _compute_allowed(self):
        product_obj = self.env['product.template']
        for order in self:
            if order.only_allowed_products and order.partner_id:
                suppinfo = self.env['product.supplierinfo'].search(
                    [('name', 'in', (order.partner_id.commercial_partner_id.id,
                                     order.partner_id.id)),
                     ('approved', '=', True)])
                order.allowed_tmpl_ids = suppinfo.mapped(
                    'product_tmpl_id').filtered(
                        lambda x: x.purchase_ok)
            else:
                order.allowed_tmpl_ids = product_obj.search(
                    [('purchase_ok', '=', True)])
            order.allowed_product_ids =\
                order.mapped(
                    'allowed_tmpl_ids.product_variant_ids').filtered(
                        lambda x: x.purchase_ok
                        and any(x.seller_ids.mapped("approved")))
