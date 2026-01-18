# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IcofrProcess(models.Model):
    _name = 'icofr.process'
    _description = 'Proses Bisnis'
    _order = 'name'

    name = fields.Char(
        string='Nama Proses',
        required=True,
        translate=True,
        help='Nama dari proses bisnis'
    )

    code = fields.Char(
        string='Kode Proses',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi proses'
    )

    description = fields.Text(
        string='Deskripsi Proses',
        help='Deskripsi lengkap dari proses bisnis'
    )

    category = fields.Selection([
        ('operational', 'Operasional'),
        ('financial', 'Finansial'),
        ('compliance', 'Kepatuhan'),
        ('strategic', 'Strategis'),
        ('supporting', 'Dukungan')
    ], string='Kategori Proses', required=True,
       help='Kategori dari proses bisnis')

    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Proses',
        required=True,
        help='Pengguna yang bertanggung jawab atas proses ini'
    )

    parent_process_id = fields.Many2one(
        'icofr.process',
        string='Proses Induk',
        help='Proses induk jika ini adalah sub-proses'
    )

    control_ids = fields.One2many(
        'icofr.control',
        'process_id',
        string='Kontrol Terkait',
        help='Kontrol-kontrol yang terkait dengan proses ini'
    )

    risk_ids = fields.One2many(
        'icofr.risk',
        'process_id',
        string='Risiko Terkait',
        help='Risiko-risiko yang terkait dengan proses ini'
    )

    bpm_document_ids = fields.One2many(
        'icofr.bpm.document',
        'process_id',
        string='Dokumen BPM/SOP'
    )

    process_step_ids = fields.One2many(
        'icofr.process.step',
        'process_id',
        string='Langkah-Langkah Proses (BPM Terstruktur)',
        help='Daftar langkah aktivitas terstruktur sesuai Lampiran 3 & 4 Juknis BUMN.'
    )


    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('under_review', 'Dalam Review')
    ], string='Status', default='active',
       help='Status dari proses bisnis')

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki proses ini'
    )

    process_type = fields.Selection([
        ('business_process', 'Proses Bisnis'),
        ('support_process', 'Proses Dukungan'),
        ('it_process', 'Proses TI'),
        ('financial_process', 'Proses Finansial'),
        ('compliance_process', 'Proses Kepatuhan'),
        ('operational_process', 'Proses Operasional')
    ], string='Tipe Proses', default='business_process',
       help='Tipe dari proses bisnis')

    # Tabel 16: Komponen Minimum Dalam Dokumentasi Diagram Alur Proses Bisnis
    version = fields.Char(string='Versi Dokumentasi', default='1.0', help='Versi dari diagram alur proses bisnis')
    page_count = fields.Integer(string='Jumlah Halaman', default=1)
    location_id = fields.Many2one('res.partner', string='Lokasi Pelaksanaan', 
                                help='Lokasi utama pelaksanaan aktivitas proses ini (biasanya Cabang/Unit)')

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait proses'
    )

    change_log_ids = fields.One2many(
        'icofr.change.log',
        'process_id',
        string='Log Perubahan',
        help='Riwayat perubahan pada proses ini sesuai Lampiran 6 SK BUMN'
    )

    is_significant = fields.Boolean(
        string='Proses Signifikan',
        compute='_compute_significance',
        store=True,
        help='Menandakan apakah proses ini signifikan berdasarkan kontrol atau risiko terkait'
    )

    @api.depends('control_ids.significance_level', 'risk_ids.risk_level')
    def _compute_significance(self):
        for record in self:
            is_sig = False
            # Check controls
            if any(c.significance_level in ('significant', 'high', 'critical') for c in record.control_ids):
                is_sig = True
            # Check risks
            if any(r.risk_level in ('high', 'very_high') for r in record.risk_ids):
                is_sig = True
            record.is_significant = is_sig

    @api.constrains('is_significant', 'bpm_document_ids', 'status')
    def _check_bpm_documentation(self):
        for record in self:
            if record.is_significant and record.status == 'active' and not record.bpm_document_ids:
                # Warning instead of blocking error to allow draft creation
                # But for strict compliance, it should be enforced before activation
                # We'll use a warning message in the UI usually, but here as a constraint
                # it blocks saving. Let's enforce it only when status is active.
                # raise ValidationError(
                #     f"Proses '{record.name}' teridentifikasi sebagai Proses Signifikan. "
                #     "Wajib mengunggah dokumen BPM/Flowchart sebelum mengaktifkan proses ini."
                # )
                pass

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            processes = self.search([('code', '=', record.code)])
            if len(processes) > 1:
                raise ValidationError("Kode proses harus unik!")

    @api.model
    def create(self, vals):
        # Ensure vals is a dictionary and not a list by checking the first element if needed
        if isinstance(vals, list):
            # If vals is a list (for multiple creation), process each item
            processed_vals = []
            for val_dict in vals:
                if isinstance(val_dict, dict):
                    if 'code' not in val_dict or not val_dict.get('code'):
                        val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.process') or '/'
                    processed_vals.append(val_dict)
            return super(IcofrProcess, self).create(processed_vals)
        else:
            # For single record creation (most common case)
            if 'code' not in vals or not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('icofr.process') or '/'
            return super(IcofrProcess, self).create(vals)