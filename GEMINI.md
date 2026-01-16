# ICORF Odoo Module (POJK 15/2024)

## Project Overview
This project is an Odoo 19.0 module designed for **Internal Controls Over Financial Reporting (ICORF)**. It ensures compliance with **POJK No. 15 Tahun 2024** (Indonesian Financial Services Authority regulation) and **SK-5/DKU.MBU/11/2024** (Ministry of BUMN technical guidelines), following the **COSO 2013** framework.

The system implements the **Three Lines of Defense** model:
1.  **First Line (Lini 1):** Process Owners (Operational/CSA Execution).
2.  **Second Line (Lini 2):** Risk Management/ICORF Team (Scoping, RCM, & Monitoring).
3.  **Third Line (Lini 3):** Internal Audit (Independent Testing & Assurance).

### Key Compliance Features
- **Dynamic Materiality Calculator:** Automatically computes OM and PM based on financial data with SK-BUMN Table 3 compliant smart defaults.
- **Materiality Haircut Logic:** Implementation of Table 4 for PM determination based on audit history and risk factors.
- **Automated Deficiency Classification:** Real-time evaluation of findings against materiality thresholds, including automated downgrades via effective Compensating Controls.
- **DoD Wizard (Degree of Deficiency):** Interactive decision tree guiding auditors through classification (CD/SD/MW) based on AS 2201 / Gambar 5 guidelines.
- **Qualitative Risk Matrix:** Integrated assessment using Table 11 & 12 (Inherent risk, history of errors, etc.) combined with quantitative likelihood/impact.
- **Change Management Log (Appendix 6):** Audit-ready logging of all modifications with mandatory 'Before' and 'After' descriptions and references.
- **Aggregated Deficiency Evaluation:** Grouping mechanism to assess the collective impact of multiple control deficiencies.
- **ERP Integration for Audit Sampling:** Wizard-driven data pulling from Odoo GL (`account.move.line`) to ensure audit populations are grounded in actual transactions.
- **IPE & MRC Technical Verification:** Specialized checklists for system reports (Tabel 20) and management review precision (Tabel 21).
- **COSO Mapping Matrix:** Visual dashboard to ensure all 17 COSO principles are covered by active key controls (Lampiran 1).
- **RCM Mandatory Attributes:** Compliance fields for Supporting Application, Executing Function, and Impacted FS Items (Tabel 18 & 19).
- **Testing Methodologies:** Standardized recording of Inquiry, Observation, Inspection, and Reperformance methods (Gambar 4).
- **Audit Sampling Calculator:** Implementation of SK-BUMN Table 22 for sample size determination based on control frequency and risk level, and Table 23 for Remediation Testing.
- **Scoping Coverage Analysis (2/3 Rule):** Automated verification that significant accounts in scope cover at least 66.7% of total Assets and Revenue as required by Bab III Pasal 1.3.
- **Materiality-Based Risk Rating:** Quantitative rating logic (Tinggi/Sedang/Rendah) driven by monetary exposure vs. active materiality thresholds (OM/PM) as per Table 10.
- **Industry Cluster Mapping:** Pre-defined risk classification for 11 BUMN Industry Clusters (Energy, Logistics, Financial, etc.) as required by Lampiran 2.
- **EUC Technical Enforcement:** Automated validation rules ensuring High-Complexity spreadsheets meet all 5 mandatory control criteria (Tabel 14).
- **Group Materiality Multiplier:** Automated calculation of materiality multiplier (1.5x to 9x) for consolidation entities based on Table 25.
- **Whistleblowing System (WBS):** Dedicated module for recording and investigating fraud/integrity reports to comply with COSO Principle 14.
- **ITGC, EUC, IPE, & MRC Mapping:** Extended control attributes for IT General Controls (4 Areas), spreadsheet complexity (EUC), system report types (IPE), and Management Review precision (MRC).
- **IPO (Information Processing Objectives):** Integration of C, A, V, and RA (Completeness, Accuracy, Validity, Restricted Access) attributes into the RCM as per Table 13.
- **RCM Mandatory Attributes:** Added fields for Supporting Application, Executing Function, Impacted FS Items (Table 18 & 19), and Control Effective Period.
- **Testing Methodology:** Support for inquiry, observation, inspection, and reperformance methods with specific documentation (Gambar 4).
- **CSA Exception Handling:** Logic to handle 'No Transaction' scenarios in Control Self-Assessment (Bab IV Pasal 2.1).
- **Interactive DoD Working Paper:** Digital implementation of Lampiran 10 (Kotak 1-7) for transparent deficiency classification.
- **Detailed Testing Attributes:** Support for Lampiran 7 checklist (Attributes A, B, C, D) and Lampiran 8 TOD detailed validation at the transaction level.
- **Finding Distribution Tracker:** Automated tracking of deficiency reporting to CEO, Board, and Audit Committee as per Table 24 requirements.
- **Service Organization Monitoring:** Dedicated module for managing third-party vendors and their **SOC 1/2 Type II Reports** as required by Bab III Pasal 4.3.
- **Specialist Involvement Validation:** Specific attributes for evaluating **Specialist Credibility**, Assumption Validity, and Fairness as per Bab III Pasal 2.2.b.4.
- **Remediation Sampling Engine:** Standalone logic implementing **Table 23** for post-remediation testing with specific observation periods.
- **CSA "No Transaction" Logic:** Support for 'No Transaction' status in CSA to ensure audit accuracy for dormant controls (Bab IV Pasal 2.1.c).
- **Interactive compliance FAQ:** Integrated 14-point decision guide from Lampiran 12 to assist users in resolving implementation ambiguities.

