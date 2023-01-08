# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


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
        self.env.company.odoogpt_openai_prompt_prefix = self.odoogpt_openai_prompt_prefix
        self.env.company.odoogpt_openai_prompt_suffix = self.odoogpt_openai_prompt_suffix
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            odoogpt_openai_prompt_prefix = self.env.company.odoogpt_openai_prompt_prefix,
            odoogpt_openai_prompt_suffix = self.env.company.odoogpt_openai_prompt_suffix
        )
        return res
