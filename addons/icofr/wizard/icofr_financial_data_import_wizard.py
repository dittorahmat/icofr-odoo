# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64

class IcofrFinancialDataImportWizard(models.TransientModel):
    _name = 'icofr.financial.data.import.wizard'
    _description = 'Wizard Import Data Keuangan dari Excel'

    materiality_id = fields.Many2one('icofr.materiality', string='Kalkulasi Materialitas', required=True)
    excel_file = fields.Binary(string='File Excel', required=True)
    file_name = fields.Char(string='Nama File')

    def action_import_excel(self):
        self.ensure_one()
        return self.materiality_id.action_import_financial_data_from_excel(self.excel_file, self.file_name)
