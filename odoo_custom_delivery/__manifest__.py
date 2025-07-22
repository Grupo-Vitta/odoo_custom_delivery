{
    'name': 'Método de Envío Personalizado',
    'version': '1.0',
    'category': 'Delivery',
    'summary': 'Tarifas de envío por peso y zona (AMBA / Interior)',
    'depends': ['delivery', 'sale'],
    'data': [
        'views/delivery_rate_view.xml',
        'data/delivery_rate_data.xml',
    ],
    'installable': True,
    'application': False,
}