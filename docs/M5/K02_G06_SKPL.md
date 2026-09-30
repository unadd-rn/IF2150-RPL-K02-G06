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
| *A* | *Memperbaiki tabel diagram kelas keseluruhan.* |

<br>

# BAB 1: Pendahuluan

## 1.1 Tujuan Penulisan Dokumen
Dokumen SKPL ini dibuat untuk menjelaskan apa itu web aplikasi Food Waste Stop untuk memenuhi Tugas Besar RPL. Dokumen SKPL digunakan untuk para asisten dan/atau dosen RPL.

## 1.2 Lingkup Masalah
Food Waste Stop merupakan web aplikasi untuk kegiatan jual-beli makanan surplus. Food Waste Stop berfokus menjadi solusi permasalahan sampah makanan industri. Selain itu, Food Waste Stop juga mengurangi kerugian ekonomi industri.

## 1.3 Definisi, Istilah, dan Singkatan
Tabel 1.3. Definisi Istilah dan Singkatan

| Singkatan, Akronim, atau Istilah | Penjelasan |
| :--- | :--- |
| *P/L* | *Singkatan dari Perangkat Lunak, yaitu aplikasi yang memberikan perintah kepada komputer untuk menjalankan tugas tertentu.* |
| *SKPL* | *Singkatan dari Spesifikasi Kebutuhan Perangkat Lunak, yaitu dokumen yang merangkum kriteria-kriteria yang diperlukan untuk membangun aplikasi menjalankan tugasnya.* |
| *KF* | *Singkatan dari Kebutuhan Fungsional.* |
| *KNF* | *Singkatan dari Kebutuhan Non-Fungsional.* |
| *UC* | *Singkatan dari Use Case.* |
| *EARS* | *Easy Approach to Requirements Syntax, yaitu pola penulisan kebutuhan agar konsisten dan mudah diuji.* |

## 1.4 Aturan Penomoran
Tabel 1.4. Aturan Penomoran

| Hal/Bagian | Penomoran | Keterangan |
| :--- | :--- | :--- |
| *Kebutuhan Fungsional* | *KFXX* | *Layanan atau fungsi yang harus disediakan sistem, yaitu apa yang dapat dilakukan sistem terhadap masukan dan bagaimana sistem berperilaku pada situasi tertentu* |
| *Kebutuhan Non-Fungsional* | *KNFXX* | *Batasan atau kualitas yang harus dipenuhi sitem, seperti performa, keamanan, keandalan, dan kemudahan penggunaan* |
| *Aktor* | *AXX* | *Pihak di luar sistem (pengguna, perangkat, atau sistem lain) yang berinteraksi dengan sistem* |
| *Use Case* | *UCXX* | *Rangkaian interaksi antara aktor dan sistem untuk mencapai suatu tujuan tertentu* |
| *Kelas* | *CXX* | *Representasi objek dalam sistem yang memiliki atribut dan metode, digunakan dalam perancangan struktur sistem* |
| *...* | *...* |

## 1.5 Referensi
PowerPoint Rekayasa Perangkat Lunak Minggu 1 "Disiplin-Bukti-Konteks"
PowerPoint Rekayasa Perangkat Lunak Minggu 2 "Efisiensi Kebutuhan" & "Perumusan Kebutuhan"
PowerPoint Rekayasa Perangkat Lunak Minggu 3 "Skenario dan Keterlacakan" & "Diagram Use Case"
PowerPoint Rekayasa Perangkat Lunak Minggu 4 "Objek, Tanggung Jawab, dan Kolaborasi" & "Stereotipe, Gaya Kendali, dan Lapisan"
PowerPoint Rekayasa Perangkat Lunak Minggu 5 "SKPL"
PowerPoint Asistensi Rekayasa Perangkat Lunak  "Class Diagram"

## 1.6 Deskripsi Umum Dokumen (Ikhtisar)
BAB 2 membahas deskripsi P/L
Bab 3 membahas deskripsi Kebutuhan P/L
Bab 4 menampilkan pemodelan Use Case
Bab 5 menampilkan pemodelan Kelas

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
<i>Gambar 5. Swimlane Diagram untuk Reward dari Login Streak</i>
</p>

<br>

