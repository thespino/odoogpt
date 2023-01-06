# -*- coding: utf-8 -*-

import json
from odoo import models, fields, _
from odoo.exceptions import UserError
import openai


class OdoogptOpenaiInteraction(models.AbstractModel):
    _name = 'odoogpt.openai.utils'
    _description = 'OdooGPT OpenAI Utils'


    PARAMETERS = [
        # Odoo name, OpenAI name
        ('odoogpt_openai_api_key', 'api_key'),
        ('odoogpt_openai_model', 'model'),
        ('odoogpt_openai_max_tokens', 'max_tokens'),
        ('odoogpt_openai_temperature', 'temperature'),
    ]


    def _get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        params = {}
        for PARAM in self.PARAMETERS:
            params[PARAM[1]] = self.env.company[PARAM[0]]

        return params
    
    def _check_token(self):
        if not self.env.company.odoogpt_openai_api_key:
            raise UserError(_('OpenAI Api Token not set in settings!'))


    def completition_create(self, prompt, **kwargs):
        """Create a Completition. Ref. https://beta.openai.com/docs/api-reference/completions"""
        response = openai.Completion.create(
            prompt=prompt,
            **{
                **self._get_parameters(),
                **kwargs,
            }
        )

        self.env['odoogpt.openai.interaction'].sudo().create({
            'prompt': prompt,
            'response_raw': str(response),
            'response': response['choices'][0]['text'],
        })

        return response['choices'][0]['text']