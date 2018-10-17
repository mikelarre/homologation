# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests import common
from openerp import fields


class TestPurchaseContractSpecification(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseContractSpecification, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
            'supplier': True,
        })
        product_model = cls.env['product.product']
        cls.product1 = product_model.create({
            'name': 'Test Product 1',
            'purchase_ok': True,
        })
        cls.product2 = product_model.create({
            'name': 'Test Product 2',
            'purchase_ok': True,
        })
        cls.manufacturer = cls.env['manufacturer.line'].create({
            'name': 'Manufacturer to test',
            'approval_start_date': '2018-10-11',
        })
        cls.supplierinfo = cls.env['product.supplierinfo'].create({
            'name': cls.partner.id,
            'product_tmpl_id': cls.product1.product_tmpl_id.id,
            'manufacturer_ids': [(6, 0, [cls.manufacturer.id])]
        })

        cls.purchase_order = cls.env['purchase.order'].create({
            'partner_id': cls.partner.id,
            'pricelist_id': cls.env.ref('purchase.list0').id,
            'only_allowed_products': True,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
        })
        cls.purchase_line = cls.env['purchase.order.line'].create({
            'name': 'Purchase line test',
            'order_id': cls.purchase_order.id,
            'product_id': cls.product1.id,
            'price_unit': cls.product1.list_price,
            'date_planned': fields.Datetime.now(),
        })
        cls.env['stock.production.lot'].create({
            'name': 'Test lot',
            'product_id': cls.product1.id
        })
        cls.picking = cls.env['stock.picking'].create({
            'name': 'Test picking',
            'picking_type_id': cls.env.ref('stock.picking_type_in').id
        })
        cls.move = cls.env['stock.move'].create({
            'name': 'Test move',
            'purchase_line_id': cls.purchase_line.id,
            'picking_id': cls.picking.id,
            'product_uom': cls.product1.uom_id.id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'location_dest_id':  cls.env.ref('stock.stock_location_stock').id,
            'product_id': cls.product1.id,
        })
        cls.wiz = cls.env['stock.transfer_details']

    def test_purchase_allowed_manufacturer(self):
        self.assertTrue(self.supplierinfo.manufacturer_ids)

        self.wiz_inst = self.wiz.create({
            'picking_id': self.picking.id
        })
        # self.wiz_inst.with_context(
        #     active_model='stock.picking', active_ids=self.picking.id
        # ).default_get()
        # pass