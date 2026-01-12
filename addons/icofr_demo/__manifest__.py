# -*- coding: utf-8 -*-
{
    'name': 'ICORF Demo Data',
    'version': '1.0',
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
    ],
    'demo': [
        'icofr_demo_data.xml',
        'data/icofr_coso_demo_mapping.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}