# ICORF Demo Scenarios

## Pendahuluan
Dokumen ini berisi beberapa skenario demonstrasi untuk modul ICORF (Internal Controls Over Financial Reporting). Setiap skenario dirancang untuk menunjukkan aspek berbeda dari sistem manajemen kontrol internal sesuai dengan standar COSO 2013 dan regulasi POJK No. 15 Tahun 2024. Skema ini disusun berdasarkan urutan logis dari proses implementasi dan penggunaan sistem ICORF.

## Skenario 1: Implementasi Awal dan Pemetaan Kontrol Eksisting

### Latar Belakang
Sebuah organisasi baru akan mengimplementasikan sistem ICORF. Organisasi tersebut sudah memiliki kerangka kontrol internal yang terdokumentasi dalam dokumen prosedur, tetapi belum terdigitalisasi. Tujuan dari skenario ini adalah memetakan kontrol-kontrol eksisting ke dalam sistem ICORF.

### Tujuan
- Mendigitalkan kontrol internal yang sudah ada
- Membuat struktur proses bisnis dalam sistem
- Mengidentifikasi dan mendokumentasikan risiko dari kontrol yang ada
- Membuat inventarisasi kontrol secara menyeluruh sebelum sertifikasi pertama
- Menetapkan tanggung jawab atas masing-masing kontrol

### Langkah-langkah:
1. **Audit Kontrol Eksisting**
   - Kumpulkan semua dokumen kebijakan dan prosedur internal
   - Identifikasi proses-proses bisnis utama dari dokumen tersebut
   - Catat kontrol-kontrol yang saat ini berjalan (baik yang efektif maupun yang tidak)
   - Dokumentasikan risiko yang dituju oleh masing-masing kontrol

2. **Persiapan Data Master**
   - Buka menu "ICORF" > "Master Data" > "Proses Bisnis"
   - Buat semua proses bisnis utama berdasarkan dokumen eksisting:
     - Proses: "Pengelolaan Kas Masuk"
     - Kode: PROC-CASHIN-001
     - Kategori: "Operasional"
     - Pemilik: Finance Manager
     - Ulangi untuk semua proses utama (Penggajian, Pembelian, Penjualan, dll.)

3. **Dokumentasi Kontrol Eksisting**
   - Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
   - Masukkan kontrol-kontrol dari dokumen ke dalam sistem:
     - Kontrol: "Otorisasi Pencairan Dana"
     - Kode: CTRL-WITHDR-001
     - Tipe: "Preventive Control"
     - Frekuensi: "Per transaksi"
     - Kaitkan dengan proses "Pengelolaan Kas Keluar"
     - Ulangi untuk semua kontrol dalam dokumen eksisting

4. **Identifikasi Risiko Eksisting**
   - Buka menu "ICORF" > "Master Data" > "Risiko Finansial"
   - Dokumentasikan risiko-risiko yang teridentifikasi:
     - Risiko: "Pengeluaran tanpa otorisasi"
     - Kode: RISK-UNAUTH-001
     - Kategori: "Operasional"
     - Kaitkan dengan proses "Pengelolaan Kas Keluar" dan kontrol "Otorisasi Pencairan Dana"
     - Ulangi untuk semua risiko dalam dokumen eksisting

5. **Validasi dan Pengujian Awal**
   - Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
   - Buat entri pengujian awal untuk menilai efektivitas kontrol-kontrol yang ada
   - Catat hasil temuan awal (bisa positif maupun negatif)
   - Jika ditemukan ketidaksesuaian, dokumentasikan sebagai temuan awal

6. **Pembuatan Jadwal Pengujian Berkelanjutan**
   - Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian"
   - Buat jadwal untuk semua kontrol penting:
     - Jadwal: "Pengujian Otorisasi Dana Bulanan"
     - Kaitkan dengan kontrol "Otorisasi Pencairan Dana"
     - Frekuensi: "Bulanan"
     - Pelaksana: Senior Internal Auditor

7. **Penetapan Pemilik Proses dan Pengendalian**
   - Pastikan setiap proses memiliki pemilik yang jelas
   - Pastikan setiap kontrol memiliki pemilik yang bertanggung jawab
   - Tetapkan frekuensi pengujian yang sesuai dengan tingkat risiko
   - Validasi bahwa semua dokumentasi sesuai dengan praktik yang sebenarnya

8. **Penyusunan Laporan Awal dan Kesiapan Sertifikasi**
   - Buka menu "ICORF" > "Dashboard" untuk melihat status awal kontrol
   - Gunakan menu "ICORF" > "Pelaporan" untuk menghasilkan laporan inventarisasi
   - Identifikasi area yang membutuhkan perhatian sebelum sertifikasi
   - Buka menu "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024" untuk menyiapkan laporan awal

9. **Rekonsiliasi dan Validasi Akhir**
   - Bandingkan kontrol dalam sistem dengan dokumen eksisting
   - Pastikan tidak ada kontrol penting yang terlewat
   - Lakukan sampling untuk memastikan akurasi data
   - Siapkan rencana aksi untuk menutup gap yang ditemukan

---

