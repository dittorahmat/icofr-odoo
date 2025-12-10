# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from datetime import date, timedelta


class IcofrDashboardController(http.Controller):
    
    @http.route('/icofr/dashboard/data', type='json', auth='user')
    def get_dashboard_data(self):
        """Mengambil data untuk dashboard ICORF"""
        # Ambil data statistik untuk dashboard
        controls = request.env['icofr.control'].search([])
        total_controls = len(controls)
        
        effective_controls = len(controls.filtered(lambda c: c.effectiveness_rating == 'high'))
        
        risks = request.env['icofr.risk'].search([])
        total_risks = len(risks)
        
        high_risks = len(risks.filtered(lambda r: r.risk_level in ['high', 'very_high']))
        
        # Ambil data pengujian yang terjadwal
        today = date.today()
        next_30_days = today + timedelta(days=30)
        scheduled_tests = request.env['icofr.testing'].search([
            ('test_date', '>=', today),
            ('test_date', '<=', next_30_days),
            ('status', '!=', 'completed')
        ])
        
        # Data ringkasan kontrol
        control_summary = []
        for control in controls[:5]:  # Ambil 5 kontrol teratas
            control_summary.append({
                'name': control.name,
                'effectiveness': control.effectiveness_rating,
                'compliance_rate': control.compliance_rate,
                'next_test_date': control.next_test_date,
            })
        
        # Data risiko terbaru
        recent_risks = []
        for risk in risks.sorted(key=lambda r: r.create_date, reverse=True)[:5]:
            recent_risks.append({
                'name': risk.name,
                'risk_level': risk.risk_level,
                'owner': risk.owner_id.name,
                'status': risk.status,
            })
        
        # Data pengujian terjadwal
        scheduled_testing = []
        for test in scheduled_tests:
            scheduled_testing.append({
                'name': test.name,
                'control': test.control_id.name,
                'test_date': test.test_date,
                'tester': test.tester_id.name,
                'status': test.status,
            })
        
        return {
            'total_controls': total_controls,
            'effective_controls': effective_controls,
            'total_risks': total_risks,
            'high_risks': high_risks,
            'control_summary': control_summary,
            'recent_risks': recent_risks,
            'scheduled_testing': scheduled_testing,
        }
    
    @http.route('/icofr/export/control_data', type='http', auth='user')
    def export_control_data(self, **kwargs):
        """Ekspor data kontrol ke format CSV atau Excel"""
        # Dalam implementasi nyata, fungsi ini akan menghasilkan file untuk diunduh
        # Misalnya dalam format CSV atau Excel sesuai kebutuhan fungsional #9
        import io
        import csv
        from odoo.tools.safe_eval import safe_eval
        
        controls = request.env['icofr.control'].search([])
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Nama Kontrol', 'Kode', 'Jenis Kontrol', 'Frekuensi', 
            'Pemilik', 'Status', 'Efektivitas', 'Tanggal Terakhir Diuji',
            'Tanggal Pengujian Berikutnya', 'Total Pengujian', 'Pengujian Efektif'
        ])
        
        # Data
        for control in controls:
            writer.writerow([
                control.name, 
                control.code, 
                control.control_type, 
                control.frequency,
                control.owner_id.name,
                control.status,
                control.effectiveness_rating,
                control.last_tested_date,
                control.next_test_date,
                control.total_tests,
                control.effective_tests
            ])
        
        output.seek(0)
        csv_content = output.getvalue()
        
        return request.make_response(
            csv_content,
            headers=[
                ('Content-Type', 'text/csv'),
                ('Content-Disposition', 'attachment; filename="icofr_control_data.csv"')
            ]
        )