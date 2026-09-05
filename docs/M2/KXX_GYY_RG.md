<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 2
<br>
REQUIREMENT GATHERING
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
| *B* | |
| *C* | |
| ... | |

<br>
<br>

# BAB 1: Deskripsi Umum

## 1.1 Deskripsi Umum Sistem

Abstraksikan sistem solusi menurut sudut pandang pengguna yang telah ditentukan. Jelaskan secara ringkas mengenai apa saja ekspektasi pengguna terhadap sistem yang akan dikembangkan, alur kerja sistem yang diinginkan, serta harapan dari penerapan solusi dalam bentuk narasi.

> *Sistem adalah kesatuan utuh antara perangkat lunak, pengguna, perangkat keras, dan proses bisnis (urutan langkah logis yang dilakukan di dunia nyata untuk menyelesaikan suatu pekerjaan atau mencapai tujuan tertentu).*

## 1.2 Deskripsi Pengguna Perangkat Lunak

| Aktor | Deskripsi |
| :--- | :--- |
| *Pembeli* | *Pengguna ini bertindak sebagai pembeli yang mencari makanan sisa toko yang sudah tidak memenuhi standar jual normal namun masih layak dikonsumsi, dengan keuntungan, harga yang lebih murah. Karakteristik pengguna ini mengutamakan kemudahan melihat pilihan makanan yang tersedia lengkap dengan deskripsi, harga, dan informasi toko, serta kemudahan dalam melakukan pemesanan dan pembayaran. Pembeli memiliki quest log in harian dan bisa mendapatkan diskon apabila sudah mencapai jumlah memenuhi* |
| *Penjual* | *Pengguna ini bertindak sebagai pihak toko yang pada jam tutup (atau mendekati) memiliki makanan tidak terjual dan tidak dapat dijual kembali esok/kemudian hari karena tidak memenuhi standar jual toko, namun makanan tersebut masih layak dikonsumsi. Dengan menjual makanan tersebut dengan harga diskon, toko dapat mengurangi kerugian. Karakteristik pengguna ini mengutamakan kemudahan dalam mengelola profil toko serta memasukkan, memperbarui, dan menghapus informasi makanan yang dijual.* |
---

# BAB 2: Deskripsi Kebutuhan Perangkat Lunak

## 2.1 Kebutuhan Pengguna Awal

Definisikan apa yang ingin dicapai oleh pengguna saat menggunakan sistem ini dalam format *User Story* (Sebagai [Aktor], saya ingin [Aktivitas/Kebutuhan], sehingga [Tujuan/Nilai]). Pastikan kalian berfokus pada "apa yang ingin dilakukan pengguna".

| ID | Aktor | Kebutuhan / Aktivitas | Tujuan / Nilai |
| :--- | :--- | :--- | :--- |
| US-01 | *Pembeli* | *Mendaftar dan mengisi profil akun (nama, nomor kontak, dan alamat)* | *Sistem memiliki informasi yang dibutuhkan untuk proses pengiriman makanan* |
| US-02 | *Pembeli* | *Melihat daftar makanan yang dijual beserta deskripsinya (nama dan bahan utama, nama dan alamat toko, jam buka toko, kuantitas tersedia, tanggal dijual, dan estimasi tanggal kadaluarsa)* | *Informasi makanan mudah dibaca dan dipahami* |
| US-03 | *Pembeli* | *Memilih makanan beserta kuantitas dan melakukan pemesanan dengan pembayaran QRIS* | *Makanan yang dipesan dapat dikirim ke alamat sesuai profil akun* |
| US-04 | *Pembeli* | *Mendapat reward dari log-in harian* | *Promo tambahan dari quest log in harian di website. Tujuan gamifikasi seru dan mudah dilakukan meskipun harian* |
| US-05 | *Penjual* | *Memasukkan profil toko (nama dan alamat toko, nomor telepon toko, dan deskripsi spesialisasi makanan seperti lauk, roti, atau camilan)* | *Toko dapat dikenali pembeli dan penjual bisa memantau total pendapatan dari makanan terjual* |
| US-06 | *Penjual* | *Menambahkan makanan yang dijual beserta deskripsinya (nama dan bahan utama, jam ketersediaan, kuantitas, tanggal dijual, tanggal kadaluarsa, dan keterangan tambahan opsional)* | *Kemudahan mempublikasikan informasi makanan* |
| US-07 | *Penjual* | *Mengedit deskripsi makanan yang sudah diunggah* | *Kemudahan memperbarui informasi makanan apabila terjadi perubahan* |
| US-08 | *Penjual* | *Menerima notifikasi saat makanan dibeli dan dibayar, dengan saldo bertambah otomatis serta kuantitas makanan berkurang (stok habis jika mencapai nol)* | *Transaksi dan pengelolaan stok berjalan otomatis tanpa perlu diproses manual* |

## 2.2 Deskripsi Aktivitas

