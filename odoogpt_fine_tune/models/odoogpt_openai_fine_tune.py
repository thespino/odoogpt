# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OdoogptOpenaiFineTune(models.Model):
    _name = 'odoogpt.openai.fine.tune'
    _description = 'OdooGPT OpenAI Fine-tune'
    _rec_name = 'openai_id'

    _sql_constraints = [
        ('UNIQUE_OPENAI_ID', 'UNIQUE(openai_id)', _('The OpenAI Id of a Fine-tune must be unique!'))
    ]


    openai_id = fields.Char(
        string='OpenAI Id',
        required=False,
        default=False,
        index=True,
    )

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


    # UTILS
    def _get_as_dict(self, domain=[]):
        """Get all records in a dict format (openai_id: record)"""
        recs = self.search(domain)

        return {rec.openai_id: rec for rec in recs}


    @api.model
    def refresh_from_api(self, format='model'):
        """Refresh Records stored in database from OpenAI apis"""
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']

        # Check and get OpenAI Api Key
        api_key = OdoogptOpenaiUtils._odoogpt_check_api_key(raise_err=True)

        # Get Models from OpenAI
        try:
            openai_records = OdoogptOpenaiUtils.fine_tunes_list(api_key=api_key)
        except Exception as ex:
            raise UserError(ex)

        if not openai_records and not len(openai_records):
            raise ValidationError(_('No Fine-tunes found from OpenAI api'))

        # Store/update models in our database
        odoogpt_records = self._get_as_dict()
        for openai_record in openai_records:
            if openai_record.get('object', '') != 'fine-tune':
                continue

            odoogpt_record = odoogpt_records.get(openai_record['id'])
            if odoogpt_record:
                odoogpt_record.write({
                    'status': openai_record.get('status', odoogpt_record.status),
                    'model': openai_record.get('model', odoogpt_record.model),
                    'fine_tuned_model': openai_record.get('fine_tuned_model', odoogpt_record.fine_tuned_model),
                })
            elif openai_record.get('id'):
                odoogpt_record = self.create({
                    'openai_id': openai_record.get('id'),
                    'status': openai_record.get('status'),
                    'model': openai_record.get('model'),
                    'fine_tuned_model': openai_record.get('fine_tuned_model'),
                })

                odoogpt_records[odoogpt_record.openai_id] = odoogpt_record

        # Return
        if format == 'dict':
            return odoogpt_records
        else:   # format == 'model' or anything else
            ret = self
            for model in odoogpt_records.values():
                ret += model