## 2.2 Deskripsi Umum Perangkat Lunak
Diisi dengan deskripsi umum perangkat lunak untuk mendukung proses bisnis yang telah diuraikan pada sub-bab sebelumnya. Uraian harus menunjukkan lingkup perangkat lunak, mencakup keterkaitan perangkat lunak dengan sistem lain di luar (misalnya *Payment Gateway* atau layanan pihak ketiga lain yang dipakai).

Food Waste Stop adalah aplikasi berbasis web (*web application*) yang memberikan fasilitas transaksi jual beli makanan surplus yang masih layak dikonsumsi untuk mengurangi limbah makanan indrustri dan kerugian ekonomi penjual. Aplikasi ini memiliki layanan simulasi *Payment Gateway* dalam bentuk QRIS *dummy* untuk memproses dan mengonfirmasi pembayaran secara daring. Sistem akan menampilkan simulasi pembayaran setelah menerima input dari pengguna pada sisi pembeli dalam bentuk pencarian, penyaringan, lalu pemilihan serta pemesanan makanan surplus. Di sisi lain, penjual mengelola listing makanan surplus melalui antarmuka web dari penambahan makanan baru, pembaruan stok dan harga diskon, sampai pengeditan dan penghapusan listing. Selain dari fungsi transaksi yang merupakan inti dari sistem ini, perangkat lunak mengintegrasikan gamifikasi berupa *quest login harian* yang secara otomatis mencatat *steak* pengguna dan memberikan poin reward yang dapat ditukarkan untuk kupon potongan harga transaksi.

## 2.3 Pengguna dan Kebutuhan Pengguna Perangkat Lunak
| Aktor | Deskripsi |
| :--- | :--- |
| *Penjual* | *Pengguna yang mengelola listing makanan surplus, meliputi mendaftarkan toko, menambahkan makanan surplus baru (foto sto, porsi, harga, dan deskripsi), mengurangkan atau mengedit data listing, dan memantau pesanan dan pendapatan penjualan* |
| *Pembeli* | *Pengguna yang melihat, mencari, menyaring daftar listing, melihat detail makanan surplus, melakukan pemesanan dan pembayaran melalui simulasi pembayaran, dan melakukan **login** harian untuk mendapatkan poin.* |

## 2.4 Batasan Perangkat Lunak
Batasan yang harus dituliskan, di antaranya:
1. *Perangkat lunak harus berinteraksi dengan API simulasi **Payment Gateway** (QRIS **dummy**) untuk menampilkan kode pembayaran dan mengonfirmasi status transaksi.*
2. *Berkas gambar makanan yang diunggah oleh penjual ke dalam sistem harus dalam format PNG atau JPG dan berukuran maksimal 10 MB.*
3. *Perangkat lunak tidak menyediakan layanan pengantaran, sehingga pengambilan makanan yang telah dibeli dilakukan secara mandiri oleh pembeli di lokasi toko penjual.*
4. *Perangkat lunak tidak melakukan pengujian kualitas makanan secara langsung, sehingga kelayakan makanan surplus yang dimasukkan ke dalam listing menjadi tanggung jawab penjual.*
5. *Poin yang didapatkan dari **quest login harian** hanya dapat ditukarkan dalam bentuk potongan harga pembelian dalam aplikasi dan tidak bisa dicairkan dalam bentuk uang tunai.*
6. *Perangkat lunak harus berfungsi pada seluruh **web broswer** modern yang terhubung pada jaringan internet.*

## 2.5 Lingkungan Operasi Perangkat Lunak
Spesifikasi *operating system* atau lingkungan yang dibutuhkan P/L untuk beroperasi. Bagian ini digunakan untuk memastikan pengguna memiliki spesifikasi yang cukup untuk menjalankan P/L. Misalnya mencakup komponen server, client, OS, DBMS, tetapi tidak menutupi kemungkinan komponen lain.

| Komponen | Spesifikasi |
| :--- | :--- |
| *Server* | *Server lokal* |
| *Client* | *Web browser modern (Chrome, Firefox, Edge, Safari versi terbaru) di desktop maupun mobile; mendukung PWA* |
| *Front-End* | *Next.js (React), Node.js v20 untuk proses build* |
| *Back-End* | *Fast API* |
| *DBMS* | *PostgreSQL 15 (managed database dari penyedia PaaS)* |
| *OS* | *Windows/Linux/macOS/Android/iOS melalui browser* |

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
<i>Gambar 6. Use Case Diagram</i>
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


