# -*- coding: utf-8 -*-
{
    'name': "SUNAT TC",

    'summary': """
       - Actualiza el TC de moneda UDS desde sunat
       - Actualiza TC todos los dias""",

    'description': """
    """,

    'author': "Tagre System",
    'website': "https://tagre.app",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'iap'],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        'views/currency_rate_wizard.xml',
        'views/res_currency_views.xml',
    ],
}
