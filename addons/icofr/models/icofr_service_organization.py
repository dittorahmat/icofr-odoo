# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrServiceOrganization(models.Model):
    _name = 'icofr.service.organization'
    _description = 'Organisasi Jasa (Service Organization)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Organisasi Jasa', required=True, tracking=True)
    service_type = fields.Char(string='Jenis Layanan', help='Contoh: Payroll Outsourcing, Cloud Hosting, Asset Management')
    contact_person = fields.Char(string='Kontak Person')
    email = fields.Char(string='Email')
    
    soc_report_ids = fields.One2many(
        'icofr.soc.report', 
        'service_org_id', 
        string='Laporan SOC (1/2/3)'
    )
    
    control_ids = fields.One2many(
        'icofr.control',
        'service_org_id',
        string='Kontrol Terkait',
        help='Kontrol internal perusahaan yang dialihkan ke penyedia jasa ini.'
    )

    active = fields.Boolean('Aktif', default=True)

class IcofrSocReport(models.Model):
    _name = 'icofr.soc.report'
    _description = 'Laporan SOC (Service Organization Control)'
    _order = 'period_end desc'

    name = fields.Char(string='Nomor Laporan/Referensi', required=True)
    service_org_id = fields.Many2one('icofr.service.organization', string='Organisasi Jasa', required=True)
    
    report_type = fields.Selection([
        ('soc1_type1', 'SOC 1 Type 1'),
        ('soc1_type2', 'SOC 1 Type 2'),
        ('soc2_type1', 'SOC 2 Type 1'),
        ('soc2_type2', 'SOC 2 Type 2'),
        ('soc3', 'SOC 3')
    ], string='Tipe Laporan', required=True, default='soc1_type2')
    
    auditor_firm = fields.Char(string='Auditor Independen', help='Kantor Akuntan Publik yang menerbitkan laporan')
    period_start = fields.Date(string='Periode Awal')
    period_end = fields.Date(string='Periode Akhir')
    opinion_date = fields.Date(string='Tanggal Opini')
    
    conclusion = fields.Selection([
        ('unqualified', 'Wajar Tanpa Pengecualian (Unqualified)'),
        ('qualified', 'Wajar Dengan Pengecualian (Qualified)'),
        ('adverse', 'Tidak Wajar (Adverse)'),
        ('disclaimer', 'Tidak Memberikan Pendapat (Disclaimer)')
    ], string='Opini Auditor', required=True)
    
    cuec_review = fields.Text(
        string='Review CUEC (Complementary User Entity Controls)',
        help='Evaluasi atas kontrol yang harus dijalankan oleh perusahaan pengguna (User Entity) sesuai laporan SOC.'
    )
    
    bridge_letter_received = fields.Boolean(
        string='Bridge Letter Diterima?',
        help='Surat jembatan untuk menutup celah periode antara tanggal laporan SOC dan tanggal tutup buku perusahaan.'
    )
    
    attachment_id = fields.Many2one('ir.attachment', string='File Laporan')
