# Qwen Code Context File - ICORF Module for Odoo

## Project Overview

This is an Odoo module project for **ICORF (Internal Controls Over Financial Reporting)**, a comprehensive system designed to help organizations, especially financial institutions and state-owned enterprises (BUMN) in Indonesia, comply with POJK No. 15 Tahun 2024 regulations regarding Financial Reporting Integrity.

The module provides tools to manage, monitor, and report on the effectiveness of internal controls over financial reporting, following the COSO 2013 framework, and supports CEO/CFO certification processes as required by regulations.

## Project Structure

```
D:\development\icofr-odoo/
├── addons/                 # Odoo addons directory
│   ├── base_account_budget/
│   ├── base_accounting_kit/
│   ├── icofr/              # Main ICORF module
│   ├── icofr_demo/         # Demo module for ICORF (newly created)
│   └── icofr_demo_new_features/ # Demo module for new features
├── tasks/                  # Development documentation
│   ├── prd-icofr-system.md # Product Requirements Document
│   └── tasks-icofr-system.md # Task breakdown and progress
├── docker-compose.yml      # Docker configuration for development
├── Dockerfile              # Docker image configuration
├── odoo.conf               # Odoo server configuration
├── icofr_summary.md        # ICORF business requirements
├── create-prd.md           # PRD generation rules
└── generate-tasks.md       # Task generation rules
```

## Recent Updates

### ICORF Demo Module (@addons/icofr_demo and <!-- Import failed: addons/icofr_demo_new_features) - ENOENT: no such file or directory, access 'D:\development\icofr-odoo\addons\icofr_demo_new_features' -->
I have created additional modules called `icofr_demo` and `icofr_demo_new_features` that provide sample data for demonstrating the ICORF system. The modules include:

- **Demo data for all 7 scenarios** from the ICORF Demo Scenarios documentation
- **Comprehensive sample records** for processes, risks, controls, testing, findings, and certifications
- **Proper XML data file** (`icofr_demo_data.xml` and `icofr_demo_new_features_data.xml`) with correct syntax and field names
- **Complete module manifests** with proper dependencies
- **Instructions and documentation** in README.md

### Key Fixes Implemented
- **Fixed missing menu items**: Added menu items for Control, Risk, Testing, and Certification modules that were missing in the UI
- **Fixed XML syntax errors**: Corrected special character escaping in XML files (e.g., `>` to `&gt;`)
- **Fixed field name errors**: Identified and corrected improper field usage (e.g., `groups_id` vs `groups_ids` in user records)
- **Fixed status value mismatches**: Ensured all status fields use valid values according to each model's selection options
- **Fixed required field omissions**: Added required fields like `likelihood` and `impact` for risk records
- **Fixed reference resolution issues**: Fixed the testing schedule model's create method to properly handle batch creation during XML data loading
- **Fixed selection field mismatches**: Corrected invalid selection values like `fraud` for `risk_type` (changed to valid values: `inherent`, `residual`, `control`)
- **Added multi-company support**: All models now support multi-company operations
- **Implemented Copy Period feature**: Wizard to copy data between fiscal periods for efficiency
- **Enhanced all models**: Added additional SK BUMN compliance attributes and automatic classification features
- **Fixed view type issues**: Changed 'tree' view types to 'list' view types for UI compatibility
- **Added accounting integration**: Integration with Odoo's accounting system for mapping GL accounts to FSLI
- **Implemented Excel upload functionality**: For importing account mappings in bulk
- **Added additional menu item**: For easy access to the Excel upload wizard
- **Implemented Three Lines of Defense**: Proper role separation with distinct access rights
- **Added COBIT 2019 Framework Integration**: Complete implementation of COBIT elements with ITGC mapping
- **Developed Automated Notification System**: For CSA and testing deadline reminders
- **Implemented Line-Specific Reporting**: Dedicated reports for each line of defense (Lini 1, 2, and 3)
- **Created Qualitative Risk Assessment Tools**: Structured questionnaires for evaluating non-financial risks
- **Established BPM/SOP Document Repository**: Centralized management of business process documentation
- **Integrated ERP Financial Data**: Automatic pulling of financial data from Odoo's accounting modules
- **Improved UI/UX**: Enhanced user interfaces with mobile responsiveness and better navigation
- **Added Deficiency Quantification Tools**: Financial impact assessment capabilities
- **Implemented Manual Override Capability**: For management to adjust deficiency classifications
- **Enhanced Security**: Granular access controls for each line of defense
- **Added Excel Import for Financial Data**: Capability to import financial data directly via Excel for organizations that prefer this method over ERP integration
- **Developed Campaign Management**: For CSA period management and task distribution to Line 1
- **Created Population Upload for Audit Sampling**: For Lini 3 to receive transaction populations from Lini 1 for audit sampling
- **Implemented Master Data Upload**: For bulk upload of locations and business processes
- **Enhanced RCM Import**: With full Risk-Control Matrix import capabilities
- **Digital Signature Integration**: Implemented digital sign-off for POJK Reports with record locking.
- **Explicit TOD/TOE Workflows**: Refined the Testing module to strictly distinguish between Test of Design and Test of Operating Effectiveness.
- **Advanced Audit Sampling**: Added a wizard for manual and random selection of samples from a transaction population.
- **CEO Statement Generation**: Added automated generation of management statements based on Lampiran 11.

