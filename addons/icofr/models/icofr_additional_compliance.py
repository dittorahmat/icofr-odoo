# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrServiceOrganization(models.Model):
    _name = 'icofr.service.organization'
    _description = 'Organisasi Layanan (Pihak Ketiga)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nama Organisasi', required=True, tracking=True)
    code = fields.Char('Kode Vendor')
    service_description = fields.Text('Deskripsi Layanan')
    contact_person = fields.Char('Kontak Person')
    email = fields.Char('Email')
    phone = fields.Char('Telepon')
    
    soc_report_ids = fields.One2many('icofr.soc.report', 'service_org_id', string='Laporan SOC')
    control_ids = fields.One2many('icofr.control', 'service_org_id', string='Kontrol Terkait')

    active = fields.Boolean(default=True)

class IcofrSocReport(models.Model):
    _name = 'icofr.soc.report'
    _description = 'Laporan Service Organisation Control (SOC)'
    _order = 'period_end desc'

    name = fields.Char('Judul Laporan', required=True)
    service_org_id = fields.Many2one('icofr.service.organization', string='Organisasi Layanan', required=True)
    report_type = fields.Selection([
        ('soc1_t1', 'SOC 1 Type I'),
        ('soc1_t2', 'SOC 1 Type II'),
        ('soc2_t1', 'SOC 2 Type I'),
        ('soc2_t2', 'SOC 2 Type II'),
        ('other', 'Lainnya')
    ], string='Tipe Laporan', default='soc1_t2', required=True)
    
    period_start = fields.Date('Periode Mulai')
    period_end = fields.Date('Periode Selesai')
    report_date = fields.Date('Tanggal Laporan')
    external_auditor = fields.Char('Kantor Akuntan Publik (KAP)')
    
    conclusion = fields.Selection([
        ('unqualified', 'WTP (Unqualified)'),
        ('qualified', 'WDP (Qualified)'),
        ('adverse', 'Tidak Wajar (Adverse)'),
        ('disclaimer', 'Tidak Memberikan Pendapat (Disclaimer)')
    ], string='Opini Auditor', required=True)
    
    # Hal 56-57: Gap Analysis Periode SOC
    has_bridge_letter = fields.Boolean('Ada Bridge Letter?', help='Surat keterangan dari vendor yang menjamin kontrol tetap efektif sejak akhir periode SOC hingga akhir tahun buku perusahaan.')
    gap_analysis_notes = fields.Text('Analisis Celah Periode', help='Catatan evaluasi jika periode laporan SOC tidak mencakup seluruh tahun buku perusahaan (Gap Analysis).')
    
    notes = fields.Text('Catatan/Pengecualian Penting')
    attachment = fields.Binary('Lampiran Laporan')
    file_name = fields.Char('Nama File')

class IcofrFaq(models.Model):
    _name = 'icofr.faq'
    _description = 'FAQ Panduan Juknis ICOFR'
    _order = 'sequence'

    sequence = fields.Integer('No Urut', default=10)
    question = fields.Text('Pertanyaan', required=True)
    answer = fields.Text('Jawaban', required=True)
    category = fields.Selection([
        ('general', 'Umum'),
        ('scoping', 'Scoping'),
        ('testing', 'Pengujian'),
        ('reporting', 'Pelaporan')
    ], string='Kategori', default='general')
