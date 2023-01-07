# -*- coding: utf-8 -*-

from odoo import models, fields, _


class OdoogptOpenaiModelSelectWizard(models.TransientModel):
    _name = 'odoogpt.openai.model.select.wizard'
    _description = 'OdooGPT OpenAI Model Selector'


    odoogpt_openai_model = fields.Many2one(
        string='OpenAI Model',
        comodel_name='odoogpt.openai.model',
        required=True,
        default=False,
    )


    def action_ok(self):
        self.ensure_one()

        self.env.company.write({
            'odoogpt_openai_model': self.odoogpt_openai_model.openai_id
        })

        return {'type': 'ir.actions.client', 'tag': 'reload'}
