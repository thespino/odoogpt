# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json


class OdoogptOpenaiModel(models.Model):
    _name = 'odoogpt.openai.model'
    _inherit= 'odoogpt.openai.mixin'
    _description = 'OdooGPT OpenAI Model'

    REC_TYPES = ['model']


    owned_by = fields.Char(
        string='OpenAI Owned by',
        required=False,
        default=False,
    )

    permission = fields.Json(
        string='OpenAI permission',
        required=False,
        default=False,
    )
    permission_string = fields.Text(
        string='OpenAI permission',
        required=False,
        default=False,
        store=False,
        compute='_compute_permission_string'
    )


    def _compute_permission_string(self):
        for openai_model in self:
            openai_model.permission_string = json.dumps(
                self.permission or {},
                indent=4
            )


    # REFRESH FROM API
    @api.model
    def _refresh_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        api_key = OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=True)
        return OdoogptOpenaiUtils.models_list(api_key=api_key)

    @property
    def _refresh_from_api_fields(self):
        return [
            'owned_by',
            'permission',
        ]
