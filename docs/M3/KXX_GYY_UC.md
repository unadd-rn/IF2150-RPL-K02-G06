<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 3
<br>
USE CASE & SCENARIO USE CASE
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
<br>

# BAB 1: Deskripsi Perangkat Lunak
Food Waste Stop merupakan sistem web aplikasi yang menjadi wadah transaksi makanan surplus yang menyediakan dua sisi pengguna, yaitu Penjual dan Pembeli. Menurut Penjual, sistem diharapkan menjadi solusi meminimalisir kerugian. Sistem menjadi sarana penjualan makanan surplus yang masih layak konsumsi. Dengan adanya sistem, konsumer (Pembeli) dapat memperoleh informasi serta memesan makanan surplus dengan harga lebih murah. Alur kerja sistem dimulai ketika Penjual mendaftarkan profil toko dan menambahkan makanan surplus yang tersedia beserta harga dan deskripsinya ke dalam sistem. Pembeli kemudian dapat menjelajahi daftar makanan surplus tersebut, memilih makanan yang diminati beserta jumlah kuantitasnya, lalu melakukan pemesanan. Alur ini berulang setiap kali terdapat makanan surplus baru yang perlu dipublikasikan oleh Penjual atau pesanan baru yang dibuat oleh Pembeli. Secara umum, Food Waste Stop merupakan satu kesatuan utuh yang diharapkan menghadirkan manfaat timbal balik berupa pengurangan kerugian ekonomi bagi Penjual, akses makanan terjangkau bagi Pembeli, serta kontribusi terhadap upaya pengurangan sampah makanan di masyarakat.

---

# BAB 2: Kebutuhan Fungsional (KF)
Salin ulang **seluruh Kebutuhan Fungsional (KF)** yang telah didefinisikan pada dokumen *Requirement Gathering*. Tabel ini menjadi acuan *traceability*, dimana setiap Use Case pada BAB 3 wajib ditelusuri ke satu atau lebih ID KF di tabel ini, dan sebaliknya setiap KF idealnya tercakup oleh minimal satu Use Case. Pastikan juga sudah menggunakan **format EARS** dalam penulisan KF.

| ID KF | ID Kebutuhan | Penjelasan |
| :--- | :--- | :--- |
| *KF01* | *R01* | *Selama pengguna mengisi form makanan surplus, jika pengguna menekan tombol simpan, perangkat lunak akan memvalidasi kelengkapan data (nama, stok, harga) dan kesesuaian input (format foto JPG/PNG maks. 10 MB, stok/harga non-negatif). Jika seluruh data valid, perangkat lunak menyimpan data tersebut ke dalam database, tapi jika data tidak valid, perangkat lunak menampilkan pesan error.* |
| *KF02* | *R03* | *Saat pembeli membuka website, perangkat lunak akan menampilkan daftar makanan berlebih dari berbagai penjual beserta foto, porsi, kondisi, dan harga.* |
| *KF03* | *R04* | *Ketika pengguna memasukkan ketentuan penyaringan yang diinginkan, perangkat lunak akan menyaring listing yang ada sesuai ketentuan tersebut, lalu menampilkan hasil penyaringan kepada pengguna.* |
| *KF04* | *R05* | *Saat pengguna melanjutkan ke tahap pembayaran, perangkat lunak akan menampilkan halaman pembayaran berisi kode QRIS dummy sebagai simulasi metode pembayaran.* |
| *KF05* | *R07* | *Ketika pengguna melakukan perubahan pada listing (stok, harga, deskripsi) melalui fitur edit dan menyimpannya, perangkat lunak akan menyimpan perubahan tersebut ke dalam database.* |
| *KF06* | *R10* | *Ketika pengguna melakukan login untuk pertama kalinya pada hari tersebut, perangkat lunak akan mendeteksi login harian, memberikan poin quest secara otomatis, dan menyimpan progres reward yang dimiliki pengguna.* |
| *KF07* | *R14* | *Jika terjadi kesalahan pada sistem, maka perangkat lunak akan menampilkan pesan error yang informasional kepada pengguna, contohnya "Email atau password salah" apabila kredensial yang dimasukkan tidak sesuai.* |

<sub> ***Catatan***: *Jika ada KF dari ML2 yang berubah/bertambah/dihapus setelah asistensi, pastikan tabel ini konsisten dengan versi KF terbaru sebelum dikumpulkan.*
<sub>

---

# BAB 3: Model Use Case

## 3.1 Identifikasi Aktor
Daftarkan seluruh aktor yang terlibat dalam use case yang akan dimodelkan. Aktor berupa pengguna manusia yang berinteraksi dengan solusi. Perlu diperhatikan bahwa Admin/Developer/ Pihak Eksternal lain yang bisa diotomisasi, tidak perlu dijadikan aktor.

| Aktor | Deskripsi |
| :--- | :--- |
| *Penjual* | *Pengguna yang mengelola listing makanan surplus, meliputi menambahkan, mengurangkan, mengedit, dan memantau pendapatan penjualan* |
| *Pembeli* | *Pengguna yang melihat, mencari, memilih, dan membeli listing makanan surplus* |

