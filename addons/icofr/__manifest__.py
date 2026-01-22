{
    "name": "ICORF (Internal Controls Over Financial Reporting)",
    "version": "19.0.1.2.0",
    "category": "Accounting",
    "summary": "Modul untuk mengelola Internal Controls Over Financial Reporting sesuai POJK 15/2024",
    "description": """
Modul ini menyediakan sistem untuk mengelola Internal Controls Over Financial Reporting (ICORF)
sesuai dengan standar COSO 2013 dan regulasi POJK No. 15 Tahun 2024 tentang Integritas
Pelaporan Keuangan Bank. Modul ini mendukung proses dokumentasi, pengujian, pelaporan,
dan sertifikasi kontrol internal atas pelaporan keuangan.
    """,
    "author": "ICORF Development Team",
    "website": "https://www.icofr-system.com",
    "depends": [
        "base",
        "account",
        "mail",
        "web",
    ],
    "data": [
        # Data
        "data/icofr_data.xml",
        "data/icofr_coso_data.xml",
        "data/icofr_cobit_data.xml",
        "data/icofr_industry_data.xml",
        "data/icofr_industry_risk_data.xml",
        "data/icofr_faq_data.xml",

        # Security
        "security/security.xml",
        "security/ir.model.access.csv",

        # Actions
        "views/line_report_actions.xml",
        "views/cobit_element_actions.xml",
        "views/additional_actions.xml",
        "views/csa_campaign_actions.xml",
        "views/icofr_new_feature_actions.xml",
        "views/audit_population_actions.xml",

        # Wizards
        "views/account_mapping_upload_wizard_views.xml",
        "views/master_data_upload_wizard_views.xml",
        "views/rcm_upload_wizard_views.xml",
        "views/sample_selection_wizard_views.xml",
        "views/financial_data_import_wizard_views.xml",
        "views/population_pull_erp_wizard_views.xml",
        "views/copy_period_wizard_views.xml",
        "wizard/icofr_test_roll_forward_wizard_views.xml",
        "wizard/icofr_remediation_report_wizard_views.xml",

        # Views
        "views/audit_population_views.xml",
        "views/disclosure_views.xml",
        "views/icofr_menu.xml",
        "views/control_views.xml",
        "views/application_views.xml",
        "views/risk_views.xml",
        "views/icofr_risk_heatmap_views.xml",
        "views/testing_views.xml",
        "views/certification_views.xml",
        "views/workflow_views.xml",
        "views/calendar_views.xml",
        "views/coso_element_views.xml",
        "views/coso_mapping_views.xml",
        "views/itgc_mapping_views.xml",
        "views/materiality_views.xml",
        "views/company_scoping_views.xml",
        "views/pojk_report_views.xml",
        "views/csa_views.xml",
        "views/schedule_views.xml",
        "views/finding_views.xml",
        "views/finding_group_views.xml",
        "views/workflow_integration_views.xml",
        "views/report_export_views.xml",
        "views/export_views.xml",
        "views/dashboard_views.xml",
        "views/reporting_views.xml",
        "views/icofr_process_views.xml",
        "views/cobit_element_views.xml",
        "views/notification_scheduler_views.xml",
        "views/line_report_views.xml",
        "views/csa_campaign_views.xml",
        "views/new_features_views.xml",
        "views/icofr_wbs_views.xml",
        "views/additional_compliance_views.xml",
        "views/icofr_registers_views.xml",
        "views/elc_assessment_views.xml",
        "views/audit_dossier_views.xml",
        "views/ipe_euc_dashboard_views.xml",
        "views/service_organization_views.xml",

        # Reports
        "reports/icofr_dod_report.xml",
        "reports/icofr_line3_report.xml",
        "reports/icofr_remediation_report.xml",
        "reports/icofr_statement_letter_report.xml",

        # Data
        "data/account_mapping_upload_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
    "post_init_hook": "post_init_hook",
}