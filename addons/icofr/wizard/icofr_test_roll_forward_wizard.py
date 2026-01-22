# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IcofrTestRollForwardWizard(models.TransientModel):
    _name = 'icofr.test.roll.forward.wizard'
    _description = 'Wizard Roll-forward Testing'

    test_id = fields.Many2one('icofr.testing', string='Pengujian Interim', required=True)
    roll_forward_date = fields.Date(string='Tanggal Pengujian Baru', default=fields.Date.today, required=True)
    roll_forward_period = fields.Char(string='Periode Pemutakhiran', required=True, placeholder="Contoh: Okt - Des 2024")
    
    def action_confirm(self):
        self.ensure_one()
        if self.test_id.status not in ['approved', 'completed', 'reviewed']:
            raise UserError(_("Hanya pengujian interim yang sudah Selesai, Direview, atau Disetujui yang dapat di-roll forward."))
            
        # Create the roll-forward record
        new_test = self.test_id.copy({
            'name': f"Roll-forward: {self.test_id.name}",
            'is_roll_forward': True,
            'original_test_id': self.test_id.id,
            'test_date': self.roll_forward_date,
            'roll_forward_period': self.roll_forward_period,
            'status': 'planned',
            'test_results': f"Roll-forward dari {self.test_id.name}. Fokus pada periode {self.roll_forward_period}.",
            'evidence_attachment_ids': [], # Clear previous evidence
        })
        
        return {
            'name': _('Pengujian Roll-forward Baru'),
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.testing',
            'res_id': new_test.id,
            'view_mode': 'form',
            'target': 'current',
        }