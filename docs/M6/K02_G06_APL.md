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
| *AuthController*              | *Controller*          | *Memproses permintaan login Penjual dan Pembeli (UC07): meneruskan kredensial ke Validasi, mencocokkan password terenkripsi SHA-256 dengan data Pengguna, lalu memerintahkan RewardLogin menambah poin jika ini login pertama pengguna pada hari tersebut. Hasilnya dikembalikan ke View sesuai peran pengguna.* |
| *KatalogController*           | *Controller*          | *Memproses permintaan Pembeli untuk melihat listing (UC02), melihat detail satu listing (UC03), serta mencari dengan kata kunci dan menyaring berdasarkan rentang harga (UC04). Listing yang stoknya habis atau sudah kedaluwarsa tidak dikirim ke View.* |
| *ListingController*           | *Controller*          | *Memproses permintaan Penjual untuk menambahkan (UC01), mengedit (UC06), dan menghapus (UC09) listing makanan surplus. Input diteruskan ke Validasi sebelum ListingMakanan disimpan, diubah, atau dihapus dari database.* |
| *PembayaranController*        | *Controller*          | *Memproses checkout dan pembayaran Pembeli (UC05): membuat Transaksi, menghitung total harga, meminta kode QRIS dummy melalui PaymentGatewayAdapter, lalu memperbarui status Transaksi dan mengurangi stok ListingMakanan setelah pembayaran dikonfirmasi. Jika pembeli keluar sebelum membayar, transaksi dibatalkan. Seluruh proses dijalankan dalam satu transaksi database agar memenuhi prinsip ACID (KNF01).* |
| *RewardController*            | *Controller*          | *Memproses permintaan Pembeli untuk melihat progres poin dan mengklaim reward login (UC08). RewardController memeriksa kecukupan poin melalui RewardLogin, mengurangi poin yang terpakai, dan mengembalikan status klaim ke View.* |
| *Validasi*                    | *Pendukung*           | *Memvalidasi input sebelum diproses controller. Untuk listing (dipakai ListingController), dicek kelengkapan field wajib (nama, foto, harga), stok dan harga tidak bernilai negatif, serta foto berformat PNG/JPG dengan ukuran maksimal 10 MB. Untuk login (dipakai AuthController), dicek format email dan password yang tidak kosong. Jika input tidak valid, pesan error dikembalikan ke controller.* |
| *PaymentGatewayAdapter*       | *Integrasi Eksternal* | *Mengirim permintaan pembayaran dari PembayaranController ke Payment Gateway QRIS dummy, menerima kode QRIS untuk ditampilkan, lalu meneruskan status konfirmasi pembayaran (berhasil atau batal) kembali ke PembayaranController.* |

# BAB 3: Model Arsitektur Perangkat Lunak

*Architectural View* adalah bagaimana cara kita melihat/mendeskripsikan arsitektur sebuah sistem dari sudut pandang tertentu. Dalam perancangan arsitektur aplikasi, dibutuhkan *Architectural View* yang dapat mempermudah pemahaman dari proses aplikasi yang akan dikembangkan. Tujuan dari *Architectural View* adalah menjadi bahan komunikasi, pemisahan masalah, mempermudah analisis, dan pemandu saat eksekusi pengembangan sistem tersebut.

Buatlah model arsitektur dari aplikasi yang akan dirancang dalam bentuk *view*. Model arsitektur ini berfungsi untuk memperlihatkan bagaimana setiap komponen, modul, dan subsistem saling berinteraksi serta berkolaborasi dalam menjalankan fungsi utama sistem secara keseluruhan. Anda dapat membuat satu atau lebih *view* tergantung kebutuhan dalam bentuk gambar. Pilihlah notasi yang sesuai. Contoh *view* yang dapat digunakan antara lain ***Logical View***, ***Process View***, ***Development View***, serta ***Physical View***.

Ketentuan pengisian BAB 3:
1. Setiap view menggambarkan **keseluruhan sistem**, bukan satu use case atau satu fitur saja.
2. Buat **minimal satu view**. Setiap view dituliskan dalam subbab tersendiri (3.1, 3.2, dan seterusnya). Tidak perlu membuat keempat view, pilih yang paling membantu menjelaskan P/L Anda, lalu jelaskan alasan pemilihannya.
3. Setiap view harus **konsisten dengan BAB 2**. Seluruh komponen pada Tabel 2.1 harus muncul dengan nama yang sama, dan tidak boleh ada komponen pada view yang tidak terdaftar di Tabel 2.1.
4. Setiap view harus **mencerminkan style/pattern pada BAB 1**. Misalnya, jika memilih MVC, pembagian *Model*, *View*, dan *Controller* harus terlihat jelas pada diagram.
5. Jika membuat lebih dari satu view, setiap view harus menggambarkan sistem yang sama dari sudut pandang berbeda. View tambahan melengkapi view pertama, bukan mengulanginya.
6. Beri label pada setiap garis atau panah yang menghubungkan komponen agar hubungan antarkomponen dapat dipahami tanpa penjelasan tambahan.
7. Jika membuat *Physical View*, gambarkan lingkungan operasi pada Tabel 1.1.

## 3.1 XXX View

Tuliskan secara singkat mengenai model arsitektur perangkat lunak yang Anda pilih dan sertakan alasan mengapa model arsitektur tersebut cocok untuk aplikasi Anda.

<p align="center">
<img alt="Contoh Logical View pada P/L E-Commerce" src="./assets/diagram/contoh-logical-view.webp" width="100%">
</p>
<p align="center">
<i>Gambar 2. Contoh Logical View pada P/L E-Commerce</i>
</p>

Gambar 2 adalah contoh *Logical View* dalam bentuk *block diagram*. Seluruh komponen pada Tabel 2.1 digambarkan dan dikelompokkan sesuai pola MVC (*View*, *Controller*, *Model*), ditambah komponen pendukung dan basis data. Sistem di luar P/L, seperti *Payment Gateway (dummy)*, digambarkan dengan garis putus-putus dan tidak perlu dimasukkan ke Tabel 2.1. Setiap garis diberi label: "Memanggil" untuk *View* yang memanggil *Controller*, "akses" untuk *Controller* yang mengakses *Model*, serta agregasi dan komposisi untuk hubungan antar-*Model*.

<sub><b><i>Catatan</i></b>: <i>Ganti XXX dengan nama view yang dibuat, misalnya Logical View. Gambar 2 hanya contoh untuk P/L e-commerce, ganti dengan view milik kelompok Anda yang memuat seluruh komponen pada Tabel 2.1. Jenis view dan notasinya boleh berbeda dari contoh. Jika membuat view tambahan, lanjutkan pola 3.x ini (3.2, 3.3, dan seterusnya).</i></sub>

---

# Referensi

- Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson. Chapter 6: *Architectural Design*: [https://software-engineering-book.com/slides/](https://software-engineering-book.com/slides/)
- Diagram arsitektur: [https://www.drawio.com/](https://www.drawio.com/), [https://staruml.io/](https://staruml.io/)
