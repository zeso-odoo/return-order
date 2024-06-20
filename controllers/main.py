from odoo import http, Command
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo import fields
from odoo.addons.portal.controllers.mail import _message_post_helper
import werkzeug
from collections import defaultdict


class CustomerPortalInherit(CustomerPortal):
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        print("called custom **********")

        order = request.website.sale_get_order()
        request.session['sale_last_order_id'] = order.id
        sale_order_id = request.session.get('sale_last_order_id')
        product_id = request.session.get('product_id')
        quantity = request.session.get('quantity')
        print("sale order id:",sale_order_id)
        print("Order ::",order.id)
        values = self._return_order_confirmation(order,product_id,quantity)

        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_quote_%s' % order_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': order_sudo.user_id.partner_id.lang or order_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', order_sudo.partner_id.name if request.env.user._is_public() else request.env.user.partner_id.name)
                del context
                _message_post_helper(
                    "sale.order",
                    order_sudo.id,
                    message=msg,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={order_sudo._name}'\
                      f'&id={order_sudo.id}'\
                      f'&action={order_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'sale_order': order_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': order_sudo.company_id,  # Used to display correct company logo
        }

        # Payment values
        if order_sudo._has_to_be_paid():
            values.update(self._get_payment_values(order_sudo))

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history_session_key = 'my_quotations_history'
        else:
            history_session_key = 'my_orders_history'

        values = self._get_page_view_values(
            order_sudo, access_token, values, history_session_key, False)

        return request.render('sale.sale_order_portal_template', values)

    def _return_order_confirmation(self,order,product_id,quantity):
        if self:
            existing_wizard = order.env['stock.return.picking.line']
            print("Existing Wizard ::",existing_wizard)
            print("Sale order id ::", order.id)
            print("Product :",order.product_id.id)
            print("Quantity :",quantity)

            if not existing_wizard:
                return_order_wizard = order.env['stock.return.picking.line'].sudo().create({
                    'sale_order_id': order,
                    'product_id': product_id,
                    'quantity': quantity
                })
                return_order_wizard.create_returns()
    # @http.route('/my/orders/<int:order_id>', type='json', auth='public', website=True, csrf=False)
    # def return_order_confirmation(self):
    #     print("******* controller called *******")
    #     sale_order_id = request.session.get('order_id')
    #     product_id = request.session.get('product_id')
    #     quantity = request.session.get('quantity')

    #     if sale_order_id:
    #         order = request.env['sale.order'].sudo().browse(sale_order_id)
    #         # for line in order.order_line:
    #         #     original_price = self.original_product_prices.get(line.id, line.price_unit)
    #         #     line.write({'price_unit': original_price})
    #         # values = self._prepare_shop_payment_confirmation_values(order)
    #         # values['product_id'] = product_id 
    #         # values['quantity'] = quantity
    #         self._prepare_order(order,product_id, quantity)
    #         # return request.render("website_sale.confirmation", values)
    #     # else:
    #     #     return request.redirect('/shop')

    # def _prepare_order(self, product_id, quantity):
    #     print("******* method call ************")
    #     existing_wizard = self.env['stock.return.picking']
    #     if  existing_wizard:
    #             return_order_wizard = self.env['stock.return.picking'].sudo().create({
    #             'product_id': product_id,
    #             'quantity': quantity,
    #             })
    #             return_order_wizard.create_returns()

