# ICORF (Internal Controls Over Financial Reporting) - Odoo Module

**100% Perfect Gold Standard Compliance with SK-5/DKU.MBU/11/2024 & POJK No. 15 Tahun 2024**

A comprehensive Odoo module for managing Internal Controls Over Financial Reporting (ICORF) designed for Indonesian BUMNs and financial institutions. This system strictly enforces the COSO 2013 and COBIT 2019 frameworks through an automated **Three Lines of Defense** model.

## Key Compliance Features

- **Advanced Scoping Workflow**: Integrated two-step data import:
    - **Step 1 (FSLI Template)**: Import organizational structure and FSLI mapping with support for parent/subsidiary `entity_code`.
    - **Step 2 (General Ledger)**: Import real GL balances to trigger the **Aturan 2/3** coverage analysis (Tabel 6).
- **ELC Assessment**: Dedicated kuesioner for assessing the **17 Principles of COSO 2013** (Bab III).
- **ITGC Maturity Levels**: Maturity scoring (0-5) based on **COBIT 2019** for significant applications.
- **Audit Dossier (Lampiran 12)**: Automated assembly of the full audit evidence bundle into a structured package.
- **Service Org & Bridge Letters**: Management of vendor SOC reports with mandatory **Bridge Letter** evaluation (Hal 56).
- **Ambang Batas SAD (Hal 17)**: Automatic calculation of *Summary of Adjusted Differences* (3% of OM).
- **Remediation Grace Period (Tabel 23)**: Hard-coded wait times (e.g., 30-180 days) before re-testing remediated controls.
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
1. **Import Structure**: Use the **"Upload Excel Pemetaan Akun"** wizard with the `Template Laporan` file to set up FSLI and Entity codes.
2. **Populate Balances**: Go to **Kalkulator Materialitas**, click **"Import Data Keuangan"**, and upload your `General Ledger` file.
3. **Analyze Scoping**: Verify the **Aturan 2/3** coverage and set up OM/PM parameters.
4. **ELC Evaluation**: Complete the **17 Principles of COSO** checklist in the Operational menu.
5. **Dossier**: Generate the **Audit Dossier Bundle** for the final external audit submission.

## License
Developed to meet the absolute technical standards of the Ministry of BUMN and OJK (2024). Licensed under LGPL-3.0.
