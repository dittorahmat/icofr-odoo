# Panduan Pengguna Komprehensif: Modul ICORF Odoo
**Versi:** 1.3 (Perfect Gold Standard - POJK 15/2024 & SK-5/DKU.MBU/11/2024)

## Daftar Isi
1. [Pendahuluan & Kerangka Kerja](#1-pendahuluan--kerangka-kerja)
2. [Fase 1: Persiapan Data Master & ELC](#2-fase-1-persiapan-data-master--elc)
3. [Fase 2: Scoping & Materialitas](#3-fase-2-scoping--materialitas)
4. [Fase 3: ITGC, EUC & Service Organization](#4-fase-3-itgc-euc--service-organization)
5. [Fase 4: Manajemen Risiko & Kontrol (RCM)](#5-fase-4-manajemen-risiko--kontrol-rcm)
6. [Fase 5: Operasional Pengujian (Testing)](#6-fase-5-operasional-pengujian-testing)
7. [Fase 6: Temuan & Remediasi](#7-fase-6-temuan--remediasi)
8. [Fase 7: Pelaporan DoD & Audit Dossier](#8-fase-7-pelaporan-dod--audit-dossier)

---

## 1. Pendahuluan & Kerangka Kerja
Modul ini memastikan organisasi mematuhi standar **Internal Control over Financial Reporting (ICORF)** dengan integrasi kerangka:
*   **COSO 2013:** Untuk kontrol bisnis (ELC & TLC).
*   **COBIT 2019:** Untuk maturity level kontrol IT.
*   **Three Lines of Defense:** Pemisahan tugas Lini 1, Lini 2, dan Lini 3.

---

## 2. Fase 1: Persiapan Data Master & ELC
### 2.1 Evaluasi ELC (Entity Level Control)
*   **Menu:** `ICORF > Operasional > Evaluasi ELC (COSO 17)`
*   **Tujuan:** Menilai 17 prinsip COSO secara kualitatif. Jika terdapat prinsip yang "Tidak Efektif", status ELC secara keseluruhan akan menjadi *Material Weakness*.

### 2.2 Pemetaan Akun GL-FSLI (Template Laporan)
*   **Menu:** `ICORF > Master Data > Pemetaan Akun GL-FSLI`
*   **Upload Excel:** Klik tombol **"Import Template Laporan (Excel)"** di bagian atas daftar (List View). Gunakan file `Input_Data-Template Laporan` untuk membangun struktur FSLI per entitas.
*   **Field Penting:** Kode BSPL, Kategori (Neraca/Laba Rugi), Sub-Kategori (Aset/Kewajiban/dll), dan Kode Entity (Induk/Anak).

### 2.3 Dokumentasi BPM/SOP
*   **Menu:** `ICORF > Master Data > Proses Bisnis`
*   Unggah Flowchart BPM sesuai Lampiran 4.

---

## 3. Fase 2: Scoping & Materialitas
### 3.1 Kalkulator Materialitas (OM, PM, SAD)
*   **Menu:** `ICORF > Master Data > Kalkulator Materialitas`
*   **Import Saldo GL:** Klik tombol **"Import General Ledger (Excel)"** di bagian atas daftar (List View). Pilih file `Input_Data-General_Ledger`. Sistem akan mencocokkan saldo ke FSLI berdasarkan `Kode_Entity` + `Kode_FSLI`.
*   **Overall Materiality (OM):** Tentukan basis (Pendapatan/Aset). Persentase standar 0.5% - 5% (Tabel 3).
*   **Performance Materiality (PM):** Ditentukan oleh **Haircut Logic** (Tabel 4). Risiko Rendah (Haircut 20% -> PM 80% OM), Risiko Tinggi (Haircut 55% -> PM 45% OM).
*   **Ambang Batas SAD (Clearly Trivial):** Otomatis dihitung 3% dari OM (Hal 17) untuk mengabaikan kesalahan kecil.
*   **Multiplier Grup (Tabel 25):** Untuk entitas konsolidasi, multiplier (1.0x - 9.0x) digunakan untuk alokasi OM ke anak perusahaan.

### 3.2 Aturan 2/3 (Scoping Coverage Analysis)
*   **Status "LULUS":** Hanya tercapai jika cakupan akun signifikan >= 66.7% pada 4 metrik finansial utama (Aset, Pendapatan, Beban, Liabilitas) sesuai Tabel 6.
*   **Analisis Lokasi:** Sistem juga memverifikasi cakupan 2/3 pada tingkat entitas/anak perusahaan signifikan.

---

## 4. Fase 3: ITGC, EUC & Service Organization
### 4.1 Maturity Score ITGC
*   **Menu:** `ICORF > Master Data > Aplikasi`
*   Tentukan skor kematangan (0-5) berbasis COBIT untuk setiap aplikasi signifikan.

### 4.2 SOC Reports & Bridge Letters
*   **Menu:** `ICORF > Master Data > Organisasi Layanan`
*   Catat evaluasi atas laporan SOC 1 Type 2 dan verifikasi keberadaan **Bridge Letter** untuk menutupi celah periode audit.

---

## 5. Fase 4: Manajemen Risiko & Kontrol (RCM)
### 5.1 Register EUC & IPE
*   **Menu:** `ICORF > Register Pendukung > Register EUC / IPE`
*   **EUC (Spreadsheet):** Wajib memenuhi 5 kriteria kontrol jika kompleksitas "Tinggi".

---

## 6. Fase 5: Operasional Pengujian (Testing)
### 6.1 Metode & Sampling
*   **Metode Pengujian (Gambar 4):** Pilih antara *Inquiry, Observation, Inspection,* atau *Reperformance*.
*   **Kontak Personil (Lampiran 7):** Auditor wajib mendokumentasikan personil Lini 1 yang terlibat dalam sampel pengujian pada tab "Personil & Skenario ITAC".
*   **Mandatory December Sample:** Sistem akan memblokir penyelesaian pengujian jika tidak ada sampel Desember (Tabel 22).

### 6.2 Pengujian Otomatis (ITAC)
*   Untuk kontrol otomatis, gunakan tabel **"Skenario ITAC"** untuk mencatat pengujian negatif/positif, hasil yang diharapkan, dan hasil aktual sesuai Lampiran 7 (Hal 101).

### 6.3 Prosedur Roll-forward

---

## 7. Fase 6: Temuan & Remediasi
### 7.1 Remediation Lock
*   Sistem memblokir *Retest* kontrol yang diremediasi hingga masa tunggu (30-180 hari) terlampaui sesuai frekuensi kontrol (Tabel 23).

---

## 8. Fase 7: Pelaporan DoD & Audit Dossier
### 8.1 Kertas Kerja DoD (Lampiran 10)
*   **Menu:** `ICORF > Pelaporan > Evaluasi Agregat`
*   Generate matriks 7 kolom untuk klasifikasi defisiensi akhir tahun.

### 8.2 Audit Dossier (Bundel Dokumen)
*   **Menu:** `ICORF > Pelaporan > Dossier Audit (Bundle)`
*   Fitur otomatis untuk mengumpulkan seluruh dokumen bukti audit (RCM, Flowchart, Testing, Sertifikasi) ke dalam satu paket final (Lampiran 12).

---
*Dokumen ini diperbarui untuk memastikan kepatuhan 100% Perfect Gold Standard terhadap regulasi BUMN & OJK.*