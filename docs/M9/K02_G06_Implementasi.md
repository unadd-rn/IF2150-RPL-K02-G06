<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 9
<br>
IMPLEMENTASI PERANGKAT LUNAK
</h1>
<br>

## *SaveBite*
<img width="40%" alt="logo" src=".\assets\save_bite.PNG" />

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

**Deadline:** Rabu, 11 November 2026, 21.50 WIB
**Asistensi akbar:** Senin, 2 November 2026, 19.00 WIB, https://teams.microsoft.com/l/message/19:BGAB6hurIuLXWy3ZVN_CgpiGR7eTfgHyMzlVJhu-dzo1@thread.tacv2/1793620051162?tenantId=db6e1183-4c65-405c-82ce-7cd53fa6e9dc&groupId=5cce5463-c3b7-4b81-9f9c-e6de1abd54c0&parentMessageId=1793620051162&teamName=2026%20IF2150%20RPL&channelName=General&createdTime=1793620051162

---

# BAGIAN B: Laporan Implementasi

## B.1 Perubahan dari DPPL

Tabel B.1. Perubahan dari DPPL

| No | Bagian DPPL | Rancangan Awal | Implementasi Akhir | Alasan |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Tabel 2.1 Lingkungan Implementasi | DBMS PostgreSQL 15, Python 3.11, Node.js v20 | SQLite (modul `sqlite3` bawaan Python, satu file `src/savebite.db` yang dibuat otomatis oleh `init_db()`), Python 3.12, Node.js 22, Next.js 16.4.4, React 19.3.0 | Basis data dapat dijalankan lokal tanpa instalasi server sesuai ketentuan A.2. Akibatnya `SELECT ... FOR UPDATE` diganti `BEGIN IMMEDIATE`, `NOW()` diganti parameter waktu dengan `datetime()`, dan `RETURNING` diganti `lastrowid` |
| 2 | Kelas C01 Pengguna, C02 Penjual, C03 Pembeli | Hierarki kelas dengan operasi `verifikasiPassword()`, `getPeran()`, `bukaListing()`, dan `memilikiListing()` yang dipanggil AuthController dan ListingController | Ketiga kelas tetap ada di `models.py`, tetapi tidak dibuat objeknya saat aplikasi berjalan. Verifikasi password dilakukan dengan `bcrypt.checkpw` di `routers/auth.py`, peran ditentukan query Q-C15-01 (`LEFT JOIN pembeli`), kepemilikan listing diperiksa dengan `WHERE id_penjual = ?`, dan `bukaListing()` menjadi `GET /api/listing/penjual` | Data pengguna diakses dengan SQL langsung tanpa ORM, sehingga aturan yang sama lebih sederhana ditulis pada query |
| 3 | Kelas C04 ListingMakanan | Operasi `ubahData()`, `kurangiStok()`, `nonaktifkan()`. Tidak ada atribut draf | Ketiga operasi diwujudkan sebagai `UPDATE` langsung: Q-C04-04 di `ubah_listing`, Q-C04-05 di `hapus_listing`, dan pengurangan stok bersyarat (`stok >= :jumlah` dan masih tersedia) di `konfirmasi_bayar`. Ditambah atribut `draft: Boolean`, yang ikut menjadi syarat `KONDISI_TERSEDIA` | `UPDATE` bersyarat membuat pengurangan stok atomik tanpa `FOR UPDATE`. Atribut `draft` dibutuhkan tombol Save dan Show pada UI-06 |
| 4 | Kelas C06 Transaksi | Operasi `hitungTotal()`, `tandaiLunas()`, `batalkan()`, `isLewatBatasWaktu()`. Tujuh atribut | Operasi dijalankan langsung oleh PembayaranController dalam satu transaksi basis data. Ditambah atribut `waktu_diambil`, `token_bayar`, dan `kode_kupon`, serta tabel baru `pengambilan_penjual` | `token_bayar` mengidentifikasi transaksi pada simulasi pembayaran, `kode_kupon` mencatat kupon yang ditebus, dan `waktu_diambil` mencatat pengambilan pesanan di toko |
| 5 | Kelas C08 ItemTransaksi | Tabel 4.1: `idItem`, `idListing`, `jumlah`, `hargaSatuan` | Ditambah atribut `idTransaksi: Integer` (sudah tercantum pada Tabel 5.8.2) | Menjadi foreign key ke tabel `transaksi` untuk merealisasikan komposisi Transaksi 1 ◆— 1..* ItemTransaksi |
| 6 | Kelas C12 ListingView | Tabel 4.1: tanpa atribut, penghapusan hanya melalui `tampilkanKonfirmasiHapus()` | Mengikuti Tabel 5.12: `idListingDiedit` menjadi parameter rute `/penjual/listing/[id]/edit` dan properti `isEditing`, `adaPerubahan` menjadi state `isDirty`, dan `hapusMakanan()` menjadi `handleKonfirmasiHapus` | Satu komponen form dipakai untuk tambah dan edit. `isDirty` menentukan perlu tidaknya dialog konfirmasi keluar (UC01) |
| 7 | Kelas C15 AuthController | `login()` mengembalikan objek Pengguna. Tidak ada rancangan sesi | `POST /api/auth/login` mengembalikan `id_pengguna`, `nama`, `peran`, lalu memasang cookie httpOnly `session_token` dan `role` (berlaku 24 jam). Ditambah tabel `auth_session`, `POST /api/auth/logout`, *role guard* `require_roles()`, dan `middleware.ts` di frontend | Setiap endpoint harus dapat memastikan pengguna sudah login dan memiliki peran yang sesuai |
| 8 | Kelas C17 ListingController | Kelas dengan tiga operasi | Diwujudkan sebagai fungsi *route* (`tambah_listing`, `ubah_listing`, `hapus_listing`) di `api/listing_routes.py`. Ditambah `GET /api/listing/penjual`, `GET /api/listing/{id}`, dan `POST /api/listing/upload-foto` | Mengikuti gaya FastAPI. Endpoint tambahan dibutuhkan untuk daftar listing penjual, form edit, dan unggah foto |
| 9 | Kelas C18 PembayaranController; layar UI-05 | `checkout(idPembeli, idListing, jumlah)` untuk satu listing. Ada `batalkan()` dan `batalkanLewatBatasWaktu()` yang berjalan berkala | `checkout_banyak()` membuat satu transaksi dari seluruh isi keranjang dan menerima `kode_kupon`. `checkout()` satu listing tetap ada. `batalkan()`, `batalkanLewatBatasWaktu()`, dan `kirimBatal()` pada C13 **tidak diimplementasikan**: transaksi yang melewati batas 15 menit ditandai BATAL saat pembayaran dicoba | Keranjang sesuai relasi Transaksi 1..* ItemTransaksi. Stok baru dikurangi saat pembayaran dikonfirmasi, sehingga transaksi yang belum dibatalkan tidak menahan stok |
| 10 | Kelas C21 PaymentGatewayAdapter; C13 PembayaranView | `buatTagihan()` mengembalikan kode QRIS dari QRIS dummy. `cekStatus()` meneruskan status dari gateway | `buatTagihan()` mengembalikan gambar QR dalam bentuk data URI PNG yang dibuat pustaka `qrcode` (isi tetap `SAVEBITE-DEMO-PAYMENT`). `cekStatus()` selalu mengembalikan `"BELUM"`. Pembayaran dikonfirmasi lewat tombol Simulate Payment yang memanggil `POST /api/pembayaran/scan/{token_bayar}` | Pembayaran hanya disimulasikan. QR sengaja tidak memuat tautan agar pemindaian tidak dapat mengonfirmasi pembayaran |
| 11 | Kelas C20 Validasi | `validasiListing()` juga memeriksa foto (PNG/JPG, maks. 10 MB) | Pemeriksaan foto dipindah ke `services/listing_service.py` (ekstensi, ukuran, dan *magic bytes*) dan `_validasi_foto()`. Aturan field juga dijaga skema Pydantic `DataListing`. Ditambah `validasiToko()` | Berkas foto diunggah lewat endpoint terpisah sebelum form dikirim |
| 12 | Layar UI-01 Sign Up | Layar pendaftaran akun | **Tidak diimplementasikan.** Akun Penjual dan Pembeli dibuat oleh `seed.py` | Tidak ada use case pendaftaran pada SKPL (hanya UC07 Login) |
| 13 | Layar UI-02 Log In | Memuat tautan "Forgot Password ?", "Sign Up", dan "Register your shop" | Hanya kolom email, kolom password, tombol tampil/sembunyi password, dan tombol Log In | Ketiga tautan menuju fitur di luar use case SKPL |
| 14 | Layar UI-03 Home | Memuat daftar kategori (UI03-03, UI03-04) | Kategori tidak diimplementasikan. Layar menampilkan "Today's Menu", kolom cari, dan kolom harga minimum/maksimum (UC04). Kartu menampilkan nama dan alamat toko | C04 tidak memiliki atribut kategori. Penyaringan harga mengikuti `tampilkanPilihanHarga()` pada C11 |
| 15 | Layar UI-04 (UI04-03, UI04-04, UI04-06); C07, C14 | "3 Day Streak" dan 7 indikator hari | Streak tidak diimplementasikan. Layar menampilkan status login hari ini, tanggal login terakhir, total poin, *progress bar* menuju `POIN_PER_KLAIM`, dan tombol klaim. Tombol selalu dapat ditekan; jika poin kurang, tampil pesan peringatan. Tombol Log Out juga ada di layar ini | C07 hanya menyimpan `poinTerkumpul` dan `tanggalLoginTerakhir`, sehingga streak tidak dapat dihitung tanpa mengubah skema |
| 16 | Layar UI-04 (UI04-08), UI-05 (UI05-12, UI05-14); C09 Kupon | Voucher "10% Discount" yang dipilih dari kartu voucher. Poin bertambah saat membeli | Kupon bernilai tetap Rp10.000 dan berlaku 7 hari. Kupon dipakai dengan mengetik kodenya pada kolom Coupon code di My Cart. Backend memeriksa pemilik, status terpakai, dan masa berlaku, memotong total (minimal Rp0), lalu mengembalikan kupon jika transaksi BATAL. Poin hanya bertambah dari login harian | `nilaiPotongan: Integer` pada C09 berupa nominal rupiah. Aturan poin mengikuti C07 |
| 17 | Layar UI-06 Add Product | Memuat field Category. Tidak ada field porsi dan kondisi | Tanpa Category. Ditambah field Serving (porsi) dan Condition (kondisi) yang wajib diisi. Tombol Save Draft menyimpan draf, tombol Show menampilkan listing ke katalog | Porsi dan kondisi adalah atribut wajib C04 dan diperiksa `validasiListing()` |
| 18 | Layar UI-07 Detail Produk | Tombol favorit (♡) dan tombol Add to Cart | Tanpa tombol favorit. Add to Cart diganti pengatur jumlah (− / +) yang langsung mengubah isi keranjang, dengan batas maksimum stok. Detail juga menampilkan nama toko, alamat, porsi, kondisi, dan batas kedaluwarsa | Favorit tidak memiliki use case maupun kelas. Pengatur jumlah yang sama dipakai di kartu katalog (UI03-11 s.d. UI03-13) |
| 19 | Tidak ada di DPPL | – | Ditambah dashboard Penjual berisi pesanan lunas dan tombol tandai sudah diambil (`api/penjualan_routes.py`), serta profil toko (`api/toko_routes.py`, halaman `/penjual/account`) | `kodePengambilan` pada C06 perlu dipakai Penjual saat pesanan diambil. Nama dan alamat toko ditampilkan di katalog sebagai lokasi pengambilan |

