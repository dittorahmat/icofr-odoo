# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrWorkflowLog(models.Model):
    _name = 'icofr.workflow.log'
    _description = 'Riwayat Workflow ICORF'
    _order = 'timestamp desc'

    workflow_id = fields.Many2one(
        'icofr.workflow',
        string='Workflow',
        required=True,
        ondelete='cascade',
        help='Workflow yang terkait dengan log ini'
    )
    
    action = fields.Selection([
        ('submitted', 'Disubmit'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('escalated', 'Di-escallate'),
        ('revised', 'Direvisi'),
        ('cancelled', 'Dibatalkan')
    ], string='Aksi',
       required=True,
       help='Jenis aksi dalam workflow')
    
    description = fields.Text(
        string='Deskripsi',
        required=True,
        help='Deskripsi lengkap dari aksi yang dilakukan'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Pengguna',
        required=True,
        help='Pengguna yang melakukan aksi'
    )
    
    timestamp = fields.Datetime(
        string='Waktu',
        required=True,
        default=lambda self: fields.Datetime.now(),
        help='Waktu kapan aksi dilakukan'
    )
    
    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait log workflow'
    )