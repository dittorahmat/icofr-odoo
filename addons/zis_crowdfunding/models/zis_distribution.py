from odoo import models, fields

class ZISDistribution(models.Model):
    _name = 'zis.distribution'
    _description = 'ZIS Distribution'

    name = fields.Char(string='Nama Penyaluran', required=True)
    distribution_type = fields.Selection([
        ('zakat', 'Zakat'),
        ('infaq', 'Infaq'),
        ('shodaqoh', 'Shodaqoh')
    ], string='Jenis ZIS', required=True)
    amount = fields.Float(string='Nominal')
    recipient = fields.Char(string='Penerima')
    distribution_date = fields.Date(string='Tanggal Penyaluran')
    campaign_id = fields.Many2one('zis.campaign', string='Kampanye Terkait')
    category_id = fields.Many2one('zis.category', string='Kategori Mustahiq')
    notes = fields.Text(string='Catatan')