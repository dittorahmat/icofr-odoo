# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrExternalAdjustment(models.Model):
    _name = 'icofr.external.adjustment'
    _description = 'Audit Adjustment Eksternal'
    _order = 'fiscal_year desc, amount desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Deskripsi Adjustment', required=True)
    fiscal_year = fields.Char('Tahun Fiskal', required=True, default=lambda self: str(fields.Date.today().year))
    company_id = fields.Many2one('res.company', string='Perusahaan', required=True, default=lambda self: self.env.company)
    
    amount = fields.Float('Nilai Adjustment (Rp)', required=True)
    fsl_item = fields.Char('Item Laporan Keuangan (FSLI)')
    
    is_material = fields.Boolean('Kategori Material?', compute='_compute_is_material', store=True)
    
    related_control_ids = fields.Many2many('icofr.control', string='Kontrol Terkait', 
                                         help='Kontrol yang seharusnya mencegah/mendeteksi salah saji ini')
    
    finding_id = fields.Many2one('icofr.finding', string='Temuan ICORF Terkait', 
                                help='Link ke temuan ICORF jika adjustment ini memicu penemuan defisiensi')

    @api.depends('amount', 'company_id', 'fiscal_year')
    def _compute_is_material(self):
        for record in self:
            materiality = self.env['icofr.materiality'].search([
                ('company_id', '=', record.company_id.id),
                ('fiscal_year', '=', record.fiscal_year),
                ('active', '=', True)
            ], limit=1)
            
            # Hal 69: Penyesuaian signifikan (di atas PM) mengindikasikan defisiensi
            threshold = materiality.performance_materiality_amount if materiality else 0
            record.is_material = record.amount >= threshold if threshold > 0 else False