The demo modules are designed to showcase the full functionality of the ICORF system with realistic data that mirrors real-world implementation scenarios based on the documented use cases. I have also fixed a critical company hierarchy error in `icofr_demo` that was preventing module updates.

## ICORF Module Structure

```
addons/icofr/
├── __init__.py             # Module initialization
├── __manifest__.py         # Module manifest
├── controllers/            # Web controllers
├── data/                   # Initial data and configurations
├── models/                 # Data models
│   ├── icofr_control.py     # Control management
│   ├── icofr_risk.py        # Risk management
│   ├── icofr_testing.py     # Testing management
│   ├── icofr_certification.py # Certification process
│   ├── icofr_workflow.py    # Workflow management
│   ├── icofr_finding.py     # Finding management
│   ├── icofr_schedule.py    # Scheduling system
│   ├── icofr_pojk_report.py # POJK 15/2024 report
│   ├── icofr_notification.py # Notification system
│   ├── icofr_process.py     # Business process management
│   ├── icofr_export.py      # Export functionality
│   ├── icofr_materiality.py # Materiality calculator
│   ├── icofr_account_mapping.py # Account mapping
│   ├── icofr_csa.py         # Control Self Assessment
│   ├── icofr_action_plan.py # Action plan management
│   ├── icofr_cobit_element.py # COBIT element model
│   ├── icofr_notification_scheduler.py # Notification scheduler model
│   ├── icofr_line_reports.py # Line-specific report models
│   ├── icofr_qualitative_assessment.py # Qualitative assessment model
│   ├── icofr_bpm_document.py # BPM document model
│   ├── icofr_dashboard.py   # Dashboard model
│   ├── icofr_copy_period_wizard.py # Copy period wizard
│   ├── icofr_account_mapping_upload_wizard.py # Excel upload wizard
│   ├── icofr_master_data_upload_wizard.py # Master data upload wizard
│   ├── icofr_rcm_upload_wizard.py # RCM upload wizard
│   ├── icofr_csa_campaign.py # CSA campaign model
│   ├── icofr_audit_population.py # Audit population model
│   └── icofr_population_upload_wizard.py # Population upload wizard
├── reports/                # Report templates and logic
├── security/               # Access rights and security
├── static/                 # Static assets (CSS, JS)
├── tests/                  # Unit tests
├── views/                  # User interface views
│   ├── control_views.xml
│   ├── risk_views.xml
│   ├── testing_views.xml
│   ├── certification_views.xml
│   ├── workflow_views.xml
│   ├── finding_views.xml
│   ├── schedule_views.xml
│   ├── pojk_report_views.xml
│   ├── notification_views.xml
│   ├── process_views.xml
│   ├── export_views.xml
│   ├── materiality_views.xml
│   ├── account_mapping_views.xml
│   ├── csa_views.xml
│   ├── action_plan_views.xml
│   ├── cobit_element_views.xml
│   ├── notification_scheduler_views.xml
│   ├── line_report_views.xml
│   ├── qualitative_assessment_views.xml
│   ├── bpm_document_views.xml
│   ├── dashboard_views.xml
│   ├── copy_period_wizard_views.xml
│   ├── account_mapping_upload_wizard_views.xml
│   ├── master_data_upload_wizard_views.xml
│   ├── rcm_upload_wizard_views.xml
│   ├── csa_campaign_views.xml
│   ├── csa_campaign_actions.xml
│   ├── audit_population_views.xml
│   ├── population_upload_wizard_views.xml
│   └── icofr_menu.xml       # Main menu definition
└── README.md               # User guide and module documentation
```

