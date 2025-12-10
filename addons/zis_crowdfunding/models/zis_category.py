from odoo import models, fields

class ZISCategory(models.Model):
    _name = 'zis.category'
    _description = 'Kategori ZIS'

    name = fields.Char(string='Nama Kategori', required=True)
    description = fields.Text(string='Deskripsi')
    is_zakat_category = fields.Boolean(string='Kategori untuk Zakat')
    is_active = fields.Boolean(string='Aktif', default=True)