## B.2 Bukti Penerapan Best Practices

Tabel B.2. Bukti Best Practices

| Praktik | Bukti | Keterangan |
| :--- | :--- | :--- |
| Branching | https://github.com/unadd-rn/IF2150-RPL-K02-G06/branches | Satu branch per fitur dengan format `<tipe>/<nama-fitur>`, misalnya `feat/auth`, `feat/katalog-cari-filter`, `feat/checkout`, `feat/qris-dummy`, `feat/reward`, `fix/integration`. Seluruh branch digabung ke branch integrasi `Development` melalui Pull Request, lalu `Development` digabung ke `main` untuk rilis |
| Semantic commit | https://github.com/unadd-rn/IF2150-RPL-K02-G06/commits/Development | Dari 67 commit non-merge sejak 3 November 2026, 56 memakai awalan tipe (`feat`, `fix`, `test`, `chore`, `refactor`, `docs`) dan 36 di antaranya memakai scope, misalnya `feat(katalog): kolom cari & filter harga di /katalog (UC04)`. Sebagian commit awal masih memakai format `feat/...` |
| Track tasks | https://github.com/unadd-rn/IF2150-RPL-K02-G06/issues | **[PERLU DIISI: jumlah issue dan pembagiannya per anggota]**. Commit merujuk nomor issue, misalnya `feat: backend for issue #14` |
| Pull request dan review | https://github.com/unadd-rn/IF2150-RPL-K02-G06/pull/47, https://github.com/unadd-rn/IF2150-RPL-K02-G06/pull/78, https://github.com/unadd-rn/IF2150-RPL-K02-G06/pull/70, https://github.com/unadd-rn/IF2150-RPL-K02-G06/pull/83 | 28 PR digabung ke `Development` (#42 s.d. #83). #47 katalog (Ghina) digabung oleh Nadia. #78 reward (Cendra) digabung oleh Renata. #70 konfirmasi bayar (Sherin) digabung oleh Nadia. #83 pengujian E2E (Renata) digabung oleh Cendra. **[PERLU DIISI: nama reviewer tiap PR]** |
| Pengujian | https://github.com/unadd-rn/IF2150-RPL-K02-G06/tree/Development/src/backend/tests, https://github.com/unadd-rn/IF2150-RPL-K02-G06/tree/Development/src/frontend/tests/e2e, https://github.com/unadd-rn/IF2150-RPL-K02-G06/blob/Development/.github/workflows/ci.yml | Backend: 132 test pytest pada 14 berkas, seluruhnya lulus (14,6 detik, Python 3.12.10). Yang diuji: model RewardLogin dan klaim kupon (UC08), checkout, pembayaran atomik, rebutan stok terakhir, batas waktu bayar, dan kupon (UC05), skenario alternatif katalog (UC02 s.d. UC04), listing, validasi, dan unggah foto (UC01, UC06, UC09), pesanan penjual, profil toko, serta alur pembeli dari login sampai pengambilan. Frontend: 6 test Playwright pada 4 berkas. Cara menjalankan: `cd src/backend && python -m pytest`, dan `cd src/frontend && npm test` (backend harus berjalan dan sudah di-*seed*). CI menjalankan keduanya beserta *lint* dan *build* pada setiap push dan PR ke `Development` |

