<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 5
<br>
SPESIFIKASI KEBUTUHAN PERANGKAT LUNAK (SKPL)
</h1>
<br>

## *Food Waste Stop*

### Untuk: *Aurelia Jennifer Gunawan*

Dipersiapkan oleh:
| Informasi | Keterangan |
| --- | --- |
| Kelas | *K02* |
| Kelompok | *G06*  |

| NIM | Nama |
|---|---|
| *13525122* | *Nadia Aulia Syafarani* |
| *13525041* | *Renata Puspanegara Ninagan* |
| *13525119* | *Ghina Emelia Yantes* |
| *13525017* | *Cendra Asih Chairunnisa* |
| *13525089* | *Sherin Felicia Danessa* |
---

## Daftar Perubahan

| Revisi | Deskripsi |
| :--- | :--- |
| *A* | *Deskripsikan perubahan yang dilakukan dari dokumen sebelumnya pada dokumen ini. Jika tidak terdapat perubahan, harap kosongkan tabel.* |
| *B* |  |
| *C* |  |
| ... |  |

<br>

# BAB 1: Pendahuluan

## 1.1 Tujuan Penulisan Dokumen
Tuliskan dengan ringkas tujuan dokumen SKPL ini dibuat dan siapa saja yang akan menggunakan dokumen ini.

## 1.2 Lingkup Masalah
Tuliskan dengan ringkas nama aplikasi dan deskripsi singkatnya. Bagian ini maksimal berisi satu paragraf, dapat diringkas dari BAB 1 *Analisis Permasalahan* pada dokumen *Topic Brainstorming*.

## 1.3 Definisi, Istilah, dan Singkatan
Semua definisi dan singkatan yang digunakan dalam dokumen ini beserta penjelasannya.

Tabel 1.3. Definisi Istilah dan Singkatan

| Singkatan, Akronim, atau Istilah | Penjelasan |
| :--- | :--- |
| *P/L* | *Singkatan dari Perangkat Lunak, yaitu aplikasi yang memberikan perintah kepada komputer untuk menjalankan tugas tertentu.* |
| *SKPL* | *Singkatan dari Spesifikasi Kebutuhan Perangkat Lunak, yaitu dokumen yang merangkum kriteria-kriteria yang diperlukan untuk membangun aplikasi menjalankan tugasnya.* |
| *KF* | *Singkatan dari Kebutuhan Fungsional.* |
| *KNF* | *Singkatan dari Kebutuhan Non-Fungsional.* |
| *UC* | *Singkatan dari Use Case.* |
| *EARS* | *Easy Approach to Requirements Syntax, yaitu pola penulisan kebutuhan agar konsisten dan mudah diuji.* |
| *...* | *...* |

## 1.4 Aturan Penomoran
Tuliskan aturan penomoran (ID) yang digunakan dalam dokumen ini. Gunakan pola ID yang **sama** dengan yang sudah dipakai pada dokumen-dokumen sebelumnya, jangan membuat pola baru di dokumen ini.

Tabel 1.4. Aturan Penomoran

| Hal/Bagian | Penomoran | Keterangan |
| :--- | :--- | :--- |
| *Kebutuhan Fungsional* | *KFXX* | |
| *Kebutuhan Non-Fungsional* | *KNFXX* | |
| *Aktor* | *AXX* | |
| *Use Case* | *UCXX* | |
| *Kelas* | *CXX* | |
| *...* | *...* |

## 1.5 Referensi
Dokumentasi P/L yang dirujuk oleh dokumen ini. Referensi dapat berupa buku, panduan, ataupun dokumentasi lain yang dipakai dalam pengembangan P/L ini.

## 1.6 Deskripsi Umum Dokumen (Ikhtisar)
Tuliskan sistematika pembahasan dokumen SKPL ini secara runut (misalnya: BAB 2 membahas deskripsi umum P/L, BAB 3 membahas kebutuhan fungsional dan non-fungsional, dst).

---

# BAB 2: Deskripsi Perangkat Lunak

## 2.1 Deskripsi Umum Sistem
Bagian ini dapat disalin dari BAB 1.1 *Deskripsi Umum Sistem* pada dokumen *Requirement Gathering*, disesuaikan bila ada perubahan alur bisnis. Lengkapi dengan gambaran proses bisnis dalam bentuk *Activity Diagram* (boleh disalin dan diperbarui dari 3.3 *Model Proses Bisnis* pada dokumen *Topic Brainstorming*).

