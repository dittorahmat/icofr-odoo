# ICORF (Internal Controls Over Financial Reporting)

Modul ini menyediakan sistem untuk mengelola Internal Controls Over Financial Reporting (ICORF) sesuai dengan standar COSO 2013 dan regulasi POJK No. 15 Tahun 2024 tentang Integritas Pelaporan Keuangan Bank. Modul ini mendukung proses dokumentasi, pengujian, pelaporan, dan sertifikasi kontrol internal atas pelaporan keuangan.

## Fitur Utama

### 1. Manajemen Kontrol Internal
- Buat dan kelola kontrol internal dengan berbagai jenis, frekuensi, dan pemilik
- Kaitkan kontrol dengan proses bisnis dan risiko terkait
- Lacak efektivitas dan status kontrol

### 2. Manajemen Risiko
- Identifikasi dan evaluasi risiko finansial dengan matriks risiko
- Kaitkan risiko dengan kontrol yang relevan
- Pantau mitigasi dan perubahan risiko

### 3. Manajemen Proses Bisnis
- Definisikan dan dokumentasikan proses bisnis
- Kaitkan proses dengan kontrol dan risiko
- Kelompokkan kontrol berdasarkan proses bisnis

### 4. Jadwal Pengujian
- Buat jadwal pengujian berkala untuk kontrol
- Otomatis hasilkan tugas pengujian
- Terima notifikasi sebelum jadwal tiba

### 5. Pengujian Kontrol
- Dokumentasikan hasil pengujian kontrol
- Simpan bukti dan temuan selama pengujian
- Evaluasi efektivitas kontrol berdasarkan hasil pengujian

### 6. Temuan dan Rencana Tindakan
- Catat temuan dari proses pengujian
- Buat rencana tindakan untuk mengatasi temuan
- Lacak pelaksanaan rencana tindakan

### 7. Sertifikasi dan Persetujuan
- Proses sertifikasi CEO/CFO untuk kontrol internal
- Workflow persetujuan untuk sertifikasi
- Dokumentasi dan pelacakan status sertifikasi

### 8. Laporan POJK 15/2024
- Laporan sesuai format POJK 15/2024
- Kepatuhan terhadap regulasi
- Ekspor ke format Excel atau PDF

### 9. Dashboard dan Metrik
- Dashboard real-time untuk status kontrol
- KPI dan metrik efektivitas
- Visualisasi dan grafik

### 10. Fungsi Ekspor Data
- Ekspor data ke format CSV, Excel, atau PDF
- Pilihan untuk mengekspor data tertentu
- Filter berdasarkan tanggal dan status

### 11. Pelaporan Komprehensif
- Laporan ringkasan dan detail tentang kontrol internal
- Parameter laporan yang dapat disesuaikan
- Termasuk hasil pengujian dan penilaian risiko
- Fungsi ekspor laporan

### 12. Kalender Aktivitas
- Tampilan kalender untuk semua aktivitas terjadwal
- Menampilkan jadwal pengujian kontrol
- Warna berbeda untuk masing-masing pelaksana pengujian
- Integrasi dengan fitur jadwal pengujian

### 13. Kalkulator Materialitas
- Fitur perhitungan materialitas otomatis untuk Overall Materiality dan Performance Materiality
- Berdasarkan standar POJK No. 15 Tahun 2024
- Menggunakan metode persentase pendapatan, total aset, atau laba bersih
- Dapat diakses melalui menu "ICORF" > "Master Data" > "Kalkulator Materialitas"

### 14. Pemetaan Akun
- Pemetaan akun General Ledger (GL) ke Financial Statement Line Item (FSLI)
- Mendukung kalkulasi materialitas yang lebih akurat
- Terintegrasi dengan kalkulator materialitas
- Dapat diakses melalui menu "ICORF" > "Master Data" > "Pemetaan Akun GL-FSLI"
- Mengambil data akun langsung dari sistem akuntansi Odoo
- Menyediakan opsi pengisian manual jika tidak menggunakan akun dari sistem Odoo
- Fitur upload Excel untuk import data pemetaan akun secara massal
- Termasuk template Excel untuk kemudahan pengisian data

