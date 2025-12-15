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

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki rencana tindakan ini'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait rencana tindakan'
    )

    created_by_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat rencana tindakan'
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
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    finding_id = new_val_dict.get('finding_id')
                    if isinstance(finding_id, int):
                        # Finding reference is resolved, generate name
                        finding = self.env['icofr.finding'].browse(finding_id)
                        new_val_dict['name'] = f'Rencana Tindakan: {finding.name or "Temuan"}'
                    # If finding_id is not resolved, skip name generation for now
                processed_vals.append(new_val_dict)
            return super(IcofrActionPlan, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                finding_id = new_vals.get('finding_id')
                if isinstance(finding_id, int):
                    # Finding reference is resolved, generate name
                    finding = self.env['icofr.finding'].browse(finding_id)
                    new_vals['name'] = f'Rencana Tindakan: {finding.name or "Temuan"}'
                # If finding_id is not resolved, skip name generation for now
            return super(IcofrActionPlan, self).create(new_vals)