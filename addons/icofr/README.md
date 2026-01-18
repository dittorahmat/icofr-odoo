# ICORF (Internal Controls Over Financial Reporting)

Modul ini menyediakan sistem untuk mengelola Internal Controls Over Financial Reporting (ICORF) sesuai dengan standar COSO 2013, regulasi **POJK No. 15 Tahun 2024** tentang Integritas Pelaporan Keuangan Bank, serta Juknis BUMN **SK-5/DKU.MBU/11/2024**.

## Fitur Utama

### 1. Kalkulator Materialitas & Scoping Akurat
- Fitur perhitungan materialitas otomatis untuk OM dan PM berdasarkan **Tabel 3 & 4 (Haircut Logic)**.
- **Alokasi Proporsional (Hal 115)**: Otomasi alokasi OM ke anak perusahaan berdasarkan proporsi aset.
- **Dokumentasi Konsultasi Auditor**: Log khusus untuk mencatat masukan auditor eksternal atas metodologi materialitas (Hal 16).
- **Analisis Aturan 2/3 Berbasis Nilai**: Verifikasi cakupan 66.7% berdasarkan kontribusi finansial riil (**Aset, Pendapatan, Beban, dan Liabilitas**) dari akun dan lokasi signifikan (Tabel 6).
- **Transisi Entitas Baru (FAQ 13)**: Flag khusus untuk mengecualikan anak perusahaan baru dari kewajiban evaluasi di tahun pertama akuisisi.

### 2. Manajemen Proses Bisnis Terstruktur (BPM)
- Dokumentasi langkah-langkah proses bisnis menggunakan simbol standar Lampiran 3 (*Manual, Automated, Interface, Output, Decision, Archive, Note*).
- **Visualisasi Alur**: Pemetaan titik risiko dan kontrol langsung pada setiap langkah aktivitas menggunakan model `icofr.process.step`.

### 3. Pengujian Kontrol & Sampling Engine
- **Kalkulator Sampling Otomatis**: Menghitung jumlah sampel berdasarkan Tabel 22 (TOE standar) dan **Tabel 23 (Remediasi)**, lengkap dengan persyaratan **Periode Pengujian Minimum** (misal: 3 bulan untuk kontrol bulanan).
- **Validasi Sampel Desember**: Penegakan sistem wajib menyertakan sampel bulan Desember/Kuartal IV untuk kontrol Bulanan/Kuartalan (Tabel 22 Note).
- Dokumentasi hasil pengujian TOD (Desain) dan TOE (Operasi) dengan checklist teknis lengkap (**Lampiran 8, Tabel 20 & 21**).

### 4. Manajemen Temuan & Penegakan Distribusi
- **DoD Wizard (7 Kotak)**: Wizard penentuan tingkat defisiensi (CD/SD/MW) yang presisi mengikuti alur 7 kotak **Lampiran 10 (Gambar 5)**, termasuk kriteria kualitatif *Prudent Official*.
- **Evaluasi Agregasi Lanjutan**: Pengelompokan temuan berdasarkan Akun, Proses, atau **Asersi Laporan Keuangan**, dengan dukungan **Kontrol Kompensasi Grup** untuk penurunan klasifikasi (Hal 69).
- **Penegakan Distribusi (Tabel 24)**: Validasi sistem untuk memastikan temuan MW/SD dilaporkan ke CEO, Board, dan Komite Audit sebelum ditutup.

### 5. Sertifikasi CEO/CFO Digital (Lampiran 11)
- Digitalisasi surat pernyataan efektivitas dengan checkbox wajib untuk 5 poin integritas.
- **Tabel Ringkasan Otomatis**: Rekapitulasi jumlah temuan MW, SD, dan CD secara real-time pada dokumen sertifikasi.

