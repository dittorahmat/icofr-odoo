# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrFinding(models.Model):
    _name = 'icofr.finding'
    _description = 'Temuan ICORF'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Temuan',
        required=True,
        help='Nama deskriptif dari temuan'
    )
    
    code = fields.Char(
        string='Kode Temuan',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi temuan'
    )
    
    finding_type = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('process_inefficiency', 'Ketidakefisienan Proses'),
        ('compliance_violation', 'Pelanggaran Kepatuhan'),
        ('risk_exposure', 'Eksposur Risiko'),
        ('material_weakness', 'Kelemahan Material'),
        ('significant_deficiency', 'Kekurangan Signifikan')
    ], string='Jenis Temuan', required=True,
       help='Jenis dari temuan yang ditemukan')
    
    severity_level = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('critical', 'Kritis')
    ], string='Tingkat Keparahan', required=True,
       help='Tingkat keparahan dari temuan')
    
    description = fields.Text(
        string='Deskripsi Temuan',
        help='Deskripsi lengkap dari temuan'
    )
    
    impact_assessment = fields.Text(
        string='Penilaian Dampak',
        help='Penilaian dampak dari temuan terhadap organisasi'
    )
    
    root_cause = fields.Text(
        string='Penyebab Utama',
        help='Analisis akar penyebab dari temuan'
    )
    
    certification_id = fields.Many2one(
        'icofr.certification',
        string='Sertifikasi Terkait',
        help='Sertifikasi atau audit yang menemukan isu ini'
    )
    
    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Terkait',
        help='Kontrol internal yang terkait dengan temuan'
    )
    
    risk_id = fields.Many2one(
        'icofr.risk',
        string='Risiko Terkait',
        help='Risiko yang terkait dengan temuan'
    )
    
    status = fields.Selection([
        ('open', 'Terbuka'),
        ('in_progress', 'Dalam Proses'),
        ('closed', 'Ditutup'),
        ('wont_fix', 'Tidak Akan Diperbaiki')
    ], string='Status', default='open',
       help='Status penanganan temuan saat ini')
    
    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Temuan',
        required=True,
        help='Pengguna yang bertanggung jawab menangani temuan ini'
    )
    
    due_date = fields.Date(
        string='Tanggal Jatuh Tempo',
        help='Tanggal penyelesaian yang diharapkan'
    )
    
    closed_date = fields.Date(
        string='Tanggal Ditutup',
        help='Tanggal temuan sebenarnya ditutup'
    )
    
    action_plan_ids = fields.One2many(
        'icofr.action.plan',
        'finding_id',
        string='Rencana Tindakan',
        help='Rencana tindakan untuk mengatasi temuan'
    )
    
    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti yang mendukung temuan'
    )
    
    recommendation = fields.Text(
        string='Rekomendasi',
        help='Rekomendasi untuk mengatasi temuan'
    )
    
    created_by_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat temuan'
    )
    
    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait temuan'
    )
    
    def action_close_finding(self):
        """Method untuk menutup temuan"""
        self.ensure_one()
        self.write({
            'status': 'closed',
            'closed_date': fields.Date.today()
        })
        return True

    def action_reopen_finding(self):
        """Method untuk membuka kembali temuan"""
        self.ensure_one()
        self.write({
            'status': 'open',
            'closed_date': False
        })
        return True

    @api.model
    def create(self, vals):
        # Generate a default code if not provided
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('icofr.finding') or '/'
        return super(IcofrFinding, self).create(vals)