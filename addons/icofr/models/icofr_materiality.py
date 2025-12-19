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

    net_income_amount = fields.Float(
        string='Jumlah Laba Bersih',
        help='Jumlah laba bersih perusahaan (dalam satuan mata uang lokal)'
    )

    overall_materiality_percent = fields.Float(
        string='Persentase Overall Materiality',
        default=0.5,
        help='Persentase Overall Materiality (contoh: 0.5%)'
    )

    performance_materiality_percent = fields.Float(
        string='Persentase Performance Materiality',
        default=0.75,
        help='Persentase Performance Materiality sebagai faktor dari Overall Materiality (contoh: 75%)'
    )

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