# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IcofrOnboardingSession(models.Model):
    _name = 'icofr.onboarding.session'
    _description = 'ICORF Onboarding Session'
    _order = 'create_date desc'

    name = fields.Char(string='Session Name', required=True, copy=False, default='New')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    state = fields.Selection([
        ('active', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='active', required=True)
    
    progress_percent = fields.Float(string='Progress (%)', default=0.0)
    total_lines = fields.Integer(string='Total Lines')
    processed_lines = fields.Integer(string='Processed Lines')
    
    staging_line_ids = fields.One2many('icofr.onboarding.staging.line', 'session_id', string='Staging Lines')
    
    _sql_constraints = [
        ('unique_active_session', 'unique(company_id, fiscal_year, state)', 
         'An active onboarding session already exists for this company and fiscal year!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('icofr.onboarding.session') or 'ONB/' + fields.Datetime.now().strftime('%Y%m%d/%H%M')
        return super(IcofrOnboardingSession, self).create(vals)

    def action_complete(self):
        self.write({'state': 'completed', 'progress_percent': 100.0})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        # Cleanup staging lines
        self.staging_line_ids.unlink()
