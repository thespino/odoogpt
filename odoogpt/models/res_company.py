# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'


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
