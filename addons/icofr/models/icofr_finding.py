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
        ('draft', 'Draf'),
        ('planned', 'Dijadwalkan'),
        ('open', 'Terbuka'),
        ('in_progress', 'Dalam Proses'),
        ('closed', 'Ditutup'),
        ('wont_fix', 'Tidak Akan Diperbaiki')
    ], string='Status', default='draft',
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

    recommended_action = fields.Text(
        string='Tindakan yang Direkomendasikan',
        help='Tindakan spesifik yang direkomendasikan untuk mengatasi temuan'
    )
    
    created_by_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat temuan'
    )
    
    # Add reference to testing that generated this finding
    test_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian Terkait',
        help='Pengujian yang menemukan temuan ini'
    )

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
        ('process_deficiency', 'Kekurangan Proses'),
        ('process_inefficiency', 'Ketidakefisienan Proses'),
        ('timing_deficiency', 'Kekurangan Waktu Pelaksanaan'),
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

    classification_method = fields.Selection([
        ('automatic', 'Otomatis'),
        ('manual', 'Manual'),
        ('hybrid', 'Gabungan (Otomatis + Justifikasi Manual)')
    ], string='Metode Klasifikasi',
       default='automatic',
       help='Metode yang digunakan untuk mengklasifikasikan kekurangan')

    deficiency_classification_reason = fields.Text(
        string='Alasan Klasifikasi Defisiensi',
        compute='_compute_classification_reason',
        store=True,
        help='Alasan untuk klasifikasi defisiensi'
    )

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

    # Manual input fields for Lini 3/Management to specify monetary impact
    manual_monetary_impact_amount = fields.Float(
        string='Dampak Moneter Manual',
        help='Nilai dampak moneter yang dimasukkan secara manual oleh Lini 3'
    )

    manual_impact_currency_id = fields.Many2one(
        'res.currency',
        string='Mata Uang Dampak Manual',
        default=lambda self: self.env.company.currency_id,
        help='Mata uang untuk nilai dampak moneter manual'
    )

    manual_qualitative_impact_score = fields.Float(
        string='Skor Dampak Kualitatif Manual',
        help='Skor kualitatif untuk dampak temuan yang diinput manual oleh Lini 3'
    )

    # Field to allow Lini 2/management to override system classification
    override_deficiency_classification = fields.Selection([
        ('control_deficiency', 'Kekurangan Kontrol'),
        ('significant_deficiency', 'Kekurangan Signifikan'),
        ('material_weakness', 'Kelemahan Material')
    ], string='Klasifikasi Defisiensi Manual',
       help='Klasifikasi defisiensi yang ditentukan secara manual oleh Lini 2/manajemen')

    override_reason = fields.Text(
        string='Alasan Override',
        help='Alasan manajemen untuk mengoverride klasifikasi defisiensi sistem'
    )

    overridden_by_id = fields.Many2one(
        'res.users',
        string='Dioverride Oleh',
        help='Pengguna yang melakukan override terhadap klasifikasi defisiensi'
    )

    override_date = fields.Datetime(
        string='Tanggal Override',
        help='Tanggal klasifikasi defisiensi dilakukan override'
    )

    # Enhanced impact assessment fields
    impact_assessment_method = fields.Selection([
        ('automatic', 'Otomatis (berdasarkan kuantitatif dan kualitatif)'),
        ('manual', 'Manual'),
        ('hybrid', 'Gabungan (Otomatis + Justifikasi Manual)')
    ], string='Metode Penilaian Dampak', default='automatic',
       help='Metode yang digunakan untuk menilai dampak temuan')

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait temuan'
    )

    @api.depends('severity_level', 'quantitative_impact_amount', 'qualitative_impact_score',
                 'manual_monetary_impact_amount', 'manual_qualitative_impact_score',
                 'override_deficiency_classification')
    def _compute_deficiency_classification(self):
        """Classification of deficiency based on quantitative and qualitative factors, with manual override capability"""
        for record in self:
            # Check if there is a manual override
            if record.override_deficiency_classification:
                record.deficiency_classified = record.override_deficiency_classification
                continue

            # Use manual inputs if provided and method is manual or hybrid
            if record.impact_assessment_method == 'manual':
                monetary_impact = record.manual_monetary_impact_amount
                qualitative_score = record.manual_qualitative_impact_score
            elif record.impact_assessment_method == 'hybrid':
                # Use the higher of automatic or manual values for more conservative approach
                monetary_impact = max(record.quantitative_impact_amount or 0, record.manual_monetary_impact_amount or 0)
                qualitative_score = max(record.qualitative_impact_score or 0, record.manual_qualitative_impact_score or 0)
            else:  # automatic
                monetary_impact = record.quantitative_impact_amount
                qualitative_score = record.qualitative_impact_score

            # Apply classification rules based on values
            if record.severity_level == 'critical' or monetary_impact > 1000000000 or qualitative_score >= 4.5:
                record.deficiency_classified = 'material_weakness'
            elif record.severity_level == 'high' or monetary_impact > 100000000 or qualitative_score >= 3.5:
                record.deficiency_classified = 'significant_deficiency'
            else:
                record.deficiency_classified = 'control_deficiency'

    @api.depends('deficiency_classified', 'quantitative_impact_amount', 'qualitative_impact_score',
                 'manual_monetary_impact_amount', 'manual_qualitative_impact_score', 'severity_level',
                 'override_deficiency_classification', 'override_reason')
    def _compute_classification_reason(self):
        """Computes the reason for the (auto or manual) classification"""
        for record in self:
            reasons = []

            # Check if there's a manual override
            if record.override_deficiency_classification:
                reasons.append(f"Dioverride manual ke {dict(record._fields['override_deficiency_classification'].selection).get(record.override_deficiency_classification)}")
                if record.override_reason:
                    reasons.append(f"Alasan override: {record.override_reason}")
            else:
                # Automatic classification reasons
                if record.severity_level == 'critical':
                    reasons.append('Tingkat keparahan kritis')
                elif record.severity_level == 'high':
                    reasons.append('Tingkat keparahan tinggi')

                # Check monetary impact (using appropriate value based on method)
                monetary_impact = record.manual_monetary_impact_amount if record.impact_assessment_method in ['manual', 'hybrid'] else (record.quantitative_impact_amount or 0)
                if monetary_impact and monetary_impact > 1000000000:
                    reasons.append(f'Dampak kuantitatif sangat tinggi: Rp. {monetary_impact:,.0f}')
                elif monetary_impact and monetary_impact > 100000000:
                    reasons.append(f'Dampak kuantitatif menengah: Rp. {monetary_impact:,.0f}')

                # Check qualitative score
                qualitative_score = record.manual_qualitative_impact_score if record.impact_assessment_method in ['manual', 'hybrid'] else (record.qualitative_impact_score or 0)
                if qualitative_score and qualitative_score >= 4.5:
                    reasons.append(f'Skor dampak kualitatif sangat tinggi: {qualitative_score}')
                elif qualitative_score and qualitative_score >= 3.5:
                    reasons.append(f'Skor dampak kualitatif tinggi: {qualitative_score}')

            record.classification_reason = ', '.join(reasons) if reasons else 'Tidak ada kriteria klasifikasi yang terpenuhi'

    # Method to apply manual override
    def action_apply_override(self):
        """Method to apply manual override to deficiency classification"""
        for record in self:
            if record.override_deficiency_classification:
                record.deficiency_classified = record.override_deficiency_classification
                record.overridden_by_id = self.env.user
                record.override_date = fields.Datetime.now()

                # Log the change
                record.message_post(
                    body=f"Klasifikasi defisiensi diubah menjadi '{dict(record._fields['override_deficiency_classification'].selection).get(record.override_deficiency_classification)}' secara manual. "
                         f"Alasan: {record.override_reason or 'Tidak ada alasan diberikan.'}",
                    subtype_xmlid='mail.mt_note',
                    author_id=self.env.user.partner_id.id
                )
        return True
    
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