### ICORF Demo Module Structures

```
addons/icofr_demo/
├── __init__.py             # Module initialization
├── __manifest__.py         # Module manifest
├── data/                   # Demo data files
│   └── icofr_demo_data.xml # XML file with all demo scenarios
└── README.md               # Documentation for the demo module
```

```
addons/icofr_demo_new_features/
├── __init__.py             # Module initialization
├── __manifest__.py         # Module manifest
├── data/                   # Demo data files
│   └── icofr_demo_new_features_data.xml # XML file with new features demo
└── README.md               # Documentation for the demo module
```

## Development Status

Based on the `tasks\tasks-icofr-system.md` file, all major development tasks have been completed:

1. **Module Structure Setup** (Completed)
   - Basic module skeleton created
   - Directory structure established
   - Manifest and dependencies defined

2. **Core Models Implementation** (Completed)
   - Control management model
   - Risk management model
   - Testing management model
   - View and access rights defined

3. **Dashboard and Interface** (Completed)
   - Control monitoring dashboard
   - Notification and reminder system
   - Real-time status components
   - Effectiveness metrics and graphs
   - Data export functionality

4. **Reporting and Certification** (Completed)
   - Certification management model
   - POJK 15/2024 format reports
   - Finding and action plan management
   - Audit trail implementation
   - PDF and Excel report templates

5. **Workflow and Calendar** (Completed)
   - Approval workflow system
   - Testing schedule management
   - Calendar integration
   - Automated notifications
   - Workflow integration with certification

6. **User Documentation** (Completed)
   - Comprehensive user guide (README.md) created
   - End-user instructions for all features

7. **Enhanced Features** (Completed)
   - Materiality calculator with automatic OM and PM calculation
   - Account mapping to FSLI (Financial Statement Line Items)
   - Control Self-Assessment (CSA) workflow
   - Automated deficiency classification
   - Impact quantification tools
   - Three Lines of Defense implementation
   - Copy Period functionality for efficiency
   - COBIT 2019 framework integration
   - Automated notification system
   - Line-specific reporting capabilities
   - Qualitative risk assessment tools
   - BPM/SOP document repository
   - ERP financial data integration
   - Mobile responsiveness features
   - Excel import for financial data
   - CSA campaign management
   - Population data upload for audit sampling
   - Master data bulk import
   - Enhanced RCM import functionality

## Key Features

### Core Functionalities
- **Control Management**: Create, manage, and monitor internal controls with types, frequencies, and owners
- **Risk Management**: Identify, assess, and mitigate financial risks with risk matrices and tracking
- **Process Management**: Link controls and risks to specific business processes for better organization
- **Testing Framework**: Document and track testing procedures with evidence collection
- **Dashboard**: Real-time monitoring with KPIs, charts, and metrics
- **Certification Process**: Support for CEO/CFO certification as required by SOX and POJK
- **POJK 15/2024 Compliance**: Reports and workflows specifically designed for Indonesian banking regulations
- **User Documentation**: Comprehensive user guide included for end users

