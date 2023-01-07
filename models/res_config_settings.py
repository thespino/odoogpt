# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    odoogpt_openai_api_key = fields.Char(
        string='OpenAI Api token',
        help="""Open AI Api token can be found at https://beta.openai.com/account/api-keys""",
        related='company_id.odoogpt_openai_api_key',
        default=False,
        required=False,
        readonly=False,
    )

    odoogpt_openai_model = fields.Char(
        string='OpenAI Model',
        help="""Open AI Model to use: https://beta.openai.com/docs/models/overview""",
        related='company_id.odoogpt_openai_model',
        default='text-davinci-003',
        required=True,
        readonly=False,
    )

    odoogpt_openai_max_tokens = fields.Integer(
        string='OpenAI Max tokens',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-max_tokens""",
        related='company_id.odoogpt_openai_max_tokens',
        default=150,
        required=True,
        readonly=False,
    )

    odoogpt_openai_temperature = fields.Integer(
        string='OpenAI Temperature',
        help="""See https://beta.openai.com/docs/api-reference/completions/create#completions/create-temperature""",
        related='company_id.odoogpt_openai_temperature',
        default=1,
        required=True,
        readonly=False,
    )


    def set_values(self):
        res = super().set_values()
        self.env.company.odoogpt_openai_api_key = self.odoogpt_openai_api_key
        self.env.company.odoogpt_openai_model = self.odoogpt_openai_model
        self.env.company.odoogpt_openai_max_tokens = self.odoogpt_openai_max_tokens
        self.env.company.odoogpt_openai_temperature = self.odoogpt_openai_temperature
        return res

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            odoogpt_openai_api_key = self.env.company.odoogpt_openai_api_key,
            odoogpt_openai_model = self.env.company.odoogpt_openai_model,
            odoogpt_openai_max_tokens = self.env.company.odoogpt_openai_max_tokens,
            odoogpt_openai_temperature = self.env.company.odoogpt_openai_temperature
        )
        return res


    def odoogpt_openai_model_select_from_db(self):
        """Get Models from OpenAI api and show selector wizart"""
        self.odoogpt_openai_model_refresh_from_api(format='model')
        return self.env.ref('odoogpt.odoogpt_openai_model_select_wizard_act_window').read()[0]


    # UTILS

    # FIXME: Move to odoogpt.openai.model 
    @api.model
    def odoogpt_openai_model_refresh_from_api(self, format='model'):
        """Refresh Models stored in database from OpenAI apis"""
        # TODO: Check what to do with unlinking of inexistent model. Maybe we
        #       can keep them.
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        OdoogptOpenaiModel = self.env['odoogpt.openai.model']
        
        # Check Api Key from actual settings or from stored settings
        api_key = self.odoogpt_openai_api_key or OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=False)
        if not api_key:
            return {
                'warning': {
                    'title': _('Missing OpenAI api key'),
                    'message': _('You need to specify the OpenAI api key first!'),
                }
            }

        # Get Models from OpenAI
        openai_models = OdoogptOpenaiUtils.models_list(api_key=api_key)

        if not openai_models and not len(openai_models):
            return {
                'warning': {
                    'title': _('No Models'),
                    'message': _('No Models found from OpenAI api'),
                }
            }

        # Store/update models in our database
        odoogpt_models = OdoogptOpenaiModel._get_models_as_dict()
        for openai_model in openai_models:
            if openai_model.get('object', '') != 'model':
                continue

            odoogpt_model = odoogpt_models.get(openai_model['id'])
            if odoogpt_model:
                odoogpt_model.write({
                    'openai_owned_by': openai_model.get('owned_by', odoogpt_model.openai_owned_by),
                    'openai_permissions': openai_model.get('permissions', odoogpt_model.openai_permissions),
                })
            elif openai_model.get('id'):
                odoogpt_model = OdoogptOpenaiModel.create({
                    'openai_id': openai_model.get('id'),
                    'openai_owned_by': openai_model.get('owned_by'),
                    'openai_permissions': openai_model.get('permissions'),
                })

                odoogpt_models[odoogpt_model.openai_id] = odoogpt_model

        # Return
        if format == 'dict':
            return odoogpt_models
        else:   # formt == 'model' or anything else
            ret = OdoogptOpenaiModel
            for model in odoogpt_models.values():
                ret += model