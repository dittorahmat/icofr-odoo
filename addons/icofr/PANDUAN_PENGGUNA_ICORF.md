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

### 2.2 Dokumentasi BPM/SOP
*   **Menu:** `ICORF > Master Data > Proses Bisnis`
*   Unggah Flowchart BPM sesuai Lampiran 4.

---

## 3. Fase 2: Scoping & Materialitas
### 3.1 Aturan 2/3 (Scoping Coverage)
*   **Status "LULUS":** Hanya tercapai jika cakupan akun signifikan >= 66.7% pada 4 metrik finansial utama (Aset, Pendapatan, Beban, Liabilitas).

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
### 6.1 Mandatory December Sample
*   Sistem mewajibkan sampel dari bulan Desember untuk pengujian frekuensi bulanan/kuartalan (Tabel 22).

### 6.2 Prosedur Roll-forward
*   Wajib dilakukan untuk pengujian interim agar hasil valid hingga 31 Desember.

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