{
    'name': "Disable Sent Purchase Order",
    'summary': """
        """,

    'description': """
        - Hide sent RFQ to customers on PO
        - Hide print button on header PO
    """,

    'author': "Amirul M.",
    'website': "http://linkedin.com/in/amirulm",
    'category': 'Extra Tools',
    'version': '15.0.1.0.0',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_view.xml',
    ],
}