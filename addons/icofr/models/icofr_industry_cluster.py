# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrIndustryCluster(models.Model):
    _name = 'icofr.industry.cluster'
    _description = 'Klaster Industri BUMN'
    _order = 'sequence, name'

    name = fields.Char('Nama Klaster', required=True, translate=True)
    code = fields.Char('Kode Klaster', required=True)
    sequence = fields.Integer('Urutan', default=10)
    description = fields.Text('Deskripsi Klaster')
    
    risk_ids = fields.One2many('icofr.risk', 'industry_cluster_id', string='Contoh Risiko Terkait')
    
    # _sql_constraints = [
    #     ('code_unique', 'unique(code)', 'Kode klaster harus unik!')
    # ]
