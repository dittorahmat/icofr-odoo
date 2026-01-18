# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools

class IcofrItgcMapping(models.Model):
    _name = 'icofr.itgc.mapping'
    _description = 'Matriks Pemetaan ITGC vs COBIT 2019'
    _auto = False
    _order = 'cobit_code'

    cobit_id = fields.Many2one('icofr.cobit.element', string='Objektif COBIT 2019', readonly=True)
    cobit_code = fields.Char(string='Kode COBIT', readonly=True)
    cobit_name = fields.Char(string='Nama Objektif', readonly=True)
    
    # Area ITGC (Booleans based on Table 1)
    is_required_prog_dev = fields.Boolean('Wajib: Prog Dev', readonly=True)
    is_required_prog_change = fields.Boolean('Wajib: Prog Changes', readonly=True)
    is_required_comp_ops = fields.Boolean('Wajib: Comp Ops', readonly=True)
    is_required_access_data = fields.Boolean('Wajib: Access Data', readonly=True)

    # Coverage Status (Count of controls)
    ctrl_count_prog_dev = fields.Integer('Jml Kontrol: Prog Dev', readonly=True)
    ctrl_count_prog_change = fields.Integer('Jml Kontrol: Prog Changes', readonly=True)
    ctrl_count_comp_ops = fields.Integer('Jml Kontrol: Comp Ops', readonly=True)
    ctrl_count_access_data = fields.Integer('Jml Kontrol: Access Data', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                WITH cobit_ref AS (
                    SELECT id, code, name
                    FROM icofr_cobit_element
                    WHERE code IN (
                        'APO09', 'APO10', 'APO13', 'BAI02', 'BAI03', 'BAI04', 
                        'BAI06', 'BAI07', 'BAI10', 'DSS01', 'DSS02', 'DSS03', 
                        'DSS04', 'DSS05', 'DSS06'
                    )
                ),
                table_1_logic AS (
                    SELECT 
                        id as cobit_id,
                        code as cobit_code,
                        name as cobit_name,
                        -- Logic Table 1 Page 16
                        (code IN ('APO09', 'APO10', 'BAI02', 'BAI03', 'BAI04', 'BAI07', 'DSS01', 'DSS02')) as is_required_prog_dev,
                        (code IN ('APO09', 'APO10', 'BAI02', 'BAI03', 'BAI04', 'BAI06', 'BAI07', 'BAI10', 'DSS02')) as is_required_prog_change,
                        (code IN ('APO09', 'APO10', 'APO13', 'BAI06', 'BAI07', 'BAI10', 'DSS01', 'DSS02', 'DSS03', 'DSS04', 'DSS05', 'DSS06')) as is_required_comp_ops,
                        (code IN ('APO09', 'APO10', 'APO13', 'BAI06', 'BAI07', 'BAI10', 'DSS01', 'DSS04', 'DSS05', 'DSS06')) as is_required_access_data
                    FROM cobit_ref
                )
                SELECT 
                    t.cobit_id as id,
                    t.cobit_id,
                    t.cobit_code,
                    t.cobit_name,
                    t.is_required_prog_dev,
                    t.is_required_prog_change,
                    t.is_required_comp_ops,
                    t.is_required_access_data,
                    (SELECT count(c.id) FROM icofr_control c 
                     JOIN icofr_control_cobit_rel rel ON c.id = rel.control_id 
                     WHERE rel.cobit_element_id = t.cobit_id AND c.itgc_area = 'prog_dev' AND c.status = 'active') as ctrl_count_prog_dev,
                    (SELECT count(c.id) FROM icofr_control c 
                     JOIN icofr_control_cobit_rel rel ON c.id = rel.control_id 
                     WHERE rel.cobit_element_id = t.cobit_id AND c.itgc_area = 'prog_change' AND c.status = 'active') as ctrl_count_prog_change,
                    (SELECT count(c.id) FROM icofr_control c 
                     JOIN icofr_control_cobit_rel rel ON c.id = rel.control_id 
                     WHERE rel.cobit_element_id = t.cobit_id AND c.itgc_area = 'comp_ops' AND c.status = 'active') as ctrl_count_comp_ops,
                    (SELECT count(c.id) FROM icofr_control c 
                     JOIN icofr_control_cobit_rel rel ON c.id = rel.control_id 
                     WHERE rel.cobit_element_id = t.cobit_id AND c.itgc_area = 'access_data' AND c.status = 'active') as ctrl_count_access_data
                FROM table_1_logic t
            )
        """ % self._table)
