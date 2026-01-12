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
- **Change Management Log (Appendix 6):** Audit-ready logging of all modifications to business processes and controls with before/after snapshots.
- **Aggregated Deficiency Evaluation:** Grouping mechanism to assess the collective impact of multiple control deficiencies.
- **ERP Integration for Audit Sampling:** Wizard-driven data pulling from Odoo GL (`account.move.line`) to ensure audit populations are grounded in actual transactions.
- **Audit Sampling Calculator:** Implementation of SK-BUMN Table 22 for sample size determination based on control frequency and risk level.
- **ITGC & COBIT 2019 Mapping:** Specific support for IT General Controls mapped to international standards.

### Key Components
...

### Key Models

- `icofr.control`: Internal controls registry with change history logging.

- `icofr.risk`: Financial risk matrix with integrated **Qualitative Factors (Tabel 11)**.

- `icofr.change.log`: Dedicated log for **Appendix 6** (Change Management) compliance.

- `icofr.testing`: Testing procedures and results (TOD, TOE, and Design Validation).

- `icofr.certification`: CEO/CFO certification workflow.

- `icofr.pojk.report`: Regulatory reporting with digital signature support.

- `icofr.audit.population`: Transaction population for audit sampling.

- `icofr.finding`: Findings documentation with **DoD Wizard** decision tree.

- `icofr.finding.group`: Aggregated evaluation of multiple small deficiencies.

- `icofr.materiality`: Calculation of thresholds with **Haircut Logic (Tabel 4)**.



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



### Known Issues / Gotchas

*   **Company Hierarchy:** Avoid setting `parent_id` for `res.company` in XML data after initial creation, as Odoo prevents hierarchy changes once data exists.

*   **External IDs:** Ensure wizards are defined before they are used in button actions to avoid `External ID not found` errors.


