# ICORF (Internal Controls Over Financial Reporting)

Modul ini menyediakan sistem untuk mengelola Internal Controls Over Financial Reporting (ICORF) sesuai dengan standar COSO 2013 dan regulasi POJK No. 15 Tahun 2024 tentang Integritas Pelaporan Keuangan Bank serta Juknis BUMN SK-5/DKU.MBU/11/2024. Modul ini mendukung proses dokumentasi, pengujian, pelaporan, dan sertifikasi kontrol internal atas pelaporan keuangan.

## Fitur Utama

### 1. Manajemen Kontrol Internal
- Buat dan kelola kontrol internal dengan berbagai jenis, frekuensi, dan pemilik.
- Kaitkan kontrol dengan proses bisnis dan risiko terkait.
- Lacak efektivitas dan status kontrol.
- **Hierarki Level Pengendalian**: Kategorisasi formal ELC (Direct/Indirect/Monitoring) dan TLC sesuai Tabel 17-19.
- **Dukungan Spesialis**: Atribut khusus untuk mencatat kredibilitas dan validitas asumsi tenaga ahli (Bab III Pasal 2.2.b.4).

### 2. Manajemen Risiko
- Identifikasi dan evaluasi risiko finansial dengan matriks risiko.
- Kaitkan risiko dengan kontrol yang relevan.
- Pantau mitigasi dan perubahan risiko.

### 3. Manajemen Proses Bisnis
- Definisikan dan dokumentasikan proses bisnis.
- Kaitkan proses dengan kontrol dan risiko.
- Kelompokkan kontrol berdasarkan proses bisnis.
- **Dukungan Sub-proses**: Implementasi struktur hierarki proses sesuai Lampiran 3 (Tabel 7).

### 4. Jadwal Pengujian
- Buat jadwal pengujian berkala untuk kontrol.
- Otomatis hasilkan tugas pengujian.
- Terima notifikasi sebelum jadwal tiba.

### 5. Pengujian Kontrol & Sampling
- Dokumentasikan hasil pengujian kontrol (TOD & TOE).
- **Kalkulator Sampling Otomatis**: Menghitung jumlah sampel berdasarkan Tabel 22 (TOE standar) dan **Tabel 23 (Remediasi)**.
- Simpan bukti dan temuan selama pengujian.
- Evaluasi efektivitas kontrol berdasarkan hasil pengujian.

### 6. Temuan dan Rencana Tindakan
- Catat temuan dari proses pengujian.
- **Evaluasi Agregasi**: Pengelompokan temuan berdasarkan Akun, Prinsip COSO, atau Proses Bisnis untuk menilai dampak kolektif.
- Buat rencana tindakan untuk mengatasi temuan.
- Lacak pelaksanaan rencana tindakan.

### 7. Sertifikasi dan Persetujuan
- Proses sertifikasi CEO/CFO untuk kontrol internal.
- Workflow persetujuan untuk sertifikasi.
- Dokumentasi dan pelacakan status sertifikasi.

### 8. Laporan POJK 15/2024
- Laporan sesuai format POJK 15/2024.
- Kepatuhan terhadap regulasi.
- Ekspor ke format Excel atau PDF.

### 9. Dashboard dan Metrik
- Dashboard real-time untuk status kontrol.
- KPI dan metrik efektivitas.
- Visualisasi dan grafik.

### 10. Fungsi Ekspor Data
- Ekspor data ke format CSV, Excel, atau PDF.
- Pilihan untuk mengekspor data tertentu.
- Filter berdasarkan tanggal dan status.

### 11. Pelaporan Komprehensif
- Laporan ringkasan dan detail tentang kontrol internal.
- Parameter laporan yang dapat disesuaikan.
- Termasuk hasil pengujian dan penilaian risiko.

### 12. Kalender Aktivitas
- Tampilan kalender untuk semua aktivitas terjadwal.
- Menampilkan jadwal pengujian kontrol.
- Warna berbeda untuk masing-masing pelaksana pengujian.

### 13. Kalkulator Materialitas
- Fitur perhitungan materialitas otomatis untuk Overall Materiality dan Performance Materiality.
- Berdasarkan standar POJK No. 15 Tahun 2024.
- Menggunakan metode persentase pendapatan, total aset, atau laba bersih.
- **Analisis Cakupan Scoping Otomatis**: Verifikasi Aturan 2/3 (66.7%) untuk akun dan lokasi signifikan.

### 14. Pemetaan Akun
- Pemetaan akun General Ledger (GL) ke Financial Statement Line Item (FSLI).
- Mendukung kalkulasi materialitas yang lebih akurat.
- **Scoping Kualitatif Lanjutan**: Triger signifikansi otomatis untuk akun WIP, Pihak Ketiga, dan Loan Covenant (Tabel 5).
- Fitur upload Excel untuk import data pemetaan akun secara massal.

