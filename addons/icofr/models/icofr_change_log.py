# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrChangeLog(models.Model):
    _name = 'icofr.change.log'
    _description = 'Log Perubahan Proses Bisnis dan Pengendalian'
    _order = 'date_report desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nomor Referensi',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company
    )

    process_id = fields.Many2one(
        'icofr.process',
        string='Proses Bisnis',
        required=True,
        tracking=True
    )

    sub_process_id = fields.Many2one(
        'icofr.process',
        string='Sub Proses Bisnis',
        domain="[('parent_process_id', '=', process_id)]",
        help="Sub-proses jika relevan"
    )

    control_id = fields.Many2one(
        'icofr.control',
        string='Pengendalian',
        domain="[('process_id', '=', process_id)]",
        tracking=True,
        help="Pengendalian yang mengalami perubahan"
    )

    date_report = fields.Date(
        string='Tanggal Laporan',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    control_owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Pengendalian',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )

    # Before Change
    description_before = fields.Text(
        string='Deskripsi Sebelum Perubahan',
        required=True,
        help="Deskripsi proses bisnis dan/atau pengendalian sebelum perubahan"
    )
    
    ref_before = fields.Char(
        string='Referensi Sebelum Perubahan',
        help="Referensi dokumen/SOP sebelum perubahan"
    )

    # After Change
    description_after = fields.Text(
        string='Deskripsi Setelah Perubahan',
        required=True,
        help="Deskripsi proses bisnis dan/atau pengendalian setelah perubahan"
    )

    ref_after = fields.Char(
        string='Referensi Setelah Perubahan',
        help="Referensi dokumen/SOP setelah perubahan"
    )

    date_effective = fields.Date(
        string='Tanggal Efektif',
        required=True,
        tracking=True
    )

    # Approval
    approved_by = fields.Many2one(
        'res.users',
        string='Disetujui Oleh (Pemilik)',
        tracking=True,
        help="Pihak yang menyetujui perubahan (biasanya Pemilik Pengendalian)"
    )

    known_by = fields.Many2one(
        'res.users',
        string='Diketahui Oleh (Fungsi ICOFR)',
        tracking=True,
        help="Pihak Lini Kedua (Fungsi ICOFR) yang mengetahui perubahan ini"
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('icofr.change.log') or 'New'
        return super(IcofrChangeLog, self).create(vals_list)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.ensure_one()
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id
        })

    def action_acknowledge(self):
        """Action for Line 2 to acknowledge the change"""
        self.ensure_one()
        self.write({
            'known_by': self.env.user.id
        })
