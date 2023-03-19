# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OdoogptOpenaiFile(models.Model):
    _name = 'odoogpt.openai.file'
    _description = 'OdooGPT OpenAI File'
    _inherit= 'odoogpt.openai.mixin'
    _rec_name = 'filename'

    REC_TYPES = ['file']


    filename = fields.Char(
        string='File Name',
        required=False,
        default=False,
    )

    purpose = fields.Char(
        string='Purpose',
        required=False,
        default=False,
    )


    def delete_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        try:
            for file in self:
                OdoogptOpenaiUtils.files_delete(file.openai_id)
                file.unlink()
        except Exception as ex:
            raise UserError(ex)

        action = self.env.ref('odoogpt.odoogpt_openai_file_act_window').read()[0]
        return action


    # REFRESH FROM API
    @api.model
    def _refresh_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        api_key = OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=True)
        return OdoogptOpenaiUtils.files_list(api_key=api_key)

    @property
    def _refresh_from_api_fields(self):
        return [
            'filename',
            'purpose',
        ]