### 15. Penilaian Mandiri Kontrol (CSA)
- Workflow lengkap untuk Control Self-Assessment.
- **Status "No Transaction"**: Mendukung pelaporan kontrol tanpa aktivitas sesuai Bab IV Pasal 2.1.c.
- Review oleh tim risiko/ICOFR (Lini 2).

### 16. Klasifikasi Kekurangan
- Klasifikasi otomatis temuan (MW, SD, CD) berdasarkan faktor kuantitatif dan kualitatif.
- Kertas kerja DoD interaktif sesuai Lampiran 10.

### 17. Dukungan Multi-Perusahaan
- Isolasi data perusahaan untuk organisasi dengan entitas ganda.
- Semua modul utama mendukung multi-perusahaan.

### 18. Kuantifikasi Dampak Defisiensi
- Fitur kuantifikasi dampak moneter dari temuan kontrol.
- Perhitungan otomatis klasifikasi defisiensi berdasarkan kriteria moneter.

### 19. Pemetaan COBIT 2019
- Integrasi dengan kerangka kerja COBIT 2019 untuk kontrol TI.
- Pemetaan kontrol ke elemen COBIT.

### 20. Penjadwal Notifikasi Otomatis
- Sistem penjadwalan notifikasi untuk CSA dan pengujian kontrol.
- Pengingat otomatis sebelum tenggat waktu.

### 21. Sinkronisasi Data Keuangan dari ERP
- Sinkronisasi otomatis data keuangan dari modul akuntansi Odoo.
- Penarikan data pendapatan, aset, dan laba bersih secara otomatis.

### 22. Laporan Khusus per Lini Pertahanan
- Laporan khusus untuk Lini 1 (Pemilik Proses), Lini 2 (Tim Risiko/ICOFR), dan Lini 3 (Audit Internal).
- **Pelaporan Lini 3 Profesional**: Narasi ringkasan eksekutif dan rincian defisiensi untuk laporan formal (Bab VII).

### 23. Fitur Copy Period
- Wizard untuk menyalin data dari satu periode fiskal ke periode lain (efisiensi RCM).

### 24. Input Manual Dampak dan Penyesuaian Defisiensi
- Fungsi override untuk manajemen/Lini 2 untuk menyesuaikan klasifikasi defisiensi dengan justifikasi.

### 25. Kepatuhan SK BUMN
- Implementasi lengkap atribut dan proses sesuai Surat Keputusan BUMN SK-5/DKU.MBU/11/2024.

### 26. Matriks Kepatuhan COSO
- Tampilan visual pemetaan 17 Prinsip COSO ke kontrol utama (Lampiran 1).

### 27. Sistem Whistleblowing (WBS)
- Modul untuk mencatat dan mengelola aduan fraud/integritas (Prinsip COSO 14).

### 28. Validasi Teknis Mendalam
- Checklist verifikasi otomatis untuk IPE (Tabel 20) dan MRC (Tabel 21).
- Validasi minimum kontrol untuk EUC (Tabel 14).
- Kertas kerja TOD detail sesuai Lampiran 8.

### 29. Dukungan Sektor Perbankan
- Data demo dan framework risiko khusus: Pemberian Kredit, GWM, dan AML/KYC.

### 30. Manajemen Service Organization (Pihak Ketiga)
- Registri vendor pihak ketiga dan pengelolaan **SOC 1/2 Type II Reports** (Bab III Pasal 4.3).

### 31. Panduan Juknis Interaktif (FAQ)
- Repositori 14 poin tanya-jawab dari **Lampiran 12 Juknis BUMN**.

### 32. Matriks Pemetaan ITGC-COBIT
- Dashboard visual pemetaan 4 area ITGC (Prog Dev, Changes, Ops, Access) ke objektif COBIT 2019 sesuai **Tabel 1**.

### 33. Asurans Praktisi Eksternal
- Modul pelacakan opini dan asurans dari Praktisi Eksternal (KAP) sesuai mandat **Bab VIII**.

### 34. Sertifikasi Terintegrasi Lampiran 11
- Digitalisasi surat pernyataan CEO/CFO dengan checkbox wajib untuk 5 poin pengakuan integritas pelaporan.

### 35. Manajemen Aplikasi Signifikan
- Registri sistem IT yang terintegrasi dengan kontrol otomatis untuk analisis dampak ITGC (Bab III 1.5).

## Panduan Penggunaan

### 1. Awal Penggunaan
1. Instal modul ICORF melalui menu Apps.
2. Akses modul melalui menu utama "ICORF".
3. Pelajari aturan main di menu "Utilitas" > "Panduan Juknis (FAQ)".

### 2. Membuat Proses Bisnis
1. Buka menu "ICORF" > "Master Data" > "Proses Bisnis".
2. Klik "New" untuk membuat proses baru.
3. Isi informasi proses seperti nama, kode, dan pemilik.
4. Simpan entri.

