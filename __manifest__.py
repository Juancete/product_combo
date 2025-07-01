{
    "name": "Producto Combo Extensión",
    "version": "18.0.1.0.0",
    "category": "Sales",
    'author': "Juan Contardo",
    "summary": "Permite modificar componentes de productos combo en Pedidos de Venta y Facturas",
    'description': """
        Este módulo hereda la vista de combos para agregar un campo de cantidad.
    """,
    "depends": ["base", "product", "product_combo", "sale"]
    "data": [
        "security/ir.model.access.csv",
        "views/product_combo_views_inherit.xml",
        "static/src/xml/combo_configurator_dialog_view_inherit.xml"
        "views/combo_configurator_inherit.xml",
    ],
    'assets': { # Esta sección es para los archivos JavaScript y otros assets
        'web.assets_backend': [
            "tu_modulo_custom/static/src/js/combo_configurator_dialog_extension.js",
            # Puedes añadir tus archivos CSS si los tienes:
            # 'tu_modulo_custom/static/src/scss/my_custom_styles.scss',
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
