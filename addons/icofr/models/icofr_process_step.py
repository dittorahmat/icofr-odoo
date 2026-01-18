# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrProcessStep(models.Model):
    _name = 'icofr.process.step'
    _description = 'Langkah Proses Bisnis (BPM)'
    _order = 'process_id, sequence'

    name = fields.Char(string='Nama Langkah/Aktivitas', required=True)
    sequence = fields.Integer(string='Urutan', default=10)
    process_id = fields.Many2one('icofr.process', string='Proses Bisnis', ondelete='cascade', required=True)
    
    # Lampiran 3: Legenda Simbol
    step_type = fields.Selection([
        ('start_end', 'Awal/Akhir Proses (Oval)'),
        ('manual', 'Aktivitas Manual Tanpa Sistem (Kotak)'),
        ('manual_it', 'Aktivitas Pelaku dalam Sistem (Kotak dengan Nama Sistem)'),
        ('automated', 'Aktivitas Otomatis Sistem (Kotak Berbayang dengan Nama Sistem)'),
        ('interface', 'Interface / Media Perpindahan Data (Tabung)'),
        ('output', 'Output dari Sistem (Jajaran Genjang)'),
        ('decision', 'Cabang/Keputusan (Belah Ketupat)'),
        ('third_party', 'Aktivitas Pihak Ketiga (Kotak Abu-abu)'),
        ('document', 'Data Fisik / Dokumen (Kertas)'),
        ('reference_on', 'Sambungan Halaman Sama (Lingkaran)'),
        ('reference_off', 'Sambungan Halaman Berbeda (Pentagon)'),
        ('risk', 'Titik Risiko (Heksagon Merah)'),
        ('control', 'Titik Pengendalian (Lingkaran Hijau)'),
        ('note', 'Informasi Tambahan / Note'),
        ('archive', 'Arsip (Segitiga Terbalik)')
    ], string='Tipe Langkah/Simbol', default='manual_it', required=True)

    symbol_image = fields.Binary(string='Ikon Simbol', help='Visualisasi simbol sesuai Lampiran 3')


    actor_role = fields.Char(string='Peran/Pelaku', help='Fungsi atau jabatan yang melakukan aktivitas ini.')
    
    application_id = fields.Many2one('icofr.application', string='Sistem/Aplikasi', help='Sistem yang digunakan dalam langkah ini.')
    
    # Integrasi Risiko & Kontrol pada Titik Proses (Lampiran 4)
    risk_ids = fields.Many2many('icofr.risk', string='Risiko di Langkah Ini')
    control_ids = fields.Many2many('icofr.control', string='Kontrol di Langkah Ini')
    
    description = fields.Text(string='Deskripsi Langkah')
    
    company_id = fields.Many2one('res.company', string='Perusahaan', 
                                default=lambda self: self.env.company)