### B.2.1 Profiling dan Optimasi

| Informasi | Keterangan |
| :--- | :--- |
| Fitur / proses yang diprofil | Katalog Pembeli: `GET /api/katalog` (UC02), pencarian dan filter harga (UC04), dan `GET /api/katalog/{id}` (UC03). Sebagai pembanding, verifikasi password saat login (UC07) |
| Alat | `cProfile`, `EXPLAIN QUERY PLAN` SQLite, dan pencatatan waktu respons dengan `time.perf_counter` melalui FastAPI `TestClient` (Windows 11, Python 3.12.10, tanpa jaringan) |
| Temuan (sebelum) | Lihat tabel hasil pengukuran di bawah |
| Perbaikan | Tidak ada perubahan kode |
| Hasil (sesudah) | Sama dengan temuan, karena tidak ada perubahan kode |

Hasil pengukuran (median, p95 dalam kurung):

| Jumlah listing di tabel | `GET /api/katalog` | Cari + filter harga | Detail satu listing | Ukuran respons daftar |
| :--- | :--- | :--- | :--- | :--- |
| 15 (setara data *seed*) | 9,7 ms (12,3 ms) | 11,3 ms (15,3 ms) | 10,0 ms (13,3 ms) | 3,3 KB |
| 1.000 | 31,6 ms (41,1 ms) | 13,9 ms (17,8 ms) | 11,0 ms (13,2 ms) | 240 KB |
| 10.000 | 225 ms (308 ms) | 28,7 ms (33,9 ms) | 10,0 ms (11,0 ms) | 2,4 MB |

