{
    "name": "Product Combo Extension",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Permite modificar componentes de productos combo en Pedidos de Venta y Facturas",
    "depends": ["product", "sale", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
}
