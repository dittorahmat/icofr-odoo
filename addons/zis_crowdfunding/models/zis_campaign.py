from odoo import models, fields, api

class ZISCampaign(models.Model):
    _name = 'zis.campaign'
    _description = 'ZIS Campaign'

    name = fields.Char(string='Nama Kampanye', required=True)
    zis_type = fields.Selection([
        ('zakat', 'Zakat'),
        ('infaq', 'Infaq'),
        ('shodaqoh', 'Shodaqoh')
    ], string='Jenis ZIS', required=True)
    
    target_amount = fields.Float(string='Target Dana', required=True)
    collected_amount = fields.Float(string='Terkumpul', compute='_compute_collected')
    category_id = fields.Many2one('zis.category', string='Kategori Mustahiq')
    
    # One2many field to link donations to this campaign
    zis_donation_ids = fields.One2many(
        'zis.donation', 'campaign_id', string='Donasi ZIS'
    )
    
    description = fields.Text(string='Deskripsi')  # Mengganti Html ke Text untuk sementara
    start_date = fields.Date(string='Tanggal Mulai')
    end_date = fields.Date(string='Tanggal Berakhir')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Dibuka'),
        ('close', 'Ditutup'),
        ('cancel', 'Dibatalkan')
    ], string='Status', default='draft')
    
    # Image field for campaign
    image = fields.Binary(string='Gambar Kampanye', attachment=True, 
                         help='Unggah gambar untuk kampanye ini')
    image_filename = fields.Char(string='Nama File Gambar')

    @api.depends('zis_donation_ids.amount')
    def _compute_collected(self):
        for campaign in self:
            campaign.collected_amount = sum(donation.amount for donation in campaign.zis_donation_ids)