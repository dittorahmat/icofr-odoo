# ICORF Odoo Module (POJK 15/2024)

## Project Overview
This project is an Odoo 19.0 module designed for **Internal Controls Over Financial Reporting (ICORF)**. It ensures compliance with **POJK No. 15 Tahun 2024** (Indonesian Financial Services Authority regulation) and **SK-5/DKU.MBU/11/2024** (Ministry of BUMN technical guidelines), following the **COSO 2013** framework.

The system implements the **Three Lines of Defense** model:
1.  **First Line (Lini 1):** Process Owners (Operational/CSA Execution).
2.  **Second Line (Lini 2):** Risk Management/ICORF Team (Scoping, RCM, & Monitoring).
3.  **Third Line (Lini 3):** Internal Audit (Independent Testing & Assurance).

### Key Compliance Features
- **Dynamic Materiality Calculator:** Automatically computes OM and PM based on financial data with SK-BUMN Table 3 compliant smart defaults and **External Auditor Consultation** tracking (Hal 16).
- **Proportional Materiality Allocation:** Automated calculation of materiality allocation to subsidiaries based on **asset proportion** as required by Hal 115.
- **Materiality Haircut Logic:** Implementation of Table 4 for PM determination based on audit history and risk factors.
- **Automated Deficiency Classification:** Real-time evaluation of findings against materiality thresholds, including automated downgrades via effective Compensating Controls.
- **DoD Wizard (Degree of Deficiency):** Advanced decision tree following the **7-Box Logic (Lampiran 10 / Gambar 5)**. Includes qualitative overrides for **Prudent Official** conclusions and automated routing based on assertion relevance, likelihood, and magnitude.
- **Qualitative Risk Matrix:** Integrated assessment using Table 11 & 12 (Inherent risk, history of errors, etc.) combined with quantitative likelihood/impact.
- **Industry-Specific Risk Library:** Pre-defined risk templates for **11 BUMN Industrial Clusters** (Energy, Logistics, Financial, etc.) as required by Lampiran 2.
- **Change Management Log (Appendix 6):** Audit-ready logging of all modifications with mandatory 'Before' and 'After' descriptions and references.
- **Aggregated Deficiency Evaluation:** Grouping mechanism to assess the collective impact of multiple control deficiencies, with **Grouping Basis** by Account, COSO Principle, Process, or **Assertion** (Hal 69).
- **ERP Integration for Audit Sampling:** Wizard-driven data pulling from Odoo GL (`account.move.line`) to ensure audit populations are grounded in actual transactions.
- **IPE & MRC Technical Verification:** Specialized checklists for system reports (Tabel 20) and management review precision (Tabel 21) integrated into testing workpapers.
- **COSO Mapping Matrix:** Visual dashboard to ensure all 17 COSO principles are covered by active key controls (Lampiran 1).
- **ITGC vs COBIT Dashboard:** Visual mapping of 4 ITGC areas to 15 COBIT 2019 objectives as required by **Tabel 1**.
- **Significant Application Registry:** System-wide mapping of IT applications to automated controls with **ITGC Impact Logic** (FAQ 4) and **Cybersecurity focus** (Hal 46). Automated controls are flagged if supporting ITGC is ineffective.
- **Control Level Classification:** Structural mapping of ELC (Direct/Indirect/Monitoring) and TLC (Transaction Level) as per **Tabel 17-19**.
- **Qualitative Account Significance:** Support for non-monetary scoping triggers like WIP BUMN Konstruksi, Loan Covenants, and 3rd Party Assets (**Tabel 5**).
- **Line 3 Audit Reporting:** Formally structured reports with executive summaries, detailed deficiency disclosures, and **Remediation Progress** tracking (**Bab VII**).
- **RCM Mandatory Attributes:** Compliance fields for Supporting Application, Executing Function, IPO (C, A, V, RA), and Impacted FS Items (Tabel 18 & 19).
- **Testing Methodologies:** Standardized recording of Inquiry, Observation, Inspection, Reperformance, and **Data Analysis (CAATs)** methods (Gambar 4).
- **Audit Sampling Calculator:** Implementation of SK-BUMN Table 22 (TOE) and **Table 23 (Remediation)**. Automatic calculation of sample sizes and **Minimum Testing Periods** (e.g., 3 months for monthly controls) with **Mandatory December/Q4 Sample** enforcement.
- **Scoping Coverage Analysis (2/3 Rule):** Automated verification that significant accounts and locations in scope cover at least 66.7% of total **Assets, Revenue, Expenses, and Liabilities** as required by Bab III Pasal 1.3 and Table 6.
- **Newly Acquired Entity Transition:** Support for FAQ 13 logic to exclude new subsidiaries from year-one evaluation while maintaining disclosure integrity.
- **Structured BPM Documentation:** Digital implementation of **Lampiran 3 & 4** with standardized activity types (Manual, Automated, Interface, Archive, Note) via `icofr.process.step`.
- **Materiality-Based Risk Rating:** Quantitative rating logic (Tinggi/Sedang/Rendah) driven by monetary exposure vs. active materiality thresholds (OM/PM) as per Table 10.
- **Industry Cluster Mapping:** Pre-defined risk classification for 11 BUMN Industry Clusters (Energy, Logistics, Financial, etc.) as required by Lampiran 2.
- **EUC Technical Enforcement:** Automated validation rules ensuring High-Complexity spreadsheets meet all 5 mandatory control criteria (Tabel 14).
- **Group Materiality Multiplier:** Automated calculation of materiality multiplier (1.5x to 9x) for consolidation entities based on Table 25, with automated counting of significant locations.
- **Group Materiality Allocation:** Automated validation rule ensuring subsidiary materiality thresholds do not exceed the Group Overall Materiality (Hal 115).
- **External Assurance Tracking:** Dedicated module for recording independent auditor reviews and opinions on management's ICOFR assessment (Bab VIII).
- **Interactive Certification Paper:** Digitized Lampiran 11 with mandatory CEO/CFO point-by-point acknowledgment checkboxes and **Automated Finding Summary Tables**.
- **Whistleblowing System (WBS):** Enhanced module for recording fraud/integrity reports via multiple sources (Hotline, Web, Email) with disposition tracking and finding integration (Principle 14).
- **ITGC, EUC, IPE, & MRC Mapping:** Extended control attributes for IT General Controls (4 Areas), spreadsheet complexity (EUC), system report types (IPE), and Management Review precision (MRC).
- **Finding Distribution Enforcement:** Automated tracking and **hard-stop validation** of deficiency reporting to CEO, Board, and Audit Committee as per Table 24 requirements.
- **Management Adjustments (Hal 71):** Module to record both External (Audit) and **Internal Management Adjustments** as mitigating measures or deficiency indicators.
- **SSO Monitoring:** Enhanced monitoring for Shared Service Organizations with **Right to Audit** verification (Hal 30 & 40).
- **Line 2 vs Line 3 Reconciliation:** Dashboard for comparing CSA results (Lini 2) with Audit results (Lini 3) as required by Hal 61.