### 4.4.2 Skenario UC02

**Nama Use Case:** *Melihat listing makanan surplus*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli melihat listing makanan surplus* | *Sistem mengecek ketersediaan listing makanan surplus, menyembuyikan makanan surplus yang terdeteksi deskripsi sudah melewati kedauluwarsa dan stok habis. Sistem mendapat tidak ada listing yang tersedia* |
| 2 | *(tidak ada aksi lanjutan)* | *Sitem menampilkan listing makanan surplus yang tersedia* |

<br>

**Skenario Alternatif 1: Listing makanan surplus tidak tersedia**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli melihat listing makanan surplus* | *Sistem mengecek ketersediaan listing makanan surplus, menyembuyikan makanan surplus yang terdeteksi deskripsi sudah melewati kedauluwarsa dan stok habis. Sistem mendapat tidak ada listing yang tersedia* |
| 2 | *(tidak ada aksi lanjutan)* | *Sitem menampilkan pesan bahwa saat ini tidak ada makanan surplus yang tersedia* |

<br>

**Skenario Alternatif 2: Kegagalan memuat listing (error teknis)**
| 1 | *Pembeli melihat listing makanan surplus* | *Sistem gagal mengambil data* |
| 2 | *(tidak ada aksi lanjutan)* | *Sitem menampilkan pesan error dan opsi untung memuat ulang* |

### 4.4.3 Skenario UC03

**Nama Use Case:** *Melihat detail makanan surplus*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli membuka halaman listing* | *Sistem menampilkan seluruh listing* |
| 2 | *Pembeli memencet salah satu opsi pada listing makanan surplus* | *Sistem menampilkan pop-up berisi detail makanan surplus yang dipilih* |


<br>

**Skenario Alternatif 1: Listing yang dipilih tiba-tiba dihapus**


| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli membuka halaman listing* | *Sistem menampilkan seluruh listing* |
| 2 | *Pembeli memencet salah satu opsi pada listing makanan surplus yang sudah dihapus* | *Sistem menampilkan pesan error yang mengatakan bahwa listing tersebut sudah tidak ada* |

### 4.4.4 Skenario UC04

**Nama Use Case:** *Menyaring listing makanan surplus*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli memasukkan kata kunci yang ingin dicari ke search bar* | *Sistem hanya menampilkan listing yang mengandung kata kunci tersebut* |
| 2 | *Pembeli mengklik drop-down untuk memilih rentang harga* | *Sistem menampilkan beberapa rentang harga yang dapat dipilih* |
| 3 | *Pembeli mengklik salah satu rentang harga* | *Sistem hanya menampilkan listing dengan rentang harga yang dipilih* |

<br>

**Skenario Alternatif 1: Kata kunci yang dicari tidak ada**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli memasukkan kata kunci yang tidak ada ke search bar* | *Sistem menampilkan halaman kosong dengan pesan error yang mengatakan bahwa tidak ada makanan surplus dengan kata kunci tersebut* |

**Skenario Alternatif 2: Rentang harga yang dicari tidak ada**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli mengklik drop-down untuk memilih rentang harga* | *Sistem menampilkan beberapa rentang harga yang dapat dipilih* |
| 2 | *Pembeli mengklik salah satu rentang harga yang sedang tidak ada dalam sistem* | *Sistem menampilkan halaman kosong dengan pesan error yang mengatakan bahwa tidak ada makanan surplus dalam rentang harga tersebut* |

### 4.4.5 Skenario UC05

**Nama Use Case:** *Melakukan pembayaran*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli memilih menu checkout setelah memilih listing* | *Sistem menampilkan halaman pembayaran berisi kode QRIS dummy sebagai simulasi metode pembayaran serta tombol untuk melanjutkan simulasi* |
| 2 | *Pembeli melakukan "pembayaran" dengan mengetuk tombol untuk melanjutkan simulasi pembayaran* | *Sistem menampilkan halaman konfirmasi bahwa pembayaran telah berhasil dilakukan* | 

<br>

**Skenario Alternatif 1: Penjual membatalkan pembayaran**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli menutup atau keluar dari halaman pembayaran sebelum mengetuk tombol untuk melanjutkan simulasi pembayaran* | *Sistem membatalkan transaksi dan mengembalikan pembeli ke halaman sebelumnya* |