## Skenario 2: Implementasi Kontrol Internal untuk Proses Penerimaan Kas

### Latar Belakang
Sebuah perusahaan perbankan sedang mengimplementasikan kontrol internal untuk proses penerimaan kas. Proses ini penting karena terkait langsung dengan aset perusahaan dan merupakan area berisiko tinggi terhadap penipuan atau kesalahan.

### Tujuan
- Mengidentifikasi dan mendokumentasikan risiko dalam proses penerimaan kas
- Membuat kontrol internal yang efektif untuk mitigasi risiko
- Melakukan pengujian kontrol untuk memastikan efektivitas
- Menyusun laporan sertifikasi ICORF untuk proses ini

### Langkah-langkah:
1. **Buat Proses Bisnis**
   - Buka menu "ICORF" > "Master Data" > "Proses Bisnis"
   - Buat proses baru: "Penerimaan Kas"
   - Kode: PROC-CASH-001
   - Kategori: "Operasional"
   - Pemilik: John Doe (Teller Manager)

2. **Identifikasi Risiko**
   - Buka menu "ICORF" > "Master Data" > "Risiko Finansial"
   - Buat risiko: "Kecurangan dalam penerimaan kas"
   - Kategori: "Operasional"
   - Tipe: "Fraud Risk"
   - Kaitkan dengan proses "Penerimaan Kas"

3. **Buat Kontrol Internal**
   - Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
   - Buat kontrol: "Otorisasi transaksi lebih dari Rp. 10.000.000"
   - Kode: CTRL-CASH-001
   - Tipe: "Preventive Control"
   - Frekuensi: "Per transaksi"
   - Kaitkan dengan proses "Penerimaan Kas" dan risiko "Kecurangan dalam penerimaan kas"
   - Pemilik: John Doe

4. **Buat Jadwal Pengujian**
   - Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian"
   - Buat jadwal: "Pengujian Otorisasi Transaksi"
   - Kaitkan dengan kontrol "Otorisasi transaksi lebih dari Rp. 10.000.000"
   - Frekuensi: "Mingguan"
   - Pelaksana: Jane Smith (Internal Auditor)

5. **Lakukan Pengujian**
   - Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
   - Buat entri pengujian baru
   - Isi hasil pengujian: "Semua transaksi >Rp. 10,000,000 memiliki otorisasi yang valid"
   - Status: "Efektif"

6. **Catat Temuan (Jika Ada)**
   - Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
   - Dalam skenario ini tidak ada temuan karena pengujian efektif

7. **Sertifikasi dan Pelaporan**
   - Buka menu "ICORF" > "Kepatuhan" > "Sertifikasi ICORF"
   - Buat sertifikasi untuk periode Q1 2024
   - Isi pernyataan efektivitas kontrol
   - Untuk laporan formal, buka "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"

---

## Skenario 3: Sertifikasi CEO/CFO untuk Laporan Tahunan (POJK Compliance)

### Latar Belakang
Perusahaan harus melakukan sertifikasi CEO/CFO untuk laporan keuangan tahunan sesuai dengan POJK No. 15 Tahun 2024. Ini merupakan proses penting yang menunjukkan komitmen manajemen terhadap integritas pelaporan keuangan.

### Tujuan
- Menyusun sertifikasi CEO/CFO untuk periode laporan keuangan tahunan
- Memastikan semua kontrol internal efektif sebelum sertifikasi
- Menghasilkan laporan sesuai format POJK 15/2024
- Mendemonstrasikan peran manajemen senior dalam ICORF

### Langkah-langkah:
1. **Persiapan Dokumentasi**
   - Buka menu "ICORF" > "Dashboard" untuk melihat ringkasan kontrol
   - Evaluasi total kontrol efektif vs tidak efektif
   - Pastikan semua temuan sebelumnya telah ditutup

2. **Verifikasi Proses dan Kontrol**
   - Buka menu "ICORF" > "Master Data" > "Proses Bisnis"
   - Pastikan semua proses utama telah terdokumentasi
   - Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
   - Verifikasi bahwa kontrol untuk proses-proses utama telah terdokumentasi

3. **Verifikasi Hasil Pengujian**
   - Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
   - Pastikan semua kontrol kritis telah diuji dalam periode pelaporan
   - Konfirmasi bahwa tidak ada hasil pengujian yang menunjukkan kegagalan kontrol signifikan

4. **Buat Sertifikasi ICORF**
   - Buka menu "ICORF" > "Kepatuhan" > "Sertifikasi ICORF"
   - Buat entri sertifikasi baru
   - Isi informasi:
     - Tahun Fiskal: 2024
     - Tanggal Sertifikasi: Akhir tahun fiskal
     - Disertifikasi oleh: CEO/Presiden Direktur
     - Cakupan: Semua kontrol internal atas pelaporan keuangan

5. **Isi Pernyataan Efektivitas**
   - Nyatakan bahwa manajemen telah menetapkan kerangka kerja kontrol internal yang memadai
   - Konfirmasi bahwa penilaian efektivitas kontrol internal dilakukan sesuai standar yang ditentukan
   - Nyatakan bahwa berdasarkan penilaian tersebut, kontrol internal atas pelaporan keuangan efektif

