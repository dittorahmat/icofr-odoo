# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrFinding(models.Model):
    """
    Extending the existing finding model to add manual impact and deficiency adjustment capabilities
    """
    _inherit = 'icofr.finding'
    
    # Manual input fields for Lini 3 to specify monetary impact
    manual_monetary_impact_amount = fields.Float(
        string='Dampak Moneter Manual',
        help='Nilai dampak moneter yang dimasukkan secara manual oleh Lini 3'
    )

    manual_impact_currency_id = fields.Many2one(
        'res.currency',
        string='Mata Uang Dampak Manual',
        default=lambda self: self.env.company.currency_id,
        help='Mata uang untuk nilai dampak moneter manual'
    )

    manual_qualitative_impact_score = fields.Float(
        string='Skor Dampak Kualitatif Manual',
        help='Skor kualitatif untuk dampak temuan yang diinput manual oleh Lini 3'
    )

    # Field to allow Lini 2/management to override system classification
    override_deficiency_classification = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('significant_deficiency', 'Kekurangan Signifikan'),
        ('material_weakness', 'Kelemahan Material')
    ], string='Klasifikasi Defisiensi Manual',
       help='Klasifikasi defisiensi yang ditentukan secara manual oleh Lini 2/manajemen')

    override_reason = fields.Text(
        string='Alasan Override',
        help='Alasan manajemen untuk mengoverride klasifikasi defisiensi sistem'
    )

    overridden_by_id = fields.Many2one(
        'res.users',
        string='Dioverride Oleh',
        help='Pengguna yang melakukan override terhadap klasifikasi defisiensi'
    )

    override_date = fields.Datetime(
        string='Tanggal Override',
        help='Tanggal klasifikasi defisiensi dilakukan override'
    )

    # Enhanced impact assessment fields
    impact_assessment_method = fields.Selection([
        ('automatic', 'Otomatis (berdasarkan kuantitatif dan kualitatif)'),
        ('manual', 'Manual'),
        ('hybrid', 'Gabungan (Otomatis + Justifikasi Manual)')
    ], string='Metode Penilaian Dampak', default='automatic',
       help='Metode yang digunakan untuk menilai dampak temuan')

    # Method to apply manual override
    def action_apply_override(self):
        """Method to apply manual override to deficiency classification"""
        for record in self:
            if record.override_deficiency_classification:
                record.deficiency_classified = record.override_deficiency_classification
                record.overridden_by_id = self.env.user
                record.override_date = fields.Datetime.now()
                
                # Log the change
                record.message_post(
                    body=f"Klasifikasi defisiensi diubah menjadi '{dict(record._fields['override_deficiency_classification'].selection).get(record.override_deficiency_classification)}' secara manual. "
                         f"Alasan: {record.override_reason or 'Tidak ada alasan diberikan.'}",
                    subtype_xmlid='mail.mt_note',
                    author_id=self.env.user.partner_id.id
                )
        return True

    # Override the compute method to incorporate manual inputs
    @api.depends('severity_level', 'quantitative_impact_amount', 'qualitative_impact_score',
                 'manual_monetary_impact_amount', 'manual_qualitative_impact_score',
                 'override_deficiency_classification')
    def _compute_deficiency_classification(self):
        """Compute deficiency classification with option for manual override"""
        for record in self:
            # Check if there is a manual override
            if record.override_deficiency_classification:
                record.deficiency_classified = record.override_deficiency_classification
                continue
            
            # Use manual inputs if provided and method is manual or hybrid
            if record.impact_assessment_method == 'manual':
                monetary_impact = record.manual_monetary_impact_amount
                qualitative_score = record.manual_qualitative_impact_score
            elif record.impact_assessment_method == 'hybrid':
                # Use the higher of automatic or manual values for more conservative approach
                monetary_impact = max(record.quantitative_impact_amount or 0, record.manual_monetary_impact_amount or 0)
                qualitative_score = max(record.qualitative_impact_score or 0, record.manual_qualitative_impact_score or 0)
            else:  # automatic
                monetary_impact = record.quantitative_impact_amount
                qualitative_score = record.qualitative_impact_score

            # Apply classification rules based on values
            if record.severity_level == 'critical' or monetary_impact > 1000000000 or qualitative_score >= 4.5:
                record.deficiency_classified = 'material_weakness'
            elif record.severity_level == 'high' or monetary_impact > 100000000 or qualitative_score >= 3.5:
                record.deficiency_classified = 'significant_deficiency'
            else:
                record.deficiency_classified = 'control_deficiency'

    @api.depends('deficiency_classified', 'quantitative_impact_amount', 'qualitative_impact_score', 
                 'manual_monetary_impact_amount', 'manual_qualitative_impact_score', 'severity_level',
                 'override_deficiency_classification', 'override_reason')
    def _compute_classification_reason(self):
        """Computes the reason for the (auto or manual) classification"""
        for record in self:
            reasons = []
            
            # Check if there's a manual override
            if record.override_deficiency_classification:
                reasons.append(f"Dioverride manual ke {dict(record._fields['override_deficiency_classification'].selection).get(record.override_deficiency_classification)}")
                if record.override_reason:
                    reasons.append(f"Alasan override: {record.override_reason}")
            else:
                # Automatic classification reasons
                if record.severity_level == 'critical':
                    reasons.append('Tingkat keparahan kritis')
                elif record.severity_level == 'high':
                    reasons.append('Tingkat keparahan tinggi')

                # Check monetary impact (using appropriate value based on method)
                monetary_impact = record.manual_monetary_impact_amount if record.impact_assessment_method in ['manual', 'hybrid'] else (record.quantitative_impact_amount or 0)
                if monetary_impact and monetary_impact > 1000000000:
                    reasons.append(f'Dampak kuantitatif sangat tinggi: Rp. {monetary_impact:,.0f}')
                elif monetary_impact and monetary_impact > 100000000:
                    reasons.append(f'Dampak kuantitatif menengah: Rp. {monetary_impact:,.0f}')

                # Check qualitative score
                qualitative_score = record.manual_qualitative_impact_score if record.impact_assessment_method in ['manual', 'hybrid'] else (record.qualitative_impact_score or 0)
                if qualitative_score and qualitative_score >= 4.5:
                    reasons.append(f'Skor dampak kualitatif sangat tinggi: {qualitative_score}')
                elif qualitative_score and qualitative_score >= 3.5:
                    reasons.append(f'Skor dampak kualitatif tinggi: {qualitative_score}')

            record.classification_reason = ', '.join(reasons) if reasons else 'Tidak ada kriteria klasifikasi yang terpenuhi'