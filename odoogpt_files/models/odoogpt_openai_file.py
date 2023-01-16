# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OdoogptOpenaiFile(models.Model):
    _name = 'odoogpt.openai.file'
    _description = 'OdooGPT OpenAI File'
    _rec_name = 'filename'

    _sql_constraints = [
        ('UNIQUE_OPENAI_ID', 'UNIQUE(openai_id)', _('The OpenAI Id of a File must be unique!'))
    ]


    openai_id = fields.Char(
        string='OpenAI Id',
        required=False,
        default=False,
        index=True,
    )

    filename = fields.Char(
        string='File Name',
        required=False,
        default=False,
    )

    purpose = fields.Char(
        string='Purpose',
        required=False,
        default=False,
    )


    def delete_from_api(self):
        OdoogptOpenaiUtils = self.env['odoogpt.openai.utils']
        try:
            for file in self:
                OdoogptOpenaiUtils.files_delete(file.openai_id)
                file.unlink()
        except Exception as ex:
            raise UserError(ex)

        action = self.env.ref('odoogpt_files.odoogpt_openai_file_act_window').read()[0]
        return action


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
            openai_records = OdoogptOpenaiUtils.files_list(api_key=api_key)
        except Exception as ex:
            raise UserError(ex)

        if not openai_records and not len(openai_records):
            raise ValidationError(_('No Files found from OpenAI api'))

        # Store/update models in our database
        odoogpt_records = self._get_as_dict()
        for openai_record in openai_records:
            if openai_record.get('object', '') != 'file':
                continue

            odoogpt_record = odoogpt_records.get(openai_record['id'])
            if odoogpt_record:
                odoogpt_record.write({
                    'filename': openai_record.get('filename', odoogpt_record.filename),
                    'purpose': openai_record.get('purpose', odoogpt_record.purpose),
                })
            elif openai_record.get('id'):
                odoogpt_record = self.create({
                    'openai_id': openai_record.get('id'),
                    'filename': openai_record.get('filename'),
                    'purpose': openai_record.get('purpose'),
                })

                odoogpt_records[odoogpt_record.openai_id] = odoogpt_record

        # Return
        if format == 'dict':
            return odoogpt_records
        else:   # format == 'model' or anything else
            ret = self
            for model in odoogpt_records.values():
                ret += model