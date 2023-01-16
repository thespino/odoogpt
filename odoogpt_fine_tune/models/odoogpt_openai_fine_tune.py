# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OdoogptOpenaiFineTune(models.Model):
    _name = 'odoogpt.openai.fine.tune'
    _description = 'OdooGPT OpenAI Fine-tune'
    _inherit= 'odoogpt.openai.mixin'

    REC_TYPES = ['fine-tune']


    status = fields.Selection(
        string='Process Status',
        required=False,
        default=False,
        selection=[
            ('pending', 'Pending'),
            ('running', 'Running'),
            ('succeeded', 'Succeeded'),
            ('cancelled', 'Cancelled'),
        ]
    )

    # TODO: Create many2one?
    model = fields.Char(
        string='Base model',
        required=False,
        default=False,
    )

    # TODO: Create many2one?
    fine_tuned_model = fields.Char(
        string='Fine tuned model',
        required=False,
        default=False,
    )


    def cancel_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        try:
            for rec in self:
                OdoogptOpenaiUtils.fine_tunes_cancel(rec.openai_id)
        except Exception as ex:
            raise UserError(ex)

        self.refresh_from_api()

        return self


    # REFRESH FROM API
    @api.model
    def _refresh_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        api_key = OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=True)
        return OdoogptOpenaiUtils.fine_tunes_list(api_key=api_key)

    @property
    def _refresh_from_api_fields(self):
        return [
            'status',
            'model',
            'fine_tuned_model',
        ]
