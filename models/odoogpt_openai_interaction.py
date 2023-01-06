# -*- coding: utf-8 -*-

from odoo import models, fields, _


class OdoogptOpenaiInteraction(models.Model):
    _name = 'odoogpt.openai.interaction'
    _description = 'OdooGPT OpenAI Interaction'


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