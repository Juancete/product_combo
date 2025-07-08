{
    "name": "Product Combo Extension",
    "version": "18.0.1.0.0",
    "category": "Sales",
    'author': "Juan Contardo",
    "summary": "Permite modificar componentes de productos combo en Pedidos de Venta y Facturas",
    'description': """
        Este módulo hereda la vista de combos para agregar un campo de cantidad.
    """,
    "depends": ["product", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_combo_views_inherit.xml",
    ],
    'assets': {
      'web.assets_backend': [
          'sale.assets_backend', # <--- ADD THIS LINE
          'product_combo/static/src/js/sale_combo_field_extension.js',
          'product_combo/static/src/xml/combo_configurator_dialog_extension.xml',
          'product_combo/static/src/js/combo_configurator_dialog_extension.js',
      ]
    },
    "installable": True,
    "application": False,
} # type: ignore
