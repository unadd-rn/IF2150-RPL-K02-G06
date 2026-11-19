<h1>
IF2150 REKAYASA PERANGKAT LUNAK
<br>
TUGAS 10
<br>
HASIL IMPLEMENTASI DAN UJI PERANGKAT LUNAK (HIUPL)
</h1>
<br>

## *SaveBite*
<img width="40%" alt="Logo SaveBite" src="./assets/save_bite.PNG" />

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

## Daftar Isi

- [BAB 1: Pendahuluan](#bab-1-pendahuluan)
  - [1.1 Tujuan Penulisan Dokumen](#11-tujuan-penulisan-dokumen)
  - [1.2 Lingkup Masalah](#12-lingkup-masalah)
  - [1.3 Definisi, Istilah, dan Singkatan](#13-definisi-istilah-dan-singkatan)
  - [1.4 Aturan Penomoran](#14-aturan-penomoran)
  - [1.5 Referensi](#15-referensi)
  - [1.6 Deskripsi Umum Dokumen (Ikhtisar)](#16-deskripsi-umum-dokumen-ikhtisar)
- [BAB 2: Deskripsi Umum Perangkat Lunak](#bab-2-deskripsi-umum-perangkat-lunak)
- [BAB 3: Implementasi](#bab-3-implementasi)
  - [3.1 Lingkungan Implementasi](#31-lingkungan-implementasi)
  - [3.2 Implementasi Modul](#32-implementasi-modul)
  - [3.3 Implementasi Antarmuka](#33-implementasi-antarmuka)
  - [3.4 File Lain](#34-file-lain)
- [BAB 4: Hasil Pengujian](#bab-4-hasil-pengujian)
  - [4.1 Strategi dan Kedalaman Pengujian Kelas](#41-strategi-dan-kedalaman-pengujian-kelas)
  - [4.2 Pengujian Unit Kelas](#42-pengujian-unit-kelas)
  - [4.3 Pengujian Integrasi](#43-pengujian-integrasi)
  - [4.4 Pengujian Use Case](#44-pengujian-use-case)
  - [4.5 Pengujian Kebutuhan Non-Fungsional (KNF)](#45-pengujian-kebutuhan-non-fungsional-knf)
  - [4.6 Tangkapan Layar dan Bukti Hasil Pengujian](#46-tangkapan-layar-dan-bukti-hasil-pengujian)
- [BAB 5: Traceability](#bab-5-traceability)

---

## Daftar Perubahan

| Revisi | Deskripsi |
| :--- | :--- |
| *A* | *Dokumen HIUPL disusun berdasarkan SKPL, APL, DPPL2, dan laporan Implementasi M9; hasil implementasi dan pengujian aktual ditambahkan.* |
| *B* |  |
| *C* |  |
| ... |  |

---

# BAB 1: Pendahuluan

## 1.1 Tujuan Penulisan Dokumen
Dokumen Hasil Implementasi dan Uji Perangkat Lunak (HIUPL) SaveBite menjelaskan lingkungan dan realisasi implementasi, hasil pengujian unit, integrasi, use case, dan kebutuhan non-fungsional, serta pemetaan kebutuhan terhadap kode dan bukti uji. Dokumen ini ditujukan bagi dosen/asisten dan anggota kelompok sebagai bahan evaluasi serta acuan pemeliharaan perangkat lunak.

## 1.2 Lingkup Masalah
SaveBite adalah aplikasi web untuk mempertemukan penjual makanan surplus dengan pembeli melalui pengelolaan listing, katalog dan pencarian, keranjang, checkout dengan QRIS dummy, serta reward login berupa kupon; aplikasi berjalan pada frontend Next.js dan backend FastAPI dengan basis data SQLite lokal, tanpa integrasi ke payment gateway eksternal.

## 1.3 Definisi, Istilah, dan Singkatan

Tabel 1.3. Definisi Istilah dan Singkatan

| Singkatan, Akronim, atau Istilah | Penjelasan |
| :--- | :--- |
| *P/L* | *Singkatan dari Perangkat Lunak, yaitu aplikasi yang memberikan perintah kepada komputer untuk menjalankan tugas tertentu.* |
| *SKPL* | *Singkatan dari Spesifikasi Kebutuhan Perangkat Lunak, yaitu dokumen yang merangkum kriteria-kriteria yang diperlukan untuk membangun aplikasi menjalankan tugasnya.* |
| *DPPL* | *Singkatan dari Deskripsi Perancangan Perangkat Lunak, yaitu dokumen yang menjelaskan rancangan arsitektur, kelas, dan antarmuka P/L.* |
| *HIUPL* | *Singkatan dari Hasil Implementasi dan Uji Perangkat Lunak, yaitu dokumen yang melaporkan hasil implementasi dan pengujian P/L.* |
| *KF* | *Singkatan dari Kebutuhan Fungsional.* |
| *KNF* | *Singkatan dari Kebutuhan Non-Fungsional.* |
| *UC* | *Singkatan dari Use Case.* |
| *TC* | *Singkatan dari Test Case, yaitu satu kasus uji untuk skenario tertentu.* |
| *UT* | *Singkatan dari Unit Test, yaitu test case tingkat kelas/operasi.* |
| *INT* | *Singkatan dari Integration Test, yaitu test case yang menguji interaksi antarkomponen.* |
| *Boundary* | *Kasus uji pada nilai batas masukan, misalnya nilai minimum, maksimum, atau tepat di ambang aturan.* |
| *Coverage* | *Persentase baris/cabang kode yang dieksekusi oleh pengujian.* |
| *SQLite* | *DBMS relasional berbasis berkas yang dipakai aplikasi pada implementasi M9.* |
| *E2E* | *End-to-end, pengujian alur aplikasi dari antarmuka sampai layanan backend.* |

## 1.4 Aturan Penomoran

Tabel 1.4. Aturan Penomoran

| Hal/Bagian | Penomoran | Keterangan |
| :--- | :--- | :--- |
| *Kebutuhan Fungsional* | *KFXX* | *Sesuai SKPL* |
| *Kebutuhan Non-Fungsional* | *KNFXX* | *Sesuai SKPL* |
| *Use Case* | *UCXX* | *Sesuai SKPL* |
| *Kelas* | *CXX* | *Sesuai DPPL* |
| *Antarmuka* | *I-XX* | *Sesuai DPPL* |
| *Test Case Unit* | *CXX-UTYY* | *XX adalah nomor kelas, YY adalah nomor urut test case unit pada kelas tersebut* |
| *Test Case Integrasi* | *INT-TCYY* | *YY adalah nomor urut test case integrasi* |
| *Test Case Use Case* | *UCXX-TCYY* | *XX adalah nomor use case, YY adalah nomor urut test case pada use case tersebut* |
| *Test Case KNF* | *KNFXX-TCYY* | *XX adalah nomor KNF, YY adalah nomor urut test case KNF tersebut* |

## 1.5 Referensi
- K02_G06_SKPL, Tugas 5, `docs/M5/K02_G06_SKPL.md`.
- K02_G06_APL, Tugas 6, `docs/M6/K02_G06_APL.md`.
- K02_G06_DPPL2, Tugas 8, `docs/M8/K02_G06_DPPL2.md`.
- K02_G06_Implementasi, Tugas 9, `docs/M9/K02_G06_Implementasi.md`.
- FastAPI, Python `pytest`, `pytest-cov`, Playwright, Next.js, React, dan SQLite; versi implementasi dicatat pada Subbab 3.1.

## 1.6 Deskripsi Umum Dokumen (Ikhtisar)
Bab 1 menjelaskan tujuan, lingkup, istilah, penomoran, dan referensi. Bab 2 memberi gambaran sistem. Bab 3 mencatat lingkungan serta modul, antarmuka, dan file implementasi. Bab 4 melaporkan strategi dan hasil pengujian unit, integrasi, use case, dan KNF berikut buktinya. Bab 5 memetakan kebutuhan fungsional dan non-fungsional ke implementasi dan pengujian.

<br>

---

# BAB 2: Deskripsi Umum Perangkat Lunak

SaveBite merupakan aplikasi web untuk jual-beli makanan surplus. Pembeli menggunakan katalog, pencarian dan filter harga, detail listing, keranjang, pembayaran QRIS dummy, serta reward login. Penjual mengelola listing dan pesanan. Frontend Next.js mengakses backend FastAPI dan data disimpan di SQLite. Tidak ada payment gateway eksternal yang terhubung. Diagram use case berikut merujuk SKPL M5.

<p align="center">
<img alt="Use Case Diagram SaveBite" src="../M5/assets/diagram/Diagram%20Use%20Case.png" width="90%">
</p>
<p align="center">
<i>Gambar 2.1. Use Case Diagram SaveBite (sumber: SKPL M5)</i>
</p>

<br>

---

# BAB 3: Implementasi

Bagian ini diisi dengan informasi tentang elemen P/L yang dikembangkan (*executable files*, *configuration files*, *data files*, dan sebagainya) serta perubahannya terhadap rancangan pada DPPL (jika ada).

## 3.1 Lingkungan Implementasi

Tuliskan *hardware* dan *software* yang digunakan untuk implementasi, mencakup *operating system*, bahasa pemrograman beserta versinya, *framework*/*library*, DBMS, *development tools*, dan *version control*. Lingkungan ini harus konsisten dengan **Subbab 2.1 DPPL**; jelaskan jika ada perubahan. Cantumkan juga *framework* dan alat pengujian yang dipakai.

Implementasi akhir menyimpang dari rancangan APL/DPPL yang menyebut PostgreSQL, Python 3.11, dan Node.js 20. Implementasi M9 yang lebih baru menetapkan SQLite, Python 3.12, dan Node.js 22. Bukti eksekusi pengujian M10 mencatat Windows 11 dan Python 3.13.7; versi runtime untuk seluruh anggota perlu diseragamkan/ditetapkan sesuai mesin rilis yang diuji.

Tabel 3.1. Lingkungan Implementasi

| Aspek | Keterangan |
| :--- | :--- |
| *Hardware* | *Belum tercatat pada dokumen implementasi atau bukti uji; lengkapi spesifikasi perangkat pengujian.* |
| *Operating System* | *Windows 11 (mesin bukti pytest M10); browser Chromium untuk E2E.* |
| *Bahasa Pemrograman* | *Python 3.13.7 pada bukti pengujian; TypeScript; versi Node.js 22 menurut laporan M9.* |
| *Framework/Library* | *FastAPI, Pydantic, Next.js 16.4.4, React 19.3.0, bcrypt 4.1.2, qrcode, Playwright.* |
| *DBMS* | *SQLite melalui modul `sqlite3` bawaan Python; basis data `src/savebite.db`.* |
| *Development Tools* | *Visual Studio Code, Git/GitHub, npm.* |
| *Testing Tools* | *pytest 8+, pytest-cov/coverage, FastAPI TestClient/httpx, Playwright 1.64.1, Chromium.* |

## 3.2 Implementasi Modul

Tabel 3.2. Implementasi Modul

| No | ID Kelas | Nama Modul/Kelas | Nama File Fisik | Nama File Executable |
| :--- | :--- | :--- | :--- | :--- |
| 1 | C01 | Pengguna | `src/backend/models.py`; `src/backend/routers/auth.py` | - |
| 2 | C02 | Penjual | `src/backend/models.py`; `src/backend/api/toko_routes.py` | - |
| 3 | C03 | Pembeli | `src/backend/models.py` | - |
| 4 | C04 | ListingMakanan | `src/backend/models.py`; `src/backend/controllers/katalog_controller.py`; `src/backend/api/listing_routes.py` | - |
| 5 | C05 | MetodePembayaran | `src/backend/adapters/metode_pembayaran.py` | - |
| 6 | C06 | Transaksi | `src/backend/models.py`; `src/backend/controllers/pembayaran_controller.py` | - |
| 7 | C07 | RewardLogin | `src/backend/models.py` | - |
| 8 | C08 | ItemTransaksi | `src/backend/models.py` | - |
| 9 | C09 | Kupon | `src/backend/models.py` | - |
| 10 | C15 | AuthController | `src/backend/routers/auth.py` | - |
| 11 | C16 | KatalogController | `src/backend/controllers/katalog_controller.py` | - |
| 12 | C17 | ListingController | `src/backend/api/listing_routes.py`; `src/backend/services/listing_service.py` | - |
| 13 | C18 | PembayaranController | `src/backend/controllers/pembayaran_controller.py`; `src/backend/api/pembayaran_routes.py` | - |
| 14 | C19 | RewardController | `src/backend/controllers/reward_controller.py` | - |
| 15 | C20 | Validasi | `src/backend/validation.py`; `src/backend/schemas/listing_schema.py` | - |
| 16 | C21 | PaymentGatewayAdapter | `src/backend/adapters/payment_gateway_adapter.py` | - |

C10â€“C14 adalah kelas antarmuka dan dicantumkan pada Tabel 3.3.

## 3.3 Implementasi Antarmuka

Tabel 3.3. Implementasi Antarmuka

| No | ID Antarmuka | Nama Antarmuka | Nama File Fisik | Nama File Executable |
| :--- | :--- | :--- | :--- | :--- |
| 1 | UI-02 / C10 | Login | `src/frontend/app/login/page.tsx` | Next.js |
| 2 | UI-03 / C11 | Katalog dan detail listing | `src/frontend/app/katalog/page.tsx`; `src/frontend/app/katalog/[id]/page.tsx`; `src/frontend/components/katalog/` | Next.js |
| 3 | UI-04 / C14 | My Reward | `src/frontend/app/reward/page.tsx` | Next.js |
| 4 | UI-05 / C13 | My Cart dan Pembayaran | `src/frontend/app/cart/page.tsx`; `src/frontend/app/pembayaran/[idTransaksi]/page.tsx` | Next.js |
| 5 | UI-06 / C12 | Manajemen listing Penjual | `src/frontend/app/penjual/listing/page.tsx`; `src/frontend/app/penjual/listing/tambah/page.tsx`; `src/frontend/app/penjual/listing/[id]/edit/page.tsx` | Next.js |

## 3.4 File Lain

Tabel 3.4. File Lain

| No | Nama File | Keterangan |
| :--- | :--- | :--- |
| 1 | `src/backend/main.py` | Titik masuk backend FastAPI dan registrasi router. |
| 2 | `src/backend/seed.py` | Pembuatan skema dan data awal untuk pengembangan/pengujian. |
| 3 | `src/savebite.db` | Basis data lokal SQLite. |
| 4 | `src/backend/requirements.txt` | Daftar dependensi backend. |
| 5 | `src/frontend/package.json`, `package-lock.json` | Skrip dan dependensi frontend. |
| 6 | `src/backend/tests/` | Suite pengujian backend pytest. |
| 7 | `src/frontend/tests/e2e/` | Suite pengujian antarmuka Playwright. |
| 8 | `src/frontend/next.config.ts`, `src/frontend/playwright.config.ts` | Konfigurasi proxy aplikasi dan Playwright. |

<br>

---

# BAB 4: Hasil Pengujian

Bab ini melaporkan hasil pengujian P/L pada level unit, integrasi, dan sistem. Pengujian dilakukan pada tag release terakhir Tugas 9. Hasil aktual diisi berdasarkan pengamatan saat pengujian. Kesimpulan diisi `Pass` atau `Fail`, dan untuk `Fail` dilengkapi penyebab serta usulan perbaikan.

## 4.1 Strategi dan Kedalaman Pengujian Kelas

Pengujian mendalam diberikan pada kelas yang mengandung aturan bisnis, validasi, status, keamanan, atau transaksi. Kelas data murni dan View diuji melalui alur use case. Basis pemetaan adalah daftar C01–C21 pada DPPL2 dan traceability implementasi M9.

| ID Kelas | Nama | Kedalaman | Dasar dan cakupan bukti |
| :--- | :--- | :--- | :--- |
| C01 | Pengguna | Sedang | Autentikasi/hash diuji melalui C15; `models.py`. |
| C02 | Penjual | Tidak perlu | Data peran; perilaku listing/toko diuji pada UC01/06/09 dan API toko. |
| C03 | Pembeli | Tidak perlu | Data akun; digunakan oleh alur katalog, reward, checkout. |
| C04 | ListingMakanan | Mendalam | Ketersediaan, batas stok, tanggal, dan data listing; `models.py`, listing dan katalog. |
| C05 | MetodePembayaran | Sedang | Interface adapter pembayaran; uji adapter dan controller. |
| C06 | Transaksi | Mendalam | Status, tenggat, pembayaran dan konsistensi transaksi. |
| C07 | RewardLogin | Mendalam | Akumulasi poin, batas harian, ambang klaim. |
| C08 | ItemTransaksi | Sedang | Subtotal dan relasi item terhadap transaksi. |
| C09 | Kupon | Mendalam | Kepemilikan, masa berlaku, status terpakai, diskon, pengembalian. |
| C10 | LoginView | Sedang | Tampilan login dan validasi alur Playwright. |
| C11 | KatalogView | Sedang | Daftar, detail, pencarian dan filter; E2E serta screenshot UC02–04. |
| C12 | ListingView | Sedang | Form tambah/edit/hapus dan dialog konfirmasi; screenshot UC01/06/09. |
| C13 | PembayaranView | Sedang | Keranjang, pembayaran simulasi dan status; Playwright UC05. |
| C14 | RewardView | Sedang | Progres dan klaim reward; screenshot UC08 dan Playwright. |
| C15 | AuthController | Mendalam | Kredensial, sesi, peran dan login harian. |
| C16 | KatalogController | Mendalam | Ambil daftar/detail, cari, filter, ketersediaan. |
| C17 | ListingController | Mendalam | Kepemilikan, tambah/edit/hapus, unggah dan validasi foto. |
| C18 | PembayaranController | Mendalam | Checkout multi item, validasi stok, transaksi atomik dan status. |
| C19 | RewardController | Mendalam | Klaim kupon dan pengurangan poin atomik. |
| C20 | Validasi | Mendalam | Input kredensial/listing/toko dan foto. |
| C21 | PaymentGatewayAdapter | Sedang | Pembuatan QR dummy dan status pembayaran simulasi. |

## 4.2 Pengujian Unit Kelas

Perintah dan hasil sesuai artefak uji M10: dari `src/backend`, jalankan `python -m pytest -v --cov=backend --cov-branch --cov-report=term-missing`. Artefak mencatat 132 passed, 0 failed, total coverage 82% statements dan 87% branches. Lokasi test: `src/backend/tests/`; keluaran lengkap pada [pytest-backend.txt](./assets/bukti/pytest-backend.txt).

Kasus mendalam mencakup listing dan validasi (normal, batas, input salah, tanggal kedaluwarsa, foto), reward/kupon (poin cukup/tidak cukup, kupon kedaluwarsa/telah dipakai/milik pengguna lain), checkout dan pembayaran (jumlah/stok/status, banyak item, batas waktu, bayar ganda, rollback dan konkurensi). Detail nama fungsi dan hasil tiap kasus tercantum pada log pytest. Laporan coverage tersedia per berkas, bukan per kelas; karena itu angka coverage tidak diklaim sebagai coverage kelas DPPL. Angka berkas utama: `models.py` 89%, `katalog_controller.py` 100%, `pembayaran_controller.py` 98%, `reward_controller.py` 90%, `auth.py` 80%, `validation.py` 80%, `payment_gateway_adapter.py` 83%. Target minimal 70% per kelas belum dapat diverifikasi dari laporan agregat.

## 4.3 Pengujian Integrasi

Bukti backend menjalankan komponen FastAPI, controller, model dan SQLite pada fixture pengujian. Cakupan interaksi utama berikut dapat ditelusuri ke test pada log; ID INT di bawah merupakan pengelompokan dokumentasi M10 atas test yang sudah berjalan.

| ID Antarmuka | Komponen asal → tujuan | Batas | Test terkait |
| :--- | :--- | :--- | :--- |
| I-01 | KatalogController/API → ListingMakanan/SQLite | Controller–Model–DB | INT-TC01: katalog, detail, pencarian/filter, alternatif tersedia/kosong. |
| I-02 | ListingController/API → Validasi, listing_service, SQLite | Controller–validasi–DB/file | INT-TC02: tambah/edit/hapus, kepemilikan penjual, foto PNG/JPG dan penolakan file invalid. |
| I-03 | Auth API → Pengguna, RewardLogin, sesi SQLite | API–model–DB | INT-TC03: login berhasil/gagal, peran, sesi dan poin login. |
| I-04 | PembayaranController/API → Transaksi, ItemTransaksi, SQLite | Controller–model–DB/transaksi | INT-TC04: checkout valid, multi item, rollback jika satu item gagal, stok bersaing dan pembayaran ganda. |
| I-05 | PembayaranController → PaymentGatewayAdapter | Controller–adapter | INT-TC05: QR dummy dibuat, status tetap belum lunas sampai aksi simulasi, scan dan pembayaran terkonfirmasi. |
| I-06 | RewardController/API → RewardLogin, Kupon, SQLite | Controller–model–DB | INT-TC06: klaim cukup/tidak cukup, validasi kupon dan pemakaian pada checkout. |

Hasil seluruh test yang tercakup dalam log backend lulus. ID INT adalah indeks dokumentasi, bukan ID yang sudah tercetak oleh runner. Pengujian browser lintas frontend/backend dicatat terpisah oleh Playwright pada Tabel 4.6.
## 4.4 Pengujian Use Case

Pengujian use case mengacu pada skenario SKPL M5. Prosedur dijalankan pada antarmuka aplikasi; hasil ditelusuri melalui bukti layar dengan ID test case. Kesimpulan di bawah mengikuti bukti yang disimpan pada `docs/M10/assets/bukti/`.

| ID Pengujian | ID KF | Use Case dan Skenario | Prosedur/Masukan ringkas | Hasil yang diharapkan dan hasil aktual | Kesimpulan | Bukti |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| UC01-TC01 | KF01 | UC01 tambah listing, normal | Penjual mengisi form listing valid dan menyimpan/menampilkan listing. | Listing tersimpan dan muncul pada pengelolaan penjual/katalog. Bukti menunjukkan form dan hasil listing. | Pass | [TC01a](./assets/bukti/UC01-TC01a.png), [TC01b](./assets/bukti/UC01-TC01b.png) |
| UC01-TC02 | KF01 | UC01 validasi gagal | Kirim form dengan data wajib tidak valid. | Sistem menolak penyimpanan dan memberi umpan balik validasi. | Pass | [TC02](./assets/bukti/UC01-TC02.png) |
| UC01-TC04 | KF01 | UC01 keluar saat form berubah | Ubah form lalu coba keluar; periksa dialog dan pilihan pengguna. | Dialog konfirmasi tampil; pengguna dapat tetap mengedit atau keluar. | Pass | [TC04a](./assets/bukti/UC01-TC04a.png), [TC04b](./assets/bukti/UC01-TC04b.png) |
| UC02-TC01 | KF02 | UC02 katalog tersedia, normal | Login sebagai Pembeli lalu buka katalog. | Listing tersedia tampil. | Pass | [bukti gabungan UC07/UC02](./assets/bukti/UC07-TC01_UC02-TC01.png) |
| UC02-TC02 | KF02 | UC02 katalog kosong | Buka katalog tanpa listing tersedia. | Empty state memberi tahu bahwa katalog kosong. | Pass | [TC02](./assets/bukti/UC02-TC02.png) |
| UC02-TC03 | KF02 | UC02 listing tidak tersedia | Buka detail listing yang tidak lagi tersedia. | Sistem tidak menampilkan listing sebagai tersedia. | Pass | [TC03](./assets/bukti/UC02-TC03.png) |
| UC03-TC01 | KF02 | UC03 detail listing, normal | Pilih listing tersedia dari katalog. | Detail listing yang dipilih tampil. | Pass | [TC01](./assets/bukti/UC03-TC01.png) |
| UC03-TC02 | KF02 | UC03 listing hilang/tidak tersedia | Buka detail listing yang sudah tidak tersedia. | Sistem menolak detail dan menampilkan kondisi tidak tersedia. | Pass | [TC02](./assets/bukti/UC03-TC02.png) |
| UC04-TC01 | KF03 | UC04 pencarian/filter normal | Cari kata kunci dan terapkan batas harga yang memiliki hasil. | Hanya listing yang sesuai kriteria tampil. | Pass | [TC01](./assets/bukti/UC04-TC01.png) |
| UC04-TC02 | KF03 | UC04 kata kunci tanpa hasil | Cari teks yang tidak cocok dengan listing. | Empty state hasil pencarian tampil. | Pass | [TC02](./assets/bukti/UC04-TC02.png) |
| UC04-TC03 | KF03 | UC04 rentang harga tanpa hasil | Terapkan rentang harga tanpa listing cocok. | Empty state filter tampil. | Pass | [TC03](./assets/bukti/UC04-TC03.png) |
| UC04-TC04 | KF03 | UC04 rentang tidak valid | Masukkan nilai harga minimum/maksimum yang tidak valid. | Masukan ditolak/hasil tidak valid ditangani. | Pass | [TC04](./assets/bukti/UC04-TC04.png) |
| UC05-TC01 | KF04 | UC05 pembayaran, normal | Checkout item, buka QR dummy, lalu tekan Simulate Payment. | Transaksi menjadi lunas dan konfirmasi tampil. | Pass | [TC01a](./assets/bukti/UC05-TC01a.png), [TC01b](./assets/bukti/UC05-TC01b.png) |
| UC05-TC02 | KF04 | UC05 pembayaran tidak diteruskan/bermasalah | Ikuti skenario alternatif pembayaran yang tercatat pada bukti. | Transaksi tidak dinyatakan lunas tanpa konfirmasi simulasi. | Pass | [TC02](./assets/bukti/UC05-TC02.png) |
| UC06-TC01 | KF05 | UC06 edit listing, normal | Ubah data listing milik Penjual dan simpan. | Perubahan tersimpan. | Pass | [TC01](./assets/bukti/UC06-TC01.png) |
| UC06-TC02 | KF05 | UC06 input edit tidak valid | Kirim perubahan dengan input tidak valid. | Perubahan ditolak dan data lama tetap. | Pass | [TC02](./assets/bukti/UC06-TC02.png) |
| UC07-TC01 | KF06 | UC07 login, normal | Masukkan kredensial akun uji yang valid. | Pengguna masuk dan diarahkan sesuai perannya. | Pass | [bukti gabungan UC07/UC02](./assets/bukti/UC07-TC01_UC02-TC01.png) |
| UC07-TC02 | KF06 | UC07 kredensial tidak valid | Masukkan password salah. | Login ditolak dengan pesan kesalahan. | Pass | [TC02](./assets/bukti/UC07-TC02.png) |
| UC08-TC01 | KF06 | UC08 klaim reward, normal | Login harian, capai ambang poin, klaim kupon. | Poin berkurang dan kupon diterbitkan. | Pass | [TC01a](./assets/bukti/UC08-TC01a.png), [TC01b](./assets/bukti/UC08-TC01b.png) |
| UC08-TC02 | KF06 | UC08 poin belum cukup | Klaim saat poin di bawah ambang. | Klaim ditolak dan kekurangan poin diinformasikan. | Pass | [TC02](./assets/bukti/UC08-TC02.png) |
| UC09-TC01 | KF02 | UC09 hapus listing, normal | Penjual pilih listing, konfirmasi penghapusan. | Listing dinonaktifkan dari katalog. | Pass | [TC01a](./assets/bukti/UC09-TC01a.png), [TC01b](./assets/bukti/UC09-TC01b.png) |
| UC09-TC02 | KF02 | UC09 batal hapus | Batalkan dialog konfirmasi hapus. | Listing tetap ada dan aktif. | Pass | [TC02](./assets/bukti/UC09-TC02.png) |

Catatan: penamaan skenario TC02/TC03 di atas disimpulkan dari nama bukti dan skenario SKPL; jika urutan dalam skenario manual pengujian kelompok berbeda, sesuaikan label sebelum pengumpulan.

<br>

## 4.5 Pengujian Kebutuhan Non-Fungsional (KNF)

KNF dinilai berdasarkan bukti yang tersedia. Uji putus jaringan eksplisit dan pengamanan transport HTTPS tidak terlihat pada bukti M10 sehingga tidak diklaim telah lulus.

Tabel 4.5. Hasil Pengujian KNF

| ID Pengujian | ID KNF | Parameter | Target Terukur | Metode dan Alat | Hasil Aktual | Kesimpulan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KNF01-TC01 | KNF01 | Reliability | Tidak ada perubahan parsial/ganda ketika transaksi pembayaran gagal. | Suite pytest: rollback seluruh item, pembayaran ganda, dan dua pembeli berebut stok terakhir. | Bukti backend menunjukkan skenario tersebut lulus; pemutusan jaringan literal tidak disimulasikan. | Pass terbatas* |
| KNF02-TC01 | KNF02 | Security | Password tidak disimpan plaintext; SKPL secara khusus mensyaratkan SHA-256 sebelum transmisi. | Tinjau autentikasi, penyimpanan password, dan test kredensial salah. | Implementasi memakai bcrypt untuk penyimpanan, tetapi tidak melakukan SHA-256 di client sebelum pengiriman; HTTPS tidak dibuktikan. | Fail terhadap requirement saat ini |

*Pass KNF01 terbatas pada konsistensi transaksi yang diuji. Untuk membuktikan target penuh, tambahkan skenario putus jaringan. KNF02 perlu diselaraskan oleh kelompok dengan pengajar: bcrypt merupakan mekanisme penyimpanan yang lebih tepat dibanding SHA-256, tetapi requirement SKPL belum diperbarui dan meminta hash sebelum password dikirim.

## 4.6 Tangkapan Layar dan Bukti Hasil Pengujian

Bukti tersimpan di `docs/M10/assets/bukti/`. Screenshot per skenario ditautkan pada Tabel 4.4.

| Jenis bukti | Hasil/bukti |
| :--- | :--- |
| Backend | [pytest-backend.txt](./assets/bukti/pytest-backend.txt): 132 passed, total coverage 82% statements dan 87% branches. |
| Frontend E2E | [playwright-frontend.txt](./assets/bukti/playwright-frontend.txt): 6 passed di Chromium headless. |
| Coverage per berkas | `models.py` 89%; `katalog_controller.py` 100%; `pembayaran_controller.py` 98%; `reward_controller.py` 90%; `auth.py` 80%; `validation.py` 80%; `payment_gateway_adapter.py` 83%. Angka tersebut tidak memisahkan coverage per kelas DPPL. |
| Bukti performa | Angka profiling katalog/login pada laporan M9 bagian B.2.1; ini bukan pengukuran baru M10 dan tidak dibandingkan dengan target KNF karena SKPL tidak menetapkan target angka response time. |

---

# BAB 5: Traceability

Setiap KF ditautkan ke use case, kelas, file, dan pengujian. `KF07` dipetakan sebagai validasi yang digunakan lintas alur sesuai tabel SKPL M5.

Tabel 5.1. Matriks Kerunutan KF terhadap Implementasi dan Pengujian

| KF ID | KNF terkait | Use Case ID | Kelas terkait | Implementasi file terkait | Test Case (UC) | Test Case pendukung |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KF01 | - | UC01 | C04 ListingMakanan, C17 ListingController, C20 Validasi | `src/backend/api/listing_routes.py`; `src/backend/services/listing_service.py`; UI-06 | UC01-TC01, TC02, TC04 | test_listing, test_listing_validation, test_upload_foto; INT-TC02 |
| KF02 | - | UC02, UC03, UC09 | C04 ListingMakanan, C16 KatalogController, C17 ListingController | `src/backend/controllers/katalog_controller.py`; `src/backend/api/listing_routes.py`; UI-03/UI-06 | UC02-TC01–TC03; UC03-TC01–TC02; UC09-TC01–TC02 | test_listing, test_katalog_skenario_alternatif; INT-TC01–TC02 |
| KF03 | - | UC04 | C11 KatalogView, C16 KatalogController, C20 Validasi | `src/backend/controllers/katalog_controller.py`; `src/frontend/components/katalog/`; UI-03 | UC04-TC01–TC04 | test_katalog_skenario_alternatif; INT-TC01 |
| KF04 | KNF01 | UC05 | C06 Transaksi, C08 ItemTransaksi, C18 PembayaranController, C21 PaymentGatewayAdapter | `src/backend/controllers/pembayaran_controller.py`; `src/backend/api/pembayaran_routes.py`; UI-05 | UC05-TC01–TC02 | test_checkout, test_pembeli_checkout_unit, test_pembeli_pembayaran_unit, test_qris; INT-TC04–TC05; KNF01-TC01 |
| KF05 | - | UC06 | C04 ListingMakanan, C12 ListingView, C17 ListingController, C20 Validasi | `src/backend/api/listing_routes.py`; `src/backend/services/listing_service.py`; UI-06 | UC06-TC01–TC02 | test_listing, test_listing_validation, test_upload_foto; INT-TC02 |
| KF06 | KNF02 | UC07, UC08 | C01 Pengguna, C07 RewardLogin, C09 Kupon, C14 RewardView, C15 AuthController, C19 RewardController, C20 Validasi | `src/backend/routers/auth.py`; `src/backend/controllers/reward_controller.py`; UI-02/UI-04 | UC07-TC01–TC02; UC08-TC01–TC02 | test_reward_login, test_reward, test_pembeli_e2e_flow; INT-TC03/06; KNF02-TC01 (Fail terhadap spesifikasi SHA-256 saat transmisi) |
| KF07 | KNF02 | UC01, UC02, UC04, UC06, UC07, UC08 | C20 Validasi serta kelas terkait | `src/backend/validation.py`; `src/backend/schemas/`; `src/backend/services/listing_service.py` | Test validasi pada UC01, UC04, UC06, UC07, UC08 | test_listing_validation, test_listing, test_katalog_skenario_alternatif; KNF02-TC01 |

Tabel 5.2. Matriks Kerunutan KNF terhadap Pengujian

| ID KNF | Parameter | KF/UC terkait | Test Case | Status |
| :--- | :--- | :--- | :--- | :--- |
| KNF01 | Reliability | KF04 / UC05 | KNF01-TC01; uji rollback, bayar ganda, dan persaingan stok | Pass terbatas; belum ada simulasi putus jaringan eksplisit. |
| KNF02 | Security | KF06 / UC07, UC08 | KNF02-TC01 | Fail terhadap SKPL saat ini; implementasi menyimpan hash bcrypt, tetapi SHA-256 sebelum transmisi belum dilakukan. |
