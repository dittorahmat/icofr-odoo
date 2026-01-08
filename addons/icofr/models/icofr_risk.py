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
    
    # Qualitative Factors (Table 11 SK BUMN)
    qualitative_risk_level = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi')
    ], string='Rating Risiko Kualitatif', compute='_compute_qualitative_risk_level', store=True,
       help='Penilaian risiko berdasarkan faktor kualitatif (Tabel 11)')

    factor_inherent_risk = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Risiko Bawaan', default='low', help='Risiko bawaan yang berhubungan dengan akun dan asersi')

    factor_volume_changes = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Perubahan Volume/Sifat', default='low', help='Terjadi perubahan volume/sifat transaksi')

    factor_history_errors = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Riwayat Error', default='low', help='Riwayat kesalahan/error sebelumnya')

    factor_elc_effectiveness = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Efektivitas ELC', default='low', help='Efektivitas Entity Level Control')

    factor_control_characteristics = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Karakteristik Kontrol', default='low', help='Kompleksitas dan frekuensi kontrol')

    factor_competence = fields.Selection([
        ('low', 'Rendah'), ('medium', 'Sedang'), ('high', 'Tinggi')
    ], string='Faktor: Kompetensi Personel', default='low', help='Kompetensi personel pelaksana')

    # Add SK BUMN attributes
    risk_category_detailed = fields.Selection([
        ('operational', 'Operasional'),
        ('financial', 'Finansial'),
        ('compliance', 'Kepatuhan'),
        ('strategic', 'Strategis'),
        ('reputational', 'Reputasi')
    ], string='Kategori Risiko Terperinci', default='operational',
       help='Kategori terperinci dari risiko finansial')

    risk_type_detailed = fields.Selection([
        ('inherent', 'Inheren'),
        ('residual', 'Residu'),
        ('control', 'Kontrol')
    ], string='Tipe Risiko Terperinci', default='inherent',
       help='Tipe risiko terperinci sesuai dengan SK BUMN')

    risk_cause = fields.Text(
        string='Penyebab Risiko',
        help='Deskripsi penyebab mendasar dari risiko'
    )

    risk_impact_description = fields.Text(
        string='Deskripsi Dampak Risiko',
        help='Deskripsi rinci tentang dampak yang mungkin terjadi dari risiko'
    )

    risk_monitoring_procedures = fields.Text(
        string='Prosedur Pemantauan Risiko',
        help='Prosedur untuk memantau risiko secara berkelanjutan'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki risiko ini'
    )

    risk_date = fields.Date(
        string='Tanggal Risiko',
        default=fields.Date.context_today,
        help='Tanggal terkait dengan identifikasi atau penilaian risiko'
    )

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait risiko'
    )
    
    @api.depends(
        'factor_inherent_risk', 'factor_volume_changes', 'factor_history_errors',
        'factor_elc_effectiveness', 'factor_control_characteristics', 'factor_competence'
    )
    def _compute_qualitative_risk_level(self):
        """
        Menghitung Rating Risiko Kualitatif (Tabel 11).
        Logic: Jika ADA SATU SAJA faktor 'High', maka High.
        Jika tidak ada High tapi ada 'Medium', maka Medium.
        Sisanya Low.
        """
        factors = [
            'factor_inherent_risk', 'factor_volume_changes', 'factor_history_errors',
            'factor_elc_effectiveness', 'factor_control_characteristics', 'factor_competence'
        ]
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        
        for record in self:
            max_score = 1
            for f in factors:
                val = getattr(record, f)
                if val:
                    max_score = max(max_score, priority_map.get(val, 1))
            
            if max_score == 3:
                record.qualitative_risk_level = 'high'
            elif max_score == 2:
                record.qualitative_risk_level = 'medium'
            else:
                record.qualitative_risk_level = 'low'

    @api.depends('likelihood', 'impact', 'qualitative_risk_level')
    def _compute_risk_level(self):
        """
        Menghitung tingkat risiko Kombinasi (Tabel 12 SK BUMN).
        Menggabungkan Faktor Kuantitatif (Likelihood x Impact) dengan Faktor Kualitatif.
        Prinsip Tabel 12: Jika SALAH SATU (Kuantitatif atau Kualitatif) adalah TINGGI, maka Total Risiko = TINGGI.
        """
        # Matrix Kuantitatif (Likelihood x Impact)
        # Mapping outcome matrix ke High/Medium/Low standard
        quant_map = {
            'very_low': 'low',
            'low': 'low',
            'medium': 'medium',
            'high': 'high',
            'very_high': 'high'
        }

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
        
        priority_map = {'high': 3, 'medium': 2, 'low': 1} # For final comparison

        for record in self:
            # 1. Hitung Kuantitatif (Existing Logic)
            quant_result_raw = 'medium'
            if record.likelihood and record.impact:
                quant_result_raw = risk_matrix.get((record.likelihood, record.impact), 'medium')
            
            # Map raw quantitative result (very_low..very_high) to simple Low/Medium/High for comparison
            quant_simple = quant_map.get(quant_result_raw, 'medium')
            
            # 2. Ambil Kualitatif
            qual_simple = record.qualitative_risk_level or 'low'

            # 3. Kombinasi (Table 12 Logic - Max Concept)
            score_quant = priority_map.get(quant_simple, 2)
            score_qual = priority_map.get(qual_simple, 1)
            
            final_score = max(score_quant, score_qual)
            
            # Kembalikan ke format field risk_level (yang punya very_low..very_high)
            # Kita mapping High -> High, Medium -> Medium, Low -> Low
            # (Note: risk_level field uses 5 scales, Table 12 uses 3. We map conservatively)
            if final_score == 3: # High
                record.risk_level = 'high' 
            elif final_score == 2: # Medium
                record.risk_level = 'medium'
            else: # Low
                record.risk_level = 'low'
    
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