# ICORF (Internal Controls Over Financial Reporting)

Modul ini menyediakan sistem **100% Audit-Proof** untuk mengelola Internal Controls Over Financial Reporting (ICORF) sesuai dengan standar COSO 2013, regulasi **POJK No. 15 Tahun 2024**, serta Juknis BUMN **SK-5/DKU.MBU/11/2024**.

## Fitur Teknis Utama (Perfect Gold Standard)

### 1. Metodologi Scoping & Materialitas (BAB III)
- **Advanced Import Data**: Mendukung alur import dua tahap:
    1. **Template Laporan**: Membangun struktur FSLI dan memetakan `entity_code` untuk membedakan Induk dan Anak Perusahaan.
    2. **General Ledger**: Menarik saldo riil GL dan melakukan agregasi otomatis ke 4 pilar finansial.
- **Kalkulator Aturan 2/3 (Tabel 6)**: Dashboard otomatis yang memverifikasi cakupan 66.7% dari (**Aset, Pendapatan, Beban, Liabilitas**).
- **Ambang Batas SAD (Hal 17)**: Otomasi penghitungan *Summary of Adjusted Differences* (3% dari OM).

### 2. Evaluasi Entitas & IT (COSO & COBIT)
- **Checklist 17 Prinsip COSO**: Kuesioner terstruktur untuk menilai lingkungan pengendalian (ELC) secara kualitatif.
- **ITGC Maturity Score**: Penilaian tingkat kematangan (0-5) aplikasi berbasis **COBIT 2019**.
- **Evaluasi SOC & Bridge Letter**: Verifikasi kelengkapan bukti audit dari *Service Organization* (Hal 56).

### 3. Pengujian & Remediasi (BAB V)
- **Advanced Testing Log (Lampiran 7)**: Dokumentasi personil Lini 1 yang menjalankan kontrol dan detail skenario pengujian ITAC (Expected vs Actual).
- **Remediation Lock (Tabel 23)**: Validasi masa tunggu wajib (30-180 hari) setelah kontrol diperbaiki.
- **Roll-forward Testing (Hal 51)**: Prosedur pembaruan hasil pengujian interim.
- **Integritas Auditor (Hal 19)**: Penegakan masa jeda 12 bulan (*Cooling-off*).

### 4. Pelaporan Audit (BAB VI & Lampiran 12)
- **Audit Dossier Wizard**: Mengumpulkan RCM, Flowchart, TOD/TOE, DoD, dan Sertifikasi ke dalam satu bundel audit terstruktur.
- **Kertas Kerja DoD PDF (Lampiran 10)**: Laporan matriks 7 kolom otomatis.

## Data Demo & Skenario Industri (Lampiran 2)
Modul ini menyertakan simulasi risiko dan kontrol untuk berbagai klaster BUMN:
- **Energi & Minerba**: Estimasi cadangan, royalti batubara, dan PNBP.
- **Pangan & Pupuk**: Klaim subsidi RDKK dan verifikasi penyaluran.
- **Infrastruktur & Logistik**: Pengakuan POC Konstruksi dan validasi POD Logistik.
- **Asuransi & Jasa Keuangan**: Asumsi aktuaria PSAK 74 dan penurunan nilai investasi.

## Panduan Cepat
1. **Import Master**: Gunakan wizard **Pemetaan Akun GL-FSLI** dengan file `Template Laporan`.
2. **Import Balances**: Gunakan wizard **Kalkulator Materialitas** dengan file `General Ledger`.
3. **Evaluasi ELC**: Isi kuesioner 17 Prinsip COSO.
4. **Execute Tests**: Jalankan pengujian interim dengan prosedur *Roll-forward*.
5. **Bundle Dossier**: Siapkan dokumen final bagi Auditor Eksternal via menu "Dossier Audit".

---
Dikembangkan oleh Tim ICORF untuk kepatuhan BUMN Indonesia.
