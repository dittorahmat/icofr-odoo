# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrExportWizard(models.TransientModel):
    """
    Wizard untuk ekspor data ICORF
    """
    _name = 'icofr.export.wizard'
    _description = 'Wizard Ekspor Data ICORF'

    export_format = fields.Selection([
        ('csv', 'CSV'),
        ('xlsx', 'Excel (XLSX)'),
        ('pdf', 'PDF')
    ], string='Format Ekspor', default='xlsx',
       required=True,
       help='Format file untuk ekspor data')

    export_type = fields.Selection([
        ('control', 'Kontrol'),
        ('risk', 'Risiko'),
        ('testing', 'Pengujian'),
        ('certification', 'Sertifikasi'),
        ('finding', 'Temuan'),
        ('pojk_report', 'Laporan POJK'),
        ('all', 'Semua Data')
    ], string='Jenis Ekspor', required=True,
       help='Jenis data yang akan diekspor')

    date_from = fields.Date(
        string='Tanggal Dari',
        help='Filter data dari tanggal tertentu'
    )

    date_to = fields.Date(
        string='Tanggal Sampai',
        help='Filter data sampai tanggal tertentu'
    )

    include_attachments = fields.Boolean(
        string='Sertakan Lampiran',
        default=False,
        help='Sertakan file lampiran dalam ekspor (jika tersedia)'
    )

    include_inactive = fields.Boolean(
        string='Sertakan Data Tidak Aktif',
        default=False,
        help='Sertakan data dengan status tidak aktif dalam ekspor'
    )

    def action_export(self):
        """Eksekusi proses ekspor data"""
        self.ensure_one()

        # Di sini akan diimplementasikan logika ekspor data berdasarkan parameter
        # Dalam implementasi sebenarnya, ini akan menghasilkan file sesuai format
        # dan mengembalikan action untuk mendownload file

        # Untuk sekarang, kita hanya kembalikan pesan bahwa ekspor sedang berlangsung
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Ekspor Data',
                'message': f'Ekspor data {self.export_type} dalam format {self.export_format} sedang diproses...',
                'type': 'info',
                'sticky': False
            }
        }