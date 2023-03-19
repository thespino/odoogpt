# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError
import base64


class OdoogptOpenaiFileCreateWizard(models.TransientModel):
    _name = 'odoogpt.openai.file.create.wizard'
    _description = 'OdooGPT OpenAI File Upload'


    file = fields.Binary(
        string='File',
        required=True,
    )
    file_name = fields.Char(
        string='File Name',
        required=False,
        default=False,
    )

    purpose = fields.Selection(
        string='Purpose',
        selection=[
            ('fine-tune', 'fine-tune'),
            ('search', 'search'),
        ],
        default='fine-tune',
        required=True,
    )


    def action_ok(self):
        self.ensure_one()

        try:
            OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
            OdoogptOpenaiFile = self.env['odoogpt.openai.file']

            OdoogptOpenaiUtils.files_create(
                file=base64.decodebytes(self.file),
                purpose=self.purpose,
                user_provided_filename=self.file_name or 'file'
            )

            OdoogptOpenaiFile.refresh_from_api()

            action = self.env.ref('odoogpt.odoogpt_openai_file_act_window').read()[0]
            return action
        except Exception as ex:
            raise UserError(ex)
