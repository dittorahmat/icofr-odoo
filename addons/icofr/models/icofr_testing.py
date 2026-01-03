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
        ('tod', 'Test of Design (TOD)'),
        ('toe', 'Test of Operating Effectiveness (TOE)'),
        ('walkthrough', 'Walkthrough'),
        ('compliance', 'Kepatuhan (General)'),
        ('substantive', 'Substantif')
    ], string='Jenis Pengujian', required=True,
       default='toe',
       help='Jenis dari pengujian kontrol (TOD atau TOE sesuai Juknis)')
    
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

    # Fields for sampling calculator according to SK BUMN
    control_frequency = fields.Selection([
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
        ('monthly', 'Bulanan'),
        ('quarterly', 'Triwulanan'),
        ('yearly', 'Tahunan')
    ], string='Frekuensi Kontrol',
       help='Frekuensi pelaksanaan kontrol yang diuji')

    population_size = fields.Integer(
        string='Ukuran Populasi',
        help='Jumlah total item dalam populasi kontrol'
    )

    sample_size_calculated = fields.Integer(
        string='Ukuran Sampel Terhitung',
        compute='_compute_sample_size',
        help='Ukuran sampel yang dihitung menggunakan kalkulator sampling'
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

    @api.depends('test_type', 'control_frequency', 'population_size', 'confidence_level', 'control_id.control_risk_level', 'control_id.control_type_detailed')
    def _compute_sample_size(self):
        """
        Compute sample size based on frequency and risk level according to 
        Table 22: Ilustrasi - Penentuan Jumlah Sampel (Juknis ICOFR BUMN)
        """
        for record in self:
            # Default to 0 if not TOE
            if record.test_type != 'toe':
                record.sample_size_calculated = 0
                continue

            size = 0
            # Check for Automated Controls (1 sample per scenario)
            if record.control_id.control_type_detailed == 'automated':
                size = 1
            else:
                # Manual / ITDM Controls logic based on Frequency & Risk
                risk = record.control_id.control_risk_level or 'low'
                freq = record.control_frequency or record.control_id.frequency
                
                if freq == 'yearly': # Tahunan
                    size = 1
                elif freq == 'quarterly': # Kuartalan
                    size = 2 if risk == 'low' else 3
                elif freq == 'monthly': # Bulanan
                    size = 2 if risk == 'low' else 5
                elif freq == 'weekly': # Mingguan
                    size = 5 if risk == 'low' else 15
                elif freq == 'daily': # Harian
                    size = 15 if risk == 'low' else 40
                elif freq in ('per_transaction', 'every_change', 'event_driven'): 
                    size = 30 if risk == 'low' else 60
                else:
                    size = 25

            # Cap at population size if known and non-zero
            if record.population_size and record.population_size > 0:
                size = min(size, record.population_size)
                
            record.sample_size_calculated = size
    
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