### 6. Manajemen Kontrol, ITGC & Spesialis
- **Dampak ITGC (FAQ 4)**: Otomasi deteksi kontrol otomatis yang tidak reliabel jika ITGC aplikasi pendukungnya Tidak Efektif.
- **Keamanan Siber (Hal 46)**: Tagging khusus untuk pengendalian ITGC yang memitigasi risiko cybersecurity.
- **Hierarki Level Pengendalian**: Kategorisasi formal ELC (Direct/Indirect/Monitoring) dan TLC sesuai Tabel 17-19.
- **Dukungan Spesialis & Pihak Ketiga**: Atribut khusus untuk validasi kredibilitas tenaga ahli, monitoring **SOC 1/2 Reports**, dan verifikasi **Right to Audit** vendor (Hal 30 & 40).

### 7. Pelaporan Lini Pertahanan (Line Reports)
- **Pelaporan Lini 3**: Narasi ringkasan eksekutif, rincian defisiensi, dan **Progres Remediasi Audit**.
- **Pelaporan Lini 2**: Rekonsiliasi perbandingan hasil pengujian dengan Lini 3 (Hal 61) dan rincian perubahan proses bisnis.

### 8. Whistleblowing & Penyesuaian Manajemen
- **Sistem Whistleblowing (WBS)**: Modul aduan terpadu dengan pelacakan disposisi unit dan integrasi ke temuan ICORF (Prinsip COSO 14).
- **Penyesuaian Manajemen (Hal 71)**: Pencatatan jurnal penyesuaian internal (Lini 1) sebagai mitigasi atas kontrol yang tidak efektif.

### 9. Excel-First & ERP Sync
- **Import Masif**: Fitur upload Excel untuk Financial Data, RCM, dan Account Mapping.
- **Sinkronisasi ERP**: Penarikan data saldo dan angka laporan keuangan langsung dari General Ledger Odoo.

## Panduan Penggunaan

### 1. Persiapan Awal
1. Instal modul ICORF dan aktifkan fitur multi-company jika diperlukan.
2. Atur **Kalkulator Materialitas** dan isi dokumentasi **Konsultasi Auditor Eksternal**.
3. Pastikan scoping mencapai ambang **Aturan 2/3** untuk seluruh metrik (Aset, Revenue, Beban, Liabilitas).

### 2. Dokumentasi RCM & BPM
1. Susun langkah-langkah aktivitas pada **Proses Bisnis** (BPM Terstruktur).
2. Identifikasi **Risiko** (sesuai Klaster BUMN Lampiran 2) dan rancang **Kontrol** (ELC/TLC).
3. Hubungkan kontrol otomatis dengan **Aplikasi Signifikan** dan pastikan status **ITGC** aplikasi tersebut efektif.

### 3. Pelaksanaan CSA & Testing
1. Lini 1 melakukan penilaian mandiri berkala melalui menu **CSA**.
2. Lini 3 menjalankan pengujian operasional (**TOE**) dengan memastikan adanya **Sampel Desember**.
3. Jika ditemukan salah saji, catat pada menu **Penyesuaian Manajemen** untuk memitigasi dampak sebelum laporan diterbitkan.

### 4. Penanganan Defisiensi
1. Catat temuan dan tentukan klasifikasi menggunakan wizard **DoD**.
2. Gunakan menu **Evaluasi Agregat** untuk menilai dampak gabungan berdasarkan **asersi**.
3. Pastikan MW/SD dilaporkan ke Komite Audit sebelum status diubah menjadi ditutup.

### 5. Finalisasi & Sertifikasi
1. Tinjau laporan rekonsiliasi Lini 2 vs Lini 3.
2. Buat dokumen **Sertifikasi ICORF** tahunan.
3. CEO/CFO melakukan review poin integritas dan menandatangani secara digital.

## Peran Pengguna
- **CFO/CEO**: Sertifikasi akhir dan pelaporan integritas keuangan.
- **Internal Audit (Lini 3)**: Pengujian independen, klasifikasi defisiensi, dan pemantauan remediasi.
- **Tim Risiko/ICOFR (Lini 2)**: Scoping, pemeliharaan RCM, verifikasi desain, dan rekonsiliasi hasil.
- **Process Owner (Lini 1)**: Operasional harian, penilaian mandiri (CSA), dan penyesuaian angka laporan.

## Dukungan
Silakan hubungi admin sistem atau konsultan implementasi ICOFR untuk bantuan teknis.
