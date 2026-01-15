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

    # Lampiran 10: Kertas Kerja DoD (Kotak 1 - 7)
    box_1_direct_relation = fields.Boolean('Kotak 1: Berhubungan langsung dengan asersi?')
    box_2_likelihood = fields.Boolean('Kotak 2: Terdapat kemungkinan (likelihood) salah saji?')
    box_3_magnitude = fields.Boolean('Kotak 3: Besaran dampak (magnitude) berpotensi material?')
    box_4_important = fields.Boolean('Kotak 4: Cukup penting untuk perhatian pengawas?')
    box_5_compensating = fields.Boolean('Kotak 5: Terdapat compensating control efektif?')
    box_6_prudent_official = fields.Boolean('Kotak 6: Auditor menyimpulkan sebagai Kelemahan Material?')
    box_7_aggregate = fields.Boolean('Kotak 7: Terdapat defisiensi lain yang memengaruhi akun yang sama?')

    # Tabel 24: Distribusi Pelaporan (Pihak-pihak yang telah diinformasikan)
    reported_to_ceo = fields.Boolean('Dilaporkan ke CEO & Direksi Terkait', help='Wajib untuk CD, SD, MW')
    reported_to_board = fields.Boolean('Dilaporkan ke Dewan Komisaris/Pengawas', help='Wajib untuk SD, MW')
    reported_to_audit_committee = fields.Boolean('Dilaporkan ke Komite Audit', help='Wajib untuk CD, SD, MW')
    reported_to_mgmt_assessment = fields.Boolean('Tercantum dalam Asesmen Manajemen', help='Wajib untuk SD, MW')

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki temuan ini'
    )

    # Compensating Control Logic
    compensating_control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Pengganti (Compensating Control)',
        help='Kontrol yang dapat memitigasi risiko jika kontrol utama gagal. Keberadaannya dapat menurunkan klasifikasi defisiensi.'
    )

    is_compensating_control_effective = fields.Boolean(
        string='Kontrol Pengganti Efektif?',
        help='Apakah kontrol pengganti telah diuji dan terbukti efektif?'
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
                 'override_deficiency_classification', 'compensating_control_id', 'is_compensating_control_effective', 'company_id')
    def _compute_deficiency_classification(self):
        """Classification of deficiency based on quantitative and qualitative factors, with manual override capability"""
        for record in self:
            # Check if there is a manual override
            if record.override_deficiency_classification:
                record.deficiency_classified = record.override_deficiency_classification
                continue

            # Determine Monetary Impact
            if record.impact_assessment_method == 'manual':
                monetary_impact = record.manual_monetary_impact_amount
                qualitative_score = record.manual_qualitative_impact_score
            elif record.impact_assessment_method == 'hybrid':
                monetary_impact = max(record.quantitative_impact_amount or 0, record.manual_monetary_impact_amount or 0)
                qualitative_score = max(record.qualitative_impact_score or 0, record.manual_qualitative_impact_score or 0)
            else:  # automatic
                monetary_impact = record.quantitative_impact_amount
                qualitative_score = record.qualitative_impact_score

            # Fetch Active Materiality Thresholds for the Company and Year
            # Assumes Fiscal Year is current year or year of creation.
            # Ideally, finding should have fiscal_year field. Using current year for simplicity or matching record date.
            fiscal_year = str(record.create_date.year) if record.create_date else str(fields.Date.today().year)
            materiality = self.env['icofr.materiality'].search([
                ('company_id', '=', record.company_id.id),
                ('fiscal_year', '=', fiscal_year),
                ('active', '=', True)
            ], limit=1)

            om_threshold = materiality.overall_materiality_amount if materiality else 1000000000.0 # Fallback default
            pm_threshold = materiality.performance_materiality_amount if materiality else 500000000.0 # Fallback default

            # Initial Classification
            classification = 'control_deficiency'
            
            # Quantitative Logic
            if monetary_impact > om_threshold:
                classification = 'material_weakness'
            elif monetary_impact > pm_threshold:
                classification = 'significant_deficiency'
            
            # Qualitative Logic (Enhancement)
            if qualitative_score and qualitative_score >= 4.5:
                classification = 'material_weakness'
            elif qualitative_score and qualitative_score >= 3.5 and classification != 'material_weakness':
                classification = 'significant_deficiency'
            
            # Criticality Logic override
            if record.severity_level == 'critical':
                classification = 'material_weakness'
            elif record.severity_level == 'high' and classification != 'material_weakness':
                classification = 'significant_deficiency'

            # Compensating Control Logic (Downgrade)
            if record.compensating_control_id and record.is_compensating_control_effective:
                if classification == 'material_weakness':
                    classification = 'significant_deficiency' # Downgrade MW to SD
                elif classification == 'significant_deficiency':
                    classification = 'control_deficiency' # Downgrade SD to CD

            record.deficiency_classified = classification

    @api.depends('deficiency_classified', 'quantitative_impact_amount', 'qualitative_impact_score',
                 'manual_monetary_impact_amount', 'manual_qualitative_impact_score', 'severity_level',
                 'override_deficiency_classification', 'override_reason', 'compensating_control_id', 'is_compensating_control_effective')
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
                # Materiality Context
                fiscal_year = str(record.create_date.year) if record.create_date else str(fields.Date.today().year)
                materiality = self.env['icofr.materiality'].search([
                    ('company_id', '=', record.company_id.id),
                    ('fiscal_year', '=', fiscal_year),
                    ('active', '=', True)
                ], limit=1)
                
                om_threshold = materiality.overall_materiality_amount if materiality else 0
                pm_threshold = materiality.performance_materiality_amount if materiality else 0

                # Automatic classification reasons
                if record.severity_level == 'critical':
                    reasons.append('Tingkat keparahan kritis')
                elif record.severity_level == 'high':
                    reasons.append('Tingkat keparahan tinggi')

                # Check monetary impact
                monetary_impact = record.manual_monetary_impact_amount if record.impact_assessment_method in ['manual', 'hybrid'] else (record.quantitative_impact_amount or 0)
                
                if materiality:
                    if monetary_impact > om_threshold:
                        reasons.append(f'Dampak (Rp {monetary_impact:,.0f}) melebihi Overall Materiality (Rp {om_threshold:,.0f})')
                    elif monetary_impact > pm_threshold:
                        reasons.append(f'Dampak (Rp {monetary_impact:,.0f}) melebihi Performance Materiality (Rp {pm_threshold:,.0f})')
                else:
                    # Fallback reason if no materiality record found
                    if monetary_impact > 1000000000:
                        reasons.append(f'Dampak kuantitatif sangat tinggi (Fallback Threshold): Rp. {monetary_impact:,.0f}')

                # Check qualitative score
                qualitative_score = record.manual_qualitative_impact_score if record.impact_assessment_method in ['manual', 'hybrid'] else (record.qualitative_impact_score or 0)
                if qualitative_score and qualitative_score >= 4.5:
                    reasons.append(f'Skor dampak kualitatif sangat tinggi: {qualitative_score}')
                elif qualitative_score and qualitative_score >= 3.5:
                    reasons.append(f'Skor dampak kualitatif tinggi: {qualitative_score}')

                # Compensating Control Note
                if record.compensating_control_id and record.is_compensating_control_effective:
                    reasons.append(f"Klasifikasi diturunkan karena adanya Kontrol Pengganti Efektif: {record.compensating_control_id.name}")

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