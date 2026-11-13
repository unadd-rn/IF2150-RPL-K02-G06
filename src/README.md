# SaveBite

SaveBite adalah aplikasi web untuk mengurangi limbah makanan. **Penjual** (toko roti, kantin, warung) memasang makanan berlebih yang masih layak konsumsi dengan harga lebih murah dan batas waktu kedaluwarsa. **Pembeli** menelusuri katalog, memasukkan makanan ke keranjang, membayar melalui QRIS (simulasi), lalu mengambil pesanan di toko dengan kode pengambilan. Pembeli juga mendapat poin dari login harian yang dapat ditukar dengan kupon.

Dikerjakan oleh Kelompok G06, Kelas K02, IF2150 Rekayasa Perangkat Lunak.

---

## 1. Teknologi

| Lapisan | Teknologi | Versi |
| :--- | :--- | :--- |
| Bahasa backend | Python | 3.12 (minimal 3.10) |
| Framework backend | FastAPI + Uvicorn | FastAPI ≥ 0.110, Uvicorn ≥ 0.28 |
| Validasi data | Pydantic | ≥ 2.6 |
| Hash password | bcrypt | 4.1.2 |
| QR code | qrcode[pil] | ≥ 7.4 |
| Test backend | pytest + httpx | pytest ≥ 8.0 |
| Runtime frontend | Node.js | 22 |
| Framework frontend | Next.js (App Router) + React | Next.js 16.4.4, React 19.3.0 |
| Bahasa frontend | TypeScript | 5 |
| Styling | Tailwind CSS | 4 |
| Test frontend (E2E) | Playwright | ≥ 1.64 |
| Basis data | SQLite | bawaan Python (`sqlite3`), tidak perlu instalasi terpisah |

Daftar lengkap dependensi ada di [backend/requirements.txt](backend/requirements.txt) dan [frontend/package.json](frontend/package.json) (versi terkunci di `frontend/package-lock.json`). Versi Python dan Node di atas sama dengan yang dipakai CI ([.github/workflows/ci.yml](../.github/workflows/ci.yml)).

Arsitektur: client-server. Frontend Next.js (port 3000) meneruskan seluruh request `/api/*` ke backend FastAPI (port 8000) melalui *rewrite* di [frontend/next.config.ts](frontend/next.config.ts), sehingga cookie sesi tetap *same-origin*. Backend memakai pola MVC berlapis: `routers/`, `api/`, `controllers/` (C), `schemas/` + `models.py` (M), dan halaman/komponen Next.js (V).

---

## 2. Prasyarat dan Instalasi

Software yang harus terpasang:

- **Python 3.12**
- **Node.js 22** beserta npm
- Git

Langkah instalasi (dari root repo):

```bash
git clone https://github.com/unadd-rn/IF2150-RPL-K02-G06.git
cd IF2150-RPL-K02-G06/src
```

**Backend**

```bash
# Buat dan aktifkan virtual environment
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (Git Bash):    source .venv/Scripts/activate
# macOS / Linux:         source .venv/bin/activate

pip install -r backend/requirements.txt
```

**Frontend**

```bash
cd frontend
npm ci
cd ..
```

---

## 3. Konfigurasi

### 3.1 Environment variable

Aplikasi **dapat dijalankan tanpa mengatur environment variable apa pun**; semua variabel punya nilai bawaan untuk lingkungan lokal. Daftar variabel ada di [.env.example](.env.example):

| Variabel | Dipakai oleh | Bawaan | Kegunaan |
| :--- | :--- | :--- | :--- |
| `SAVEBITE_PUBLIC_WEB_URL` | Backend | `http://localhost:3000` | Alamat frontend yang ditanam di QR pembayaran. Ganti dengan IP LAN komputer (mis. `http://192.168.1.10:3000`) jika QR ingin dipindai dari HP. |
| `NEXT_PUBLIC_API_URL` | Frontend | `http://localhost:8000` | Alamat backend, dipakai untuk memuat foto listing. |

Cara mengatur jika perlu:

