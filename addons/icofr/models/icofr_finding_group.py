# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IcofrFindingGroup(models.Model):
    """
    Model for Aggregated Deficiency Evaluation.
    Allows grouping of multiple findings to evaluate their collective impact against materiality.
    """
    _name = 'icofr.finding.group'
    _description = 'Evaluasi Defisiensi Agregat'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Grup Defisiensi',
        required=True,
        default=lambda self: _('Evaluasi Agregat Baru'),
        help='Nama deskriptif untuk grup temuan ini'
    )

    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        default=lambda self: str(fields.Date.today().year),
        help='Tahun fiskal evaluasi'
    )

    # Bab VII Pasal 1.1.g: Evaluasi Agregasi
    grouping_basis = fields.Selection([
        ('account', 'Akun/FSLI yang Sama'),
        ('disclosure', 'Pengungkapan yang Sama'),
        ('assertion', 'Asersi Laporan Keuangan yang Sama'),
        ('coso', 'Komponen/Prinsip COSO yang Sama'),
        ('process', 'Proses Bisnis yang Sama'),
        ('other', 'Pertimbangan Profesional Lainnya')
    ], string='Dasar Pengelompokan', required=True, default='account')

    impacted_fsli_id = fields.Many2one('icofr.account.mapping', string='Akun/FSLI Terkait')
    
    disclosure_id = fields.Many2one('icofr.disclosure', string='Pengungkapan Terkait', help='Digunakan jika dasar pengelompokan adalah Pengungkapan.')

    assertion_type = fields.Selection([
        ('existence', 'Existence/Occurrence'),
        ('completeness', 'Completeness'),
        ('accuracy', 'Accuracy'),
        ('cutoff', 'Cut-Off'),
        ('valuation', 'Valuation and Allocation'),
        ('rights', 'Rights and Obligation'),
        ('presentation', 'Presentation and Disclosure')
    ], string='Asersi Terkait', help='Digunakan jika dasar pengelompokan adalah Asersi.')

    coso_principle_id = fields.Many2one('icofr.coso.element', string='Prinsip COSO Terkait', domain="[('is_principle', '=', True)]")

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan terkait'
    )

    finding_ids = fields.Many2many(
        'icofr.finding',
        string='Temuan dalam Grup',
        domain="[('company_id', '=', company_id)]",
        help='Daftar temuan yang dikelompokkan untuk dievaluasi secara bersama-sama'
    )

    total_quantitative_impact = fields.Float(
        string='Total Dampak Kuantitatif (Rp)',
        compute='_compute_total_impact',
        store=True,
        help='Jumlah total dampak moneter dari semua temuan dalam grup'
    )

    description = fields.Text(
        string='Deskripsi Evaluasi',
        help='Penjelasan mengenai alasan pengelompokan temuan ini (misal: akun sama, proses sama)'
    )

    aggregated_deficiency_class = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol (Aggregate)'),
        ('significant_deficiency', 'Kekurangan Signifikan (Aggregate)'),
        ('material_weakness', 'Kelemahan Material (Aggregate)')
    ], string='Klasifikasi Agregat',
       compute='_compute_aggregated_classification',
       store=True,
       help='Hasil klasifikasi defisiensi berdasarkan total dampak grup terhadap materialitas')

    # Hal 69: Mitigasi via Compensating Control untuk Agregasi
    compensating_control_id = fields.Many2one(
        'icofr.control', 
        string='Kontrol Kompensasi (Grup)',
        help='Kontrol yang memitigasi risiko dari gabungan temuan ini.'
    )
    is_compensating_control_effective = fields.Boolean(
        string='Kontrol Kompensasi Efektif?',
        help='Apakah kontrol kompensasi untuk grup ini telah terbukti efektif?'
    )

    evaluation_notes = fields.Text(
        string='Catatan Evaluasi',
        help='Catatan tambahan dari evaluator mengenai hasil agregasi'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('evaluated', 'Dievaluasi'),
        ('confirmed', 'Dikonfirmasi')
    ], string='Status', default='draft')

    @api.depends('finding_ids', 'finding_ids.quantitative_impact_amount', 'finding_ids.manual_monetary_impact_amount', 'finding_ids.impact_assessment_method')
    def _compute_total_impact(self):
        for record in self:
            total = 0.0
            for finding in record.finding_ids:
                # Use the effective monetary impact from each finding logic
                if finding.impact_assessment_method == 'manual':
                    impact = finding.manual_monetary_impact_amount
                elif finding.impact_assessment_method == 'hybrid':
                    impact = max(finding.quantitative_impact_amount or 0, finding.manual_monetary_impact_amount or 0)
                else:
                    impact = finding.quantitative_impact_amount
                total += impact or 0.0
            record.total_quantitative_impact = total

    @api.depends('total_quantitative_impact', 'company_id', 'fiscal_year', 'compensating_control_id', 'is_compensating_control_effective')
    def _compute_aggregated_classification(self):
        for record in self:
            # Fetch active materiality
            materiality = self.env['icofr.materiality'].search([
                ('company_id', '=', record.company_id.id),
                ('fiscal_year', '=', record.fiscal_year),
                ('active', '=', True)
            ], limit=1)

            # Use defaults if no materiality found
            om_threshold = materiality.overall_materiality_amount if materiality else 1000000000.0
            pm_threshold = materiality.performance_materiality_amount if materiality else 500000000.0

            res = 'control_deficiency'
            if record.total_quantitative_impact > om_threshold:
                res = 'material_weakness'
            elif record.total_quantitative_impact > pm_threshold:
                res = 'significant_deficiency'
            
            # Downgrade logic via Compensating Control (Hal 69)
            if record.compensating_control_id and record.is_compensating_control_effective:
                if res == 'material_weakness':
                    res = 'significant_deficiency'
                elif res == 'significant_deficiency':
                    res = 'control_deficiency'

            record.aggregated_deficiency_class = res

    def action_confirm_evaluation(self):
        self.write({'state': 'confirmed'})
        return True

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
        return True
