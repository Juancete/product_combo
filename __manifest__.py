{
    "name": "Product Combo Extension",
    "version": "18.0.1.0.0",
    "category": "Sales",
    'author': "Juan Contardo",
    "summary": "Permite modificar componentes de productos combo en Pedidos de Venta y Facturas",
    'description': """
        Este módulo hereda la vista de combos para agregar un campo de cantidad.
    """,
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_combo_views_inherit.xml",
    ],
    "installable": True,
    "application": False,
}
