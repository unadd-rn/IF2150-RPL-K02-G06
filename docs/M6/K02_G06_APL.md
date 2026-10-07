<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 6
<br>
ARSITEKTUR PERANGKAT LUNAK (APL)
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

<br>

# BAB 1: Style/Pattern Arsitektur Acuan

### 1.1 Style/Pattern yang Dipilih dan Peran Komponen
Style yang digunakan yaitu client-server, yang menentukan bagaimana sistem dijalankan, yaitu dengan client meminta layanan dari server yang kemudian memproses pelayanan. Kemudian, pattern yang digunakan adalah MVC yang mengatur isi di dalamnya, yaitu View darri sisi client, sedangkan Controller dan Model di sisi server.

Peran komponen yang pertama View dari sisi client yang menampilkan data kepada pengguna dan menerima aksi pengguna. Kemudian ada Controller dari sisi server yang menerima permintaan dari View dan mengakses data di Model agar dapat diproses dan dikembalikan hasilnya ke View. Lalu, ada Model yang berisi aturan cara kerja dan data untuk diproses. Kemudian ada tambahan Database untuk menyimpan seluruh data yang ada.

<p align="center">
  <img width="522" height="482" alt="Untitled Diagram drawio (1)" src="https://github.com/user-attachments/assets/c05b7e88-bbfc-4aca-8004-37839e45328c" />
  <br>
  <i>Gambar 1. Arsitektur MVC</i>
</p>

### 1.2 Alasan Pemilihan
Alasan pemilihan style/pattern tersebut yaitu:
1. Memastikan alur pengguna yang berbeda sesuai peran (pembeli atau penjual) terpisah tampilannya (view) tapi dapat menggunakan logika yang sama (controller dan model)
2. Pengguna yang menggunakan perangkat terpisah tapi data harus sama, maka perlu server untuk mengaturnya (client-server)
3. Penggunaan server lebih aman terutama untuk KNF yang mewajibkan enkripsi password dan disesuaikan juga dengan KF yang memerlukan logika terpusat di server

### 1.3 Lingkungan Operasi

Tabel 1.1. Lingkungan Operasi Perangkat Lunak
| Komponen | Spesifikasi |
| :--- | :--- |
| *Server* | *Server lokal* |
| *Client* | *Web browser modern (Chrome, Firefox, Edge, Safari versi terbaru) di desktop maupun mobile* |
| *Front-End* | *Next.js (React), Node.js v20 untuk proses build* |
| *Back-End* | *Fast API* |
| *DBMS* | *PostgreSQL 15* |
| *OS* | *Windows/Linux/macOS/Android/iOS melalui browser* |

Next.js menjalankan View di sisi client. FastAPI menjalankan Controller dan Model di sisi server. PostgreSQL menjadi bagian database yang diakses oleh Model. Kemudian. frontend dan backend saling berkomunikasi dengan logika terpisah sesuai dengan style client-server.

---

# BAB 2: Identifikasi Komponen / Modul / Subsistem

Tabel 2.1. Identifikasi Komponen/Modul/Subsistem

