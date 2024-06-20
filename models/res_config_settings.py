from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_sale_enabled_portal_return_order_button = fields.Boolean(string="Return Order From Portal",related='website_id.enabled_portal_return_order_button',readonly=False)
 