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

    # RCM Minimum Info (Tabel 18 & 19)
    executing_department = fields.Char(
        string='Fungsi Pelaksana (Departemen)',
        help='Unit/Departemen yang menjalankan aktivitas pengendalian'
    )
    
    executing_job_title = fields.Char(
        string='Pelaku Pengendalian (Jabatan)',
        help='Posisi/Jabatan yang melakukan aktivitas pengendalian (misal: Kasir, Accounting Manager)'
    )

    supporting_app = fields.Char(
        string='Aplikasi Pendukung',
        help='Nama sistem/aplikasi yang menunjang kontrol (Wajib untuk Otomatis/ITDM)'
    )

    impacted_fsli_ids = fields.Many2many(
        'icofr.account.mapping',
        'icofr_control_fsli_rel',
        'control_id', 'fsli_id',
        string='Item Laporan Keuangan Terdampak',
        help='FSLI yang dimitigasi risikonya oleh kontrol ini'
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

    # IPO Attributes (SK BUMN Tabel 13 & Lampiran 5)
    ipo_completeness = fields.Boolean('IPO: Completeness', help='Menjamin seluruh transaksi tercatat')
    ipo_accuracy = fields.Boolean('IPO: Accuracy', help='Menjamin transaksi dicatat dengan nilai/periode tepat')
    ipo_validity = fields.Boolean('IPO: Validity', help='Menjamin hanya transaksi terotorisasi yang tercatat')
    ipo_restricted_access = fields.Boolean('IPO: Restricted Access', help='Menjamin data diproteksi dari akses tidak sah')

    control_type_detailed = fields.Selection([
        ('manual', 'Manual'),
        ('semi_manual', 'Semi-Manual'),
        ('automated', 'Otomatis'),
        ('manual_automatic', 'Manual dan Otomatis'),
        ('it_dependent', 'Berdasarkan IT')
    ], string='Tipe Kontrol Terperinci',
       help='Jenis kontrol yang lebih rinci')

    # Detailed Automated Types (Lampiran 5b Point xxvii)
    automated_control_type = fields.Selection([
        ('auto_control', 'Automated Control'),
        ('auto_calc', 'Automated Calculation'),
        ('restricted_access', 'Restricted Access'),
        ('interface', 'Interface')
    ], string='Jenis Otomatis Spesifik', help='Klasifikasi detail untuk kontrol otomatis sesuai Juknis')

    control_specific_type = fields.Selection([
        ('standard', 'Standar'),
        ('mrc', 'Management Review Control (MRC)'),
        ('euc', 'End User Computing (EUC)'),
        ('ipe', 'Information Produced by Entity (IPE)'),
        ('service_org', 'Service Organization (Pihak Ketiga)')
    ], string='Kategori Spesifik', default='standard',
       help='Kategori kontrol spesifik yang memerlukan prosedur validasi khusus sesuai Juknis')

    # ITGC Areas (SK BUMN Tabel 1)
    itgc_area = fields.Selection([
        ('prog_dev', 'Program Development'),
        ('prog_change', 'Program Changes'),
        ('comp_ops', 'Computer Operations'),
        ('access_data', 'Access to Program and Data')
    ], string='Area ITGC', help='4 Area Utama ITGC sesuai Tabel 1 Juknis BUMN')

    # EUC Attributes (SK BUMN Tabel 14)
    euc_complexity = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi')
    ], string='Kompleksitas EUC', help='Tingkat kompleksitas Spreadsheet/EUC')
    
    euc_has_version_ctrl = fields.Boolean('Version Control')
    euc_has_access_ctrl = fields.Boolean('Access Control')
    euc_has_change_ctrl = fields.Boolean('Change Control')
    euc_has_integrity_ctrl = fields.Boolean('Data Integrity')
    euc_has_availability_ctrl = fields.Boolean('Availability Control', help='Checklist availability sesuai Tabel 14')

    @api.constrains('control_specific_type', 'euc_complexity', 'euc_has_version_ctrl', 'euc_has_access_ctrl', 'euc_has_change_ctrl', 'euc_has_integrity_ctrl', 'euc_has_availability_ctrl')
    def _check_euc_minimum_controls(self):
        """
        Validation according to Table 14: Ilustrasi – Pengendalian Sesuai dengan Tingkat Kompleksitasnya.
        High Complexity EUC requires all 5 controls.
        """
        for record in self:
            if record.control_specific_type == 'euc' and record.euc_complexity == 'high':
                if not all([record.euc_has_version_ctrl, record.euc_has_access_ctrl, 
                           record.euc_has_change_ctrl, record.euc_has_integrity_ctrl, 
                           record.euc_has_availability_ctrl]):
                    raise ValidationError("Sesuai Juknis BUMN Tabel 14, EUC Kompleksitas Tinggi WAJIB memiliki seluruh kontrol: Version, Access, Change, Integrity, dan Availability!")

    # IPE Attributes (SK BUMN Tabel 15)
    ipe_type = fields.Selection([
        ('standard', 'Laporan Standar'),
        ('custom', 'Laporan Custom'),
        ('query', 'Laporan Query (Ad-hoc)')
    ], string='Tipe IPE', help='Jenis laporan yang dihasilkan sistem')

    # MRC Attributes (Bab III 2.2.c.2)
    mrc_precision_threshold = fields.Char(
        string='Threshold Presisi MRC',
        help='Contoh: Selisih > 5% atau > Rp 1 Miliar harus diinvestigasi'
    )

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
        ('draft', 'Draft'),
        ('waiting_l1_approval', 'Menunggu Persetujuan L1'),
        ('under_review', 'Review Lini 2'),
        ('waiting_l2_approval', 'Menunggu Persetujuan L2'),
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('obsolete', 'Usang')
    ], string='Status', default='draft', tracking=True,
       help='Status siklus hidup kontrol internal')

    # Effective Period (Lampiran 5)
    valid_from = fields.Date(string='Berlaku Sejak', help='Tanggal mulai efektif berlakunya kontrol')
    valid_to = fields.Date(string='Berlaku Hingga', help='Tanggal berakhirnya validitas kontrol (jika ada)')
    
    design_validation_ids = fields.One2many(
        'icofr.testing',
        'control_id',
        domain=[('test_type', '=', 'design_validation')],
        string='Validasi Rancangan',
        help='Riwayat validasi rancangan (Test of One) oleh Lini 2'
    )
    
    # --- Workflow Methods ---

    def action_submit_l1(self):
        """Lini 1 Staff submit ke Lini 1 Manager"""
        self.ensure_one()
        self.write({'status': 'waiting_l1_approval'})
        self.message_post(body="Kontrol disubmit oleh Staff Lini 1, menunggu persetujuan Manajer Unit.")

    def action_approve_l1(self):
        """Lini 1 Manager approve, lanjut ke Lini 2 Staff"""
        self.ensure_one()
        self.write({'status': 'under_review'})
        self.message_post(body="Kontrol disetujui Manajer Lini 1, diserahkan ke Tim ICORF (Lini 2) untuk review.")

    def action_verify_l2(self):
        """Lini 2 Staff verifikasi desain, lanjut ke Lini 2 Manager"""
        self.ensure_one()
        self.write({'status': 'waiting_l2_approval'})
        self.message_post(body="Desain divalidasi oleh Staff ICORF, menunggu final approval Manajer ICORF.")

    def action_approve_l2(self):
        """Lini 2 Manager final approve -> Active"""
        self.ensure_one()
        self.write({'status': 'active'})
        self.message_post(body="Kontrol RESMI AKTIF. Disetujui oleh Manajer ICORF.")

    def action_draft(self):
        """Reset ke Draft (Reject)"""
        self.ensure_one()
        self.write({'status': 'draft'})
        self.message_post(body="Kontrol dikembalikan ke status Draft (Revisi Diperlukan).")

    # Deprecated methods kept for compatibility if needed, redirected to new flow
    def action_submit(self):
        return self.action_submit_l1()

    def action_validate(self):
        return self.action_verify_l2()

    # --- Restored Fields ---

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