# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IcofrMateriality(models.Model):
    _name = 'icofr.materiality'
    _description = 'Kalkulator Materialitas ICORF'
    _order = 'fiscal_year desc, create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nama Perhitungan',
        required=True,
        default='Kalkulasi Materialitas',
        help='Nama deskriptif dari perhitungan materialitas'
    )

    fiscal_year = fields.Char(
        string='Tahun Fiskal',
        required=True,
        help='Tahun fiskal untuk perhitungan materialitas ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company,
        help='Perusahaan yang menjadi basis perhitungan'
    )

    revenue_amount = fields.Float(
        string='Jumlah Pendapatan',
        required=True,
        help='Jumlah pendapatan perusahaan (dalam satuan mata uang lokal)'
    )

    total_assets_amount = fields.Float(
        string='Jumlah Total Aset',
        required=True,
        help='Jumlah total aset perusahaan (dalam satuan mata uang lokal)'
    )

    total_expense_amount = fields.Float(
        string='Jumlah Total Beban',
        help='Jumlah beban perusahaan untuk kalkulasi cakupan scoping.'
    )

    total_liability_amount = fields.Float(
        string='Jumlah Total Liabilitas',
        help='Jumlah liabilitas perusahaan untuk kalkulasi cakupan scoping.'
    )

    # Group Materiality Multiplier (Table 25 SK BUMN)
    is_group_consolidation = fields.Boolean('Entitas Grup/Konsolidasian?')
    number_of_significant_locations = fields.Integer(
        string='Jumlah Lokasi/Entitas Signifikan',
        compute='_compute_significant_locations',
        store=True, readonly=False,
        help='Jumlah entitas signifikan untuk penentuan Multiplier (Tabel 25). '
             'Dihitung otomatis dari data Perusahaan yang dicentang "Lokasi Signifikan".'
    )

    @api.depends('is_group_consolidation')
    def _compute_significant_locations(self):
        for record in self:
            if record.is_group_consolidation:
                # Count companies marked as significant
                count = self.env['res.company'].search_count([('is_significant_location', '=', True)])
                record.number_of_significant_locations = count or 1
            else:
                record.number_of_significant_locations = 1

    group_multiplier = fields.Float(
        string='Multiplier Grup',
        compute='_compute_group_multiplier',
        help='Tingkat perkalian berdasarkan jumlah lokasi (Tabel 25)'
    )

    @api.depends('is_group_consolidation', 'number_of_significant_locations')
    def _compute_group_multiplier(self):
        """
        Logic Table 25: Penentuan Tingkat Perkalian (Multiplier)
        """
        for record in self:
            if not record.is_group_consolidation:
                record.group_multiplier = 1.0
                continue
            
            n = record.number_of_significant_locations
            if n <= 1: record.group_multiplier = 1.0
            elif n == 2: record.group_multiplier = 1.5
            elif 3 <= n <= 4: record.group_multiplier = 2.0
            elif 5 <= n <= 6: record.group_multiplier = 2.5
            elif 7 <= n <= 9: record.group_multiplier = 3.0
            elif 10 <= n <= 14: record.group_multiplier = 3.5
            elif 15 <= n <= 19: record.group_multiplier = 4.0
            elif 20 <= n <= 25: record.group_multiplier = 4.5
            elif 26 <= n <= 30: record.group_multiplier = 5.0
            elif 31 <= n <= 40: record.group_multiplier = 5.5
            elif 41 <= n <= 50: record.group_multiplier = 6.0
            elif 51 <= n <= 64: record.group_multiplier = 6.5
            elif 65 <= n <= 80: record.group_multiplier = 7.0
            elif 81 <= n <= 94: record.group_multiplier = 7.5
            elif 95 <= n <= 110: record.group_multiplier = 8.0
            elif 111 <= n <= 130: record.group_multiplier = 8.5
            else: record.group_multiplier = 9.0

    net_income_amount = fields.Float(
        string='Jumlah Laba Bersih',
        help='Jumlah laba bersih perusahaan (dalam satuan mata uang lokal)'
    )

    overall_materiality_percent = fields.Float(
        string='Persentase Overall Materiality',
        default=5.0,
        help='Persentase Overall Materiality (contoh: 5% dari Laba Sebelum Pajak)'
    )

    # Haircut / Risk Factors (Table 4 SK BUMN)
    history_audit_adjustment = fields.Boolean(
        string='Riwayat Audit Adjustment Signifikan',
        help='Apakah terdapat riwayat audit adjustment yang sering atau material?'
    )

    history_deficiencies = fields.Boolean(
        string='Riwayat Defisiensi (MW/SD)',
        help='Apakah terdapat riwayat Material Weakness atau Significant Deficiency?'
    )

    high_misstatement_risk = fields.Boolean(
        string='Risiko Salah Saji Tinggi',
        help='Potensi kesalahan penyajian > OM atau risiko fraud tinggi'
    )

    restatement_history = fields.Boolean(
        string='Riwayat Restatement',
        help='Apakah pernah terjadi penyajian kembali laporan keuangan (Restatement)?'
    )

    risk_factor_level = fields.Selection([
        ('low', 'Risiko Rendah (Haircut 20%)'),
        ('high', 'Risiko Tinggi (Haircut >55%)')
    ], string='Faktor Risiko (Kesimpulan)', compute='_compute_risk_factor_level', store=True, readonly=False,
       help='Tingkat risiko untuk menentukan haircut Performance Materiality (Tabel 4 Juknis)')

    performance_materiality_percent = fields.Float(
        string='Persentase Performance Materiality',
        default=45.0,
        help='Persentase PM dari OM (100% - Haircut). Risiko Rendah ~80%, Risiko Tinggi <45%'
    )

    @api.depends('history_audit_adjustment', 'history_deficiencies', 'high_misstatement_risk', 'restatement_history')
    def _compute_risk_factor_level(self):
        for record in self:
            # Logic: If ANY high risk factor is present -> High Risk
            if any([record.history_audit_adjustment, record.history_deficiencies, 
                    record.high_misstatement_risk, record.restatement_history]):
                record.risk_factor_level = 'high'
            else:
                record.risk_factor_level = 'low'

    @api.onchange('risk_factor_level')
    def _onchange_risk_factor(self):
        if self.risk_factor_level == 'low':
            self.performance_materiality_percent = 80.0  # 100% - 20% haircut
        elif self.risk_factor_level == 'high':
            self.performance_materiality_percent = 45.0  # 100% - 55% haircut (conservative)

    @api.onchange('materiality_basis')
    def _onchange_materiality_basis(self):
        """
        Set default percentage based on SK BUMN Table 3 guidelines:
        - Laba/Rugi sebelum Pajak: 5%
        - Pendapatan: 0.5% - 1% (Defaults to 1%)
        - Total Aset: 0.5% - 1% (Defaults to 1%)
        - Ekuitas: 1% (If applicable)
        """
        if self.materiality_basis == 'revenue':
            self.overall_materiality_percent = 1.0
        elif self.materiality_basis == 'total_assets':
            self.overall_materiality_percent = 1.0
        elif self.materiality_basis == 'net_income':
            self.overall_materiality_percent = 5.0
        # Hybrid or others keep existing or user input

    overall_materiality_amount = fields.Float(
        string='Jumlah Overall Materiality',
        compute='_compute_materiality_amounts',
        store=True,
        help='Jumlah Overall Materiality dalam satuan mata uang lokal'
    )

    performance_materiality_amount = fields.Float(
        string='Jumlah Performance Materiality',
        compute='_compute_materiality_amounts',
        store=True,
        help='Jumlah Performance Materiality dalam satuan mata uang lokal'
    )

    # Scoping Coverage Analysis (2/3 Rule - Table 6 Juknis)
    coverage_revenue_percent = fields.Float(
        string='Cakupan Pendapatan (%)',
        compute='_compute_coverage_ratios',
        help='Persentase cakupan akun pendapatan signifikan terhadap total pendapatan'
    )

    coverage_assets_percent = fields.Float(
        string='Cakupan Aset (%)',
        compute='_compute_coverage_ratios',
        help='Persentase cakupan akun aset signifikan terhadap total aset'
    )

    coverage_expenses_percent = fields.Float(
        string='Cakupan Beban (%)',
        compute='_compute_coverage_ratios',
        help='Persentase cakupan akun beban signifikan terhadap total beban'
    )

    coverage_liabilities_percent = fields.Float(
        string='Cakupan Liabilitas (%)',
        compute='_compute_coverage_ratios',
        help='Persentase cakupan akun liabilitas signifikan terhadap total liabilitas'
    )

    # Tabel 6 Juknis BUMN: Scoping Level Lokasi/Entitas
    coverage_locations_percent = fields.Float(
        string='Cakupan Lokasi (%)',
        compute='_compute_coverage_ratios',
        help='Persentase kontribusi aset/revenue dari lokasi signifikan terpilih terhadap total grup'
    )

    coverage_status = fields.Selection([
        ('pass', 'LULUS (>= 66.7%)'),
        ('fail', 'GAGAL (< 66.7%)')
    ], string='Status Cakupan (Aturan 2/3)', compute='_compute_coverage_ratios',
       help='Status pemenuhan kriteria kecukupan ruang lingkup sesuai Bab III Pasal 1.3 Juknis (Akun dan Lokasi)')

    @api.depends('account_mapping_ids.is_significant_account', 'account_mapping_ids.account_balance', 
                 'revenue_amount', 'total_assets_amount', 'is_group_consolidation')
    def _compute_coverage_ratios(self):
        for record in self:
            # 1. Account Coverage (Tabel 6: Minimal 2/3 nilai akun/FSLI)
            sig_accounts = record.account_mapping_ids.filtered(lambda x: x.is_significant_account)
            rev_mapped = sum(sig_accounts.filtered(lambda x: 'Revenue' in (x.fsl_item or '') or 'Pendapatan' in (x.fsl_item or '')).mapped('account_balance'))
            record.coverage_revenue_percent = (rev_mapped / record.revenue_amount * 100) if record.revenue_amount > 0 else 0
            
            asset_mapped = sum(sig_accounts.filtered(lambda x: 'Asset' in (x.fsl_item or '') or 'Aset' in (x.fsl_item or '') or 'Aktiva' in (x.fsl_item or '')).mapped('account_balance'))
            record.coverage_assets_percent = (asset_mapped / record.total_assets_amount * 100) if record.total_assets_amount > 0 else 0
            
            exp_mapped = sum(sig_accounts.filtered(lambda x: 'Expense' in (x.fsl_item or '') or 'Beban' in (x.fsl_item or '') or 'Biaya' in (x.fsl_item or '')).mapped('account_balance'))
            record.coverage_expenses_percent = (exp_mapped / record.total_expense_amount * 100) if record.total_expense_amount > 0 else 0

            lia_mapped = sum(sig_accounts.filtered(lambda x: 'Liability' in (x.fsl_item or '') or 'Liabilitas' in (x.fsl_item or '') or 'Kewajiban' in (x.fsl_item or '') or 'Utang' in (x.fsl_item or '')).mapped('account_balance'))
            record.coverage_liabilities_percent = (lia_mapped / record.total_liability_amount * 100) if record.total_liability_amount > 0 else 0

            # 2. Location Coverage (Bab III 1.3 - Tabel 6)
            # Menggunakan kontribusi finansial riil dari perusahaan, bukan sekadar jumlah (count).
            if record.is_group_consolidation:
                # FAQ 13: Entitas baru diakuisisi dikecualikan dari kewajiban evaluasi di tahun pertama.
                # Kita hanya menghitung entitas yang 'eligible' (bukan newly acquired).
                eligible_companies = self.env['res.company'].search([('is_newly_acquired', '=', False)])
                sig_companies = eligible_companies.filtered(lambda c: c.is_significant_location)
                
                # Hitung total kontribusi dari lokasi signifikan terpilih
                sig_revenue = sum(sig_companies.mapped('icofr_revenue_contribution'))
                sig_assets = sum(sig_companies.mapped('icofr_asset_contribution'))
                
                # Denominator adalah total eligible (bukan total absolut grup agar fair terhadap entitas baru)
                total_eligible_rev = sum(eligible_companies.mapped('icofr_revenue_contribution')) or record.revenue_amount
                total_eligible_assets = sum(eligible_companies.mapped('icofr_asset_contribution')) or record.total_assets_amount
                
                # Ambil nilai terendah antara cakupan aset dan revenue untuk status lokasi
                loc_rev_ratio = (sig_revenue / total_eligible_rev * 100) if total_eligible_rev > 0 else 0
                loc_asset_ratio = (sig_assets / total_eligible_assets * 100) if total_eligible_assets > 0 else 0
                record.coverage_locations_percent = min(loc_rev_ratio, loc_asset_ratio)
            else:
                record.coverage_locations_percent = 100.0

            # Overall Status (Must meet 2/3 threshold for ALL metrics)
            threshold = 66.67
            if (record.coverage_revenue_percent >= threshold and 
                record.coverage_assets_percent >= threshold and 
                record.coverage_expenses_percent >= threshold and
                record.coverage_liabilities_percent >= threshold and
                record.coverage_locations_percent >= threshold):
                record.coverage_status = 'pass'
            else:
                record.coverage_status = 'fail'

    materiality_basis = fields.Selection([
        ('revenue', 'Pendapatan'),
        ('total_assets', 'Total Aset'),
        ('net_income', 'Laba Bersih'),
        ('hybrid', 'Campuran')
    ], string='Basis Perhitungan', default='revenue',
       help='Basis utama untuk perhitungan materialitas')

    calculation_method = fields.Selection([
        ('percent_revenue', 'Persen dari Pendapatan'),
        ('percent_assets', 'Persen dari Total Aset'),
        ('percent_net_income', 'Persen dari Laba Bersih'),
        ('fixed_amount', 'Jumlah Tetap'),
        ('other', 'Lainnya')
    ], string='Metode Perhitungan', default='percent_revenue',
       help='Metode yang digunakan untuk menghitung materialitas')

    notes = fields.Text(
        string='Catatan Perhitungan',
        help='Catatan tentang perhitungan materialitas dan pertimbangan lainnya'
    )

    # Hal 16 Juknis BUMN: Dokumentasi Konsultasi Auditor Eksternal
    has_auditor_consultation = fields.Boolean(
        string='Sudah Diskusi dengan Auditor Eksternal?',
        help='Centang jika pendekatan materialitas telah didiskusikan dengan Auditor Eksternal sesuai Hal 16.'
    )
    auditor_consultation_date = fields.Date('Tanggal Konsultasi')
    auditor_consultation_notes = fields.Text('Catatan Masukan Auditor')

    active = fields.Boolean(
        string='Aktif',
        default=True,
        help='Status aktivasi dari kalkulasi materialitas'
    )

    account_mapping_ids = fields.One2many(
        'icofr.account.mapping',
        'materiality_id',
        string='Pemetaan Akun',
        help='Pemetaan akun ke FSLI (Financial Statement Line Item)'
    )

    # Hal 115: Aturan Alokasi Materialitas Grup
    parent_materiality_id = fields.Many2one(
        'icofr.materiality', 
        string='Materialitas Grup (Induk)',
        domain="[('is_group_consolidation', '=', True), ('fiscal_year', '=', fiscal_year)]",
        help='Referensi ke perhitungan materialitas tingkat grup untuk validasi alokasi.'
    )

    @api.constrains('overall_materiality_amount', 'parent_materiality_id')
    def _check_group_allocation_limit(self):
        """
        Hal 115 Juknis BUMN: Nilai alokasi materialitas dari masing-masing 
        Lokasi/Perusahaan tidak boleh melebihi nilai OM Grup.
        """
        for record in self:
            if record.parent_materiality_id:
                group_om = record.parent_materiality_id.overall_materiality_amount
                if record.overall_materiality_amount > group_om:
                    raise ValidationError(
                        f"Sesuai Juknis BUMN Hal 115, Overall Materiality entitas (Rp {record.overall_materiality_amount:,.0f}) "
                        f"TIDAK BOLEH melebihi Overall Materiality Grup (Rp {group_om:,.0f})!"
                    )

    @api.depends('revenue_amount', 'total_assets_amount', 'net_income_amount',
                 'overall_materiality_percent', 'performance_materiality_percent',
                 'materiality_basis')
    def _compute_materiality_amounts(self):
        for record in self:
            # Calculate overall materiality amount based on selected basis
            if record.materiality_basis == 'revenue':
                base_amount = record.revenue_amount
            elif record.materiality_basis == 'total_assets':
                base_amount = record.total_assets_amount
            elif record.materiality_basis == 'net_income':
                base_amount = record.net_income_amount or record.total_assets_amount
            else:  # hybrid - use largest value
                base_amount = max(record.revenue_amount, record.total_assets_amount,
                                 record.net_income_amount or 0)

            record.overall_materiality_amount = base_amount * (record.overall_materiality_percent / 100)
            record.performance_materiality_amount = record.overall_materiality_amount * (record.performance_materiality_percent / 100)

    @api.model
    def create(self, vals):
        # Handle both single and batch creation
        if isinstance(vals, list):
            # Process each item in the list
            processed_vals = []
            for val_dict in vals:
                new_val_dict = val_dict.copy()
                if 'name' not in new_val_dict or not new_val_dict.get('name'):
                    fiscal_year = new_val_dict.get('fiscal_year', fields.Date.today().year)
                    company_id = new_val_dict.get('company_id', '')
                    new_val_dict['name'] = f'Materialitas {fiscal_year} - {company_id}'
                processed_vals.append(new_val_dict)
            return super(IcofrMateriality, self).create(processed_vals)
        else:
            # Single record creation
            new_vals = vals.copy()
            if 'name' not in new_vals or not new_vals.get('name'):
                fiscal_year = new_vals.get('fiscal_year', fields.Date.today().year)
                company_id = new_vals.get('company_id', '')
                new_vals['name'] = f'Materialitas {fiscal_year} - {company_id}'
            return super(IcofrMateriality, self).create(new_vals)

    def action_allocate_to_subsidiaries(self):
        """
        Hal 115 Juknis BUMN: Menghitung alokasi materialitas secara proporsional 
        berdasarkan total aset masing-masing Lokasi/Perusahaan signifikan.
        """
        self.ensure_one()
        if not self.is_group_consolidation:
            raise ValidationError("Fitur alokasi hanya tersedia untuk entitas tingkat Grup/Konsolidasian.")

        # Cari anak perusahaan (lokasi signifikan)
        subsidiaries = self.env['res.company'].search([
            ('is_significant_location', '=', True),
            ('id', '!=', self.company_id.id)
        ])
        
        if not subsidiaries:
            raise ValidationError("Tidak ditemukan anak perusahaan yang ditandai sebagai Lokasi Signifikan.")

        total_group_assets = sum(subsidiaries.mapped('icofr_asset_contribution'))
        if total_group_assets <= 0:
            raise ValidationError("Total aset kontribusi anak perusahaan harus lebih besar dari nol untuk kalkulasi proporsional.")

        # Nilai maksimal yang boleh dialokasikan (Group OM * Multiplier)
        total_allocatable_om = self.overall_materiality_amount * self.group_multiplier
        
        results = []
        for sub in subsidiaries:
            # Hitung proporsi
            porsi = sub.icofr_asset_contribution / total_group_assets
            allocated_om = total_allocatable_om * porsi
            
            # Pastikan tidak melebihi Group OM absolut (Hal 115 poin a)
            final_om = min(allocated_om, self.overall_materiality_amount)
            
            # Cari atau buat record materiality untuk anak perusahaan
            sub_mat = self.env['icofr.materiality'].search([
                ('company_id', '=', sub.id),
                ('fiscal_year', '=', self.fiscal_year),
                ('active', '=', True)
            ], limit=1)
            
            vals = {
                'company_id': sub.id,
                'fiscal_year': self.fiscal_year,
                'parent_materiality_id': self.id,
                'total_assets_amount': sub.icofr_asset_contribution,
                'revenue_amount': sub.icofr_revenue_contribution,
                'overall_materiality_amount': final_om,
                'materiality_basis': 'hybrid',
                'notes': f'Alokasi otomatis dari Grup {self.company_id.name} (Proporsi Aset: {porsi*100:.2f}%)'
            }
            
            if sub_mat:
                sub_mat.write(vals)
            else:
                self.env['icofr.materiality'].create(vals)
            
            results.append(f"{sub.name}: Rp {final_om:,.0f}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Alokasi Materialitas Selesai',
                'message': f'Berhasil mengalokasikan ke {len(subsidiaries)} entitas:\n' + '\n'.join(results),
                'type': 'success',
            }
        }

    def action_calculate_materiality(self):
        """Method untuk mengkalkulasi ulang materialitas jika ada perubahan data"""
        self._compute_materiality_amounts()
        return True

    def action_export_materiality(self):
        """Method untuk mengekspor data materialitas"""
        # Placeholder for export functionality
        # In a real implementation, this would export the materiality data
        # to a file in various formats (Excel, PDF, etc.)
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/binary/download_document/{self.id}/icofr.materiality/export',
            'target': 'new',
        }


    def action_update_balances_from_erp(self):
        """Memperbarui seluruh saldo akun yang terpetakan dari sistem ERP Odoo"""
        self.ensure_one()
        for mapping in self.account_mapping_ids:
            if mapping.account_gl_id:
                mapping.action_refresh_balance()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sinkronisasi ERP Selesai',
                'message': 'Seluruh saldo akun yang terhubung telah diperbarui.',
                'type': 'success',
            }
        }

    def action_pull_financial_data_from_erp(self):
        """Pull financial data (revenue, assets, net income) from Odoo's accounting modules"""
        self.ensure_one()

        # Create context with fiscal year range
        fiscal_year = self.fiscal_year
        if not fiscal_year or len(str(fiscal_year)) != 4:
            raise ValidationError(f"Format tahun fiskal '{fiscal_year}' tidak valid. Format yang benar: YYYY")

        date_from = f"{fiscal_year}-01-01"
        date_to = f"{fiscal_year}-12-31"

        # Context untuk periode fiskal
        ctx = dict(self.env.context)
        ctx.update({
            'date_from': date_from,
            'date_to': date_to,
            'company_id': self.company_id.id,
            'all_entries': True,
            'state': 'posted',  # hanya entri yang sudah diposting
            'fiscalyear': True,
        })

        # Pull revenue (pendapatan) - typically from income accounts
        revenue_accounts = self.env['account.account'].with_context(ctx).search([
            ('user_type_id.type', '=', 'other'),
            ('user_type_id.name', 'like', '%Revenue%'),
            ('company_id', '=', self.company_id.id)
        ])

        total_revenue = sum(acc.balance for acc in revenue_accounts)

        # Pull assets (aset) - from asset accounts
        asset_accounts = self.env['account.account'].with_context(ctx).search([
            ('user_type_id.type', '=', 'other'),
            ('user_type_id.name', 'like', '%Asset%'),
            ('company_id', '=', self.company_id.id)
        ])

        total_assets = sum(acc.balance for acc in asset_accounts)

        # Alternative approach: Get specific account types
        # For assets, we might need to be more specific
        account_types = self.env['account.account.type'].search([
            ('name', 'in', ['Assets', 'Asset', 'Aktiva'])
        ])
        specific_asset_accounts = self.env['account.account'].with_context(ctx).search([
            ('user_type_id', 'in', account_types.ids),
            ('company_id', '=', self.company_id.id)
        ])

        specific_assets = sum(acc.balance for acc in specific_asset_accounts)

        # Pull net income - from profit and loss accounts or Retained Earnings
        # Calculate by getting income and expense accounts
        income_accounts = self.env['account.account'].with_context(ctx).search([
            ('user_type_id.type', '=', 'other'),
            ('user_type_id.name', 'in', ['Income', 'Revenue', 'Pendapatan']),
            ('company_id', '=', self.company_id.id)
        ])

        expense_accounts = self.env['account.account'].with_context(ctx).search([
            ('user_type_id.type', '=', 'other'),
            ('user_type_id.name', 'in', ['Expense', 'Beban', 'Biaya']),
            ('company_id', '=', self.company_id.id)
        ])

        total_income = sum(acc.balance for acc in income_accounts if acc.balance > 0) + sum(abs(acc.balance) for acc in income_accounts if acc.balance < 0)
        total_expenses = sum(acc.balance for acc in expense_accounts if acc.balance > 0) + sum(abs(acc.balance) for acc in expense_accounts if acc.balance < 0)

        net_income = total_income - total_expenses

        # Update the materiality record with pulled data
        self.write({
            'revenue_amount': abs(total_revenue),
            'total_assets_amount': abs(total_assets + specific_assets),  # Use the higher accuracy
            'net_income_amount': abs(net_income)
        })

        # Recalculate materiality amounts
        self._compute_materiality_amounts()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Data Keuangan Terambil',
                'message': f'Data keuangan berhasil diambil dari sistem ERP:\n'
                          f'Pendapatan: {total_revenue:,.2f}\n'
                          f'Aset: {total_assets + specific_assets:,.2f}\n'
                          f'Laba Bersih: {net_income:,.2f}',
                'type': 'success',
            }
        }

    def action_import_financial_data_from_excel(self, excel_file, file_name):
        """
        Import financial data from Excel file
        """
        self.ensure_one()

        if not excel_file:
            raise ValidationError("Silakan pilih file Excel terlebih dahulu.")

        if not file_name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Hanya file Excel (.xlsx atau .xls) yang diperbolehkan.")

        try:
            # Decode file Excel
            decoded_file = base64.b64decode(excel_file)
            import xlrd
            from io import BytesIO
            workbook = xlrd.open_workbook(file_contents=decoded_file)
            worksheet = workbook.sheet_by_index(0)

            # Baca header dari baris pertama
            headers = [str(worksheet.cell_value(0, col)).strip() for col in range(worksheet.ncols)]

            # Validasi header
            required_headers = ['Tahun Fiskal', 'Pendapatan', 'Total Aset']
            for header in required_headers:
                if header not in headers:
                    raise ValidationError(f'Header "{header}" tidak ditemukan dalam file Excel. '
                                          f'Header yang diperlukan: {", ".join(required_headers)}')

            # Proses baris data (mulai dari baris ke-1 karena baris ke-0 adalah header)
            import_result = {
                'created': 0,
                'updated': 0,
                'errors': []
            }

            # Hanya proses baris pertama setelah header
            for row_idx in range(1, min(worksheet.nrows, 2)):  # Batasi hanya 1 baris data
                try:
                    row_data = [worksheet.cell_value(row_idx, col) for col in range(worksheet.ncols)]

                    # Konversi ke dictionary
                    row_dict = dict(zip(headers, row_data))

                    # Ambil data dari Excel
                    fiscal_year = str(int(row_dict.get('Tahun Fiskal', ''))).strip()
                    revenue = float(row_dict.get('Pendapatan', 0))
                    total_assets = float(row_dict.get('Total Aset', 0))
                    net_income = float(row_dict.get('Laba Bersih', 0)) if row_dict.get('Laba Bersih') else 0.0

                    # Ambil parameter tambahan jika tersedia
                    om_percent = float(row_dict.get('Persentase Overall Materiality', 0.5)) if row_dict.get('Persentase Overall Materiality') else 0.5
                    pm_percent = float(row_dict.get('Persentase Performance Materiality', 75)) if row_dict.get('Persentase Performance Materiality') else 75
                    materiality_basis = str(row_dict.get('Basis Perhitungan', 'revenue')).strip() if row_dict.get('Basis Perhitungan') else 'revenue'

                    # Validasi data
                    if not fiscal_year or len(fiscal_year) != 4 or not fiscal_year.isdigit():
                        raise ValidationError(f'Format Tahun Fiskal tidak valid di baris {row_idx + 1}. Harus format YYYY.')

                    # Update data pada record materiality
                    update_data = {
                        'fiscal_year': fiscal_year,
                        'revenue_amount': revenue,
                        'total_assets_amount': total_assets,
                        'net_income_amount': net_income,
                        'overall_materiality_percent': om_percent,
                        'performance_materiality_percent': pm_percent,
                        'materiality_basis': materiality_basis,
                    }

                    self.write(update_data)

                    # Recalculate materiality amounts
                    self._compute_materiality_amounts()

                    import_result['updated'] += 1

                except Exception as e:
                    import_result['errors'].append(f'Baris {row_idx + 1}: Error saat memproses data - {str(e)}')

            # Return hasil import
            result_message = f"Import data keuangan selesai:\n"
            result_message += f"- Jumlah record diperbarui: {import_result['updated']}\n"

            if import_result['errors']:
                result_message += f"- Jumlah error: {len(import_result['errors'])}\n"
                result_message += "Daftar error:\n" + "\n".join(f"  - {err}" for err in import_result['errors'])

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Import Data Keuangan Selesai',
                    'message': result_message,
                    'type': 'success' if not import_result['errors'] else 'warning',
                }
            }

        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f"Error saat membaca file Excel: {str(e)}")