# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrApplication(models.Model):
    _name = 'icofr.application'
    _description = 'Aplikasi Signifikan (IT System)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Nama Aplikasi/Sistem', required=True, tracking=True)
    code = fields.Char('Kode Aplikasi', required=True)
    description = fields.Text('Deskripsi Fungsi Aplikasi')
    vendor = fields.Char('Developer/Vendor')
    
    # Bab III 1.5: Kriteria Signifikansi
    is_processes_auto_ctrl = fields.Boolean('Memproses Kontrol Otomatis?', help='Centang jika aplikasi menjalankan automated control.')
    is_processes_sig_account = fields.Boolean('Memproses Akun Signifikan?', help='Centang jika aplikasi memproses transaksi untuk akun di atas PM.')
    
    # ITGC Status
    itgc_status = fields.Selection([
        ('effective', 'ITGC Efektif'),
        ('ineffective', 'ITGC Tidak Efektif'),
        ('not_tested', 'Belum Diuji')
    ], string='Status ITGC', default='not_tested', tracking=True)
    
    control_ids = fields.One2many('icofr.control', 'application_id', string='Kontrol Terkait')
    
    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('deprecated', 'Ditinggalkan')
    ], string='Status', default='active')

    # Bab III 1.5 & FAQ 4: Efektivitas ITGC Aplikasi
    itgc_effectiveness = fields.Selection([
        ('effective', 'Efektif'),
        ('ineffective', 'Tidak Efektif'),
        ('not_assessed', 'Belum Dinilai')
    ], string='Efektivitas ITGC', default='not_assessed', tracking=True,
       help='Status efektivitas ITGC aplikasi ini. Jika Tidak Efektif, maka kontrol otomatis di dalamnya dianggap tidak dapat diandalkan (FAQ 4).')
    
    last_itgc_assessment_date = fields.Date('Tanggal Penilaian ITGC Terakhir')

    company_id = fields.Many2one('res.company', string='Perusahaan', default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    # _sql_constraints = [
    #     ('code_unique', 'unique(code, company_id)', 'Kode aplikasi harus unik per perusahaan!')
    # ]
