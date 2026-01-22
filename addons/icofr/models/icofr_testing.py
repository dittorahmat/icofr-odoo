# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class IcofrTesting(models.Model):
    _name = 'icofr.testing'
    _description = 'Pengujian Kontrol Internal'
    _order = 'test_date desc'

    code = fields.Char(
        string='Kode Pengujian',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('icofr.testing') or '/',
        help='Kode unik untuk identifikasi pengujian'
    )

    name = fields.Char(
        string='Nama Pengujian',
        required=True,
        help='Nama unik dari pengujian kontrol'
    )
    
    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol yang Diuji',
        required=True,
        help='Kontrol internal yang menjadi subjek pengujian'
    )
    
    test_type = fields.Selection([
        ('design_validation', 'Validasi Rancangan (Test of One)'),
        ('tod', 'Test of Design (TOD)'),
        ('toe', 'Test of Operating Effectiveness (TOE)'),
        ('walkthrough', 'Walkthrough'),
        ('compliance', 'Kepatuhan (General)'),
        ('substantive', 'Substantif')
    ], string='Jenis Pengujian', required=True,
       default='design_validation',
       help='Jenis dari pengujian kontrol (Validasi Rancangan oleh Lini 2, TOD/TOE oleh Lini 3)')
    
    # TOD Specific Fields
    design_description = fields.Text(
        string='Deskripsi Desain Kontrol',
        help='Evaluasi apakah desain kontrol secara logis dapat memitigasi risiko'
    )
    
    design_conclusion = fields.Selection([
        ('effective', 'Desain Efektif'),
        ('ineffective', 'Desain Tidak Efektif')
    ], string='Kesimpulan Desain',
       help='Kesimpulan atas efektivitas rancangan pengendalian (TOD)')

    # Lampiran 8: Detail Verifikasi Rancangan (Checklist)
    tod_objective_attainment = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Pencapaian Objektif')
    tod_timing_accuracy = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Ketepatan Waktu/Frekuensi')
    tod_authority_competence = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Wewenang & Kompetensi')
    tod_info_reliability = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Keandalan Informasi')
    tod_period_coverage = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Cakupan Periode')
    tod_evidence_sufficiency = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Kecukupan Bukti')

    # Tabel 20: Atribut IPE (Information Produced by Entity)
    ipe_parameter_verified = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Verifikasi Parameter Laporan')
    ipe_extraction_valid = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Validitas Ekstraksi Data')
    ipe_itgc_effective = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Kecukupan ITGC Aplikasi')

    # Tabel 21: Atribut MRC (Management Review Control)
    mrc_skepticism_applied = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Penerapan Professional Skepticism')
    mrc_threshold_appropriate = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Kesesuaian Ambang Batas (Threshold)')
    mrc_reperformance_done = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Pelaksanaan Reperformance Analisis')
    mrc_investigation_proven = fields.Selection([('pass', 'Ya'), ('fail', 'Tidak')], string='Bukti Investigasi Anomali')

    # Design Validation Specific Fields (Line 2)
    design_validation_conclusion = fields.Selection([
        ('effective', 'Rancangan Efektif'),
        ('ineffective', 'Rancangan Tidak Efektif'),
        ('no_transaction', 'Tidak Ada Transaksi')
    ], string='Kesimpulan Validasi Rancangan',
       help='Kesimpulan atas validasi rancangan (Test of One) oleh Lini 2')

    # TOE Specific Fields
    population_reference = fields.Char(
        string='Referensi Populasi',
        help='Keterangan mengenai sumber populasi data (misalnya: Jurnal Penjualan Jan-Des)'
    )
    
    sample_selection_method = fields.Selection([
        ('random', 'Acak'),
        ('systematic', 'Sistematik'),
        ('judgmental', 'Penilaian Profesional'),
        ('block', 'Blok')
    ], string='Metode Pemilihan Sampel',
       help='Metode yang digunakan untuk memilih sampel dari populasi')
    
    testing_steps = fields.Text(
        string='Langkah-langkah Pengujian',
        help='Rincian langkah yang dilakukan saat menguji sampel'
    )
    
    exceptions_noted = fields.Text(
        string='Pengecualian yang Ditemukan',
        help='Rincian jika ditemukan sampel yang gagal atau tidak sesuai'
    )

    # Tabel 22 Note **: Sampel harus mencakup Desember/Kuartal IV
    has_december_sample = fields.Boolean(
        string='Mencakup Sampel Desember/Q4?',
        help='Centang jika pengujian telah menyertakan sampel dari bulan Desember atau Kuartal IV (Wajib untuk frekuensi Bulanan/Kuartalan).'
    )

    test_date = fields.Date(
        string='Tanggal Pengujian',
        required=True,
        default=fields.Date.today,
        help='Tanggal pelaksanaan pengujian'
    )
    
    tester_id = fields.Many2one(
        'res.users',
        string='Pelaksana Pengujian',
        required=True,
        help='Pengguna yang melaksanakan pengujian'
    )
    
    sample_size = fields.Integer(
        string='Ukuran Sampel',
        help='Jumlah sampel yang diuji'
    )
    
    testing_procedures = fields.Text(
        string='Prosedur Pengujian',
        help='Prosedur yang diikuti dalam pengujian ini'
    )
    
    test_results = fields.Text(
        string='Hasil Pengujian',
        help='Hasil dari pengujian kontrol'
    )

    # Roll-forward Logic (Hal 51)
    is_roll_forward = fields.Boolean(
        string='Pengujian Roll-forward',
        default=False,
        help='Centang jika ini adalah pengujian pemutakhiran (Roll-forward) dari pengujian interim.'
    )
    original_test_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian Interim Asal',
        help='Referensi ke pengujian interim yang di-roll forward.'
    )
    roll_forward_period = fields.Char(
        string='Periode Pemutakhiran',
        help='Misal: Oktober - Desember'
    )
    
    findings = fields.Text(
        string='Temuan',
        help='Temuan selama proses pengujian'
    )

    # Bab V 1.1: Metode Pengujian (Gambar 4)
    testing_method = fields.Selection([
        ('inquiry', 'Wawancara (Inquiry)'),
        ('observation', 'Observasi (Observation)'),
        ('inspection', 'Inspeksi Dokumen/Fisik (Inspection)'),
        ('reperformance', 'Pelaksanaan Kembali (Reperformance)'),
        ('data_analysis', 'Analisis Data (CAATs)')
    ], string='Metode Pengujian Utama', help='Metode yang digunakan sesuai Gambar 4 Juknis BUMN. Kombinasi metode disarankan untuk bukti yang lebih kuat.')
    
    testing_method_detail = fields.Text(
        string='Rincian Metode',
        help='Jelaskan bagaimana metode diterapkan (misal: Wawancara dengan siapa, dokumen apa yang diinspeksi).'
    )

    effectiveness = fields.Selection([
        ('effective', 'Efektif'),
        ('partially_effective', 'Efektif Sebagian'),
        ('ineffective', 'Tidak Efektif'),
        ('no_transaction', 'Tidak Ada Transaksi (N/A)'),
        ('not_tested', 'Tidak Diuji')
    ], string='Efektivitas', required=True,
       help='Efektivitas kontrol berdasarkan hasil pengujian (termasuk opsi No Transaction sesuai Hal 59)')
    
    status = fields.Selection([
        ('planned', 'Terjadwal'),
        ('in_progress', 'Dalam Proses'),
        ('completed', 'Selesai'),
        ('reviewed', 'Direview'),
        ('approved', 'Disetujui')
    ], string='Status Pengujian', default='planned',
       help='Status dari proses pengujian')

    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti yang mendukung hasil pengujian'
    )

    # Lampiran 7: Atribut Pengujian (Checklist Format)
    attr_a_desc = fields.Char('Deskripsi Atribut A')
    attr_b_desc = fields.Char('Deskripsi Atribut B')
    attr_c_desc = fields.Char('Deskripsi Atribut C')
    attr_d_desc = fields.Char('Deskripsi Atribut D')

    is_remediation_test = fields.Boolean(
        string='Pengujian Remediasi',
        default=False,
        help='Centang jika ini adalah pengujian ulang setelah perbaikan (Remediasi) sesuai Tabel 23 Juknis'
    )
    
    action_plan_id = fields.Many2one(
        'icofr.action.plan',
        string='Rencana Aksi Terkait',
        help='Rencana aksi yang diperbaiki dan sekarang sedang diuji ulang (Wajib untuk remediasi)'
    )
    
    remediation_min_period = fields.Char(
        string='Periode Minimum (Remediasi)',
        compute='_compute_sample_size',
        store=True,
        help='Periode pengoperasian baru sebelum boleh diuji ulang sesuai Tabel 23.'
    )

    @api.constrains('tester_id', 'control_id', 'test_date')
    def _check_cooling_off_period(self):
        """
        Hal 19 Juknis BUMN: Prinsip Objektivitas & Integritas.
        Auditor (Lini 3) dilarang melakukan audit terhadap aktivitas yang menjadi 
        tanggung jawabnya (sebagai Lini 1) dalam waktu 1 (satu) tahun terakhir.
        """
        for record in self:
            if record.test_type in ['tod', 'toe']:
                # Cari riwayat log perubahan atau kepemilikan kontrol
                # Cek jika tester pernah menjadi owner_id kontrol ini dalam 12 bulan terakhir
                twelve_months_ago = record.test_date - timedelta(days=365)
                
                # 1. Cek owner saat ini (Jika tester adalah owner saat ini -> Pelanggaran)
                if record.control_id.owner_id == record.tester_id:
                    raise ValidationError(
                        f"Pelanggaran Prinsip Objektivitas (Hal 19): Auditor {record.tester_id.name} "
                        f"adalah Pemilik Pengendalian (Owner) saat ini. Auditor dilarang menguji kontrol milik sendiri."
                    )
                
                # 2. Cek riwayat perubahan owner (jika ada model change log atau auditor tercatat di log)
                past_changes = self.env['icofr.change.log'].search([
                    ('control_id', '=', record.control_id.id),
                    ('control_owner_id', '=', record.tester_id.id),
                    ('date_effective', '>=', twelve_months_ago)
                ])
                
                if past_changes:
                    last_change = past_changes[0]
                    raise ValidationError(
                        f"Pelanggaran Cooling-off Period (Hal 19): Auditor {record.tester_id.name} "
                        f"tercatat pernah mengelola/memiliki kontrol ini pada {last_change.date_effective}. "
                        f"Auditor harus menunggu minimal 12 bulan sejak tanggal tersebut sebelum diperbolehkan menguji kembali."
                    )

    @api.constrains('is_remediation_test', 'test_date', 'action_plan_id')
    def _check_remediation_wait_period(self):
        """
        Tabel 23 (Hal 98): Kontrol yang diremediasi wajib beroperasi minimal selama 
        periode tertentu sebelum boleh di-retest.
        Contoh: Harian (30 hari), Mingguan (5 minggu), Bulanan (3 bulan).
        """
        # Skip during installation, import or module upgrade
        # Skip during installation, import or module upgrade
        if self.env.context.get('install_mode') or self.env.context.get('import_file') or self.env.context.get('module_upgrade'):
            return

        for record in self:
            if record.is_remediation_test and record.action_plan_id:
                if not record.action_plan_id.actual_completion_date:
                    raise ValidationError("Rencana aksi harus memiliki 'Tanggal Penyelesaian Aktual' sebelum dapat diuji ulang!")
                
                # Hitung selisih hari
                completion_date = record.action_plan_id.actual_completion_date
                test_date = record.test_date
                days_passed = (test_date - completion_date).days
                
                # Map wait days according to Table 23
                freq = record.control_id.frequency
                wait_days_map = {
                    'daily': 30,
                    'weekly': 35, # 5 weeks
                    'monthly': 90, # 3 months
                    'quarterly': 180, # 2 quarters
                    'yearly': 365,
                }
                min_days = wait_days_map.get(freq, 25) # Default 25 transactions for others
                
                if days_passed < min_days:
                    raise ValidationError(
                        f"Pelanggaran Tabel 23: Kontrol {freq} wajib beroperasi minimal {min_days} hari "
                        f"sejak remediasi selesai ({completion_date}) sebelum diuji ulang. "
                        f"Baru berjalan {days_passed} hari. Retest paling cepat tanggal {completion_date + timedelta(days=min_days)}."
                    )

    remediation_min_period = fields.Char(
        string='Periode Minimum (Remediasi)',
        compute='_compute_sample_size',
        store=True,
        help='Periode pengoperasian baru sebelum boleh diuji ulang sesuai Tabel 23.'
    )
    
    sample_size_recommended = fields.Char(
        string='Rekomendasi Jumlah Sampel',
        compute='_compute_sample_size',
        store=True,
        help='Rentang jumlah sampel yang disarankan sesuai Tabel 22/23 Juknis BUMN'
    )

    # Fields for sampling calculator according to SK BUMN
    control_frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('yearly', 'Tahunan'),
        ('event_driven', 'Berdasarkan Kejadian'),
        ('per_transaction', 'Per Transaksi')
    ], string='Frekuensi Kontrol',
       help='Frekuensi pelaksanaan kontrol yang diuji')

    population_size = fields.Integer(
        string='Ukuran Populasi',
        help='Jumlah total item dalam populasi kontrol'
    )

    sample_size_calculated = fields.Integer(
        string='Ukuran Sampel (Target)',
        compute='_compute_sample_size',
        store=True,
        help='Jumlah sampel minimal yang harus diuji sesuai kalkulator sampling'
    )

    sampling_method = fields.Selection([
        ('random', 'Acak'),
        ('systematic', 'Sistematik'),
        ('judgmental', 'Penilaian Profesional'),
        ('block', 'Blok'),
        ('statistical', 'Statistikal')
    ], string='Metode Sampling', default='random',
       help='Metode sampling yang digunakan')

    confidence_level = fields.Float(
        string='Tingkat Kepercayaan (%)',
        default=95.0,
        help='Tingkat kepercayaan untuk sampling (dalam persen)'
    )

    monetary_impact_threshold = fields.Float(
        string='Ambang Dampak Moneter',
        help='Ambang batas dampak moneter untuk penilaian temuan'
    )

    testing_workspace = fields.Html(
        string='Ruang Kerja Pengujian',
        help='Area kerja untuk mendokumentasikan hasil pengujian'
    )

    @api.depends('test_type', 'control_frequency', 'population_size', 'is_remediation_test', 'control_id.control_risk_level', 'control_id.control_type_detailed')
    def _compute_sample_size(self):
        """
        Compute sample size according to Table 22 (TOE) and Table 23 (Remediation)
        of Juknis ICOFR BUMN (SK-5/DKU.MBU/11/2024)
        """
        for record in self:
            risk = record.control_id.control_risk_level or 'low'
            freq = record.control_frequency or record.control_id.frequency
            
            if record.test_type == 'design_validation':
                record.sample_size_calculated = 1
                record.sample_size_recommended = "1 (Test of One)"
                record.remediation_min_period = "N/A"
                continue

            if record.test_type != 'toe':
                record.sample_size_calculated = 0
                record.sample_size_recommended = "N/A"
                record.remediation_min_period = "N/A"
                continue

            size = 0
            recommended = ""
            min_period = ""

            # TABLE 23: Remediation Testing Logic
            if record.is_remediation_test:
                mapping = {
                    'yearly': (1, "1", "1 Tahun"),
                    'quarterly': (2, "2", "2 Kuartal"),
                    'monthly': (2, "2", "3 Bulan"),
                    'weekly': (5, "5", "5 Minggu"),
                    'daily': (15, "15", "30 Hari"),
                    'per_transaction': (30, "30", "25 Kali (Beberapa Hari)"),
                    'event_driven': (30, "30", "25 Kali (Beberapa Hari)"),
                }
                val = mapping.get(freq, (25, "25", "Variatif"))
                size = val[0]
                recommended = val[1]
                min_period = val[2]
            
            # TABLE 22: Standard TOE Logic
            else:
                record.remediation_min_period = "N/A"
                if record.control_id.control_type_detailed == 'automated':
                    size = 1
                    recommended = "1 (Per Skenario)"
                else:
                    if freq == 'yearly':
                        size = 1
                        recommended = "1"
                    elif freq == 'quarterly':
                        size = 3 if risk == 'high' else 2
                        recommended = "2 - 3"
                    elif freq == 'monthly':
                        size = 5 if risk == 'high' else 2
                        recommended = "2 - 5"
                    elif freq == 'weekly':
                        size = 15 if risk == 'high' else 5
                        recommended = "5 - 15"
                    elif freq == 'daily':
                        size = 40 if risk == 'high' else 25
                        recommended = "25 - 40"
                    else: # > Daily / Per Transaction / Every Change / Event Driven
                        # Table 22 (Hal 97) Rules for Populations:
                        pop_size = record.population_size
                        if pop_size > 0:
                            if pop_size <= 50:
                                size = pop_size if risk == 'high' else max(2, int(pop_size * 0.1))
                            elif pop_size <= 250:
                                size = min(25, max(10, int(pop_size * 0.1)))
                            else:
                                size = 25
                            recommended = f"Formula Tabel 22 (Populasi: {pop_size})"
                        else:
                            size = 60 if risk == 'high' else 25
                            recommended = "25 - 60 (Populasi Belum Diketahui)"

            # Cap at population size if known
            if record.population_size > 0:
                size = min(size, record.population_size)
                
            record.sample_size_calculated = size
            record.sample_size_recommended = recommended
            if record.is_remediation_test:
                record.remediation_min_period = min_period
    
    recommendation = fields.Text(
        string='Rekomendasi',
        help='Rekomendasi untuk perbaikan kontrol jika diperlukan'
    )
    
    due_date = fields.Date(
        string='Tanggal Jatuh Tempo',
        help='Tanggal jatuh tempo pelaksanaan pengujian'
    )
    
    completion_date = fields.Date(
        string='Tanggal Selesai',
        help='Tanggal sebenarnya pengujian selesai'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki pengujian ini'
    )

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait pengujian'
    )

    schedule_id = fields.Many2one(
        'icofr.testing.schedule',
        string='Jadwal Terkait',
        help='Jadwal yang terkait dengan pengujian ini'
    )

    sample_ids = fields.One2many(
        'icofr.audit.population',
        'testing_id',
        string='Sampel Terpilih',
        help='Item populasi yang dipilih sebagai sampel untuk pengujian ini'
    )
    
    @api.constrains('control_frequency', 'has_december_sample', 'status')
    def _check_december_sampling(self):
        """
        Validation according to Table 22:
        Untuk pengendalian dengan frekuensi bulanan dan kuartalan, sampel pengujian harus mencakup Kuartal Keempat dan bulan Desember.
        """
        for record in self:
            if record.status == 'completed' and record.test_type == 'toe':
                if record.control_frequency in ['monthly', 'quarterly'] and not record.has_december_sample:
                    raise ValidationError("Sesuai Juknis BUMN Tabel 22, pengujian untuk frekuensi Bulanan/Kuartalan WAJIB menyertakan sampel dari bulan Desember/Kuartal IV!")

    # Hal 51: Prosedur Roll-forward untuk Pengujian Interim
    is_interim_test = fields.Boolean(
        string='Pengujian Interim?',
        help='Centang jika pengujian dilakukan sebelum akhir tahun (misal: s/d Sept) dan memerlukan roll-forward.'
    )
    
    roll_forward_required = fields.Boolean(
        string='Wajib Roll-forward?',
        compute='_compute_roll_forward_required',
        store=True,
        help='Otomatis True jika pengujian interim dilakukan jauh sebelum tanggal tutup buku.'
    )
    
    roll_forward_procedures = fields.Text(
        string='Prosedur Roll-forward',
        help='Prosedur tambahan (Inquiry/Observation) untuk memastikan kontrol tetap efektif dari tanggal interim s/d akhir tahun.'
    )
    
    roll_forward_conclusion = fields.Selection([
        ('effective', 'Tetap Efektif'),
        ('ineffective', 'Menjadi Tidak Efektif'),
        ('not_done', 'Belum Dilaksanakan')
    ], string='Kesimpulan Roll-forward', default='not_done')

    @api.depends('is_interim_test', 'test_date')
    def _compute_roll_forward_required(self):
        for record in self:
            # Jika interim dan dilakukan sebelum November, wajib roll-forward (Hal 51)
            if record.is_interim_test and record.test_date and record.test_date.month < 11:
                record.roll_forward_required = True
            else:
                record.roll_forward_required = False

    @api.constrains('tester_id', 'control_id', 'test_date')
    def _check_auditor_cooling_off(self):
        """
        Hal 19 Juknis BUMN: Auditor Internal (Lini 3) tidak boleh menguji aktivitas 
        yang pernah menjadi tanggung jawabnya dalam 12 bulan terakhir.
        """
        # Skip validation during installation, import or module upgrade
        # Skip during installation, import or module upgrade
        if self.env.context.get('install_mode') or self.env.context.get('import_file') or self.env.context.get('module_upgrade'):
            return

        for record in self:
            if not record.tester_id or not record.control_id or not record.test_date:
                continue
            
            twelve_months_ago = record.test_date - timedelta(days=365)
            
            # 1. Check if tester was the owner (Lini 1)
            if record.control_id.owner_id == record.tester_id:
                raise ValidationError(
                    f"Pelanggaran Cooling-off (Hal 19): {record.tester_id.name} adalah pemilik kontrol ini. "
                    "Auditor tidak boleh menguji kontrol yang dikelolanya sendiri."
                )
            
            # 2. Check if tester performed Lini 2 validation in the last 12 months
            previous_l2_checks = self.env['icofr.testing'].search([
                ('control_id', '=', record.control_id.id),
                ('tester_id', '=', record.tester_id.id),
                ('test_type', '=', 'design_validation'),
                ('test_date', '>', twelve_months_ago),
                ('id', '!=', record.id)
            ])
            
            if previous_l2_checks:
                raise ValidationError(
                    f"Pelanggaran Cooling-off (Hal 19): {record.tester_id.name} pernah melakukan validasi desain (Lini 2) "
                    f"untuk kontrol ini pada {previous_l2_checks[0].test_date}. "
                    "Wajib ada masa jeda 12 bulan sebelum dapat melakukan pengujian Lini 3."
                )

    @api.onchange('control_id')
    def _onchange_control_id(self):
        """Isi field testing_procedures dengan prosedur dari kontrol jika kosong"""
        if self.control_id and not self.testing_procedures:
            self.testing_procedures = self.control_id.testing_procedures
    
    @api.constrains('test_date', 'completion_date')
    def _check_dates(self):
        """Validasi tanggal pengujian"""
        for record in self:
            if record.test_date and record.completion_date and record.test_date > record.completion_date:
                raise ValidationError("Tanggal pengujian tidak boleh setelah tanggal selesai!")
    
    def create_approval_workflow(self):
        """Method untuk membuat workflow persetujuan untuk pengujian"""
        self.ensure_one()
        # Implementasi sederhana: buat entri workflow baru
        workflow = self.env['icofr.workflow'].create({
            'name': f'Workflow Pengujian: {self.name}',
            'model_ref': f'icofr.testing,{self.id}',
            'initiator_id': self.tester_id.id,
            'status': 'active'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Workflow Persetujuan',
            'res_model': 'icofr.workflow',
            'res_id': workflow.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_complete_testing(self):
        """Method untuk menandai pengujian sebagai selesai"""
        self.ensure_one()
        self.write({
            'status': 'completed',
            'completion_date': fields.Date.today()
        })
        return True

    def action_export_testing(self):
        """Method untuk membuka wizard ekspor pengujian"""
        self.ensure_one()
        # Buka wizard ekspor dengan parameter yang sesuai
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'testing',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Pengujian Kontrol',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'testing',
                'default_export_format': 'xlsx'
            }
        }

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    # Generate name based on control if not provided
                    control_id = new_val_dict.get('control_id')
                    if isinstance(control_id, int):
                        # Control reference is resolved, generate name
                        control = self.env['icofr.control'].browse(control_id)
                        new_val_dict['name'] = f'Pengujian {control.name or "Kontrol"} - {fields.Date.to_string(fields.Date.today())}'
                    # If control_id is not resolved, skip name generation for now
                processed_vals.append(new_val_dict)
            return super(IcofrTesting, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                control_id = new_vals.get('control_id')
                if isinstance(control_id, int):
                    # Control reference is resolved, generate name
                    control = self.env['icofr.control'].browse(control_id)
                    new_vals['name'] = f'Pengujian {control.name or "Kontrol"} - {fields.Date.to_string(fields.Date.today())}'
                # If control_id is not resolved, skip name generation for now
            return super(IcofrTesting, self).create(new_vals)

    # --- New Relations for Lampiran 7 Compliance ---
    line1_contact_ids = fields.One2many(
        'icofr.testing.line1.contact', 
        'testing_id', 
        string='Personil Pelaksana Pengendalian (Lini 1)',
        help='Daftar personil yang menjalankan aktivitas pengendalian sesuai Lampiran 7.'
    )

    itac_scenario_ids = fields.One2many(
        'icofr.testing.itac.scenario',
        'testing_id',
        string='Detail Skenario ITAC',
        help='Dokumentasi skenario pengujian kontrol otomatis sesuai Lampiran 7 Hal 101.'
    )

class IcofrTestingLine1Contact(models.Model):
    """Lampiran 7 Hal 99: Kontak Informasi Pelaksana Pengendalian"""
    _name = 'icofr.testing.line1.contact'
    _description = 'Kontak Personil Pelaksana Lini 1'

    testing_id = fields.Many2one('icofr.testing', string='Pengujian', ondelete='cascade')
    name = fields.Char('Nama Personel', required=True)
    position = fields.Char('Jabatan/Posisi', required=True)
    email = fields.Char('Email')
    department = fields.Char('Unit Kerja')

class IcofrTestingItacScenario(models.Model):
    """Lampiran 7 Hal 101: Format Hasil Pengujian ITAC"""
    _name = 'icofr.testing.itac.scenario'
    _description = 'Skenario Pengujian ITAC'

    testing_id = fields.Many2one('icofr.testing', string='Pengujian', ondelete='cascade')
    scenario_name = fields.Char('Skenario ITAC', required=True, help='Contoh: Input nilai minus, Transaksi > limit, dll.')
    expected_result = fields.Text('Hasil yang Diharapkan')
    actual_result = fields.Text('Hasil Aktual/Hasil Pengujian')
    is_deficient = fields.Boolean('Defisiensi?', help='Centang jika hasil aktual tidak sesuai harapan.')
    notes = fields.Text('Keterangan')