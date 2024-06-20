from odoo import fields, models

class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking.line"

    def create_returns(self):
        return this._create_returns()
