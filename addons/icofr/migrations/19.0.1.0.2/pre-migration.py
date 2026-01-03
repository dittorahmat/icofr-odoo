# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Migration script to add company_id column to icofr_csa table"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Add the company_id column to the database table if it doesn't exist
    cr.execute("""
        ALTER TABLE icofr_csa ADD COLUMN IF NOT EXISTS company_id INTEGER
    """)
    
    # Set default company for existing records
    cr.execute("""
        UPDATE icofr_csa SET company_id = %s WHERE company_id IS NULL
    """, (env.company.id,))