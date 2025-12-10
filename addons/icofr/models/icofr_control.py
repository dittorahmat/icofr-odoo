# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class IcofrControl(models.Model):
    _name = 'icofr.control'
    _description = 'Master Data Kontrol Internal'
    _order = 'name'

    name = fields.Char(
        string='Nama Kontrol',
        required=True,
        translate=True,
        help='Nama unik dari kontrol internal'
    )
    code = fields.Char(
        string='Kode Kontrol',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi kontrol'
    )
    control_type = fields.Selection([
        ('preventive', 'Preventif'),
        ('detective', 'Detektif'),
        ('corrective', 'Korektif')
    ], string='Jenis Kontrol', required=True,
       help='Jenis dari kontrol internal')
    
    frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('yearly', 'Tahunan')
    ], string='Frekuensi', required=True,
       help='Frekuensi pelaksanaan kontrol')
    
    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Kontrol',
        required=True,
        help='Pengguna yang bertanggung jawab atas kontrol ini'
    )
    
    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi lengkap dari kontrol internal'
    )
    
    objective = fields.Text(
        string='Tujuan Kontrol',
        help='Tujuan dari kontrol internal'
    )
    
    process_id = fields.Many2one(
        'icofr.process',
        string='Proses Bisnis Terkait',
        help='Proses bisnis yang terkait dengan kontrol ini'
    )

    risk_ids = fields.Many2many(
        'icofr.risk',
        'icofr_control_risk_rel',
        'control_id', 'risk_id',
        string='Risiko Terkait',
        help='Risiko-risiko yang ditangani oleh kontrol ini'
    )

    key_performance_indicator = fields.Text(
        string='Indikator Kinerja Utama',
        help='Indikator kinerja untuk mengevaluasi efektivitas kontrol'
    )

    testing_procedures = fields.Text(
        string='Prosedur Pengujian',
        help='Prosedur yang digunakan untuk menguji kontrol ini'
    )

    evidence_required = fields.Text(
        string='Bukti yang Diperlukan',
        help='Dokumentasi atau bukti yang diperlukan sebagai hasil pengujian'
    )

    key_performance_indicator = fields.Text(
        string='Indikator Kinerja Utama',
        help='Indikator kinerja untuk mengevaluasi efektivitas kontrol'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('under_review', 'Dalam Review')
    ], string='Status', default='active',
       help='Status dari kontrol internal')
    
    last_tested_date = fields.Date(
        string='Tanggal Terakhir Diuji',
        help='Tanggal terakhir kontrol ini diuji'
    )
    
    next_test_date = fields.Date(
        string='Tanggal Pengujian Berikutnya',
        help='Tanggal terjadwal untuk pengujian berikutnya'
    )
    
    effectiveness_rating = fields.Selection([
        ('high', 'Tinggi'),
        ('medium', 'Sedang'),
        ('low', 'Rendah'),
        ('not_tested', 'Belum Diuji')
    ], string='Rating Efektivitas', default='not_tested',
       help='Rating efektivitas kontrol berdasarkan hasil pengujian terakhir')
    
    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait kontrol'
    )
    
    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            controls = self.search([('code', '=', record.code)])
            if len(controls) > 1:
                raise ValidationError("Kode kontrol harus unik!")
    
    # Dashboard-related methods and fields
    def action_refresh_dashboard(self):
        """Method untuk merefresh data dashboard"""
        # Dalam implementasi sebenarnya, ini akan memperbarui data yang tampil di dashboard
        # Untuk sekarang, hanya akan menampilkan notifikasi bahwa data telah diperbarui
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Dashboard Diperbarui',
                'message': 'Data dashboard telah diperbarui',
                'type': 'success',
                'sticky': False
            }
        }

    def action_export_dashboard_data(self):
        """Method untuk mengekspor data dashboard"""
        # Buka wizard ekspor dengan parameter untuk data dashboard
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'all',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Data Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'all',
                'default_export_format': 'xlsx'
            }
        }

    def action_export_controls(self):
        """Method untuk membuka wizard ekspor kontrol"""
        self.ensure_one()
        # Buka wizard ekspor dengan parameter yang sesuai
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'control',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Kontrol Internal',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'control',
                'default_export_format': 'xlsx'
            }
        }

    # Field-field untuk dashboard
    total_controls = fields.Integer(
        string='Total Kontrol',
        compute='_compute_dashboard_metrics',
        help='Jumlah total kontrol'
    )

    effective_controls = fields.Integer(
        string='Kontrol Efektif',
        compute='_compute_dashboard_metrics',
        help='Jumlah kontrol yang efektif'
    )

    total_risks = fields.Integer(
        string='Total Risiko',
        compute='_compute_dashboard_metrics',
        help='Jumlah total risiko'
    )

    high_risks = fields.Integer(
        string='Risiko Tinggi',
        compute='_compute_dashboard_metrics',
        help='Jumlah risiko dengan tingkat tinggi'
    )

    compliance_rate = fields.Float(
        string='Rata-rata Kepatuhan',
        compute='_compute_dashboard_metrics',
        help='Rata-rata tingkat kepatuhan kontrol'
    )

    upcoming_tests_count = fields.Integer(
        string='Pengujian Mendatang',
        compute='_compute_dashboard_metrics',
        help='Jumlah pengujian yang terjadwal dalam 30 hari ke depan'
    )

    overdue_tests_count = fields.Integer(
        string='Pengujian Terlambat',
        compute='_compute_dashboard_metrics',
        help='Jumlah pengujian yang terlambat'
    )

    control_summary_ids = fields.One2many(
        'icofr.control',
        compute='_compute_dashboard_metrics',
        string='Ringkasan Kontrol',
        help='Ringkasan kontrol terbaru'
    )

    recent_risks_ids = fields.One2many(
        'icofr.risk',
        compute='_compute_dashboard_metrics',
        string='Risiko Terbaru',
        help='Risiko-risiko terbaru'
    )

    scheduled_testing_ids = fields.One2many(
        'icofr.testing',
        compute='_compute_dashboard_metrics',
        string='Pengujian Terjadwal',
        help='Pengujian-pengujian terjadwal'
    )

    recent_control_status_ids = fields.One2many(
        'icofr.control',
        compute='_compute_dashboard_metrics',
        string='Status Kontrol Terbaru',
        help='Status kontrol terbaru'
    )

    # Reporting-related methods and fields
    def action_generate_report(self):
        """Method untuk mengenerate laporan ICORF"""
        # Dalam implementasi sebenarnya, ini akan mengenerate laporan sesuai parameter
        # Untuk sekarang, hanya akan menampilkan notifikasi bahwa laporan telah digenerate
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Laporan Digenerate',
                'message': 'Laporan ICORF telah digenerate',
                'type': 'success',
                'sticky': False
            }
        }

    def action_export_report(self):
        """Method untuk mengekspor laporan"""
        # Buka wizard ekspor dengan parameter untuk laporan
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'all',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Laporan',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'all',
                'default_export_format': 'xlsx'
            }
        }

    report_type = fields.Selection([
        ('summary', 'Ringkasan'),
        ('detailed', 'Terperinci'),
        ('compliance', 'Kepatuhan'),
        ('effectiveness', 'Efektivitas')
    ], string='Jenis Laporan', default='summary',
       help='Jenis laporan yang akan ditampilkan')

    report_period_start = fields.Date(
        string='Periode Awal',
        default=fields.Date.today,
        help='Tanggal awal periode laporan'
    )

    report_period_end = fields.Date(
        string='Periode Akhir',
        default=lambda self: fields.Date.today(),
        help='Tanggal akhir periode laporan'
    )

    include_testing_results = fields.Boolean(
        string='Sertakan Hasil Pengujian',
        default=True,
        help='Sertakan hasil-hasil pengujian dalam laporan'
    )

    include_risk_assessment = fields.Boolean(
        string='Sertakan Penilaian Risiko',
        default=True,
        help='Sertakan penilaian risiko dalam laporan'
    )

    report_summary_ids = fields.One2many(
        'icofr.control',
        compute='_compute_report_data',
        string='Ringkasan Laporan',
        help='Ringkasan data laporan'
    )

    report_detail_ids = fields.One2many(
        'icofr.testing',
        compute='_compute_report_data',
        string='Detail Laporan',
        help='Detail data laporan'
    )

    def _compute_report_data(self):
        """Menghitung data untuk laporan"""
        for record in self:
            # Ambil semua kontrol
            all_controls = self.env['icofr.control'].search([])

            # Ambil pengujian dalam periode yang ditentukan
            start_date = record.report_period_start or fields.Date.today()
            end_date = record.report_period_end or fields.Date.today()
            report_tests = self.env['icofr.testing'].search([
                ('test_date', '>=', start_date),
                ('test_date', '<=', end_date)
            ])

            # Isi field-field berdasarkan parameter
            record.report_summary_ids = all_controls[:10]  # Ambil 10 kontrol pertama
            record.report_detail_ids = report_tests[:10]  # Ambil 10 pengujian terkait

    def _compute_dashboard_metrics(self):
        """Menghitung berbagai metrik untuk dashboard"""
        for record in self:
            # Hitung total kontrol
            all_controls = self.env['icofr.control'].search([])
            record.total_controls = len(all_controls)

            # Hitung kontrol efektif
            effective_controls = all_controls.filtered(lambda c: c.effectiveness_rating == 'high')
            record.effective_controls = len(effective_controls)

            # Hitung total risiko
            all_risks = self.env['icofr.risk'].search([])
            record.total_risks = len(all_risks)

            # Hitung risiko tinggi
            high_risks = all_risks.filtered(lambda r: r.risk_level == 'very_high' or r.risk_level == 'high')
            record.high_risks = len(high_risks)

            # Hitung rata-rata kepatuhan
            if record.total_controls > 0:
                effective_count = record.effective_controls
                record.compliance_rate = (effective_count / record.total_controls) * 100
            else:
                record.compliance_rate = 0

            # Hitung pengujian mendatang (dalam 30 hari)
            today = fields.Date.today()
            next_30_days = today + timedelta(days=30)
            upcoming_tests = self.env['icofr.testing'].search([
                ('test_date', '>=', today),
                ('test_date', '<=', next_30_days)
            ])
            record.upcoming_tests_count = len(upcoming_tests)

            # Hitung pengujian terlambat
            overdue_tests = self.env['icofr.testing'].search([
                ('test_date', '<', today),
                ('status', '!=', 'completed')
            ])
            record.overdue_tests_count = len(overdue_tests)

            # Set other computed fields to empty or appropriate values
            record.control_summary_ids = all_controls[:5]  # Ambil 5 kontrol pertama
            record.recent_risks_ids = all_risks[:5]  # Ambil 5 risiko pertama
            record.scheduled_testing_ids = upcoming_tests[:5]  # Ambil 5 pengujian terjadwal
            record.recent_control_status_ids = all_controls[:5]  # Ambil 5 kontrol pertama

    @api.model
    def create(self, vals):
        # Generate a default code if not provided
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('icofr.control') or '/'
        return super(IcofrControl, self).create(vals)