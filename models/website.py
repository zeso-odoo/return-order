from odoo import fields, models

class Website(models.Model):
    _inherit = 'website'

    enabled_portal_return_order_button = fields.Boolean(string="Return Order From Portal") 
