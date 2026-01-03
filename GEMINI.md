# ICORF Odoo Module (POJK 15/2024)

## Project Overview
This project is an Odoo 19.0 module designed for **Internal Controls Over Financial Reporting (ICORF)**. It ensures compliance with **POJK No. 15 Tahun 2024** (Indonesian Financial Services Authority regulation) and follows the **COSO 2013** framework.

The system implements the **Three Lines of Defense** model:
1.  **First Line (Lini 1):** Process Owners (Operational).
2.  **Second Line (Lini 2):** Risk Management/ICORF Team (Monitoring).
3.  **Third Line (Lini 3):** Internal Audit (Independent Assurance).

### Key Components
-   **Core Module:** `addons/icofr/` containing all business logic, views, and reports.
-   **Demo Data:** `addons/icofr_demo/` and `addons/icofr_demo_new_features/` containing comprehensive scenarios for testing.
-   **Frameworks:** COSO 2013, COBIT 2019 (ITGC), POJK 15/2024.

## Architecture & Structure
The project follows a standard Odoo addon structure, containerized via Docker.

### Directory Layout
-   `addons/icofr/`: Main application code.
    -   `models/`: Python business logic (Controls, Risks, Testing, Certification).
    -   `views/`: XML definitions for UI (Forms, Lists, Kanban, Graphs).
    -   `security/`: Access control lists (`ir.model.access.csv`) and Record Rules (`security.xml`).
    -   `data/`: Initial data and demo data.
    -   `reports/`: QWeb report templates (PDF/Excel).
-   `addons/icofr_demo/`: Specialized module for loading pre-validated demo scenarios.
-   `docker-compose.yml`: Orchestrates Odoo 19.0 and PostgreSQL 15 services.

### Key Models

- `icofr.control`: Internal controls registry.

- `icofr.risk`: Financial risk matrix.

- `icofr.testing`: Testing procedures and results (TOD and TOE).

- `icofr.certification`: CEO/CFO certification workflow.

- `icofr.pojk.report`: Regulatory reporting with digital signature support.

- `icofr.audit.population`: Transaction population for audit sampling.



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

*   **Testing Workflows:** `icofr.testing` must distinguish between `tod` (Test of Design) and `toe` (Test of Operating Effectiveness).

*   **Sampling:** Use `icofr.sample.selection.wizard` for bulk linking of population records to TOE tests.

*   **Batch Creation:** Always handle `vals_list` in `create()` overrides to support XML imports.



### Known Issues / Gotchas

*   **Company Hierarchy:** Avoid setting `parent_id` for `res.company` in XML data after initial creation, as Odoo prevents hierarchy changes once data exists.

*   **External IDs:** Ensure wizards are defined before they are used in button actions to avoid `External ID not found` errors.


