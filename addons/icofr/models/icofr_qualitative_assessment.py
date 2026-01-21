# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrQualitativeAssessment(models.Model):
    _name = 'icofr.qualitative.assessment'
    _description = 'Asesmen Risiko Kualitatif Akun'

    account_mapping_id = fields.Many2one(
        'icofr.account.mapping',
        string='Pemetaan Akun',
        ondelete='cascade',
        required=True
    )

    question = fields.Char(string='Pertanyaan', required=True)
    answer = fields.Selection([
        ('0', 'Rendah (0)'),
        ('1', 'Menengah (1)'),
        ('2', 'Tinggi (2)'),
        ('3', 'Sangat Tinggi (3)')
    ], string='Jawaban', default='0', required=True)
    
    score = fields.Integer(string='Skor', compute='_compute_score', store=True)
    notes = fields.Text(string='Catatan/Justifikasi')

    @api.depends('answer')
    def _compute_score(self):
        for record in self:
            record.score = int(record.answer)

class IcofrAccountMapping(models.Model):
    _inherit = 'icofr.account.mapping'

    qualitative_assessment_ids = fields.One2many(
        'icofr.qualitative.assessment',
        'account_mapping_id',
        string='Asesmen Kualitatif'
    )

    qualitative_total_score = fields.Integer(
        string='Total Skor Kualitatif',
        compute='_compute_qualitative_score',
        store=True
    )

    @api.depends('qualitative_assessment_ids.score')
    def _compute_qualitative_score(self):
        for record in self:
            record.qualitative_total_score = sum(record.qualitative_assessment_ids.mapped('score'))

    @api.depends('account_balance', 'materiality_id.performance_materiality_amount', 
                 'has_fraud_risk', 'is_complex_transaction', 'has_related_party', 
                 'is_volume_high', 'is_characteristic_specific', 'is_volatile',
                 'is_construction_wip', 'is_held_by_third_party', 'is_loan_covenant', 
                 'is_onerous_contract', 'is_asset_impairment', 'is_complex_estimate',
                 'qualitative_total_score')
    def _compute_scoping_flags(self):
        # Call super to get base calculation
        super(IcofrAccountMapping, self)._compute_scoping_flags()
        for record in self:
            # Override with qualitative score triggers (Hal 24: Kriteria Kualitatif)
            if record.qualitative_total_score >= 5:
                record.is_qualitative_significant = True
                record.is_in_scope = True
            elif record.qualitative_total_score >= 3:
                # Moderate risk still considered qualitative significant for scoping purposes in many BUMNs
                record.is_qualitative_significant = True
                record.is_in_scope = True

    def action_generate_questions(self):
        """Generate default qualitative questions as per PwC suggestions"""
        self.ensure_one()
        questions = [
            "Kompleksitas transaksi pada akun ini?",
            "Kerawanan terhadap fraud atau penyalahgunaan?",
            "Volume transaksi yang tidak rutin?",
            "Ketergantungan pada estimasi atau penilaian subjektif manajemen?",
            "Adanya transaksi dengan pihak berelasi?"
        ]
        
        existing_questions = self.qualitative_assessment_ids.mapped('question')
        for q in questions:
            if q not in existing_questions:
                self.env['icofr.qualitative.assessment'].create({
                    'account_mapping_id': self.id,
                    'question': q,
                    'answer': '0'
                })
        return True
