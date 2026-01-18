# ICORF (Internal Controls Over Financial Reporting) - Odoo Module

A comprehensive Odoo module for managing Internal Controls Over Financial Reporting (ICORF) that helps organizations, especially financial institutions in Indonesia, comply with POJK No. 15 Tahun 2024 regulations regarding Financial Reporting Integrity.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

The ICORF module implements the COSO 2013 Internal Control framework and complies with POJK 15/2024 regulations. It supports documentation, testing, reporting, and certification of internal controls over financial reporting, facilitating executive certifications (CEO/CFO) and audit readiness.

### Regulatory Framework
- **COSO Framework 2013**: Five-component internal control framework
- **POJK No. 15 Tahun 2024**: Indonesian Financial Services Authority regulation on Financial Reporting Integrity
- **SOX Compliance**: Sarbanes-Oxley Act requirements for executive certifications

### Target Users
- Chief Financial Officers (CFO)
- Chief Executive Officers (CEO)
- Internal Controllers
- Internal Auditors
- External Auditors
- Compliance Officers
- State-Owned Enterprises (BUMN) management

## Features

- **Control Management**: Create, document, and monitor internal controls with types, frequencies, and owners
- **Risk Management**: Identify, assess, and link financial risks with appropriate controls using risk matrices
- **Process Management**: Define business processes and link them to corresponding controls and risks
- **Testing Framework**: Document testing procedures, collect evidence, and track test results
- **Scheduling System**: Automate testing schedules with recurring patterns and notifications
- **Workflow Management**: Multi-stage approval processes for controls, testing, and certifications
- **Certification Process**: Support for CEO/CFO certifications as required by SOX and POJK regulations
- **Dashboard**: Real-time monitoring with KPIs, charts, and effectiveness metrics
- **POJK 15/2024 Reporting**: Generate compliance reports in required formats
- **Finding Management**: Document and track audit findings with action plans
- **Export Functionality**: Export data in CSV, Excel, and PDF formats
- **Calendar Integration**: Interactive calendar for planning and scheduling activities
- **Automated Notifications**: Reminders and alerts for upcoming activities and deadlines
- **Materiality Calculator**: Automatic calculation of Overall Materiality and Performance Materiality following POJK No. 15 Tahun 2024 requirements, including **Tabel 4 Haircut Logic**.
- **Scoping Coverage Analysis**: Automated verification of the **2/3 Rule** (66.7% coverage) for significant accounts in scope.
- **Group Multiplier Engine**: Automated materiality multiplier calculation (1.5x to 9x) for consolidation based on **Tabel 25**.
- **Materiality-Driven Risk Rating**: Precision quantitative rating (Tinggi/Sedang/Rendah) drive by per-company materiality thresholds as per **Tabel 10**.
- **Industry Risk Clusters**: Pre-defined risk frameworks for 11 BUMN clusters (Energy, Logistics, etc.) following **Lampiran 2**.
- **Technical Control Enforcement**: Strict automated validation ensuring High-Complexity EUCs meet all **Tabel 14** mandatory controls.
- **Audit Sampling Engine**: Precision calculator implementing **Tabel 22** (TOE) and **Tabel 23** (Remediation) based on frequency and risk.
- **Whistleblowing System (WBS)**: Fraud and integrity reporting module for COSO Principle 14 compliance.
- **Technical Attribute Matrix**: Specialized fields for **ITGC Areas**, **EUC Complexity**, **IPE Types**, **MRC Precision**, and **IPO (C, A, V, RA)**.
- **Interactive DoD Working Paper**: Digital version of **Lampiran 10** for transparent severity assessment.
- **Detailed TOD Checklist**: Comprehensive Design Effectiveness validation grid as per **Lampiran 8**.
- **Finding Distribution Tracking**: Automated flags for reporting to CEO, Board, and Audit Committee as per **Tabel 24**.
- **COSO Principle Matrix**: Visual assurance dashboard mapping active controls to all 17 COSO principles (**Lampiran 1**).
- **IPE & MRC Verification**: specialized technical checklists for system reports and management review precision (**Tabel 20 & 21**).
- **Extended RCM Attributes**: Comprehensive tracking of Supporting Applications, Executing Functions, Impacted FS Items, and **Effective Period** (**Tabel 18 & 19**).
- **Testing Method Framework**: Support for Inquiry, Observation, Inspection, and Reperformance methodologies (**Gambar 4**).
- **Three Lines of Defense**: Complete role separation for Lini 1 (Process Owners), Lini 2 (Risk/ICOFR Team), and Lini 3 (Internal Auditors) with appropriate access controls.
- **Control Workflow**: Robust hierarchical approval workflow (`Staff` -> `Manager`) for both Lini 1 and Lini 2, enforcing the "4-Eyes Principle" and Segregation of Duties.
- **Master Data Integration**: Built-in **COSO 2013** (Principles & Attributes) and **COBIT 2019** (Objectives) frameworks as System Data, ensuring standardized compliance from day one.
- **Qualitative Risk Assessment**: Advanced risk rating combining traditional matrix with **Tabel 11 qualitative factors** (competence, history of errors, etc.).
- **DoD Wizard**: Interactive wizard for **Degree of Deficiency** classification following AS 2201 standards.
- **Change Management Log**: Automated logging of process and control changes as required by **Appendix 6** of the regulation.
- **Control Self-Assessment (CSA)**: Complete workflow for Control Self-Assessment process with evaluation results and effectiveness measurement.
- **Deficiency Classification**: Automated classification of control deficiencies based on quantitative and qualitative factors
- **Account Mapping**: Mapping of GL accounts to Financial Statement Line Items (FSLI) for comprehensive materiality assessment
- **Multi-company Support**: Complete company isolation for organizations with multiple entities
- **Copy Period Functionality**: Wizard to copy data from one fiscal period to another for increased efficiency (addressing PwC recommendation that 80-90% of RCM remains same year-over-year)
- **SK BUMN Compliance**: Complete compliance with Surat Keputusan BUMN requirements and attributes as specified in POJK 15/2024
- **Comprehensive Demo Modules**: Separate modules for basic functionality (`icofr_demo`) and advanced features (`icofr_demo_new_features`) providing complete demonstration datasets for all scenarios
- **Excel-First Strategy**: 
  - **Financial Data Import**: Upload financial statements via Excel for materiality calculation without live ERP integration.
  - **RCM Bulk Upload**: Migrate existing Risk Control Matrices (Excel) into the system instantly via the Utilitas menu.
  - **Account Mapping Import**: Bulk upload General Ledger accounts and FSLI mappings.
