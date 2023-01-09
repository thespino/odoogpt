# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json


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