6. **Hasilkan Laporan POJK 15/2024**
   - Buka menu "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"
   - Buat laporan baru
   - Isi semua bagian yang diperlukan:
     - Penilaian kerangka kerja
     - Temuan dan respons manajemen
     - Tindakan perbaikan
   - Ekspor laporan dalam format yang diperlukan

7. **Tinjau dan Kirim ke Komite Audit**
   - Buka menu "ICORF" > "Kepatuhan" > "Sertifikasi ICORF"
   - Tinjau kembali sertifikasi yang disiapkan
   - Kirim ke komite audit untuk review

---

## Skenario 4: Respons terhadap Temuan Audit Internal

### Latar Belakang
Audit internal menemukan bahwa beberapa kontrol dalam proses penggajian tidak berjalan efektif, yang mengakibatkan beberapa kesalahan pembayaran gaji. Perusahaan harus menangani temuan ini secara sistematis sesuai dengan kerangka ICORF.

### Tujuan
- Mendokumentasikan temuan dengan tepat
- Menyusun rencana tindakan yang efektif
- Memantau implementasi rencana tindakan
- Memperbarui kontrol internal berdasarkan pelajaran dari temuan

### Langkah-langkah:
1. **Dokumentasikan Temuan**
   - Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
   - Buat entri temuan baru
   - Informasi temuan:
     - Nama: "Kesalahan Pembayaran Gaji"
     - Kode: FIND-PAY-001
     - Tipe: "Control Deficiency"
     - Tingkat Keparahan: "Significant Deficiency"
     - Deskripsi: "Beberapa pembayaran gaji tidak melalui otorisasi yang tepat"
     - Kaitkan dengan: Proses "Penggajian", Kontrol "Otorisasi Pembayaran", Risiko "Pembayaran Salah"

2. **Lakukan Penilaian Dampak**
   - Isi bagian "Penilaian Dampak" dengan informasi keuangan dan operasional
   - Identifikasi "Penyebab Akar": Prosedur otorisasi tidak diikuti secara konsisten

3. **Buat Rencana Tindakan**
   - Buka bagian "Rencana Tindakan" dalam entri temuan atau buka menu "ICORF" > "Kepatuhan" > "Rencana Tindakan"
   - Buat rencana tindakan:
     - Nama: "Perkuat Prosedur Otorisasi Penggajian"
     - Pemilik Tindakan: HR Manager
     - Tanggal Target Penyelesaian: 60 hari dari tanggal temuan
     - Prioritas: Tinggi
     - Langkah-langkah Implementasi: "Implementasikan sistem otorisasi ganda untuk pembayaran >Rp. 5,000,000"

4. **Perbarui atau Buat Kontrol Baru**
   - Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
   - Tambahkan kontrol baru: "Otorisasi Ganda untuk Pembayaran Gaji >Rp. 5,000,000"
   - Kaitkan dengan proses "Penggajian" dan temuan "Kesalahan Pembayaran Gaji"
   - Tetapkan frekuensi: "Per transaksi"

5. **Monitoring dan Update Status**
   - Tetap perbarui status rencana tindakan saat implementasi berlangsung
   - Melakukan pengujian kontrol baru setelah implementasi
   - Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol" untuk membuat entri pengujian
   - Setelah implementasi selesai, update status temuan menjadi "Ditutup"

6. **Pelaporan dan Review**
   - Buka menu "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"
   - Pastikan temuan dan respons terhadapnya terdokumentasi dalam laporan
   - Tinjau efektivitas kontrol yang diperbarui dalam "ICORF" > "Dashboard"

---

## Skenario 5: Kalender dan Pengelolaan Aktivitas ICORF

### Latar Belakang
Departemen kepatuhan ingin menggunakan kalender ICORF untuk mengatur dan melacak semua aktivitas pengujian kontrol secara efisien. Ini termasuk pengujian rutin dan jadwal review tahunan.

### Tujuan
- Menjadwalkan semua aktivitas pengujian kontrol
- Menggunakan kalender untuk pemantauan dan pengingat
- Mengoptimalkan alokasi sumber daya audit
- Menjamin bahwa semua kontrol diuji secara tepat waktu

### Langkah-langkah:
1. **Buat Jadwal Pengujian**
   - Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian"
   - Buat beberapa jadwal pengujian:
     - Pengujian "Otorisasi Transaksi Harian" - Frekuensi Harian - Pelaksana: John (Auditor Harian)
     - Pengujian "Rekonsiliasi Rekening Bank" - Frekuensi Mingguan - Pelaksana: Sarah (Auditor Senior)
     - Pengujian "Akses Sistem" - Frekuensi Bulanan - Pelaksana: Mike (IT Auditor)

2. **Lihat Aktivitas di Kalender**
   - Buka menu "ICORF" > "Kalender"
   - Lihat semua aktivitas terjadwal dalam tampilan bulan
   - Gunakan filter untuk melihat aktivitas berdasarkan pelaksana
   - Klik pada event untuk melihat detail kontrol yang akan diuji

