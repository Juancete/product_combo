{
    "name": "Producto Combo Extensión",
    "version": "18.0.1.0.0",
    "category": "Sales",
    'author': "Juan Contardo",
    "summary": "Permite modificar componentes de productos combo en Pedidos de Venta y Facturas",
    'description': """
        Este módulo hereda la vista de combos para agregar un campo de cantidad.
    """,
    "depends": ["base", "product", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_combo_views_inherit.xml",
        "views/combo_configurator_inherit.xml",
    ],
    'assets': {
        'web.assets_backend': [
            # Your JavaScript file for patching the component
            'static/src/js/combo_configurator_dialog_extension.js',
            # Your QWeb template inheritance file MUST be here
            'static/src/xml/combo_configurator_dialog_view_inherit.xml',
            # Add any other frontend assets (like CSS) here
            # 'product_combo/static/src/scss/my_custom_styles.scss',
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
