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
        self.ensure_one()
        # obtenemos la moneda para convertir
        currency = self.order_id.pricelist_id.currency_id
        date = self.order_id.date_order
        company = self.company_id

        # precio unitario del ítem (base + extra) convertido
        unit_price = currency._convert(
            from_amount=self.combo_item_id.lst_price + self.combo_item_id.extra_price,
            to_currency=self.currency_id,
            company=company,
            date=date,
        )
        # devolvemos precio total de esa línea: unit_price * qty
        return unit_price 