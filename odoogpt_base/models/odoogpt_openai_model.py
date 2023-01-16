# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json


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
    openai_permission_string = fields.Text(
        string='OpenAI permission',
        required=False,
        default=False,
        store=False,
        compute='_compute_openai_permission_string'
    )


    def _compute_openai_permission_string(self):
        for openai_model in self:
            openai_model.openai_permission_string = json.dumps(
                self.openai_permission or {},
                indent=4
            )


    # UTILS
    def _get_as_dict(self, domain=[]):
        """Get all models in a dict format (openai_id: record)"""
        models = self.search(domain)

        return {model.openai_id: model for model in models}


    @api.model
    def refresh_from_api(self, format='model'):
        """Refresh Models stored in database from OpenAI apis"""
        # TODO: Check what to do with unlinking of inexistent model. Maybe we
        #       can keep them.
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']

        # Check and get OpenAI Api Key
        api_key = OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=True)

        # Get Models from OpenAI
        try:
            openai_models = OdoogptOpenaiUtils.models_list(api_key=api_key)
        except Exception as ex:
            raise UserError(ex)

        if not openai_models and not len(openai_models):
            raise ValidationError(_('No Models found from OpenAI api'))

        # Store/update models in our database
        odoogpt_models = self._get_as_dict()
        for openai_model in openai_models:
            if openai_model.get('object', '') != 'model':
                continue

            odoogpt_model = odoogpt_models.get(openai_model['id'])
            if odoogpt_model:
                odoogpt_model.write({
                    'openai_owned_by': openai_model.get('owned_by', odoogpt_model.openai_owned_by),
                    'openai_permission': openai_model.get('permission', odoogpt_model.openai_permission),
                })
            elif openai_model.get('id'):
                odoogpt_model = self.create({
                    'openai_id': openai_model.get('id'),
                    'openai_owned_by': openai_model.get('owned_by'),
                    'openai_permission': openai_model.get('permission'),
                })

                odoogpt_models[odoogpt_model.openai_id] = odoogpt_model

        # Return
        if format == 'dict':
            return odoogpt_models
        else:   # format == 'model' or anything else
            ret = self
            for model in odoogpt_models.values():
                ret += model