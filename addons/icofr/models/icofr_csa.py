# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCsa(models.Model):
    _name = 'icofr.csa'
    _description = 'Control Self-Assessment (CSA)'
    _order = 'assessment_period desc, control_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama CSA',
        required=True,
        help='Nama deskriptif dari Control Self-Assessment'
    )

    code = fields.Char(
        string='Kode CSA',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi CSA'
    )

    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol',
        required=True,
        help='Kontrol internal yang akan dievaluasi melalui CSA'
    )

    assessment_period = fields.Char(
        string='Periode Penilaian',
        required=True,
        help='Periode penilaian CSA (misalnya: Q1 2024, Januari 2024)'
    )

    assessment_date = fields.Date(
        string='Tanggal Penilaian',
        required=True,
        default=fields.Date.today,
        help='Tanggal CSA dilakukan'
    )

    control_owner_id = fields.Many2one(
        'res.users',
        string='Pemilik Kontrol',
        required=True,
        help='Pemilik kontrol yang akan melakukan CSA (Lini 1)'
    )

    reviewer_id = fields.Many2one(
        'res.users',
        string='Reviewer CSA',
        help='Reviewer CSA dari Lini 2 (Risk/ICOFR Team)'
    )

    assessment_type = fields.Selection([
        ('quarterly', 'Triwulanan'),
        ('semiannual', 'Semesteran'),
        ('annual', 'Tahunan'),
        ('adhoc', 'Insidental')
    ], string='Tipe Penilaian', default='quarterly',
       help='Tipe dari penilaian CSA')

    compliance_result = fields.Selection([
        ('fully_compliant', 'Sepenuhnya Patuh'),
        ('mostly_compliant', 'Mayoritas Patuh'),
        ('partially_compliant', 'Sebagian Patuh'),
        ('non_compliant', 'Tidak Patuh')
    ], string='Hasil Kepatuhan',
       help='Hasil keseluruhan dari penilaian kepatuhan kontrol')

    effectiveness_result = fields.Selection([
        ('highly_effective', 'Sangat Efektif'),
        ('effective', 'Efektif'),
        ('partially_effective', 'Efektif Sebagian'),
        ('ineffective', 'Tidak Efektif')
    ], string='Hasil Efektivitas',
       help='Efektivitas kontrol berdasarkan hasil CSA')

    # CSA Questionnaire Fields
    design_effective = fields.Boolean(
        string='Apakah desain kontrol efektif?',
        help='Kontrol telah dirancang secara efektif untuk mencapai tujuan kontrol'
    )

    operating_effective = fields.Boolean(
        string='Apakah kontrol beroperasi secara efektif?',
        help='Kontrol beroperasi secara efektif sesuai dengan desainnya'
    )

    frequency_complied = fields.Boolean(
        string='Apakah kontrol dilaksanakan sesuai frekuensi?',
        help='Kontrol dilaksanakan sesuai dengan frekuensi yang ditentukan'
    )

    documentation_accurate = fields.Boolean(
        string='Apakah dokumentasi kontrol akurat?',
        help='Dokumentasi kontrol mencerminkan pelaksanaan yang sebenarnya'
    )

    exception_handled = fields.Boolean(
        string='Apakah pengecualian ditangani dengan baik?',
        help='Pengecualian dari kontrol ditangani secara tepat'
    )

    # Additional CSA fields
    sample_size = fields.Integer(
        string='Ukuran Sampel',
        default=25,
        help='Jumlah sampel yang diuji dalam CSA (sesuai dengan sampling calculator)'
    )

    testing_evidence = fields.Text(
        string='Bukti Pengujian',
        help='Deskripsi bukti yang dikumpulkan selama CSA'
    )

    evidence_attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Lampiran Bukti',
        help='File bukti yang mendukung CSA'
    )

    findings = fields.Text(
        string='Temuan CSA',
        help='Temuan selama pelaksanaan CSA'
    )

    recommendations = fields.Text(
        string='Rekomendasi',
        help='Rekomendasi untuk perbaikan kontrol jika ditemukan kelemahan'
    )

    status = fields.Selection([
        ('planned', 'Terjadwal'),
        ('in_progress', 'Dalam Proses'),
        ('completed', 'Selesai'),
        ('reviewed', 'Direview'),
        ('approved', 'Disetujui'),
        ('archived', 'Diarsipkan')
    ], string='Status CSA', default='planned',
       help='Status dari proses CSA')

    next_csa_date = fields.Date(
        string='Tanggal CSA Berikutnya',
        help='Tanggal penilaian CSA berikutnya'
    )

    approval_note = fields.Text(
        string='Catatan Persetujuan',
        help='Catatan dari reviewer atau approver tentang CSA'
    )

    workflow_id = fields.Many2one(
        'icofr.workflow',
        string='Workflow Persetujuan',
        help='Workflow persetujuan yang terkait dengan CSA ini'
    )

    finding_ids = fields.One2many(
        'icofr.finding',
        'csa_id',
        string='Temuan Terkait CSA',
        help='Temuan-temuan yang dihasilkan dari CSA ini'
    )

    notes = fields.Text(
        string='Catatan Tambahan',
        help='Catatan tambahan terkait CSA'
    )

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                # Generate a default name if not provided
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    control_id = new_val_dict.get('control_id')
                    if control_id:
                        control = self.env['icofr.control'].browse(control_id)
                        period = new_val_dict.get('assessment_period', fields.Date.today().year)
                        new_val_dict['name'] = f'CSA: {control.name or "Kontrol"} - {period}'
                    else:
                        period = new_val_dict.get('assessment_period', fields.Date.today().year)
                        new_val_dict['name'] = f'CSA: Kontrol - {period}'

                # Generate code if not provided
                if 'code' not in new_val_dict or not new_val_dict.get('code'):
                    new_val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.csa') or '/'

                processed_vals.append(new_val_dict)
            return super(IcofrCsa, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            # Generate a default name if not provided
            if 'name' not in new_vals or not new_vals.get('name'):
                control_id = new_vals.get('control_id')
                if control_id:
                    control = self.env['icofr.control'].browse(control_id)
                    period = new_vals.get('assessment_period', fields.Date.today().year)
                    new_vals['name'] = f'CSA: {control.name or "Kontrol"} - {period}'
                else:
                    period = new_vals.get('assessment_period', fields.Date.today().year)
                    new_vals['name'] = f'CSA: Kontrol - {period}'

            # Generate code if not provided
            if 'code' not in new_vals or not new_vals.get('code'):
                new_vals['code'] = self.env['ir.sequence'].next_by_code('icofr.csa') or '/'

            return super(IcofrCsa, self).create(new_vals)

    @api.onchange('assessment_period')
    def _onchange_assessment_period(self):
        """Calculate next CSA date based on period"""
        if self.assessment_period:
            # Simple logic to set next CSA date based on type
            if 'Q1' in self.assessment_period:
                self.next_csa_date = fields.Date.from_string(f'{self.assessment_period.split()[-1]}-04-01')
            elif 'Q2' in self.assessment_period:
                self.next_csa_date = fields.Date.from_string(f'{self.assessment_period.split()[-1]}-07-01')
            elif 'Q3' in self.assessment_period:
                self.next_csa_date = fields.Date.from_string(f'{self.assessment_period.split()[-1]}-10-01')
            elif 'Q4' in self.assessment_period:
                next_year = int(self.assessment_period.split()[-1]) + 1
                self.next_csa_date = fields.Date.from_string(f'{next_year}-01-01')

    def action_submit_csa(self):
        """Method to submit CSA for review by Line 2"""
        self.ensure_one()
        self.write({
            'status': 'reviewed'
        })
        # Send notification to reviewer
        if self.reviewer_id:
            self.message_post(
                body=f"CSA telah disubmit untuk review oleh {self.env.user.name}",
                partner_ids=[self.reviewer_id.partner_id.id],
                subtype_xmlid='mail.mt_comment'
            )
        return True

    def action_approve_csa(self):
        """Method for Line 2 to approve CSA"""
        self.ensure_one()
        self.write({
            'status': 'approved',
            'approval_note': f'Disetujui oleh {self.env.user.name} pada {fields.Datetime.now()}'
        })
        return True

    def action_create_workflow(self):
        """Method to create approval workflow for CSA"""
        self.ensure_one()
        # Create a new workflow for CSA approval
        workflow = self.env['icofr.workflow'].create({
            'name': f'Workflow Persetujuan CSA: {self.name}',
            'model_ref': f'icofr.csa,{self.id}',
            'initiator_id': self.env.user.id,
            'status': 'active'
        })

        # Link workflow to CSA record
        self.write({'workflow_id': workflow.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Workflow CSA',
            'res_model': 'icofr.workflow',
            'res_id': workflow.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_schedule_csa_notification(self):
        """Method to create scheduled notification for CSA assignments"""
        for csa in self:
            # Create a scheduler for the CSA assignment notification
            scheduler = self.env['icofr.notification.scheduler'].create({
                'name': f'Notifikasi CSA: {csa.name}',
                'notification_type': 'csa_assignment',
                'model_ref': f'icofr.csa,{csa.id}',
                'recipient_ids': [(4, csa.control_owner_id.id)] if csa.control_owner_id else [],
                'next_run_date': fields.Datetime.now(),
                'active': True,
                'interval_number': 1,
                'interval_type': 'days',
                'company_id': csa.company_id.id,
            })

            # Add notification message
            scheduler._generate_notification_content()