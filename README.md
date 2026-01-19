# ICORF (Internal Controls Over Financial Reporting) - Odoo Module

**100% Audit-Proof Compliance with SK-5/DKU.MBU/11/2024 & POJK No. 15 Tahun 2024**

A comprehensive Odoo module for managing Internal Controls Over Financial Reporting (ICORF) designed for Indonesian BUMNs and financial institutions. This system strictly enforces the COSO 2013 and COBIT 2019 frameworks through an automated **Three Lines of Defense** model.

## Key Compliance Features

- **Remediation Grace Period (Tabel 23)**: Hard-coded wait times (e.g., 30-90 days) ensuring remediated controls operate effectively before re-testing is allowed.
- **Precision Scoping (Aturan 2/3)**: Automated coverage analysis verifying that significant accounts and locations cover >= **66.7%** of **Assets, Revenue, Expenses, and Liabilities** (Tabel 6).
- **Roll-forward Methodology**: Integrated workflow for interim testing with mandatory validation for the remaining period (Hal 51).
- **Audit Sampling Engine**: Precision calculator implementing **Tabel 22** population rules and **Mandatory December Sample** enforcement.
- **Aggregated Evaluation**: Grouping findings by **Financial Assertion** or **COSO Principle** with automated **Compensating Control** reduction logic (Hal 69).
- **Management Override Prevention**: Dedicated risk scenarios and detective controls for **Senior Management Jurnal Manual (MOC)** as per FAQ 14.
- **Auditor Independence**: Hard validation of the **12-month Cooling-off Period** for Lini 3 testers (Hal 19).
- **EUC & IPE Integrity**: Specialized checklists for **High-Complexity Spreadsheets** (Tabel 14) and system-generated reports (Tabel 20).
- **Shared Service Monitoring**: Manage **SSO/Third-party** risks with **SOC Report Gap Analysis** and **Bridge Letters**.

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
1. **Scoping**: Set up Materiality and ensure **Aturan 2/3** coverage is reached across 4 metrics.
2. **Testing**: Execute **Interim Tests** and perform **Roll-forward** procedures or **Remediation Retests** after the mandatory wait period.
3. **MOC Detection**: Utilize the pre-defined **Management Override** risk library to safeguard against fraud.

## License
Developed to meet the technical standards of the Ministry of BUMN and OJK (2024). Licensed under LGPL-3.0.
