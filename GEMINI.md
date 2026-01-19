# ICORF Odoo Module (POJK 15/2024 & SK-5/DKU.MBU/11/2024)

## Project Overview
This project is an Odoo 19.0 module designed for **Internal Controls Over Financial Reporting (ICORF)**. It ensures 100% compliance with **POJK No. 15 Tahun 2024** and **SK-5/DKU.MBU/11/2024** (Ministry of BUMN), following the **COSO 2013** and **COBIT 2019** frameworks.

The system implements the **Three Lines of Defense** model with hard-coded regulatory constraints and audit-ready simulations.

### Key Compliance Features
- **Dynamic Materiality Calculator:** Computes OM/PM with **Haircut Logic**. Includes **Proportional Allocation** (Hal 115) and validation of **Accumulated Group Limit**.
- **Aturan 2/3 Scoping Coverage:** Automated verification that significant accounts cover >= 66.7% of **Assets, Revenue, Expenses, and Liabilities** (Tabel 6).
- **Roll-forward Methodology:** Tracking for interim tests with mandatory roll-forward procedures and conclusions (Hal 51).
- **Remediation Lock (Tabel 23):** Hard validation preventing re-testing of fixed controls until the mandatory minimum operating period has passed (e.g., 30 days for daily controls).
- **Audit Sampling Calculator:** Precision logic based on population size (Tabel 22) with **Mandatory December Sample** enforcement.
- **DoD Wizard (Degree of Deficiency):** Decisions follow the **7-Box Logic (Lampiran 10)** with qualitative overrides.
- **Aggregated Evaluation:** Multi-basis grouping by **Account, Process, Assertion, or COSO Principle (1-17)** with compensating control logic (Hal 69).
- **EUC Technical Enforcement:** High-complexity spreadsheets must pass all **5 mandatory criteria** (Tabel 14).
- **Auditor Integrity:** Hard-stop **Cooling-off Period** (12 months) preventing auditors from testing their own previous L1/L2 responsibilities (Hal 19).
- **Management Override (MOC):** Specialized risk and control attributes to detect and prevent senior management intervention (FAQ 14).

### Key Models
- `icofr.control`: Master controls with EUC checklists, ITGC phases, and IPO attributes.
- `icofr.testing`: Precision sampling, **Roll-forward**, and **Remediation Lock** logic.
- `icofr.materiality`: Scoping dashboard with **Aturan 2/3** coverage metrics.
- `icofr.finding.group`: Aggregated evaluation by assertion or **COSO Principle**.
- `icofr.service.organization`: Monitoring of SOC Reports with **Bridge Letter** validation.

### Coding Standards
*   **Remediation Rule**: Prevents retest if `test_date - action_completion_date < min_days` (Tabel 23).
*   **Financial Scoping Rule**: Coverage status fails if < 66.7% on ANY of the 4 metrics (Tabel 6).
*   **Workflow**: `draft` -> `waiting_l1_approval` -> `under_review` -> `waiting_l2_approval` -> `active`.