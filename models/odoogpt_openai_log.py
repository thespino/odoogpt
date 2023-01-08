# -*- coding: utf-8 -*-

from odoo import models, fields, _


class OdoogptOpenaiLog(models.Model):
    _name = 'odoogpt.openai.log'
    _description = 'OdooGPT OpenAI Log'
    _rec_name = 'prompt'


    prompt = fields.Text(
        string='Prompt',
        help="""Prompt text given by an user""",
        required=True,
    )

    response_raw = fields.Text(
        string='Raw Response',
        help="""The response, as it is, given by OpenAI api""",
        required=True,
    )

    response = fields.Text(
        string='Response',
        help="""Response text given by OpenAI"""
    )