Food Waste Stop merupakan sistem web aplikasi yang menjadi wadah transaksi makanan surplus yang menyediakan dua sisi pengguna, yaitu Penjual dan Pembeli. Menurut Penjual, sistem diharapkan menjadi solusi meminimalisir kerugian. Sistem menjadi sarana penjualan makanan surplus yang masih layak konsumsi. Dengan adanya sistem, konsumer (Pembeli) dapat memperoleh informasi serta memesan makanan surplus dengan harga lebih murah. Alur kerja sistem dimulai ketika Penjual mendaftarkan profil toko dan menambahkan makanan surplus yang tersedia beserta harga dan deskripsinya ke dalam sistem. Pembeli kemudian dapat menjelajahi daftar makanan surplus tersebut, memilih makanan yang diminati beserta jumlah kuantitasnya, lalu melakukan pemesanan. Alur ini berulang setiap kali terdapat makanan surplus baru yang perlu dipublikasikan oleh Penjual atau pesanan baru yang dibuat oleh Pembeli. Secara umum, Food Waste Stop merupakan satu kesatuan utuh yang diharapkan menghadirkan manfaat timbal balik berupa pengurangan kerugian ekonomi bagi Penjual, akses makanan terjangkau bagi Pembeli, serta kontribusi terhadap upaya pengurangan sampah makanan di masyarakat.

<p align="center">
<img alt="Swimlane Diagram Sistem Login Penjual" src="https://github.com/user-attachments/assets/40124979-d1a9-45d3-86da-ed159426420e" width="70%"> 
</p>
<p align="center">
<i>Gambar 1. Swimlane Diagram Sistem Login Penjual</i>
</p>

<br>

<p align="center">
<img alt="Swimlane Diagram Sistem Login Pembeli" src="https://github.com/user-attachments/assets/c5ff9026-2821-4e41-9777-4a52b1c73a60" width="70%"> 
</p>
<p align="center">
<i>Gambar 2. Swimlane Diagram Sistem Login Pembeli</i>
</p>

<br>

<p align="center">
<img alt="Swimlane Diagram Transaksi Pembelian Makanan di Aplikasi" src="https://github.com/user-attachments/assets/949d3571-fb1f-4f49-8fa5-b5f41b13507f" width="70%"> 
</p>
<p align="center">
<i>Gambar 3. Swimlane Diagram untuk Transaksi Pembelian Makanan di Aplikasi</i>
</p>

<br>

<p align="center">
<img alt="Swimlane Diagram untuk Edit Data Penjualan Toko" src="https://github.com/user-attachments/assets/df73195a-de37-42ca-a3b4-93583ae10d38" width="70%"> 
</p>
<p align="center">
<i>Gambar 4. Swimlane Diagram untuk Edit Data Penjualan Toko</i>
</p>

<br>

<p align="center">
<img alt="Swimlane Diagram untuk Reward dari Login Streak" src="https://github.com/user-attachments/assets/3febbd8d-a276-4754-9200-cd2bee1feacd" width="70%"> 
</p>
<p align="center">
<i>Gambar 4. Swimlane Diagram untuk Reward dari Login Streak</i>
</p>

<br>

## 2.2 Deskripsi Umum Perangkat Lunak
Diisi dengan deskripsi umum perangkat lunak untuk mendukung proses bisnis yang telah diuraikan pada sub-bab sebelumnya. Uraian harus menunjukkan lingkup perangkat lunak, mencakup keterkaitan perangkat lunak dengan sistem lain di luar (misalnya *Payment Gateway* atau layanan pihak ketiga lain yang dipakai).

*Contoh narasi:* "*[Nama P/L]* merupakan aplikasi *[deskripsi singkat]* yang berinteraksi dengan *Payment Gateway (dummy)* untuk memproses otorisasi pembayaran. Sistem menerima input dari *Pelanggan* melalui antarmuka aplikasi dan mengirimkan permintaan transaksi ke *Payment Gateway* setiap kali pelanggan melakukan checkout."

## 2.3 Pengguna dan Kebutuhan Pengguna Perangkat Lunak
| :--- | :--- |
| *Penjual* | *Pengguna yang mengelola listing makanan surplus, meliputi menambahkan, mengurangkan, mengedit, dan memantau pendapatan penjualan* |
| *Pembeli* | *Pengguna yang melihat, mencari, memilih, dan membeli listing makanan surplus* |

