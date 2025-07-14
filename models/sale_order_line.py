from odoo import models
import logging

_logger = logging.getLogger(__name__)

def _sum_individual_combo_prices(self):
    # Suma extra_price de cada combo_item en lugar de prorratear
    return sum(
        item.extra_price + item.base_price_converted()  # asume método para convertir base
        for item in self.product_template_id.combo_ids
        if item.id == self.combo_item_id.id
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_combo_item_display_price(self):
        _logger.warning("LA CONCHA DE TU MADRES!!")
        # Reemplazamos cálculo proporcional por suma directa
        # Suma los valores base y extra de cada ítem
        price = self.combo_item_id.extra_price
        # Obtenemos todos los combos del template con su base_price en currency
        template = self.product_template_id
        currency = self.order_id.pricelist_id.currency_id
        prices = []
        for item in template.combo_ids:
            base = currency._convert(
                from_amount=item.base_price,
                to_currency=self.currency_id,
                company=self.company_id,
                date=self.order_id.date_order,
            )
            prices.append(base + item.extra_price)
        # Devolvemos la suma de todos o solo del ítem actual
        return sum(prices)