### 3. Membuat Kontrol Internal
1. Buka menu "ICORF" > "Master Data" > "Kontrol Internal".
2. Klik "New" untuk membuat kontrol baru.
3. Isi informasi kontrol seperti nama, kode, jenis, dan frekuensi.
4. Tentukan **Level Pengendalian** (ELC/TLC).
5. Untuk kontrol outsourcing, centang **"Kontrol Outsourcing?"** dan hubungkan dengan **Service Organization**.
6. Jika melibatkan tenaga ahli, centang **"Melibatkan Spesialis?"** dan isi data kredibilitasnya.
7. Hubungkan dengan proses bisnis, risiko, Prinsip COSO, dan Elemen COBIT.

### 4. Membuat Risiko
1. Buka menu "ICORF" > "Master Data" > "Risiko Finansial".
2. Klik "New" untuk membuat risiko baru.
3. Isi informasi risiko seperti nama, kategori, dan deskripsi.
4. Hubungkan dengan proses bisnis dan kontrol terkait.

### 5. Membuat Jadwal Pengujian
1. Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian".
2. Klik "New" untuk membuat jadwal baru.
3. Pilih kontrol yang akan diuji dan frekuensi pengujian.
4. Tentukan pelaksana pengujian.

### 6. Melakukan Pengujian (TOD & TOE)
1. Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol".
2. Pilih jenis pengujian (**TOD** untuk desain, **TOE** untuk operasi).
3. Gunakan **Kalkulator Sampling** di dalam form untuk menentukan jumlah sampel yang tepat.
4. Isi hasil pengujian, bukti, dan temuan.
5. Update status pengujian menjadi "Selesai".

### 7. Membuat dan Mengelola Temuan
1. Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF".
2. Klik "New" untuk mencatat temuan baru.
3. Deskripsikan temuan dan rekomendasi tindakan.
4. Buat rencana tindakan (Action Plan) untuk perbaikan.

### 8. Evaluasi Defisiensi Agregat
1. Jika terdapat beberapa temuan kecil pada akun atau prinsip COSO yang sama, buka menu "Kepatuhan" > "Evaluasi Agregat".
2. Klik "New" dan pilih **"Dasar Pengelompokan"** (misal: Akun/FSLI).
3. Tambahkan temuan-temuan terkait untuk melihat total dampak moneter gabungan.

### 9. Sertifikasi dan Laporan
1. Buka menu "ICORF" > "Kepatuhan" > "Sertifikasi ICORF".
2. Buat entri sertifikasi baru untuk periode tahunan/kuartalan.
3. Pastikan poin pernyataan (1-5) telah dicentang sesuai **Lampiran 11**.
4. Lakukan proses persetujuan oleh CFO dan CEO.
5. Untuk laporan regulasi, buka "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024".

### 10. Menggunakan Dashboard
1. Buka menu "ICORF" > "Dashboard".
2. Lihat ringkasan status kontrol, risiko, dan pengujian secara real-time.
3. Akses **"Matriks ITGC-COBIT"** untuk memastikan cakupan tata kelola TI sudah sesuai standar.

### 11. Perhitungan Materialitas & Scoping
1. Buka menu "ICORF" > "Master Data" > "Kalkulator Materialitas".
2. Masukkan data keuangan (Pendapatan, Aset, Laba) atau klik **"Tarik Data dari ERP"**.
3. Sistem akan menghitung OM/PM otomatis.
4. Pastikan status scoping menunjukkan **"LULUS"** pada analisis aturan 2/3 (Akun & Lokasi).

### 12. Penilaian Mandiri Kontrol (CSA)
1. Buka menu "ICORF" > "Operasional" > "Penilaian Mandiri Kontrol".
2. Pemilik Kontrol (Lini 1) mengisi efektivitas harian.
3. Jika tidak ada aktivitas transaksi pada periode tersebut, pilih status **"Tidak Ada Transaksi"**.
4. Submit untuk direview oleh Lini 2.

### 13. Pelaporan Aduan (Whistleblowing)
1. Buka menu "ICORF" > "Operasional" > "Whistleblowing (WBS)".
2. Klik "New" untuk mencatat aduan fraud atau pelanggaran integritas.
3. Lacak status investigasi hingga resolusi selesai.

## Peran Pengguna
- **CFO/CEO**: Bertanggung jawab atas sertifikasi akhir dan pelaporan integritas keuangan kepada regulator.
- **Internal Audit (Lini 3)**: Melakukan pengujian independen (TOE) dan menentukan klasifikasi defisiensi (DoD).
- **Risk Management / ICORF Team (Lini 2)**: Melakukan scoping, pemeliharaan RCM, evaluasi desain (TOD), dan verifikasi CSA.
- **Process Owner (Lini 1)**: Menjalankan kontrol harian, mendokumentasikan bukti, dan melakukan penilaian mandiri (CSA).

## Dukungan dan Bantuan
Silakan hubungi tim IT atau konsultan implementasi sistem untuk bantuan teknis lebih lanjut.