### 15. Penilaian Mandiri Kontrol (CSA)
- Workflow lengkap untuk Control Self-Assessment
- Evaluasi efektivitas kontrol oleh pemilik proses (Lini 1)
- Review oleh tim risiko/ICOFR (Lini 2)
- Dukungan untuk penilaian kepatuhan dan efektivitas
- Dapat diakses melalui menu "ICORF" > "Operasional" > "Penilaian Mandiri Kontrol"

### 16. Klasifikasi Kekurangan
- Klasifikasi otomatis temuan kekurangan kontrol
- Berdasarkan faktor kuantitatif dan kualitatif
- Menghasilkan kategori seperti kelemahan material, kekurangan signifikan, atau kekurangan kontrol
- Terintegrasi dengan modul temuan dan laporan POJK

### 17. Dukungan Multi-Perusahaan
- Isolasi data perusahaan untuk organisasi dengan entitas ganda
- Semua modul utama mendukung multi-perusahaan

### 18. Kuantifikasi Dampak Defisiensi
- Fitur kuantifikasi dampak moneter dari temuan kontrol
- Perhitungan otomatis klasifikasi defisiensi (Kekurangan Kontrol, Kekurangan Signifikan, Kelemahan Material)
- Berdasarkan kriteria kuantitatif dan kualitatif

### 19. Pemetaan COBIT 2019
- Integrasi dengan kerangka kerja COBIT 2019 untuk kontrol TI
- Pemetaan kontrol ke elemen COBIT
- Klasifikasi kontrol TI berdasarkan area risiko dan tipe aset TI

### 20. Penjadwal Notifikasi Otomatis
- Sistem penjadwalan notifikasi untuk CSA dan pengujian kontrol
- Pengingat otomatis sebelum tenggat waktu
- Pemberitahuan multi-channel untuk stakeholder terkait

### 21. Sinkronisasi Data Keuangan dari ERP
- Sinkronisasi otomatis data keuangan dari modul akuntansi Odoo
- Penarikan data pendapatan, aset, dan laba bersih secara otomatis
- Pembaruan saldo akun untuk keperluan scoping

### 22. Laporan Khusus per Lini Pertahanan
- Laporan khusus untuk Lini 1 (Pemilik Proses)
- Laporan khusus untuk Lini 2 (Tim Risiko/ICOFR)
- Laporan khusus untuk Lini 3 (Audit Internal)
- Penyajian metrik dan KPI berdasarkan peran masing-masing lini
- Akses data terbatas pada perusahaan yang sesuai dengan pengguna

### 23. Fitur Copy Period
- Wizard untuk menyalin data dari satu periode fiskal ke periode lain
- Meningkatkan efisiensi karena 80-90% RCM biasanya tetap sama dari tahun ke tahun
- Tersedia di menu "ICORF" > "Utilitas" > "Salin Periode"
- Opsi untuk memilih entitas yang akan disalin (proses, kontrol, risiko, temuan, rencana aksi, dll.)

### 24. Input Manual Dampak dan Penyesuaian Defisiensi
- Kemampuan untuk memasukkan dampak moneter secara manual oleh Lini 3
- Skor dampak kualitatif yang dapat diinput manual
- Fungsi override untuk manajemen/Lini 2 untuk menyesuaikan klasifikasi defisiensi
- Alasan override yang harus diberikan saat penyesuaian klasifikasi
- Opsi metode penilaian dampak: otomatis, manual, atau gabungan

### 25. Kepatuhan SK BUMN
- Implementasi lengkap atribut dan proses sesuai Surat Keputusan BUMN
- Cocok dengan persyaratan POJK 15/2024
- Melengkapi framework COSO 2013 dengan elemen khusus Indonesia