Temuan:
1. Query katalog memindai seluruh tabel dan mengurutkan dengan B-tree sementara (`SCAN listing_makanan | USE TEMP B-TREE FOR ORDER BY`), karena `batas_kedaluwarsa` dibungkus `datetime()` sehingga indeks tidak dapat dipakai. Query detail memakai primary key (`SEARCH ... USING INTEGER PRIMARY KEY`) dan waktunya tetap sekitar 10 ms.
2. Pada 10.000 listing, query bukan bottleneck utama. Dari 1,95 detik untuk 5 permintaan di bawah `cProfile`, `_dengan_toko()` memakan 1,22 detik (62%), dan 0,96 detik di antaranya (49%) adalah `dataclasses.asdict()` yang dipanggil untuk setiap listing. `fetchall()` SQLite hanya 0,15 detik (8%).
3. Katalog mengirim seluruh listing tersedia tanpa paginasi, sehingga waktu dan ukuran respons naik linear.
4. `bcrypt.checkpw` pada login memakan 362 ms (median). Ini disengaja untuk KNF02 dan terjadi sekali per login.

Fitur dinilai sudah memadai tanpa perbaikan. Pada skala demonstrasi (12 listing contoh) seluruh permintaan katalog selesai sekitar 10 ms, dan pada 1.000 listing masih sekitar 32 ms. Jika jumlah listing bertambah jauh, perbaikan yang disarankan adalah paginasi pada `GET /api/katalog`, mengganti `asdict()` dengan pemetaan langsung atau `JOIN` ke tabel `penjual`, dan menyimpan `batas_kedaluwarsa` dalam satu format agar dapat diindeks.