- **Banking Sector Support**: Specialized demo data and risk frameworks for the financial sector, including **Kredit Ritel**, **Giro Wajib Minimum (GWM)**, and **Compliance AML/KYC** processes.
- **Service Organization Monitoring**: Manage third-party vendors and track **SOC 1/2 Reports** to ensure external control effectiveness (**Bab III Pasal 4.3**).
- **Interactive Compliance Guide (FAQ)**: Built-in repository of the 14 most common implementation questions from **Lampiran 12 Juknis BUMN**.
- **Specialist Validation**: Document and evaluate third-party experts' credibility and assumptions (**Bab III Pasal 2.2.b.4**).
- **Remediation Sampling Engine**: Automated sample size calculation specifically for post-fix testing based on **Tabel 23**.
- **CSA "No Transaction" Support**: Accurate handling of controls with no activity during the assessment period to maintain audit integrity.

## Prerequisites

- **Docker** and **Docker Compose**
- **Odoo 19.0** Community Edition
- Compatible with both Linux and Windows development environments

## Installation

### Docker Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/icofr-odoo.git
   cd icofr-odoo
   ```

2. Build and start services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access Odoo via browser at `http://localhost:8069`

4. Login with admin credentials and navigate to Apps section

5. Search and install the "ICORF (Internal Controls Over Financial Reporting)" module

### Manual Installation

1. Ensure Odoo 19.0 is installed on your system

2. Add the `addons/icofr` directory to your Odoo addons path

3. Restart the Odoo server

4. In Odoo interface, go to Apps → Update Apps List

5. Search for "ICORF" and install the module

## Configuration