3. **Atur Pengingat dan Notifikasi**
   - Pastikan sistem notifikasi aktif (jika telah dikonfigurasi)
   - Pelaksana pengujian akan menerima notifikasi sebelum jadwal tiba
   - Kepala bagian akan menerima ringkasan mingguan tentang aktivitas yang akan datang

4. **Eksekusi Pengujian dari Kalender**
   - Saat tanggal jadwal tiba, buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
   - Buat entri pengujian baru sesuai dengan jadwal
   - Isi hasil pengujian dan bukti yang diperlukan
   - Update status pengujian

5. **Gunakan Kalender untuk Perencanaan Tahunan**
   - Buka kalender untuk tahun berikutnya
   - Rencanakan jadwal pengujian tahunan untuk kontrol-kontrol penting
   - Koordinasikan dengan kalender audit eksternal dan periode pelaporan

6. **Laporan Aktivitas Kalender**
   - Gunakan menu "ICORF" > "Pelaporan" untuk melihat ringkasan aktivitas
   - Generate laporan pengujian berdasarkan periode tertentu
   - Evaluasi efisiensi dan efektivitas dalam menjalankan pengujian sesuai jadwal

---

## Skenario 6: Pelaporan dan Analisis ICORF

### Latar Belakang
Manajemen ingin menganalisis efektivitas kontrol internal secara keseluruhan dan memahami tren dari waktu ke waktu. Ini penting untuk perbaikan berkelanjutan dan pemenuhan kewajiban pelaporan.

### Tujuan
- Menghasilkan laporan komprehensif tentang kontrol internal
- Menganalisis tren dan pola dalam hasil pengujian
- Mengidentifikasi area yang membutuhkan perhatian khusus
- Menyediakan informasi untuk pengambilan keputusan manajemen

### Langkah-langkah:
1. **Gunakan Dashboard untuk Ringkasan**
   - Buka menu "ICORF" > "Dashboard"
   - Lihat metrik utama: Jumlah total kontrol, kontrol efektif, risiko tinggi
   - Gunakan filter untuk fokus pada bagian organisasi tertentu

2. **Generate Laporan Kustom**
   - Buka menu "ICORF" > "Pelaporan"
   - Set parameter laporan:
     - Jenis Laporan: "Efektivitas Kontrol"
     - Periode: Q1 2024
     - Termasuk hasil pengujian: Ya
     - Termasuk penilaian risiko: Ya

3. **Analisis Hasil Laporan**
   - Tinjau kontrol yang menunjukkan efektivitas rendah
   - Identifikasi proses bisnis dengan paling banyak temuan
   - Evaluasi distribusi risiko dalam organisasi

4. **Gunakan Fitur Ekspor**
   - Buka menu "Ekspor" pada entri kontrol atau risiko sesuai kebutuhan
   - Pilih format Excel untuk analisis lanjutan
   - Ekspor data untuk disusun dalam presentasi manajemen

5. **Bandingkan Dengan Periode Sebelumnya**
   - Generate laporan untuk periode sebelumnya
   - Bandingkan metrik penting untuk mengidentifikasi perbaikan atau kemunduran
   - Susun analisis tren untuk disajikan dalam rapat manajemen

6. **Tindak Lanjut Berdasarkan Analisis**
   - Gunakan informasi dari laporan untuk mengidentifikasi kontrol yang perlu diperkuat
   - Update prioritas dalam jadwal pengujian berdasarkan hasil analisis
   - Prioritaskan pelatihan atau sumber daya tambahan di area yang bermasalah

---

## Skenario 7: Penanganan Temuan Negatif dan Proses Remediasi

### Latar Belakang
Dalam pelaksanaan audit semesteran, ditemukan bahwa kontrol otorisasi pada pengeluaran kas tidak berjalan secara efektif. Banyak transaksi melebihi batas otorisasi yang ditentukan tidak memiliki persetujuan yang memadai dari manajemen. Temuan ini merupakan temuan negatif yang memerlukan tindakan korektif segera untuk menghindari risiko kehilangan aset atau fraud.

### Tujuan
- Mendokumentasikan temuan negatif secara menyeluruh
- Mengembangkan rencana remediasi yang efektif
- Melacak pelaksanaan perbaikan hingga selesai
- Memperkuat kontrol internal untuk mencegah kejadian serupa di masa depan
- Menyediakan akuntabilitas atas tindakan perbaikan

### Langkah-langkah:
1. **Dokumentasi Temuan Negatif**
   - Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
   - Buat temuan baru dengan informasi:
     - Nama: "Kegagalan Kontrol Otorisasi Pengeluaran Kas"
     - Kode: FIND-OUTCASH-001
     - Tipe: "Control Failure"
     - Tingkat Keparahan: "Material Weakness"
     - Deskripsi: "Ditemukan 47 transaksi pengeluaran kas di atas Rp. 50,000,000 tanpa otorisasi manajer"
     - Kaitkan dengan: Proses "Pengeluaran Kas", Kontrol "Otorisasi Pengeluaran", Risiko "Pengeluaran Tanpa Otorisasi"
     - Tanggal Ditemukan: tanggal pelaksanaan audit
     - Status: "Open"

