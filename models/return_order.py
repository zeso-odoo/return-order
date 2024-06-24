from odoo import fields, models
from odoo.http import request

class ReturnOrder(models.Model):
    _name = 'return_order'
    _inherit = 'stock.return.picking'
    _description = "Return order from website"

    def prepare_order(self):
        print("*******************")

        sale_order_id = request.session.get('sale_last_order_id')
        product_id = request.env['stock.return.picking.line'].browse(product_id)
        quantity = request.env['stock.return.picking.line'].browse(quantity)

        print("sale order id",sale_order_id)
        print("product_id",product_id)
        print("quantity",quantity)
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
        
        print("Order :",order)
        self._create_return_order(order,product_id,quantity)


    def _create_return_order(self,order,product_id,quantity):
        existing_wizard = order.env['stock.return.picking'].sudo().search([('sale_order_ids','in',[order.id])],limit=1)
        print("Existing wizard",existing_wizard)
        if not existing_wizard:
            return_order_wizard = order.env['stock.return.picking'].sudo().new({
                'sale_order_ids': order,
                'product_id': product_id,
                'quantity': quantity
            })
            return_order_wizard.create_returns()

        # line = request.env['stock.return.picking.line'].search([
        #     ('product_id','=',10)
        #     # ('quantity','=', quantity)
        # ])
        # print("Picking line1 : ",line)
        # picking_line = request.env['stock.return.picking'].new({
        #     'picking_id': 40,
        #     'product_id': line[0].product_id
        #     # 'quantity': line[1].quantity
        # })
        # result = picking_line.create_returns()
        # return result
        # result = super()._create_returns()