## 2.4 Batasan Perangkat Lunak
Batasan yang harus dituliskan, di antaranya:
1. *P/L harus memakai file data/API dari sistem lain (sebutkan, misal Payment Gateway dummy).*
2. *P/L harus memakai format data yang sama dengan sistem lain.*
3. *P/L harus berfungsi pada platform tertentu (misal: web browser modern, atau desktop Windows dan Linux).*
4. *...*

## 2.5 Lingkungan Operasi Perangkat Lunak
Spesifikasi *operating system* atau lingkungan yang dibutuhkan P/L untuk beroperasi. Bagian ini digunakan untuk memastikan pengguna memiliki spesifikasi yang cukup untuk menjalankan P/L. Misalnya mencakup komponen server, client, OS, DBMS, tetapi tidak menutupi kemungkinan komponen lain.

| Komponen | Spesifikasi |
| :--- | :--- |
| *Server* | *[contoh: Node.js v20, dijalankan pada layanan cloud]* |
| *Client* | *[contoh: Web Browser modern (Chrome, Firefox terbaru)]* |
| *DBMS* | *[contoh: PostgreSQL 15]* |
| *OS* | *[contoh: Cross-platform (Windows/Linux/MacOS) melalui browser]* |
| *...* | *...* |

---

# BAB 3: Deskripsi Kebutuhan Perangkat Lunak

## 3.1 Kebutuhan Fungsional (KF)
Salin ulang **seluruh Kebutuhan Fungsional (KF)** versi terbaru dari BAB 2.1 dokumen *Class Diagram* (sudah versi final dan sudah memakai format EARS). Pastikan ID Kebutuhan (kolom "ID Kebutuhan") juga konsisten dengan ID pada tabel Pemetaan Kebutuhan di dokumen *Requirement Gathering*.

Tabel 3.1. Kebutuhan Fungsional

| ID UC | Nama Use Case | Deskripsi Singkat | Aktor | ID KF |
| :--- | :--- | :--- | :--- | :--- |
| *UC01* | *Menambahkan listing makanan surplus* | *Penjual mengisi form makanan surplus dan divalidasi sistem sebelum dikirim* | *Penjual* | *KF01, KF07* |
| *UC02* | *Melihat listing makanan surplus* | *Pembeli dapat melihat lisiting makanan surplus* | *Pembeli* | *KF02, KF07* |
| *UC03* | *Melihat detail makanan surplus* | *Pembeli dapat mengklik salah satu makanan dalam listing dan melihat detailnya* | *Pembeli* | *KF02, KF07* |
| *UC04* | *Menyaring listing makanan surplus* | *Pembeli memilih ketentuan makanan surplus tertentu dan sistem menyaring makanan surplus apa yang ditampilkan sesuai ketentuan* | *Pembeli* | *KF03, KF07* |
| *UC05* | *Melakukan pembayaran* | *Pembeli melakukan pembayaran dengan ditampilkan QRIS dummy* | *Pembeli* | *KF04* |
| *UC06* | *Mengedit listing* | *Penjual dapat mengubah  dan menyimpan perubahan isi detail pada listing* | *Penjual* | *KF05, KF07* |
| *UC07* | *Login ke sistem* | *Pengguna dapat masuk dan melakukan login ke sistem dengan mengisi kredensial mereka* | *Penjual, Pembeli* | *KF06, KF07* |
| *UC08* | *Mengklaim reward login* | *Pembeli yang sudah mengumpulkan cukup banyak poin login dapat mengklaim reward login* | *Pembeli* | *KF06, KF07* |
| *UC09* | *Menghapus listing* | *Penjual dapat menghapus listing* | *Penjual* | *KF02, KF07* |

## 3.2 Kebutuhan Non-Fungsional (KNF)
Salin ulang Kebutuhan Non-Fungsional dari BAB 2.5 dokumen *Requirement Gathering*, sesuaikan ID Kebutuhan (kolom "ID Kebutuhan") apabila terjadi perubahan penomoran pada BAB 3.1 di atas.

Tabel 3.2. Kebutuhan Non-Fungsional

