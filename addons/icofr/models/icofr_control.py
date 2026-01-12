# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class IcofrControl(models.Model):
    _name = 'icofr.control'
    _description = 'Master Data Kontrol Internal'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Kontrol',
        required=True,
        translate=True,
        tracking=True,
        help='Nama unik dari kontrol internal'
    )
    code = fields.Char(
        string='Kode Kontrol',
        required=True,
        copy=False,
        tracking=True,
        help='Kode unik untuk identifikasi kontrol'
    )
    control_type = fields.Selection([
        ('preventive', 'Preventif'),
        ('detective', 'Detektif'),
        ('corrective', 'Korektif')
    ], string='Jenis Kontrol', required=True, tracking=True,
       help='Jenis dari kontrol internal')
    
    frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('yearly', 'Tahunan'),
        ('every_change', 'Setiap Perubahan'),
        ('event_driven', 'Berdasarkan Kejadian'),
        ('per_transaction', 'Per Transaksi')
    ], string='Frekuensi', required=True, tracking=True,
       help='Frekuensi pelaksanaan kontrol')
    
    # Three Lines of Defense
    control_owner_line = fields.Selection([
        ('line_1', 'Lini 1 (Lini Bisnis)'),
        ('line_2', 'Lini 2 (Risk/ICOFR Team)'),
        ('line_3', 'Lini 3 (Internal Audit)')
    ], string='Lini Pemilik Kontrol', default='line_1', tracking=True,
       help='Lini pertahanan yang memiliki kontrol ini')

    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Kontrol',
        required=True,
        tracking=True,
        help='Pengguna yang bertanggung jawab atas kontrol ini'
    )

    # SK BUMN Attributes
    assertion_existence = fields.Boolean(
        string='Asersi Keberadaan',
        default=True,
        help='Kontrol ini menjamin keberadaan asersi'
    )

    assertion_completeness = fields.Boolean(
        string='Asersi Kelengkapan',
        default=True,
        help='Kontrol ini menjamin kelengkapan asersi'
    )

    assertion_accuracy = fields.Boolean(
        string='Asersi Akurasi',
        default=True,
        help='Kontrol ini menjamin akurasi asersi'
    )

    assertion_authorization = fields.Boolean(
        string='Asersi Otorisasi',
        default=True,
        help='Kontrol ini menjamin otorisasi asersi'
    )

    assertion_valuation = fields.Boolean(
        string='Asersi Valuasi',
        default=True,
        help='Kontrol ini menjamin valuasi asersi'
    )

    control_type_detailed = fields.Selection([
        ('manual', 'Manual'),
        ('semi_manual', 'Semi-Manual'),
        ('automated', 'Otomatis'),
        ('manual_automatic', 'Manual dan Otomatis'),
        ('it_dependent', 'Berdasarkan IT')
    ], string='Tipe Kontrol Terperinci',
       help='Jenis kontrol yang lebih rinci')

    control_specific_type = fields.Selection([
        ('standard', 'Standar'),
        ('mrc', 'Management Review Control (MRC)'),
        ('euc', 'End User Computing (EUC)'),
        ('ipe', 'Information Produced by Entity (IPE)'),
        ('service_org', 'Service Organization (Pihak Ketiga)')
    ], string='Kategori Spesifik', default='standard',
       help='Kategori kontrol spesifik yang memerlukan prosedur validasi khusus sesuai Juknis')

    control_risk_level = fields.Selection([
        ('low', 'Rendah'),
        ('high', 'Tinggi')
    ], string='Tingkat Risiko Pengendalian', default='low',
       required=True,
       help='Tingkat risiko pengendalian untuk penentuan jumlah sampel (Tabel 22 Juknis)')

    # SOC / Service Organization Fields
    service_provider_name = fields.Char(
        string='Nama Penyedia Jasa (Service Org)',
        help='Nama pihak ketiga/vendor jika kontrol dikelola oleh Service Organization'
    )
    
    soc_report_ref = fields.Char(
        string='Referensi Laporan SOC',
        help='Nomor/Tanggal Laporan SOC 1 Type 2 yang relevan'
    )

    frequency_detailed = fields.Selection([
        ('per_transaction', 'Per Transaksi'),
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('biweekly', 'Dua Mingguan'),
        ('monthly', 'Bulanan'),
        ('bimonthly', 'Dua Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('semiyearly', 'Semesteran'),
        ('yearly', 'Tahunan'),
        ('event_driven', 'Berdasarkan Kejadian')
    ], string='Frekuensi Terperinci', default='monthly',
       help='Frekuensi pelaksanaan kontrol secara terperinci')

    coso_element_id = fields.Many2one(
        'icofr.coso.element',
        string='Elemen COSO',
        help='Elemen dari kerangka kerja COSO 2013'
    )

    itgc_control = fields.Boolean(
        string='Kontrol ITGC',
        default=False,
        help='Apakah ini adalah kontrol ITGC (Information Technology General Controls)'
    )

    cobit_element_id = fields.Many2one(
        'icofr.cobit.element',
        string='Elemen COBIT',
        help='Elemen COBIT 2019 yang terkait dengan kontrol ini'
    )

    cobit_element_ids = fields.Many2many(
        'icofr.cobit.element',
        'icofr_control_cobit_rel',
        'control_id', 'cobit_element_id',
        string='Elemen-2 COBIT',
        help='Elemen-elemen COBIT 2019 yang terkait dengan kontrol ini'
    )

    monitoring_frequency = fields.Selection([
        ('continuous', 'Kontinu'),
        ('periodic', 'Periodik'),
        ('event_driven', 'Didorong Kejadian')
    ], string='Frekuensi Monitoring',
       help='Frekuensi monitoring kontrol ini')

    exception_handling_procedure = fields.Text(
        string='Prosedur Penanganan Pengecualian',
        help='Prosedur untuk menangani pengecualian dari kontrol ini'
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
        tracking=True,
        help='Risiko-risiko yang ditangani oleh kontrol ini'
    )

    key_performance_indicator = fields.Text(
        string='Indikator Kinerja Utama',
        help='Indikator kinerja untuk mengevaluasi efektivitas kontrol'
    )

    testing_frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('yearly', 'Tahunan'),
        ('event_driven', 'Berdasarkan Kejadian'),
        ('per_transaction', 'Per Transaksi')
    ], string='Frekuensi Pengujian', default='quarterly',
       help='Frekuensi pelaksanaan pengujian kontrol')

    testing_procedures = fields.Text(
        string='Prosedur Pengujian',
        tracking=True,
        help='Prosedur yang digunakan untuk menguji kontrol ini'
    )

    evidence_required = fields.Text(
        string='Bukti yang Diperlukan',
        help='Dokumentasi atau bukti yang diperlukan sebagai hasil pengujian'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('under_review', 'Dalam Review')
    ], string='Status', default='active',
       help='Status dari kontrol internal')
    
    design_validation_ids = fields.One2many(
        'icofr.testing',
        'control_id',
        domain=[('test_type', '=', 'design_validation')],
        string='Validasi Rancangan',
        help='Riwayat validasi rancangan (Test of One) oleh Lini 2'
    )

    design_effective = fields.Boolean(
        string='Rancangan Efektif',
        compute='_compute_design_effective',
        store=True,
        help='Status efektivitas rancangan berdasarkan validasi terakhir'
    )

    @api.depends('design_validation_ids.design_validation_conclusion')
    def _compute_design_effective(self):
        for record in self:
            last_validation = self.env['icofr.testing'].search([
                ('control_id', '=', record.id),
                ('test_type', '=', 'design_validation')
            ], order='test_date desc', limit=1)
            
            if last_validation and last_validation.design_validation_conclusion == 'effective':
                record.design_effective = True
            else:
                record.design_effective = False

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

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki kontrol ini'
    )

    significance_level = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('significant', 'Signifikan'),
        ('high', 'Tinggi'),
        ('critical', 'Kritis')
    ], string='Tingkat Signifikansi', default='medium',
       help='Tingkat signifikansi dari kontrol internal')

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait kontrol'
    )

    change_log_ids = fields.One2many(
        'icofr.change.log',
        'control_id',
        string='Log Perubahan',
        help='Riwayat perubahan pada kontrol ini sesuai Lampiran 6 SK BUMN'
    )
    
    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            controls = self.search([('code', '=', record.code)])
            if len(controls) > 1:
                raise ValidationError("Kode kontrol harus unik!")
    
    def action_submit(self):
        """Method to submit control for review by Line 2"""
        self.ensure_one()
        self.write({
            'status': 'under_review'
        })
        # Send notification
        self.message_post(
            body=f"Kontrol telah disubmit untuk review oleh {self.env.user.name}",
            subtype_xmlid='mail.mt_comment'
        )
        return True

    def action_validate(self):
        """Method for Line 2 to validate control design"""
        self.ensure_one()
        self.write({
            'status': 'active'
        })
        self.message_post(
            body=f"Desain kontrol telah divalidasi oleh {self.env.user.name}",
            subtype_xmlid='mail.mt_comment'
        )
        return True

    # Dashboard-related methods and fields
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

    @api.model
    def create(self, vals):
        # Ensure vals is a dictionary and not a list by checking the first element if needed
        if isinstance(vals, list):
            # If vals is a list (for multiple creation), process each item
            processed_vals = []
            for val_dict in vals:
                if isinstance(val_dict, dict):
                    if 'code' not in val_dict or not val_dict.get('code'):
                        val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.control') or '/'
                    processed_vals.append(val_dict)
            return super(IcofrControl, self).create(processed_vals)
        else:
            # For single record creation (most common case)
            if 'code' not in vals or not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('icofr.control') or '/'
            return super(IcofrControl, self).create(vals)