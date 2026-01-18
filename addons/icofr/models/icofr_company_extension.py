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

    is_newly_acquired = fields.Boolean(
        string='Entitas Baru Diakuisisi?',
        default=False,
        help='Sesuai Juknis BUMN FAQ 13, entitas yang baru diakuisisi memiliki masa transisi implementasi ICOFR.'
    )

    icofr_revenue_contribution = fields.Float(
        string='Kontribusi Pendapatan (ICORF)',
        help='Nilai pendapatan entitas ini untuk kalkulasi Aturan 2/3 di tingkat grup.'
    )

    icofr_asset_contribution = fields.Float(
        string='Kontribusi Aset (ICORF)',
        help='Nilai total aset entitas ini untuk kalkulasi Aturan 2/3 di tingkat grup.'
    )

    bumn_cluster_id = fields.Many2one(
        'icofr.industry.cluster',
        string='Klaster Industri BUMN',
        help='Klaster industri BUMN sesuai Lampiran 2 Juknis BUMN (Energi, Logistik, Jasa Keuangan, dll)'
    )
