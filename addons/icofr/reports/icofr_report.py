# -*- coding: utf-8 -*-
from odoo import models, fields, api
import io
import base64
from datetime import datetime


class IcofrPojkReportTemplate(models.AbstractModel):
    _name = 'report.icofr.pojk_report_template'
    _description = 'Laporan POJK 15/2024 Template'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Menghasilkan nilai-nilai untuk template laporan"""
        docs = self.env['icofr.pojk.report'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'icofr.pojk.report',
            'docs': docs,
            'data': data,
        }


class IcofrPojkReport(models.Model):
    _inherit = 'icofr.pojk.report'

    def print_report(self):
        """Fungsi untuk mencetak laporan POJK dalam format PDF"""
        self.ensure_one()
        return self.env.ref('icofr.pojk_report_pdf').report_action(self)

    def export_to_excel(self):
        """Fungsi untuk mengekspor laporan ke format Excel"""
        try:
            # Impor library yang dibutuhkan
            import xlsxwriter

            # Buat buffer untuk file Excel
            output = io.BytesIO()

            # Buat workbook dan worksheet
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('Laporan POJK')

            # Format format
            header_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': '#3498db',
                'font_color': 'white'
            })

            title_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'align': 'center',
                'valign': 'vcenter'
            })

            section_format = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#ecf0f1',
                'border': 1
            })

            data_format = workbook.add_format({
                'border': 1,
                'text_wrap': True
            })

            # Tulis header
            worksheet.merge_range('A1:D1', f'LAPORAN POJK 15/2024 - {self.name}', title_format)
            worksheet.write('A3', 'Periode Pelaporan', section_format)
            worksheet.write('B3', self.reporting_period, data_format)
            worksheet.write('C3', 'Tahun Fiskal', section_format)
            worksheet.write('D3', self.fiscal_year, data_format)
            worksheet.write('A4', 'Tanggal Laporan', section_format)
            worksheet.write('B4', str(self.report_date), data_format)
            worksheet.write('C4', 'Perusahaan', section_format)
            worksheet.write('D4', self.company_id.name, data_format)

            # Statistik Utama
            row = 6
            worksheet.write(row, 0, 'Statistik Utama', section_format)
            row += 1
            worksheet.write(row, 0, 'Jumlah Total Kontrol', data_format)
            worksheet.write(row, 1, self.total_controls, data_format)
            worksheet.write(row, 2, 'Kontrol Efektif', data_format)
            worksheet.write(row, 3, self.effective_controls, data_format)
            row += 1
            worksheet.write(row, 0, 'Persentase Efektivitas', data_format)
            worksheet.write(row, 1, f"{self.effectiveness_percentage}%", data_format)
            worksheet.write(row, 2, 'Jumlah Total Risiko', data_format)
            worksheet.write(row, 3, self.total_risks, data_format)
            row += 1
            worksheet.write(row, 0, 'Risiko Tingkat Tinggi', data_format)
            worksheet.write(row, 1, self.high_risks, data_format)
            worksheet.write(row, 2, 'Jumlah Total Temuan', data_format)
            worksheet.write(row, 3, self.total_findings, data_format)
            row += 2

            # Penilaian Kerangka Kerja
            worksheet.write(row, 0, 'Penilaian Kerangka Kerja', section_format)
            row += 1
            worksheet.write(row, 0, 'Deskripsi Kerangka Kerja', data_format)
            worksheet.write(row, 1, self.framework_description or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Penilaian Lingkungan Pengendalian', data_format)
            worksheet.write(row, 1, self.control_environment_assessment or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Praktik Penilaian Risiko', data_format)
            worksheet.write(row, 1, self.risk_assessment_practices or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Efektivitas Aktivitas Pengendalian', data_format)
            worksheet.write(row, 1, self.control_activity_effectiveness or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Kualitas Informasi dan Komunikasi', data_format)
            worksheet.write(row, 1, self.information_communication_quality or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Hasil Aktivitas Pemantauan', data_format)
            worksheet.write(row, 1, self.monitoring_activity_results or '', data_format)
            row += 2

            # Temuan dan Respon
            worksheet.write(row, 0, 'Temuan dan Respon Manajemen', section_format)
            row += 1
            worksheet.write(row, 0, 'Detail Kekurangan Signifikan', data_format)
            worksheet.write(row, 1, self.significant_deficiencies_detail or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Detail Kelemahan Material', data_format)
            worksheet.write(row, 1, self.material_weaknesses_detail or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Detail Respon Manajemen', data_format)
            worksheet.write(row, 1, self.management_response_detail or '', data_format)
            row += 2

            # Tindakan Perbaikan
            worksheet.write(row, 0, 'Tindakan Perbaikan', section_format)
            row += 1
            worksheet.write(row, 0, 'Tindakan Perbaikan', data_format)
            worksheet.write(row, 1, self.improvement_actions or '', data_format)
            row += 2

            # Kepatuhan
            worksheet.write(row, 0, 'Kepatuhan', section_format)
            row += 1
            worksheet.write(row, 0, 'Status Kepatuhan', data_format)
            worksheet.write(row, 1, dict(self._fields['compliance_status'].selection).get(self.compliance_status, self.compliance_status), data_format)
            row += 1
            worksheet.write(row, 0, 'Catatan Kepatuhan', data_format)
            worksheet.write(row, 1, self.compliance_notes or '', data_format)

            # Tutup workbook
            workbook.close()

            # Ambil konten dari buffer
            output.seek(0)
            excel_data = output.read()

            # Buat attachment
            attachment = self.env['ir.attachment'].create({
                'name': f'Laporan_POJK_{self.fiscal_year}_{self.reporting_period}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(excel_data),
                'res_model': 'icofr.pojk.report',
                'res_id': self.id,
            })

            # Kembalikan action untuk download
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}/{attachment.name}?download=true',
                'target': 'self',
            }

        except ImportError:
            # Jika xlsxwriter tidak tersedia, beri tahu pengguna
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Export Excel Gagal',
                    'message': 'Modul xlsxwriter tidak terinstal. Mohon instal terlebih dahulu.',
                    'type': 'danger',
                    'sticky': True
                }
            }


class IcofrCertification(models.Model):
    _inherit = 'icofr.certification'

    def export_certification_to_excel(self):
        """Fungsi untuk mengekspor sertifikasi ke format Excel"""
        try:
            import xlsxwriter

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('Sertifikasi ICORF')

            # Format
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'align': 'center',
                'valign': 'vcenter'
            })

            section_format = workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#ecf0f1',
                'border': 1
            })

            data_format = workbook.add_format({
                'border': 1,
                'text_wrap': True
            })

            # Header
            worksheet.merge_range('A1:D1', f'SERTIFIKASI ICORF - {self.name}', title_format)
            worksheet.write('A3', 'Tahun Fiskal', section_format)
            worksheet.write('B3', self.fiscal_year, data_format)
            worksheet.write('C3', 'Tanggal Sertifikasi', section_format)
            worksheet.write('D3', str(self.certification_date), data_format)
            worksheet.write('A4', 'Disertifikasi Oleh', section_format)
            worksheet.write('B4', self.certified_by_id.name, data_format)
            worksheet.write('C4', 'Status', section_format)
            worksheet.write('D4', dict(self._fields['status'].selection).get(self.status, self.status), data_format)

            # Lingkup dan efektivitas
            row = 6
            worksheet.write(row, 0, 'Lingkup Sertifikasi', section_format)
            worksheet.write(row, 1, self.scope or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Deskripsi Lingkup', section_format)
            worksheet.write(row, 1, self.scope_description or '', data_format)
            row += 1
            worksheet.write(row, 0, 'Pernyataan Efektivitas', section_format)
            worksheet.write(row, 1, self.effectiveness_statement or '', data_format)
            row += 2

            # Temuan
            if self.finding_ids:
                worksheet.write(row, 0, 'Temuan', section_format)
                row += 1
                worksheet.write(row, 0, 'Nama Temuan', section_format)
                worksheet.write(row, 1, 'Jenis', section_format)
                worksheet.write(row, 2, 'Tingkat Keparahan', section_format)
                worksheet.write(row, 3, 'Status', section_format)
                row += 1

                for finding in self.finding_ids:
                    worksheet.write(row, 0, finding.name, data_format)
                    worksheet.write(row, 1, dict(finding._fields['finding_type'].selection).get(finding.finding_type, finding.finding_type), data_format)
                    worksheet.write(row, 2, dict(finding._fields['severity_level'].selection).get(finding.severity_level, finding.severity_level), data_format)
                    worksheet.write(row, 3, dict(finding._fields['status'].selection).get(finding.status, finding.status), data_format)
                    row += 1
                row += 1

            # Rencana Tindakan
            if self.action_plan_ids:
                worksheet.write(row, 0, 'Rencana Tindakan', section_format)
                row += 1
                worksheet.write(row, 0, 'Nama Tindakan', section_format)
                worksheet.write(row, 1, 'Status', section_format)
                worksheet.write(row, 2, 'Target Selesai', section_format)
                worksheet.write(row, 3, 'Prioritas', section_format)
                row += 1

                for action_plan in self.action_plan_ids:
                    worksheet.write(row, 0, action_plan.name, data_format)
                    worksheet.write(row, 1, dict(action_plan._fields['status'].selection).get(action_plan.status, action_plan.status), data_format)
                    worksheet.write(row, 2, str(action_plan.target_completion_date), data_format)
                    worksheet.write(row, 3, dict(action_plan._fields['priority'].selection).get(action_plan.priority, action_plan.priority), data_format)
                    row += 1

            workbook.close()

            output.seek(0)
            excel_data = output.read()

            attachment = self.env['ir.attachment'].create({
                'name': f'Sertifikasi_{self.fiscal_year}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(excel_data),
                'res_model': 'icofr.certification',
                'res_id': self.id,
            })

            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}/{attachment.name}?download=true',
                'target': 'self',
            }

        except ImportError:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Export Excel Gagal',
                    'message': 'Modul xlsxwriter tidak terinstal. Mohon instal terlebih dahulu.',
                    'type': 'danger',
                    'sticky': True
                }
            }