### Advanced Features
- **Workflow Management**: Multi-stage approval processes for controls, testing, and certification
- **Scheduling System**: Automated testing schedules with recurring patterns
- **Notification System**: Automated reminders and alerts for upcoming activities
- **Audit Trail**: Complete tracking of all activities and changes
- **Export Functionality**: Data export in CSV, Excel, and PDF formats
- **Calendar Integration**: Interactive calendar for planning and scheduling
- **Materiality Calculator**: Automatic calculation of Overall Materiality and Performance Materiality
- **Account Mapping**: Mapping of GL accounts to FSLI (Financial Statement Line Items)
- **Control Self-Assessment (CSA)**: Self-assessment process following Three Lines of Defense
- **Deficiency Classification**: Automatic classification of deficiencies based on quantitative and qualitative factors
- **Three Lines of Defense**: Clear separation of duties between Process Owners (Line 1), Risk/ICOFR Team (Line 2), and Internal Audit (Line 3)
- **COBIT 2019 Integration**: Framework for IT governance and management
- **Line-specific Reporting**: Dedicated reports for each line of defense
- **Qualitative Assessment**: Tools for evaluating non-financial risks
- **BPM/SOP Repository**: Document management for business processes
- **ERP Connectivity**: Integration with Odoo's accounting data
- **Mobile Responsiveness**: Optimized UI for mobile devices
- **Excel Import Options**: Both ERP integration and Excel file import capabilities
- **CSA Campaign Management**: For organizing periodic assessment periods
- **Population Upload for Sampling**: For audit teams to receive transaction populations from process owners
- **Master Data Upload**: For bulk import of locations and business processes
- **Enhanced RCM Import**: With full Risk-Control Matrix import capabilities

### Technical Architecture
- Built for **Odoo Community Edition 19**
- Uses **Python** for backend logic
- **QWeb** for report templates
- **JavaScript** for interactive UI components
- Integrates with **mail** and **web** modules for notifications and UI
- Supports multi-company and Bahasa Indonesia localization

## Building and Running

### Prerequisites
- Docker and Docker Compose
- Odoo 19.0 environment

### Setup
1. Clone the repository
2. Ensure the `addons` directory contains the `icofr` module
3. Update `odoo.conf` to include the correct `addons_path` with `/mnt/extra-addons` for Docker
4. Build and start the containers:

```bash
docker-compose up -d
```

### Module Installation
1. Access Odoo via browser at `http://localhost:8069`
2. Login with admin credentials
3. Navigate to Apps section
4. Install the "ICORF (Internal Controls Over Financial Reporting)" module

### Development Commands
```bash
# Build the Docker images
docker-compose build

# Start the services
docker-compose up -d

# Check logs
docker-compose logs -f odoo

# Stop services
docker-compose down
```

## Development Conventions

### Code Style
- Python code follows Odoo standards
- Use UTF-8 encoding with `# -*- coding: utf-8 -*-`
- Model names follow `icofr.model_name` convention
- Views follow `view_icofr_model_view_type` naming convention
- All user interface elements in Bahasa Indonesia

### Model Structure
- All models inherit from `models.Model`
- Computed fields use `@api.depends` decorator
- Validation constraints use `@api.constrains` decorator
- Methods for business logic are grouped by functionality

### Security
- Access rights defined in `security/ir.model.access.csv`
- All models properly secured by user groups
- Sensitive operations require appropriate permissions

## Project Goals

1. **Comprehensive Internal Control Management**: Following COSO framework standards
2. **Regulatory Compliance**: Specifically for POJK No. 15 Tahun 2024 requirements in Indonesia
3. **Real-time Monitoring**: Dashboard with KPIs and metrics
4. **Audit Readiness**: Complete documentation and audit trails
5. **User Collaboration**: Support for multiple stakeholders (CFO, Controller, Internal Auditors, Process Owners)

## Success Metrics

Based on the PRD, the system aims to:
1. Improve efficiency of ICORF compliance reporting by 50%
2. Increase accuracy of control documentation by 80%
3. Reduce time for CEO/CFO certification by 30%
4. Increase visibility of control effectiveness
5. Meet external audit requirements for ICORF
6. Achieve adoption by all stakeholders involved in ICORF

## Additional Fixes

One critical issue was discovered during installation testing where certain models were failing with the error `'list' object has no attribute 'get'`. This occurred because during XML data loading, Odoo sometimes passes a list of dictionaries to the create method rather than a single dictionary. The following models were fixed:

