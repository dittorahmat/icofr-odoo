# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCertification(models.Model):
    _name = 'icofr.certification'
    _description = 'Sertifikasi ICORF'
    _order = 'fiscal_year desc'

    name = fields.Char(
        string='Nama Sertifikasi',
        required=True,
        help='Nama dari sertifikasi ICORF'
    )
    
    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk sertifikasi'
    )
    
    certification_date = fields.Date(
        string='Tanggal Sertifikasi',
        required=True,
        default=fields.Date.today,
        help='Tanggal sertifikasi dilakukan'
    )
    
    certified_by_id = fields.Many2one(
        'res.users',
        string='Disertifikasi Oleh',
        required=True,
        help='Pengguna yang melakukan sertifikasi (biasanya CEO/CFO)'
    )
    
    status = fields.Selection([
        ('draft', 'Draf'),
        ('submitted', 'Dikirim'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('archived', 'Diarsipkan')
    ], string='Status', default='draft',
       help='Status dari proses sertifikasi')
    
    effectiveness_statement = fields.Text(
        string='Pernyataan Efektivitas',
        help='Pernyataan mengenai efektivitas kontrol internal'
    )
    
    scope = fields.Text(
        string='Lingkup Sertifikasi',
        help='Lingkup dari sertifikasi kontrol internal'
    )
    
    finding_ids = fields.One2many(
        'icofr.finding',
        'certification_id',
        string='Temuan Terkait',
        help='Temuan-temuan yang terkait dengan sertifikasi ini'
    )

    workflow_id = fields.Many2one(
        'icofr.workflow',
        string='Workflow Persetujuan',
        help='Workflow persetujuan yang terkait dengan sertifikasi ini'
    )

    action_plan_ids = fields.One2many(
        'icofr.action.plan',
        'certification_id',
        string='Rencana Tindakan Terkait',
        help='Rencana tindakan yang terkait dengan sertifikasi ini'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait sertifikasi'
    )

    def create_certification_workflow(self):
        """Method untuk membuat workflow persetujuan untuk sertifikasi"""
        self.ensure_one()
        # Implementasi sederhana: buat entri workflow baru
        workflow = self.env['icofr.workflow'].create({
            'name': f'Workflow untuk {self.name}',
            'model_ref': f'icofr.certification,{self.id}',
            'initiator_id': self.certified_by_id.id,
            'status': 'active'
        })

        # Hubungkan workflow ke sertifikasi
        self.write({'workflow_id': workflow.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Workflow Persetujuan',
            'res_model': 'icofr.workflow',
            'res_id': workflow.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def export_certification_to_excel(self):
        """Method untuk mengekspor sertifikasi ke format Excel"""
        self.ensure_one()
        # Implementasi dasar untuk ekspor ke Excel
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel
        # dengan data sertifikasi
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/binary/download_document/{self.id}/icofr.certification/excel_export',
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        # Generate a default name if not provided
        if 'name' not in vals or not vals['name']:
            vals['name'] = f'Sertifikasi {vals.get("fiscal_year", fields.Date.today().year)}'
        return super(IcofrCertification, self).create(vals)