## B.3 Kendala dan Catatan Penting

**Menjalankan aplikasi**
- Backend dan frontend dijalankan di dua terminal. Backend dari folder `src/`: `uvicorn backend.main:app --port 8000`. Frontend dari `src/frontend/`: `npm ci`, lalu `npm run dev`.
- Aplikasi harus dibuka di `http://localhost:3000`. Frontend meneruskan `/api/*` ke `http://localhost:8000`, dan CORS backend hanya mengizinkan asal tersebut.
- Jalankan `python seed.py` di `src/backend/` sebelum login pertama. Basis data `src/savebite.db` dibuat otomatis. Pada Windows, jalankan dengan `PYTHONUTF8=1` jika muncul `UnicodeEncodeError`.
- Akun uji (data fiktif, password `password123`): Pembeli `pembeli@test.com`; Penjual `penjual@test.com`, `kantin@test.com`, `warung@test.com`. Akun Pembeli disemai dengan 100 poin agar klaim kupon dapat langsung dicoba.
- Tidak ada layanan eksternal dan tidak ada environment variable yang wajib diisi.

**Alur yang perlu diketahui saat menilai**
- Pembayaran adalah simulasi. Pada halaman Payment, tekan Simulate Payment. Memindai QR tidak mengonfirmasi pembayaran.
- Setelah lunas, Pembeli mendapat kode pengambilan. Pesanan muncul di dashboard Penjual pemilik listing, yang dapat menandainya sudah diambil.
- Kupon dipakai dengan mengetik kodenya (dari halaman Account) pada kolom Coupon code di My Cart.

