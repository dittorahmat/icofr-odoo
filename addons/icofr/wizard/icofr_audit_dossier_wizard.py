# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrAuditDossierWizard(models.TransientModel):
    _name = 'icofr.audit.dossier.wizard'
    _description = 'Wizard Bundel Dokumen Audit (Lampiran 12)'

    fiscal_year = fields.Char('Tahun Fiskal', required=True, default=lambda self: str(fields.Date.today().year))
    company_id = fields.Many2one('res.company', string='Perusahaan', required=True, default=lambda self: self.env.company)
    
    include_rcm = fields.Boolean('Sertakan RCM (Matrix)', default=True)
    include_flowcharts = fields.Boolean('Sertakan Flowchart BPM', default=True)
    include_testing_results = fields.Boolean('Sertakan Laporan TOD/TOE', default=True)
    include_dod_working_paper = fields.Boolean('Sertakan Kertas Kerja DoD', default=True)
    include_certification = fields.Boolean('Sertakan Sertifikasi CEO/CFO', default=True)

    def action_generate_dossier(self):
        """
        Simulasi pembuatan bundel dokumen audit sesuai Lampiran 12.
        Dalam implementasi nyata, ini akan mengumpulkan PDF dan mem-zip mereka.
        """
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Dossier Audit Sedang Diproses',
                'message': f'Bundel Dokumen Audit Tahun {self.fiscal_year} sedang disiapkan. Silakan cek folder unduhan Anda dalam beberapa saat.',
                'type': 'success',
                'sticky': False
            }
        }
