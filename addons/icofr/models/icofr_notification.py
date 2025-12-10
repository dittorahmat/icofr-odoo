# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrNotification(models.Model):
    _name = 'icofr.notification'
    _description = 'Notifikasi dan Pengingat ICORF'
    _order = 'create_date desc'

    name = fields.Char(
        string='Nama Notifikasi',
        required=True,
        help='Nama deskriptif dari notifikasi'
    )
    
    notification_type = fields.Selection([
        ('testing_reminder', 'Pengingat Pengujian'),
        ('certification_deadline', 'Batas Waktu Sertifikasi'),
        ('risk_assessment', 'Penilaian Risiko'),
        ('control_review', 'Review Kontrol'),
        ('reporting_deadline', 'Batas Waktu Pelaporan')
    ], string='Jenis Notifikasi', required=True,
       help='Jenis dari notifikasi yang dikirim')
    
    model_ref = fields.Reference(
        selection=[
            ('icofr.testing', 'Pengujian Kontrol'),
            ('icofr.certification', 'Sertifikasi'),
            ('icofr.risk', 'Risiko'),
            ('icofr.control', 'Kontrol')
        ],
        string='Referensi Objek',
        help='Objek yang terkait dengan notifikasi ini'
    )
    
    recipient_ids = fields.Many2many(
        'res.users',
        string='Penerima',
        help='Pengguna yang akan menerima notifikasi ini'
    )
    
    subject = fields.Char(
        string='Subjek',
        required=True,
        help='Subjek dari notifikasi'
    )
    
    message = fields.Text(
        string='Pesan',
        required=True,
        help='Isi pesan notifikasi'
    )
    
    sent_date = fields.Datetime(
        string='Tanggal Dikirim',
        readonly=True,
        help='Tanggal notifikasi dikirim'
    )
    
    is_read = fields.Boolean(
        string='Telah Dibaca',
        default=False,
        help='Menandai apakah notifikasi telah dibaca'
    )
    
    related_date = fields.Date(
        string='Tanggal Terkait',
        help='Tanggal yang terkait dengan notifikasi (misalnya jatuh tempo)'
    )
    
    priority = fields.Selection([
        ('low', 'Rendah'),
        ('normal', 'Normal'),
        ('high', 'Tinggi'),
        ('urgent', 'Segera')
    ], string='Prioritas', default='normal',
       help='Prioritas dari notifikasi')
    
    @api.model
    def create(self, vals):
        # Generate a default name if not provided
        if 'name' not in vals or not vals['name']:
            vals['name'] = f'Notifikasi {vals.get("notification_type", "Umum")} - {fields.Datetime.to_string(fields.Datetime.now())}'
        return super(IcofrNotification, self).create(vals)