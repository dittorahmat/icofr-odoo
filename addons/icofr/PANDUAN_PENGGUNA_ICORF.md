# Panduan Pengguna Komprehensif: Modul ICORF Odoo
**Versi:** 1.4 (Final Gold Standard - Compliance 100% SK BUMN)

## Daftar Isi
1. [Pendahuluan & Kerangka Kerja](#1-pendahuluan--kerangka-kerja)
2. [Fase 1: Persiapan Data Master & ELC](#2-fase-1-persiapan-data-master--elc)
3. [Fase 2: Scoping & Materialitas (Holding & Subsidiaries)](#3-fase-2-scoping--materialitas-holding--subsidiaries)
4. [Fase 3: ITGC, EUC & Service Organization (SOC)](#4-fase-3-itgc-euc--service-organization-soc)
5. [Fase 4: Manajemen Risiko & Matriks Kontrol (RCM)](#5-fase-4-manajemen-risiko--matriks-kontrol-rcm)
6. [Fase 5: Operasional Pengujian (Testing & Roll-forward)](#6-fase-5-operasional-pengujian-testing--roll-forward)
7. [Fase 6: Temuan & Agregasi Defisiensi](#7-fase-6-temuan--agregasi-defisiensi)
8. [Fase 7: Sertifikasi & Surat Pernyataan Direksi](#8-fase-7-sertifikasi--surat-pernyataan-direksi)
9. [Fase 8: Dashboard Maturity & Audit Dossier](#9-fase-8-dashboard-maturity--audit-dossier)

---

## 1. Pendahuluan & Kerangka Kerja
Modul ini memastikan organisasi mematuhi standar **Internal Control over Financial Reporting (ICORF)** sesuai **SK-5/DKU.MBU/11/2024** dengan integrasi:
*   **COSO 2013:** 17 Prinsip untuk kontrol bisnis (ELC & TLC).
*   **COBIT 2019:** Maturity level 0-5 untuk kontrol IT.
*   **Holding Structure:** Mendukung alokasi materialitas grup ke anak perusahaan (Tabel 25).

---

## 2. Fase 1: Persiapan Data Master & ELC
### 2.1 Evaluasi ELC (Entity Level Control)
*   **Menu:** `ICORF > Operasional > Evaluasi ELC (COSO 17)`
*   **Dashboard Maturity:** Gunakan view **Graph/Radar** untuk melihat tren kematangan ELC antar tahun.

### 2.2 Pemetaan Akun GL-FSLI (Template Laporan)
*   **Menu:** `ICORF > Master Data > Pemetaan Akun GL-FSLI`
*   **Upload Excel:** Klik **"Import Template Laporan (Excel)"**. Gunakan format kolom: `Kode_Entity, Kode_BSPL, Kategori, Sub_Kategori, Kode_FSLI, Deskripsi_FSLI`.

---

## 3. Fase 2: Scoping & Materialitas (Holding & Subsidiaries)
### 3.1 Kalkulator Materialitas (OM, PM, SAD)
*   **Import Saldo GL:** Klik **"Import General Ledger (Excel)"**. Kolom wajib: `Kode_Entity, No_GL, GL_Desc, GL_Balance, Kode_FSLI`.
*   **Haircut Logic:** PM otomatis dihitung berdasarkan tingkat risiko (Haircut 20% atau 55%).

### 3.2 Scoping Lokasi (Tabel 10) & Alokasi (Hal 115)
*   **Scoping Lokasi:** Klik tombol **"Scoping Lokasi (Tabel 10)"**. Sistem akan menandai anak perusahaan sebagai "Signifikan" jika kontribusi Aset/Revenue > PM Grup.
*   **Alokasi:** Klik **"Alokasi ke Anak Perusahaan"**. Sistem menggunakan **Multiplier Tabel 25** (1.5x s/d 9.0x) untuk menghitung jatah OM masing-masing entitas.

---

## 4. Fase 3: ITGC, EUC & Service Organization (SOC)
### 4.1 Maturity Score ITGC
*   **Menu:** `ICORF > Master Data > Aplikasi`
*   Pantau gap kematangan sistem melalui **Maturity Radar Chart**.

### 4.2 Organisasi Jasa (SOC 1/2/3)
*   **Menu:** `ICORF > Master Data > Organisasi Jasa (SOC)`
*   Wajib mencatat opini auditor (Unqualified/dll) dan status **Bridge Letter** jika laporan SOC tidak mengcover hingga akhir tahun fiskal (Hal 56).

---

## 5. Fase 4: Manajemen Risiko & Matriks Kontrol (RCM)
### 5.1 Risk Control Matrix (RCM) - Lampiran 4
*   **Cetak RCM:** Buka daftar kontrol, pilih kontrol, lalu klik **Print > Risk Control Matrix (Lampiran 4)**. 
*   Laporan ini menyandingkan Risiko, Fraud Flag, Aktivitas Kontrol, Asersi, dan IPO dalam satu tabel.

---

## 6. Fase 5: Operasional Pengujian (Testing & Roll-forward)
### 6.1 Mandatory December Sample & Cooling-off
*   **December Sample:** Sistem memblokir status 'Selesai' jika frekuensi bulanan tidak memiliki sampel Desember.
*   **Cooling-off (Hal 19):** Auditor dilarang menguji kontrol yang pernah mereka miliki/kelola dalam 12 bulan terakhir.

### 6.2 Wizard Roll-forward (Hal 51)
*   **Tujuan:** Memutakhirkan hasil pengujian interim (Jan-Sept) agar mengcover setahun penuh.
*   **Cara:** Buka record pengujian interim yang sudah disetujui, klik tombol **"Roll-forward"**. Sistem akan membuat draf pengujian baru untuk periode pemutakhiran.

---

## 7. Fase 6: Temuan & Agregasi Defisiensi
### 7.1 Evaluasi Agregat (Tabel 17)
*   **Menu:** `ICORF > Operasional > Evaluasi Defisiensi Agregat`
*   Gabungkan beberapa temuan kecil pada akun/proses yang sama untuk melihat apakah secara kolektif menjadi *Significant Deficiency*.

---

## 8. Fase 7: Sertifikasi & Surat Pernyataan Direksi
### 8.1 Surat Pernyataan Efektivitas (Lampiran 1 & 2)
*   **Menu:** `ICORF > Kepatuhan > Sertifikasi`
*   Setelah evaluasi selesai, klik **Print > Surat Pernyataan Efektivitas**. Report ini berisi pernyataan legal CEO/CFO sesuai format baku Kementerian BUMN.

---

## 9. Fase 8: Dashboard Maturity & Audit Dossier
### 9.1 Dashboard Eksekutif
*   Pantau **Heatmap Risiko 5x5**, **ELC Radar**, dan **ITGC Maturity** untuk laporan ke Komite Audit.

### 9.2 Audit Dossier (Lampiran 12)
*   Klik satu tombol untuk menyiapkan seluruh paket bukti audit (RCM, TOD/TOE, DoD, Sertifikasi).

---
*Dokumen ini merupakan panduan final untuk kepatuhan 100% terhadap Juknis BUMN & POJK.*