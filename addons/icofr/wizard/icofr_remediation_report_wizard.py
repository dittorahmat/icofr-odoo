# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

class IcofrRemediationReportWizard(models.TransientModel):
    _name = 'icofr.remediation.report.wizard'
    _description = 'Laporan Pemantauan Tindak Lanjut (Lampiran 13)'

    report_date = fields.Date(string='Tanggal Laporan', default=fields.Date.today, required=True)
    company_id = fields.Many2one('res.company', string='Perusahaan', default=lambda self: self.env.company, required=True)
    
    # Filter options
    filter_by_department = fields.Boolean(string='Filter per Departemen')
    department_names = fields.Char(string='Departemen (pisahkan koma)', help="Contoh: Finance, HR, IT")

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref('icofr.action_report_remediation_monitor').report_action(self)

    def get_remediation_stats(self):
        """
        Returns a dictionary of stats grouped by Department.
        Structure:
        {
            'Finance': {
                'total': 10,
                'open': 5,
                'closed': 5,
                'overdue': 2,
                'details': [recordset of overdue plans]
            }
        }
        """
        self.ensure_one()
        domain = [('company_id', '=', self.company_id.id)]
        
        plans = self.env['icofr.action.plan'].search(domain)
        
        stats = {}
        
        for plan in plans:
            dept = plan.responsible_department or 'Unassigned'
            
            # Simple filter if enabled
            if self.filter_by_department and self.department_names:
                allowed_depts = [d.strip().lower() for d in self.department_names.split(',')]
                if dept.lower() not in allowed_depts:
                    continue

            if dept not in stats:
                stats[dept] = {
                    'total': 0,
                    'open': 0,
                    'closed': 0,
                    'overdue': 0,
                    'details': self.env['icofr.action.plan']
                }
            
            stats[dept]['total'] += 1
            
            is_closed = plan.status == 'completed'
            if is_closed:
                stats[dept]['closed'] += 1
            else:
                stats[dept]['open'] += 1
                if plan.target_completion_date and plan.target_completion_date < self.report_date:
                    stats[dept]['overdue'] += 1
                    stats[dept]['details'] |= plan
        
        return stats