| ID KNF | ID Kebutuhan | Parameter | Deskripsi Kebutuhan |
| :--- | :--- | :--- | :--- |
| *KNF01* | *R03* | *Reliability* | *Proses transaksi pembayaran harus memenuhi prinsip ACID untuk mencegah terjadinya data tersangkut (lost update) apabila terjadi kegagalan jaringan di tengah proses.* |
| *KNF02* | *R04* | *Security* | *Sistem harus mengenkripsi PIN atau password pengguna menggunakan algoritma SHA-256 sebelum data dikirimkan ke server, serta tidak menyimpannya dalam bentuk plain-text di database.* |
| *...* | *...* | *...* | *...* |

<sub>*Silakan pilih parameter yang relevan dengan P/L kalian (Availability, Reliability, Ergonomy, Portability, Memory, Response time, Safety, Security, dsb), tidak perlu semua parameter diisi. Lihat kembali dokumen Requirement Gathering untuk penjelasan tiap parameter.*<sub>

---

# BAB 4: Pemodelan Use Case

## 4.1 Identifikasi Aktor
Salin ulang daftar aktor final dari BAB 3.1 dokumen *Use Case & Scenario Use Case* atau *Class Diagram*. Tambahkan ID Aktor mengikuti Aturan Penomoran pada 1.4.

| ID Aktor | Aktor | Deskripsi |
| :--- | :--- | :--- |
| *A01* | *Pelanggan* | *Pengguna yang memesan produk, mengelola keranjang, dan menyelesaikan pembayaran melalui sistem.* |
| *A02* | *Pembeli* | *Pengguna yang melihat, mencari, memilih, dan membeli listing makanan surplus* |

## 4.2 Identifikasi Use Case
Salin ulang daftar Use Case versi terbaru dari BAB 3.2 dokumen *Class Diagram*, pastikan seluruh ID KF yang dirujuk sudah sesuai dengan tabel pada 3.1.

| ID UC | Nama Use Case | Deskripsi Singkat | Aktor | ID KF |
| :--- | :--- | :--- | :--- | :--- |
| *UC01* | *Menambahkan listing makanan surplus* | *Penjual mengisi form makanan surplus dan divalidasi sistem sebelum dikirim* | *Penjual* | *KF01, KF07* |
| *UC02* | *Melihat listing makanan surplus* | *Pembeli dapat melihat lisiting makanan surplus* | *Pembeli* | *KF02, KF07* |
| *UC03* | *Melihat detail makanan surplus* | *Pembeli dapat mengklik salah satu makanan dalam listing dan melihat detailnya* | *Pembeli* | *KF02, KF07* |
| *UC04* | *Menyaring listing makanan surplus* | *Pembeli memilih ketentuan makanan surplus tertentu dan sistem menyaring makanan surplus apa yang ditampilkan sesuai ketentuan* | *Pembeli* | *KF03, KF07* |
| *UC05* | *Melakukan pembayaran* | *Pembeli melakukan pembayaran dengan ditampilkan QRIS dummy* | *Pembeli* | *KF04* |
| *UC06* | *Mengedit listing* | *Penjual dapat mengubah  dan menyimpan perubahan isi detail pada listing* | *Penjual* | *KF05, KF07* |
| *UC07* | *Login ke sistem* | *Pengguna dapat masuk dan melakukan login ke sistem dengan mengisi kredensial mereka* | *Penjual, Pembeli* | *KF06, KF07* |
| *UC08* | *Mengklaim reward login* | *Pembeli yang sudah mengumpulkan cukup banyak poin login dapat mengklaim reward login* | *Pembeli* | *KF06, KF07* |
| *UC09* | *Menghapus listing* | *Penjual dapat menghapus listing* | *Penjual* | *KF02, KF07* |

## 4.3 Use Case Diagram
Salin ulang Use Case Diagram dari BAB 3.3 dokumen *Use Case & Scenario Use Case* atau *Class Diagram* (gunakan versi paling akhir/terbaru apabila terdapat perubahan).

<p align="center">
<img width="100%" alt="Untitled Diagram drawio (4)" src="https://github.com/user-attachments/assets/2cdc32f2-0599-476a-870b-4bc1425b7360" />
</p>
<p align="center">
<i>Gambar 1. Use Case Diagram</i>
</p>
<br>

