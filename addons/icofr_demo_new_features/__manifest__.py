# -*- coding: utf-8 -*-
{
    'name': 'ICORF Demo New Features',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Demo data for new features in ICORF (Internal Controls Over Financial Reporting) module',
    'description': """
ICORF Demo New Features Module
================================

This module provides sample data for demonstrating the NEW features added to the ICORF (Internal Controls Over Financial Reporting) functionality.

Based on the comprehensive demo scenarios, this module includes:
- Sample materiality calculations
- Sample account mappings with GL to FSLI mappings
- Sample CSA (Control Self-Assessment) records
- Sample deficiency classifications
- Sample copy period usage
- Sample Three Lines of Defense role assignments
- All data follows scenarios 12-16 in the ICORF Demo Scenarios document
    """,
    'author': 'Your Organization',
    'depends': [
        'icofr',
        'icofr_demo',
        'base',
    ],
    'data': [
        'icofr_demo_new_features_data.xml',
    ],
    'demo': [
        'icofr_demo_new_features_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}