## 3.2 Identifikasi Use Case
Identifikasi seluruh use case yang mencakup Kebutuhan Fungsional pada BAB 2. Satu use case boleh mencakup lebih dari satu KF, dan sebaliknya satu KF boleh muncul di lebih dari satu use case bila memang relevan.

| ID UC | Nama Use Case | Deskripsi Singkat | Aktor Terlibat | ID KF Terkait |
| :--- | :--- | :--- | :--- | :--- |
| *UC01* | *Melakukan Pembayaran Digital* | *Pelanggan memilih metode pembayaran dan menyelesaikan transaksi.* | *Pelanggan* | *KF01, KF02* |
| *UC02* | *Memverifikasi Status Pembayaran* | *Kasir mengecek status transaksi pelanggan sebelum menyerahkan barang.* | *Kasir* | *KF03* |
| *...* | *...* | *...* | *...* | *...* |

## 3.3 Use Case Diagram
Buatlah **satu** use case diagram yang mencakup seluruh aktor dan use case. Sertakan relasi *include*/*extend* apabila ada use case yang saling bergantung.
<br>
<p align="center">
<img alt="Contoh Activity Diagram" src="./assets/diagram/contoh-uc-diagram.webp" width="70%">
</p>
<p align="center">
<i>Gambar 1. Contoh Use Case Diagram</i>
</p>
<br>

Hal-hal yang perlu diperhatikan dalam pembuatan use case diagram:
- Pastikan notasi UML use case (aktor, oval use case, garis asosiasi, *include/extend*) digambar dengan benar.
- Seluruh aktor dan use case yang telah didefinisikan harus muncul di diagram, tidak ada yang terlewat maupun berlebih.
- Hindari garis yang saling bersilangan tanpa alasan jelas, susun diagram agar mudah dibaca.
- Hindari istilah solusi teknis (misalnya nama tabel database, nama endpoint API) muncul di dalam diagram use case karena use case menjelaskan *interaksi fungsional*, bukan detail implementasi.

## 3.4 Skenario Use Case
Buat skenario untuk **setiap** use case yang telah diidentifikasi pada 3.2. Setiap skenario dapat terdiri dari dua jenis alur:
- **Skenario Normal**: alur utama (*happy path*) di mana interaksi aktor-sistem berjalan lancar tanpa kendala hingga tujuan use case tercapai.
- **Skenario Alternatif**: alur percabangan dari skenario normal, misalnya kondisi gagal, input tidak valid, atau pilihan lain yang tersedia bagi aktor. Boleh ada lebih dari satu skenario alternatif per use case jika ada beberapa titik percabangan berbeda.

Format tabel skenario: kolom **Aksi Aktor** berisi apa yang dilakukan/diinput aktor, kolom **Reaksi Perangkat Lunak** berisi respons sistem terhadap aksi tersebut secara **berurutan** (nomor langkah harus berpasangan/selaras antar dua kolom).


### 3.4.1 Skenario UC01

**Nama Use Case:** *Melakukan Pembayaran Digital*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pelanggan memilih menu checkout* | *Sistem menampilkan ringkasan pesanan dan pilihan metode pembayaran* |
| 2 | *Pelanggan memilih metode pembayaran (misal: e-wallet)* | *Sistem mengarahkan pelanggan ke halaman konfirmasi e-wallet* |
| 3 | *Pelanggan mengonfirmasi pembayaran* | *Sistem menerima respons pembayaran berhasil, memperbarui status pesanan menjadi "Lunas", dan menampilkan notifikasi pembayaran berhasil* |


<br>

**Skenario Alternatif 1: Otorisasi Pembayaran Gagal**


| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Pelanggan memilih menu checkout* | *Sistem menampilkan ringkasan pesanan dan pilihan metode pembayaran* |
| 2 | *Pelanggan memilih metode pembayaran (misal: e-wallet)* | *Sistem mengarahkan pelanggan ke halaman konfirmasi e-wallet* |
| 3 | *Pelanggan mengonfirmasi pembayaran* | *Sistem menerima respons pembayaran gagal (misal: saldo tidak cukup). Sistem menampilkan pesan error dan meminta pelanggan memilih metode pembayaran lain* |
| 4 | *Pelanggan memilih metode pembayaran lain* | *Sistem kembali ke langkah 2 skenario normal* |

### 3.4.2 Skenario UC02

**Nama Use Case:** *Memverifikasi Status Pembayaran*

**Skenario Normal**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Kasir memasukkan ID Pesanan pelanggan* | *Sistem menampilkan status pembayaran ("Lunas") beserta detail transaksi* |

<br>

**Skenario Alternatif 1: ID Pesanan Tidak Ditemukan**

| No | Aksi Aktor | Reaksi Perangkat Lunak |
| :--- | :--- | :--- |
| 1 | *Kasir memasukkan ID Pesanan yang salah/tidak ada* | *Sistem menampilkan pesan "ID Pesanan tidak ditemukan" dan meminta kasir memasukkan ulang* |


<sub>*Lanjutkanlah pola 3.4.x ini untuk setiap ID UC yang telah diidentifikasi pada 3.2, sampai seluruh use case memiliki skenario normal dan skenario alternatif (tidak usah dibuat jika use case tersebut memang tidak memiliki skenario alternatif).*<sub>