## Panduan Penggunaan

### 1. Awal Penggunaan
1. Instal modul ICORF melalui menu Apps
2. Akses modul melalui menu utama "ICORF"
3. Mulai dengan membuat proses bisnis terlebih dahulu

### 2. Membuat Proses Bisnis
1. Buka menu "ICORF" > "Master Data" > "Proses Bisnis"
2. Klik "Create" untuk membuat proses baru
3. Isi informasi proses seperti nama, kode, dan pemilik
4. Simpan entri

### 3. Membuat Kontrol Internal
1. Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
2. Klik "Create" untuk membuat kontrol baru
3. Isi informasi kontrol seperti nama, kode, jenis, dan frekuensi
4. Hubungkan dengan proses bisnis dan risiko terkait
5. Simpan entri

### 4. Membuat Risiko
1. Buka menu "ICORF" > "Master Data" > "Risiko Finansial"
2. Klik "Create" untuk membuat risiko baru
3. Isi informasi risiko seperti nama, kategori, dan deskripsi
4. Hubungkan dengan proses bisnis dan kontrol terkait
5. Simpan entri

### 5. Membuat Jadwal Pengujian
1. Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian"
2. Klik "Create" untuk membuat jadwal baru
3. Pilih kontrol yang akan diuji dan frekuensi pengujian
4. Tentukan pelaksana pengujian
5. Simpan entri

### 6. Melakukan Pengujian
1. Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
2. Klik "Create" atau gunakan jadwal untuk membuat pengujian
3. Isi hasil pengujian, bukti, dan temuan
4. Update status pengujian
5. Simpan entri

### 7. Membuat dan Mengelola Temuan
1. Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
2. Klik "Create" untuk membuat temuan baru
3. Deskripsikan temuan dan rekomendasi tindakan
4. Buat rencana tindakan jika diperlukan
5. Update status temuan
6. Simpan entri

### 8. Sertifikasi dan Laporan
1. Buka menu "ICORF" > "Kepatuhan" > "Sertifikasi ICORF"
2. Buat entri sertifikasi baru
3. Lakukan proses sertifikasi sesuai workflow
4. Untuk laporan POJK, buka "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"

### 9. Menggunakan Dashboard
1. Buka menu "ICORF" > "Dashboard"
2. Lihat ringkasan status kontrol, risiko, dan pengujian
3. Gunakan filter untuk melihat data spesifik
4. Gunakan tombol refresh untuk memperbarui data

### 10. Ekspor Data
1. Buka entri yang ingin diekspor (kontrol, risiko, dll.)
2. Klik tombol "Export" atau "Export Kontrol" tergantung model
3. Pilih format ekspor (Excel, CSV, PDF)
4. Atur parameter seperti tanggal dan status
5. Klik "Ekspor" untuk menghasilkan file

### 11. Menggunakan Pelaporan
1. Buka menu "ICORF" > "Pelaporan"
2. Atur parameter laporan seperti jenis laporan dan periode
3. Pilih apakah akan menyertakan hasil pengujian dan penilaian risiko
4. Klik "Generate Laporan" untuk membuat laporan
5. Gunakan tombol "Export Laporan" untuk mengekspor hasil

### 12. Menggunakan Kalender
1. Buka menu "ICORF" > "Kalender"
2. Lihat semua aktivitas terjadwal dalam tampilan kalender
3. Gunakan filter untuk melihat aktivitas berdasarkan pelaksana
4. Klik pada event untuk melihat detail aktivitas
5. Gunakan tombol navigasi untuk berpindah antar bulan

### 13. Menggunakan Kalkulator Materialitas
1. Buka menu "ICORF" > "Master Data" > "Kalkulator Materialitas"
2. Buat perhitungan materialitas baru dengan mengisi:
   - Nama perhitungan
   - Tahun fiskal
   - Perusahaan
   - Basis perhitungan (pendapatan, total aset, laba bersih)
   - Metode perhitungan
   - Jumlah pendapatan, total aset, dan laba bersih
