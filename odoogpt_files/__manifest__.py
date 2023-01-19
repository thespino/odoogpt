# -*- coding: utf-8 -*-
{
    'name': 'OdooGPT files',
    'summary': 'Manage OpenAI Files',
    'description': """Manage OpenAI Files""",
    'license': 'LGPL-3',
    'version': '0.0.5',
    'price': '4.99',
    'category': 'Productivity',
    'author': 'thespino',
    'website': 'https://github.com/thespino',

    'depends': [
        'odoogpt_base',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/odoogpt_openai_file.xml',

        'wizard/odoogpt_openai_file_create_wizard.xml',

        'views/menu.xml',
    ],

    'images': [
        'static/description/cover/odoogpt_files.png',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
