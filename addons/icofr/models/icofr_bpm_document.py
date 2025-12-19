# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrBpmDocument(models.Model):
    _name = 'icofr.bpm.document'
    _description = 'Repositori Dokumen BPM dan SOP'
    _order = 'version desc, create_date desc'

    name = fields.Char(string='Nama Dokumen', required=True)
    document_type = fields.Selection([
        ('bpm_flowchart', 'Flowchart BPM'),
        ('sop', 'SOP (Standard Operating Procedure)'),
        ('policy', 'Kebijakan'),
        ('other', 'Lainnya')
    ], string='Tipe Dokumen', default='bpm_flowchart', required=True)
    
    version = fields.Char(string='Versi', default='1.0', required=True)
    process_id = fields.Many2one('icofr.process', string='Proses Bisnis', ondelete='cascade')
    
    document_file = fields.Binary(string='File Dokumen', required=True)
    file_name = fields.Char(string='Nama File')
    
    status = fields.Selection([
        ('draft', 'Draf'),
        ('active', 'Aktif'),
        ('obsolete', 'Usang')
    ], string='Status', default='draft', required=True)
    
    description = fields.Text(string='Deskripsi/Catatan Perubahan')
    
    owner_id = fields.Many2one('res.users', string='Pemilik Dokumen', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Perusahaan', default=lambda self: self.env.company)
