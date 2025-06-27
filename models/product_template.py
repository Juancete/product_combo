from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_combo = fields.Boolean(
        string="¿Producto Combo?",
        help="Marcar si este producto es un combo/bundle."
    )
    combo_line_ids = fields.One2many(
        "product.combo.line", "combo_id", string="Componentes del Combo"
    )


class ProductComboLine(models.Model):
    _name = "product.combo.line"
    _description = "Línea de componente de producto Combo"

    combo_id = fields.Many2one(
        "product.template", string="Producto Combo", ondelete="cascade", required=True
    )
    product_id = fields.Many2one(
        "product.product", string="Componente", required=True
    )
    qty = fields.Float(
        string="Cantidad por unidad de combo", default=1.0, required=True
    )
