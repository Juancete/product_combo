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
