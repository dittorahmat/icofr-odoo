# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
from io import BytesIO


class IcofrMasterDataUploadWizard(models.TransientModel):
    """
    Wizard untuk upload Excel data master (lokasi dan proses bisnis) ke sistem ICORF
    """
    _name = 'icofr.master.data.upload.wizard'
    _description = 'Wizard Upload Data Master (Lokasi dan Proses Bisnis)'

    excel_file = fields.Binary(
        string='File Excel',
        required=True,
        help='File Excel yang berisi data master (lokasi dan proses bisnis)'
    )

    file_name = fields.Char(
        string='Nama File',
        help='Nama file Excel yang diupload'
    )

    import_type = fields.Selection([
        ('location', 'Lokasi'),
        ('business_process', 'Proses Bisnis'),
        ('both', 'Keduanya')
    ], string='Jenis Import', default='both',
       help='Pilih jenis data master yang akan diimport dari Excel')

    import_result = fields.Text(
        string='Hasil Import',
        readonly=True,
        help='Detail hasil import data dari Excel'
    )

    @api.model
    def default_get(self, fields):
        res = super(IcofrMasterDataUploadWizard, self).default_get(fields)
        active_model = self.env.context.get('active_model')

        # Jika wizard dipanggil dari halaman tertentu, kita bisa mengatur nilai default
        if active_model == 'icofr.process':
            res['import_type'] = 'business_process'
        elif active_model == 'res.partner':
            res['import_type'] = 'location'

        return res

    def action_upload_excel(self):
        """
        Method untuk memproses upload dan import data Excel ke master data (lokasi dan proses bisnis)
        """
        self.ensure_one()

        if not self.excel_file:
            raise ValidationError("Silakan pilih file Excel terlebih dahulu.")

        if not self.file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(self.excel_file)

            if self.import_type in ['location', 'both']:
                self._import_locations(decoded_file)
            if self.import_type in ['business_process', 'both']:
                self._import_business_processes(decoded_file)

            # Return action untuk menampilkan hasil
            action = {
                'type': 'ir.actions.act_window',
                'name': 'Hasil Import Data Master',
                'res_model': 'icofr.master.data.upload.wizard',
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

    def _import_locations(self, decoded_file):
        """
        Method untuk memproses upload dan import data Excel ke lokasi
        """
        import xlrd
        workbook = xlrd.open_workbook(file_contents=decoded_file)
        
        # Cari sheet untuk lokasi (biasanya sheet pertama atau dengan nama tertentu)
        worksheet = None
        for sheet in workbook.sheets():
            if 'lokasi' in sheet.name.lower() or 'location' in sheet.name.lower():
                worksheet = sheet
                break
        
        # Jika tidak ditemukan sheet khusus, gunakan sheet pertama
        if not worksheet:
            worksheet = workbook.sheet_by_index(0)

        # Baca header dari baris pertama
        headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

        # Validasi header untuk lokasi, jika ini adalah sheet lokasi
        location_headers = ['Kode Lokasi', 'Nama Lokasi', 'Alamat', 'Kota', 'Provinsi']
        is_location_sheet = all(header in headers for header in ['Kode Lokasi', 'Nama Lokasi'])

        if not is_location_sheet:
            # Jika tidak semua header lokasi, mungkin ini bukan sheet yang tepat
            # Tapi kita tetap akan mencoba mengimport data lokasi jika import_type mengizinkan
            pass

        # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
        created_locations = []
        updated_locations = []
        error_messages = []

        for row_idx in range(1, worksheet.nrows):
            try:
                row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]
                
                # Konversi ke dictionary
                row_dict = dict(zip(headers, row_data))

                # Periksa apakah ini adalah data lokasi
                location_code = str(row_dict.get('Kode Lokasi', '')).strip()
                location_name = str(row_dict.get('Nama Lokasi', '')).strip()

                if not location_code and not location_name:
                    # Baris kosong, lanjut ke baris berikutnya
                    continue

                if location_code:
                    # Siapkan data untuk pembuatan lokasi
                    location_data = {
                        'name': location_name or location_code,  # Gunakan kode jika nama tidak ada
                        'ref': location_code,
                        'street': str(row_dict.get('Alamat', '')).strip(),
                        'city': str(row_dict.get('Kota', '')).strip(),
                        'state_id': self._get_state_id(str(row_dict.get('Provinsi', '')).strip()),
                    }

                    # Cek apakah lokasi dengan kode tersebut sudah ada
                    existing_location = self.env['res.partner'].search([
                        ('ref', '=', location_code),
                        ('is_company', '=', False)  # Lokasi biasanya adalah contact bukan company
                    ], limit=1)

                    if existing_location:
                        # Update lokasi yang sudah ada
                        existing_location.write(location_data)
                        updated_locations.append(existing_location.name)
                    else:
                        # Buat lokasi baru - dalam hal ini sebagai contact partner
                        location_data['is_company'] = False
                        location_data['type'] = 'delivery'  # Type for location
                        new_location = self.env['res.partner'].create(location_data)
                        created_locations.append(new_location.name)

            except Exception as e:
                error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data lokasi - {str(e)}')

        # Buat pesan hasil import
        result_message = f"Import data lokasi selesai:\n"
        result_message += f"- Jumlah lokasi baru: {len(created_locations)}\n"
        result_message += f"- Jumlah lokasi diperbarui: {len(updated_locations)}\n"

        if error_messages:
            result_message += f"- Jumlah error: {len(error_messages)}\n"
            result_message += "Daftar error:\n" + "\n".join(f"  - {err}" for err in error_messages)
        else:
            result_message += "Tidak ada error ditemukan."

        # Update hasil import
        self.import_result = result_message

    def _import_business_processes(self, decoded_file):
        """
        Method untuk memproses upload dan import data Excel ke proses bisnis
        """
        import xlrd
        workbook = xlrd.open_workbook(file_contents=decoded_file)
        
        # Cari sheet untuk proses bisnis (biasanya sheet khusus atau sheet pertama)
        worksheet = None
        for sheet in workbook.sheets():
            if 'proses' in sheet.name.lower() or 'process' in sheet.name.lower():
                worksheet = sheet
                break
        
        # Jika tidak ditemukan sheet khusus, gunakan sheet pertama
        if not worksheet:
            worksheet = workbook.sheet_by_index(0)

        # Baca header dari baris pertama
        headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

        # Validasi header untuk proses bisnis
        process_headers = ['Kode Proses', 'Nama Proses', 'Deskripsi Proses', 'Pemilik Proses']
        is_process_sheet = all(header in headers for header in ['Kode Proses', 'Nama Proses'])

        if not is_process_sheet:
            # Jika tidak semua header proses, mungkin ini bukan sheet yang tepat
            # Tapi kita tetap akan mencoba mengimport data proses jika import_type mengizinkan
            pass

        # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
        created_processes = []
        updated_processes = []
        error_messages = []

        for row_idx in range(1, worksheet.nrows):
            try:
                row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]
                
                # Konversi ke dictionary
                row_dict = dict(zip(headers, row_data))

                # Periksa apakah ini adalah data proses bisnis
                process_code = str(row_dict.get('Kode Proses', '')).strip()
                process_name = str(row_dict.get('Nama Proses', '')).strip()

                if not process_code and not process_name:
                    # Baris kosong, lanjut ke baris berikutnya
                    continue

                if process_code:
                    # Cari user yang menjadi pemilik proses berdasarkan nama
                    owner_name = str(row_dict.get('Pemilik Proses', '')).strip()
                    owner_id = False
                    if owner_name:
                        user = self.env['res.users'].search([('name', 'ilike', owner_name)], limit=1)
                        owner_id = user.id if user else False

                    # Siapkan data untuk pembuatan proses bisnis
                    process_data = {
                        'name': process_name or process_code,  # Gunakan kode jika nama tidak ada
                        'code': process_code,
                        'description': str(row_dict.get('Deskripsi Proses', '')).strip(),
                        'owner_id': owner_id,
                    }

                    # Cek apakah proses dengan kode tersebut sudah ada
                    existing_process = self.env['icofr.process'].search([
                        ('code', '=', process_code)
                    ], limit=1)

                    if existing_process:
                        # Update proses yang sudah ada
                        existing_process.write(process_data)
                        updated_processes.append(existing_process.name)
                    else:
                        # Buat proses baru
                        new_process = self.env['icofr.process'].create(process_data)
                        created_processes.append(new_process.name)

            except Exception as e:
                error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data proses - {str(e)}')

        # Tambahkan informasi proses ke pesan hasil import
        if created_processes or updated_processes or error_messages:
            if self.import_result:
                self.import_result += "\n\n"
            
            result_message = f"Import data proses bisnis selesai:\n"
            result_message += f"- Jumlah proses baru: {len(created_processes)}\n"
            result_message += f"- Jumlah proses diperbarui: {len(updated_processes)}\n"

            if error_messages:
                result_message += f"- Jumlah error: {len(error_messages)}\n"
                result_message += "Daftar error:\n" + "\n".join(f"  - {err}" for err in error_messages)
            else:
                result_message += "Tidak ada error ditemukan."

            # Update atau tambahkan hasil import
            if self.import_result:
                self.import_result += result_message
            else:
                self.import_result = result_message

    def _get_state_id(self, state_name):
        """
        Helper method untuk mendapatkan ID provinsi berdasarkan nama
        """
        if not state_name:
            return False
        
        # Cari provinsi berdasarkan nama
        state = self.env['res.country.state'].search([
            ('name', 'ilike', state_name)
        ], limit=1)
        
        return state.id if state else False

    def action_download_template(self):
        """
        Method untuk mengunduh template Excel untuk upload master data
        """
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel template
        # Untuk sekarang, kita hanya menampilkan notifikasi
        message = (
            'Template Excel tersedia di direktori data modul ICORF.\n'
            'Untuk data lokasi, kolom wajib: Kode Lokasi, Nama Lokasi\n'
            'Untuk data proses, kolom wajib: Kode Proses, Nama Proses'
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Template Excel Data Master',
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }