# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json

class IcofrOnboardingStagingLine(models.Model):
    _name = 'icofr.onboarding.staging.line'
    _description = 'ICORF Onboarding Staging Line'

    session_id = fields.Many2one('icofr.onboarding.session', string='Session', required=True, ondelete='cascade')
    type = fields.Selection([
        ('fsli', 'FSLI Structure'),
        ('entity', 'Entity Reconciliation'),
        ('gl', 'General Ledger Balance'),
        ('risk', 'Risk'),
        ('control', 'Control'),
        ('rcm', 'Risk-Control Mapping')
    ], string='Type', required=True)
    
    raw_data = fields.Text(string='Raw Data (JSON)')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Valid'),
        ('error', 'Error'),
        ('processed', 'Processed')
    ], string='Status', default='draft')
    
    error_log = fields.Text(string='Error Log')
    
    # Generic reference to created record if needed
    res_model = fields.Char(string='Target Model')
    res_id = fields.Integer(string='Target ID')

    def get_data(self):
        if self.raw_data:
            return json.loads(self.raw_data)
        return {}

    def set_data(self, data):
        self.raw_data = json.dumps(data)