### 4.4.6 Skenario UC06

**Nama Use Case:** *Mengedit listing*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual membuka halaman edit pada salah satu listing miliknya* | *Sistem menampilkan form edit berisi detail listing (stok, harga, deskripsi) yang dapat diubah* |
| 2 | *Penjual mengubah isi detail listing dan menekan tombol simpan* | *Sistem menyimpan perubahan tersebut ke dalam database dan menampilkan listing dengan detail yang telah diperbarui* |

<br>

**Skenario Alternatif 1: Input tidak valid**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual mengubah stock atau harga menjadi nilai negatif atai  mengunggah foto dengan format atau ukuran selain PNG atau JPG atau lebih dari 10 MB* | *Sistem menampilkan pesan error dan tidak menyimpan perubahan yang dilakukan* |


### 4.4.7 Skenario UC07
 
**Nama Use Case:** *Login ke sistem*
 
**Skenario Normal**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pengguna membuka halaman login, memasukkan email dan password, lalu menekan tombol masuk* | *Sistem memvalidasi kredensial yang dimasukkan. Jika valid, sistem memeriksa apakah ini login pertama pengguna pada hari tersebut; jika ya, sistem memberikan poin quest login harian secara otomatis dan menyimpan progres reward pengguna* |
| 2 | *(tidak ada aksi lanjutan)* | *Sistem mengarahkan pengguna ke halaman utama sesuai perannya (Penjual atau Pembeli)* |
 
<br>

**Skenario Alternatif 1: Kredensial Tidak Valid**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pengguna memasukkan email atau password yang salah, lalu menekan tombol masuk* | *Sistem mendeteksi kredensial tidak sesuai, menampilkan pesan error "Email atau password salah", dan meminta pengguna memasukkan ulang kredensial* |
 
### 4.4.8 Skenario UC08
 
**Nama Use Case:** *Mengklaim reward login*
 
**Skenario Normal**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli membuka halaman reward/progres poin* | *Sistem menampilkan jumlah poin quest login yang telah terkumpul beserta status apakah reward sudah dapat diklaim* |
| 2 | *Pembeli menekan tombol klaim reward* | *Sistem memvalidasi bahwa poin telah mencukupi, mengurangi poin yang terpakai, memberikan reward kepada pembeli, dan menampilkan notifikasi bahwa reward berhasil diklaim* |
 
<br>

**Skenario Alternatif 1: Poin Belum Mencukupi**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pembeli membuka halaman reward saat poin yang terkumpul belum mencukupi* | *Sistem menampilkan status bahwa poin belum mencukupi untuk mengklaim reward beserta jumlah poin yang masih dibutuhkan, dan menonaktifkan tombol klaim* |

### 4.4.9 Skenario UC09
 
**Nama Use Case:** *Menghapus listing*
 
**Skenario Normal**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual memilih listing yang ingin dihapus* | *Sistem menampilkan opsi untuk menghapus pilihan listing* |
| 2 | *Penjual menekan tombol hapus* | *Sistem memberikan konfirmasi untuk menghapus* |
| 3 | *Penjual menekan tombol konfirmasi* | *Sistem menghapus listing dari database* |
 
<br>

**Skenario Alternatif 1: Penjual batal menghapus**
 
| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Penjual memilih listing yang ingin dihapus* | *Sistem menampilkan opsi untuk menghapus pilihan listing* |
| 2 | *Penjual menekan tombol hapus* | *Sistem memberikan konfirmasi untuk menghapus* |
| 3 | *Penjual menekan tombol batal* | *Sistem tidak menghapus listing dari database* |
---

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

### 5.2.1 Use Case UC01

**Nama Use Case:** *Menambahkan listing makanan surplus*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C01* | *Penjual* | *Mengisi form makanan surplus.* |
| *C02* | *ListingMakanan* | *Menyimpan data makanan.* |

#### Diagram Kelas

<p align="center">
<img  width="70%" alt="Screenshot 2026-09-23 154410" src="https://github.com/user-attachments/assets/2ef8d96a-f00c-4d9f-aaa2-cf2c930a2546" />
</p>
<p align="center">
<i>Gambar 7. Diagram Kelas Use Case UC01</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Penjual* | *idPenjual, toko* | *tambahMakanan()* |
| *C02* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *tambahListing()* |

### 5.2.2 Use Case UC02