- **Backend** tidak membaca file `.env` secara otomatis. Set variabel di terminal sebelum menjalankan backend, misalnya `export SAVEBITE_PUBLIC_WEB_URL=http://192.168.1.10:3000` (bash) atau `$env:SAVEBITE_PUBLIC_WEB_URL="http://192.168.1.10:3000"` (PowerShell).
- **Frontend**: salin baris `NEXT_PUBLIC_API_URL` ke file `frontend/.env.local`. Next.js membacanya otomatis.

File `.env` dan `.env.local` sudah masuk `.gitignore`; jangan di-commit.

### 3.2 Basis data dan seed

Basis data berupa satu file SQLite, `src/savebite.db`, yang **dibuat otomatis**. Tidak ada server basis data yang perlu dipasang.

- Tabel dibuat (dan dimigrasi ringan, mis. penambahan kolom baru) oleh `init_db()` di [backend/models.py](backend/models.py) setiap kali backend dijalankan.
- Akun uji dan data katalog contoh diisi oleh skrip seed:
| *10-11-2026* | *Cendra Asih Chairunnisa* | *setup reward* | *3* | *Done* | *-* |
```bash
cd backend
python seed.py          # isi data jika masih kosong (aman dijalankan berulang kali)
python seed.py --reset  # kosongkan seluruh listing lalu semai ulang katalog
cd ..
```

> **Pengguna Windows:** skrip seed mencetak simbol Unicode (✓, ℹ). Jika muncul `UnicodeEncodeError: 'charmap' codec ...`, jalankan dengan mode UTF-8:
> PowerShell: `$env:PYTHONUTF8=1; python seed.py` · Git Bash: `PYTHONUTF8=1 python seed.py`

Seed bersifat idempoten: akun yang sudah ada tidak diduplikasi, dan katalog hanya diisi jika masih kosong. Selain 12 listing contoh, seed juga membuat 3 listing untuk skenario alternatif (stok habis, sudah kedaluwarsa, dan nonaktif) yang **tidak** akan tampil di katalog pembeli.

Untuk mulai dari basis data kosong, hapus `src/savebite.db` lalu jalankan `python seed.py` lagi.

---

## 4. Menjalankan Aplikasi

Jalankan backend dan frontend di **dua terminal terpisah**.

**Terminal 1: backend** (dari folder `src/`, dengan venv aktif)

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend berjalan di http://localhost:8000. Dokumentasi API interaktif (Swagger) tersedia di http://localhost:8000/docs.

**Terminal 2: frontend** (dari folder `src/frontend/`)

```bash
npm run dev
```

Buka http://localhost:3000, lalu login memakai salah satu akun di [Bagian 5](#5-akun-uji).

Urutan singkat dari nol:

```bash
cd src
python -m venv .venv && source .venv/bin/activate   # sesuaikan dengan OS
pip install -r backend/requirements.txt
(cd backend && python seed.py)
uvicorn backend.main:app --reload --port 8000        # terminal 1
cd frontend && npm ci && npm run dev                 # terminal 2
```

### 4.1 Menjalankan test

**Backend** (pytest, 76 test unit dan integrasi; memakai basis data sementara sehingga tidak mengubah `savebite.db`):

```bash
cd backend
python -m pytest
```

**Frontend** (Playwright E2E, lint, dan build):

```bash
cd frontend
npx playwright install chromium   # sekali saja, mengunduh browser untuk test
npm test                          # menyalakan dev server otomatis di 127.0.0.1:3000
npm run lint
npm run build
```

Test E2E login sebagai akun uji, jadi pastikan **backend sudah berjalan** dan **seed sudah dijalankan** sebelum `npm test`.

Kedua rangkaian test ini juga dijalankan otomatis oleh GitHub Actions pada setiap push/PR ke branch `Development`.

---

## 5. Akun Uji

Semua akun dibuat oleh `python seed.py` dan memakai password yang sama: **`password123`**. Seluruh data bersifat fiktif.

| Peran | Email | Nama / Toko | Keterangan |
| :--- | :--- | :--- | :--- |
| Pembeli | `pembeli@test.com` | Pembeli E2E | Katalog, keranjang, pembayaran QRIS, reward dan kupon |
| Penjual | `penjual@test.com` | Toko Roti Berkah | Kelola listing, pesanan masuk, konfirmasi pengambilan, profil toko |
| Penjual | `kantin@test.com` | Kantin Kampus Sehat | Penjual kedua (listing berbeda) |
| Penjual | `warung@test.com` | Warung Makan Bu Sari | Penjual ketiga (listing berbeda) |

