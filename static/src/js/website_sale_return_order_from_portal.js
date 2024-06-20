/** @odoo-module **/

import tour from 'web_tour.tour';
import wsTourUtils from 'website_sale.tour_utils';
import wTourUtils from 'website.tour_utils';

tour.register('website_sale_return_order_from_portal', {
        test: true,
        url: '/my/orders',
    },
    [
        // Initial reorder, nothing in cart
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_return_order_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_return_order_confirm'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 1",
            trigger: ".js_quantity[value='1']",
        },
        // Second reorder, add reorder to cart
        {
            content: "Go back to my orders",
            trigger: "body",
            run: () => {
                window.location = "/my/orders";
            }
        },
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_return_order_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_return_order_confirm'),
        wTourUtils.clickOnElement('No', 'button:contains(No)'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 2",
            trigger: ".js_quantity[value='2']",
        },
        // Third reorder, clear cart and reorder
        {
            content: "Go back to my orders",
            trigger: "body",
            run: () => {
                window.location = "/my/orders";
            }
        },
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_return_order_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_return_order_confirm'),
        wTourUtils.clickOnElement('Yes', 'button:contains(Yes)'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 1",
            trigger: ".js_quantity[value='1']",
        },
    ]
);
