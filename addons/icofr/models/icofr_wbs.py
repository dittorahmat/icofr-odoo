# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrWbsEntry(models.Model):
    _name = 'icofr.wbs.entry'
    _description = 'Whistleblowing System Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'report_date desc'

    name = fields.Char('Subjek Aduan', required=True, tracking=True)
    code = fields.Char('Nomor Laporan', required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('icofr.wbs.entry') or '/')
    
    report_date = fields.Date('Tanggal Laporan', default=fields.Date.today, required=True)
    
    report_source = fields.Selection([
        ('hotline', 'Hotline / Telepon'),
        ('email', 'Email Khusus WBS'),
        ('website', 'Portal Web WBS'),
        ('letter', 'Surat Tertulis'),
        ('direct', 'Laporan Langsung')
    ], string='Media Pelaporan', default='website')

    reporter_type = fields.Selection([
        ('internal', 'Internal (Karyawan)'),
        ('external', 'Eksternal (Vendor/Masyarakat)'),
        ('anonymous', 'Anonim')
    ], string='Tipe Pelapor', default='anonymous')

    category = fields.Selection([
        ('fraud', 'Kecurangan / Korupsi'),
        ('integrity', 'Pelanggaran Integritas / Kode Etik'),
        ('reporting', 'Salah Saji Pelaporan Keuangan'),
        ('asset_misuse', 'Penyalahgunaan Aset'),
        ('other', 'Lainnya')
    ], string='Kategori Aduan', required=True, tracking=True)

    description = fields.Text('Uraian Aduan', required=True)
    
    impact_financial = fields.Boolean('Berdampak Finansial?')
    estimated_impact_amount = fields.Float('Estimasi Nilai Dampak')

    related_process_id = fields.Many2one('icofr.process', string='Proses Bisnis Terkait')
    related_control_id = fields.Many2one('icofr.control', string='Kontrol Terkait (Jika Ada)')

    status = fields.Selection([
        ('received', 'Diterima'),
        ('investigating', 'Sedang Diinvestigasi'),
        ('proven', 'Terbukti'),
        ('not_proven', 'Tidak Terbukti'),
        ('closed', 'Selesai / Ditutup')
    ], string='Status Penanganan', default='received', tracking=True)

    disposition_to = fields.Char('Disposisi kepada Unit', help='Unit atau fungsi yang menangani investigasi.')
    
    finding_id = fields.Many2one('icofr.finding', string='Temuan Terkait', 
                                help='Link ke temuan ICORF jika aduan ini memicu identifikasi defisiensi kontrol.')

    investigation_notes = fields.Text('Catatan Investigasi')
    resolution = fields.Text('Resolusi / Tindak Lanjut')

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('icofr.wbs.entry') or '/'
        return super(IcofrWbsEntry, self).create(vals)
