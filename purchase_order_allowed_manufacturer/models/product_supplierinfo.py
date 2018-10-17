# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models

date2string = fields.Date.to_string


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    approved = fields.Boolean(string="Approved",
                              compute="_compute_approved_supplier")
    manufacturer_ids = fields.Many2many(
        comodel_name="manufacturer.line", string="Manufacturer lines")

    @api.multi
    @api.depends("manufacturer_ids")
    def _compute_approved_supplier(self):
        for record in self:
            record.approved = any(
                [x.approved for x in record.manufacturer_ids] or [True])


class ManufacturerLine(models.Model):
    _name = "manufacturer.line"

    name = fields.Char(string="Manufacturer")
    approved = fields.Boolean(string="Approved",
                              compute="_compute_approved_manufacturer")
    approval_start_date = fields.Date(string="Approval start date")
    approval_end_date = fields.Date(string="Approval end date")
    active = fields.Boolean(string="Active", default=True)


    @api.multi
    @api.depends('approval_start_date', 'approval_end_date')
    def _compute_approved_manufacturer(self):
        for record in self:
            today = fields.Date.today()
            start_date = record.approval_start_date
            end_date = record.approval_end_date or today
            record.approved = start_date <= today <= end_date
