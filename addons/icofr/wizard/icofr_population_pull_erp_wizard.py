# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IcofrPopulationPullErpWizard(models.TransientModel):
    """
    Wizard to pull transaction data from Odoo's account.move.line into ICOFR Audit Population.
    This fulfills the requirement for advanced audit sampling integration.
    """
    _name = 'icofr.population.pull.erp.wizard'
    _description = 'Wizard Tarik Data Transaksi ERP untuk Populasi'

    control_id = fields.Many2one(
        'icofr.control',
        string='Kontrol Terkait',
        required=True
    )

    testing_id = fields.Many2one(
        'icofr.testing',
        string='Pengujian Terkait',
        domain="[('control_id', '=', control_id)]"
    )

    date_from = fields.Date(
        string='Dari Tanggal',
        required=True,
        default=lambda self: fields.Date.today().replace(month=1, day=1)
    )

    date_to = fields.Date(
        string='Sampai Tanggal',
        required=True,
        default=fields.Date.today()
    )

    account_ids = fields.Many2many(
        'account.account',
        string='Akun GL',
        help='Pilih satu atau lebih akun GL untuk menarik transaksi'
    )

    journal_ids = fields.Many2many(
        'account.journal',
        string='Jurnal',
        help='Filter berdasarkan jurnal tertentu (opsional)'
    )

    min_amount = fields.Float(
        string='Nilai Minimum',
        help='Hanya tarik transaksi dengan nilai lebih besar dari angka ini'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        required=True,
        default=lambda self: self.env.company
    )

    def action_pull_data(self):
        self.ensure_one()
        
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('company_id', '=', self.company_id.id),
            ('parent_state', '=', 'posted')
        ]

        if self.account_ids:
            domain.append(('account_id', 'in', self.account_ids.ids))
        
        if self.journal_ids:
            domain.append(('journal_id', 'in', self.journal_ids.ids))
        
        if self.min_amount:
            domain.append(('balance', '!=', 0)) # Basic check
            # For amount, we usually care about the absolute value of the debit/credit
            # But domain doesn't support abs() easily. We'll filter in loop if needed or use simple logic.

        move_lines = self.env['account.move.line'].search(domain)
        
        if not move_lines:
            raise UserError(_('Tidak ditemukan transaksi pada kriteria tersebut.'))

        population_model = self.env['icofr.audit.population']
        count = 0
        
        for line in move_lines:
            # Filter by amount if specified
            amount = abs(line.balance)
            if self.min_amount and amount < self.min_amount:
                continue
                
            # Check if already imported
            existing = population_model.search([
                ('transaction_no', '=', line.move_id.name),
                ('control_id', '=', self.control_id.id)
            ], limit=1)
            
            if existing:
                continue

            population_model.create({
                'transaction_no': line.move_id.name,
                'transaction_date': line.date,
                'amount': amount,
                'description': f"{line.move_id.ref or ''} - {line.name or ''}".strip(' -'),
                'control_id': self.control_id.id,
                'testing_id': self.testing_id.id if self.testing_id else False,
                'company_id': self.company_id.id,
                'uploaded_by_id': self.env.user.id,
                'notes': _('Ditarik otomatis dari ERP (Account: %s)') % line.account_id.display_name
            })
            count += 1

        # Update population size in testing if linked
        if self.testing_id:
            total_pop = population_model.search_count([('control_id', '=', self.control_id.id)])
            self.testing_id.write({'population_size': total_pop})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Data Berhasil Ditarik'),
                'message': _('Berhasil menarik %s transaksi ke dalam populasi.') % count,
                'type': 'success',
            }
        }
