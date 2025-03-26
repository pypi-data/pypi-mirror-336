# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    set_carrier_connection = fields.Boolean(
        compute="_compute_set_carrier_connection", store=True, readonly=False
    )

    @api.depends("code")
    def _compute_set_carrier_connection(self):
        for rec in self:
            rec.set_carrier_connection = rec.code == "outgoing"
