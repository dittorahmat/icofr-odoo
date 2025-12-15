{
    "name": "ICORF (Internal Controls Over Financial Reporting)",
    "version": "19.0.1.0.1",
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
        # Security
        "security/ir.model.access.csv",

        # Views
        "views/icofr_menu.xml",
        "views/control_views.xml",
        "views/risk_views.xml",
        "views/testing_views.xml",
        "views/certification_views.xml",
        "views/workflow_views.xml",
        "views/calendar_views.xml",
        "views/coso_element_views.xml",
        "views/materiality_views.xml",
        "views/pojk_report_views.xml",
        "views/csa_views.xml",
        "views/copy_period_wizard_views.xml",
        "views/schedule_views.xml",
        "views/finding_views.xml",
        "views/workflow_integration_views.xml",
        "views/report_export_views.xml",
        "views/export_views.xml",
        "views/dashboard_views.xml",
        "views/reporting_views.xml",
        "views/icofr_process_views.xml",

        # Data
        "data/icofr_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}