2. **Analisis Penyebab Akar**
   - Di bagian "Penyebab Akar", dokumentasikan:
     - Ketidaktahuan staf tentang kebijakan otorisasi
     - Sistem otorisasi yang tidak terintegrasi dengan sistem pengeluaran
     - Tekanan waktu dalam proses pembayaran yang membuat staf melewati prosedur
   - Evaluasi dampak finansial dari kegagalan kontrol ini

3. **Pembuatan Rencana Tindakan Remediasi**
   - Buka bagian "Rencana Tindakan" atau menu "ICORF" > "Kepatuhan" > "Rencana Tindakan"
   - Buat beberapa rencana tindakan:
     - Rencana 1: "Pelatihan ulang staf terhadap kebijakan otorisasi"
       - Pemilik: HR Manager
       - Target: 30 hari
       - Prioritas: Tinggi
       - Keterangan: "Semua staf yang menangani pengeluaran harus mengikuti pelatihan ulang"
     - Rencana 2: "Integrasi sistem otorisasi dengan sistem pengeluaran"
       - Pemilik: IT Manager
       - Target: 90 hari
       - Prioritas: Tinggi
       - Keterangan: "Sistem harus mencegah entri transaksi tanpa otorisasi yang sesuai"
     - Rencana 3: "Revisi kebijakan untuk memperjelas batas otorisasi"
       - Pemilik: Finance Manager
       - Target: 45 hari
       - Prioritas: Sedang
       - Keterangan: "Kebijakan harus diperbarui dengan otorisasi multi-level"

4. **Implementasi Perbaikan Kontrol**
   - Buka menu "ICORF" > "Master Data" > "Kontrol Internal"
   - Revisi kontrol "Otorisasi Pengeluaran":
     - Tambahkan sub-kontrol: "Verifikasi sistem otorisasi"
     - Atur frekuensi: "Per transaksi" (real-time)
     - Update deskripsi untuk menyertakan persyaratan integrasi sistem
   - Buat kontrol tambahan jika diperlukan: "Pemeriksaan berkala terhadap transaksi tanpa otorisasi"

5. **Pemantauan dan Update Status**
   - Secara berkala buka menu "ICORF" > "Kepatuhan" > "Rencana Tindakan"
   - Update status setiap rencana tindakan saat progres dicapai
   - Tambahkan bukti pelaksanaan (dokumen pelatihan, tangkapan layar sistem baru, dsb.)
   - Jika target tidak tercapai, tambahkan catatan dan revisi tanggal target

6. **Pengujian Ulang dan Validasi**
   - Setelah rencana tindakan selesai, lakukan pengujian ulang kontrol yang diperbaiki
   - Buka menu "ICORF" > "Operasional" > "Pengujian Kontrol"
   - Buat entri pengujian baru untuk kontrol yang telah diperbaiki
   - Pastikan hasil menunjukkan kontrol berjalan efektif

7. **Penutupan Temuan**
   - Setelah yakin kontrol telah diperbaiki dan berjalan efektif:
     - Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
     - Update status temuan menjadi "In Progress" saat implementasi
     - Setelah semua rencana tindakan selesai dan divalidasi, update menjadi "Closed"
   - Tambahkan catatan tentang bagaimana perbaikan berhasil dilakukan

8. **Pelaporan dan Dokumentasi**
   - Buka menu "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"
   - Dokumentasikan temuan dan remediasi dalam bagian "Temuan dan Respons Manajemen"
   - Sertakan detail tentang efektivitas tindakan perbaikan
   - Buka menu "ICORF" > "Dashboard" untuk memastikan metrik kontrol diperbarui

9. **Pencegahan di Masa Depan**
   - Tinjau jadwal pengujian kontrol untuk memastikan kejadian serupa tidak terlewat
   - Buka menu "ICORF" > "Operasional" > "Jadwal Pengujian"
   - Tambahkan frekuensi pengujian yang lebih tinggi untuk kontrol yang diperbaiki
   - Pertimbangkan untuk menambahkan peringatan otomatis jika kontrol gagal

---

## Kesimpulan

Ketujuh skenario di atas mencakup berbagai aspek dari implementasi dan pengelolaan Internal Controls Over Financial Reporting sesuai dengan standar COSO 2013 dan POJK No. 15 Tahun 2024. Setiap skenario menunjukkan alur kerja yang berbeda dan menekankan aspek-aspek penting dari manajemen risiko dan kontrol internal:

1. **Skenario 1** membahas implementasi awal dan pemetaan kontrol eksisting
2. **Skenario 2** fokus pada implementasi kontrol untuk proses operasional spesifik
3. **Skenario 3** menunjukkan proses sertifikasi senior management dan kepatuhan POJK
4. **Skenario 4** menggambarkan respons sistematis terhadap temuan audit
5. **Skenario 5** menekankan perencanaan dan penjadwalan pengujian kontrol
6. **Skenario 6** menyoroti analisis dan pelaporan untuk pengambilan keputusan
7. **Skenario 7** secara khusus menangani temuan negatif dan proses remediasi

Semua skenario ini dapat digunakan untuk pelatihan pengguna, demonstrasi sistem, atau referensi dalam implementasi ICORF di organisasi keuangan.

