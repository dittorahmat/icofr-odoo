# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
from io import BytesIO


class IcofrAccountMappingUploadWizard(models.TransientModel):
    """
    Wizard untuk upload Excel data pemetaan akun ke FSLI
    """
    _name = 'icofr.account.mapping.upload.wizard'
    _description = 'Wizard Upload Pemetaan Akun ke FSLI dari Excel'

    excel_file = fields.Binary(
        string='File Excel',
        required=True,
        help='File Excel yang berisi data pemetaan akun ke FSLI'
    )

    file_name = fields.Char(
        string='Nama File',
        help='Nama file Excel yang diupload'
    )

    materiality_id = fields.Many2one(
        'icofr.materiality',
        string='Perhitungan Materialitas',
        required=True,
        help='Perhitungan materialitas yang akan digunakan untuk data yang diupload'
    )

    import_result = fields.Text(
        string='Hasil Import',
        readonly=True,
        help='Detail hasil import data dari Excel'
    )

    @api.model
    def default_get(self, fields):
        res = super(IcofrAccountMappingUploadWizard, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        # Jika wizard dipanggil dari halaman materiality, gunakan materiality tersebut
        if active_model == 'icofr.materiality' and active_id:
            res['materiality_id'] = active_id

        return res

    def action_upload_excel(self):
        """
        Method untuk memproses upload dan import data Excel ke pemetaan akun
        """
        self.ensure_one()

        if not self.excel_file:
            raise ValidationError("Silakan pilih file Excel terlebih dahulu.")

        if not self.file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(self.excel_file)
            workbook = xlrd.open_workbook(file_contents=decoded_file)
            worksheet = workbook.sheet_by_index(0)

            # Baca header dari baris pertama
            headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]
            
            # Validasi header
            required_headers = ['Kode Akun GL', 'Nama Akun GL', 'FSLI', 'Deskripsi FSLI', 'Tingkat Signifikansi']
            for header in required_headers:
                if header not in headers:
                    raise ValidationError(f'Header "{header}" tidak ditemukan dalam file Excel. '
                                          f'Header yang diperlukan: {", ".join(required_headers)}')

            # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
            created_records = []
            updated_records = []
            error_messages = []

            for row_idx in range(1, worksheet.nrows):
                try:
                    row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]
                    
                    # Konversi ke dictionary
                    row_dict = dict(zip(headers, row_data))
                    
                    # Validasi data
                    if not str(row_dict.get('Kode Akun GL', '')).strip():
                        error_messages.append(f'Baris {row_idx + 1}: Kode Akun GL tidak boleh kosong.')
                        continue
                    
                    # Cek apakah akun GL dengan kode tersebut ada di sistem Odoo
                    gl_account_code = str(row_dict.get('Kode Akun GL', '')).strip()
                    gl_account = self.env['account.account'].search([('code', '=', gl_account_code)], limit=1)
                    
                    if not gl_account:
                        # Jika tidak ditemukan, gunakan field manual
                        gl_account_manual = f"{gl_account_code} - {str(row_dict.get('Nama Akun GL', '')).strip()}"
                        gl_account_id = False
                    else:
                        # Gunakan akun GL dari sistem
                        gl_account_id = gl_account.id
                        gl_account_manual = False

                    # Siapkan data untuk pembuatan record
                    mapping_data = {
                        'gl_account_id': gl_account_id,
                        'gl_account_manual': gl_account_manual,
                        'fsl_item': str(row_dict.get('FSLI', '')).strip(),
                        'fsl_description': str(row_dict.get('Deskripsi FSLI', '')).strip(),
                        'materiality_id': self.materiality_id.id,
                        'significance_level': str(row_dict.get('Tingkat Signifikansi', 'moderate')).strip().lower(),
                        'notes': f'Diimport dari file: {self.file_name} pada baris {row_idx + 1}',
                    }

                    # Cek apakah sudah ada record dengan kombinasi yang sama
                    existing_record = self.env['icofr.account.mapping'].search([
                        '|',
                        ('gl_account_id', '=', gl_account_id if gl_account_id else -1),
                        ('gl_account_manual', '=', gl_account_manual if gl_account_manual else ''),
                        ('fsl_item', '=', mapping_data['fsl_item']),
                        ('materiality_id', '=', self.materiality_id.id)
                    ], limit=1)

                    if existing_record:
                        # Update record yang sudah ada
                        existing_record.write(mapping_data)
                        updated_records.append(existing_record.name)
                    else:
                        # Buat record baru
                        new_record = self.env['icofr.account.mapping'].create(mapping_data)
                        created_records.append(new_record.name)

                except Exception as e:
                    error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data - {str(e)}')

            # Buat pesan hasil import
            result_message = f"Import selesai:\n"
            result_message += f"- Jumlah record baru: {len(created_records)}\n"
            result_message += f"- Jumlah record diperbarui: {len(updated_records)}\n"
            
            if error_messages:
                result_message += f"- Jumlah error: {len(error_messages)}\n"
                result_message += "Daftar error:\n" + "\n".join(f"  - {err}" for err in error_messages)
            else:
                result_message += "Tidak ada error ditemukan."

            # Update hasil import
            self.write({'import_result': result_message})

            # Return action untuk menampilkan hasil
            action = {
                'type': 'ir.actions.act_window',
                'name': 'Hasil Import Excel',
                'res_model': 'icofr.account.mapping.upload.wizard',
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

    def action_download_template(self):
        """
        Method untuk mengunduh template Excel untuk upload
        """
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel template
        # Untuk sekarang, kita hanya menampilkan notifikasi
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Template Excel',
                'message': 'Template Excel tersedia di direktori data modul ICORF',
                'type': 'info',
                'sticky': False,
            }
        }