**Known issues**
- Pendaftaran akun (UI-01) dan pemulihan password belum tersedia. Akun hanya berasal dari *seed*.
- Baris Discount di My Cart selalu menampilkan Rp0. Potongan kupon baru terlihat pada Total di halaman Payment.
- Pembatalan transaksi berkala belum ada. Transaksi yang melewati batas 15 menit baru menjadi BATAL saat pembayaran dicoba, dan kupon yang menempel baru dikembalikan pada saat itu. Stok tidak terpengaruh.
- Pesan kesalahan dari backend (misalnya "Stok tidak mencukupi") belum diteruskan ke layar. Pengguna melihat pesan umum "A server error occurred (HTTP 409)".
- `middleware.ts` hanya menjaga rute `/penjual` dan `/katalog`. Halaman `/cart`, `/reward`, dan `/pembayaran` dapat dibuka tanpa login, tetapi seluruh API-nya menolak dengan 401/403 dan halaman menampilkan tautan login.
- Teks antarmuka berbahasa Inggris, dengan beberapa teks yang masih berbahasa Indonesia.
- Kategori makanan, favorit, dan streak login tidak diimplementasikan (lihat B.1).

## B.4 Kontribusi Anggota

Tabel B.4. Kontribusi Anggota

| NIM | Nama | Modul / Fitur yang Dikerjakan | Persentase Kontribusi |
| :--- | :--- | :--- | :--- |
| *13525041* | *Renata Puspanegara Ninagan* | Fondasi sistem dan Login (UC07): skema basis data, autentikasi bcrypt, sesi dan *role guard*, LoginView, layout dan navbar. Keranjang, kupon pada checkout, dashboard pesanan dan profil toko Penjual, *seed data*, perapian UI/UX, integrasi antarfitur, dan pengujian E2E Pembeli | *20%* |
| *13525122* | *Nadia Aulia Syafarani* | Pengelolaan Listing Penjual (UC01, UC06, UC09): tambah, ubah, hapus (*soft delete*), draf, unggah foto, validasi listing. Penyesuaian QR pembayaran, penerjemahan antarmuka, dan pengujian E2E Penjual | *20%* |
| *13525119* | *Ghina Emelia Yantes* | Katalog Pembeli (UC02, UC03, UC04): daftar listing, detail listing, pencarian, filter harga, skenario alternatif beserta pengujiannya. Penyiapan CI | *20%* |
| *13525089* | *Sherin Felicia Danessa* | Pembayaran (UC05): *checkout*, ItemTransaksi, QRIS *dummy*, konfirmasi pembayaran dan pengurangan stok secara atomik, beserta pengujiannya | *20%* |
| *13525017* | *Cendra Asih Chairunnisa* | Reward (UC08): model RewardLogin dan Kupon, pencatatan poin saat login, RewardController, halaman My Reward, beserta pengujiannya. Perbaikan konfigurasi CI dan *rewrite* API, serta laporan M9 | *20%* |

## B.5 Traceability Kelas Perancangan ke Implementasi

Tabel B.5. Traceability Kelas Perancangan ke Implementasi

Seluruh lokasi relatif terhadap `src/`.

