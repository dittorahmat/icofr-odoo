# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IcofrCosoMapping(models.Model):
    _name = 'icofr.coso.mapping'
    _description = 'Matriks Pemetaan Prinsip COSO'
    _auto = False # Use SQL View for matrix

    principle_code = fields.Char('Kode Prinsip')
    principle_name = fields.Char('Nama Prinsip')
    component_name = fields.Char('Komponen COSO')
    control_count = fields.Integer('Jumlah Kontrol Terpetakan')
    
    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW icofr_coso_mapping AS (
                SELECT 
                    ce.id as id,
                    ce.code as principle_code,
                    ce.name as principle_name,
                    cp.name as component_name,
                    (SELECT count(*) FROM icofr_control WHERE coso_element_id = ce.id AND status = 'active') as control_count
                FROM 
                    icofr_coso_element ce
                LEFT JOIN 
                    icofr_coso_element cp ON ce.parent_id = cp.id
                WHERE 
                    ce.is_sub_element = true
            )
        """)
