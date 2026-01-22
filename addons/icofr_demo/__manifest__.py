# -*- coding: utf-8 -*-
{
    'name': 'ICORF Demo Data',
    'version': '1.1.0',
    'category': 'Accounting',
    'summary': 'Demo data for ICORF (Internal Controls Over Financial Reporting) module',
    'description': """
ICORF Demo Data Module
========================

This module provides sample data for demonstrating the ICORF (Internal Controls Over Financial Reporting) functionality.

Based on the comprehensive demo scenarios, this module includes:
- Sample business processes
- Sample risks and controls
- Sample testing schedules and results
- Sample certifications
- Sample findings and action plans
- Calendar events and reporting data

All data follows the scenarios outlined in the ICORF Demo Scenarios document,
providing a realistic demonstration of the system for training and evaluation purposes.
    """,
    'author': 'Your Organization',
    'depends': [
        'icofr',
        'base',
    ],
    'data': [
        'icofr_demo_data.xml',
        'data/icofr_demo_workflow.xml',
        'data/icofr_banking_demo_data.xml',
        'data/icofr_missing_features_demo.xml',
        'data/icofr_demo_industry_clusters.xml',
        'data/icofr_demo_industry_clusters_v2.xml',
        'data/gl_mapping_import.xml',
        'data/qualitative_scoping_demo.xml',
        'data/holding_scoping_demo.xml',
        'data/remediation_demo.xml',
        'data/service_org_demo.xml',
        'data/elc_aggregated_demo.xml',
        'data/icofr_missing_features_demo.xml',
    ],
    'demo': [
        'icofr_demo_data.xml',
        'data/icofr_coso_demo_mapping.xml',
        'data/icofr_missing_features_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}