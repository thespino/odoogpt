# -*- coding: utf-8 -*-
{
    'name': 'OdooGPT files',
    'summary': 'Manage OpenAI Files',
    'description': """Manage OpenAI Files""",
    'license': 'LGPL-3',
    'version': '0.0.1',
    'category': 'Productivity',
    'author': 'thespino',
    'website': 'https://github.com/thespino',

    'depends': [
        'odoogpt_base',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/odoogpt_openai_file.xml',

        'views/menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
