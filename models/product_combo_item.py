from odoo import models, fields

class ProductComboItem(models.Model):
    _inherit = 'product.combo'

    quantity = fields.Integer(
        string='Cantidad',
        default=1,
        help='Número de unidades de este producto',
    )