| Nama Komponen/Modul/Subsistem | Jenis                 | Penjelasan |
| :---------------------------- | :-------------------- | :--------- |
| *LoginView*              | *View*          | *Menampilkan form login untuk Penjual dan Pembeli, mengenkripsi password dengan SHA-256 sebelum dikirim (KNF02), meneruskan kredensial ke AuthController, lalu mengarahkan pengguna ke halaman sesuai perannya.* |
| *KatalogView*              | *View*          | *Menampilkan daftar listing, detail satu listing, serta kolom pencarian dan penyaringan harga kepada Pembeli, dan meneruskan aksinya ke KatalogController.* |
| *ListingView*              | *View*          | *Menampilkan form tambah dan edit listing serta tombol hapus listing kepada Penjual, dan meneruskan aksinya ke ListingController.* |
| *PembayaranView*              | *View*          | *Menampilkan ringkasan pesanan dan kode QRIS dummy kepada Pembeli, serta menerima aksi bayar atau batal untuk diteruskan ke PembayaranController.* |
| *RewardView*              | *View*          | *Menampilkan progres poin login dan tombol klaim reward kepada Pembeli, lalu meneruskan aksi klaim ke RewardController.* |
| *AuthController*              | *Controller*          | *Memproses permintaan login Penjual dan Pembeli (UC07): meneruskan kredensial ke Validasi, mencocokkan password terenkripsi SHA-256 dengan data Pengguna, lalu memerintahkan RewardLogin menambah poin jika ini login pertama pengguna pada hari tersebut. Hasilnya dikembalikan ke View sesuai peran pengguna.* |
| *KatalogController*           | *Controller*          | *Memproses permintaan Pembeli untuk melihat listing (UC02), melihat detail satu listing (UC03), serta mencari dengan kata kunci dan menyaring berdasarkan rentang harga (UC04). Listing yang stoknya habis atau sudah kedaluwarsa tidak dikirim ke View.* |
| *ListingController*           | *Controller*          | *Memproses permintaan Penjual untuk menambahkan (UC01), mengedit (UC06), dan menghapus (UC09) listing makanan surplus. Input diteruskan ke Validasi sebelum ListingMakanan disimpan, diubah, atau dihapus dari database.* |
| *PembayaranController*        | *Controller*          | *Memproses checkout dan pembayaran Pembeli (UC05): membuat Transaksi, menghitung total harga, meminta kode QRIS dummy melalui PaymentGatewayAdapter, lalu memperbarui status Transaksi dan mengurangi stok ListingMakanan setelah pembayaran dikonfirmasi. Jika pembeli keluar sebelum membayar, transaksi dibatalkan. Seluruh proses dijalankan dalam satu transaksi database agar memenuhi prinsip ACID (KNF01).* |
| *RewardController*            | *Controller*          | *Memproses permintaan Pembeli untuk melihat progres poin dan mengklaim reward login (UC08). RewardController memeriksa kecukupan poin melalui RewardLogin, mengurangi poin yang terpakai, dan mengembalikan status klaim ke View.* |
| *Pengguna*              | *Model*          | *Merepresentasikan data akun Penjual dan Pembeli (email, password terenkripsi SHA-256, dan peran) serta metode untuk mengakses dan mengubahnya.* |
| *ListingMakanan*              | *Model*          | *Merepresentasikan data listing makanan surplus (nama, foto, harga, stok, dan batas kedaluwarsa) milik Penjual serta metode untuk mengakses dan mengubahnya.* |
| *Transaksi*              | *Model*          | *Merepresentasikan data transaksi pembelian Pembeli (listing yang dibeli, total harga, dan status pembayaran) serta metode untuk mengakses dan mengubahnya.* |
| *RewardLogin*              | *Model*          | *Merepresentasikan poin login Pembeli, tanggal login terakhir, dan status klaim reward serta metode untuk menambah dan mengurangi poin.* |
| *Validasi*                    | *Pendukung*           | *Memvalidasi input sebelum diproses controller. Untuk listing (dipakai ListingController), dicek kelengkapan field wajib (nama, foto, harga), stok dan harga tidak bernilai negatif, serta foto berformat PNG/JPG dengan ukuran maksimal 10 MB. Untuk login (dipakai AuthController), dicek format email dan password yang tidak kosong. Jika input tidak valid, pesan error dikembalikan ke controller.* |
| *PaymentGatewayAdapter*       | *Integrasi Eksternal* | *Mengirim permintaan pembayaran dari PembayaranController ke Payment Gateway QRIS dummy, menerima kode QRIS untuk ditampilkan, lalu meneruskan status konfirmasi pembayaran (berhasil atau batal) kembali ke PembayaranController.* |
| *Database*              | *Penyimpanan Data*          | *Menyimpan seluruh data Model secara persisten pada PostgreSQL 15 dan menjalankan transaksi database yang memenuhi prinsip ACID.* |

---

# BAB 3: Model Arsitektur Perangkat Lunak

## 3.1 Logical View

Aplikasi dibuat dengan arsitektur client-server karena arsitektur ini sangat cocok untuk aplikasi e-commerce yang sifatnya memisahkan tugas antara aplikasi di HP pengguna (client) dan sistem pusat data yang mengelola semua proses bisnis (server).

<p align="center">
<img width="1052" height="662" alt="Untitled Diagram drawio (2)" src="https://github.com/user-attachments/assets/e115d579-4f88-49de-913b-5d40c2c35a95" />
</p>
<p align="center">
<i>Gambar 2. Logical View</i>
</p>

# Referensi

- Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson. Chapter 6: *Architectural Design*: [https://software-engineering-book.com/slides/](https://software-engineering-book.com/slides/)
- Diagram arsitektur: [https://www.drawio.com/](https://www.drawio.com/), [https://staruml.io/](https://staruml.io/)
