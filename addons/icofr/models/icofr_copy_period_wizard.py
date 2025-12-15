# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCopyPeriodWizard(models.TransientModel):
    """
    Wizard untuk menyalin data ICORF dari satu periode ke periode berikutnya
    Sesuai dengan kebutuhan PwC untuk efisiensi penggunaan sistem
    """
    _name = 'icofr.copy.period.wizard'
    _description = 'Wizard Salin Data ICORF Antar Periode'

    source_period = fields.Char(
        string='Periode Sumber',
        required=True,
        help='Periode sumber dari mana data akan disalin (misalnya: 2024)'
    )

    target_period = fields.Char(
        string='Periode Tujuan',
        required=True,
        help='Periode tujuan ke mana data akan disalin (misalnya: 2025)'
    )

    copy_processes = fields.Boolean(
        string='Salin Proses Bisnis',
        default=True,
        help='Salin data proses bisnis dari periode sumber ke periode tujuan'
    )

    copy_controls = fields.Boolean(
        string='Salin Kontrol Internal',
        default=True,
        help='Salin data kontrol internal dari periode sumber ke periode tujuan'
    )

    copy_risks = fields.Boolean(
        string='Salin Risiko',
        default=True,
        help='Salin data risiko dari periode sumber ke periode tujuan'
    )

    copy_findings = fields.Boolean(
        string='Salin Temuan',
        default=False,  # Default false karena temuan biasanya kontekstual per periode
        help='Salin data temuan dari periode sumber ke periode tujuan'
    )

    copy_action_plans = fields.Boolean(
        string='Salin Rencana Tindakan',
        default=False,  # Default false karena rencana tindakan biasanya kontekstual per periode
        help='Salin data rencana tindakan dari periode sumber ke periode tujuan'
    )

    copy_schedules = fields.Boolean(
        string='Salin Jadwal Pengujian',
        default=True,
        help='Salin data jadwal pengujian dari periode sumber ke periode tujuan'
    )

    copy_certifications = fields.Boolean(
        string='Salin Sertifikasi',
        default=False,  # Default false karena sertifikasi biasanya tahunan
        help='Salin data sertifikasi dari periode sumber ke periode tujuan'
    )

    copy_reports = fields.Boolean(
        string='Salin Laporan POJK',
        default=False,  # Default false karena laporan kontekstual per periode
        help='Salin data laporan POJK dari periode sumber ke periode tujuan'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait proses salin data'
    )

    def action_copy_period_data(self):
        """Method utama untuk menyalin data dari satu periode ke periode lain"""
        self.ensure_one()
        
        # Dictionary untuk menyimpan statistik penyalinan
        stats = {}

        if self.copy_processes:
            stats['processes'] = self._copy_processes()

        if self.copy_controls:
            stats['controls'] = self._copy_controls()

        if self.copy_risks:
            stats['risks'] = self._copy_risks()

        if self.copy_findings:
            stats['findings'] = self._copy_findings()

        if self.copy_action_plans:
            stats['action_plans'] = self._copy_action_plans()

        if self.copy_schedules:
            stats['schedules'] = self._copy_schedules()

        if self.copy_certifications:
            stats['certifications'] = self._copy_certifications()

        if self.copy_reports:
            stats['reports'] = self._copy_reports()
        
        # Return pesan sukses dengan statistik
        summary_message = self._generate_summary_message(stats)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sukses!',
                'message': summary_message,
                'type': 'success',
                'sticky': False,
            }
        }

    def _copy_processes(self):
        """Method untuk menyalin proses bisnis"""
        processes_source = self.env['icofr.process'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for process in processes_source:
            # Copy the process record with updated target period
            process.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.process') or '/',
                'fiscal_year': self.target_period,
                'name': f"{process.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_controls(self):
        """Method untuk menyalin kontrol internal"""
        controls_source = self.env['icofr.control'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')  # Fixed to use source_period
        ])

        copied_count = 0
        for control in controls_source:
            # Copy the control record with updated target period
            control.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.control') or '/',
                'fiscal_year': self.target_period,
                'name': f"{control.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_risks(self):
        """Method untuk menyalin risiko"""
        risks_source = self.env['icofr.risk'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for risk in risks_source:
            # Copy the risk record with updated target period
            risk.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.risk') or '/',
                'fiscal_year': self.target_period,
                'name': f"{risk.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_findings(self):
        """Method untuk menyalin temuan"""
        findings_source = self.env['icofr.finding'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for finding in findings_source:
            # Copy the finding record with updated target period
            finding.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.finding') or '/',
                'fiscal_year': self.target_period,
                'name': f"{finding.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_action_plans(self):
        """Method untuk menyalin rencana tindakan"""
        action_plans_source = self.env['icofr.action.plan'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for action_plan in action_plans_source:
            # Copy the action plan record with updated target period
            action_plan.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.action.plan') or '/',
                'fiscal_year': self.target_period,
                'name': f"{action_plan.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_schedules(self):
        """Method untuk menyalin jadwal pengujian"""
        schedules_source = self.env['icofr.testing.schedule'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for schedule in schedules_source:
            # Copy the schedule record with updated target period
            schedule.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.testing.schedule') or '/',
                'fiscal_year': self.target_period,
                'name': f"{schedule.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_certifications(self):
        """Method untuk menyalin sertifikasi"""
        certifications_source = self.env['icofr.certification'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for certification in certifications_source:
            # Copy the certification record with updated target period
            certification.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.certification') or '/',
                'fiscal_year': self.target_period,
                'name': f"{certification.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _copy_reports(self):
        """Method untuk menyalin laporan POJK"""
        reports_source = self.env['icofr.pojk.report'].search([
            '|', ('fiscal_year', '=', self.source_period),
                 ('create_date', 'like', f'{self.source_period}%')
        ])

        copied_count = 0
        for report in reports_source:
            # Copy the report record with updated target period
            report.copy(default={
                'code': self.env['ir.sequence'].next_by_code('icofr.pojk.report') or '/',
                'fiscal_year': self.target_period,
                'name': f"{report.name} - {self.target_period}",
            })
            copied_count += 1

        return copied_count

    def _generate_summary_message(self, stats):
        """Generate summary message of the copy operation"""
        summary_parts = []
        for model, count in stats.items():
            if count > 0:
                model_names = {
                    'processes': 'Proses Bisnis',
                    'controls': 'Kontrol Internal',
                    'risks': 'Risiko',
                    'findings': 'Temuan',
                    'action_plans': 'Rencana Tindakan',
                    'schedules': 'Jadwal Pengujian',
                    'certifications': 'Sertifikasi',
                    'reports': 'Laporan POJK'
                }
                summary_parts.append(f"{model_names.get(model, model.title())}: {count} record")

        if not summary_parts:
            return "Tidak ada data yang disalin karena semua opsi penyalinan dinonaktifkan."

        return f"Data dari periode {self.source_period} berhasil disalin ke periode {self.target_period}. Rincian: " + "; ".join(summary_parts)