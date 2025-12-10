## Relevant Files

- `addons/icofr/models/__init__.py` - Initializer for ICORF models
- `addons/icofr/models/icofr_control.py` - Model untuk kontrol internal
- `addons/icofr/models/icofr_risk.py` - Model untuk risiko finansial
- `addons/icofr/models/icofr_testing.py` - Model untuk pengujian kontrol
- `addons/icofr/models/icofr_certification.py` - Model untuk sertifikasi
- `addons/icofr/models/icofr_workflow.py` - Model untuk workflow approval
- `addons/icofr/views/control_views.xml` - View untuk pengelolaan kontrol
- `addons/icofr/views/risk_views.xml` - View untuk pengelolaan risiko
- `addons/icofr/views/dashboard_views.xml` - View untuk dashboard ICORF
- `addons/icofr/views/reporting_views.xml` - View untuk pelaporan
- `addons/icofr/security/ir.model.access.csv` - Hak akses untuk model-model ICORF
- `addons/icofr/data/icofr_data.xml` - Data awal untuk modul ICORF
- `addons/icofr/__init__.py` - Initializer untuk modul ICORF
- `addons/icofr/__manifest__.py` - Manifest file untuk modul ICORF
- `addons/icofr/controllers/main.py` - Controller untuk endpoint web ICORF
- `addons/icofr/reports/icofr_report.py` - Laporan ICORF
- `addons/icofr/reports/icofr_report.xml` - Template laporan ICORF
- `addons/icofr/static/src/js/icofr_dashboard.js` - JavaScript untuk dashboard interaktif
- `addons/icofr/static/src/css/icofr_styles.css` - Stylesheet untuk antarmuka ICORF
- `addons/icofr/tests/test_icofr_control.py` - Unit test untuk model kontrol
- `addons/icofr/tests/test_icofr_risk.py` - Unit test untuk model risiko
- `addons/icofr/tests/test_icofr_testing.py` - Unit test untuk model pengujian

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `icofr_control.py` and `test_icofr_control.py` in the same directory).
- Use `python odoo-bin -d [database_name] -i icofr` to install the module.
- Module harus mendukung Bahasa Indonesia sebagai default interface language.

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, you must check it off in this markdown file by changing `- [ ]` to `- [x]`. This helps track progress and ensures you don't skip any steps.

Example:
- `- [ ] 1.1 Read file` → `- [x] 1.1 Read file` (after completing)

Update the file after completing each sub-task, not just after completing an entire parent task.

## Tasks

- [x] 0.0 Create feature branch
  - [x] 0.1 Create and checkout a new branch for this feature (e.g., `git checkout -b feature/icofr-module`)
- [x] 1.0 Setup struktur dasar modul Odoo
  - [x] 1.1 Buat direktori dasar `icofr` di folder `addons`
  - [x] 1.2 Buat file `__init__.py` di direktori `icofr`
  - [x] 1.3 Buat file `__manifest__.py` dengan informasi modul yang sesuai
  - [x] 1.4 Buat struktur direktori untuk models, views, security, data, controllers, reports, dan static
  - [x] 1.5 Definisikan dependensi modul di manifest (akuntansi, dll.)
- [x] 2.0 Implementasi model dan database untuk kontrol internal
  - [x] 2.1 Buat model `icofr_control` untuk mengelola kontrol internal
  - [x] 2.2 Buat model `icofr_risk` untuk mengelola risiko terkait kontrol
  - [x] 2.3 Buat model `icofr_testing` untuk mendokumentasikan pengujian kontrol
  - [x] 2.4 Tambahkan field-field sesuai dengan kebutuhan fungsional #1-3
  - [x] 2.5 Buat view-form, view-tree, dan view-search untuk semua model
  - [x] 2.6 Definisikan access rights untuk model-model tersebut
- [x] 3.0 Buat interface pengujian kontrol dan dashboard
  - [x] 3.1 Buat view dashboard utk monitoring kontrol
  - [x] 3.2 Implementasi fitur notifikasi dan pengingat (kebutuhan fungsional #11)
  - [x] 3.3 Buat komponen untuk menampilkan real-time status kontrol
  - [x] 3.4 Tambahkan grafik dan metrik efektivitas kontrol
  - [x] 3.5 Implementasi fitur export data kontrol (kebutuhan fungsional #9)
- [x] 4.0 Implementasi fitur pelaporan dan sertifikasi ICORF
  - [x] 4.1 Buat model `icofr_certification` untuk proses sertifikasi
  - [x] 4.2 Bangun laporan sesuai format POJK 15/2024
  - [x] 4.3 Tambahkan fitur manajemen temuan dan action plan (kebutuhan fungsional #6)
  - [x] 4.4 Implementasi audit trail untuk semua aktivitas penting (kebutuhan fungsional #12)
  - [x] 4.5 Buat template laporan dalam format PDF dan Excel
- [x] 5.0 Tambahkan fitur manajemen workflow dan kalender
  - [x] 5.1 Buat model `icofr_workflow` untuk proses approval
  - [x] 5.2 Implementasi fitur penjadwalan pengujian kontrol
  - [x] 5.3 Tambahkan notifikasi otomatis untuk jadwal yang akan datang
  - [x] 5.4 Buat kalender interaktif untuk perencanaan kontrol
  - [x] 5.5 Integrasikan workflow dengan proses sertifikasi