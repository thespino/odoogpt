# -*- coding: utf-8 -*-

from odoo import models, fields, _


class OdoogptOpenaiModelSelectWizard(models.TransientModel):
    _name = 'odoogpt.openai.model.select.wizard'
    _description = 'OdooGPT OpenAI Model Selector'


    # linked document
    res_id = fields.Many2oneReference('Document ID', model_field='res_model', readonly=True, required=False)
    # res_model_id = fields.Many2one('ir.model', 'Document Model', ondelete='cascade')
    res_model = fields.Char('Document Model Name', readonly=True, required=False)

    odoogpt_openai_model = fields.Many2one(
        string='OpenAI Model',
        comodel_name='odoogpt.openai.model',
        required=True,
        default=False,
    )


    def action_ok(self):
        self.ensure_one()

        if not self.res_id or not self.res_model:
            self.env.company.write({
                'odoogpt_openai_model': self.odoogpt_openai_model.openai_id
            })
        else:
            self.env[self.res_model].browse(self.res_id).write({
                'odoogpt_openai_model': self.odoogpt_openai_model.openai_id
            })


        return {'type': 'ir.actions.client', 'tag': 'reload'}
