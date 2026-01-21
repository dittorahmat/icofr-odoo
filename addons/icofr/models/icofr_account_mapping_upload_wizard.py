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

    import_type = fields.Selection([
        ('account_mapping', 'Pemetaan Akun'),
        ('financial_data', 'Data Keuangan')
    ], string='Jenis Import', default='account_mapping',
       help='Pilih jenis data yang akan diimport dari Excel')

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
        Method untuk memproses upload dan import data Excel ke pemetaan akun atau data keuangan
        """
        self.ensure_one()

        if not self.excel_file:
            raise ValidationError("Silakan pilih file Excel terlebih dahulu.")

        if not self.file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(self.excel_file)

            if self.import_type == 'account_mapping':
                return self._import_account_mapping(decoded_file)
            elif self.import_type == 'financial_data':
                return self._import_financial_data(decoded_file)
            else:
                raise ValidationError("Jenis import tidak valid.")

        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f"Error saat membaca file Excel: {str(e)}")

    def _import_account_mapping(self, decoded_file):
        """
        Method untuk memproses upload dan import data Excel ke pemetaan akun (Template Laporan)
        Format: Kode_BSPL, FSLI, Kategori, Sub_Kategori, No_Urut, Kode_Entity
        """
        self.ensure_one()

        import xlrd
        workbook = xlrd.open_workbook(file_contents=decoded_file)
        worksheet = workbook.sheet_by_index(0)

        # Baca header dari baris pertama
        headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

        # Validasi header (Support both exact match and likely matches)
        required_mapping = {
            'Kode_BSPL': ['Kode_BSPL', 'Kode BSPL', 'FSLI Code'],
            'FSLI': ['FSLI', 'Account Item'],
            'Kode_Entity': ['Kode_Entity', 'Kode Entity', 'Entity Code']
        }
        
        header_map = {}
        for key, possible_names in required_mapping.items():
            found = False
            for name in possible_names:
                if name in headers:
                    header_map[key] = headers.index(name)
                    found = True
                    break
            if not found:
                raise ValidationError(f'Header untuk "{key}" tidak ditemukan. Pastikan file sesuai format Template Laporan.')

        # Optional headers
        optional_mapping = {
            'Kategori': ['Kategori', 'Category'],
            'Sub_Kategori': ['Sub_Kategori', 'Sub Kategori', 'Sub Category'],
            'No_Urut': ['No_Urut', 'No Urut', 'Sequence']
        }
        for key, possible_names in optional_mapping.items():
            for name in possible_names:
                if name in headers:
                    header_map[key] = headers.index(name)
                    break

        created_records = 0
        updated_records = 0
        error_messages = []

        for row_idx in range(1, worksheet.nrows):
            try:
                # Ambil data berdasarkan map header
                bspl_code = str(worksheet.cell_value(row_idx, header_map['Kode_BSPL'])).strip()
                fsli_name = str(worksheet.cell_value(row_idx, header_map['FSLI'])).strip()
                entity_code = str(worksheet.cell_value(row_idx, header_map['Kode_Entity'])).split('.')[0].strip() # Clean numeric codes

                if not bspl_code or bspl_code == '0.0': continue

                # Siapkan data untuk pembuatan record
                mapping_data = {
                    'fsl_item': bspl_code,
                    'fsl_description': fsli_name,
                    'entity_code': entity_code,
                    'materiality_id': self.materiality_id.id,
                    'gl_account': 'PENDING', # Placeholder until GL is imported
                    'kategori': str(worksheet.cell_value(row_idx, header_map.get('Kategori'))) if 'Kategori' in header_map else '',
                    'sub_kategori': str(worksheet.cell_value(row_idx, header_map.get('Sub_Kategori'))) if 'Sub_Kategori' in header_map else '',
                    'sequence': int(worksheet.cell_value(row_idx, header_map.get('No_Urut'))) if 'No_Urut' in header_map else 10,
                }

                # Cek apakah sudah ada record dengan FSLI & Entity yang sama di materiality ini
                existing_record = self.env['icofr.account.mapping'].search([
                    ('fsl_item', '=', bspl_code),
                    ('entity_code', '=', entity_code),
                    ('materiality_id', '=', self.materiality_id.id)
                ], limit=1)

                if existing_record:
                    existing_record.write(mapping_data)
                    updated_records += 1
                else:
                    self.env['icofr.account.mapping'].create(mapping_data)
                    created_records += 1

            except Exception as e:
                error_messages.append(f'Baris {row_idx + 1}: {str(e)}')

        result_message = f"Import Template Laporan selesai:\n"
        result_message += f"- Record baru: {created_records}\n"
        result_message += f"- Record diperbarui: {updated_records}\n"
        if error_messages:
            result_message += "Daftar error:\n" + "\n".join(error_messages[:10])

        self.write({'import_result': result_message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hasil Import Template',
            'res_model': 'icofr.account.mapping.upload.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def _import_financial_data(self, decoded_file):
        """
        Method untuk memproses upload dan import data Excel ke data keuangan materiality
        """
        self.ensure_one()

        import xlrd
        workbook = xlrd.open_workbook(file_contents=decoded_file)
        worksheet = workbook.sheet_by_index(0)

        # Baca header dari baris pertama
        headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

        # Validasi header
        required_headers = ['Tahun Fiskal', 'Pendapatan', 'Total Aset']
        for header in required_headers:
            if header not in headers:
                raise ValidationError(f'Header "{header}" tidak ditemukan dalam file Excel. '
                                      f'Header yang diperlukan: {", ".join(required_headers)}')

        # Jika materiality_id tidak diisi dan ini untuk data keuangan, tidak apa-apa
        # karena kita akan mengupdate record yang sedang aktif saat ini
        materiality_record = self.materiality_id
        if not materiality_record:
            # Jika dipanggil dari context selain materiality, mungkin dari menu
            # Tapi dalam kasus ini, kita asumsikan materiality_id diisi
            raise ValidationError("Silakan pilih perhitungan materialitas yang akan diupdate.")

        # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
        updated_records = 0
        error_messages = []

        # Hanya proses baris pertama setelah header
        for row_idx in range(1, min(worksheet.nrows, 2)):  # Batasi hanya 1 baris data
            try:
                row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]

                # Konversi ke dictionary
                row_dict = dict(zip(headers, row_data))

                # Ambil data dari Excel
                fiscal_year = str(int(row_dict.get('Tahun Fiskal', ''))).strip()
                revenue = float(row_dict.get('Pendapatan', 0))
                total_assets = float(row_dict.get('Total Aset', 0))
                net_income = float(row_dict.get('Laba Bersih', 0)) if row_dict.get('Laba Bersih') else 0.0

                # Ambil parameter tambahan jika tersedia
                om_percent = float(row_dict.get('Persentase Overall Materiality', 0.5)) if row_dict.get('Persentase Overall Materiality') else 0.5
                pm_percent = float(row_dict.get('Persentase Performance Materiality', 75)) if row_dict.get('Persentase Performance Materiality') else 75
                materiality_basis = str(row_dict.get('Basis Perhitungan', 'revenue')).strip() if row_dict.get('Basis Perhitungan') else 'revenue'

                # Validasi data
                if not fiscal_year or len(fiscal_year) != 4 or not fiscal_year.isdigit():
                    raise ValidationError(f'Format Tahun Fiskal tidak valid di baris {row_idx + 1}. Harus format YYYY.')

                # Update data pada record materiality
                update_data = {
                    'fiscal_year': fiscal_year,
                    'revenue_amount': revenue,
                    'total_assets_amount': total_assets,
                    'net_income_amount': net_income,
                    'overall_materiality_percent': om_percent,
                    'performance_materiality_percent': pm_percent,
                    'materiality_basis': materiality_basis,
                }

                materiality_record.write(update_data)

                # Recalculate materiality amounts
                materiality_record._compute_materiality_amounts()

                updated_records += 1

            except Exception as e:
                error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data - {str(e)}')

        # Buat pesan hasil import
        result_message = f"Import data keuangan selesai:\n"
        result_message += f"- Jumlah record diperbarui: {updated_records}\n"

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
            'name': 'Hasil Import Excel Data Keuangan',
            'res_model': 'icofr.account.mapping.upload.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context
        }

        return action

    def action_download_template(self):
        """
        Method untuk mengunduh template Excel untuk upload
        """
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel template
        # Untuk sekarang, kita hanya menampilkan notifikasi yang sesuai dengan tipe import
        if self.import_type == 'account_mapping':
            message = 'Template Excel pemetaan akun tersedia di direktori data modul ICORF (file: account_mapping_template.txt)'
        else:
            message = 'Template Excel data keuangan tersedia di direktori data modul ICORF (file: financial_data_template.txt)'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Template Excel',
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }