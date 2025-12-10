# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrActionPlan(models.Model):
    _name = 'icofr.action.plan'
    _description = 'Rencana Tindakan ICORF'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Rencana Tindakan',
        required=True,
        help='Nama deskriptif dari rencana tindakan'
    )

    finding_id = fields.Many2one(
        'icofr.finding',
        string='Temuan Terkait',
        help='Temuan yang ditangani oleh rencana tindakan ini'
    )

    certification_id = fields.Many2one(
        'icofr.certification',
        string='Sertifikasi Terkait',
        help='Sertifikasi terkait dengan rencana tindakan'
    )

    description = fields.Text(
        string='Deskripsi Tindakan',
        help='Deskripsi lengkap dari tindakan yang direncanakan'
    )

    action_owner_id = fields.Many2one(
        'res.users',
        string='Pelaksana Tindakan',
        required=True,
        help='Pengguna yang akan melaksanakan tindakan'
    )

    responsible_department = fields.Char(
        string='Departemen Bertanggung Jawab',
        help='Departemen yang bertanggung jawab atas pelaksanaan tindakan'
    )

    target_completion_date = fields.Date(
        string='Tanggal Target Selesai',
        required=True,
        help='Tanggal target penyelesaian tindakan'
    )

    actual_completion_date = fields.Date(
        string='Tanggal Selesai Aktual',
        help='Tanggal sebenarnya tindakan selesai'
    )

    status = fields.Selection([
        ('planned', 'Direncaanakan'),
        ('in_progress', 'Dalam Proses'),
        ('completed', 'Selesai'),
        ('delayed', 'Tertunda'),
        ('cancelled', 'Dibatalkan')
    ], string='Status', default='planned',
       help='Status pelaksanaan rencana tindakan')

    implementation_steps = fields.Text(
        string='Langkah Implementasi',
        help='Langkah-langkah spesifik untuk melaksanakan rencana tindakan'
    )

    resource_requirement = fields.Text(
        string='Kebutuhan Sumber Daya',
        help='Sumber daya yang diperlukan untuk pelaksanaan tindakan'
    )

    cost_estimate = fields.Float(
        string='Estimasi Biaya',
        help='Estimasi biaya pelaksanaan rencana tindakan'
    )

    effectiveness_check = fields.Text(
        string='Pemeriksaan Efektivitas',
        help='Metode untuk memeriksa efektivitas implementasi tindakan'
    )

    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti pelaksanaan tindakan'
    )

    priority = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('urgent', 'Segera')
    ], string='Prioritas', default='medium',
       help='Prioritas pelaksanaan rencana tindakan')

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait rencana tindakan'
    )

    def action_mark_in_progress(self):
        """Method untuk menandai rencana tindakan sebagai dalam proses"""
        self.ensure_one()
        self.write({
            'status': 'in_progress'
        })
        return True

    def action_mark_completed(self):
        """Method untuk menandai rencana tindakan sebagai selesai"""
        self.ensure_one()
        self.write({
            'status': 'completed',
            'actual_completion_date': fields.Date.today()
        })
        return True

    @api.model
    def create(self, vals):
        # Jika tidak ada nama, buat berdasarkan temuan
        if 'name' not in vals or not vals['name']:
            finding = self.env['icofr.finding'].browse(vals.get('finding_id'))
            if finding:
                vals['name'] = f'Rencana Tindakan: {finding.name}'
        return super(IcofrActionPlan, self).create(vals)