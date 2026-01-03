## Relevant Files

- `addons/icofr/models/icofr_pojk_report.py` - Core model for the regulatory report; needs Digital Signature logic.
- `addons/icofr/views/pojk_report_views.xml` - Views for the report; needs "Sign Now" button.
- `addons/icofr/models/icofr_testing.py` - Testing model; needs distinct TOD/TOE types and fields.
- `addons/icofr/views/testing_views.xml` - Testing views; needs structural update for TOD vs TOE.
- `addons/icofr/models/icofr_audit_population.py` - Population model; needs better linkage to Testing.
- `addons/icofr/views/audit_population_views.xml` - Population views.
- `addons/icofr/data/icofr_data.xml` - Master data; ensuring defaults match new requirements.

### Notes

- **Digital Signature:** For MVP, we will use Odoo's standard `portal.mixin` / `sign` concepts if available, or simulate a robust digital signature flow (e.g., storing a hash + timestamp + user ID as a "signature") if external providers are not configured. The PRD mentions "integration with digital signature provider", so we will add hooks for this.
- **TOD vs TOE:** Currently `test_type` has `compliance`, `substantive`, `walkthrough`. We need to map these or replace them to strictly follow `Test of Design` and `Test of Operating Effectiveness`.

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, you must check it off in this markdown file by changing `- [ ]` to `- [x]`. This helps track progress and ensures you don't skip any steps.

Example:
- `- [ ] 1.1 Read file` → `- [x] 1.1 Read file` (after completing)

Update the file after completing each sub-task, not just after completing an entire parent task.

## Tasks

- [x] 0.0 Create feature branch
  - [x] 0.1 Create and checkout a new branch `feature/icofr-refinement`

- [x] 1.0 Implement Digital Signature Integration for POJK Reports
  - [x] 1.1 Modify `icofr.pojk.report` model to add signature fields (`signed_by`, `signed_date`, `signature_hash`, `signature_image`).
  - [x] 1.2 Implement a `action_sign_report` method that captures the current user's signature (simulated or via widget) and freezes the report state.
  - [x] 1.3 Update `icofr.pojk.report` form view to show a "Sign Report" button for the CEO/CFO when status is 'approved'.
  - [x] 1.4 Add a logical check: Report cannot be modified after signing.

- [x] 2.0 Refine Testing Module for Explicit TOD & TOE Workflows
  - [x] 2.1 Modify `icofr.testing` model: Update `test_type` selection to include `tod` (Test of Design) and `toe` (Test of Operating Effectiveness).
  - [x] 2.2 Add specific fields for TOD: `design_description`, `design_conclusion` (Effective/Ineffective).
  - [x] 2.3 Add specific fields for TOE: `population_reference`, `sample_selection_method`, `testing_steps`, `exceptions_noted`.
  - [x] 2.4 Update `icofr.testing` form view to conditionally show TOD vs TOE fields based on `test_type`.
  - [x] 2.5 Ensure `sample_size_calculated` logic in `icofr.testing` is applied primarily when `test_type` is `toe`.

- [x] 3.0 Enhance Audit Sampling & Population Selection UI
  - [x] 3.1 Modify `icofr.audit.population` to allow bulk selection of records to be "linked" to a specific `icofr.testing` record (currently it links one-by-one or via upload).
  - [x] 3.2 Create a wizard `icofr.sample.selection.wizard` that allows an auditor to:
    - Select a `icofr.testing` record (TOE).
    - Filter `icofr.audit.population` records.
    - Randomly or manually select $N$ records.
    - Link them to the test.
  - [x] 3.3 Update `icofr.testing` view to show a smart button or notebook tab listing the specific "Selected Samples" from the population.

- [x] 4.0 Compliance Polish (POJK 15/2024 & SK BUMN Alignment)
  - [x] 4.1 Verify `icofr.control` model has all specific SK BUMN attributes (Assertions are already there, check for `risk_level` alignment with Table 22).
  - [x] 4.2 Ensure `icofr.finding` model correctly maps "Deficiency" -> "Significant Deficiency" -> "Material Weakness" logic (Review `_compute_deficiency_classification`).
  - [x] 4.3 Add a "Generate CEO Statement" button on `icofr.pojk.report` that populates the `management_response_detail` with the standard legal text from Lampiran 11.

- [x] 5.0 Final System Verification & Data flow Test
  - [x] 5.1 Verify flow: Upload Population -> Create TOE Test -> Select Samples -> Record Result -> Create Finding -> Remediation.
  - [x] 5.2 Verify flow: Create Report -> Approve -> Digital Sign -> Lock.
