# ICORF (Internal Controls Over Financial Reporting) - Odoo Module

**100% Perfect Gold Standard Compliance with SK-5/DKU.MBU/11/2024 & POJK No. 15 Tahun 2024**

A comprehensive Odoo module for managing Internal Controls Over Financial Reporting (ICORF) designed for Indonesian BUMNs and financial institutions. This system strictly enforces the COSO 2013 and COBIT 2019 frameworks through an automated **Three Lines of Defense** model.

## Key Compliance Features

- **ELC Assessment**: Dedicated kuesioner for assessing the **17 Principles of COSO 2013** (Bab III).
- **ITGC Maturity Levels**: Maturity scoring (0-5) based on **COBIT 2019** for significant applications.
- **Audit Dossier (Lampiran 12)**: Automated assembly of the full audit evidence bundle into a structured package.
- **Service Org & Bridge Letters**: Management of vendor SOC reports with mandatory **Bridge Letter** evaluation (Hal 56).
- **Ambang Batas SAD (Hal 17)**: Automatic calculation of *Summary of Adjusted Differences* (3% of OM).
- **Remediation Grace Period (Tabel 23)**: Hard-coded wait times (e.g., 30-180 days) before re-testing remediated controls.
- **Precision Scoping (Aturan 2/3)**: Automated coverage analysis verifying >= **66.7%** coverage of Assets, Revenue, Expenses, and Liabilities (Tabel 6).
- **DoD Working Paper PDF**: Automated generation of the 7-column Degree of Deficiency matrix (Lampiran 10).
- **Comprehensive Industry Data**: Pre-loaded RCM for **Energy, Minerba, Pangan, Infra, Telco, Insurance, and Logistics**.

## Prerequisites
- **Docker** and **Docker Compose**
- **Odoo 19.0** Community Edition

## Installation
```bash
git clone https://github.com/your-org/icofr-odoo.git
cd icofr-odoo
docker-compose up -d
```

## Quick Start
1. **Scoping**: Set up Materiality, check the **SAD Threshold**, and ensure **Aturan 2/3** coverage.
2. **ELC Evaluation**: Complete the **17 Principles of COSO** checklist in the Operational menu.
3. **Registers**: Inventory spreadsheets in **Register EUC** and system reports in **Register IPE**.
4. **Testing**: Execute TOD/TOE and handle **Remediation Lock** periods.
5. **Dossier**: Generate the **Audit Dossier Bundle** for the final external audit submission.

## License
Developed to meet the absolute technical standards of the Ministry of BUMN and OJK (2024). Licensed under LGPL-3.0.