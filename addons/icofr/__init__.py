# -*- coding: utf-8 -*-
from . import models
from . import wizard


def post_init_hook(env):
    """Post-initialization hook to ensure proper data after module installation"""
    # Add the company_id column if it doesn't already exist in the database
    env.cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'icofr_csa' AND column_name = 'company_id'
    """)

    if not env.cr.fetchone():
        # Add the company_id column if it doesn't already exist
        env.cr.execute("""
            ALTER TABLE icofr_csa ADD COLUMN company_id INTEGER DEFAULT 1
        """)

    # Set default company for any remaining records without company_id
    env.cr.execute("""
        UPDATE icofr_csa SET company_id = %s WHERE company_id IS NULL OR company_id = 0
    """, [1])  # Using default company ID 1