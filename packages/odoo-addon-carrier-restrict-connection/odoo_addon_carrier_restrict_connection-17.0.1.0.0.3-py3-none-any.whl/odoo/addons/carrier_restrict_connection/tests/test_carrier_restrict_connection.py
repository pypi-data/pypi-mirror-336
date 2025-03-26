# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCarrierRestrictConnection(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shipping_id = cls.env.ref("delivery.free_delivery_carrier")
        cls.shipping_id.fixed_price = 10.0
        cls.picking_type_id = cls.env.ref("stock.picking_type_out")
        cls.partner_id = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.location_id = cls.env.ref("stock.stock_location_stock")
        cls.location_destination_id = cls.env.ref("stock.stock_location_customers")
        cls.product_id = cls.product_id = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )
        cls.picking_id = cls.env["stock.picking"].create(
            {
                "partner_id": cls.partner_id.id,
                "picking_type_id": cls.picking_type_id.id,
                "location_id": cls.location_id.id,
                "location_dest_id": cls.location_destination_id.id,
                "carrier_id": cls.shipping_id.id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_id.name,
                            "product_id": cls.product_id.id,
                            "product_uom": cls.product_id.uom_id.id,
                            "product_uom_qty": 1,
                            "quantity": 1,
                            "location_id": cls.location_id.id,
                            "location_dest_id": cls.location_destination_id.id,
                        },
                    )
                ],
            }
        )

    def test_1default(self):
        self.assertTrue(self.picking_type_id.set_carrier_connection)
        self.assertFalse(self.env.ref("stock.picking_type_in").set_carrier_connection)

    def test_carrier_connection(self):
        self.picking_id.button_validate()
        self.assertEqual(self.picking_id.carrier_price, 10.0)

    def test_carrier_no_connection(self):
        self.picking_type_id.set_carrier_connection = False
        self.picking_id.button_validate()
        self.assertEqual(self.picking_id.carrier_price, 0.0)
        self.assertEqual(self.picking_id.carrier_tracking_ref, False)