Buatlah daftar seluruh aktivitas yang terdapat dalam sistem solusi, lengkap dengan ID dan penjelasan. Telusuri hubungan aktivitas tersebut dengan *user story* yang sudah dituliskan sebelumnya. Bisa dibuat dalam bentuk tabel.

kriteria seperti kantin, rentang harga, atau kategori makanan. | US-02 |
| B03 | Melihat detail informasi makanan | Pembeli membuka satu listing untuk melihat foto, berat/porsi, kondisi, dan harga diskon secara rinci. | US-02 |
| B04 | Memeriksa ketersediaan stok | Pembeli memastikan stok listing yang diminati masih tersedia sebelum melanjutkan ke proses berikutnya. | US-02 |
| B05 | Memilih makanan untuk dibeli | Pembeli menandai listing yang diminati dan melanjutkan ke proses pemesanan. | US-03 |
| B06 | Mengonfirmasi pesanan dan harga | Sistem menampilkan ringkasan pesanan beserta harga diskon untuk dikonfirmasi pembeli sebelum pembayaran. | US-03 |
| B07 | Melakukan pembayaran | Pembeli menyelesaikan pembayaran sesuai harga diskon yang telah dikonfirmasi. | US-03 |
| B08 | Mengambil makanan di kantin | Pembeli menunjukkan bukti pemesanan dan mengambil makanan langsung di kantin, sesuai batasan sistem yang tidak menyediakan layanan pengantaran. | US-03 |


## 2.3 Pemetaan Kebutuhan

Perhatikan kembali semua aktivitas yang telah didefinisikan pada tabel deskripsi aktivitas atau *activity diagram*. Jabarkan kebutuhan sistem yang akan dibuat dengan mengacu pada aktivitas-aktivitas tersebut. Setiap aktivitas (ID Aktivitas) dapat memiliki satu atau lebih kebutuhan yang berbeda. Pastikan untuk mengidentifikasi dan mengisi semua jenis kebutuhan yang relevan untuk setiap aktivitas, yaitu:

- **User Requirement**, yaitu kebutuhan dari sudut pandang pengguna (apa yang dapat dilakukan pengguna).
- **Business Requirement**, yaitu aturan, kebijakan, atau standar bisnis yang harus dipenuhi oleh sistem.
- **System Requirement**, yaitu kebutuhan yang menjelaskan apa yang harus dilakukan sistem dan bagaimana sistem harus bekerja dari segi performa, keamanan, keandalan, dsb.

Lengkapi juga dengan penjelasannya dan apakah keperluan tersebut perlu didukung oleh perangkat lunak atau tidak. Jenis kebutuhan tidak terbatas hanya dari tiga jenis di atas, dapat ditambahkan yang lain juga bila diperlukan, misalnya kebutuhan regulasi (*Legal*).

| ID Kebutuhan | ID Aktivitas | Jenis Kebutuhan | Deskripsi Kebutuhan | P/L |
| :--- | :--- | :--- | :--- | :--- |
| *R01* | *PL01, BL01* | *System* | *Sistem dapat diakses baik di desktop maupun mobile tanpa mengunduh aplikasi tambahan* | *Ya* |
| *R02* | *PL03, BL03* | *System* | *Sistem dapat memverifikasi kredensial yang dimasukkan pengguna dan memberi pesan error saat kredensial tidak sesuai* | *Ya* |
| *R03* | *B07* | *System* | *Sistem harus mengintegrasikan API Payment Gateway dengan prinsip ACID (Atomicity, Consistency, Isolation, Durability), jika terjadi kegagalan jaringan saat saldo terpotong, sistem harus secara otomatis membatalkan transaksi atau meneruskan dana (reliable).* | *Ya* |
| *R04* | *PL04, BL04* | *System* | *Kata sandi (password) atau PIN pengguna saat otorisasi pembayaran harus di-hash dan tidak disimpan dalam bentuk plain-text.* | *Ya* |
| *R05* | *PL05, BL05* | *System* | *Sistem menyimpan status login pengguna agar tidak perlu login berulang tiap halaman* | *Ya* |
| *R06* | *A03* | *System* | *Sistem harus membatasi ukuran maksimal foto sampai 10 MB dan jenis file yang dikirimkan hanya berupa JPG/PNG* | *Ya* |
| *R07* | *A06* | *System* | *Sistem menyimpan listing ke database dan mengupdate listing secara real-time di halaman pengguna* | *Ya* |
| *R08* | *B02* | *System* | *Sistem mengimplementasikan fitur filtering yang memungkinkan pengguna mencari barang dengan kata kunci tertentu* | *Ya* |
| *R09* | *A09, B04* | *System* | *Sistem mengecek ketersediaan stok sebelum memproses pesanan, dan menampilkan pesan error jika stok tiba-tiba habis* | *Ya* |
| *R10* | *A09, A10, B04* | *System* | *Sistem dapat menghapus barang apabila stoknya sudah mencapai 0* | *Ya* |
| *R11* | *B05, B06* | *System* | *Sistem dapat mengkalkulasikan total harga barang yang dibeli* | *Ya* |
| *R12* | *B06* | *System* | *Sistem menampilkan halaman pembayaran (menampilkan QRIS dunmy) beserta tombol "Simulasikan Pembayaran Berhasil"* | *Ya* |
| *R13* | *A09, B07* | *System* | *Setelah pembayaran berhasil, sistem otomatis mengurangi jumlah stok makanan di database sesuai jumlah yang dibeli* | *Ya* |
| *R14* | *B08* | *System* | *Sistem memberikan kode unik pembayaran sebagai bukti pembelian* | *Ya* |
| *R15* | *BL04, PL04* | *Legal* | *Registrasi menggunakan data pribadi sehingga harus mematuhi UU Perlindungan Data yang berlaku* | *Ya* |

