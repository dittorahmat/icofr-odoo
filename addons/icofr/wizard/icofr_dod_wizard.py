# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrDoDWizard(models.TransientModel):
    _name = 'icofr.dod.wizard'
    _description = 'Wizard Penentuan DoD (Degree of Deficiency)'

    finding_id = fields.Many2one('icofr.finding', string='Temuan', required=True, readonly=True)
    
    # Kotak 1: Link to Assertion
    q1_assertion_related = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='1. Apakah defisiensi berhubungan langsung dengan satu atau lebih asersi laporan keuangan?', required=True)

    # Kotak 2: Likelihood
    q2_likelihood = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='2. Apakah terdapat kemungkinan (likelihood) dari salah saji dihasilkan dari defisiensi tersebut?')

    # Kotak 3: Magnitude
    q3_material_magnitude = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='3. Apakah terdapat kemungkinan besaran (magnitude) dari potensi salah saji bersifat material?')

    # Kotak 4: Importance
    q4_important_attention = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='4. Apakah defisiensi cukup penting untuk mendapat perhatian dari pihak yang bertanggung jawab atas pengawasan pelaporan keuangan (Dewan Komisaris/Dewan Pengawas, Komite Audit, atau Direksi)?')

    # Kotak 5: Compensating Control
    q5_compensating_control = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='5. Apakah terdapat pengendalian yang dapat beroperasi secara efektif pada tingkat ketepatan yang cukup untuk mencegah atau mendeteksi salah saji material (Compensating Control)?')

    # Kotak 6: Prudent Official
    q6_prudent_official = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='6. Akankah individu yang berpengetahuan luas, kompeten dan objektif (prudent official) menyimpulkan defisiensi sebagai Kelemahan Material?')

    # Kotak 7: Aggregation
    q7_aggregation_needed = fields.Selection([
        ('yes', 'Ya'),
        ('no', 'Tidak')
    ], string='7. Apakah terdapat beberapa pengendalian defisiensi yang memengaruhi account balance atau disclosure dari laporan keuangan yang sama?')

    final_classification = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol (CD)'),
        ('significant_deficiency', 'Kekurangan Signifikan (SD)'),
        ('material_weakness', 'Kelemahan Material (MW)'),
        ('none', 'Bukan Defisiensi')
    ], string='Kesimpulan Klasifikasi', compute='_compute_classification')

    @api.depends('q1_assertion_related', 'q2_likelihood', 'q3_material_magnitude', 
                 'q4_important_attention', 'q5_compensating_control', 
                 'q6_prudent_official', 'q7_aggregation_needed')
    def _compute_classification(self):
        """
        Flow logic based on Juknis BUMN Lampiran 10 (Gambar 5 / AS 2201)
        """
        for record in self:
            result = 'none'
            
            # Start Flow
            # Kotak 1 & 2 & 3 leads to Kotak 4 or Kotak 5
            target_is_k4 = False
            target_is_k5 = False

            if record.q1_assertion_related == 'no':
                target_is_k4 = True
            elif record.q2_likelihood == 'no':
                target_is_k4 = True
            elif record.q3_material_magnitude == 'no':
                target_is_k4 = True
            else:
                target_is_k5 = True

            # Kotak 5 Flow
            if target_is_k5:
                if record.q5_compensating_control == 'yes':
                    target_is_k4 = True
                else:
                    result = 'material_weakness'

            # Kotak 4 Flow
            if target_is_k4:
                if record.q4_important_attention == 'yes':
                    # Pindah ke Kotak 6
                    if record.q6_prudent_official == 'yes':
                        result = 'material_weakness'
                    else:
                        result = 'significant_deficiency'
                else:
                    result = 'control_deficiency'

            record.final_classification = result

    def action_confirm(self):

        self.ensure_one()

        # Update the finding record

        self.finding_id.write({

            'override_deficiency_classification': self.final_classification if self.final_classification != 'none' else False,

            'override_reason': f"Hasil Wizard DoD (Lampiran 10):\n"

                               f"K1. Hubungan Asersi: {self.q1_assertion_related}\n"

                               f"K2. Likelihood: {self.q2_likelihood}\n"

                               f"K3. Magnitude Material: {self.q3_material_magnitude}\n"

                               f"K4. Penting/Perhatian: {self.q4_important_attention}\n"

                               f"K5. Kontrol Pengganti: {self.q5_compensating_control}\n"

                               f"K6. Prudent Official: {self.q6_prudent_official}\n"

                               f"K7. Agregasi: {self.q7_aggregation_needed}",

            'overridden_by_id': self.env.user.id,

            'override_date': fields.Datetime.now(),

            # Update Lampiran 10 Work Paper fields

            'box_1_direct_relation': self.q1_assertion_related == 'yes',

            'box_2_likelihood': self.q2_likelihood == 'yes',

            'box_3_magnitude': self.q3_material_magnitude == 'yes',

            'box_4_important': self.q4_important_attention == 'yes',

            'box_5_compensating': self.q5_compensating_control == 'yes',

            'box_6_prudent_official': self.q6_prudent_official == 'yes',

            'box_7_aggregate': self.q7_aggregation_needed == 'yes',

        })

        return {'type': 'ir.actions.act_window_close'}