### Key Models

- `icofr.control`: Internal controls registry with ITGC reliance logic, technical attributes, and hierarchical workflow.

- `icofr.process.step`: Structured BPM activity registry following **Lampiran 3** legends.

- `icofr.application`: Registry for significant IT systems with **ITGC Effectiveness** tracking (FAQ 4).

- `icofr.service.organization`: Registry for third-party service providers with **Right to Audit** tracking.

- `icofr.soc.report`: Tracking of SOC reports with Bridge Letter validation.

- `icofr.itgc.mapping`: SQL-view dashboard for monitoring ITGC coverage.

- `icofr.external.assurance`: Tracking of independent auditor reviews (Bab VIII).

- `icofr.faq`: Interactive repository of Juknis Lampiran 12 FAQ.

- `icofr.finding.group`: Aggregated evaluation module with **Assertion** grouping and **Group Compensating Control** logic.

- `icofr.wbs.entry`: Whistleblowing System with disposition and finding integration.

- `icofr.testing`: Testing procedures with automated sampling (including December/Q4 enforcement, Remediation periods) and TOD/TOE checklists.

- `icofr.materiality`: Materiality thresholds with automated **Aturan 2/3** (4 metrics), **Proportional Allocation**, and **Auditor Consultation** logs.

- `icofr.finding`: Findings documentation with **DoD Working Paper (7-Box Logic)** and **Reporting Enforcement**.

- `icofr.risk`: Financial risk matrix with integrated **Qualitative Factors** and **Industry Cluster** mapping.

- `icofr.coso.mapping`: Dynamic SQL-view matrix for COSO coverage.

- `icofr.external.adjustment`: Registry for External/Internal adjustments with auto-finding creation.

### Coding Standards

*   **Financial Scoping Rule**: The system automatically fails coverage status if significant accounts and locations do not meet the 66.7% threshold of total **Assets, Revenue, Expenses, and Liabilities** as per Table 6.

*   **Risk Rating Logic**: Final Risk Rating is automatically computed by taking the HIGHER of Quantitative and Qualitative scores (Table 12).

*   **Reporting Distribution**: Enforces validation rules to ensure MW/SD findings are marked as reported to the Audit Committee and Board before closure (Table 24).

*   **BPM Structure**: Processes must be documented using structured steps (`icofr.process.step`) to support standard legends.

*   **Certification Reporting**: Uses formal verbiage from **Lampiran 11** and includes **Automated summary tables**.

*   **ITGC Reliance Logic**: Automated controls automatically show **reliance failure** if the supporting IT system's ITGC is marked as Ineffective (FAQ 4).

*   **December Sampling Rule**: Hard validation preventing completion of Monthly/Quarterly TOE tests if they don't include a December/Q4 sample (Table 22).

*   **Control Workflow**: Hierarchical review workflow (`draft` -> `waiting_l1_approval` -> `under_review` -> `waiting_l2_approval` -> `active`).