---

### 12. Kalkulasi Materialitas dan Pemetaan Akun (SK BUMN Compliance)

#### Latar Belakang
Sebuah perusahaan BUMN perlu menghitung materialitas secara otomatis sesuai dengan ketentuan POJK No. 15 Tahun 2024 dan Surat Keputusan BUMN. Perusahaan juga perlu memetakan akun buku besar ke item laporan keuangan untuk analisis materialitas yang komprehensif.

#### Tujuan
- Menghitung Overall Materiality dan Performance Materiality secara otomatis
- Membuat pemetaan akun GL ke FSLI (Financial Statement Line Items)
- Memastikan kepatuhan terhadap SK BUMN dan POJK 15/2024
- Meningkatkan akurasi penilaian materialitas

#### Langkah-langkah:
1. **Hitung Materialitas**
   - Buka menu "ICORF" > "Master Data" > "Kalkulator Materialitas"
   - Buat perhitungan baru dengan informasi:
     - Nama: "Perhitungan Materialitas Tahun 2024"
     - Tahun Fiskal: 2024
     - Perusahaan: PT. Contoh BUMN
     - Basis Perhitungan: Pendapatan
     - Pendapatan: 1000000000000 (1 Triliun)
     - Aset Total: 1500000000000 (1.5 Triliun)
     - Laba Bersih: 100000000000 (100 Miliar)
     - Persentase Overall Materiality: 0.5%
     - Persentase Performance Materiality: 75%

2. **Buat Pemetaan Akun**
   - Buka menu "ICORF" > "Master Data" > "Pemetaan Akun GL-FSLI"
   - Buat pemetaan baru:
     - Nama: "Pemetaan Pendapatan 2024"
     - Kode Akun GL: "41001"
     - Deskripsi Akun GL: "Pendapatan Operasional"
     - FSLI: "Pendapatan"
     - Deskripsi FSLI: "Pendapatan dari operasional utama"
     - Tingkat Signifikansi: Signifikan
     - Status: Aktif
     - Hubungkan ke perhitungan materialitas "Perhitungan Materialitas Tahun 2024"

3. **Gunakan Pemetaan untuk Analisis Materialitas**
   - Di form kalkulator materialitas, lihat bagian "Pemetaan Akun" yang menunjukkan akun yang terkait
   - Lakukan validasi bahwa pemetaan akun sudah benar

4. **Verifikasi Kepatuhan SK BUMN**
   - Pastikan semua atribut khusus SK BUMN telah diimplementasikan
   - Periksa bahwa kontrol-kontrol sesuai persyaratan BUMN

---

### 13. Penilaian Mandiri Kontrol (Control Self-Assessment - CSA)

#### Latar Belakang
Lini 1 (pemilik proses/kontrol) perlu melakukan penilaian mandiri terhadap efektivitas kontrol yang mereka miliki. Proses ini kemudian direview oleh Lini 2 (tim risiko/ICOFR) sebelum proses sertifikasi.

#### Tujuan
- Meningkatkan tanggung jawab Lini 1 terhadap efektivitas kontrol
- Memberikan input langsung dari pemilik kontrol tentang efektivitas kontrol
- Menyediakan bukti dokumentasi untuk proses sertifikasi
- Mengintegrasikan CSA ke dalam workflow sertifikasi

#### Langkah-langkah:
1. **Buat CSA oleh Pemilik Kontrol (Lini 1)**
   - Buka menu "ICORF" > "Operasional" > "Penilaian Mandiri Kontrol"
   - Buat CSA baru:
     - Nama CSA: "CSA Pengeluaran Kas Q1 2024"
     - Kode: CSA-OUTCASH-001
     - Kontrol: "Otorisasi Pengeluaran Dana"
     - Periode Penilaian: Q1 2024
     - Tanggal Penilaian: 31 Mar 2024
     - Pemilik Kontrol: Finance Manager (Lini 1)
     - Reviewer CSA: Risk Manager (Lini 2)
     - Tipe Penilaian: Triwulanan

2. **Isi Formulir CSA**
   - Apakah desain kontrol efektif?: Ya
   - Apakah kontrol beroperasi secara efektif?: Ya
   - Apakah kontrol dilaksanakan sesuai frekuensi?: Ya
   - Apakah dokumentasi kontrol akurat?: Ya
   - Apakah pengecualian ditangani dengan baik?: Tidak (catat temuan)

3. **Dokumentasikan Temuan dan Rekomendasi**
   - Di bagian temuan CSA: "Beberapa pengeluaran tanpa dokumentasi yang memadai"
   - Rekomendasi: "Perkuat dokumentasi untuk pengeluaran kecil"
   - Status: Selesai (oleh Lini 1)

4. **Review oleh Lini 2 (Risk/ICOFR Team)**
   - Lini 2 menerima notifikasi tentang CSA yang siap direview
   - Buka CSA dan evaluasi hasil penilaian
   - Tambahkan catatan review
   - Setujui CSA atau kembalikan untuk perbaikan

