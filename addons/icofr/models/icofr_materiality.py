# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrMateriality(models.Model):
    _name = 'icofr.materiality'
    _description = 'Kalkulator Materialitas ICORF'
    _order = 'fiscal_year desc, create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Perhitungan',
        required=True,
        default='Kalkulasi Materialitas',
        help='Nama deskriptif dari perhitungan materialitas'
    )

    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk perhitungan materialitas ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang menjadi basis perhitungan'
    )

    revenue_amount = fields.Float(
        string='Jumlah Pendapatan',
        required=True,
        help='Jumlah pendapatan perusahaan (dalam satuan mata uang lokal)'
    )

    total_assets_amount = fields.Float(
        string='Jumlah Total Aset',
        required=True,
        help='Jumlah total aset perusahaan (dalam satuan mata uang lokal)'
    )

    net_income_amount = fields.Float(
        string='Jumlah Laba Bersih',
        help='Jumlah laba bersih perusahaan (dalam satuan mata uang lokal)'
    )

    overall_materiality_percent = fields.Float(
        string='Persentase Overall Materiality',
        default=0.5,
        help='Persentase Overall Materiality (contoh: 0.5%)'
    )

    performance_materiality_percent = fields.Float(
        string='Persentase Performance Materiality',
        default=0.75,
        help='Persentase Performance Materiality sebagai faktor dari Overall Materiality (contoh: 75%)'
    )

    overall_materiality_amount = fields.Float(
        string='Jumlah Overall Materiality',
        compute='_compute_materiality_amounts',
        store=True,
        help='Jumlah Overall Materiality dalam satuan mata uang lokal'
    )

    performance_materiality_amount = fields.Float(
        string='Jumlah Performance Materiality',
        compute='_compute_materiality_amounts',
        store=True,
        help='Jumlah Performance Materiality dalam satuan mata uang lokal'
    )

    materiality_basis = fields.Selection([
        ('revenue', 'Pendapatan'),
        ('total_assets', 'Total Aset'),
        ('net_income', 'Laba Bersih'),
        ('hybrid', 'Campuran')
    ], string='Basis Perhitungan', default='revenue',
       help='Basis utama untuk perhitungan materialitas')

    calculation_method = fields.Selection([
        ('percent_revenue', 'Persen dari Pendapatan'),
        ('percent_assets', 'Persen dari Total Aset'),
        ('percent_net_income', 'Persen dari Laba Bersih'),
        ('fixed_amount', 'Jumlah Tetap'),
        ('other', 'Lainnya')
    ], string='Metode Perhitungan', default='percent_revenue',
       help='Metode yang digunakan untuk menghitung materialitas')

    notes = fields.Text(
        string='Catatan Perhitungan',
        help='Catatan tentang perhitungan materialitas dan pertimbangan lainnya'
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help='Status aktivasi dari kalkulasi materialitas'
    )

    account_mapping_ids = fields.One2many(
        'icofr.account.mapping',
        'materiality_id',
        string='Pemetaan Akun',
        help='Pemetaan akun ke FSLI (Financial Statement Line Item)'
    )

    @api.depends('revenue_amount', 'total_assets_amount', 'net_income_amount',
                 'overall_materiality_percent', 'performance_materiality_percent',
                 'materiality_basis')
    def _compute_materiality_amounts(self):
        for record in self:
            # Calculate overall materiality amount based on selected basis
            if record.materiality_basis == 'revenue':
                base_amount = record.revenue_amount
            elif record.materiality_basis == 'total_assets':
                base_amount = record.total_assets_amount
            elif record.materiality_basis == 'net_income':
                base_amount = record.net_income_amount or record.total_assets_amount
            else:  # hybrid - use largest value
                base_amount = max(record.revenue_amount, record.total_assets_amount,
                                 record.net_income_amount or 0)

            record.overall_materiality_amount = base_amount * (record.overall_materiality_percent / 100)
            record.performance_materiality_amount = record.overall_materiality_amount * (record.performance_materiality_percent / 100)

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    fiscal_year = new_val_dict.get('fiscal_year', fields.Date.today().year)
                    company_id = new_val_dict.get('company_id', '')
                    new_val_dict['name'] = f'Materialitas {fiscal_year} - {company_id}'
                processed_vals.append(new_val_dict)
            return super(IcofrMateriality, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                fiscal_year = new_vals.get('fiscal_year', fields.Date.today().year)
                company_id = new_vals.get('company_id', '')
                new_vals['name'] = f'Materialitas {fiscal_year} - {company_id}'
            return super(IcofrMateriality, self).create(new_vals)

    def action_calculate_materiality(self):
        """Method untuk mengkalkulasi ulang materialitas jika ada perubahan data"""
        self._compute_materiality_amounts()
        return True

    def action_export_materiality(self):
        """Method untuk mengekspor data materialitas"""
        # Placeholder for export functionality
        # In a real implementation, this would export the materiality data
        # to a file in various formats (Excel, PDF, etc.)
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/binary/download_document/{self.id}/icofr.materiality/export',
            'target': 'new',
        }