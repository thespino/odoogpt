# -*- coding: utf-8 -*-

from odoo import models


class ResCompany(models.Model):
    _inherit = ['res.company', 'odoogpt.settings.mixin']
    _name = 'res.company'

    # Simply add OdooGPT settings to company by inheriting the mixin
