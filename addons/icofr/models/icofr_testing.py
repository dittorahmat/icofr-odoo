# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


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
    
    findings = fields.Text(
        string='Temuan',
        help='Temuan selama proses pengujian'
    )
    
    effectiveness = fields.Selection([
        ('effective', 'Efektif'),
        ('partially_effective', 'Efektif Sebagian'),
        ('ineffective', 'Tidak Efektif'),
        ('not_tested', 'Tidak Diuji')
    ], string='Efektivitas', required=True,
       help='Efektivitas kontrol berdasarkan hasil pengujian')
    
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
                continue

            if record.test_type != 'toe':
                record.sample_size_calculated = 0
                record.sample_size_recommended = "N/A"
                continue

            size = 0
            recommended = ""

            # TABLE 23: Remediation Testing Logic
            if record.is_remediation_test:
                mapping = {
                    'yearly': (1, "1"),
                    'quarterly': (2, "2"),
                    'monthly': (2, "2"),
                    'weekly': (5, "5"),
                    'daily': (15, "15"),
                    'per_transaction': (30, "30"),
                    'event_driven': (30, "30"),
                }
                val = mapping.get(freq, (25, "25"))
                size = val[0]
                recommended = val[1]
            
            # TABLE 22: Standard TOE Logic
            else:
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
                        size = 40 if risk == 'high' else 15
                        recommended = "15 - 40"
                    else: # > Daily / Per Transaction / Every Change / Event Driven
                        size = 60 if risk == 'high' else 30
                        recommended = "30 - 60"

            # Cap at population size if known
            if record.population_size > 0:
                size = min(size, record.population_size)
                
            record.sample_size_calculated = size
            record.sample_size_recommended = recommended
    
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