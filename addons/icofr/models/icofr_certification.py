# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IcofrCertification(models.Model):
    _name = 'icofr.certification'
    _description = 'Sertifikasi ICORF'
    _order = 'fiscal_year desc'

    name = fields.Char(
        string='Nama Sertifikasi',
        required=True,
        help='Nama dari sertifikasi ICORF'
    )
    
    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk sertifikasi'
    )
    
    certification_date = fields.Date(
        string='Tanggal Sertifikasi',
        required=True,
        default=fields.Date.today,
        help='Tanggal sertifikasi dilakukan'
    )
    
    certified_by_id = fields.Many2one(
        'res.users',
        string='Disertifikasi Oleh',
        required=True,
        help='Pengguna yang melakukan sertifikasi (biasanya CEO/CFO)'
    )
    
    status = fields.Selection([
        ('draft', 'Draf'),
        ('submitted', 'Dikirim'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('archived', 'Diarsipkan')
    ], string='Status', default='draft',
       help='Status dari proses sertifikasi')
    
    effectiveness_statement = fields.Text(
        string='Pernyataan Efektivitas',
        help='Pernyataan mengenai efektivitas kontrol internal'
    )
    
    scope = fields.Text(
        string='Lingkup Sertifikasi',
        help='Lingkup dari sertifikasi kontrol internal'
    )
    
    pojk_report_ids = fields.Many2many(
        'icofr.pojk.report',
        'icofr_certification_pojk_report_rel',
        'certification_id', 'pojk_report_id',
        string='Laporan POJK Terkait',
        help='Laporan POJK yang terkait dengan sertifikasi ini'
    )

    finding_ids = fields.One2many(
        'icofr.finding',
        'certification_id',
        string='Temuan Terkait',
        help='Temuan-temuan yang terkait dengan sertifikasi ini'
    )

    workflow_id = fields.Many2one(
        'icofr.workflow',
        string='Workflow Persetujuan',
        help='Workflow persetujuan yang terkait dengan sertifikasi ini'
    )

    action_plan_ids = fields.One2many(
        'icofr.action.plan',
        'certification_id',
        string='Rencana Tindakan Terkait',
        help='Rencana tindakan yang terkait dengan sertifikasi ini'
    )

    # Additional fields for SK BUMN compliance
    scope = fields.Text(
        string='Lingkup Sertifikasi',
        help='Lingkup dari sertifikasi kontrol internal'
    )

    effectiveness_statement = fields.Text(
        string='Pernyataan Efektivitas',
        help='Pernyataan mengenai efektivitas kontrol internal'
    )

    internal_auditor_opinion = fields.Text(
        string='Opini Auditor Internal',
        help='Opini dari tim auditor internal terkait efektivitas kontrol'
    )

    external_auditor_opinion = fields.Text(
        string='Opini Auditor Eksternal',
        help='Opini dari auditor eksternal terkait efektivitas kontrol (jika ada)'
    )

    material_weakness_identified = fields.Boolean(
        string='Ada Kelemahan Material?',
        default=False,
        help='Apakah ditemukan adanya kelemahan material dalam sertifikasi ini'
    )

    significant_deficiencies_count = fields.Integer(
        string='Jumlah Kekurangan Signifikan',
        help='Jumlah kekurangan signifikan yang ditemukan'
    )

    action_plan_count = fields.Integer(
        string='Jumlah Rencana Tindakan',
        compute='_compute_related_counts',
        store=True,
        help='Jumlah rencana tindakan terkait dengan sertifikasi ini'
    )

    finding_count = fields.Integer(
        string='Jumlah Temuan',
        compute='_compute_related_counts',
        store=True,
        help='Jumlah temuan terkait dengan sertifikasi ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki sertifikasi ini'
    )

    is_consolidated = fields.Boolean(
        string='Sertifikasi Konsolidasi?',
        default=False,
        help='Menandakan apakah ini adalah sertifikasi konsolidasi yang mencakup lebih dari satu entitas'
    )

    entities_covered = fields.Text(
        string='Entitas yang Dicakup',
        help='Deskripsi entitas-entitas yang dicakup dalam sertifikasi konsolidasi ini'
    )

    material_weaknesses_identified = fields.Integer(
        string='Jumlah Kelemahan Material Teridentifikasi',
        default=0,
        help='Jumlah kelemahan material yang diidentifikasi dalam sertifikasi ini'
    )

    significant_deficiencies_identified = fields.Integer(
        string='Jumlah Kekurangan Signifikan Teridentifikasi',
        default=0,
        help='Jumlah kekurangan signifikan yang diidentifikasi dalam sertifikasi ini'
    )

    control_deficiencies_identified = fields.Integer(
        string='Jumlah Kekurangan Kontrol Teridentifikasi',
        default=0,
        help='Jumlah kekurangan kontrol yang diidentifikasi dalam sertifikasi ini'
    )

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan terkait sertifikasi'
    )

    created_by_id = fields.Many2one(
        'res.users',
        string='Dibuat Oleh',
        default=lambda self: self.env.user,
        help='Pengguna yang membuat sertifikasi'
    )

    # Lampiran 11: Poin-Poin Pernyataan CEO/CFO (Page 110)
    ack_financial_review = fields.Boolean('1. Telah menelaah laporan keuangan', default=False)
    ack_no_misstatement = fields.Boolean('2. Tidak memuat pernyataan yang tidak benar', default=False)
    ack_fair_presentation = fields.Boolean('3. Menyajikan secara wajar kondisi keuangan', default=False)
    ack_control_impl = fields.Boolean('4. Telah mengimplementasikan pengendalian internal', default=False)
    ack_deficiency_disclosure = fields.Boolean('5. Telah mengungkapkan seluruh MW dan SD', default=False)
    
    @api.constrains('status', 'ack_financial_review', 'ack_no_misstatement', 'ack_fair_presentation', 'ack_control_impl', 'ack_deficiency_disclosure')
    def _check_acknowledgments(self):
        """Sertifikasi tidak dapat disetujui jika poin-poin Lampiran 11 belum dicentang."""
        for record in self:
            if record.status == 'approved':
                if not all([record.ack_financial_review, record.ack_no_misstatement, 
                           record.ack_fair_presentation, record.ack_control_impl, 
                           record.ack_deficiency_disclosure]):
                    raise ValidationError("Sesuai Lampiran 11 Juknis BUMN, SELURUH poin pernyataan (1-5) WAJIB dicentang sebelum sertifikasi disetujui!")

    @api.depends('action_plan_ids', 'finding_ids', 'finding_ids.deficiency_classified')
    def _compute_related_counts(self):
        for record in self:
            record.action_plan_count = len(record.action_plan_ids)
            record.finding_count = len(record.finding_ids)
            
            # Count by classification for summary table (Lampiran 11)
            record.material_weaknesses_identified = len(record.finding_ids.filtered(lambda f: f.deficiency_classified == 'material_weakness'))
            record.significant_deficiencies_identified = len(record.finding_ids.filtered(lambda f: f.deficiency_classified == 'significant_deficiency'))
            record.control_deficiencies_identified = len(record.finding_ids.filtered(lambda f: f.deficiency_classified == 'control_deficiency'))
            
            # Set boolean flag if MW exists
            record.material_weakness_identified = record.material_weaknesses_identified > 0

    def create_certification_workflow(self):
        """Method untuk membuat workflow persetujuan untuk sertifikasi"""
        self.ensure_one()
        # Implementasi sederhana: buat entri workflow baru
        workflow = self.env['icofr.workflow'].create({
            'name': f'Workflow untuk {self.name}',
            'model_ref': f'icofr.certification,{self.id}',
            'initiator_id': self.certified_by_id.id,
            'status': 'active'
        })

        # Hubungkan workflow ke sertifikasi
        self.write({'workflow_id': workflow.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Workflow Persetujuan',
            'res_model': 'icofr.workflow',
            'res_id': workflow.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def export_certification_to_excel(self):
        """Method untuk mengekspor sertifikasi ke format Excel"""
        self.ensure_one()
        # Implementasi dasar untuk ekspor ke Excel
        # Dalam implementasi sebenarnya, ini akan menghasilkan file Excel
        # dengan data sertifikasi
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/binary/download_document/{self.id}/icofr.certification/excel_export',
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
                    if fiscal_year:
                        new_val_dict['name'] = f'Sertifikasi {fiscal_year}'
                    else:
                        new_val_dict['name'] = f'Sertifikasi {fields.Date.today().year}'
                processed_vals.append(new_val_dict)
            return super(IcofrCertification, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                fiscal_year = new_vals.get('fiscal_year')
                if fiscal_year:
                    new_vals['name'] = f'Sertifikasi {fiscal_year}'
                else:
                    new_vals['name'] = f'Sertifikasi {fields.Date.today().year}'
            return super(IcofrCertification, self).create(new_vals)