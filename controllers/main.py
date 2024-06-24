from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/my/orders/<int:order_id>', type='json', auth='user', website=True)
    def create_returns(self):
        print("*********** controller call ***********")
        picking_line = request.env['stock.return.picking'].create({})
        result = picking_line._create_returns()
        return result
