# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IcofrRisk(models.Model):
    _name = 'icofr.risk'
    _description = 'Risiko Finansial'
    _order = 'name'

    name = fields.Char(
        string='Nama Risiko',
        required=True,
        translate=True,
        help='Nama dari risiko finansial'
    )
    
    code = fields.Char(
        string='Kode Risiko',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi risiko'
    )
    
    risk_category = fields.Selection([
        ('operational', 'Operasional'),
        ('financial', 'Finansial'),
        ('compliance', 'Kepatuhan'),
        ('strategic', 'Strategis'),
        ('reputational', 'Reputasi')
    ], string='Kategori Risiko', required=True,
       help='Kategori dari risiko finansial')
    
    risk_type = fields.Selection([
        ('inherent', 'Inheren'),
        ('residual', 'Residu'),
        ('control', 'Kontrol')
    ], string='Jenis Risiko', required=True,
       help='Jenis dari risiko')
    
    description = fields.Text(
        string='Deskripsi Risiko',
        help='Deskripsi lengkap dari risiko'
    )
    
    objective = fields.Text(
        string='Tujuan Pengendalian',
        help='Tujuan dari pengendalian risiko ini'
    )
    
    likelihood = fields.Selection([
        ('very_low', 'Sangat Rendah'),
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('very_high', 'Sangat Tinggi')
    ], string='Kemungkinan Terjadi', required=True,
       help='Tingkat kemungkinan terjadinya risiko')
    
    impact = fields.Selection([
        ('very_low', 'Sangat Rendah'),
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('very_high', 'Sangat Tinggi')
    ], string='Dampak', required=True,
       help='Tingkat dampak dari risiko')
    
    risk_level = fields.Selection([
        ('very_low', 'Sangat Rendah'),
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('very_high', 'Sangat Tinggi')
    ], string='Tingkat Risiko', compute='_compute_risk_level',
       help='Tingkat risiko berdasarkan kemungkinan dan dampak')
    
    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Risiko',
        required=True,
        help='Pengguna yang bertanggung jawab atas pengelolaan risiko ini'
    )
    
    process_id = fields.Many2one(
        'icofr.process',
        string='Proses Bisnis Terkait',
        help='Proses bisnis yang terkait dengan risiko ini'
    )
    
    control_ids = fields.Many2many(
        'icofr.control',
        'icofr_risk_control_rel',
        'risk_id', 'control_id', 
        string='Kontrol Terkait',
        help='Kontrol-kontrol yang digunakan untuk mengelola risiko ini'
    )
    
    mitigation_plan = fields.Text(
        string='Rencana Mitigasi',
        help='Rencana mitigasi untuk mengurangi risiko'
    )
    
    status = fields.Selection([
        ('identified', 'Teridentifikasi'),
        ('assessed', 'Dinilai'),
        ('mitigated', 'Dimitigasi'),
        ('monitored', 'Dimonitor'),
        ('closed', 'Ditutup')
    ], string='Status', default='identified',
       help='Status pengelolaan risiko saat ini')
    
    last_assessment_date = fields.Date(
        string='Tanggal Penilaian Terakhir',
        help='Tanggal terakhir risiko ini dinilai'
    )
    
    next_assessment_date = fields.Date(
        string='Tanggal Penilaian Berikutnya',
        help='Tanggal terjadwal untuk penilaian risiko berikutnya'
    )
    
    residual_risk_level = fields.Selection([
        ('very_low', 'Sangat Rendah'),
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('very_high', 'Sangat Tinggi')
    ], string='Tingkat Risiko Residu',
       help='Tingkat risiko setelah kontrol diterapkan')
    
    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait risiko'
    )
    
    @api.depends('likelihood', 'impact')
    def _compute_risk_level(self):
        """Menghitung tingkat risiko berdasarkan kemungkinan dan dampak"""
        risk_matrix = {
            ('very_low', 'very_low'): 'very_low',
            ('very_low', 'low'): 'very_low',
            ('very_low', 'medium'): 'low',
            ('very_low', 'high'): 'low',
            ('very_low', 'very_high'): 'medium',
            
            ('low', 'very_low'): 'very_low',
            ('low', 'low'): 'low',
            ('low', 'medium'): 'low',
            ('low', 'high'): 'medium',
            ('low', 'very_high'): 'medium',
            
            ('medium', 'very_low'): 'low',
            ('medium', 'low'): 'low',
            ('medium', 'medium'): 'medium',
            ('medium', 'high'): 'medium',
            ('medium', 'very_high'): 'high',
            
            ('high', 'very_low'): 'medium',
            ('high', 'low'): 'medium',
            ('high', 'medium'): 'high',
            ('high', 'high'): 'high',
            ('high', 'very_high'): 'very_high',
            
            ('very_high', 'very_low'): 'medium',
            ('very_high', 'low'): 'high',
            ('very_high', 'medium'): 'high',
            ('very_high', 'high'): 'very_high',
            ('very_high', 'very_high'): 'very_high',
        }
        
        for record in self:
            if record.likelihood and record.impact:
                record.risk_level = risk_matrix.get((record.likelihood, record.impact), 'medium')
            else:
                record.risk_level = 'medium'
    
    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            risks = self.search([('code', '=', record.code)])
            if len(risks) > 1:
                raise ValidationError("Kode risiko harus unik!")
    
    def action_export_risks(self):
        """Method untuk membuka wizard ekspor risiko"""
        self.ensure_one()
        # Buka wizard ekspor dengan parameter yang sesuai
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'risk',
            'export_format': 'xlsx',
            'date_from': False,
            'date_to': False,
            'include_attachments': False,
            'include_inactive': False
        })

        return {
            'name': 'Ekspor Risiko Finansial',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',  # Buka di modal window
            'context': {
                'default_export_type': 'risk',
                'default_export_format': 'xlsx'
            }
        }

    @api.model
    def create(self, vals):
        # Ensure vals is a dictionary and not a list by checking the first element if needed
        if isinstance(vals, list):
            # If vals is a list (for multiple creation), process each item
            processed_vals = []
            for val_dict in vals:
                if isinstance(val_dict, dict):
                    if 'code' not in val_dict or not val_dict.get('code'):
                        val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.risk') or '/'
                    processed_vals.append(val_dict)
            return super(IcofrRisk, self).create(processed_vals)
        else:
            # For single record creation (most common case)
            if 'code' not in vals or not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('icofr.risk') or '/'
            return super(IcofrRisk, self).create(vals)