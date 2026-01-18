# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


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

    # Field Char untuk kode akun GL sebagai field utama untuk kompatibilitas
    gl_account = fields.Char(
        string='Kode Akun GL (General Ledger)',
        required=True,
        help='Kode akun General Ledger dari sistem atau manual'
    )

    # Field Many2one sebagai fitur tambahan untuk integrasi ke sistem akuntansi Odoo
    account_gl_id = fields.Many2one(
        'account.account',
        string='Akun GL dari Sistem',
        help='Pilih akun dari sistem akuntansi Odoo (opsional, untuk integrasi)'
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

    # Fallback field untuk deskripsi akun GL jika tidak menggunakan akun dari sistem
    gl_account_description = fields.Char(
        string='Deskripsi Akun (Manual/Import)',
        help='Deskripsi akun GL jika diinput manual atau dari file eksternal'
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
       compute='_compute_significance_level', store=True,
       readonly=False,
       help='Tingkat signifikansi dari akun terhadap laporan keuangan')

    account_balance = fields.Float(
        string='Saldo Akun',
        help='Saldo terakhir dari akun ini untuk keperluan scoping'
    )

    has_fraud_risk = fields.Boolean(
        string='Risiko Fraud?',
        help='Apakah akun ini memiliki risiko kecurangan yang tinggi?'
    )

    is_complex_transaction = fields.Boolean(
        string='Transaksi Kompleks?',
        help='Apakah transaksi pada akun ini memiliki kompleksitas yang tinggi?'
    )

    has_related_party = fields.Boolean(
        string='Pihak Berelasi?',
        help='Apakah akun ini melibatkan transaksi dengan pihak berelasi?'
    )

    # Tabel 5: Faktor Kualitatif Spesifik
    is_qualitative_significant = fields.Boolean('Signifikan (Kualitatif)?', help='Tandai jika akun signifikan karena faktor non-moneter sesuai Tabel 5.')
    is_construction_wip = fields.Boolean('WIP BUMN Konstruksi?', help='Akun Pekerjaan dalam Proses pada BUMN berbasis konstruksi.')
    is_held_by_third_party = fields.Boolean('Dikelola Pihak Ketiga?', help='Persediaan atau aset yang dikelola oleh pihak ketiga.')
    is_loan_covenant = fields.Boolean('Terkait Loan Covenant?', help='Akun yang dipersyaratkan dalam perjanjian pinjaman.')
    is_onerous_contract = fields.Boolean('Kontrak Memberatkan?', help='Provisi terkait Onerous Contract.')

    qualitative_justification = fields.Text(
        string='Justifikasi Kualitatif',
        help='Penjelasan detail mengenai faktor kualitatif yang membuat akun ini signifikan (Ref: Tabel 5)'
    )

    @api.onchange('is_construction_wip', 'is_held_by_third_party', 'is_loan_covenant', 'is_onerous_contract', 'has_fraud_risk', 'is_complex_transaction', 'has_related_party')
    def _onchange_qualitative_factors(self):
        """Auto-check the overall qualitative significance if any specific factor is set"""
        if any([self.is_construction_wip, self.is_held_by_third_party, self.is_loan_covenant, 
                self.is_onerous_contract, self.has_fraud_risk, self.is_complex_transaction, 
                self.has_related_party]):
            self.is_qualitative_significant = True

    materiality_id = fields.Many2one(
        'icofr.materiality',
        string='Perhitungan Materialitas',
        ondelete='cascade',
        help='Perhitungan materialitas yang terkait dengan pemetaan ini'
    )

    process_id = fields.Many2one(
        'icofr.process',
        string='Proses Bisnis Terkait',
        help='Proses bisnis utama yang terkait dengan akun ini'
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

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang memiliki pemetaan akun ini'
    )

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

    @api.depends('account_balance', 'materiality_id.performance_materiality_amount', 'significance_level')
    def _compute_significant_account(self):
        for record in self:
            is_significant = record.significance_level == 'significant'
            if record.materiality_id and record.account_balance > record.materiality_id.performance_materiality_amount:
                is_significant = True
            record.is_significant_account = is_significant

    @api.depends('account_balance', 'materiality_id.performance_materiality_amount', 
                 'has_fraud_risk', 'is_complex_transaction', 'has_related_party', 
                 'is_qualitative_significant', 'is_construction_wip', 'is_held_by_third_party')
    def _compute_significance_level(self):
        for record in self:
            # Quantitative limit
            pm = record.materiality_id.performance_materiality_amount if record.materiality_id else 0
            
            # Qualitative factors
            qualitative_trigger = any([
                record.has_fraud_risk, record.is_complex_transaction, record.has_related_party,
                record.is_qualitative_significant, record.is_construction_wip, 
                record.is_held_by_third_party, record.is_loan_covenant, record.is_onerous_contract
            ])
            
            if pm > 0 and record.account_balance > pm:
                record.significance_level = 'significant'
            elif qualitative_trigger:
                record.significance_level = 'significant'
            elif pm > 0 and record.account_balance > (pm * 0.5):
                record.significance_level = 'moderate'
            else:
                record.significance_level = 'minor'



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
                    gl_account_name = new_val_dict.get('gl_account', 'Akun')
                    fsl_item = new_val_dict.get('fsl_item', 'FSLI')
                    new_val_dict['name'] = f'{gl_account_name} -> {fsl_item}'
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
                gl_account_name = new_vals.get('gl_account', 'Akun')
                fsl_item = new_vals.get('fsl_item', 'FSLI')
                new_vals['name'] = f'{gl_account_name} -> {fsl_item}'
            return super(IcofrAccountMapping, self).create(new_vals)

    # Validasi akan diterapkan melalui required=True pada field gl_account

    def action_validate_mapping(self):
        """Method untuk memvalidasi pemetaan akun GL ke FSLI"""
        # Placeholder for validation functionality
        # In a real implementation, this would validate the mapping completeness
        # and correctness according to POJK 15/2024 requirements
        self.ensure_one()

        # Basic validation checks
        validation_messages = []

        # Check if gl_account is filled (it's required anyway)
        if not self.gl_account:
            validation_messages.append("Kode Akun GL belum diisi")
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

    @api.onchange('account_gl_id')
    def _onchange_account_gl_id(self):
        """Isi field deskripsi otomatis berdasarkan akun GL dari sistem yang dipilih"""
        if self.account_gl_id:
            # Ambil informasi dari akun GL terpilih
            account = self.account_gl_id

            # Jika deskripsi akun belum diisi, ambil dari akun GL
            if not self.gl_account_description:
                self.gl_account_description = account.name or account.code

            # Update kode akun GL sesuai dengan akun yang dipilih dari sistem
            if not self.gl_account:
                self.gl_account = account.code

    def action_refresh_balance(self):
        """Ambil saldo terbaru dari akun GL di sistem"""
        self.ensure_one()
        if self.account_gl_id:
            # Gunakan context untuk membatasi rentang tanggal jika ada tahun fiskal
            ctx = {}
            if self.materiality_id and self.materiality_id.fiscal_year:
                ctx.update({
                    'date_from': f"{self.materiality_id.fiscal_year}-01-01",
                    'date_to': f"{self.materiality_id.fiscal_year}-12-31"
                })
            
            # Ambil saldo dari field 'balance' standar Odoo (computed)
            account = self.account_gl_id.with_context(**ctx)
            self.account_balance = abs(account.balance)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sinkronisasi Berhasil',
                    'message': f'Saldo untuk akun {self.gl_account} telah diperbarui.',
                    'type': 'success',
                }
            }
        return False