**Nama Use Case:** *Melihat listing makanan surplus*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C01* | *Pembeli* | *Melihat listing makanan yang tersedia.* |
| *C02* | *ListingMakanan* | *Menampilkan data makanan.* |

#### Diagram Kelas

<p align="center">
<img  width="70%" alt="Screenshot 2026-09-23 153837" src="https://github.com/user-attachments/assets/55388c64-1004-49ae-bd90-a14679db1610" />
</p>
<p align="center">
<i>Gambar 8. Diagram Kelas Use Case UC02</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Pembeli* | *idPembeli, nama* | *tampilkanListingAll()* |
| *C02* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *ambilListingAll()* |

### 5.2.3 Use Case UC03

**Nama Use Case:** *Melihat detail makanan surplus*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C01* | *Pembeli* | *Melihat detail makanan yang tersedia di listing makananan tersedia.* |
| *C02* | *ListingMakanan* | *Menampilkan detail deskripsi satu makanan.* |

#### Diagram Kelas

<p align="center">
<img width="767" height="128" alt="Screenshot 2026-09-23 153837" src="https://github.com/user-attachments/assets/55388c64-1004-49ae-bd90-a14679db1610" />
</p>
<p align="center">
<i>Gambar 9. Diagram Kelas Use Case UC32</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Pembeli* | *idPembeli, nama* | *lihatDeskripsiMakanan()* |
| *C02* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *deskripsiMakanan()* |

### 5.2.4 Use Case UC04

**Nama Use Case:** *Menyaring listing makanan surplus*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C02* | *Pembeli* | *Mengirimkan batasan pencarian* |
| *C03* | *listingMakanan* | *Menyaring dan menampilkan hasil listing yang sudah disaring* |

#### Diagram Kelas

<p align="center">
<img width="442" height="62" alt="UC04 drawio" src="https://github.com/user-attachments/assets/c81885b1-4dce-48e8-a525-275a3b588436" />
</p>
<p align="center">
<i>Gambar 10. Diagram Kelas Use Case UC04</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C02* | *Pembeli* | *idPembeli, nama* | *cariListing(), saringListing()* |
| *C03* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *saringKataKunci(), saringRentangHarga()* |

### 5.2.5 Use Case UC05

**Nama Use Case:** *Melakukan pembayaran*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C02* | *Pembeli* | *Menyimpan data akun pelanggan yang membuat pesanan.* |
| *C03* | *listingMakanan* | *Mengurangi pesanan yang dipilih dari sistem* |
| *C04* | *MetodePembayaran* | *Menampilkan QRIS dummy sebagai simulasi pembayaran* |
| *C05* | *Transaksi* | *Menghitung total dan menyimpan data transaksi yang dilakukan* |

#### Diagram Kelas

<p align="center">
<img width="552" height="182" alt="UC05 drawio" src="https://github.com/user-attachments/assets/1cd6ac17-0491-497d-a2af-1fa566b64859" />
</p>
<p align="center">
<i>Gambar 11. Diagram Kelas Use Case UC05</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C02* | *Pembeli* | *idPembeli, nama* | *checkout(), bayar()* |
| *C03* | *ListingMakanan* | *idListing, stok* | *kurangiStok()* |
| *C04* | *MetodePembayaran* | *kodeQRIS* | *tampilkanQRIS()* |
| *C05* | *Transaksi* | *idTransaksi, totalHarga, tanggal, status* | *hitungTotal(), perbaruiStatus()* |

### 5.2.6 Use Case UC06

**Nama Use Case:** *Mengedit listing*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C01* | *Penjual* | *Mengakses halaman edit dan mengubah detail listing* |
| *C03* | *ListingMakanan* | *Memvalidasi input data baru dan menyimpan perubahan ke database* |

#### Diagram Kelas

<p align="center">
<img width="442" height="62" alt="UC06 drawio" src="https://github.com/user-attachments/assets/55d23821-5464-4f32-8434-744e9c5ed909" />
</p>
<p align="center">
<i>Gambar 12. Diagram Kelas Use Case UC06</learni>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Penjual* | *idPenjual, toko* | *editListing(), simpanPerubahan()* |
| *C03* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *validasiInput(), updateDatabase()* |

### 5.2.7 Use Case UC07

