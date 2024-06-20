# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # Information
    'name': "Return Order",
    'summary': "You can return your order as well",

    # Author
    'author': "Odoo PS",
    'website': "http://www.odoo.com",
    'category': 'Customization',
    'version': '16.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'website','sale', 'website_sale', 'stock'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'return_order/static/src/js/website_sale_return_order.js',
            # 'return_order/static/src/js/website_sale_return_order_from_portal.js',
            'return_order/static/src/xml/website_sale_return_order_modal.xml',
        ]
    },
    'installable': True,
    'auto_install': False,
}