5. **Hubungkan dengan Temuan dan Tindak Lanjut**
   - Dari CSA, buat temuan terkait jika diperlukan
   - Hubungkan ke rencana tindakan untuk perbaikan
   - Integrasi dengan laporan POJK 15/2024

6. **Gunakan Hasil CSA dalam Penilaian Kepatuhan**
   - Hasil CSA digunakan dalam proses sertifikasi
   - Integrasikan dengan laporan efektivitas kontrol
   - Update dashboard dengan hasil CSA

---

### 14. Klasifikasi Kekurangan Otomatis dan Kuantifikasi Dampak

#### Latar Belakang
Temuan dari audit internal dan eksternal perlu diklasifikasikan secara otomatis ke dalam kategori kekurangan kontrol, kekurangan signifikan, atau kelemahan material berdasarkan kriteria kuantitatif dan kualitatif.

#### Tujuan
- Klasifikasi otomatis temuan kontrol berdasarkan kriteria POJK 15/2024
- Kuantifikasi dampak finansial dari temuan kontrol
- Menentukan tingkat keparahan temuan secara konsisten
- Integrasi dengan laporan POJK 15/2024

#### Langkah-langkah:
1. **Buat Temuan dengan Kuantifikasi Dampak**
   - Buka menu "ICORF" > "Kepatuhan" > "Temuan ICORF"
   - Buat temuan baru:
     - Nama: "Kesalahan Pengakuan Pendapatan"
     - Kode: FIND-REVREC-001
     - Tipe: Control Deficiency
     - Deskripsi: "Pendapatan tidak diakui sesuai dengan prinsip akuntansi"
     - Dampak Kuantitatif: 500000000 (Rp. 500 jt)
     - Mata Uang Dampak: IDR
     - Skor Kualitatif: 4 (dari skala 1-5)
     - Kuantifikasi Dampak: "Dampak keuangan Rp. 500 jt, melebihi threshold materialitas 0.5% dari pendapatan"

2. **Sistem Klasifikasi Otomatis**
   - Sistem secara otomatis mengklasifikasikan temuan berdasarkan threshold:
     - Kelemahan Material: Jika dampak melebihi Overall Materiality
     - Kekurangan Signifikan: Jika dampak antara Performance Materiality dan Overall Materiality
     - Kekurangan Kontrol: Jika dampak di bawah Performance Materiality
   - Atau berdasarkan penilaian kualitatif

3. **Validasi Klasifikasi oleh Manajemen**
   - Manajemen meninjau klasifikasi yang dihasilkan secara otomatis
   - Melakukan penyesuaian jika diperlukan berdasarkan pertimbangan kualitatif
   - Menyetujui klasifikasi akhir sebelum dimasukkan ke laporan

4. **Integrasi dengan Laporan POJK**
   - Buka menu "ICORF" > "Kepatuhan" > "Laporan POJK 15/2024"
   - Temuan dengan klasifikasi otomatis muncul dalam laporan
   - Jumlah temuan berdasarkan klasifikasi ditampilkan
   - Respons manajemen terhadap temuan terdokumentasi

5. **Gunakan dalam Proses Sertifikasi**
   - Hasil klasifikasi digunakan sebagai input untuk sertifikasi CEO/CFO
   - Manajemen menilai apakah temuan mengindikasikan kegagalan material dalam kontrol internal
   - Integrasi ke dalam sertifikasi ICORF

---

### 15. Penggunaan Fitur Copy Period untuk Efisiensi RCM

#### Latar Belakang
Perusahaan ingin meningkatkan efisiensi dalam proses dokumentasi RCM (Risk Control Matrix) karena menurut rekomendasi PwC, sekitar 80-90% dari RCM biasanya tetap sama dari tahun ke tahun. Fitur copy period memungkinkan penyalinan data dari satu tahun fiskal ke tahun berikutnya.

#### Tujuan
- Meningkatkan efisiensi dokumentasi RCM
- Mengurangi waktu dan biaya dalam proses implementasi tahunan
- Memastikan konsistensi kontrol dari tahun ke tahun
- Memungkinkan fokus pada perubahan penting saja

#### Langkah-langkah:
1. **Siapkan Data untuk Copy Period**
   - Verifikasi bahwa data RCM tahun 2023 sudah lengkap dan akurat
   - Pastikan semua proses, risiko, dan kontrol untuk 2023 sudah terdokumentasi
   - Pastikan tidak ada data yang belum selesai dalam tahun 2023

2. **Akses Fitur Copy Period**
   - Buka menu "ICORF" > "Utilitas" > "Salin Periode"
   - Form wizard muncul untuk memilih opsi copy period

3. **Konfigurasi Copy Period**
   - Pilih periode sumber: Tahun Fiskal 2023
   - Pilih periode tujuan: Tahun Fiskal 2024
   - Pilih entitas yang akan disalin:
     - Proses bisnis: Ya
     - Risiko finansial: Ya
     - Kontrol internal: Ya
     - Temuan dan rencana tindakan: Ya
     - Jadwal pengujian: Ya
     - Sertifikasi (arsip): Tidak

