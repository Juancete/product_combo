from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    combo_line_ids = fields.One2many(
        "sale.order.line.combo", "order_line_id", string="Componentes", copy=True
    )

    @api.onchange("product_id")
    def _onchange_product_id_combo(self):
        res = super()._onchange_product_id()
        if self.product_id.product_tmpl_id.is_combo:
            # Reinicializa líneas hijas
            self.combo_line_ids = [(5, 0, 0)]
            for comp in self.product_id.product_tmpl_id.combo_line_ids:
                self.combo_line_ids += [(0, 0, {
                    "product_id": comp.product_id.id,
                    "quantity": comp.qty * (self.product_uom_qty or 1),
                })]
        return res

    @api.onchange("product_uom_qty")
    def _onchange_uom_qty_combo(self):
        for line in self:
            if line.product_id.product_tmpl_id.is_combo:
                for comp in line.combo_line_ids:
                    # Recupera cantidad base definida en template
                    base = next(
                        (c.qty for c in line.product_id.product_tmpl_id.combo_line_ids
                         if c.product_id.id == comp.product_id.id),
                        0
                    )
                    comp.quantity = base * line.product_uom_qty


class SaleOrderLineCombo(models.Model):
    _name = "sale.order.line.combo"
    _description = "Componente en Línea de Pedido de Ventas"

    order_line_id = fields.Many2one(
        "sale.order.line", string="Línea de Pedido", ondelete="cascade", required=True
    )
    product_id = fields.Many2one(
        "product.product", string="Componente", required=True
    )
    quantity = fields.Float(string="Cantidad", default=1.0, required=True)
