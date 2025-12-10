# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class IcofrTesting(models.Model):
    _name = 'icofr.testing'
    _description = 'Pengujian Kontrol Internal'
    _order = 'test_date desc'

    name = fields.Char(
        string='Nama Pengujian',
        required=True,
        help='Nama unik dari pengujian kontrol'
    )
    
    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol yang Diuji',
        required=True,
        help='Kontrol internal yang menjadi subjek pengujian'
    )
    
    test_type = fields.Selection([
        ('compliance', 'Kepatuhan'),
        ('substantive', 'Substantif'),
        ('walkthrough', 'Walkthrough')
    ], string='Jenis Pengujian', required=True,
       help='Jenis dari pengujian kontrol')
    
    test_date = fields.Date(
        string='Tanggal Pengujian',
        required=True,
        default=fields.Date.today,
        help='Tanggal pelaksanaan pengujian'
    )
    
    tester_id = fields.Many2one(
        'res.users',
        string='Pelaksana Pengujian',
        required=True,
        help='Pengguna yang melaksanakan pengujian'
    )
    
    sample_size = fields.Integer(
        string='Ukuran Sampel',
        help='Jumlah sampel yang diuji'
    )
    
    testing_procedures = fields.Text(
        string='Prosedur Pengujian',
        help='Prosedur yang diikuti dalam pengujian ini'
    )
    
    test_results = fields.Text(
        string='Hasil Pengujian',
        help='Hasil dari pengujian kontrol'
    )
    
    findings = fields.Text(
        string='Temuan',
        help='Temuan selama proses pengujian'
    )
    
    effectiveness = fields.Selection([
        ('effective', 'Efektif'),
        ('partially_effective', 'Efektif Sebagian'),
        ('ineffective', 'Tidak Efektif'),
        ('not_tested', 'Tidak Diuji')
    ], string='Efektivitas', required=True,
       help='Efektivitas kontrol berdasarkan hasil pengujian')
    
    status = fields.Selection([
        ('planned', 'Terjadwal'),
        ('in_progress', 'Dalam Proses'),
        ('completed', 'Selesai'),
        ('reviewed', 'Direview'),
        ('approved', 'Disetujui')
    ], string='Status Pengujian', default='planned',
       help='Status dari proses pengujian')
    
    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti yang mendukung hasil pengujian'
    )
    
    recommendation = fields.Text(
        string='Rekomendasi',
        help='Rekomendasi untuk perbaikan kontrol jika diperlukan'
    )
    
    due_date = fields.Date(
        string='Tanggal Jatuh Tempo',
        help='Tanggal jatuh tempo pelaksanaan pengujian'
    )
    
    completion_date = fields.Date(
        string='Tanggal Selesai',
        help='Tanggal sebenarnya pengujian selesai'
    )
    
    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait pengujian'
    )

    schedule_id = fields.Many2one(
        'icofr.testing.schedule',
        string='Jadwal Terkait',
        help='Jadwal yang terkait dengan pengujian ini'
    )
    
    @api.onchange('control_id')
    def _onchange_control_id(self):
        """Isi field testing_procedures dengan prosedur dari kontrol jika kosong"""
        if self.control_id and not self.testing_procedures:
            self.testing_procedures = self.control_id.testing_procedures
    
    @api.constrains('test_date', 'completion_date')
    def _check_dates(self):
        """Validasi tanggal pengujian"""
        for record in self:
            if record.test_date and record.completion_date and record.test_date > record.completion_date:
                raise ValidationError("Tanggal pengujian tidak boleh setelah tanggal selesai!")
    
    def create_approval_workflow(self):
        """Method untuk membuat workflow persetujuan untuk pengujian"""
        self.ensure_one()
        # Implementasi sederhana: buat entri workflow baru
        workflow = self.env['icofr.workflow'].create({
            'name': f'Workflow Pengujian: {self.name}',
            'model_ref': f'icofr.testing,{self.id}',
            'initiator_id': self.tester_id.id,
            'status': 'active'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Workflow Persetujuan',
            'res_model': 'icofr.workflow',
            'res_id': workflow.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_export_testing(self):
        """Method untuk membuka wizard ekspor pengujian"""
        self.ensure_one()
        # Buka wizard ekspor dengan parameter yang sesuai
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'testing',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Pengujian Kontrol',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'testing',
                'default_export_format': 'xlsx'
            }
        }

    @api.model
    def create(self, vals):
        # Generate a default name based on control if not provided
        if 'name' not in vals or not vals['name']:
            control = self.env['icofr.control'].browse(vals.get('control_id'))
            vals['name'] = f'Pengujian {control.name or "Kontrol"} - {fields.Date.to_string(fields.Date.today())}'
        return super(IcofrTesting, self).create(vals)