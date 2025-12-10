# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrWorkflow(models.Model):
    _name = 'icofr.workflow'
    _description = 'Workflow Persetujuan ICORF'
    _order = 'create_date desc'

    name = fields.Char(
        string='Nama Workflow',
        required=True,
        help='Nama dari proses workflow'
    )
    
    model_ref = fields.Reference(
        selection=[
            ('icofr.testing', 'Pengujian Kontrol'),
            ('icofr.certification', 'Sertifikasi'),
            ('icofr.risk', 'Risiko'),
            ('icofr.control', 'Kontrol')
        ],
        string='Referensi Objek',
        help='Objek yang terlibat dalam workflow ini'
    )
    
    workflow_type = fields.Selection([
        ('testing_approval', 'Persetujuan Pengujian'),
        ('certification_approval', 'Persetujuan Sertifikasi'),
        ('risk_assessment', 'Penilaian Risiko'),
        ('control_change', 'Perubahan Kontrol')
    ], string='Jenis Workflow', required=True,
       help='Jenis dari workflow persetujuan')
    
    current_approver_id = fields.Many2one(
        'res.users',
        string='Penyetuju Saat Ini',
        help='Pengguna yang saat ini harus menyetujui'
    )
    
    state = fields.Selection([
        ('draft', 'Draf'),
        ('submitted', 'Dikirim'),
        ('in_approval', 'Dalam Persetujuan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('cancelled', 'Dibatalkan')
    ], string='Status', default='draft',
       help='Status saat ini dari workflow')
    
    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi dari proses workflow'
    )
    
    submitter_id = fields.Many2one(
        'res.users',
        string='Pengirim',
        default=lambda self: self.env.user,
        help='Pengguna yang mengirim permintaan'
    )
    
    approval_date = fields.Datetime(
        string='Tanggal Disetujui',
        help='Tanggal workflow disetujui'
    )
    
    rejection_reason = fields.Text(
        string='Alasan Penolakan',
        help='Alasan jika workflow ditolak'
    )
    
    sequence = fields.Integer(
        string='Urutan',
        default=1,
        help='Urutan dalam proses approval'
    )
    
    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait workflow'
    )
    
    @api.model
    def create(self, vals):
        # Generate a default name if not provided
        if 'name' not in vals or not vals['name']:
            vals['name'] = f'Workflow {vals.get("workflow_type", "Umum")} - {fields.Datetime.to_string(fields.Datetime.now())}'
        return super(IcofrWorkflow, self).create(vals)