3. Sistem akan menghitung Overall Materiality dan Performance Materiality otomatis
4. Gunakan tombol "Hitung Ulang Materialitas" untuk perhitungan ulang

### 14. Membuat Pemetaan Akun GL-FSLI
1. Buka menu "ICORF" > "Master Data" > "Pemetaan Akun GL-FSLI"
2. Buat pemetaan baru dengan mengisi:
   - Nama pemetaan
   - Akun GL (dari sistem Odoo) atau Akun GL Manual (jika tidak menggunakan akun dari sistem)
   - Deskripsi GL
   - FSLI (Financial Statement Line Item)
   - Deskripsi FSLI
   - Tingkat signifikansi
3. Hubungkan dengan perhitungan materialitas yang relevan
4. Gunakan untuk mendukung analisis materialitas

### 15. Menggunakan Fitur Upload Excel untuk Pemetaan Akun
1. Buka menu "ICORF" > "Master Data" > "Kalkulator Materialitas"
2. Pilih entri kalkulasi materialitas yang relevan
3. Di header form, klik tombol "Upload Excel Pemetaan Akun"
4. Siapkan file Excel dengan format yang benar:
   - Kolom wajib: Kode Akun GL, Nama Akun GL, FSLI, Deskripsi FSLI, Tingkat Signifikansi
   - Jika Kode Akun GL sesuai dengan akun di sistem Odoo, sistem akan memetakan otomatis
   - Jika tidak ditemukan di sistem Odoo, sistem akan menggunakan field manual
5. Pilih file Excel dan klik "Upload & Import"
6. Sistem akan menampilkan hasil import, termasuk jumlah record baru dan diperbarui
7. Periksa hasil import dan pastikan data sudah sesuai

### 16. Melakukan Penilaian Mandiri Kontrol (CSA)
1. Buka menu "ICORF" > "Operasional" > "Penilaian Mandiri Kontrol"
2. Buat CSA baru dengan memilih:
   - Kontrol yang dinilai
   - Periode penilaian
   - Pemilik kontrol (Lini 1)
   - Reviewer CSA (Lini 2)
3. Isi formulir penilaian CSA:
   - Apakah desain kontrol efektif?
   - Apakah kontrol beroperasi secara efektif?
   - Apakah kontrol dilaksanakan sesuai frekuensi?
   - dll.
4. Submit CSA untuk review oleh Lini 2
5. Gunakan fitur temuan terkait untuk mencatat temuan dari CSA

### 17. Menggunakan Fitur Copy Period
1. Buka menu "ICORF" > "Utilitas" > "Salin Periode"
2. Pilih periode sumber dan tujuan
3. Pilih entitas yang ingin disalin (proses, kontrol, risiko, temuan, dll.)
4. Klik "Proses" untuk memulai penyalinan data
5. Tinjau hasil copy period dan lakukan validasi

### 18. Melihat Klasifikasi Kekurangan
1. Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
2. Perhatikan kolom "Klasifikasi Kekurangan" yang secara otomatis menentukan:
   - Kekurangan Kontrol (Control Deficiency)
   - Kekurangan Signifikan (Significant Deficiency)
   - Kelemahan Material (Material Weakness)
3. Sistem akan menentukan klasifikasi berdasarkan faktor kuantitatif dan kualitatif

## Peran Pengguna

Modul ini dirancang untuk digunakan oleh berbagai peran:
- **CFO/CEO**: Untuk sertifikasi dan pelaporan
- **Internal Audit**: Untuk pengujian dan penilaian kontrol
- **Controller/Manajer Proses**: Untuk dokumentasi dan pemeliharaan kontrol
- **Komite Audit**: Untuk monitoring dan review

## Dukungan dan Bantuan

Untuk bantuan teknis atau pertanyaan mengenai penggunaan modul, silakan hubungi tim IT organisasi Anda atau konsultan yang terlibat dalam implementasi sistem ini.