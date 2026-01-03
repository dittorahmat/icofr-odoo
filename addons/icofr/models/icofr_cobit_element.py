# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCobitElement(models.Model):
    _name = 'icofr.cobit.element'
    _description = 'Elemen Kerangka COBIT 2019'
    _order = 'code'

    name = fields.Char(
        string='Nama Elemen COBIT',
        required=True,
        help='Nama dari elemen dalam kerangka COBIT 2019'
    )

    code = fields.Char(
        string='Kode Elemen COBIT',
        required=True,
        copy=False,
        help='Kode singkat untuk identifikasi elemen COBIT'
    )

    description = fields.Text(
        string='Deskripsi Elemen',
        help='Deskripsi lengkap dari elemen COBIT 2019'
    )

    domain = fields.Char(
        string='Domain',
        help='Domain COBIT di mana elemen ini berada (A, B, C, D)'
    )

    process_group = fields.Char(
        string='Grup Proses',
        help='Grup proses COBIT (misalnya: Evaluate, Direct and Monitor)'
    )

    parent_id = fields.Many2one(
        'icofr.cobit.element',
        string='Sub-Elemen dari',
        help='Jika ini adalah sub-elemen dari elemen lain'
    )

    child_ids = fields.One2many(
        'icofr.cobit.element',
        'parent_id',
        string='Sub-Elemen',
        help='Sub-elemen dari elemen ini'
    )

    control_ids = fields.Many2many(
        'icofr.control',
        'icofr_control_cobit_rel',
        'cobit_element_id', 'control_id',
        string='Kontrol Terkait',
        help='Kontrol-kontrol yang terkait dengan elemen COBIT ini'
    )

    is_itgc = fields.Boolean(
        string='Kontrol ITGC?',
        help='Menandakan apakah ini adalah kontrol ITGC (Information Technology General Control)'
    )

    it_risk_area = fields.Selection([
        ('access_management', 'Manajemen Akses'),
        ('change_management', 'Manajemen Perubahan'),
        ('data_governance', 'Tata Kelola Data'),
        ('it_operations', 'Operasi IT'),
        ('security_management', 'Manajemen Keamanan'),
        ('incident_management', 'Manajemen Insiden'),
        ('capacity_management', 'Manajemen Kapasitas'),
        ('continuity_management', 'Manajemen Continuity')
    ], string='Area Risiko IT',
       help='Area risiko IT yang ditangani oleh elemen ini')

    it_asset_type = fields.Selection([
        ('application', 'Aplikasi'),
        ('database', 'Database'),
        ('network', 'Jaringan'),
        ('server', 'Server'),
        ('end_user_device', 'Perangkat Pengguna Akhir'),
        ('cloud_service', 'Layanan Cloud'),
        ('data', 'Data')
    ], string='Tipe Aset IT',
       help='Tipe aset IT yang dikaitkan dengan elemen COBIT ini')

    maturity_level = fields.Selection([
        ('0', 'Tidak Tersedia'),
        ('1', 'Awal'),
        ('2', 'Manajerial'),
        ('3', 'Ditetapkan'),
        ('4', 'Dikelola'),
        ('5', 'Optimal')
    ], string='Tingkat Kematangan', default='1',
       help='Tingkat kematangan implementasi elemen COBIT ini')

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait elemen COBIT ini'
    )

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'code' not in new_val_dict or not new_val_dict.get('code'):
                    new_val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.cobit.element') or '/'
                processed_vals.append(new_val_dict)
            return super(IcofrCobitElement, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'code' not in new_vals or not new_vals.get('code'):
                new_vals['code'] = self.env['ir.sequence'].next_by_code('icofr.cobit.element') or '/'
            return super(IcofrCobitElement, self).create(new_vals)