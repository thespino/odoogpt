# -*- coding: utf-8 -*-

from odoo import models, fields, _


class OdoogptOpenaiModel(models.Model):
    _name = 'odoogpt.openai.model'
    _description = 'OdooGPT OpenAI Model'
    _rec_name = 'openai_id'

    _sql_constraints = [
        ('UNIQUE_OPENAI_ID', 'UNIQUE(openai_id)', _('The OpenAI Id of a Model must be unique!'))
    ]


    openai_id = fields.Char(
        string='OpenAI Id',
        required=False,
        default=False,
        index=True,
    )

    openai_owned_by = fields.Char(
        string='OpenAI Owned by',
        required=False,
        default=False,
    )

    openai_permission = fields.Json(
        string='OpenAI permission',
        required=False,
        default=False,
    )


    # UTILS
    def _get_models_as_dict(self, domain=[]):
        """Get all models in a dict format (openai_id: record)"""
        models = self.search(domain)

        return {model.openai_id: model for model in models}