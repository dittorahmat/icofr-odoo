# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrDoDWizard(models.TransientModel):
    _name = 'icofr.dod.wizard'
    _description = 'Wizard Penentuan DoD (Degree of Deficiency)'

    finding_id = fields.Many2one('icofr.finding', string='Temuan', required=True, readonly=True)
    
    # Step 1: Link to Assertion
    q1_assertion_related = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='1. Apakah defisiensi berhubungan langsung dengan satu atau lebih asersi laporan keuangan?', required=True)

    # Step 2: Likelihood
    q2_likelihood = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='2. Apakah terdapat kemungkinan (likelihood) salah saji yang dihasilkan dari defisiensi tersebut?', 
       help="Pertimbangkan faktor risiko, frekuensi, dan penyebab.")

    # Step 3: Magnitude
    q3_material_magnitude = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='3. Apakah besaran (magnitude) potensi salah saji bersifat material?', 
       help="Bandingkan dengan nilai Materialitas (OM/PM).")

    # Step 4: Importance
    q4_important_attention = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='4. Apakah defisiensi cukup penting untuk mendapat perhatian dari pihak yang bertanggung jawab (Komite Audit/Direksi)?')

    # Step 5: Prudent Official
    q5_prudent_official = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='5. Apakah individu yang berpengetahuan luas (prudent official) akan menyimpulkan ini sebagai Kelemahan Material?')

    # Compensating Control Check
    q6_compensating_control = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='6. Apakah terdapat Kontrol Pengganti (Compensating Control) yang efektif?')

    final_classification = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol (CD)'),
        ('significant_deficiency', 'Kekurangan Signifikan (SD)'),
        ('material_weakness', 'Kelemahan Material (MW)'),
        ('none', 'Bukan Defisiensi')
    ], string='Kesimpulan Klasifikasi', compute='_compute_classification')

    @api.depends('q1_assertion_related', 'q2_likelihood', 'q3_material_magnitude', 
                 'q4_important_attention', 'q5_prudent_official', 'q6_compensating_control')
    def _compute_classification(self):
        for record in self:
            result = 'none'
            
            # Logic Flow based on Figure 5 (AS 2201)
            if record.q1_assertion_related == 'no':
                result = 'none'
            elif record.q2_likelihood == 'no':
                result = 'control_deficiency'
            else:
                # Likelihood is Yes
                if record.q3_material_magnitude == 'yes':
                    # Material Magnitude -> Potential MW
                    if record.q6_compensating_control == 'yes':
                        # Mitigated by Compensating Control -> Downgrade to SD or CD
                        # Usually downgrade one level from MW -> SD
                        result = 'significant_deficiency' 
                    else:
                        result = 'material_weakness'
                else:
                    # Not Material Magnitude
                    if record.q4_important_attention == 'yes':
                        result = 'significant_deficiency'
                    else:
                        result = 'control_deficiency'
                
                # Prudent Official Override (Specific to MW definition)
                if record.q5_prudent_official == 'yes':
                    result = 'material_weakness'

            record.final_classification = result

    def action_confirm(self):
        self.ensure_one()
        # Update the finding record
        self.finding_id.write({
            'override_deficiency_classification': self.final_classification if self.final_classification != 'none' else False,
            'override_reason': f"Hasil Wizard DoD:\n"
                               f"1. Hubungan Asersi: {self.q1_assertion_related}\n"
                               f"2. Kemungkinan Salah Saji: {self.q2_likelihood}\n"
                               f"3. Material: {self.q3_material_magnitude}\n"
                               f"4. Penting/Perhatian: {self.q4_important_attention}\n"
                               f"5. Prudent Official: {self.q5_prudent_official}\n"
                               f"6. Kontrol Pengganti: {self.q6_compensating_control}",
            'overridden_by_id': self.env.user.id,
            'override_date': fields.Datetime.now()
        })
        return {'type': 'ir.actions.act_window_close'}
