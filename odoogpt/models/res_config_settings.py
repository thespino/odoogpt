# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    odoogpt_openai_api_key = fields.Char(
        string='OpenAI Api token',
        help="""Open AI Api token can be found at https://beta.openai.com/account/api-keys""",
        related='company_id.odoogpt_openai_api_key',
        default=False,
        required=False,
        readonly=False,
    )

    odoogpt_openai_model = fields.Char(
        string='OpenAI Model',
        help="""Open AI Model to use: https://beta.openai.com/docs/models/overview""",
        related='company_id.odoogpt_openai_model',
        default='text-davinci-003',
        required=True,
        readonly=False,
    )

    odoogpt_openai_max_tokens = fields.Integer(
        string='OpenAI Max tokens',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-max_tokens""",
        related='company_id.odoogpt_openai_max_tokens',
        default=150,
        required=True,
        readonly=False,
    )

    odoogpt_openai_temperature = fields.Integer(
        string='OpenAI Temperature',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-temperature""",
        related='company_id.odoogpt_openai_temperature',
        default=1,
        required=True,
        readonly=False,
    )


    # CHAT CUSTOMIZATION ===========================================================================

    odoogpt_chat_method = fields.Selection(
        string='Chat method',
        help="""Which method to use for chatting""",
        related='company_id.odoogpt_chat_method',
        default='completion',
        # TODO: will be deprecated, in favour of chat-completion
        required=False,
        readonly=False,
    )


    odoogpt_chat_system_message = fields.Text(
        string='System message',
        help="""The first message that is sent to ChatGPT to give context and instructions""",
        related='company_id.odoogpt_chat_system_message',
        default="""You give useful answers about Odoo ERP and give all requested information""",
        required=False,
        readonly=False,
    )


    odoogpt_openai_prompt_prefix = fields.Char(
        string='OpenAI Prompt prefix',
        help="""Prefix to send to all OpenAI Completition Api requests""",
        related='company_id.odoogpt_openai_prompt_prefix',
        default='In Odoo: ',
        required=False,
        readonly=False,
    )

    odoogpt_openai_prompt_suffix = fields.Char(
        string='OpenAI Prompt suffix',
        help="""Suffix to send to all OpenAI Completition Api requests""",
        related='company_id.odoogpt_openai_prompt_suffix',
        default=False,
        required=False,
        readonly=False,
    )


    def set_values(self):
        res = super().set_values()
        self.env.company.odoogpt_openai_api_key = self.odoogpt_openai_api_key
        self.env.company.odoogpt_openai_model = self.odoogpt_openai_model
        self.env.company.odoogpt_openai_max_tokens = self.odoogpt_openai_max_tokens
        self.env.company.odoogpt_openai_temperature = self.odoogpt_openai_temperature
        self.env.company.odoogpt_chat_method = self.odoogpt_chat_method
        self.env.company.odoogpt_chat_system_message = self.odoogpt_chat_system_message
        self.env.company.odoogpt_openai_prompt_prefix = self.odoogpt_openai_prompt_prefix
        self.env.company.odoogpt_openai_prompt_suffix = self.odoogpt_openai_prompt_suffix
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            odoogpt_openai_api_key = self.env.company.odoogpt_openai_api_key,
            odoogpt_openai_model = self.env.company.odoogpt_openai_model,
            odoogpt_openai_max_tokens = self.env.company.odoogpt_openai_max_tokens,
            odoogpt_openai_temperature = self.env.company.odoogpt_openai_temperature,
            odoogpt_chat_method = self.env.company.odoogpt_chat_method,
            odoogpt_chat_system_message = self.env.company.odoogpt_chat_system_message,
            odoogpt_openai_prompt_prefix = self.env.company.odoogpt_openai_prompt_prefix,
            odoogpt_openai_prompt_suffix = self.env.company.odoogpt_openai_prompt_suffix
        )
        return res


    def odoogpt_openai_test(self):
        """Call Models list api to check everything is properly set up"""
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        try:
            OdoogptOpenaiUtils.models_list()
        except Exception as ex:
            raise UserError(ex)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Test success!'),
                'message': _('Everything properly set up! You\'re good to go!'),
                'sticky': False,
            }
        }


    def odoogpt_openai_model_select_from_db(self):
        """Get Models from OpenAI api and show selector wizart"""
        self.env['odoogpt.openai.model'].sudo().refresh_from_api(format='model')
        return self.env.ref('odoogpt.odoogpt_openai_model_select_wizard_act_window').read()[0]

