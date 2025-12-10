from odoo import models, fields

class ZISDonation(models.Model):
    _name = 'zis.donation'
    _description = 'ZIS Donation'

    campaign_id = fields.Many2one('zis.campaign', string='Kampanye ZIS', ondelete='cascade')
    donator_name = fields.Char(string='Nama Donatur')
    amount = fields.Float(string='Nominal')
    donation_type = fields.Selection([
        ('zakat', 'Zakat'),
        ('infaq', 'Infaq'),
        ('shodaqoh', 'Shodaqoh')
    ], string='Jenis ZIS')