Setelah login, pembeli diarahkan ke halaman katalog dan penjual ke dasbor penjual (`/penjual`). Halaman tiap peran dilindungi: pembeli tidak bisa membuka halaman penjual, dan sebaliknya.

**Mencoba reward:** setiap login pertama dalam satu hari menambah 10 poin; kupon dapat diklaim setelah poin mencapai 100.

**Mencoba pembayaran:** QRIS bersifat simulasi. Setelah checkout, pindai QR yang muncul (atau tekan tombol lanjut di halaman pembayaran) untuk menandai transaksi sebagai lunas.

---

## 6. Modul dan Pembagian Anggota

| NIM | Nama | Modul / Fitur | Use Case | Lokasi utama |
| :--- | :--- | :--- | :--- | :--- |
| 13525041 | Renata Puspanegara Ninagan | Fondasi sistem dan Login: model basis data, autentikasi bcrypt + sesi cookie, *role guard* pembeli/penjual, navbar | UC07 | `backend/models.py`, `backend/routers/auth.py`, `frontend/app/login/`, `frontend/middleware.ts`, `frontend/components/bottom-navbar.tsx` |
| 13525122 | Nadia Aulia Syafarani | Pengelolaan Listing Penjual: tambah, ubah, hapus (*soft delete*), simpan draf, unggah foto; pesanan masuk dan konfirmasi pengambilan; profil toko | UC01, UC06, UC09 | `backend/api/listing_routes.py`, `backend/api/penjualan_routes.py`, `backend/api/toko_routes.py`, `backend/validation.py`, `frontend/app/penjual/` |
| 13525119 | Ghina Emelia Yantes | Katalog Pembeli: daftar listing, detail listing, pencarian, filter harga | UC02, UC03, UC04 | `backend/controllers/katalog_controller.py`, `frontend/app/katalog/`, `frontend/components/katalog/` |
| 13525089 | Sherin Felicia Danessa | Pembayaran: keranjang, *checkout* multi-item, QRIS *dummy*, pengurangan stok secara atomik | UC05 | `backend/controllers/pembayaran_controller.py`, `backend/api/pembayaran_routes.py`, `backend/adapters/`, `frontend/app/cart/`, `frontend/app/pembayaran/` |
| 13525017 | Cendra Asih Chairunnisa | Reward login dan klaim kupon; seed data; integrasi dan QA | UC08 | `backend/controllers/reward_controller.py`, `backend/seed.py`, `frontend/app/reward/` |

