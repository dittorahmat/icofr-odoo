# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrExternalAssurance(models.Model):
    _name = 'icofr.external.assurance'
    _description = 'Asurans Praktisi Eksternal ICOFR'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fiscal_year desc'

    name = fields.Char('Nomor Laporan Asurans', required=True)
    fiscal_year = fields.Char('Tahun Fiskal', required=True, default=lambda self: str(fields.Date.today().year))
    company_id = fields.Many2one('res.company', string='Perusahaan', required=True, default=lambda self: self.env.company)
    
    auditor_firm = fields.Char('Kantor Akuntan Publik (KAP)', required=True)
    engagement_partner = fields.Char('Partner Perikatan')
    report_date = fields.Date('Tanggal Laporan Asurans', required=True)
    
    # Bab VIII Page 67: Komunikasi dengan Praktisi Eksternal
    assurance_type = fields.Selection([
        ('audit', 'Audit Pengendalian Internal'),
        ('review', 'Reviu Pengendalian Internal'),
        ('agreed_procedures', 'Prosedur yang Disepakati (AUP)')
    ], string='Jenis Perikatan', default='audit')

    opinion = fields.Selection([
        ('unqualified', 'WTP (Unqualified Opinion)'),
        ('qualified', 'WDP (Qualified Opinion)'),
        ('adverse', 'Tidak Wajar (Adverse Opinion)'),
        ('disclaimer', 'Disclaimer (No Opinion)')
    ], string='Opini Praktisi', required=True)

    findings_summary = fields.Text('Ringkasan Temuan Auditor Eksternal')
    
    certification_id = fields.Many2one('icofr.certification', string='Sertifikasi Manajemen Terkait',
                                     help='Link ke Asesmen Manajemen yang diberikan asurans.')
    
    attachment = fields.Binary('Lampiran Laporan Asurans')
    file_name = fields.Char('Nama File')

    notes = fields.Text('Catatan Tambahan')