### Initial Setup
1. After installation, access the ICORF module from the main menu
2. Configure master data:
   - Business processes
   - Risk categories
   - Control types
   - User roles and permissions

### User Roles and Permissions
- `icofr.user`: Basic access to controls, risks, and testing
- `icofr.manager`: Manage controls, risks, and testing with advanced functions
- `icofr.admin`: Full access to all features and configurations
- `icofr.certifier`: Special role for certification processes (CEO/CFO)

### Email Configuration (for notifications)
Configure your email settings in Odoo to receive automated notifications and reminders:
1. Go to Settings → General Settings → Outgoing Mail Servers
2. Configure your SMTP server details
3. Test the connection

## Usage

### Quick Start
1. Set up business processes first
2. Define financial risks associated with each process
3. Create internal controls linked to processes and risks
4. Schedule testing for controls based on frequency requirements
5. Perform testing and document results
6. Generate reports and prepare for certification

### Main Functional Areas

#### 1. Master Data Management
- **Business Processes**: Define and document business processes
- **Risks**: Identify and assess financial risks
- **Controls**: Create and manage internal controls

#### 2. Operational Management
- **Testing Schedule**: Plan and schedule control testing activities
- **Control Testing**: Execute tests and document results
- **Findings Management**: Record and track audit findings

#### 3. Compliance and Reporting
- **Certification**: Prepare and execute CEO/CFO certifications
- **POJK 15/2024 Reports**: Generate required regulatory reports
- **Dashboard**: Monitor control effectiveness in real-time

### Dashboard Navigation
1. Access the dashboard from the main ICORF menu
2. View key metrics:
   - Total controls by status
   - Upcoming testing activities
   - Risk distribution
   - Certification status
3. Use filters to focus on specific time periods or business units
4. Export dashboard data as needed

## Development

### Project Structure
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
│   ├── icofr_materiality.py # Materiality & Scoping
│   ├── icofr_coso_mapping.py # COSO Principle Matrix
│   ├── icofr_account_mapping.py # FSLI Mapping
│   ├── icofr_wbs.py         # Whistleblowing System
│   └── icofr_export.py      # Export functionality
├── reports/                # Report templates and logic
├── security/               # Access rights and security
├── static/                 # Static assets (CSS, JS)
├── tests/                  # Unit tests
├── views/                  # User interface views
└── README.md               # User guide and module documentation
```

### Running in Development Mode
1. Navigate to the project directory
2. Use Docker Compose to run the development environment:
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```
3. The Odoo server will automatically reload when files change

### Running Tests
```bash
# Execute Odoo tests for the ICORF module
docker-compose exec odoo odoo -d icofr_db -i icofr --test-enable
```

## Contributing

We welcome contributions to the ICORF module! Here's how you can help:

### Reporting Bugs
- Use the GitHub issue tracker
- Describe the problem clearly
- Include steps to reproduce
- Provide expected vs. actual behavior

### Feature Requests
- Submit feature requests through the issue tracker
- Explain the use case and business value
- Consider regulatory compliance requirements

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow Odoo coding standards
- Use Bahasa Indonesia for all user-facing elements
- Maintain compliance with POJK 15/2024 and COSO framework
- Include tests for new functionality

## License

This project is licensed under the GNU Lesser General Public License v3.0 (LGPL-3.0). 
See the [LICENSE](LICENSE) file for details.

## Support

For technical support or questions about implementation:
- Check the FAQ section of the user documentation
- Contact your Odoo implementation partner
- Report issues through the GitHub issue tracker

## Related Documentation

- [POJK No. 15 Tahun 2024](https://www.ojk.go.id/id/regulasi/peraturan-ojk/15-2024/) (OJK official site)
- [COSO Internal Control Framework 2013](https://www.coso.org/)
- [Odoo 19.0 Documentation](https://www.odoo.com/documentation/19.0/)

## About the Project

This module was developed to address the specific needs of Indonesian financial institutions and state-owned enterprises in implementing Internal Controls Over Financial Reporting (ICORF) as required by POJK No. 15 Tahun 2024. The solution combines international best practices with local regulatory requirements to provide a comprehensive control management platform.
