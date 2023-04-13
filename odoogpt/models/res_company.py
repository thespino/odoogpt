# -*- coding: utf-8 -*-
import importlib.metadata
import openai
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'


    @api.constrains('odoogpt_chat_method')
    def _check_odoogpt_chat_method(self):
        if any(company.odoogpt_chat_method == 'chat-completion' for company in self) and not hasattr(openai, 'ChatCompletion'):
            raise ValidationError(_("""OdooGPT: We're sorry, ChatCompletion is not available in your system. 
Check that openai python module version is >= 0.27.0 to use this functionality; otherwise, set "Chat method" in OdooGPT settings to "Completion". 
Installed version: {openai_version} 
See https://github.com/openai/openai-python/releases/tag/v0.27.0""").format(
                openai_version=str(importlib.metadata.version('openai'))
            ))


    odoogpt_openai_api_key = fields.Char(
        string='OpenAI Api token',
        help="""Open AI Api token can be found at https://beta.openai.com/account/api-keys""",
        default=False,
        required=False,
    )

    odoogpt_openai_model = fields.Char(
        string='OpenAI Model',
        help="""Open AI Model to use: https://beta.openai.com/docs/models/overview""",
        default='text-davinci-003',
        required=True,
    )

    odoogpt_openai_max_tokens = fields.Integer(
        string='OpenAI Max tokens',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-max_tokens""",
        default=150,
        required=True,
    )

    odoogpt_openai_temperature = fields.Integer(
        string='OpenAI Temperature',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-temperature""",
        default=1,
        required=True,
    )


    # CHAT CUSTOMIZATION ===========================================================================

    odoogpt_chat_method = fields.Selection(
        string='Chat method',
        help="""Which method to use for chatting""",
        selection=[
            ('completion', 'Completion'),
            ('chat-completion', 'Chat Completion'),
        ],
        default='completion',
        # TODO: will be deprecated, in favour of chat-completion
        required=False,
    )


    odoogpt_chat_system_message = fields.Text(
        string='System message',
        help="""The first message that is sent to ChatGPT to give context and instructions""",
        default="""You give useful answers about Odoo ERP and give all requested information""",
        required=False,
    )


    odoogpt_openai_prompt_prefix = fields.Char(
        string='OpenAI Prompt prefix',
        help="""Prefix to send to all OpenAI Completition Api requests""",
        default='In Odoo: ',
        required=False,
    )

    odoogpt_openai_prompt_suffix = fields.Char(
        string='OpenAI Prompt suffix',
        help="""Suffix to send to all OpenAI Completition Api requests""",
        default=False,
        required=False,
    )
