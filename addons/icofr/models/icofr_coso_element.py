# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IcofrCosoElement(models.Model):
    _name = 'icofr.coso.element'
    _description = 'Elemen Kerangka COSO 2013'
    _order = 'sequence'

    name = fields.Char(
        string='Nama Elemen COSO',
        required=True,
        help='Nama dari elemen dalam kerangka COSO 2013'
    )

    code = fields.Char(
        string='Kode Elemen',
        required=True,
        copy=False,
        help='Kode singkat untuk identifikasi elemen COSO'
    )

    description = fields.Text(
        string='Deskripsi Elemen',
        help='Deskripsi lengkap dari elemen COSO 2013'
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
        help='Urutan tampilan elemen dalam daftar'
    )

    parent_id = fields.Many2one(
        'icofr.coso.element',
        string='Sub-Elemen dari',
        help='Jika ini adalah sub-elemen dari elemen lain'
    )

    child_ids = fields.One2many(
        'icofr.coso.element',
        'parent_id',
        string='Sub-Elemen',
        help='Sub-elemen dari elemen ini'
    )

    control_ids = fields.One2many(
        'icofr.control',
        'coso_element_id',
        string='Kontrol Terkait',
        help='Kontrol-kontrol yang terkait dengan elemen COSO ini'
    )

    is_sub_element = fields.Boolean(
        string='Adalah Sub-Elemen',
        compute='_compute_is_sub_element',
        store=True,
        help='Menandai apakah ini adalah sub-elemen dari elemen COSO lain'
    )

    @api.depends('parent_id')
    def _compute_is_sub_element(self):
        for record in self:
            record.is_sub_element = bool(record.parent_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Generate code if not provided
            if 'code' not in vals or not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('icofr.coso.element') or '/'
        return super(IcofrCosoElement, self).create(vals_list)