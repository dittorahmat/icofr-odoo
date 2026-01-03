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

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki laporan POJK ini'
    )

    compliance_notes = fields.Text(
        string='Catatan Kepatuhan',
        help='Catatan tambahan terkait kepatuhan terhadap POJK 15/2024'
    )

    # Quantification fields for financial impact
    monetary_impact_amount = fields.Float(
        string='Jumlah Dampak Moneter',
        help='Estimasi jumlah dampak moneter dari temuan'
    )

    impact_currency_id = fields.Many2one(
        'res.currency',
        string='Mata Uang Dampak',
        default=lambda self: self.env.company.currency_id,
        help='Mata uang untuk estimasi dampak moneter'
    )

    finding_ids = fields.One2many(
        'icofr.finding',
        'pojk_report_id',
        string='Temuan Terkait',
        help='Temuan-temuan yang terkait dengan laporan POJK ini'
    )

    material_weakness_count = fields.Integer(
        string='Jumlah Kelemahan Material',
        compute='_compute_deficiency_counts',
        store=True,
        help='Jumlah temuan kelemahan material'
    )

    significant_deficiency_count = fields.Integer(
        string='Jumlah Kekurangan Signifikan',
        compute='_compute_deficiency_counts',
        store=True,
        help='Jumlah temuan kekurangan signifikan'
    )

    control_deficiency_count = fields.Integer(
        string='Jumlah Kekurangan Kontrol',
        compute='_compute_deficiency_counts',
        store=True,
        help='Jumlah total kekurangan kontrol'
    )

    is_consolidated = fields.Boolean(
        string='Konsolidasi?',
        default=False,
        help='Centang jika laporan mencakup data dari anak perusahaan'
    )

    entities_included = fields.Text(
        string='Entitas yang Disertakan',
        help='Daftar entitas yang disertakan dalam laporan konsolidasi'
    )

    # Digital Signature Fields
    signed_by = fields.Many2one(
        'res.users',
        string='Ditandatangani Oleh',
        readonly=True,
        copy=False,
        help='Pengguna yang menandatangani laporan secara digital'
    )
    
    signed_date = fields.Datetime(
        string='Tanggal Tanda Tangan',
        readonly=True,
        copy=False,
        help='Waktu saat laporan ditandatangani'
    )
    
    signature_image = fields.Binary(
        string='Tanda Tangan',
        readonly=True,
        copy=False,
        help='Gambar tanda tangan digital'
    )
    
    signature_hash = fields.Char(
        string='Hash Tanda Tangan',
        readonly=True,
        copy=False,
        help='Hash unik untuk verifikasi integritas tanda tangan'
    )
    
    is_signed = fields.Boolean(
        string='Telah Ditandatangani',
        default=False,
        readonly=True,
        copy=False,
        help='Menandakan apakah laporan telah ditandatangani secara digital'
    )

    @api.depends('finding_ids', 'finding_ids.severity_level', 'finding_ids.deficiency_classified', 'is_consolidated', 'company_id')
    def _compute_deficiency_counts(self):
        for record in self:
            domain = []
            if record.is_consolidated:
                domain = [('company_id', 'child_of', record.company_id.id)]
            else:
                domain = [('company_id', '=', record.company_id.id)]
            
            findings = self.env['icofr.finding'].search(domain)
            # Count based on deficiency classification which is more accurate for POJK reporting
            record.material_weakness_count = len(findings.filtered(
                lambda f: f.deficiency_classified == 'material_weakness'
            ))
            record.significant_deficiency_count = len(findings.filtered(
                lambda f: f.deficiency_classified == 'significant_deficiency'
            ))
            record.control_deficiency_count = len(findings.filtered(
                lambda f: f.deficiency_classified == 'control_deficiency'
            ))


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

    def action_sign_report(self):
        """Method untuk menandatangani laporan secara digital"""
        self.ensure_one()
        from odoo.exceptions import UserError
        import hashlib
        
        if self.status != 'approved':
            raise UserError('Hanya laporan yang sudah disetujui yang dapat ditandatangani.')
            
        # Create a simple hash as a digital signature placeholder
        # In a real implementation, this would involve a digital signature provider
        signature_base = f"{self.name}-{self.approved_by_id.id}-{fields.Datetime.now()}"
        signature_hash = hashlib.sha256(signature_base.encode()).hexdigest()
        
        self.write({
            'signed_by': self.env.user.id,
            'signed_date': fields.Datetime.now(),
            'is_signed': True,
            'signature_hash': signature_hash,
            'status': 'published'
        })
        return True

    def action_generate_ceo_statement(self):
        """Method untuk mengenerate pernyataan CEO/CFO sesuai Lampiran 11"""
        self.ensure_one()
        ceo_name = self.approved_by_id.name or "[Nama CEO/CFO]"
        company_name = self.company_id.name or "[Nama Perusahaan]"
        period = self.reporting_period or "[Periode]"
        
        statement = f"""Sesuai dengan Juknis Kementerian BUMN tentang ICOFR, {ceo_name} mewakili {company_name} menyatakan bahwa:

1. Kami telah menelaah laporan keuangan yang berakhir pada {period}.
2. Berdasarkan pengetahuan kami, laporan keuangan tidak memuat pernyataan yang tidak benar tentang fakta material atau tidak mencantumkan fakta material yang diperlukan untuk membuat pernyataan yang dibuat, mengingat keadaan di mana pernyataan tersebut dibuat, tidak menyesatkan.
3. Berdasarkan pengetahuan kami, laporan keuangan, dan informasi keuangan lainnya yang termasuk dalam laporan keuangan, secara wajar menyajikan dalam semua hal yang material atas kondisi keuangan dan hasil operasi untuk periode-periode yang disajikan dalam laporan.
4. Kami telah mengimplementasikan pengendalian dan prosedur atas penyusunan laporan keuangan yang dianggap perlu untuk menyusun dan menyajikan secara wajar laporan keuangan (konsolidasi) dan bebas dari salah saji material.
5. Kami telah mengungkapkan, berdasarkan hasil evaluasi pengendalian internal atas pelaporan keuangan kepada Dewan Komisaris/Dewan Pengawas, Direksi dan Komite Audit, perihal:
   a. Seluruh defisiensi signifikan dan kelemahan material dalam rancangan dan pengoperasian pengendalian internal atas pelaporan keuangan.
   b. Perubahan signifikan dalam kebijakan akuntansi, prosedur dan faktor lainnya.
   c. Setiap kecurangan (fraud), baik yang berdampak secara material maupun tidak.

Demikian pernyataan ini dibuat untuk digunakan sebagaimana mestinya."""
        
        self.write({'management_response_detail': statement})
        return True

    def write(self, vals):
        """Override write to prevent modification of signed reports"""
        from odoo.exceptions import UserError
        for record in self:
            if record.is_signed and not self.env.context.get('ignore_signed_check'):
                # Allow only specific status changes or specific fields if needed, 
                # but generally block edits on signed reports
                if set(vals.keys()) - {'message_follower_ids', 'message_ids', 'message_main_attachment_id'}:
                     raise UserError('Laporan yang telah ditandatangani tidak dapat diubah. Silakan buat revisi baru jika diperlukan.')
        return super(IcofrPojkReport, self).write(vals)

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
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    fiscal_year = new_val_dict.get('fiscal_year')
                    reporting_period = new_val_dict.get('reporting_period')
                    fiscal_year_value = fiscal_year if fiscal_year else fields.Date.today().year
                    reporting_period_value = reporting_period if reporting_period else 'Periode'
                    new_val_dict['name'] = f'Laporan POJK {fiscal_year_value} - {reporting_period_value}'
                processed_vals.append(new_val_dict)
            return super(IcofrPojkReport, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                fiscal_year = new_vals.get('fiscal_year')
                reporting_period = new_vals.get('reporting_period')
                fiscal_year_value = fiscal_year if fiscal_year else fields.Date.today().year
                reporting_period_value = reporting_period if reporting_period else 'Periode'
                new_vals['name'] = f'Laporan POJK {fiscal_year_value} - {reporting_period_value}'
            return super(IcofrPojkReport, self).create(new_vals)