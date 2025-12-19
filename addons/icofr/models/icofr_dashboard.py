# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta

class IcofrDashboard(models.Model):
    _name = 'icofr.dashboard'
    _description = 'ICORF Dashboard Metrics'

    name = fields.Char(string='Dashboard Name', default='ICORF Dashboard')

    # Metrics Fields
    total_controls = fields.Integer(string='Total Kontrol', compute='_compute_metrics')
    effective_controls = fields.Integer(string='Kontrol Efektif', compute='_compute_metrics')
    total_risks = fields.Integer(string='Total Risiko', compute='_compute_metrics')
    high_risks = fields.Integer(string='Risiko Tinggi', compute='_compute_metrics')
    compliance_rate = fields.Float(string='Rata-rata Kepatuhan', compute='_compute_metrics')
    upcoming_tests_count = fields.Integer(string='Pengujian Mendatang', compute='_compute_metrics')
    overdue_tests_count = fields.Integer(string='Pengujian Terlambat', compute='_compute_metrics')

    # Relation Fields for Display
    control_summary_ids = fields.Many2many('icofr.control', compute='_compute_metrics', string='Ringkasan Kontrol')
    recent_risks_ids = fields.Many2many('icofr.risk', compute='_compute_metrics', string='Risiko Terbaru')
    scheduled_testing_ids = fields.Many2many('icofr.testing', compute='_compute_metrics', string='Pengujian Terjadwal')
    recent_control_status_ids = fields.Many2many('icofr.control', compute='_compute_metrics', string='Status Kontrol Terbaru')

    def _compute_metrics(self):
        for record in self:
            # Controls
            all_controls = self.env['icofr.control'].search([])
            record.total_controls = len(all_controls)
            record.effective_controls = len(all_controls.filtered(lambda c: c.effectiveness_rating == 'high'))
            
            # Risks
            all_risks = self.env['icofr.risk'].search([])
            record.total_risks = len(all_risks)
            record.high_risks = len(all_risks.filtered(lambda r: r.risk_level in ('high', 'very_high')))

            # Compliance
            record.compliance_rate = (record.effective_controls / record.total_controls * 100) if record.total_controls > 0 else 0

            # Tests
            today = fields.Date.today()
            next_30_days = today + timedelta(days=30)
            upcoming = self.env['icofr.testing'].search([('test_date', '>=', today), ('test_date', '<=', next_30_days)])
            record.upcoming_tests_count = len(upcoming)
            
            overdue = self.env['icofr.testing'].search([('test_date', '<', today), ('status', '!=', 'completed')])
            record.overdue_tests_count = len(overdue)

            # Lists
            record.control_summary_ids = all_controls[:5]
            record.recent_risks_ids = all_risks[:5]
            record.scheduled_testing_ids = upcoming[:5]
            record.recent_control_status_ids = all_controls[:5]

    def action_refresh_dashboard(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Dashboard Diperbarui',
                'message': 'Data dashboard telah diperbarui',
                'type': 'success',
                'sticky': False
            }
        }

    def action_export_dashboard_data(self):
        wizard = self.env['icofr.export.wizard'].create({
            'export_type': 'all',
            'export_format': 'xlsx'
        })
        return {
            'name': 'Ekspor Data Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.export.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
