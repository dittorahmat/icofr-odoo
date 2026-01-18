# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    is_significant_location = fields.Boolean(
        string='Lokasi/Entitas Signifikan (ICORF)',
        default=False,
        help='Menandakan apakah perusahaan ini merupakan lokasi signifikan dalam ruang lingkup ICOFR (Bab III 1.3). '
             'Digunakan untuk perhitungan multiplier materialitas grup.'
    )