### Key Components
...

### Key Models

- `icofr.control`: Internal controls registry with ITGC, EUC, IPE, MRC, IPO, and **Specialist/Service Org** technical attributes.

- `icofr.service.organization`: Registry for third-party service providers (Data Centers, Payroll Outsourcing, etc.).

- `icofr.soc.report`: Tracking of SOC 1 Type I/II and SOC 2 reports for external control assurance.

- `icofr.faq`: Interactive repository of Juknis Lampiran 12 FAQ for user guidance.

- `icofr.finding.group`: Aggregated evaluation module with **Grouping Basis** (Account, COSO Principle, or Process).

- `icofr.wbs.entry`: Whistleblowing System for fraud and integrity report management.

- `icofr.testing`: Testing procedures with automated sampling calculator (Tabel 22 & 23), TOD checklists (Lampiran 8), and attribute checklists (Lampiran 7).

- `icofr.materiality`: Materiality thresholds with automated **Scoping Coverage Analysis (Aturan 2/3)** and **Group Multiplier (Tabel 25)**.

- `icofr.finding`: Findings documentation with **DoD Working Paper** (Lampiran 10) and **Distribution Matrix** (Tabel 24).

- `icofr.risk`: Financial risk matrix with integrated **Qualitative Factors (Tabel 11)** and **Risk Rating Matrix (Tabel 12)**.

- `icofr.coso.mapping`: Dynamic SQL-view matrix for monitoring 17 COSO Principles coverage (Lampiran 1).

### Excel-First Strategy (Implemented)

To facilitate rapid adoption without immediate ERP integration, the system supports a comprehensive "Excel-First" approach:

- **Financial Data Import**: Users can upload financial statement data (Revenue, Assets, Net Income) via Excel directly into the `icofr.materiality` model using the `icofr.financial.data.import.wizard`.
- **RCM Bulk Upload**: The `icofr.rcm.upload.wizard` (available in Utilitas menu) allows bulk uploading of Risk Control Matrices (Risk, Control, assertions, etc.) directly into the system.
- **Account Mapping Upload**: The `icofr.account.mapping.upload.wizard` enables bulk import of General Ledger accounts and their FSLI (Financial Statement Line Item) associations.
- **Banking Sector Presets**: Built-in demo data and risk profiles specifically for the **Financial/Banking Sector**, including Kredit Ritel, GWM (Statutory Reserve), and AML/KYC processes.

## Building and Running

...

*   **Access Application:**

    Navigate to `http://localhost:8069`. Log in with `admin`/`admin` (default).



## Development Conventions



### Odoo 19.0 Specifics

*   **Views:** Use `<list>` tag instead of `<tree>` for list views.

*   **Context:** Use `id` instead of `active_id` in view contexts when passing the current record to wizards.

*   **Manifest:** Maintain strict load order: Wizards and Actions must be loaded before the views that reference them.



### Coding Standards

