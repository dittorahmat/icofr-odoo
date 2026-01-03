# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
from io import BytesIO


class IcofrRCMUploadWizard(models.TransientModel):
    """
    Wizard untuk upload Excel data RCM (Risk-Control Matrix) ke sistem ICORF
    """
    _name = 'icofr.rcm.upload.wizard'
    _description = 'Wizard Upload RCM (Risk-Control Matrix)'

    excel_file = fields.Binary(
        string='File Excel RCM',
        required=True,
        help='File Excel yang berisi data RCM (Risk-Control Matrix)'
    )

    file_name = fields.Char(
        string='Nama File',
        help='Nama file Excel RCM yang diupload'
    )

    import_result = fields.Text(
        string='Hasil Import RCM',
        readonly=True,
        help='Detail hasil import data RCM dari Excel'
    )

    def action_upload_rcm_excel(self):
        """
        Method untuk memproses upload dan import data Excel ke RCM (Risk-Control Matrix)
        """
        self.ensure_one()

        if not self.excel_file:
            raise ValidationError("Silakan pilih file Excel RCM terlebih dahulu.")

        if not self.file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(self.excel_file)

            import xlrd
            workbook = xlrd.open_workbook(file_contents=decoded_file)
            
            # Gunakan sheet pertama atau cari sheet yang relevan
            worksheet = workbook.sheet_by_index(0)

            # Baca header dari baris pertama
            headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

            # Validasi header minimal yang harus ada
            required_headers = ['ID Risiko', 'Deskripsi Risiko', 'ID Kontrol', 'Deskripsi Kontrol']
            missing_headers = [header for header in required_headers if header not in headers]
            
            if missing_headers:
                raise ValidationError(f'Header berikut tidak ditemukan dalam file Excel: {", ".join(missing_headers)}')

            # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
            created_risks = []
            created_controls = []
            associated_mappings = []
            error_messages = []

            # Dapatkan model yang dibutuhkan
            risk_model = self.env['icofr.risk']
            control_model = self.env['icofr.control']
            process_model = self.env['icofr.process']

            for row_idx in range(1, worksheet.nrows):
                try:
                    row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]
                    
                    # Konversi ke dictionary
                    row_dict = dict(zip(headers, row_data))

                    # Ambil data RCM dari Excel
                    risk_code = str(row_dict.get('ID Risiko', '')).strip()
                    risk_name = str(row_dict.get('Deskripsi Risiko', '')).strip()
                    control_code = str(row_dict.get('ID Kontrol', '')).strip()
                    control_name = str(row_dict.get('Deskripsi Kontrol', '')).strip()

                    # Validasi bahwa kode risiko dan kontrol ada
                    if not risk_code or not control_code:
                        error_messages.append(f'Baris {row_idx + 1}: Kode Risiko dan Kode Kontrol wajib diisi.')
                        continue

                    # Ambil data tambahan jika tersedia
                    risk_category = str(row_dict.get('Kategori Risiko', 'operational')).strip()
                    control_type = str(row_dict.get('Tipe Kontrol', 'preventive')).strip()
                    assertion_exists = row_dict.get('Asersi Keberadaan', False)
                    assertion_complete = row_dict.get('Asersi Kelengkapan', False)
                    assertion_accuracy = row_dict.get('Asersi Akurasi', False)
                    assertion_auth = row_dict.get('Asersi Otorisasi', False)
                    assertion_valuation = row_dict.get('Asersi Valuasi', False)
                    
                    # Cek apakah proses bisnis terkait disertakan
                    process_code = str(row_dict.get('Kode Proses Bisnis', '')).strip()
                    process_id = None
                    if process_code:
                        process = process_model.search([('code', '=', process_code)], limit=1)
                        if process:
                            process_id = process.id
                        else:
                            error_messages.append(f'Baris {row_idx + 1}: Proses dengan kode "{process_code}" tidak ditemukan.')

                    # Cek apakah risiko sudah ada
                    existing_risk = risk_model.search([('code', '=', risk_code)], limit=1)
                    if existing_risk:
                        risk = existing_risk
                        updated_risk = True
                    else:
                        # Buat risiko baru
                        risk_data = {
                            'name': risk_name,
                            'code': risk_code,
                            'risk_category': risk_category,
                            'description': risk_name,
                        }
                        risk = risk_model.create(risk_data)
                        created_risks.append(risk.code)
                        updated_risk = False

                    # Cek apakah kontrol sudah ada
                    existing_control = control_model.search([('code', '=', control_code)], limit=1)
                    if existing_control:
                        control = existing_control
                        updated_control = True
                    else:
                        # Buat kontrol baru
                        control_data = {
                            'name': control_name,
                            'code': control_code,
                            'control_type': control_type if control_type in ['preventive', 'detective', 'corrective'] else 'preventive',
                            'description': control_name,
                            'assertion_existence': assertion_exists,
                            'assertion_completeness': assertion_complete,
                            'assertion_accuracy': assertion_accuracy,
                            'assertion_authorization': assertion_auth,
                            'assertion_valuation': assertion_valuation,
                            'process_id': process_id,
                        }
                        
                        # Set the control type according to valid options
                        if control_type in ['manual', 'semi_manual', 'automated', 'it_dependent']:
                            control_data['control_type_detailed'] = control_type
                        
                        control = control_model.create(control_data)
                        created_controls.append(control.code)
                        updated_control = False

                    # Hubungkan risiko dan kontrol (many2many relation jika ada)
                    if control not in risk.control_ids:
                        risk.write({'control_ids': [(4, control.id)]})
                        associated_mappings.append(f'Risiko {risk.code} - Kontrol {control.code}')

                except Exception as e:
                    error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data RCM - {str(e)}')

            # Buat pesan hasil import
            result_message = f"Import RCM selesai:\n"
            result_message += f"- Jumlah risiko baru: {len(created_risks)}\n"
            result_message += f"- Jumlah kontrol baru: {len(created_controls)}\n"
            result_message += f"- Jumlah asosiasi risiko-kontrol: {len(associated_mappings)}\n"

            if error_messages:
                result_message += f"- Jumlah error: {len(error_messages)}\n"
                result_message += "Daftar error:\n" + "\n".join(f"  - {err}" for err in error_messages)
            else:
                result_message += "Tidak ada error ditemukan."

            # Update hasil import
            self.import_result = result_message

            # Return action untuk menampilkan hasil
            action = {
                'type': 'ir.actions.act_window',
                'name': 'Hasil Import RCM',
                'res_model': 'icofr.rcm.upload.wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
                'context': self.env.context
            }

            return action

        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f"Error saat membaca file Excel: {str(e)}")

    def action_download_rcm_template(self):
        """
        Method untuk mengunduh template Excel untuk upload RCM
        """
        message = (
            'Template Excel RCM (Risk-Control Matrix) tersedia di direktori data modul ICORF.\n'
            'Kolom wajib: ID Risiko, Deskripsi Risiko, ID Kontrol, Deskripsi Kontrol\n'
            'Kolom opsional: Kategori Risiko, Tipe Kontrol, Asersi (Keberadaan, Kelengkapan, Akurasi, Otorisasi, Valuasi), Kode Proses Bisnis'
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Template Excel RCM',
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }