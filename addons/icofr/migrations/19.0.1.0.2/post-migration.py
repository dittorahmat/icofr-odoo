# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Post-migration script to update company_id values in icofr_csa table if needed"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Update all existing records to have the current company if null
    cr.execute("""
        UPDATE icofr_csa SET company_id = %s WHERE company_id IS NULL OR company_id = 0
    """, (env.company.id,))