# ICORF Demo New Features Module

## Overview
The ICORF Demo New Features module provides sample data for demonstrating the NEW features added to the ICORF (Internal Controls Over Financial Reporting) module. This module is specifically designed to showcase the enhanced capabilities that were added following the PwC recommendations and requirements from POJK No. 15 Tahun 2024.

## Features Covered
This module includes sample data for:

1. **Materiality Calculator**: Automatic calculation of Overall Materiality and Performance Materiality
2. **Account Mapping**: GL to FSLI (Financial Statement Line Item) mapping functionality
3. **Control Self-Assessment (CSA)**: Complete workflow for Control Self-Assessment process
4. **Deficiency Classification**: Automated classification of control deficiencies based on quantitative and qualitative factors
5. **Three Lines of Defense**: Complete role separation for Lini 1 (Process Owners), Lini 2 (Risk/ICOFR Team), and Lini 3 (Internal Auditors)
6. **Copy Period Functionality**: Sample data demonstrating the copy period feature for efficiency
7. **SK BUMN Compliance**: Complete compliance with Surat Keputusan BUMN requirements and attributes

## Purpose
This module is intended for:
- Demonstrating new features to stakeholders
- Providing realistic dataset for training on new functionality
- Facilitating hands-on learning sessions for advanced features
- Showcasing Three Lines of Defense implementation
- Demonstrating deficiency classification and quantification

## Data Provided
The module includes sample data based on scenarios 12-16 from the ICORF Demo Scenarios document:

1. **Scenario 12**: Materiality calculations and account mapping (SK BUMN compliance)
2. **Scenario 13**: Control Self-Assessment process with proper workflow
3. **Scenario 14**: Deficiency classification with quantitative impact assessment
4. **Scenario 15**: Copy Period functionality demonstration for efficiency
5. **Scenario 16**: Three Lines of Defense implementation with role assignments

## Usage
1. Install the `icofr_demo_new_features` module after installing `icofr_demo` and `icofr`
2. The demo data will be automatically loaded when the module is installed
3. Navigate through the ICORF menus to explore the new feature demonstrations
4. Use the sample data to practice new workflows and understand enhanced system capabilities

## Dependencies
- This module requires the `icofr` and `icofr_demo` modules to be installed
- Standard Odoo `base` module
- References data from the main `icofr_demo` module to maintain consistency

## Enhanced User Roles
- `line1_process_owner` (Lini 1 - Process Owner)
- `line2_risk_manager` (Lini 2 - Risk Manager) 
- `line3_internal_auditor` (Lini 3 - Internal Auditor)

## New Demonstrations
- Materiality calculation interfaces and results
- GL to FSLI mapping workflow and validation
- CSA process from initiation to approval
- Automated deficiency classification and impact quantification
- Three Lines of Defense role separation in practice
- Copy Period functionality for improving efficiency

## Important Notes
- The demo data is intended for demonstration of new features only
- Do not use this data in production environments
- This module extends the functionality showcased in the main `icofr_demo` module
- All demo data can be safely removed when uninstalling the module

## Integration with Main Demo
The data in this module builds upon and integrates with the main ICORF demo data to provide a coherent demonstration of the full system capabilities including the new features.