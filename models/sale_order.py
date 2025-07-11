from odoo import models, api
import json
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_order_line(self):
        
        
        # Guardar JSON original antes de ejecutar el onchange base
        original_items = {}
        for line in self.order_line:
            if line.product_type == 'combo' and line.selected_combo_items:
                original_items[line.id] = line.selected_combo_items

        # Llama al método original para crear/actualizar líneas de combo
        super()._onchange_order_line()
        # Recorre cada línea de combo y ajusta la cantidad de sus ítems
        for line in self.order_line:
            if line.id in original_items:
                try:
                    selected = json.loads(original_items[line.id])
                except ValueError:
                    continue

                combo_qty = line.product_uom_qty
                # Filtrar líneas hijas vinculadas al combo o virtualmente
                children = self.order_line.filtered(
                    lambda l: (l.linked_line_id and l.linked_line_id.id == line.id)
                              or (l.linked_virtual_id and l.linked_virtual_id == line.virtual_id)
                )
                for child in children:
                    item_data = next(
                        (item for item in selected if item.get('combo_item_id') == child.combo_item_id.id),
                        None
                    )
                    if item_data and 'quantity' in item_data:
                        # Multiplica la cantidad del combo por la cantidad extra del ítem
                        child.product_uom_qty = combo_qty * item_data['quantity']
                # Limpiar para evitar recursividad
                line.selected_combo_items = False