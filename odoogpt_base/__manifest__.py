# -*- coding: utf-8 -*-
{
    'name': 'OdooGPT base',
    'summary': 'Base addon with utils to make OdooGPT work fine',
    'description': """Base addon with utils to make OdooGPT work fine""",
    'license': 'LGPL-3',
    'version': '0.0.3',
    'category': 'Productivity',
    'author': 'thespino',
    'website': 'https://github.com/thespino',

    'depends': [
        'base',
        'base_setup'
    ],
    'external_dependencies': {
        'python': [
            'openai'
        ]
    },

    'data': [
        'security/ir.model.access.csv',

        'views/res_config_settings.xml',
        'views/odoogpt_openai_model.xml',
        'views/odoogpt_openai_log.xml',

        'wizard/odoogpt_openai_model_select_wizard.xml',

        'views/menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
