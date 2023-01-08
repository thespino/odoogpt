# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'


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
