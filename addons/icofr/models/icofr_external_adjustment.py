# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrExternalAdjustment(models.Model):
    _name = 'icofr.external.adjustment'
    _description = 'Audit Adjustment Eksternal'
    _order = 'fiscal_year desc, amount desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Deskripsi Adjustment', required=True)
    
    adjustment_type = fields.Selection([
        ('external', 'Audit Eksternal (KAP)'),
        ('internal', 'Internal Manajemen (Lini 1)')
    ], string='Kategori Penyesuaian', default='external', required=True,
       help='Hal 71: Lini 1 dapat melakukan penyesuaian internal untuk memastikan kewajaran angka jika kontrol tidak efektif.')

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

    def action_create_finding(self):
        """Buat temuan baru berdasarkan penyesuaian material ini"""
        self.ensure_one()
        if self.finding_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'icofr.finding',
                'res_id': self.finding_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
        
        # Determine finding category
        finding_type = 'significant_deficiency'
        if self.is_material:
            # Check if exceeds OM
            materiality = self.env['icofr.materiality'].search([
                ('company_id', '=', self.company_id.id),
                ('fiscal_year', '=', self.fiscal_year),
                ('active', '=', True)
            ], limit=1)
            if materiality and self.amount > materiality.overall_materiality_amount:
                finding_type = 'material_weakness'

        finding = self.env['icofr.finding'].create({
            'name': f'Temuan dari Adjustment: {self.name}',
            'finding_type': 'control_deficiency', # Base type
            'description': f'Penyesuaian audit ditemukan senilai Rp {self.amount:,.0f} pada FSLI {self.fsl_item or "N/A"}. Hal ini mengindikasikan kegagalan kontrol untuk mencegah salah saji.',
            'quantitative_impact_amount': self.amount,
            'company_id': self.company_id.id,
            'severity_level': 'high' if self.is_material else 'medium',
            'owner_id': self.env.user.id, # Assign to creator for now
        })
        
        self.finding_id = finding.id
        
        return {
            'name': 'Temuan Baru',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.finding',
            'res_id': finding.id,
            'view_mode': 'form',
            'target': 'current',
        }
