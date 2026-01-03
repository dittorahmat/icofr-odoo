# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCSACampaign(models.Model):
    """
    Model untuk mengelola kampanye CSA (Control Self-Assessment)
    untuk manajemen periode CSA dan distribusi tugas ke Lini 1
    """
    _name = 'icofr.csa.campaign'
    _description = 'Kampanye Control Self-Assessment'
    _order = 'fiscal_year desc, period_start_date'

    name = fields.Char(
        string='Nama Kampanye CSA',
        required=True,
        help='Nama deskriptif dari kampanye CSA (misalnya: "CSA Q1 2024")'
    )

    campaign_code = fields.Char(
        string='Kode Kampanye',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi kampanye CSA'
    )

    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk kampanye CSA ini'
    )

    period_start_date = fields.Date(
        string='Tanggal Mulai Periode',
        required=True,
        help='Tanggal mulai periode CSA'
    )

    period_end_date = fields.Date(
        string='Tanggal Akhir Periode',
        required=True,
        help='Tanggal akhir periode CSA'
    )

    description = fields.Text(
        string='Deskripsi',
        help='Deskripsi rinci tentang kampanye CSA ini'
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Berlangsung'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan')
    ], string='Status', default='draft',
       help='Status dari kampanye CSA')

    # Relasi ke Lini 2 (pembuat kampanye)
    creator_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat kampanye CSA ini (biasanya Lini 2)'
    )

    # Relasi ke proses bisnis yang menjadi scope CSA
    process_ids = fields.Many2many(
        'icofr.process',
        'icofr_csa_campaign_process_rel',
        'campaign_id', 'process_id',
        string='Proses Bisnis',
        help='Proses bisnis yang menjadi scope dari kampanye CSA ini'
    )

    # Relasi ke kontrol-kontrol yang akan dinilai
    control_ids = fields.Many2many(
        'icofr.control',
        'icofr_csa_campaign_control_rel',
        'campaign_id', 'control_id',
        string='Kontrol untuk Dinilai',
        help='Kontrol-kontrol yang akan dinilai dalam kampanye CSA ini'
    )

    # Relasi ke CSA yang dihasilkan dari kampanye ini
    csa_ids = fields.One2many(
        'icofr.csa',
        'campaign_id',
        string='CSA yang Dihasilkan',
        help='CSA yang dihasilkan dari kampanye ini'
    )

    # Jumlah CSA yang perlu diselesaikan
    total_csa_count = fields.Integer(
        string='Jumlah CSA Total',
        compute='_compute_csa_counts',
        store=True,
        help='Jumlah total CSA yang harus diselesaikan dalam kampanye ini'
    )

    completed_csa_count = fields.Integer(
        string='Jumlah CSA Selesai',
        compute='_compute_csa_counts',
        store=True,
        help='Jumlah CSA yang sudah selesai'
    )

    pending_csa_count = fields.Integer(
        string='Jumlah CSA Menunggu',
        compute='_compute_csa_counts',
        store=True,
        help='Jumlah CSA yang masih menunggu penyelesaian'
    )

    completion_percentage = fields.Float(
        string='Persentase Penyelesaian',
        compute='_compute_completion_percentage',
        store=True,
        help='Persentase penyelesaian CSA dalam kampanye ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang terkait dengan kampanye CSA ini'
    )

    @api.depends('process_ids', 'control_ids')
    def _compute_csa_counts(self):
        """Menghitung jumlah CSA berdasarkan proses dan kontrol"""
        for campaign in self:
            # Hitung jumlah CSA yang terkait dengan kampanye ini
            csas = self.env['icofr.csa'].search([
                ('campaign_id', '=', campaign.id)
            ])
            
            campaign.total_csa_count = len(csas)
            campaign.completed_csa_count = len(csas.filtered(lambda c: c.status == 'completed'))
            campaign.pending_csa_count = campaign.total_csa_count - campaign.completed_csa_count

    @api.depends('total_csa_count', 'completed_csa_count')
    def _compute_completion_percentage(self):
        """Menghitung persentase penyelesaian CSA"""
        for campaign in self:
            if campaign.total_csa_count > 0:
                campaign.completion_percentage = (campaign.completed_csa_count / campaign.total_csa_count) * 100
            else:
                campaign.completion_percentage = 0

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()

                # Generate code if not provided
                if 'campaign_code' not in new_val_dict or not new_val_dict.get('campaign_code'):
                    new_val_dict['campaign_code'] = self.env['ir.sequence'].next_by_code('icofr.csa.campaign') or '/'

                # Generate a default name if not provided
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    fiscal_year = new_val_dict.get('fiscal_year', fields.Date.today().year)
                    period = f"{new_val_dict.get('period_start_date', '')} s/d {new_val_dict.get('period_end_date', '')}"
                    new_val_dict['name'] = f'CSA {fiscal_year} - {period}'

                processed_vals.append(new_val_dict)
            return super(IcofrCSACampaign, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()

            # Generate code if not provided
            if 'campaign_code' not in new_vals or not new_vals.get('campaign_code'):
                new_vals['campaign_code'] = self.env['ir.sequence'].next_by_code('icofr.csa.campaign') or '/'

            # Generate a default name if not provided
            if 'name' not in new_vals or not new_vals.get('name'):
                fiscal_year = new_vals.get('fiscal_year', fields.Date.today().year)
                period = f"{new_vals.get('period_start_date', '')} s/d {new_vals.get('period_end_date', '')}"
                new_vals['name'] = f'CSA {fiscal_year} - {period}'

            return super(IcofrCSACampaign, self).create(new_vals)

    def action_start_campaign(self):
        """Method untuk memulai kampanye CSA - mengganti status menjadi ongoing"""
        self.ensure_one()
        if self.status == 'draft':
            # Buat tugas CSA untuk setiap kontrol yang terkait
            self._create_csa_tasks()
            self.write({'status': 'ongoing'})
        return True

    def action_complete_campaign(self):
        """Method untuk menyelesaikan kampanye CSA"""
        self.ensure_one()
        if self.status == 'ongoing':
            self.write({'status': 'completed'})
        return True

    def action_cancel_campaign(self):
        """Method untuk membatalkan kampanye CSA"""
        self.ensure_one()
        self.write({'status': 'cancelled'})
        return True

    def action_reset_to_draft(self):
        """Method untuk mereset kampanye ke draft"""
        self.ensure_one()
        self.write({'status': 'draft'})
        return True

    def _create_csa_tasks(self):
        """
        Method untuk membuat tugas CSA berdasarkan kontrol dan proses dalam kampanye
        """
        csa_model = self.env['icofr.csa']
        
        # Untuk setiap kontrol dalam kampanye, buatkan tugas CSA
        for control in self.control_ids:
            # Jika kontrol terkait dengan proses tertentu dan proses tersebut ada di kampanye ini
            if control.process_id and control.process_id in self.process_ids:
                # Pastikan belum ada CSA untuk kontrol ini dalam kampanye ini
                existing_csa = csa_model.search([
                    ('control_id', '=', control.id),
                    ('campaign_id', '=', self.id)
                ])
                
                if not existing_csa:
                    # Buat CSA baru untuk kontrol ini
                    csa_vals = {
                        'name': f'CSA: {control.name} - {self.name}',
                        'control_id': control.id,
                        'control_owner_id': control.owner_id.id,  # Kirim ke pemilik kontrol (Lini 1)
                        'assessment_period': f'{self.fiscal_year} {self.name}',
                        'assessment_date': fields.Date.today(),
                        'due_date': self.period_end_date,  # Batas waktu sesuai periode kampanye
                        'campaign_id': self.id,
                        'company_id': self.company_id.id,
                    }
                    
                    # Cek apakah pemilik kontrol terdefinisi
                    if not control.owner_id:
                        # Jika tidak ada pemilik kontrol, kita tetap buat CSA tapi tanpa pemilik
                        csa_vals['control_owner_id'] = False
                        
                    csa_model.create(csa_vals)

    def action_send_notifications(self):
        """
        Method untuk mengirimkan notifikasi ke pemilik kontrol (Lini 1)
        untuk menyelesaikan CSA yang ditugaskan
        """
        for campaign in self:
            for csa in campaign.csa_ids:
                # Kirim notifikasi ke pemilik kontrol jika belum selesai
                if csa.status in ['planned', 'in_progress']:
                    # Dalam implementasi sebenarnya, ini akan mengirim email atau notifikasi sistem
                    # Untuk sekarang, kita hanya mencatat dalam chatter
                    csa.message_post(
                        body=f"Anda memiliki tugas CSA yang harus diselesaikan dalam kampanye: {campaign.name}",
                        subtype_xmlid='mail.mt_comment',
                        partner_ids=[csa.control_owner_id.partner_id.id] if csa.control_owner_id else []
                    )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Notifikasi Dikirim',
                'message': f'Notifikasi telah dikirim ke pemilik kontrol untuk menyelesaikan CSA dalam kampanye {self.name}',
                'type': 'success',
            }
        }

    def action_view_csas(self):
        """Method untuk melihat CSA yang terkait dengan kampanye ini"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'CSA dalam Kampanye Ini',
            'res_model': 'icofr.csa',
            'domain': [('campaign_id', '=', self.id)],
            'view_mode': 'list,form',
            'context': {'default_campaign_id': self.id}
        }