## 4.4 Skenario Use Case
Salin ulang skenario **setiap** use case (skenario normal dan alternatif) dari BAB 3.4 dokumen *Use Case & Scenario Use Case*, sesuaikan dengan daftar UC final pada 4.2. Jika use case melibatkan lebih dari satu aktor manusia yang benar-benar berinteraksi langsung (misalnya *Kasir* yang memverifikasi transaksi setelah *Pelanggan* membayar), tambahkan kolom aksi tersendiri untuk aktor tersebut di samping kolom "Reaksi Perangkat Lunak". Sistem eksternal otomatis seperti *payment gateway* **bukan aktor**, sehingga interaksinya cukup dituliskan sebagai bagian dari "Reaksi Perangkat Lunak", bukan kolom aktor terpisah.

### 4.4.1 Skenario UC01

**Nama Use Case:** *Menambahkan listing makanan surplus*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual memilih tombol "tambahkan makanan"* | *Sistem menampilkan halaman yang menyediakan tempat untuk mengunggah foto makanan serta kolom terstruktur dan kolom bebas untuk mengisi deskripsi makanan* |
| 2 | *Penjual mengonfirmasi penambahan makanan* | *Sistem mengecek kelengkapan deksripsi, memperbarui listing makanan penjual, dan menampilkan notifikasi penambahan makanan berhasil* |

<br>

**Skenario Alternatif 1: Verifikasi penambahan makanan gagal**


| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual memilih tombol "tambahkan makanan"* | *Sistem menampilkan halaman yang menyediakan tempat untuk mengunggah foto makanan serta kolom terstruktur dan kolom bebas untuk mengisi deskripsi makanan* |
| 2 | *Penjual mengonfirmasi penambahan makanan* | *Sistem mengecek kelengkapan deksripsi dan ditemukan ketidaklengkapan deskripsi wajib (contoh: nama, foto, atau harga makanan yang tidak terisi). Sistem menampilkan pesan error di halaman yang sama dan meminta pelanggan memasukkan bagian yang belum terisi tersebut* |
| 4 | *Pelanggan melanjutkan mengisi* | *Sistem kembali ke langkah 1 skenario normal* |

<br>

**Skenario Alternatif 2: Percobaan keluar saat penambahan makanan**


| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual memilih tombol "Tambahkan Makanan"* | *Sistem menampilkan halaman yang menyediakan tempat untuk mengunggah foto makanan serta kolom terstruktur dan kolom bebas untuk mengisi deskripsi makanan* |
| 2 | *Penjual berupaya keluar dari halaman sebelum menyimpan* | *Sistem menampilkan dialog konfirmasi berisi peringatan bahwa deskripsi yang belum tersimpan akan hilang, disertai opsi untuk tetap berada di halaman atau melanjutkan keluar. * |
| 3 | *Penjual memilih salah satu opsi pada dialog konfirmasi* | *Sistem menerima respons penjual. Jika penjual memilih untuk tetap mengedit, sistem menutup dialog konfirmasi berisi peringatan dan mengembalikan penjual ke halaman penambahan makanan sebelumnya. Jika penjual memilih untuk keluar, sistem membatalkan proses penambahan makanan dan mengarahkan penjual ke halaman utama (profil toko)* |

<sub>*Lanjutkan pola 4.4.x ini untuk setiap ID UC pada 4.2, sampai seluruh use case memiliki skenarionya masing-masing.*<sub>

---

# BAB 5: Pemodelan Kelas

## 5.1 Identifikasi Kelas
Salin ulang seluruh kelas yang telah diidentifikasi dari BAB 4.1 dokumen *Class Diagram*.

| ID Kelas | Nama Kelas | Deskripsi Kelas | ID Use Case |
| :--- | :--- | :--- | :--- |
| *C01* | *Pengguna* | *Peran umum yang menyimpan kredensial akun* | *UC07* |
| *C02* | *Penjual* | *Peran khusus yang menyimpan data akun penjual yang dapat mengelola profil toko, menambah listing, menghapus listing, dan mengedit listing* | *UC01, UC06, UC07, UC09* |
| *C03* | *Pembeli* | *Peran khusus yang menyimpan data akun pembeli yang dapat menelusuri dan membeli listing* | *UC02, UC03, UC04, UC05, UC07, UC08* |
| *C04* | *ListingMakanan* | *Menyimpan informasi mengenai makanan surplus yang ditawarkan, seperti nama, foto, porsi, kondisi, harga, jumlah stok, deskripsi,* | *UC01, UC02, UC03, UC04, UC06, UC09* |
| *C05* | *MetodePembayaran* | *Kelas abstrak yang merepresentasikan metode pembayaran yang dipilih pelanggan yang direalisasikan dengan QRIS dummy* | *UC05* |
| *C06* | *Transaksi* | *Menyimpan catatan pemesanan makanan surplus yang dilakukan oleh pembeli, mencakup informasi kuantitas, total harga, tanggal pesanan, dan status pembayaran* | *UC05* |
| *C07* | *RewardLogin* | *Mengelola poin quest harian yang didapatkan dari aktivitas login harian serta melacak status klaim reward* | *UC07, UC08* |


