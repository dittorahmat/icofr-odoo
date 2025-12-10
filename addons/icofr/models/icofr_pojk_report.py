# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrPojkReport(models.Model):
    _name = 'icofr.pojk.report'
    _description = 'Laporan POJK 15/2024'
    _order = 'reporting_period desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Laporan',
        required=True,
        help='Nama dari laporan POJK 15/2024'
    )
    
    reporting_period = fields.Char(
        string='Periode Pelaporan',
        required=True,
        help='Periode pelaporan (misalnya: Q1 2024, Tahunan 2024)'
    )
    
    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk laporan'
    )
    
    report_date = fields.Date(
        string='Tanggal Laporan',
        required=True,
        default=fields.Date.today,
        help='Tanggal laporan disusun'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang membuat laporan'
    )
    
    prepared_by_id = fields.Many2one(
        'res.users',
        string='Disusun Oleh',
        required=True,
        help='Pengguna yang menyusun laporan'
    )
    
    reviewed_by_id = fields.Many2one(
        'res.users',
        string='Direview Oleh',
        help='Pengguna yang mereview laporan'
    )
    
    approved_by_id = fields.Many2one(
        'res.users',
        string='Disetujui Oleh',
        help='Pengguna yang menyetujui laporan (biasanya CFO)'
    )
    
    status = fields.Selection([
        ('draft', 'Draf'),
        ('review', 'Dalam Review'),
        ('submitted', 'Dikirim'),
        ('approved', 'Disetujui'),
        ('published', 'Diterbitkan')
    ], string='Status', default='draft',
       help='Status laporan saat ini')
    
    # Data utama laporan sesuai POJK 15/2024
    total_controls = fields.Integer(
        string='Jumlah Total Kontrol',
        help='Jumlah total kontrol internal'
    )
    
    effective_controls = fields.Integer(
        string='Kontrol Efektif',
        help='Jumlah kontrol yang efektif'
    )
    
    effectiveness_percentage = fields.Float(
        string='Persentase Efektivitas',
        help='Persentase efektivitas kontrol internal'
    )
    
    total_risks = fields.Integer(
        string='Jumlah Total Risiko',
        help='Jumlah total risiko teridentifikasi'
    )
    
    high_risks = fields.Integer(
        string='Risiko Tingkat Tinggi',
        help='Jumlah risiko dengan tingkat tinggi'
    )
    
    total_findings = fields.Integer(
        string='Jumlah Total Temuan',
        help='Jumlah total temuan dari proses sertifikasi'
    )
    
    closed_findings = fields.Integer(
        string='Temuan Ditutup',
        help='Jumlah temuan yang sudah ditutup'
    )
    
    pending_findings = fields.Integer(
        string='Temuan Menunggu',
        help='Jumlah temuan yang masih menunggu penanganan'
    )
    
    # Isian spesifik POJK 15/2024
    framework_description = fields.Text(
        string='Deskripsi Kerangka Kerja',
        help='Deskripsi kerangka kerja kontrol internal yang digunakan'
    )
    
    control_environment_assessment = fields.Text(
        string='Penilaian Lingkungan Pengendalian',
        help='Penilaian terhadap lingkungan pengendalian'
    )
    
    risk_assessment_practices = fields.Text(
        string='Praktik Penilaian Risiko',
        help='Deskripsi praktik penilaian risiko'
    )
    
    control_activity_effectiveness = fields.Text(
        string='Efektivitas Aktivitas Pengendalian',
        help='Evaluasi efektivitas aktivitas pengendalian'
    )
    
    information_communication_quality = fields.Text(
        string='Kualitas Informasi dan Komunikasi',
        help='Evaluasi kualitas informasi dan komunikasi'
    )
    
    monitoring_activity_results = fields.Text(
        string='Hasil Aktivitas Pemantauan',
        help='Deskripsi hasil dari aktivitas pemantauan'
    )
    
    significant_deficiencies_detail = fields.Text(
        string='Detail Kekurangan Signifikan',
        help='Deskripsi rinci tentang kekurangan signifikan'
    )
    
    material_weaknesses_detail = fields.Text(
        string='Detail Kelemahan Material',
        help='Deskripsi rinci tentang kelemahan material'
    )
    
    management_response_detail = fields.Text(
        string='Detail Respon Manajemen',
        help='Deskripsi rinci tentang respon manajemen terhadap temuan'
    )
    
    improvement_actions = fields.Text(
        string='Tindakan Perbaikan',
        help='Tindakan perbaikan yang telah atau akan dilakukan'
    )
    
    compliance_status = fields.Selection([
        ('compliant', 'Sesuai'),
        ('partially_compliant', 'Sebagian Sesuai'),
        ('non_compliant', 'Tidak Sesuai')
    ], string='Status Kepatuhan', default='partially_compliant',
       help='Status kepatuhan terhadap POJK 15/2024')
    
    compliance_notes = fields.Text(
        string='Catatan Kepatuhan',
        help='Catatan tambahan terkait kepatuhan terhadap POJK 15/2024'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Laporan',
        help='File lampiran untuk laporan POJK'
    )
    
    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait laporan'
    )
    
    def action_submit_report(self):
        """Method untuk mengirimkan laporan"""
        self.ensure_one()
        if self.status == 'draft':
            self.write({
                'status': 'submitted',
                'reviewed_by_id': self.env.user.id
            })
        return True

    def action_approve_report(self):
        """Method untuk menyetujui laporan"""
        self.ensure_one()
        if self.status == 'submitted':
            self.write({
                'status': 'approved',
                'approved_by_id': self.env.user.id
            })
        return True

    def print_report(self):
        """Method untuk mencetak laporan"""
        self.ensure_one()
        # Ini adalah contoh sederhana, bisa dikembangkan lebih lanjut
        return self.env.ref('icofr.action_icofr_pojk_report').report_action(self)

    def export_to_excel(self):
        """Method untuk mengekspor laporan ke format Excel"""
        self.ensure_one()
        # Implementasi dasar untuk ekspor ke Excel
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel
        # dengan data laporan POJK 15/2024
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/binary/download_document/{self.id}/icofr.pojk.report/excel_export',
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        # Generate a default name if not provided
        if 'name' not in vals or not vals['name']:
            vals['name'] = f'Laporan POJK {vals.get("fiscal_year", fields.Date.today().year)} - {vals.get("reporting_period", "Periode")}'
        return super(IcofrPojkReport, self).create(vals)