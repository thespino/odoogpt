# -*- coding: utf-8 -*-

from odoo import models, _
import openai


class OdoogptOpenaiUtils(models.AbstractModel):
    _inherit = 'odoogpt.openai.utils'


    # FINE TUNES =========================================================================

    def _fine_tunes_list__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def fine_tunes_list(self, **kwargs):
        """List Fine Tunes. Ref. https://beta.openai.com/docs/api-reference/fine-tunes/list"""
        response = openai.FineTune.list(
            **{
                **self._fine_tunes_list__get_parameters(),
                **kwargs,
            }
        )

        return response['data']


    def _fine_tunes_create__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def fine_tunes_create(self, training_file, **kwargs):
        """Create Fine Tune. Ref. https://beta.openai.com/docs/api-reference/fine-tunes/create"""
        response = openai.FineTune.create(
            training_file=training_file,
            **{
                **self._fine_tunes_create__get_parameters(),
                **kwargs,
            }
        )

        return response


    def _fine_tunes_cancel__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def fine_tunes_cancel(self, fine_tune_id, **kwargs):
        """Cancel Fine Tune job. Ref. https://beta.openai.com/docs/api-reference/fine-tunes/cancel"""
        response = openai.FineTune.cancel(
            id=fine_tune_id,
            **{
                **self._fine_tunes_cancel__get_parameters(),
                **kwargs,
            }
        )

        return response
