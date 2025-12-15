# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrFinding(models.Model):
    _name = 'icofr.finding'
    _description = 'Temuan ICORF'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Temuan',
        required=True,
        help='Nama deskriptif dari temuan'
    )
    
    code = fields.Char(
        string='Kode Temuan',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi temuan'
    )
    
    finding_type = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('process_inefficiency', 'Ketidakefisienan Proses'),
        ('compliance_violation', 'Pelanggaran Kepatuhan'),
        ('risk_exposure', 'Eksposur Risiko'),
        ('material_weakness', 'Kelemahan Material'),
        ('significant_deficiency', 'Kekurangan Signifikan')
    ], string='Jenis Temuan', required=True,
       help='Jenis dari temuan yang ditemukan')
    
    severity_level = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('critical', 'Kritis')
    ], string='Tingkat Keparahan', required=True,
       help='Tingkat keparahan dari temuan')
    
    description = fields.Text(
        string='Deskripsi Temuan',
        help='Deskripsi lengkap dari temuan'
    )
    
    impact_assessment = fields.Text(
        string='Penilaian Dampak',
        help='Penilaian dampak dari temuan terhadap organisasi'
    )
    
    root_cause = fields.Text(
        string='Penyebab Utama',
        help='Analisis akar penyebab dari temuan'
    )
    
    certification_id = fields.Many2one(
        'icofr.certification',
        string='Sertifikasi Terkait',
        help='Sertifikasi atau audit yang menemukan isu ini'
    )
    
    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Terkait',
        help='Kontrol internal yang terkait dengan temuan'
    )
    
    risk_id = fields.Many2one(
        'icofr.risk',
        string='Risiko Terkait',
        help='Risiko yang terkait dengan temuan'
    )
    
    status = fields.Selection([
        ('open', 'Terbuka'),
        ('in_progress', 'Dalam Proses'),
        ('closed', 'Ditutup'),
        ('wont_fix', 'Tidak Akan Diperbaiki')
    ], string='Status', default='open',
       help='Status penanganan temuan saat ini')
    
    owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Temuan',
        required=True,
        help='Pengguna yang bertanggung jawab menangani temuan ini'
    )
    
    due_date = fields.Date(
        string='Tanggal Jatuh Tempo',
        help='Tanggal penyelesaian yang diharapkan'
    )
    
    closed_date = fields.Date(
        string='Tanggal Ditutup',
        help='Tanggal temuan sebenarnya ditutup'
    )
    
    action_plan_ids = fields.One2many(
        'icofr.action.plan',
        'finding_id',
        string='Rencana Tindakan',
        help='Rencana tindakan untuk mengatasi temuan'
    )
    
    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti yang mendukung temuan'
    )
    
    recommendation = fields.Text(
        string='Rekomendasi',
        help='Rekomendasi untuk mengatasi temuan'
    )
    
    created_by_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat temuan'
    )
    
    # Add reference to CSA that generated this finding
    csa_id = fields.Many2one(
        'icofr.csa',
        string='CSA Terkait',
        help='CSA (Control Self-Assessment) yang menghasilkan temuan ini'
    )

    # Add reference to POJK report that this finding is related to
    pojk_report_id = fields.Many2one(
        'icofr.pojk.report',
        string='Laporan POJK Terkait',
        help='Laporan POJK yang terkait dengan temuan ini'
    )

    # Deficiency Classification Enhancement
    deficiency_category = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('process_inefficiency', 'Ketidakefisienan Proses'),
        ('compliance_violation', 'Pelanggaran Kepatuhan'),
        ('risk_exposure', 'Eksposur Risiko'),
        ('material_weakness', 'Kelemahan Material'),
        ('significant_deficiency', 'Kekurangan Signifikan')
    ], string='Kategori Kekurangan',
       help='Klasifikasi temuan ke dalam kategori kekurangan')

    quantitative_impact_amount = fields.Float(
        string='Dampak Kuantitatif (Rp)',
        help='Estimasi dampak kuantitatif dalam rupiah'
    )

    impact_currency_id = fields.Many2one(
        'res.currency',
        string='Mata Uang Dampak',
        default=lambda self: self.env.company.currency_id,
        help='Mata uang untuk estimasi dampak'
    )

    qualitative_impact_score = fields.Float(
        string='Skor Dampak Kualitatif',
        help='Skor kualitatif untuk dampak temuan (skala 1-5)'
    )

    deficiency_classified = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('significant_deficiency', 'Kekurangan Signifikan'),
        ('material_weakness', 'Kelemahan Material')
    ], string='Klasifikasi Kekurangan',
       compute='_compute_deficiency_classification',
       store=True,
       help='Klasifikasi otomatis temuan berdasarkan kriteria kuantitatif dan kualitatif')

    classification_reason = fields.Text(
        string='Alasan Klasifikasi',
        compute='_compute_classification_reason',
        store=True,
        help='Alasan untuk klasifikasi otomatis'
    )

    impact_assessment_details = fields.Text(
        string='Detail Penilaian Dampak',
        help='Detail penilaian dampak dari temuan'
    )

    corrective_action_required = fields.Boolean(
        string='Diperlukan Tindakan Korektif',
        default=False,
        help='Menandakan apakah diperlukan tindakan korektif untuk mengatasi temuan'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki temuan ini'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait temuan'
    )

    @api.depends('severity_level', 'quantitative_impact_amount', 'qualitative_impact_score')
    def _compute_deficiency_classification(self):
        """Automatic classification of deficiency based on quantitative and qualitative factors"""
        for record in self:
            if record.severity_level == 'critical' or record.quantitative_impact_amount > 1000000000 or record.qualitative_impact_score >= 4.5:
                record.deficiency_classified = 'material_weakness'
            elif record.severity_level == 'high' or record.quantitative_impact_amount > 100000000 or record.qualitative_impact_score >= 3.5:
                record.deficiency_classified = 'significant_deficiency'
            else:
                record.deficiency_classified = 'control_deficiency'

    @api.depends('deficiency_classified', 'quantitative_impact_amount', 'qualitative_impact_score', 'severity_level')
    def _compute_classification_reason(self):
        """Computes the reason for the automatic classification"""
        for record in self:
            reasons = []
            if record.severity_level == 'critical':
                reasons.append('Tingkat keparahan kritis')
            elif record.severity_level == 'high':
                reasons.append('Tingkat keparahan tinggi')

            if record.quantitative_impact_amount and record.quantitative_impact_amount > 1000000000:
                reasons.append(f'Dampak kuantitatif tinggi: Rp. {record.quantitative_impact_amount:,.0f}')
            elif record.quantitative_impact_amount and record.quantitative_impact_amount > 100000000:
                reasons.append(f'Dampak kuantitatif menengah: Rp. {record.quantitative_impact_amount:,.0f}')

            if record.qualitative_impact_score and record.qualitative_impact_score >= 4.5:
                reasons.append(f'Skor dampak kualitatif sangat tinggi: {record.qualitative_impact_score}')
            elif record.qualitative_impact_score and record.qualitative_impact_score >= 3.5:
                reasons.append(f'Skor dampak kualitatif tinggi: {record.qualitative_impact_score}')

            record.classification_reason = ', '.join(reasons) if reasons else 'Tidak ada kriteria klasifikasi yang terpenuhi'
    
    def action_close_finding(self):
        """Method untuk menutup temuan"""
        self.ensure_one()
        self.write({
            'status': 'closed',
            'closed_date': fields.Date.today()
        })
        return True

    def action_reopen_finding(self):
        """Method untuk membuka kembali temuan"""
        self.ensure_one()
        self.write({
            'status': 'open',
            'closed_date': False
        })
        return True

    @api.model
    def create(self, vals):
        # Ensure vals is a dictionary and not a list by checking the first element if needed
        if isinstance(vals, list):
            # If vals is a list (for multiple creation), process each item
            processed_vals = []
            for val_dict in vals:
                if isinstance(val_dict, dict):
                    if 'code' not in val_dict or not val_dict.get('code'):
                        val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.finding') or '/'
                    processed_vals.append(val_dict)
            return super(IcofrFinding, self).create(processed_vals)
        else:
            # For single record creation (most common case)
            if 'code' not in vals or not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('icofr.finding') or '/'
            return super(IcofrFinding, self).create(vals)