## 5.2 Diagram Kelas per Use Case
Salin ulang diagram kelas untuk setiap use case dari BAB 4.2 dokumen *Class Diagram*, lengkap dengan tabel atribut dan metode/operasinya.

### 5.2.1 Use Case UC01

**Nama Use Case:** *Memesan Produk*

<p align="center">
<img alt="Contoh Class Diagram" src="./assets/diagram/contoh-class-diagram.webp" width="70%">
</p>
<p align="center">
<i>Gambar 3. Contoh Diagram Kelas Use Case UC01</i>
</p>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C02* | *Pesanan* | *idPesanan, total, status* | *buatPesanan(), hitungTotal()* |
| *C03* | *Keranjang* | *daftarItem* | *tambahItem(), checkout()* |
| *...* | *...* | *...* | *...* |

> Lanjutkan pola **5.2.x** untuk setiap use case pada 4.2.

## 5.3 Diagram Kelas Keseluruhan
Gabungkan seluruh kelas dan hubungan antarkelas dari BAB 4.3 dokumen *Class Diagram* menjadi satu diagram kelas keseluruhan. Pastikan tidak ada kelas yang terduplikasi atau tertinggal.

<p align="center">
<img width="697" height="422" alt="diagram keseluruhan drawio" src="https://github.com/user-attachments/assets/9238241f-4b42-4550-9ae0-a46835934346" />
</p>
<p align="center">
<i>Gambar 10. Diagram Kelas Keseluruhan</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Pengguna* | *idPengguna, email, password* | *login(), validasiKredensial()* |
| *C02* | *Penjual* | *idPenjual, toko* | *tambahMakanan(), editListing(), simpanPerubahan(), hapusListing()* |
| *C03* | *Pembeli* | *idPembeli, nama* | *tampilkanListingAll(), lihatDeskripsiMakanan(), cariListing(), saringListing(), checkout(), bayar(), klaimReward()* |
| *C04* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *tambahListing(), ambilListingAll(), deskripsiMakanan(), saringKataKunci(), saringRentangHarga(), kurangiStok(), validasiInput(), updateDatabase(), konfirmasiHapus(), hapusDariDatabase()* |
| *C05* | *MetodePembayaran* | *kodeQRIS* | *tampilkanQRIS()* |
| *C06* | *idTransaksi, totalHarga, tanggal, status* | *hitungTotal(), perbaruiStatus()* |
| *C07* | *RewardLogin* | *idReward, poinTerkumpul, statusKlaim* | *validasiPoin(), prosesKlaim(), konfirmasiKlaim()* |

---

# BAB 6: Traceability
Salin ulang tabel Traceability dari BAB 5 dokumen *Class Diagram*, cocokkan setiap Kebutuhan Fungsional, Use Case, dan Kelas yang saling terkait.

| ID Kelas | ID Use Case | ID KF |
| :--- | :--- | :--- |
| *C01* | *UC07* | *KF06, KF07* |
| *C02* | *UC01, UC06, UC07, UC09* | *KF01, KF02, KF05, KF06,KF07* |
| *C03* | *UC02, UC03, UC04, UC05, UC07, UC08* | *KF02, KF03, KF04, KF06, KF07* |
| *C04* | *UC01, UC02, UC03, UC04, UC06, UC09* | *KF01, KF02, KF03, KF04, KF05, KF07* |
| *C05* | *UC05* | *KF04* |
| *C06* | *UC05* | *KF04* |
| *C07* | *UC07, UC08* | *KF06, KF07* |

---

# Referensi
- Diagram UML: [https://www.drawio.com/](https://www.drawio.com/), [https://staruml.io/](https://staruml.io/)
