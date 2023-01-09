# -*- coding: utf-8 -*-

from odoo import models, _
import openai


class OdoogptOpenaiUtils(models.AbstractModel):
    _inherit = 'odoogpt.openai.utils'


    # FILES ==============================================================================

    def _files_list__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def files_list(self, **kwargs):
        """List Files. Ref. https://beta.openai.com/docs/api-reference/files/list"""
        response = openai.File.list(
            **{
                **self._files_list__get_parameters(),
                **kwargs,
            }
        )

        return response['data']


    def _files_create__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def files_create(self, file, purpose='fine-tune', **kwargs):
        """Upload/Create File. Ref. https://beta.openai.com/docs/api-reference/files/upload"""
        response = openai.File.create(
            file=file,
            purpose=purpose,
            **{
                **self._files_create__get_parameters(),
                **kwargs,
            }
        )

        return response


    def _files_delete__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def files_delete(self, file_id, **kwargs):
        """Delete File. Ref. https://beta.openai.com/docs/api-reference/files/delete"""
        response = openai.File.delete(
            sid=file_id,
            **{
                **self._files_delete__get_parameters(),
                **kwargs,
            }
        )

        return response


    def _files_download__get_parameters(self):
        """Get params to pass to openai library to make a successful request"""
        return self._odoogpt_get_parameters([
            # Odoo name, OpenAI name
            ('odoogpt_openai_api_key', 'api_key'),
        ])

    def files_download(self, file_id, **kwargs):
        """Download File. Ref. https://beta.openai.com/docs/api-reference/files/retrieve-content"""
        response = openai.File.download(
            id=file_id,
            **{
                **self._files_download__get_parameters(),
                **kwargs,
            }
        )

        return response