| ID Kelas | Nama Kelas Perancangan | Bentuk Implementasi | Lokasi (File dan Nama) | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| C01 | Pengguna «abstract» | Kelas dan tabel | `backend/models.py` - `Pengguna`, tabel `pengguna` | Atribut menjadi kolom `id_pengguna`, `nama`, `email`, `password` (hash bcrypt). `verifikasiPassword()` dijalankan sebagai `bcrypt.checkpw` di `routers/auth.py`. `bukaListing()` menjadi `GET /api/listing/penjual`. Kelas tidak dibuat objeknya saat berjalan (B.1 no. 2) |
| C02 | Penjual | Kelas dan tabel | `backend/models.py` - `Penjual`, tabel `penjual`; `backend/api/toko_routes.py` | `namaToko` dan `alamatToko` menjadi kolom. `getPeran()` menjadi hasil `CASE` pada Q-C15-01. `memilikiListing()` menjadi syarat `WHERE id_penjual = ?` di `listing_routes.py` |
| C03 | Pembeli | Kelas dan tabel | `backend/models.py` - `Pembeli`, tabel `pembeli` | `namaAkun` menjadi kolom `nama_akun`. Peran ditentukan oleh keberadaan baris pada tabel `pembeli` |
| C04 | ListingMakanan | Kelas (*dataclass*) dan tabel | `backend/models.py` - `ListingMakanan`, tabel `listing_makanan` | `cariById`, `ambilSemuaTersedia`, `cariDaftar` menjadi *classmethod*. `isTersedia` menjadi `is_tersedia()` dan konstanta `KONDISI_TERSEDIA`. `ubahData`, `kurangiStok`, `nonaktifkan` menjadi `UPDATE` langsung (B.1 no. 3). Ditambah atribut `draft` |
| C05 | MetodePembayaran «interface» | Kelas abstrak (ABC) | `backend/adapters/metode_pembayaran.py` - `MetodePembayaran` | `buat_tagihan()` dan `cek_status()` sebagai metode abstrak |
| C06 | Transaksi | Kelas (*dataclass*) dan tabel | `backend/models.py` - `Transaksi`, tabel `transaksi` dan `pengambilan_penjual` | Atribut menjadi kolom, `StatusTransaksi` menjadi `CHECK` pada kolom `status`. Operasi dijalankan oleh `PembayaranController` (B.1 no. 4) |
| C07 | RewardLogin | Kelas (*dataclass*) dan tabel | `backend/models.py` - `RewardLogin`, tabel `reward_login` | `catatLogin`, `cukupUntukKlaim`, `kurangiPoin` menjadi metode dengan nama yang sama. `POIN_PER_LOGIN = 10` dan `POIN_PER_KLAIM = 100` sebagai konstanta kelas. Ditambah `cariByPembeli()` (Q-C19-01) |
| C08 | ItemTransaksi | Kelas (*dataclass*) dan tabel | `backend/models.py` - `ItemTransaksi`, tabel `item_transaksi` | `hitungSubtotal()` menjadi `hitung_subtotal()`. Ditambah `id_transaksi` |
| C09 | Kupon | Kelas (*dataclass*) dan tabel | `backend/models.py` - `Kupon`, tabel `kupon` | `isBerlaku()` menjadi `is_berlaku()`. Ditambah `simpan()` (Q-C19-04), `cariByPembeli()`, dan `carikanByKode()` |
| C10 | LoginView | Halaman (komponen React) | `frontend/app/login/page.tsx` - `LoginPage`; `frontend/app/page.tsx`; `frontend/middleware.ts` | `tampilkanForm` menjadi *render* form, `kirimKredensial` menjadi `handleSubmit`, `tampilkanPesan` menjadi state `errorMessage`, `arahkanKeBeranda` menjadi `router.push` ke `/penjual` atau `/katalog` |
| C11 | KatalogView | Halaman dan komponen React | `frontend/app/katalog/page.tsx`, `frontend/app/katalog/[id]/page.tsx`, `frontend/components/katalog/` - `DaftarListing`, `KartuListing`, `DetailListing`, `FormPencarian`, `SearchBar`, `FilterHarga`, `PengaturJumlah`, `PesanKatalog`, `EmptyState` | `tampilkanDaftar` menjadi `DaftarListing`, `tampilkanDetail` menjadi `DetailListing`, `tampilkanPilihanHarga` menjadi `FilterHarga`, `kirimPencarian` menjadi `FormPencarian` dan `cariKatalog()` di `lib/api.ts`, `pilihListing` menjadi navigasi ke `/katalog/[id]`, `tampilkanPesan` menjadi `PesanKatalog` dan `EmptyState` |
| C12 | ListingView | Halaman dan komponen React | `frontend/app/penjual/listing/page.tsx`, `tambah/page.tsx`, `[id]/edit/page.tsx`; `frontend/components/penjual/` - `FormListing`, `KartuListingPenjual`, `DialogKonfirmasiKeluar`, `DialogKonfirmasiHapus` | `tampilkanFormTambah` dan `tampilkanFormEdit` menjadi `FormListing` dengan `isEditing`, `kirimListing` menjadi `handleSubmit`, `tampilkanKonfirmasiKeluar` dan `tampilkanKonfirmasiHapus` menjadi dua dialog, `hapusMakanan` menjadi `handleKonfirmasiHapus`, `adaPerubahan` menjadi state `isDirty` |
| C13 | PembayaranView | Halaman dan komponen React | `frontend/app/cart/page.tsx` - `CartPage`; `frontend/lib/cart.tsx` - `CartProvider`, `useCart`; `frontend/app/pembayaran/[idTransaksi]/page.tsx` - `PembayaranIsi`, `Ringkasan` | `tampilkanRingkasan` menjadi `Ringkasan`, `tampilkanQRIS` menjadi gambar `kode_qris`, `kirimBayar` menjadi `handleSimulatePayment`, `tampilkanHasil` menjadi tampilan status LUNAS dengan kode pengambilan, `tampilkanPesan` menjadi state `pesan`. `kirimBatal` tidak diimplementasikan (B.1 no. 9) |
| C14 | RewardView | Halaman (komponen React) | `frontend/app/reward/page.tsx` - `RewardPage` | `tampilkanProgres` menjadi kartu poin dan *progress bar*, `kirimKlaim` menjadi `onKlaim`, `tampilkanKupon` menjadi daftar My Coupons, `tampilkanPesan` menjadi state `pesan` |
| C15 | AuthController | *Route/handler* | `backend/routers/auth.py` - `login` (`POST /api/auth/login`), `logout`, `get_current_user`, `require_roles` | `login()` menjalankan Validasi, Q-C15-01, verifikasi bcrypt, dan `RewardLogin.catatLogin()` (Q-C15-02, Q-C15-03), lalu membuat sesi pada tabel `auth_session` |
| C16 | KatalogController | Fungsi dan *route* | `backend/controllers/katalog_controller.py` - `ambilListingTersedia`, `ambilDetail`, `cariListing`; `GET /api/katalog`, `GET /api/katalog/{id_listing}`; `backend/schemas/katalog.py` | Tiga operasi menjadi fungsi dengan nama yang sama (Algo-C16-01 s.d. 03). Respons dilengkapi nama dan alamat toko |
| C17 | ListingController | *Route/handler* dan *service* | `backend/api/listing_routes.py` - `tambah_listing`, `ubah_listing`, `hapus_listing`, `upload_foto`; `backend/services/listing_service.py` - `simpan_foto_listing` | `idPenjual` diambil dari sesi. `hapusListing` berupa *soft delete* (`aktif = 0`) |
| C18 | PembayaranController | Kelas dan *route* | `backend/controllers/pembayaran_controller.py` - `PembayaranController` (`checkout`, `checkout_banyak`, `konfirmasi_bayar`); `backend/api/pembayaran_routes.py` | Atribut `metodePembayaran` menjadi `self.metode`. `batalkan` dan `batalkanLewatBatasWaktu` tidak diimplementasikan (B.1 no. 9) |
| C19 | RewardController | Fungsi dan *route* | `backend/controllers/reward_controller.py` - `lihatProgres`, `klaimReward`; `GET /api/reward`, `POST /api/reward/klaim`; `backend/schemas/reward.py` | `klaimReward` mengurangi poin dan menerbitkan Kupon dalam satu transaksi (`BEGIN IMMEDIATE`) |
| C20 | Validasi | Kelas dengan metode statis | `backend/validation.py` - `Validasi`; `backend/schemas/listing_schema.py` - `DataListing` | `validasiListing` dan `validasiKredensial` dengan nama yang sama. Ditambah `validasiToko`. Pemeriksaan foto dipindah ke `listing_service.py` (B.1 no. 11) |
| C21 | PaymentGatewayAdapter | Kelas | `backend/adapters/payment_gateway_adapter.py` - `PaymentGatewayAdapter` | Merealisasikan `MetodePembayaran`. Atribut `urlGateway` menjadi `url_gateway`. Perilaku `buat_tagihan` dan `cek_status` dijelaskan pada B.1 no. 10 |

Catatan:
- Satu kelas perancangan boleh diwujudkan oleh beberapa file/unit, dan satu file/unit boleh mewujudkan beberapa kelas perancangan. Tuliskan semuanya.
- Kelas perancangan yang **tidak diimplementasikan** atau **digabung/dipecah** tetap dicantumkan, and alasannya dicatat di Bagian B.1.
