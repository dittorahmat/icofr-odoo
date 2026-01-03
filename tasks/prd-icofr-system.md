# Product Requirements Document (PRD): ICOFR Odoo Module (POJK 15/2024)

## 1. Introduction/Overview
This document outlines the requirements for developing a comprehensive **Internal Control Over Financial Reporting (ICOFR)** module for Odoo 19.0. The system is designed to facilitate compliance with **POJK No. 15 Tahun 2024** and the **COSO 2013** framework for Indonesian State-Owned Enterprises (BUMN).

The module will serve as a governance, risk, and compliance (GRC) tool, digitizing the end-to-end ICOFR lifecycle—from scoping and design to self-assessment, independent evaluation, and regulatory reporting. It implements the "Three Lines of Defense" model, ensuring accountability across operational owners, risk management, and internal audit.

## 2. Goals
1.  **Full Regulatory Compliance:** Ensure all workflows and outputs align with SK-5/DKU.MBU/11/2024 standards.
2.  **Digitized "Three Lines" Workflow:** Enable seamless collaboration between Process Owners (L1), Risk/ICOFR Teams (L2), and Internal Audit (L3) within a single platform.
3.  **Centralized Repository:** Act as the "Single Source of Truth" for all Risk Control Matrices (RCM), Business Process Maps (BPM), and control evidence.
4.  **Automated Monitoring:** Provide real-time dashboards for control effectiveness, deficiency status, and remediation progress.
5.  **Efficiency:** Reduce manual administrative overhead for Control Self-Assessments (CSA) and audit reporting.

## 3. User Stories

### L1 - Process Owners (Operational Staff)
*   "As a Process Owner, I want to view the specific risks and controls assigned to my department so that I know what I am responsible for."
*   "As a Process Owner, I want to perform Control Self-Assessment (CSA) periodically by uploading evidence and rating effectiveness so that I can certify my controls are working."
*   "As a Process Owner, I want to receive notifications when a control deficiency is flagged so that I can implement a remediation plan."

### L2 - ICOFR/Risk Team (Middle Management)
*   "As an ICOFR Officer, I want to define and maintain the Risk Control Matrix (RCM) and Business Process Maps (BPM) so that the organization has a standardized control library."
*   "As an ICOFR Officer, I want to calculate materiality thresholds (Overall & Performance) based on financial data so that we can scope significant accounts and locations."
*   "As an ICOFR Officer, I want to validate the CSA results submitted by L1 (Test of One) to ensure their assessments are accurate."

### L3 - Internal Auditor
*   "As an Internal Auditor, I want to perform independent Test of Design (TOD) and Test of Operating Effectiveness (TOE) on key controls."
*   "As an Internal Auditor, I want to classify findings (Deficiency, Significant Deficiency, Material Weakness) based on the regulation's criteria."
*   "As an Internal Auditor, I want to generate the final Audit Opinion and Regulatory Report (Lampiran 11) for the Board."

### Management (CEO/CFO/Audit Committee)
*   "As a CFO, I want a high-level dashboard showing the overall effectiveness of ICOFR to sign off on the management assessment."

## 4. Functional Requirements

### 4.1. Master Data & Framework Setup
1.  **COSO/COBIT Structure:** System must allow users to define Principles, Components, and Attributes (user-input based on choice 3B).
2.  **Organization Structure:** Define Company, Hierarchy, and Process Owners (L1) mapped to Odoo Departments/Users.
3.  **Process Hierarchy:** Define Business Cycles (e.g., Order to Cash), Sub-processes, and Activities.

### 4.2. Phase 1: Scoping (Perancangan Scope)
4.  **Materiality Calculation:** Form to input/calculate Overall Materiality (OM) and Performance Materiality (PM) based on user-defined benchmarks (e.g., 5% of Profit Before Tax).
5.  **Account Scoping:** Ability to flag General Ledger accounts as "Significant" based on quantitative (Materiality) and qualitative factors.
6.  **Location/Unit Scoping:** Ability to select significant subsidiaries or business units for the ICOFR scope.

