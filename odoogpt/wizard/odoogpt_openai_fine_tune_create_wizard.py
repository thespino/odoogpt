# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError


class OdoogptOpenaiFineTuneCreateWizard(models.TransientModel):
    _name = 'odoogpt.openai.fine.tune.create.wizard'
    _description = 'OdooGPT OpenAI Fine Tune Create'


    training_file = fields.Many2one(
        string='Training File',
        comodel_name='odoogpt.openai.file',
        required=True,
        domain="""[
            ('purpose', '=', 'fine-tune')
        ]"""
    )
    validation_file = fields.Many2one(
        string='Validation File',
        comodel_name='odoogpt.openai.file',
        required=False,
        default=False,
    )

    model = fields.Many2one(
        string='Base Model',
        comodel_name='odoogpt.openai.model',
        required=False,
        default=False,
    )

    suffix = fields.Char(
        string='Suffix',
        required=False,
        default=False,
    )



    def action_ok(self):
        self.ensure_one()

        try:
            OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
            OdoogptOpenaiFineTune = self.env['odoogpt.openai.fine.tune']

            OdoogptOpenaiUtils.fine_tunes_create(
                **{k: v for k, v in {
                    'training_file': self.training_file.openai_id,
                    'validation_file': self.validation_file.openai_id or None,
                    'model': self.model.openai_id or None,
                    'suffix': self.suffix or None,
                }.items() if v is not None}
            )

            OdoogptOpenaiFineTune.refresh_from_api()

            action = self.env.ref('odoogpt.odoogpt_openai_fine_tune_act_window').read()[0]
            return action
        except Exception as ex:
            raise UserError(ex)
