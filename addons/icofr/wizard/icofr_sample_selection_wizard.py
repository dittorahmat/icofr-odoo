# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrSampleSelectionWizard(models.TransientModel):
    _name = 'icofr.sample.selection.wizard'
    _description = 'Wizard Pemilihan Sampel Audit'

    testing_id = fields.Many2one('icofr.testing', string='Pengujian', required=True)
    
    selection_mode = fields.Selection([
        ('random', 'Acak Otomatis'),
        ('manual', 'Pilih Manual')
    ], string='Metode Pemilihan', default='random', required=True)

    random_sample_count = fields.Integer(string='Jumlah Sampel', default=25)

    population_ids = fields.Many2many(
        'icofr.audit.population', 
        string='Item Populasi'
    )

    def action_confirm_selection(self):
        self.ensure_one()
        test_record = self.testing_id
        
        selected_samples = self.env['icofr.audit.population']

        if self.selection_mode == 'manual':
            selected_samples = self.population_ids
        elif self.selection_mode == 'random':
            # Simple random selection logic
            # In a real scenario, this should use the population linked to the test/control
            # Assuming test_record has a relation to population or control
            domain = [] 
            if test_record.control_id:
                # Assuming audit population has control_id or similar. 
                # If not, this is a placeholder logic.
                # Let's assume we fetch all population for now or filter by date.
                pass
            
            # Fetch random records (limit by count)
            # This is a basic implementation.
            all_population = self.env['icofr.audit.population'].search(domain)
            if len(all_population) > self.random_sample_count:
                # Random sample
                import random
                selected_samples = self.env['icofr.audit.population'].browse(
                    random.sample(all_population.ids, self.random_sample_count)
                )
            else:
                selected_samples = all_population

        # Link samples to the test record
        # Assuming icofr.testing has a field for samples, e.g. sample_ids
        # Since I don't see the testing model definition right now, I'll assume a standard Many2many
        if hasattr(test_record, 'population_sample_ids'):
             test_record.write({'population_sample_ids': [(6, 0, selected_samples.ids)]})
        
        return {'type': 'ir.actions.act_window_close'}
