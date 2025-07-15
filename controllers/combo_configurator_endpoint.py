from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.combo_configurator import SaleComboConfiguratorController

class SaleComboConfiguratorControllerOverride(SaleComboConfiguratorController):

    # @http.route('/sale/combo_configurator/get_data', type='json', auth='user', website=True)
    @http.route()
    def sale_combo_configurator_get_data(self, product_tmpl_id, **kwargs):
        result = super().sale_combo_configurator_get_data(product_tmpl_id, **kwargs)

        for combo in result.get('combos', []):
            combo_id = combo.get('id')
            combo_record = request.env['product.combo'].sudo().browse(combo_id)
            combo['quantity'] = combo_record.quantity
        
        return result

    @http.route('/sale/combo_configurator/add_lines', type='json', auth='user', methods=['POST'], csrf=False)
    def add_lines(self, sale_order_id, combo_line_id, selected_combo_items, **kwargs):
        # 1) Llamamos al add_lines original, que crea las líneas hijas
        new_line_ids = super().add_lines(
            sale_order_id, combo_line_id, selected_combo_items, **kwargs
        )
        # 2) Recuperamos el pedido y la línea combo
        sale_order = request.env['sale.order'].browse(sale_order_id)
        combo_line = sale_order.order_line.browse(combo_line_id)
        # 3) Para cada item venido en el JSON, reescribimos price_unit
        for sci in selected_combo_items:
            # tu front envía: { combo_item_id, price, quantity, … }
            price = sci.get('price')
            if price is None:
                continue
            # buscamos la línea hija que corresponda
            line = sale_order.order_line.filtered(lambda l:
                l.linked_line_id and l.linked_line_id.id == combo_line.id
                and l.combo_item_id.id == sci.get('combo_item_id')
            )
            if line:
                # sudo() por si acaso; sobreescribimos el unit price
                line.sudo().write({'price_unit': price})
        return new_line_ids
        
    def _get_combo_item_data(
        self, combo, combo_item, selected_combo_item, date, currency, pricelist, **kwargs
    ):
        result = super()._get_combo_item_data(combo, combo_item, selected_combo_item, date, currency, pricelist, **kwargs)
        result['product']['price'] = combo_item.lst_price
        return result