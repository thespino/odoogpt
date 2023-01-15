# -*- coding: utf-8 -*-
{
    'name': 'OdooGPT fine tune',
    'summary': 'Fine tune OpenAI models',
    'description': """Fine tune OpenAI models""",
    'license': 'LGPL-3',
    'version': '0.0.1',
    'category': 'Productivity',
    'author': 'thespino',
    'website': 'https://github.com/thespino',

    'depends': [
        'odoogpt_base',
        'odoogpt_files',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/odoogpt_openai_fine_tune.xml',

        'views/menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}