4. **Proses Copy Period**
   - Klik tombol "Proses" untuk memulai penyalinan data
   - Sistem akan membuat duplikat data dengan tahun fiskal yang disesuaikan
   - Proses ini akan mempertahankan relasi antar entitas

5. **Validasi Hasil Copy Period**
   - Verifikasi bahwa semua entitas telah disalin dengan benar
   - Periksa bahwa relasi antar entitas tetap terjaga
   - Pastikan tahun fiskal dan tanggal telah diperbarui dengan benar

6. **Update untuk Perubahan Tahun 2024**
   - Buka entitas yang disalin untuk menyesuaikan perubahan:
     - Update frekuensi pengujian yang berubah
     - Hapus atau nonaktifkan kontrol yang tidak lagi relevan
     - Tambahkan kontrol baru yang diperlukan
   - Sesuaikan pemilik kontrol dan pelaksana pengujian

7. **Gunakan sebagai Dasar untuk Tahun 2024**
   - Gunakan data tercopy sebagai dasar untuk perencanaan tahun 2024
   - Fokus hanya pada perubahan dan penyesuaian yang diperlukan
   - Hemat waktu dan tenaga dalam proses dokumentasi tahunan

---

### 16. Implementasi Tiga Lini Pertahanan (Three Lines of Defense)

#### Latar Belakang
Perusahaan perlu mengimplementasikan model Tiga Lini Pertahanan (Three Lines of Defense) sesuai dengan praktik terbaik dan regulasi POJK 15/2024. Ini mencakup peran Lini 1 (pemilik proses), Lini 2 (risiko dan fungsi pengawas internal), dan Lini 3 (audit internal).

#### Tujuan
- Menetapkan tanggung jawab yang jelas bagi masing-masing lini
- Meningkatkan efektivitas pengendalian internal
- Memastikan fungsi pengawasan yang independen
- Mewujudkan kerangka kerja kontrol internal yang komprehensif

#### Langkah-langkah:
1. **Definisikan Peran Lini 1 (Process Owners)**
   - Lini 1 bertanggung jawab atas operasional harian dan pemilik kontrol
   - Akses sistem: Mereka dapat mengakses dan memperbarui kontrol yang mereka miliki
   - Fokus utama: Membangun, mengoperasikan, dan memelihara kontrol internal

2. **Definisikan Peran Lini 2 (Risk & Function Owners)**
   - Lini 2 bertanggung jawab atas pengawasan independen atas kontrol
   - Akses sistem: Mereka dapat meninjau, mengevaluasi, dan mereview efektivitas kontrol
   - Fokus utama: Menilai efektivitas desain dan operasi kontrol

3. **Definisikan Peran Lini 3 (Internal Audit)**
   - Lini 3 bertanggung jawab atas audit independen atas kontrol internal
   - Akses sistem: Mereka dapat meninjau semua data kontrol dan mengirimkan temuan
   - Fokus utama: Mengaudit efektivitas kontrol dan memberikan rekomendasi

4. **Dokumentasi dalam Sistem**
   - Dalam modul kontrol, tetapkan "Pemilik Kontrol" yang mewakili Lini 1
   - Dalam modul temuan, tetapkan reviewer yang mewakili Lini 2 dan Lini 3
   - Dalam CSA, tetapkan pemilik sebagai Lini 1 dan reviewer sebagai Lini 2

5. **Workflow dan Persetujuan**
   - Buat workflow yang melibatkan ketiga lini dalam proses sertifikasi
   - Contoh: Lini 1 membuat CSA → Lini 2 mereview → Lini 3 mengaudit → Manajemen menyetujui

6. **Dashboard dan Pelaporan per Lini**
   - Gunakan filter berdasarkan peran untuk menampilkan data yang relevan
   - Lini 1 melihat kontrol yang mereka miliki
   - Lini 2 melihat area yang mereka supervisi
   - Lini 3 melihat hasil audit dan temuan

7. **Integrasi dengan Proses Sertifikasi**
   - Hasil evaluasi dari ketiga lini digunakan dalam sertifikasi CEO/CFO
   - Dashboard menunjukkan efektivitas kontrol dari perspektif masing-masing lini
   - Laporan POJK 15/2024 mencerminkan input dari ketiga lini

---

## Kesimpulan Tambahan

Dengan ditambahkannya skenario 12 hingga 16, kini modul ICORF memiliki dokumentasi lengkap yang mencakup semua fitur utama yang dikembangkan berdasarkan rekomendasi PwC dan persyaratan POJK No. 15 Tahun 2024:

8. **Skenario 12** membahas kalkulasi materialitas dan pemetaan akun sesuai SK BUMN
9. **Skenario 13** menunjukkan proses Control Self-Assessment untuk tiga lini pertahanan
10. **Skenario 14** menyoroti sistem klasifikasi kekurangan otomatis dengan kuantifikasi dampak
11. **Skenario 15** menggambarkan penggunaan fitur copy period untuk efisiensi kerja
12. **Skenario 16** secara khusus menangani implementasi Three Lines of Defense

Semua skenario ini dapat digunakan untuk pelatihan pengguna, demonstrasi sistem, atau referensi dalam implementasi ICORF di organisasi keuangan.