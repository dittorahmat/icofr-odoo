# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IcofrProcess(models.Model):
    _name = 'icofr.process'
    _description = 'Proses Bisnis'
    _order = 'name'

    name = fields.Char(
        string='Nama Proses',
        required=True,
        translate=True,
        help='Nama dari proses bisnis'
    )

    code = fields.Char(
        string='Kode Proses',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi proses'
    )

    description = fields.Text(
        string='Deskripsi Proses',
        help='Deskripsi lengkap dari proses bisnis'
    )

    category = fields.Selection([
        ('operational', 'Operasional'),
        ('financial', 'Finansial'),
        ('compliance', 'Kepatuhan'),
        ('strategic', 'Strategis'),
        ('supporting', 'Dukungan')
    ], string='Kategori Proses', required=True,
       help='Kategori dari proses bisnis')

    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Proses',
        required=True,
        help='Pengguna yang bertanggung jawab atas proses ini'
    )

    parent_process_id = fields.Many2one(
        'icofr.process',
        string='Proses Induk',
        help='Proses induk jika ini adalah sub-proses'
    )

    control_ids = fields.One2many(
        'icofr.control',
        'process_id',
        string='Kontrol Terkait',
        help='Kontrol-kontrol yang terkait dengan proses ini'
    )

    risk_ids = fields.One2many(
        'icofr.risk',
        'process_id',
        string='Risiko Terkait',
        help='Risiko-risiko yang terkait dengan proses ini'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('under_review', 'Dalam Review')
    ], string='Status', default='active',
       help='Status dari proses bisnis')

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait proses'
    )

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            processes = self.search([('code', '=', record.code)])
            if len(processes) > 1:
                raise ValidationError("Kode proses harus unik!")

    @api.model
    def create(self, vals):
        # Generate a default code if not provided
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('icofr.process') or '/'
        return super(IcofrProcess, self).create(vals)