1. **`icofr.testing.schedule` model** - Fixed in `icofr_schedule.py` to properly handle batch creation
2. **`icofr.testing` model** - Fixed in `icofr_testing.py` to properly handle batch creation
3. **`icofr.finding` model** - Fixed in `icofr_findin.py` to properly handle batch creation
4. **`icofr.action.plan` model** - Fixed in `icofr_action_plan.py` to properly handle batch creation
5. **`icofr.certification` model** - Fixed in `icofr_certification.py` to properly handle batch creation
6. **`icofr.pojk.report` model** - Fixed in `icofr_pojk_report.py` to properly handle batch creation
7. **`icofr.materiality` model** - Fixed in `icofr_materiality.py` to properly handle batch creation
8. **`icofr.account.mapping` model** - Fixed in `icofr_account_mapping.py` to properly handle batch creation
9. **`icofr.csa` model** - Fixed in `icofr_csa.py` to properly handle batch creation
10. **`icofr.process` model** - Fixed in `icofr_process.py` to properly handle batch creation
11. **`icofr.copy.period.wizard` model** - Fixed in `icofr_copy_period_wizard.py`
12. **`icofr.account.mapping.upload.wizard` model** - Fixed in `icofr_account_mapping_upload_wizard.py`
13. **`icofr.master.data.upload.wizard` model** - Fixed in `icofr_master_data_upload_wizard.py`
14. **`icofr.rcm.upload.wizard` model** - Fixed in `icofr_rcm_upload_wizard.py`
15. **`icofr.csa.campaign` model** - Fixed in `icofr_csa_campaign.py`
16. **`icofr.audit.population` model** - Fixed in `icofr_audit_population.py`
17. **`icofr.population.upload.wizard` model** - Fixed in `icofr_population_upload_wizard.py`

All models now have create methods that check if `vals` is a list (batch creation) or a dictionary (single creation) and handle each case appropriately.

This fix ensures that the demo data loads correctly without errors during the module installation process.

## Building the Complete Solution

These enhancements ensure the ICORF module now fully supports all PwC recommendations:

1. **Three Lines of Defense**: Proper role separation with distinct access rights and responsibilities
2. **Materiality Calculator**: Automatic calculation of OM and PM with ERP integration capability
3. **Enhanced RCM**: Complete with COSO mapping, assertions, and detailed attributes per SK BUMN
4. **CSA Workflow**: Complete Control Self-Assessment workflow with automated notifications
5. **Testing Workspace**: Enhanced with sampling calculator and quantification tools
6. **Deficiency Classification**: Automatic classification of deficiencies based on quantitative and qualitative factors
7. **Multi-company Support**: Full company isolation implemented
8. **Efficiency Features**: Copy Period wizard for copying data between years
9. **Quantification Tools**: Financial impact assessment capabilities with manual override option
10. **SK BUMN Compliance**: All attributes required by the standard implemented
11. **COBIT 2019 Integration**: Complete IT governance framework implementation
12. **Automated Notifications**: For CSA and testing deadline reminders
13. **Line-specific Reporting**: Dedicated reports for each line of defense
14. **Qualitative Risk Assessment**: Structured questionnaires for non-financial risk evaluation
15. **BPM/SOP Repository**: Centralized document management for processes
16. **ERP Integration**: Direct connection with accounting systems for financial data
17. **Mobile Responsiveness**: UI optimized for mobile devices
18. **Excel Import**: Flexible data import for organizations that prefer this method
19. **Campaign Management**: For organizing CSA periods and distributing tasks
20. **Population Upload**: For audit sampling from transaction populations
21. **Master Data Import**: For bulk import of locations and processes
22. **Enhanced RCM**: With full import capabilities

The module now provides a complete solution aligned with COSO 2013 framework and POJK No. 15 Tahun 2024 requirements as recommended by PwC, with a focus on the Three Lines of Defense model and automated quantification capabilities.

## Final Notes

The security configuration in `security.xml` was updated to properly assign user groups:
- `group_icofr_line_1`: Process Owners (Lini 1) - Can create/update their own controls and risks
- `group_icofr_line_2`: Risk/ICOFR Team (Lini 2) - Can review controls, create certifications, access all operational functions
- `group_icofr_line_3`: Internal Audit (Lini 3) - Can perform testing, create findings and action plans
- `group_icofr_manager`: Management - Can approve certifications and review all data
- `group_icofr_external_auditor`: External Auditors - Read-only access across all models

This implementation fully addresses the requirements from the PwC document and creates a comprehensive internal controls management system compliant with both international COSO standards and local Indonesian POJK regulations.