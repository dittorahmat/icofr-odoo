# ICORF (Internal Controls Over Financial Reporting) - Odoo Module

A comprehensive Odoo module for managing Internal Controls Over Financial Reporting (ICORF) that helps organizations, especially financial institutions and BUMNs in Indonesia, comply with **POJK No. 15 Tahun 2024** and **SK-5/DKU.MBU/11/2024**.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Overview

The ICORF module implements the COSO 2013 Internal Control framework and complies with POJK 15/2024 and Ministry of BUMN technical guidelines. It supports documentation, testing, reporting, and certification of internal controls, facilitating executive certifications (CEO/CFO) and audit readiness.

### Regulatory Framework
- **COSO Framework 2013**: Five-component internal control framework.
- **POJK No. 15 Tahun 2024**: Indonesian OJK regulation on Financial Reporting Integrity.
- **SK-5/DKU.MBU/11/2024**: Ministry of BUMN technical guidelines for ICOFR.

## Features

- **Materiality Calculator**: Automatic calculation of Overall Materiality and Performance Materiality with **External Auditor Consultation** tracking (Hal 16) and **Tabel 3 & 4 Haircut Logic**.
- **Financial-Based Scoping Analysis**: Precision verification of the **2/3 Rule** (66.7% coverage) for accounts and locations based on **Aset, Revenue, Expense, and Liability contribution** (Tabel 6).
- **Newly Acquired Entity Transition**: Specialized support for **FAQ 13** logic to manage the transition period for newly acquired subsidiaries.
- **Structured BPM Engine**: Digital documentation of business processes using standardized legends from **Lampiran 3 & 4** (Manual, Automated, Interface, Archive, Note).
- **Group Multiplier Engine**: Automated materiality multiplier calculation (1.5x to 9x) for consolidation based on **Tabel 25**.
- **Audit Sampling Engine**: Precision calculator implementing **Tabel 22** (TOE) and **Tabel 23** (Remediation) with **Minimum Testing Period** requirements and **Mandatory December/Q4 Sample** enforcement.
- **DoD Wizard**: Advanced decision tree following the **7-Box Logic (Lampiran 10 / Gambar 5)** for precise deficiency classification (CD/SD/MW) with **Prudent Official** override support.
- **ITGC Impact Logic**: Automatic detection of unreliable automated controls if the supporting system's ITGC is Ineffective (**FAQ 4**).
- **Technical Attribute Matrix**: Specialized fields for **ITGC Areas**, **EUC Complexity**, **IPE Types**, **MRC Precision**, and **IPO (C, A, V, RA)**.
- **Finding Distribution Enforcement**: Automated validation ensuring MW/SD findings are reported to the CEO, Board, and Audit Committee as per **Tabel 24**.
- **Aggregated Deficiency Evaluation**: Grouping mechanism to assess collective impact with **Assertion** grouping basis and **Group Compensating Control** support (Hal 69).
- **Management Adjustments (Hal 71)**: Module to record both External and Internal Management Adjustments as deficiency indicators or mitigating measures.
- **Certification Process**: Digitized **Lampiran 11** with automated finding tables and mandatory point-by-point integrity acknowledgment.
- **Three Lines of Defense Reporting**: Specialized reports for Lini 1, 2, and 3, including **Lini 2 vs Lini 3 Comparison** (Hal 61) and **Audit Remediation Progress**.
- **Whistleblowing System (WBS)**: Enhanced module for aduan management with disposition tracking and finding integration (Principle 14).
- **Service Organization Monitoring**: Manage third-party vendors and track **SOC 1/2 Type II Reports** with Gap Analysis, Bridge Letter, and **Right to Audit** verification (**Bab III Pasal 4.3**).

## Prerequisites

- **Docker** and **Docker Compose**
- **Odoo 19.0** Community Edition

## Installation

### Docker Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/icofr-odoo.git
   cd icofr-odoo
   ```

2. Build and start services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access Odoo via browser at `http://localhost:8069`

## Usage

### Quick Start
1. Set up **Materiality** and **Scoping** (Aset, Revenue, Beban, Liabilitas).
2. Document **Business Processes** using structured steps (BPM).
3. Define **Risks** and link them to **Internal Controls**.
4. Perform **CSA** (Lini 1) and **Testing** (Lini 3) with **December Sample** check.
5. Manage **Findings** and perform **Aggregated Evaluation** by Assertion.
6. Execute **CEO/CFO Certification**.

## License

This project is licensed under the LGPL-3.0. 

## About the Project

Developed to address the specific needs of Indonesian financial institutions and BUMNs in implementing Internal Controls Over Financial Reporting (ICORF) as required by POJK No. 15 Tahun 2024 and SK BUMN 2024.