## 2.4 Kebutuhan Fungsional (KF)

Untuk setiap kebutuhan yang telah diidentifikasi sebagai "didukung oleh perangkat lunak", buatlah daftar kebutuhan fungsional P/L, lengkap dengan ID Kebutuhan Fungsional (KF) dan penjelasannya. Hubungkan ID Kebutuhan Fungsional dengan ID Pemetaan Kebutuhan dari sistem.

| ID KF | ID Kebutuhan | Penjelasan |
| :--- | :--- | :--- |
| *KF01* | *R01* | *Perangkat lunak dapat menampilkan pilihan antarmuka metode pembayaran (transfer bank, e-wallet, kartu kredit) setelah pengguna melakukan checkout.* |
| *KF02* | *R01* | *Perangkat lunak dapat mengirimkan permintaan otorisasi transaksi ke API Payment Gateway beserta nominal tagihan dan ID Pesanan.* |
| ... | ... | ... |

## 2.5 Kebutuhan Non-Fungsional (KNF)

Uraikan dengan ringkas Kebutuhan Non-Fungsional dalam tabel sebagai berikut. Isilah kolom kebutuhan dengan kalimat yang jelas, spesifik, dan terukur (kelak dapat diuji untuk dipenuhi). Kolom ID KNF adalah nomor Kebutuhan Non-Fungsional yang harus ditelusuri pada saat pengujian. Hubungkan ID Kebutuhan Non-Fungsional dengan ID Pemetaan Kebutuhan Umum dari sistem.

| ID KNF | ID Kebutuhan | Parameter | Deskripsi Kebutuhan |
| :--- | :--- | :--- | :--- |
| *KNF01* | *R03* | *Reliability* | *Proses transaksi pembayaran harus memenuhi prinsip ACID untuk mencegah terjadinya data tersangkut (lost update) apabila terjadi kegagalan jaringan di tengah proses.* |
| *KNF02* | *R04* | *Security* | *Sistem harus mengenkripsi PIN atau password pengguna menggunakan algoritma SHA-256 sebelum data dikirimkan ke server, serta tidak menyimpannya dalam bentuk plain-text di database.* |
| ... | ... | ... | ... |

Silakan pilih yang relevan. Tidak perlu semua parameter menjadi kebutuhan non-fungsional. Berikut merupakan penjelasan dari setiap parameter. **Parameter dari Kebutuhan Non-Fungsional tidak terbatas hanya di bawah ini** karena hanya merupakan panduan sehingga dapat ditambah KNF yang lain, misalnya *constraint* dari sistem.

| Parameter | Penjelasan |
| :--- | :--- |
| *Availability* | Ketersediaan aplikasi, misalnya harus terus-menerus beroperasi 7 hari per minggu, 24 jam per hari tanpa gagal. |
| *Reliability* | Keandalan, misalnya tidak pernah boleh gagal (atau kegagalan yang ditolerir adalah …%) sehingga harus dipikirkan *fault tolerant architecture*. Biasanya hanya perlu untuk *critical application* yang jika gagal akan berakibat fatal. |
| *Ergonomy* | Kenyamanan pakai bagi pengguna. |
| *Portability* | Kemudahan untuk dibawa dan dioperasikan ke mesin/sistem operasi/*platform* yang lain. |
| *Memory* | Jika perhitungan kapasitas memori internal kritis (misalnya untuk P/L yang harus dijadikan *chips* dan ukurannya harus kecil). |
| *Response time* | Batasan waktu yang harus dipenuhi. Sangat penting untuk aplikasi *real time*. Contoh: "Aplikasi harus mampu menampilkan hasil dalam 4 detik", atau "ATM harus menarik kembali kartu yang tidak diambil dalam waktu 3 menit". |
| *Safety* | Yang menyangkut keselamatan manusia, misalnya untuk P/L yang dipakai pada sistem kontrol di pabrik. |
| *Security* | Aspek keamanan yang harus dipenuhi. |

<br>

# Referensi
- Diagram UML: https://www.drawio.com/, https://staruml.io/
