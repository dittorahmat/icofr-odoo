# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
from io import BytesIO


class IcofrPopulationUploadWizard(models.TransientModel):
    """
    Wizard untuk upload Excel data populasi transaksi untuk keperluan audit sampling
    """
    _name = 'icofr.population.upload.wizard'
    _description = 'Wizard Upload Data Populasi untuk Audit Sampling'

    excel_file = fields.Binary(
        string='File Excel Populasi',
        required=True,
        help='File Excel yang berisi data populasi transaksi untuk audit sampling'
    )

    file_name = fields.Char(
        string='Nama File',
        help='Nama file Excel populasi yang diupload'
    )

    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Terkait',
        help='Kontrol yang terkait dengan populasi data ini'
    )

    testing_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian Terkait',
        help='Pengujian yang akan menggunakan populasi ini'
    )

    process_owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Proses',
        help='Pemilik proses yang mengupload data populasi ini (Lini 1)'
    )

    upload_date = fields.Datetime(
        string='Tanggal Upload',
        default=fields.Datetime.now,
        help='Tanggal dan waktu data populasi diupload'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan tentang data populasi ini'
    )

    import_result = fields.Text(
        string='Hasil Import',
        readonly=True,
        help='Detail hasil import data populasi dari Excel'
    )

    def action_upload_population_excel(self):
        """
        Method untuk memproses upload dan import data Excel ke populasi untuk audit sampling
        """
        self.ensure_one()

        if not self.excel_file:
            raise ValidationError("Silakan pilih file Excel populasi terlebih dahulu.")

        if not self.file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(self.excel_file)

            workbook = xlrd.open_workbook(file_contents=decoded_file)
            
            # Gunakan sheet pertama
            worksheet = workbook.sheet_by_index(0)

            # Baca header dari baris pertama
            headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

            # Validasi header minimal yang harus ada
            required_headers = ['No Transaksi', 'Tanggal', 'Nilai', 'Deskripsi']
            missing_headers = [header for header in required_headers if header not in headers]
            
            if missing_headers:
                raise ValidationError(f'Header berikut tidak ditemukan dalam file Excel: {", ".join(missing_headers)}')

            # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
            created_population_items = []
            error_messages = []

            # Dapatkan model yang dibutuhkan
            population_model = self.env['icofr.audit.population']

            for row_idx in range(1, worksheet.nrows):
                try:
                    row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]
                    
                    # Konversi ke dictionary
                    row_dict = dict(zip(headers, row_data))

                    # Ambil data populasi dari Excel
                    transaction_no = str(row_dict.get('No Transaksi', '')).strip()
                    transaction_date = row_dict.get('Tanggal', '')
                    transaction_value = row_dict.get('Nilai', 0)
                    description = str(row_dict.get('Deskripsi', '')).strip()

                    # Validasi bahwa nomor transaksi ada
                    if not transaction_no:
                        error_messages.append(f'Baris {row_idx + 1}: Nomor Transaksi wajib diisi.')
                        continue

                    # Cek apakah tanggal valid
                    try:
                        if isinstance(transaction_date, float):
                            # Jika dalam format Excel date, konversi ke string
                            import datetime
                            base_date = datetime.date(1900, 1, 1)  # Excel base date
                            actual_date = base_date + datetime.timedelta(days=(transaction_date - 2))  # -2 adjustment for Excel bug
                            transaction_date_str = actual_date.strftime('%Y-%m-%d')
                        else:
                            transaction_date_str = str(transaction_date)[0:10]  # Ambil hanya YYYY-MM-DD
                    except:
                        transaction_date_str = fields.Date.today()

                    # Validasi atau konversi nilai transaksi
                    try:
                        transaction_amount = float(transaction_value)
                    except (ValueError, TypeError):
                        transaction_amount = 0.0

                    # Siapkan data untuk pembuatan item populasi
                    population_data = {
                        'transaction_no': transaction_no,
                        'transaction_date': transaction_date_str,
                        'amount': transaction_amount,
                        'description': description,
                        'control_id': self.control_id.id if self.control_id else None,
                        'testing_id': self.testing_id.id if self.testing_id else None,
                        'uploaded_by_id': self.process_owner_id.id if self.process_owner_id else self.env.user.id,
                        'upload_date': self.upload_date,
                        'notes': self.notes,
                    }

                    # Buat item populasi baru
                    new_item = population_model.create(population_data)
                    created_population_items.append(new_item.transaction_no)

                except Exception as e:
                    error_messages.append(f'Baris {row_idx + 1}: Error saat memproses data populasi - {str(e)}')

            # Buat pesan hasil import
            result_message = f"Import data populasi untuk audit sampling selesai:\n"
            result_message += f"- Jumlah item populasi baru: {len(created_population_items)}\n"

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
                'name': 'Hasil Import Data Populasi',
                'res_model': 'icofr.population.upload.wizard',
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
        Method untuk mengunduh template Excel untuk upload populasi
        """
        message = (
            'Template Excel untuk data populasi tersedia di direktori data modul ICORF.\n'
            'Kolom wajib: No Transaksi, Tanggal, Nilai, Deskripsi\n'
            'Kolom opsional: Pemilik Transaksi, Departemen, Keterangan Lain'
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Template Excel Data Populasi',
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }


class IcofrAuditPopulation(models.Model):
    """
    Model untuk menyimpan data populasi transaksi yang digunakan untuk audit sampling
    """
    _name = 'icofr.audit.population'
    _description = 'Populasi Data untuk Audit Sampling'
    _order = 'transaction_date desc, transaction_no'

    transaction_no = fields.Char(
        string='Nomor Transaksi',
        required=True,
        help='Nomor unik dari transaksi dalam populasi'
    )

    transaction_date = fields.Date(
        string='Tanggal Transaksi',
        required=True,
        help='Tanggal dari transaksi'
    )

    amount = fields.Float(
        string='Nilai',
        required=True,
        help='Nilai atau jumlah dari transaksi'
    )

    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi atau rincian dari transaksi'
    )

    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Terkait',
        help='Kontrol yang terkait dengan transaksi ini'
    )

    testing_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian Terkait',
        help='Pengujian yang menggunakan transaksi ini sebagai sampel'
    )

    uploaded_by_id = fields.Many2one(
        'res.users',
        string='Diupload Oleh',
        required=True,
        default=lambda self: self.env.user,
        help='Pengguna yang mengupload transaksi ini (biasanya Lini 1)'
    )

    upload_date = fields.Datetime(
        string='Tanggal Upload',
        default=fields.Datetime.now,
        help='Tanggal dan waktu transaksi diupload ke sistem'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan tentang transaksi ini'
    )

    selected_for_testing = fields.Boolean(
        string='Dipilih untuk Pengujian',
        default=False,
        help='Menandakan apakah transaksi ini dipilih sebagai sampel untuk pengujian'
    )

    testing_result = fields.Selection([
        ('pass', 'Lulus'),
        ('fail', 'Gagal'),
        ('not_applicable', 'Tidak Berlaku')
    ], string='Hasil Pengujian', 
       help='Hasil dari pengujian terhadap transaksi ini')

    testing_notes = fields.Text(
        string='Catatan Pengujian',
        help='Catatan dari auditor selama pengujian transaksi ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki transaksi ini'
    )

    def action_select_for_testing(self):
        """Method untuk memilih item untuk pengujian"""
        for record in self:
            record.selected_for_testing = True
        return True

    def action_deselect_for_testing(self):
        """Method untuk membatalkan pemilihan item untuk pengujian"""
        for record in self:
            record.selected_for_testing = False
        return True

    def action_open_sample_wizard(self):
        """Method untuk membuka wizard pemilihan sampel dari daftar populasi"""
        return {
            'name': 'Pilih Sampel untuk Pengujian',
            'type': 'ir.actions.act_window',
            'res_model': 'icofr.sample.selection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_population_ids': self.ids,
            }
        }


class IcofrSampleSelectionWizard(models.TransientModel):
    """
    Wizard untuk memilih sampel secara massal dari populasi dan menghubungkannya ke Pengujian (TOE)
    """
    _name = 'icofr.sample.selection.wizard'
    _description = 'Wizard Pemilihan Sampel Audit'

    testing_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian (TOE)',
        required=True,
        domain=[('test_type', '=', 'toe')],
        help='Pilih pengujian TOE yang akan dihubungkan dengan sampel ini'
    )

    population_ids = fields.Many2many(
        'icofr.audit.population',
        string='Item Populasi Terpilih',
        help='Item populasi yang dipilih untuk dijadikan sampel'
    )

    selection_mode = fields.Selection([
        ('manual', 'Pilihan Manual Saat Ini'),
        ('random', 'Acak dari Populasi'),
    ], string='Mode Pemilihan', default='manual')

    random_sample_count = fields.Integer(
        string='Jumlah Sampel Acak',
        help='Jumlah record yang akan dipilih secara acak jika menggunakan mode Acak'
    )

    def action_confirm_selection(self):
        """Hubungkan item populasi terpilih ke record pengujian"""
        self.ensure_one()
        
        selected_items = self.population_ids
        
        if self.selection_mode == 'random' and self.random_sample_count > 0:
            # Simple random selection from the linked population (or all available if none selected)
            all_available = self.env['icofr.audit.population'].search([
                ('control_id', '=', self.testing_id.control_id.id),
                ('testing_id', '=', False)
            ])
            import random
            if len(all_available) > self.random_sample_count:
                selected_items = self.env['icofr.audit.population'].browse(
                    random.sample(all_available.ids, self.random_sample_count)
                )
            else:
                selected_items = all_available

        if not selected_items:
            from odoo.exceptions import UserError
            raise UserError('Tidak ada item populasi yang dipilih.')

        # Link to testing and mark as selected
        selected_items.write({
            'testing_id': self.testing_id.id,
            'selected_for_testing': True
        })

        # Update population size in testing if empty
        if not self.testing_id.population_size:
            total_pop = self.env['icofr.audit.population'].search_count([
                ('control_id', '=', self.testing_id.control_id.id)
            ])
            self.testing_id.write({'population_size': total_pop})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sampel Dihubungkan',
                'message': f'{len(selected_items)} item populasi telah dihubungkan ke {self.testing_id.name}.',
                'type': 'success',
            }
        }