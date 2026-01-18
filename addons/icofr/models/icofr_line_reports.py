# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class IcofrLine1Report(models.Model):
    """
    Model untuk laporan khusus Lini 1 (Process Owner)
    Berisi kontrol dan temuan yang menjadi tanggung jawab Lini 1
    """
    _name = 'icofr.line1.report'
    _description = 'Laporan Lini 1 - Pemilik Proses'
    _order = 'report_date desc'

    name = fields.Char(
        string='Nama Laporan',
        required=True,
        default=lambda self: f'Laporan Lini 1 - {fields.Date.today()}',
        help='Nama unik dari laporan Lini 1'
    )

    report_date = fields.Date(
        string='Tanggal Laporan',
        required=True,
        default=fields.Date.today(),
        help='Tanggal laporan dibuat'
    )

    period_start = fields.Date(
        string='Awal Periode',
        default=lambda self: self._default_period_start(),
        required=True,
        help='Tanggal awal periode pelaporan'
    )

    period_end = fields.Date(
        string='Akhir Periode',
        default=fields.Date.today,
        required=True,
        help='Tanggal akhir periode pelaporan'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Pembuat Laporan',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat laporan ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang terkait dengan laporan'
    )

    line_1_controls_count = fields.Integer(
        string='Jumlah Kontrol',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah kontrol yang menjadi tanggung jawab Lini 1'
    )

    effective_controls = fields.Integer(
        string='Kontrol Efektif',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah kontrol yang efektif'
    )

    ineffective_controls = fields.Integer(
        string='Kontrol Tidak Efektif',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah kontrol yang tidak efektif'
    )

    csa_completed = fields.Integer(
        string='CSA Selesai',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah CSA yang diselesaikan'
    )

    csa_pending = fields.Integer(
        string='CSA Menunggu',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah CSA yang belum diselesaikan'
    )

    findings_assigned = fields.Integer(
        string='Temuan Ditugaskan',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah temuan yang ditugaskan ke Lini 1'
    )

    findings_resolved = fields.Integer(
        string='Temuan Diselesaikan',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah temuan yang telah diselesaikan'
    )

    findings_overdue = fields.Integer(
        string='Temuan Terlambat',
        compute='_compute_line1_data',
        store=True,
        help='Jumlah temuan yang melewati batas waktu'
    )

    summary = fields.Text(
        string='Ringkasan Laporan',
        compute='_compute_summary',
        store=True,
        help='Ringkasan data laporan Lini 1'
    )

    @api.model
    def _default_period_start(self):
        # Default ke awal bulan ini
        today = fields.Date.today()
        return today.replace(day=1)

    @api.depends('period_start', 'period_end', 'company_id')
    def _compute_line1_data(self):
        for report in self:
            # Ambil kontrol yang dimiliki oleh pengguna saat ini atau dalam departemen mereka
            my_controls = self.env['icofr.control'].search([
                ('owner_id', '=', report.user_id.id),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.line_1_controls_count = len(my_controls)
            report.effective_controls = len(my_controls.filtered(lambda c: c.effectiveness_rating == 'high'))
            report.ineffective_controls = len(my_controls.filtered(lambda c: c.effectiveness_rating in ['low', 'not_tested']))

            # CSA yang ditugaskan ke pengguna ini
            my_csa = self.env['icofr.csa'].search([
                ('control_owner_id', '=', report.user_id.id),
                ('assessment_date', '>=', report.period_start),
                ('assessment_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.csa_completed = len(my_csa.filtered(lambda c: c.status == 'completed'))
            report.csa_pending = len(my_csa.filtered(lambda c: c.status in ['planned', 'in_progress']))

            # Temuan yang ditugaskan ke pengguna ini
            my_findings = self.env['icofr.finding'].search([
                ('owner_id', '=', report.user_id.id),
                ('create_date', '>=', report.period_start),
                ('create_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.findings_assigned = len(my_findings)
            report.findings_resolved = len(my_findings.filtered(lambda f: f.status == 'closed'))
            
            # Temuan terlambat
            today = fields.Date.today()
            overdue_findings = my_findings.filtered(
                lambda f: f.due_date and f.due_date < today and f.status != 'closed'
            )
            report.findings_overdue = len(overdue_findings)

    @api.depends('line_1_controls_count', 'effective_controls', 'ineffective_controls',
                 'csa_completed', 'csa_pending', 'findings_assigned', 'findings_resolved', 'findings_overdue')
    def _compute_summary(self):
        for report in self:
            report.summary = (
                f"Ringkasan Lini 1:\n"
                f"- Jumlah kontrol: {report.line_1_controls_count}\n"
                f"- Kontrol efektif: {report.effective_controls}\n"
                f"- Kontrol tidak efektif: {report.ineffective_controls}\n"
                f"- CSA selesai: {report.csa_completed}\n"
                f"- CSA menunggu: {report.csa_pending}\n"
                f"- Temuan ditugaskan: {report.findings_assigned}\n"
                f"- Temuan diselesaikan: {report.findings_resolved}\n"
                f"- Temuan terlambat: {report.findings_overdue}"
            )

    def action_refresh_data(self):
        """Refresh data laporan"""
        self._compute_line1_data()
        return True

    def print_report(self):
        """Print laporan Lini 1"""
        self.ensure_one()
        # Ini adalah contoh sederhana, bisa dikembangkan lebih lanjut
        return self.env.ref('icofr.action_icofr_line1_report').report_action(self)


class IcofrLine2Report(models.Model):
    """
    Model untuk laporan khusus Lini 2 (Risk/ICOFR Team)
    Berisi data dan metrik yang menjadi tanggung jawab Lini 2
    """
    _name = 'icofr.line2.report'
    _description = 'Laporan Lini 2 - Tim Risiko/ICOFR'
    _order = 'report_date desc'

    name = fields.Char(
        string='Nama Laporan',
        required=True,
        default=lambda self: f'Laporan Lini 2 - {fields.Date.today()}',
        help='Nama unik dari laporan Lini 2'
    )

    report_date = fields.Date(
        string='Tanggal Laporan',
        required=True,
        default=fields.Date.today(),
        help='Tanggal laporan dibuat'
    )

    period_start = fields.Date(
        string='Awal Periode',
        default=lambda self: self._default_period_start(),
        required=True,
        help='Tanggal awal periode pelaporan'
    )

    period_end = fields.Date(
        string='Akhir Periode',
        default=fields.Date.today,
        required=True,
        help='Tanggal akhir periode pelaporan'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Pembuat Laporan',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat laporan ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang terkait dengan laporan'
    )

    controls_reviewed = fields.Integer(
        string='Kontrol Direview',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah kontrol yang direview oleh Lini 2'
    )

    csa_reviewed = fields.Integer(
        string='CSA Direview',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah CSA yang direview oleh Lini 2'
    )

    findings_identified = fields.Integer(
        string='Temuan Diidentifikasi',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah temuan yang diidentifikasi oleh Lini 2'
    )

    findings_validated = fields.Integer(
        string='Temuan Tervalidasi',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah temuan yang telah divalidasi'
    )

    testing_performed = fields.Integer(
        string='Pengujian Dilakukan',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah pengujian yang dilakukan oleh Lini 2'
    )

    material_weakness_identified = fields.Integer(
        string='Kelemahan Material',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah kelemahan material yang diidentifikasi'
    )

    significant_deficiency_identified = fields.Integer(
        string='Kekurangan Signifikan',
        compute='_compute_line2_data',
        store=True,
        help='Jumlah kekurangan signifikan yang diidentifikasi'
    )

    # Hal 61: Rekonsiliasi & Rincian Perubahan
    comparison_line3_notes = fields.Text(
        string='Perbandingan Hasil Lini 3',
        help='Catatan perbandingan hasil pengujian Lini 2 vs Lini 3 (Wajib di Q4 sesuai Hal 61).'
    )
    process_changes_details = fields.Text('Rincian Perubahan Proses Bisnis')
    ineffective_csa_details = fields.Text('Rincian CSA Tidak Efektif/Tidak Ada Transaksi')

    summary = fields.Text(
        string='Ringkasan Laporan',
        compute='_compute_summary',
        store=True,
        help='Ringkasan data laporan Lini 2'
    )

    @api.model
    def _default_period_start(self):
        # Default ke awal bulan ini
        today = fields.Date.today()
        return today.replace(day=1)

    @api.depends('period_start', 'period_end', 'company_id')
    def _compute_line2_data(self):
        for report in self:
            # Ambil data CSA yang direview oleh user ini atau dalam grupnya
            csa_reviews = self.env['icofr.csa'].search([
                ('reviewer_id', '=', report.user_id.id),
                ('assessment_date', '>=', report.period_start),
                ('assessment_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.csa_reviewed = len(csa_reviews)
            
            # Ambil temuan yang dibuat oleh user ini atau terkait dengan review CSA mereka
            findings = self.env['icofr.finding'].search([
                ('create_date', '>=', report.period_start),
                ('create_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.findings_identified = len(findings)
            report.findings_validated = len(findings.filtered(lambda f: f.status in ['closed', 'in_progress']))
            
            # Temuan berdasarkan klasifikasi
            report.material_weakness_identified = len(findings.filtered(lambda f: f.deficiency_classified == 'material_weakness'))
            report.significant_deficiency_identified = len(findings.filtered(lambda f: f.deficiency_classified == 'significant_deficiency'))

            # Pengujian yang dilakukan oleh Lini 2
            tests = self.env['icofr.testing'].search([
                ('tester_id', '=', report.user_id.id),
                ('test_date', '>=', report.period_start),
                ('test_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.testing_performed = len(tests)

            # Kontrol yang direview oleh Lini 2 (kontrol yang bukan milik mereka tapi direview)
            controls = self.env['icofr.control'].search([
                ('create_date', '>=', report.period_start),
                ('create_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            # For this report, we'll count controls that had review activity
            report.controls_reviewed = len(controls)

    @api.depends('controls_reviewed', 'csa_reviewed', 'findings_identified', 'findings_validated',
                 'testing_performed', 'material_weakness_identified', 'significant_deficiency_identified')
    def _compute_summary(self):
        for report in self:
            report.summary = (
                f"Ringkasan Lini 2:\n"
                f"- Kontrol direview: {report.controls_reviewed}\n"
                f"- CSA direview: {report.csa_reviewed}\n"
                f"- Temuan diidentifikasi: {report.findings_identified}\n"
                f"- Temuan tervalidasi: {report.findings_validated}\n"
                f"- Pengujian dilakukan: {report.testing_performed}\n"
                f"- Kelemahan material: {report.material_weakness_identified}\n"
                f"- Kekurangan signifikan: {report.significant_deficiency_identified}"
            )

    def action_refresh_data(self):
        """Refresh data laporan"""
        self._compute_line2_data()
        return True

    def print_report(self):
        """Print laporan Lini 2"""
        self.ensure_one()
        # Ini adalah contoh sederhana, bisa dikembangkan lebih lanjut
        return self.env.ref('icofr.action_icofr_line2_report').report_action(self)


class IcofrLine3Report(models.Model):
    """
    Model untuk laporan khusus Lini 3 (Internal Audit)
    Berisi data dan metrik yang menjadi tanggung jawab Lini 3
    """
    _name = 'icofr.line3.report'
    _description = 'Laporan Lini 3 - Audit Internal'
    _order = 'report_date desc'

    name = fields.Char(
        string='Nama Laporan',
        required=True,
        default=lambda self: f'Laporan Lini 3 - {fields.Date.today()}',
        help='Nama unik dari laporan Lini 3'
    )

    report_date = fields.Date(
        string='Tanggal Laporan',
        required=True,
        default=fields.Date.today(),
        help='Tanggal laporan dibuat'
    )

    period_start = fields.Date(
        string='Awal Periode',
        default=lambda self: self._default_period_start(),
        required=True,
        help='Tanggal awal periode pelaporan'
    )

    period_end = fields.Date(
        string='Akhir Periode',
        default=fields.Date.today,
        required=True,
        help='Tanggal akhir periode pelaporan'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Pembuat Laporan',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat laporan ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang terkait dengan laporan'
    )

    testing_performed = fields.Integer(
        string='Pengujian Dilakukan',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah pengujian yang dilakukan oleh Lini 3'
    )

    findings_identified = fields.Integer(
        string='Temuan Diidentifikasi',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah temuan yang diidentifikasi oleh Lini 3'
    )

    high_risk_controls_tested = fields.Integer(
        string='Kontrol Risiko Tinggi Diuji',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah kontrol risiko tinggi yang diuji'
    )

    compliance_testing = fields.Integer(
        string='Pengujian Kepatuhan',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah pengujian kepatuhan yang dilakukan'
    )

    material_weakness_identified = fields.Integer(
        string='Kelemahan Material',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah kelemahan material yang diidentifikasi'
    )

    significant_deficiency_identified = fields.Integer(
        string='Kekurangan Signifikan',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah kekurangan signifikan yang diidentifikasi'
    )

    findings_remedied = fields.Integer(
        string='Temuan Remediasi',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah temuan yang telah selesai diperbaiki/diremediasi.'
    )

    audit_recommendations = fields.Integer(
        string='Rekomendasi Audit',
        compute='_compute_line3_data',
        store=True,
        help='Jumlah rekomendasi dari hasil audit'
    )

    # Bab VII 1.2: Komponen Laporan Hasil Pengujian Lini Ketiga
    executive_summary = fields.Html(
        string='Ringkasan Eksekutif',
        help='Ringkasan hasil pengujian rancangan dan operasi pengendalian (Efektif/Tidak Efektif).'
    )

    finding_ids = fields.Many2many(
        'icofr.finding',
        string='Rincian Temuan (Defisiensi)',
        compute='_compute_line3_data',
        store=True,
        help='Daftar temuan detail untuk pelaporan (Akar Masalah, Remediasi, dll).'
    )

    summary = fields.Text(
        string='Ringkasan Laporan',
        compute='_compute_summary',
        store=True,
        help='Ringkasan data laporan Lini 3'
    )

    @api.model
    def _default_period_start(self):
        # Default ke awal bulan ini
        today = fields.Date.today()
        return today.replace(day=1)

    @api.depends('period_start', 'period_end', 'company_id')
    def _compute_line3_data(self):
        for report in self:
            # Ambil pengujian yang dilakukan oleh user ini (Lini 3 - Internal Audit)
            tests = self.env['icofr.testing'].search([
                ('tester_id', '=', report.user_id.id),
                ('test_date', '>=', report.period_start),
                ('test_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            report.testing_performed = len(tests)
            
            # Ambil temuan yang diidentifikasi oleh Lini 3 (via testing atau manual input)
            # Filter temuan yang dibuat oleh Lini 3 atau terkait dengan test Lini 3
            findings = self.env['icofr.finding'].search([
                ('create_date', '>=', report.period_start),
                ('create_date', '<=', report.period_end),
                ('company_id', '=', report.company_id.id)
            ])
            
            l3_findings = findings.filtered(
                lambda f: f.created_by_id == report.user_id or (f.test_id and f.test_id.tester_id == report.user_id)
            )
            
            report.findings_identified = len(l3_findings)
            report.finding_ids = l3_findings # Populate the Many2many field
            
            # Temuan berdasarkan klasifikasi
            report.material_weakness_identified = len(l3_findings.filtered(lambda f: f.deficiency_classified == 'material_weakness'))
            report.significant_deficiency_identified = len(l3_findings.filtered(lambda f: f.deficiency_classified == 'significant_deficiency'))
            report.findings_remedied = len(l3_findings.filtered(lambda f: f.status == 'closed'))
            
            # Hitung rekomendasi dari temuan
            report.audit_recommendations = sum(1 for f in l3_findings if f.recommendation)
            
            # Kontrol risiko tinggi yang diuji
            high_risk_controls = self.env['icofr.control'].search([
                ('risk_ids.impact', '>=', 4),  # Misalnya, risiko dengan impact >= 4 adalah risiko tinggi
                ('company_id', '=', report.company_id.id)
            ])
            
            # Hitung berapa banyak dari kontrol risiko tinggi ini yang diuji oleh Lini 3
            tested_high_risk = 0
            for ctrl in high_risk_controls:
                if tests.filtered(lambda t: t.control_id.id == ctrl.id):
                    tested_high_risk += 1
            
            report.high_risk_controls_tested = tested_high_risk
            
            # Pengujian kepatuhan - pengujian yang terkait dengan sertifikasi
            compliance_tests = tests.filtered(lambda t: t.certification_id)
            report.compliance_testing = len(compliance_tests)

    @api.depends('testing_performed', 'findings_identified', 'high_risk_controls_tested',
                 'compliance_testing', 'material_weakness_identified', 'significant_deficiency_identified',
                 'audit_recommendations')
    def _compute_summary(self):
        for report in self:
            report.summary = (
                f"Ringkasan Lini 3:\n"
                f"- Pengujian dilakukan: {report.testing_performed}\n"
                f"- Temuan diidentifikasi: {report.findings_identified}\n"
                f"- Kontrol risiko tinggi diuji: {report.high_risk_controls_tested}\n"
                f"- Pengujian kepatuhan: {report.compliance_testing}\n"
                f"- Kelemahan material: {report.material_weakness_identified}\n"
                f"- Kekurangan signifikan: {report.significant_deficiency_identified}\n"
                f"- Temuan diremediasi: {report.findings_remedied}\n"
                f"- Rekomendasi audit: {report.audit_recommendations}"
            )

    def action_refresh_data(self):
        """Refresh data laporan"""
        self._compute_line3_data()
        return True

    def print_report(self):
        """Print laporan Lini 3"""
        self.ensure_one()
        # Ini adalah contoh sederhana, bisa dikembangkan lebih lanjut
        return self.env.ref('icofr.action_icofr_line3_report').report_action(self)