**Nama Use Case:** *Login ke sistem*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C01* | *Pengguna* | *Menyimpan kredensial akun dan memvalidasi proses login* |
| *C02* | *Penjual* | *Peran khusus Pengguna yang login sebagai penjual* |
| *C03* | *Pembeli* | *Peran khusus Pengguna yang login sebagai pembeli* |

#### Diagram Kelas

<p align="center">

<img alt="Class Diagram UC07" src="https://github.com/user-attachments/assets/1f3c3f81-6fb7-4aaa-abc6-f5e63a01b18f" width="70%">
</p>
<p align="center">
<i>Gambar 13. Diagram Kelas Use Case UC07</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Pengguna* | *idPengguna, email, password* | *login(), validasiKredensial()* |

### 5.2.8 Use Case UC08

**Nama Use Case:** *Mengklaim reward login*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C03* | *Pembeli* | *Melakukan klaim reward atas poin yang telah terkumpul* |
| *C07* | *RewardLogin* | *Menyimpan progres poin, memvalidasi kecukupan poin, dan memproses klaim reward* |

#### Diagram Kelas

<p align="center">
<img alt="Class Diagram UC08" src="https://github.com/user-attachments/assets/5455478d-1709-4103-ac06-36be777558bc" width="70%">
</p>
<p align="center">
<i>Gambar 14. Diagram Kelas Use Case UC08</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C03* | *Pembeli* | *idPembeli, nama* | *klaimReward()* |
| *C07* | *RewardLogin* | *idReward, poinTerkumpul, statusKlaim* | *validasiPoin(), prosesKlaim(), konfirmasiKlaim()* |

### 5.2.9 Use Case UC09

**Nama Use Case:** *Menghapus listing*

#### Identifikasi Kelas

| ID Kelas | Nama Kelas | Deskripsi Kelas |
| :--- | :--- | :--- |
| *C02* | *Penjual* | *Memilih listing miliknya dan mengonfirmasi penghapusan* |
| *C04* | *ListingMakanan* | *Direpresentasikan sebagai data listing yang dihapus dari database* |

#### Diagram Kelas

<p align="center">
<img alt="Class Diagram UC09" src="https://github.com/user-attachments/assets/aaec2ce5-cdaa-4b48-9a27-cbffe40ae2cf" width="70%">
</p>
<p align="center">
<i>Gambar 15. Diagram Kelas Use Case UC09</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C02* | *Penjual* | *idPenjual, toko* | *hapusListing()* |
| *C04* | *ListingMakanan* | *idListing, namaMakanan* | *konfirmasiHapus(), hapusDariDatabase()* |

## 5.3 Diagram Kelas Keseluruhan
Gabungkan seluruh kelas dan hubungan antarkelas dari BAB 4.3 dokumen *Class Diagram* menjadi satu diagram kelas keseluruhan. Pastikan tidak ada kelas yang terduplikasi atau tertinggal.

<p align="center">
<img width="697" height="422" alt="diagram keseluruhan drawio" src="https://github.com/user-attachments/assets/9238241f-4b42-4550-9ae0-a46835934346" />
</p>
<p align="center">
<i>Gambar 16. Diagram Kelas Keseluruhan</i>
</p>
<br>

| ID Kelas | Nama Kelas | Atribut | Metode/Operasi |
| :--- | :--- | :--- | :--- |
| *C01* | *Pengguna* | *idPengguna, email, password* | *login(), validasiKredensial()* |
| *C02* | *Penjual* | *idPenjual, toko* | *tambahMakanan(), editListing(), simpanPerubahan(), hapusListing()* |
| *C03* | *Pembeli* | *idPembeli, nama* | *tampilkanListingAll(), lihatDeskripsiMakanan(), cariListing(), saringListing(), checkout(), bayar(), klaimReward()* |
| *C04* | *ListingMakanan* | *idListing, namaMakanan, harga, stok, deskripsi, foto* | *tambahListing(), ambilListingAll(), deskripsiMakanan(), saringKataKunci(), saringRentangHarga(), kurangiStok(), validasiInput(), updateDatabase(), konfirmasiHapus(), hapusDariDatabase()* |
| *C05* | *MetodePembayaran* | *kodeQRIS* | *tampilkanQRIS()* |
| *C06* | *Transaksi* | *idTransaksi, totalHarga, tanggal, status* | *hitungTotal(), perbaruiStatus()* |
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
