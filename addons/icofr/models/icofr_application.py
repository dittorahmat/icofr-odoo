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
    
    company_id = fields.Many2one('res.company', string='Perusahaan', required=True, default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_unique', 'unique(code, company_id)', 'Kode aplikasi harus unik per perusahaan!')
    ]
