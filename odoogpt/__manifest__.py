# -*- coding: utf-8 -*-
{
    'name': 'OdooGPT',
    'summary': 'Make OdooBot finally useful',
    'description': """Make OdooBot useful by adding GPT intelligence 🧠""",
    'license': 'LGPL-3',
    'version': '0.0.7',
    'category': 'Productivity/Discuss',
    'author': 'thespino',
    'website': 'https://github.com/thespino',

    'depends': [
        'odoogpt_base',
        'mail_bot',
    ],

    'data': [
        'views/res_config_settings.xml',
    ],

    'assets': {
        'mail.assets_messaging': [
            'odoogpt/static/src/models/*.js',
        ],
    },

    'installable': True,
    'auto_install': False,
    'application': False,
}
