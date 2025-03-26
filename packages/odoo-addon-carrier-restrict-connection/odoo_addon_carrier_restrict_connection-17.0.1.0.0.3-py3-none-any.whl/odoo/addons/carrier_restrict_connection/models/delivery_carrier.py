# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    def send_shipping(self, pickings):
        self.ensure_one()
        res = []
        for picking in pickings:
            if picking.picking_type_id.set_carrier_connection:
                res = res + super().send_shipping(picking)
            else:
                res = res + [{"exact_price": 0.0, "tracking_number": False}]
        return res
