# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta

class IcofrDashboard(models.Model):
    _name = 'icofr.dashboard'
    _description = 'ICORF Dashboard Metrics'

    name = fields.Char(string='Dashboard Name', default='ICORF Dashboard')

    # Period selection field
    fiscal_year = fields.Selection(
        selection='_get_fiscal_years',
        string='Tahun Fiskal',
        default=lambda self: str(fields.Date.today().year),
        help='Tahun fiskal untuk menampilkan data pada dashboard'
    )

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
            # Get the fiscal year to filter data
            fiscal_year = record.fiscal_year or str(fields.Date.today().year)

            # Controls - filtering by fiscal year if possible
            # First get all controls, then filter if a fiscal year field exists in the model
            all_controls_domain = []

            # Check if there's a fiscal year field in the control model (like in CSA campaigns)
            # Since controls don't have direct fiscal_year, we'll need to filter based on related campaigns or other period indicators
            all_controls = self.env['icofr.control'].search(all_controls_domain)

            # Filter controls based on related testing or CSA that match the fiscal year
            # For now, we'll use all controls, but in a real implementation we might filter by related fiscal data
            controls_to_count = all_controls
            record.total_controls = len(controls_to_count)
            record.effective_controls = len(controls_to_count.filtered(lambda c: c.effectiveness_rating == 'high'))

            # Risks - using similar approach
            all_risks = self.env['icofr.risk'].search([])
            record.total_risks = len(all_risks)
            record.high_risks = len(all_risks.filtered(lambda r: r.risk_level in ('high', 'very_high')))

            # Compliance
            record.compliance_rate = (record.effective_controls / record.total_controls * 100) if record.total_controls > 0 else 0

            # Tests - filter by date range based on fiscal year
            from datetime import datetime
            start_date = datetime.strptime(f"{fiscal_year}-01-01", "%Y-%m-%d").date()
            end_date = datetime.strptime(f"{fiscal_year}-12-31", "%Y-%m-%d").date()

            today = fields.Date.today()

            # Filter upcoming tests for the fiscal year
            next_30_days = today + timedelta(days=30)
            upcoming = self.env['icofr.testing'].search([
                ('test_date', '>=', today),
                ('test_date', '<=', next_30_days),
                ('test_date', '>=', start_date),
                ('test_date', '<=', end_date)
            ])
            record.upcoming_tests_count = len(upcoming)

            # Filter overdue tests for the fiscal year
            overdue = self.env['icofr.testing'].search([
                ('test_date', '<', today),
                ('status', '!=', 'completed'),
                ('test_date', '>=', start_date),
                ('test_date', '<=', end_date)
            ])
            record.overdue_tests_count = len(overdue)

            # Lists - filter based on fiscal year
            record.control_summary_ids = controls_to_count[:5]
            record.recent_risks_ids = all_risks[:5]
            scheduled_testing_records = self.env['icofr.testing'].search([
                ('test_date', '>=', start_date),
                ('test_date', '<=', end_date)
            ])
            record.scheduled_testing_ids = scheduled_testing_records[:5]  # Get scheduled tests for the fiscal year
            record.recent_control_status_ids = controls_to_count[:5]

    def _get_fiscal_years(self):
        """Get available fiscal years from CSA campaigns and other period-based data"""
        # Get fiscal years from CSA campaigns
        campaigns = self.env['icofr.csa.campaign'].search([])
        years = campaigns.mapped('fiscal_year')

        # Also consider testing dates for more comprehensive year coverage
        tests = self.env['icofr.testing'].search([])
        for test in tests:
            if test.test_date:
                year = str(test.test_date.year)
                if year not in years:
                    years.append(year)

        # Add current year and a few previous years if not present
        current_year = str(fields.Date.today().year)
        if current_year not in years:
            years.append(current_year)

        # Add a few previous years if not present
        for i in range(1, 4):
            prev_year = str(int(current_year) - i)
            if prev_year not in years:
                years.append(prev_year)

        # Sort years in descending order and format for selection
        sorted_years = sorted(years, reverse=True)
        return [(year, year) for year in sorted_years]

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
