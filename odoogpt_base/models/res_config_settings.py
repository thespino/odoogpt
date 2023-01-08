# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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


    def set_values(self):
        res = super().set_values()
        self.env.company.odoogpt_openai_api_key = self.odoogpt_openai_api_key
        self.env.company.odoogpt_openai_model = self.odoogpt_openai_model
        self.env.company.odoogpt_openai_max_tokens = self.odoogpt_openai_max_tokens
        self.env.company.odoogpt_openai_temperature = self.odoogpt_openai_temperature
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            odoogpt_openai_api_key = self.env.company.odoogpt_openai_api_key,
            odoogpt_openai_model = self.env.company.odoogpt_openai_model,
            odoogpt_openai_max_tokens = self.env.company.odoogpt_openai_max_tokens,
            odoogpt_openai_temperature = self.env.company.odoogpt_openai_temperature
        )
        return res


    def odoogpt_openai_model_select_from_db(self):
        """Get Models from OpenAI api and show selector wizart"""
        self.env['odoogpt.openai.model'].sudo().odoogpt_openai_model_refresh_from_api(format='model')
        return self.env.ref('odoogpt.odoogpt_openai_model_select_wizard_act_window').read()[0]
