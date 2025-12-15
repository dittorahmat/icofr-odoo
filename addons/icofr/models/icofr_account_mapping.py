# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrAccountMapping(models.Model):
    _name = 'icofr.account.mapping'
    _description = 'Pemetaan Akun ke FSLI'
    _order = 'sequence'

    name = fields.Char(
        string='Nama Pemetaan',
        required=True,
        help='Nama deskriptif dari pemetaan akun ke FSLI'
    )

    code = fields.Char(
        string='Kode Pemetaan',
        required=True,
        copy=False,
        help='Kode unik untuk identifikasi pemetaan'
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
        help='Urutan tampilan dalam daftar'
    )

    gl_account = fields.Char(
        string='Akun GL (General Ledger)',
        required=True,
        help='Kode atau nama akun General Ledger'
    )

    fsl_item = fields.Char(
        string='FSLI (Financial Statement Line Item)',
        required=True,
        help='Item baris laporan keuangan yang sesuai'
    )

    account_description = fields.Text(
        string='Deskripsi Akun GL',
        help='Deskripsi lengkap dari akun GL'
    )

    fsl_description = fields.Text(
        string='Deskripsi FSLI',
        help='Deskripsi dari item laporan keuangan'
    )

    significance_level = fields.Selection([
        ('significant', 'Signifikan'),
        ('moderate', 'Moderat'),
        ('minor', 'Minor')
    ], string='Tingkat Signifikansi', default='moderate',
       help='Tingkat signifikansi dari akun terhadap laporan keuangan')

    materiality_id = fields.Many2one(
        'icofr.materiality',
        string='Perhitungan Materialitas',
        ondelete='cascade',
        help='Perhitungan materialitas yang terkait dengan pemetaan ini'
    )

    process_ids = fields.Many2many(
        'icofr.process',
        'icofr_account_mapping_process_rel',
        'account_mapping_id', 'process_id',
        string='Proses Terkait',
        help='Proses bisnis yang terkait dengan akun ini'
    )

    risk_ids = fields.Many2many(
        'icofr.risk',
        'icofr_account_mapping_risk_rel',
        'account_mapping_id', 'risk_id',
        string='Risiko Terkait',
        help='Risiko yang terkait dengan akun ini'
    )

    control_ids = fields.Many2many(
        'icofr.control',
        'icofr_account_mapping_control_rel',
        'account_mapping_id', 'control_id',
        string='Kontrol Terkait',
        help='Kontrol internal yang terkait dengan akun ini'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('review', 'Dalam Review'),
        ('mapped', 'Telah Dipetakan')
    ], string='Status', default='active',
       help='Status dari proses pemetaan')

    notes = fields.Text(
        string='Catatan',
        help='Catatan tambahan tentang pemetaan akun ini'
    )

    is_significant_account = fields.Boolean(
        string='Akun Signifikan?',
        compute='_compute_significant_account',
        store=True,
        help='Menandakan apakah ini adalah akun yang signifikan'
    )

    @api.depends('significance_level')
    def _compute_significant_account(self):
        for record in self:
            record.is_significant_account = record.significance_level == 'significant'

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                # Generate code if not provided
                if 'code' not in new_val_dict or not new_val_dict.get('code'):
                    new_val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.account.mapping') or '/'
                # Generate name if not provided
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    new_val_dict['name'] = f'{new_val_dict.get("gl_account", "Akun")} -> {new_val_dict.get("fsl_item", "FSLI")}'
                processed_vals.append(new_val_dict)
            return super(IcofrAccountMapping, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            # Generate code if not provided
            if 'code' not in new_vals or not new_vals.get('code'):
                new_vals['code'] = self.env['ir.sequence'].next_by_code('icofr.account.mapping') or '/'
            # Generate name if not provided
            if 'name' not in new_vals or not new_vals.get('name'):
                new_vals['name'] = f'{new_vals.get("gl_account", "Akun")} -> {new_vals.get("fsl_item", "FSLI")}'
            return super(IcofrAccountMapping, self).create(new_vals)

    def action_validate_mapping(self):
        """Method untuk memvalidasi pemetaan akun GL ke FSLI"""
        # Placeholder for validation functionality
        # In a real implementation, this would validate the mapping completeness
        # and correctness according to POJK 15/2024 requirements
        self.ensure_one()

        # Basic validation checks
        validation_messages = []

        if not self.gl_account:
            validation_messages.append("Akun GL belum diisi")
        if not self.fsl_item:
            validation_messages.append("FSLI belum diisi")
        if not self.materiality_id:
            validation_messages.append("Perhitungan materialitas belum dipilih")

        if validation_messages:
            # In a real implementation, you might want to return a wizard or action
            # For now, we'll just return a simple message
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Validasi Pemetaan',
                    'message': 'Kesalahan validasi:\n' + '\n'.join(f'- {msg}' for msg in validation_messages),
                    'type': 'danger',
                }
            }

        # If all validations pass
        self.write({'status': 'review'})  # Update status to review after validation
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Validasi Berhasil',
                'message': 'Pemetaan akun telah divalidasi dan siap untuk ditinjau',
                'type': 'success',
            }
        }