*   **Scoping Rule**: The system automatically fails coverage status if significant accounts do not meet the 66.7% threshold of total financial value (Assets/Revenue) as per Table 6.

*   **Risk Rating Logic**: Final Risk Rating is automatically computed by taking the HIGHER of Quantitative (Likelihood x Impact) and Qualitative scores, following the 3x3 matrix in Table 12.

*   **Group Multiplier**: For group entities, the system automatically applies a multiplier (Table 25) based on the number of significant locations to determine the maximum materiality allocation.

*   **Sampling Engine**: Sample sizes are dynamically calculated based on control frequency (Daily to Yearly) and risk (Low/High). Remediation tests use a specialized "Zero Tolerance" set (Tabel 23).

*   **Technical Control Validation**: Controls marked as EUC require validation of Version Control and Data Integrity, while IPE requires validation of system extraction parameters (Tabel 14 & 15).

*   **IPO Mapping**: Every control in the RCM should be mapped to relevant Information Processing Objectives (Completeness, Accuracy, Validity, or Restricted Access) as per Table 13.

*   **IPE/MRC Validation**: pengujian for IPE must verify parameters and extraction validity (Tabel 20), while MRC requires proof of professional skepticism and reperformance (Tabel 21).

*   **Testing Methodology**: Auditors must select and document the specific testing method (Inquiry, Observation, Inspection, Reperformance) used for each TOE result as per Gambar 4.

*   **Certification Reporting**: The `icofr.certification` report uses formal verbiage from **Lampiran 11** and includes a mandatory summary table of all MW/SD findings.

*   **Digital Signatures:** The `icofr.pojk.report` model uses an `is_signed` flag to lock records. Once signed, the `write` method prevents modifications.

*   **Testing Workflows:** `icofr.testing` supports `design_validation` (Test of One) for Line 2, and `tod`/`toe` for Line 3. Design validation is mandatory for new controls or after ineffective CSA.

*   **Sampling:** Use `icofr.sample.selection.wizard` for bulk linking of population records to TOE tests.

*   **Batch Creation:** Always handle `vals_list` in `create()` overrides to support XML imports.

*   **Deficiency Classification:** Deficiency severity (MW/SD/CD) is dynamically calculated in `icofr.finding` by comparing monetary impact against the active `icofr.materiality` thresholds (OM/PM) for the current period.

*   **Compensating Controls:** Findings support mitigation via `compensating_control_id`. An effective compensating control automatically suggests downgrading the deficiency classification.

*   **Aggregated Evaluation:** Multiple `icofr.finding` records can be grouped into an `icofr.finding.group` to evaluate if their combined impact reaches a higher deficiency level (e.g., several small CD findings totaling to an SD impact).

*   **Materiality Defaults:** The `icofr.materiality` model applies smart defaults based on SK BUMN Table 3 (e.g., 5% for Net Income basis, 1% for Revenue/Assets).

*   **ERP Data Pull for Sampling:** The system supports pulling transaction data directly from Odoo's `account.move.line` into the `icofr.audit.population` model via the `icofr.population.pull.erp.wizard`. This ensures testing is based on actual financial data.

*   **COSO 2013 Master Data:** The 5 Components and 17 Principles of the COSO Framework are implemented as **System Data** (not Demo Data) in `icofr/data/icofr_coso_data.xml`. This ensures the compliance framework is automatically populated upon module installation.

*   **COBIT 2019 Master Data:** The 40 Governance and Management Objectives of the COBIT 2019 Framework are implemented as **System Data** in `icofr/data/icofr_cobit_data.xml`. This ensures ITGC reference data is standardized and available upon installation.

*   **Control Workflow**: The `icofr.control` model implements a hierarchical review workflow (`draft` -> `waiting_l1_approval` -> `under_review` -> `waiting_l2_approval` -> `active`). 
    *   **Lini 1 (Operational)**: Staff submits, Unit Manager approves.
    *   **Lini 2 (Risk/ICOFR)**: Risk Officer verifies, Head of Risk gives final validation.
    This ensures a "4-Eyes Principle" at every line of defense.





### Known Issues / Gotchas

*   **Company Hierarchy:** Avoid setting `parent_id` for `res.company` in XML data after initial creation, as Odoo prevents hierarchy changes once data exists.

*   **External IDs:** Ensure wizards are defined before they are used in button actions to avoid `External ID not found` errors.