### 4.3. Phase 2: Design (Perancangan Control)
7.  **Risk Repository:** Register for Financial Reporting Risks (Assertions: Existence, Completeness, etc.) and Fraud Risks.
8.  **Control Repository (RCM):** Comprehensive form to define Controls with fields:
    *   Control Type (Manual/ITDM/Automated)
    *   Frequency (Daily/Monthly/Ad-hoc)
    *   Nature (Preventive/Detective)
    *   Linked Risk & Assertions
    *   Control Owner (User Link)
9.  **BPM Linkage:** Field to link/upload Business Process Flowcharts (PDF/Image) to specific processes.

### 4.4. Phase 3: Implementation (CSA - Control Self Assessment)
10. **CSA Scheduling:** System must generate periodic CSA tasks (e.g., Quarterly) for L1 owners.
11. **CSA Execution Interface:** Simple portal for L1 to:
    *   Mark status (Effective/Ineffective/No Transaction).
    *   Upload evidence documents.
    *   Add comments.
12. **L2 Validation:** Workflow for L2 to review L1's CSA. Options: "Validate (Pass)" or "Reject (Request Revision)".

### 4.5. Phase 4: Evaluation (Audit / TOD & TOE)
13. **Test of Design (TOD):** Form for L3/L2 to assess if the control design is logically sound.
14. **Test of Operating Effectiveness (TOE):** Form to record manual sample testing results.
    *   **Manual Selection:** Auditors/L3 will manually select samples from Odoo or external sources and record transaction IDs/references in the system.
    *   Sample Size calculator/guidance based on frequency (Tabel 22).
    *   Pass/Fail status per sample.
15. **Deficiency Classification:** Logic to classify failures as Control Deficiency, Significant Deficiency, or Material Weakness (as per Lampiran 10).

### 4.6. Phase 5: Remediation
16. **Issue Tracking:** Registry of all "Ineffective" controls.
17. **Action Plans:** Fields for "Root Cause," "Corrective Action," "Target Date," and "Person in Charge."
18. **Remediation Status:** Workflow to track status (Open -> In Progress -> Ready for Retest -> Closed).

### 4.7. Phase 6: Reporting
19. **Management Assessment Report:** Auto-generate the text for the CEO/CFO Statement (Lampiran 11) based on system data.
20. **Digital Signature Integration:** The final assessment report must integrate with a digital signature provider (e.g., Odoo Sign, Privy, or similar) for formal CEO/CFO sign-off.
21. **Deficiency Matrix:** Generate the "Degree of Deficiency" matrix.
22. **Dashboard:** Visual charts for:
    *   % Controls Tested.
    *   % Effective vs. Ineffective.
    *   Open Remediation Items.

## 5. Non-Goals (Out of Scope)
*   **Automated Transaction Selection:** The system will **not** automatically pull transaction records from other Odoo modules for sampling. Auditors will input sample references manually.
*   **Active Transaction Blocking:** The system will **not** block Odoo native transactions (e.g., confirming a Sale Order) based on ICOFR status. It is a documentation layer only.
*   **Pre-loaded Content:** The system will not come populated with specific industry risks or controls. The user must populate the RCM.
*   **AI Risk Detection:** No automated AI analysis of ledger data to find anomalies.

## 6. Success Metrics
*   **Completion Rate:** 100% of defined Significant Controls have a recorded CSA status by the quarter end.
*   **Audit Efficiency:** Reduction in time spent aggregating data for external auditors by 30%.
*   **Data Integrity:** Zero discrepancies between the RCM document and the actual testing sheets.

## 7. Technical Considerations
*   **Platform:** Odoo 19.0 (Enterprise or Community).
*   **Module Structure:**
    *   `icofr`: Core logic and master data.
    *   `icofr_report`: QWeb templates for regulatory outputs.
*   **Integration:** Must support API or module-level integration with digital signature providers.
*   **Access Control:** Strict ACLs are required. L1 cannot edit RCM definitions; L3 cannot edit L1's evidence after submission.
*   **Attachments:** Must support heavy document uploads (PDF, Excel) for evidence.

## 8. Open Questions
*   *(All initial open questions have been resolved)*
