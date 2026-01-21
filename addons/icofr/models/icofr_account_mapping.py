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

    entity_code = fields.Char(
        string='Kode Entitas',
        help='Kode entitas asal (misal: 103, 114, 0101)'
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

    kategori = fields.Char(string='Kategori', help='Kategori dari Template Laporan (misal: Neraca)')
    sub_kategori = fields.Char(string='Sub Kategori', help='Sub Kategori dari Template Laporan (misal: Aset)')

    account_balance = fields.Float(
        string='Saldo Akun',
        help='Saldo terakhir dari akun ini untuk keperluan scoping'
    )

    # Qualitative Factors (Pilar Scoping Dokumen 4)
    has_fraud_risk = fields.Boolean(string='Risiko Fraud?')
    is_volume_high = fields.Boolean(string='Volume Tinggi?')
    is_complex_transaction = fields.Boolean(string='Transaksi Kompleks?')
    is_characteristic_specific = fields.Boolean(string='Karakteristik Khusus?')
    is_volatile = fields.Boolean(string='Volatilitas Tinggi?')
    has_related_party = fields.Boolean(string='Pihak Berelasi?')

    # Tabel 5: Faktor Kualitatif Tambahan
    is_construction_wip = fields.Boolean('WIP BUMN Konstruksi?')
    is_held_by_third_party = fields.Boolean('Dikelola Pihak Ketiga?')
    is_loan_covenant = fields.Boolean('Terkait Loan Covenant?')
    is_onerous_contract = fields.Boolean('Kontrak Memberatkan?')
    is_asset_impairment = fields.Boolean('Penurunan Nilai Aset?')
    is_complex_estimate = fields.Boolean('Estimasi Rumit?')

    # Scoping Indicators (Matches PDF Document 4)
    is_quantitative_significant = fields.Boolean(
        string='Signifikan Kuantitatif',
        compute='_compute_scoping_flags',
        store=True,
        help='Otomatis True jika Saldo > PM'
    )

    is_qualitative_significant = fields.Boolean(
        string='Signifikan Kualitatif', 
        compute='_compute_scoping_flags',
        store=True,
        help='Otomatis True jika ada faktor risiko kualitatif yang dicentang'
    )

    is_in_scope = fields.Boolean(
        string='Masuk Scope Audit (In-Scope)',
        compute='_compute_scoping_flags',
        store=True,
        help='Hasil akhir: Akun wajib diuji jika signifikan secara kuantitatif ATAU kualitatif'
    )

    @api.depends('account_balance', 'materiality_id.performance_materiality_amount',
                 'has_fraud_risk', 'is_complex_transaction', 'has_related_party', 
                 'is_volume_high', 'is_characteristic_specific', 'is_volatile',
                 'is_construction_wip', 'is_held_by_third_party', 'is_loan_covenant', 
                 'is_onerous_contract', 'is_asset_impairment', 'is_complex_estimate')
    def _compute_scoping_flags(self):
        for record in self:
            # 1. Signifikansi Kuantitatif
            pm = record.materiality_id.performance_materiality_amount if record.materiality_id else 0
            is_quant = (pm > 0 and record.account_balance > pm)
            record.is_quantitative_significant = is_quant

            # 2. Signifikansi Kualitatif
            is_qual = any([
                record.has_fraud_risk, record.is_complex_transaction, record.has_related_party,
                record.is_volume_high, record.is_characteristic_specific, record.is_volatile,
                record.is_construction_wip, record.is_held_by_third_party, record.is_loan_covenant,
                record.is_onerous_contract, record.is_asset_impairment, record.is_complex_estimate
            ])
            record.is_qualitative_significant = is_qual

            # 3. Hasil Akhir (In-Scope)
            record.is_in_scope = is_quant or is_qual

    qualitative_justification = fields.Text(
        string='Justifikasi Kualitatif',
        help='Penjelasan detail mengenai faktor kualitatif yang membuat akun ini signifikan'
    )

    materiality_id = fields.Many2one(
        'icofr.materiality',
        string='Perhitungan Materialitas',
        ondelete='cascade'
    )

    process_id = fields.Many2one(
        'icofr.process',
        string='Proses Bisnis Terkait'
    )

    process_ids = fields.Many2many(
        'icofr.process',
        'icofr_account_mapping_process_rel',
        'account_mapping_id', 'process_id',
        string='Proses Terkait'
    )

    risk_ids = fields.Many2many(
        'icofr.risk',
        'icofr_account_mapping_risk_rel',
        'account_mapping_id', 'risk_id',
        string='Risiko Terkait'
    )

    control_ids = fields.Many2many(
        'icofr.control',
        'icofr_account_mapping_control_rel',
        'account_mapping_id', 'control_id',
        string='Kontrol Terkait'
    )

    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('review', 'Dalam Review'),
        ('mapped', 'Telah Dipetakan')
    ], string='Status', default='active')

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company
    )

    notes = fields.Text(string='Catatan')

    # Deprecated fields kept for view stability during transition
    significance_level = fields.Selection([('minor', 'Minor')], string='Tingkat Signifikansi (Deprecated)')
    is_significant_account = fields.Boolean(string='Akun Signifikan (Deprecated)')

    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'code' not in new_val_dict or not new_val_dict.get('code'):
                    new_val_dict['code'] = self.env['ir.sequence'].next_by_code('icofr.account.mapping') or '/'
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    gl_account_name = new_val_dict.get('gl_account', 'Akun')
                    fsl_item = new_val_dict.get('fsl_item', 'FSLI')
                    new_val_dict['name'] = f'{gl_account_name} -> {fsl_item}'
                processed_vals.append(new_val_dict)
            return super(IcofrAccountMapping, self).create(processed_vals)
        else:
            new_vals = vals.copy()
            if 'code' not in new_vals or not new_vals.get('code'):
                new_vals['code'] = self.env['ir.sequence'].next_by_code('icofr.account.mapping') or '/'
            if 'name' not in new_vals or not new_vals.get('name'):
                gl_account_name = new_vals.get('gl_account', 'Akun')
                fsl_item = new_vals.get('fsl_item', 'FSLI')
                new_vals['name'] = f'{gl_account_name} -> {fsl_item}'
            return super(IcofrAccountMapping, self).create(new_vals)

    def action_validate_mapping(self):
        self.ensure_one()
        if not self.gl_account or not self.fsl_item:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Gagal',
                    'message': 'Kode Akun GL dan FSLI harus diisi.',
                    'type': 'danger',
                }
            }
        self.write({'status': 'review'})
        return True

    def action_refresh_balance(self):
        self.ensure_one()
        if self.account_gl_id:
            ctx = {}
            if self.materiality_id and self.materiality_id.fiscal_year:
                ctx.update({
                    'date_from': f"{self.materiality_id.fiscal_year}-01-01",
                    'date_to': f"{self.materiality_id.fiscal_year}-12-31"
                })
            account = self.account_gl_id.with_context(**ctx)
            self.account_balance = abs(account.balance)
            return True
        return False
