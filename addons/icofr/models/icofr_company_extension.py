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

    entity_code = fields.Char(
        string='Kode Entitas',
        help='Kode unik entitas dari sistem eksternal (misal: 103, 114, 0101)'
    )

    # Tabel 10: Faktor Kualitatif Lokasi (Hal 30)
    has_prior_misstatements = fields.Boolean('Riwayat Salah Saji Terdeteksi')
    has_fraud_risk = fields.Boolean('Kerentanan terhadap Fraud Tinggi')
    has_significant_changes = fields.Boolean('Perubahan Signifikan (Sistem/Personel)')
    has_operational_complexity = fields.Boolean('Kompleksitas Operasional Tinggi')

    qualitative_scoping_notes = fields.Text('Justifikasi Kualitatif Lokasi')

    bumn_cluster_id = fields.Many2one(
        'icofr.industry.cluster',
        string='Klaster Industri BUMN',
        help='Klaster industri BUMN sesuai Lampiran 2 Juknis BUMN (Energi, Logistik, Jasa Keuangan, dll)'
    )