Ringkasan endpoint API (detail lengkap di http://localhost:8000/docs):

| Prefix | Fitur |
| :--- | :--- |
| `/api/auth` | Login, logout |
| `/api/katalog` | Daftar dan detail listing untuk pembeli |
| `/api/listing` | CRUD listing penjual, unggah foto |
| `/api/penjualan` | Pesanan terbayar dan konfirmasi pengambilan |
| `/api/toko` | Profil toko penjual |
| `/api/pembayaran` | Checkout, status transaksi, pembayaran QRIS |
| `/api/reward` | Progres poin, klaim kupon |

---

## 7. Tabel Basis Data

Skema lengkap (SQL) didefinisikan di `CREATE_TABLES_SQL` pada [backend/models.py](backend/models.py). Semua tabel memakai `PRAGMA foreign_keys = ON`.

**`pengguna`** — akun dasar untuk semua peran

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_pengguna` | INTEGER | PK, autoincrement |
| `nama` | TEXT | wajib |
| `email` | TEXT | wajib, unik |
| `password` | TEXT | wajib, hash bcrypt |

**`penjual`** — data tambahan untuk peran Penjual

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_pengguna` | INTEGER | PK, FK → `pengguna` |
| `nama_toko` | TEXT | wajib |
| `alamat_toko` | TEXT | wajib |

**`pembeli`** — data tambahan untuk peran Pembeli

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_pengguna` | INTEGER | PK, FK → `pengguna` |
| `nama_akun` | TEXT | wajib |

**`listing_makanan`** — makanan yang dijual penjual

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_listing` | INTEGER | PK, autoincrement |
| `id_penjual` | INTEGER | FK → `penjual` |
| `nama_makanan` | TEXT | wajib |
| `deskripsi` | TEXT | opsional |
| `porsi` | TEXT | wajib |
| `kondisi` | TEXT | wajib |
| `foto` | TEXT | path relatif, mis. `uploads/listing/<uuid>.jpg` |
| `harga` | INTEGER | ≥ 0 |
| `stok` | INTEGER | ≥ 0 |
| `batas_kedaluwarsa` | DATETIME | wajib |
| `aktif` | BOOLEAN | bawaan 1; 0 = dihapus (*soft delete*) / nonaktif |
| `draft` | BOOLEAN | bawaan 0; 1 = belum ditampilkan di katalog |

**`transaksi`** — satu pesanan pembeli

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_transaksi` | INTEGER | PK, autoincrement |
| `id_pembeli` | INTEGER | FK → `pembeli` |
| `tanggal` | DATETIME | bawaan waktu sekarang |
| `batas_waktu_bayar` | DATETIME | wajib |
| `total_harga` | INTEGER | ≥ 0 |
| `status` | TEXT | `MENUNGGU_BAYAR` / `LUNAS` / `BATAL` |
| `kode_pengambilan` | TEXT | diisi setelah lunas |
| `waktu_diambil` | DATETIME | diisi saat penjual mengonfirmasi pengambilan |
| `token_bayar` | TEXT | unik, token di QR pembayaran |

**`item_transaksi`** — baris item dalam satu transaksi

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_item` | INTEGER | PK, autoincrement |
| `id_transaksi` | INTEGER | FK → `transaksi` |
| `id_listing` | INTEGER | FK → `listing_makanan` |
| `jumlah` | INTEGER | > 0 |
| `harga_satuan` | INTEGER | ≥ 0, harga saat checkout |

**`reward_login`** — poin login harian pembeli

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `id_reward` | INTEGER | PK, autoincrement |
| `id_pembeli` | INTEGER | FK → `pembeli`, unik |
| `poin_terkumpul` | INTEGER | ≥ 0 |
| `tanggal_login_terakhir` | DATE | opsional |

**`kupon`** — kupon hasil klaim reward

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `kode_kupon` | TEXT | PK |
| `id_pembeli` | INTEGER | FK → `pembeli` |
| `nilai_potongan` | INTEGER | ≥ 0, nominal rupiah |
| `berlaku_sampai` | DATE | wajib |
| `terpakai` | BOOLEAN | bawaan 0 |

**`auth_session`** — sesi login (token cookie)

| Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| `token` | TEXT | PK |
| `id_pengguna` | INTEGER | FK → `pengguna` |
| `dibuat_pada` | DATETIME | bawaan waktu sekarang |
| `kedaluwarsa_pada` | DATETIME | wajib |

Relasi utama: `pengguna` 1–1 `penjual`/`pembeli`; `penjual` 1–* `listing_makanan`; `pembeli` 1–* `transaksi`; `transaksi` 1–* `item_transaksi` *–1 `listing_makanan`; `pembeli` 1–1 `reward_login`; `pembeli` 1–* `kupon`; `pengguna` 1–* `auth_session`. Seluruh FK memakai `ON DELETE CASCADE`.

---

## 8. Struktur Folder

```
src/
├── README.md
├── .env.example
├── backend/
│   ├── main.py              # entry point FastAPI, registrasi router
│   ├── models.py            # skema SQLite + kelas domain
│   ├── seed.py              # data uji
│   ├── validation.py        # validasi input listing (C20)
│   ├── routers/ api/ controllers/   # route & controller
│   ├── schemas/             # model Pydantic request/response
│   ├── adapters/            # PaymentGatewayAdapter, metode pembayaran
│   ├── uploads/listing/     # foto listing
│   └── tests/               # test pytest
└── frontend/
    ├── app/                 # halaman Next.js (login, katalog, cart, pembayaran, reward, penjual)
    ├── components/          # komponen UI
    ├── lib/                 # klien API, state keranjang
    ├── middleware.ts        # role guard halaman
    └── tests/e2e/           # test Playwright
```
