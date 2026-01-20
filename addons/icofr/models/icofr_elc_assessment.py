# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrElcAssessment(models.Model):
    _name = 'icofr.elc.assessment'
    _description = 'Evaluasi Entity Level Control (ELC)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fiscal_year desc'

    name = fields.Char('Nama Evaluasi', required=True, tracking=True)
    fiscal_year = fields.Char('Tahun Fiskal', required=True, default=lambda self: str(fields.Date.today().year))
    company_id = fields.Many2one('res.company', string='Perusahaan', required=True, default=lambda self: self.env.company)
    evaluator_id = fields.Many2one('res.users', string='Evaluator', default=lambda self: self.env.user)
    date_assessment = fields.Date('Tanggal Evaluasi', default=fields.Date.today)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Dalam Proses'),
        ('done', 'Selesai'),
        ('cancel', 'Dibatalkan')
    ], string='Status', default='draft', tracking=True)

    # 17 COSO Principles (Checklist)
    # Control Environment
    p1_integrity = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P1: Integritas & Nilai Etika')
    p2_oversight = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P2: Tanggung Jawab Pengawasan (Dewan)')
    p3_structure = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P3: Struktur Organisasi, Wewenang & Tanggung Jawab')
    p4_competence = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P4: Komitmen terhadap Kompetensi')
    p5_accountability = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P5: Akuntabilitas')

    # Risk Assessment
    p6_objectives = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P6: Penetapan Tujuan')
    p7_risk_id = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P7: Identifikasi & Analisis Risiko')
    p8_fraud_risk = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P8: Penilaian Risiko Kecurangan')
    p9_change_id = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P9: Identifikasi & Analisis Perubahan Signifikan')

    # Control Activities
    p10_select_controls = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P10: Pemilihan & Pengembangan Aktivitas Pengendalian')
    p11_it_controls = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P11: Pemilihan & Pengembangan Kontrol Umum IT')
    p12_policies = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P12: Penyebaran melalui Kebijakan & Prosedur')

    # Information & Communication
    p13_info_quality = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P13: Penggunaan Informasi yang Relevan')
    p14_internal_comm = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P14: Komunikasi Internal')
    p15_external_comm = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P15: Komunikasi Eksternal')

    # Monitoring
    p16_ongoing_eval = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P16: Evaluasi Berkelanjutan/Terpisah')
    p17_eval_deficiencies = fields.Selection([('effective', 'Efektif'), ('ineffective', 'Tidak Efektif')], string='P17: Evaluasi & Komunikasi Defisiensi')

    summary_notes = fields.Text('Ringkasan Kesimpulan ELC')
    overall_conclusion = fields.Selection([
        ('effective', 'ELC Efektif'),
        ('material_weakness', 'Terdapat Kelemahan Material pada ELC')
    ], string='Kesimpulan Akhir', compute='_compute_overall_conclusion', store=True)

    @api.depends('p1_integrity', 'p2_oversight', 'p3_structure', 'p4_competence', 'p5_accountability',
                 'p6_objectives', 'p7_risk_id', 'p8_fraud_risk', 'p9_change_id',
                 'p10_select_controls', 'p11_it_controls', 'p12_policies',
                 'p13_info_quality', 'p14_internal_comm', 'p15_external_comm',
                 'p16_ongoing_eval', 'p17_eval_deficiencies')
    def _compute_overall_conclusion(self):
        principles = [
            self.p1_integrity, self.p2_oversight, self.p3_structure, self.p4_competence, self.p5_accountability,
            self.p6_objectives, self.p7_risk_id, self.p8_fraud_risk, self.p9_change_id,
            self.p10_select_controls, self.p11_it_controls, self.p12_policies,
            self.p13_info_quality, self.p14_internal_comm, self.p15_external_comm,
            self.p16_ongoing_eval, self.p17_eval_deficiencies
        ]
        for record in self:
            if any(p == 'ineffective' for p in principles):
                record.overall_conclusion = 'material_weakness'
            else:
                record.overall_conclusion = 'effective'

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})
