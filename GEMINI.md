# ICORF Odoo Module (POJK 15/2024 & SK-5/DKU.MBU/11/2024)

## Project Overview
This project is an Odoo 19.0 module designed for **Internal Controls Over Financial Reporting (ICORF)**. It ensures 100% compliance with **POJK No. 15 Tahun 2024** and **SK-5/DKU.MBU/11/2024** (Ministry of BUMN), following the **COSO 2013** and **COBIT 2019** frameworks.

The system implements the **Three Lines of Defense** model with hard-coded regulatory constraints and audit-ready simulations.

### Key Compliance Features (Perfect Gold Standard)
- **ELC Assessment (17 COSO Principles):** Structured kuesioner for qualitative evaluation of the entity-level control environment (Bab III).
- **ITGC Maturity Scoring (COBIT 2019):** Maturity level 0-5 tracking for significant applications.
- **Audit Dossier Wizard (Lampiran 12):** One-click assembly of structured audit evidence (RCM, Flowcharts, TOD/TOE, DoD, Certifications).
- **Service Org & Bridge Letters:** Full tracking of SOC reports with gap analysis and Bridge Letter verification (Hal 56).
- **Industry Cluster Coverage:** Expanded Risk Control Matrix (RCM) including **Energy, Minerba, Pangan, Infra, Telco, Insurance, and Logistics**.
- **Aturan 2/3 Scoping Coverage:** Automated verification that significant accounts cover >= 66.7% of **Assets, Revenue, Expenses, and Liabilities** (Tabel 6).
- **Remediation Lock (Tabel 23):** Hard validation preventing re-testing until mandatory minimum operating periods have passed.
- **Audit Sampling Calculator:** Precision logic based on population size (Tabel 22) with **Mandatory December Sample** enforcement.

### Key Models
- `icofr.control`: Master controls with EUC/IPE checklists and ITGC attributes.
- `icofr.elc.assessment`: Structured evaluation of the 17 COSO principles.
- `icofr.testing`: Precision sampling, **Roll-forward**, and **Remediation Lock** logic.
- `icofr.application`: IT system management with **ITGC Maturity Scores**.
- `icofr.materiality`: Scoping dashboard with **Aturan 2/3** and **SAD** threshold.
- `icofr.finding.group`: Aggregated evaluation with **DoD Report** integration.

### Coding Standards
*   **Remediation Rule**: Prevents retest if `test_date - action_completion_date < min_days` (Tabel 23).
*   **Financial Scoping Rule**: Coverage status fails if < 66.7% on ANY of the 4 metrics (Tabel 6).
*   **Workflow**: `draft` -> `waiting_l1_approval` -> `under_review` -> `waiting_l2_approval` -> `active`.
