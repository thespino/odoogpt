# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import ValidationError
import openai


class OdoogptOpenaiUtils(models.AbstractModel):
    _name = 'odoogpt.openai.utils'
    _description = 'OdooGPT OpenAI Utils'


    # UTILS ==============================================================================

    def _odoogpt_check_api_key(self, raise_err=True):
        """Check api key existance in company"""
        if self.env.company.odoogpt_openai_api_key:
            return self.env.company.odoogpt_openai_api_key
        if raise_err:
            raise ValidationError(_('OpenAI Api Token not set in settings!'))
        else:
            return False

    def _odoogpt_get_parameters(self, PARAMETERS):
        """Get params to pass to openai library to make a successful request"""
        params = {}
        for PARAM in PARAMETERS:
            params[PARAM[1]] = self.env.company[PARAM[0]]

        return params


    # MODELS =============================================================================

    def _models_list__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def models_list(self, **kwargs):
        """List available Models. Ref. https://beta.openai.com/docs/api-reference/models/list"""
        response = openai.Model.list(
            **{
                **self._models_list__get_parameters(),
                **kwargs,
            }
        )

        return response['data']


    # COMPLETITION =======================================================================

    def _completition_create__get_parameters(self):
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
            ('odoogpt_openai_model', 'model'),
            ('odoogpt_openai_max_tokens', 'max_tokens'),
            ('odoogpt_openai_temperature', 'temperature'),
        ])

    def completition_create(self, prompt, **kwargs):
        """Create a Completition. Ref. https://beta.openai.com/docs/api-reference/completions"""
        response = openai.Completion.create(
            prompt=prompt,
            **{
                **self._completition_create__get_parameters(),
                **kwargs,
            }
        )

        # Log
        self.env['odoogpt.openai.log'].sudo().create({
            'type': 'completition',
            'raw_request': prompt,
            'parsed_request': prompt,
            'raw_response': str(response),
            'parsed_response': response['choices'][0]['text'],
        })

        return response['choices'][0]['text']
