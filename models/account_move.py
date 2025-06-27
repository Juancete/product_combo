from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    combo_line_ids = fields.One2many(
        "account.move.line.combo", "move_line_id", string="Componentes", copy=True
    )

    @api.onchange("product_id")
    def _onchange_product_id_combo(self):
        res = super()._onchange_product_id()
        if self.product_id.product_tmpl_id.is_combo:
            self.combo_line_ids = [(5, 0, 0)]
            for comp in self.product_id.product_tmpl_id.combo_line_ids:
                self.combo_line_ids += [(0, 0, {
                    "product_id": comp.product_id.id,
                    "quantity": comp.qty * (self.quantity or 1),
                })]
        return res

    @api.onchange("quantity")
    def _onchange_quantity_combo(self):
        for line in self:
            if line.product_id.product_tmpl_id.is_combo:
                for comp in line.combo_line_ids:
                    base = next(
                        (c.qty for c in line.product_id.product_tmpl_id.combo_line_ids
                         if c.product_id.id == comp.product_id.id),
                        0
                    )
                    comp.quantity = base * line.quantity


class AccountMoveLineCombo(models.Model):
    _name = "account.move.line.combo"
    _description = "Componente en Línea de Factura"

    move_line_id = fields.Many2one(
        "account.move.line", string="Línea de Factura", ondelete="cascade", required=True
    )
    product_id = fields.Many2one(
        "product.product", string="Componente", required=True
    )
    quantity = fields.Float(string="Cantidad", default=1.0, required=True)
