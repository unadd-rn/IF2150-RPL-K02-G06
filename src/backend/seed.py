"""Script seeding basis data dev/demo.

Tidak ada argumen  : semai data hanya jika masih kosong (idempoten).
--reset / -r       : hapus seluruh isi katalog (listing) lalu semai ulang.
"""
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import bcrypt

# 1. Setup Path & Database
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.append(str(BACKEND_DIR))

try:
    from models import DATABASE_NAME, init_db
    init_db(DATABASE_NAME)
except ImportError:
    DATABASE_NAME = "savebite.db"

DB_PATH = BACKEND_DIR / DATABASE_NAME

# 2. Data akun yang disemai: (nama, email, peran, extra_data)
#    Penjual: (nama_toko, alamat_toko). Pembeli: (nama_akun,)
AKUN = [
    ("Penjual SaveBite", "penjual@test.com", "PENJUAL", ("Toko Roti Berkah", "Jl. Sudirman No. 45")),
    ("Pembeli E2E", "pembeli@test.com", "PEMBELI", ("pembelie2e",)),
    ("Kantin Sehat", "kantin@test.com", "PENJUAL", ("Kantin Kampus Sehat", "Jl. Ganesha No. 10")),
    ("Warung Bu Sari", "warung@test.com", "PENJUAL", ("Warung Makan Bu Sari", "Jl. Cikutra No. 88")),
]

# Foto yang pernah diunggah lewat /upload-foto; dipakai berputar agar kartu katalog memiliki gambar.
FOTO_TERSEDIA = [
    "uploads/listing/158ce285011340339adb5d310473c6ba.png",
    "uploads/listing/3ab3978c-6a4c-4bfa-9c0b-4e53ba87b3e6.jpg",
    "uploads/listing/409a0e236f8542a29aba237fa5599a80.png",
    "uploads/listing/40c48ffa800847798ce2f0a8fe818a14.png",
    "uploads/listing/5933eedf-022a-4b3e-9638-75d40ab20289.png",
    "uploads/listing/64d5be7870e240439b024bb202663a00.jpg",
    "uploads/listing/6840ea4b35dc4757b9e4a0a3660e2694.png",
    "uploads/listing/dfda96d63b1e429eb14e9b38f421e960.jpg",
]


def batas_kedaluwarsa(jam: int) -> str:
    """Batas kedaluwarsa `jam` jam dari sekarang, format datetime() SQLite."""
    return (datetime.now() + timedelta(hours=jam)).strftime("%Y-%m-%dT%H:%M:%S")


# 3. Data dummy katalog: (email_penjual, nama, deskripsi, porsi, kondisi, harga, stok, jam_kedaluwarsa)
LISTING_DUMMY = [
    ("penjual@test.com", "Roti Tawar Penyelamatan", "Roti tawar yang masih enak untuk disantap", "1 Pack", "Sangat Baik", 12000, 5, 72),
    ("penjual@test.com", "Nasi Goreng Spesial Late-Night", "Masih hangat dan siap dinikmati", "1 Porsi", "Hangat", 15000, 3, 8),
    ("penjual@test.com", "Croissant Chocolate", "Croissant cokelat buatan sendiri, tekstur masih renyah", "1 Buah", "Sangat Baik", 18000, 4, 24),
    ("penjual@test.com", "Donut Box Serenata", "Isi 6 donat campur rasa, masih lembut", "1 Box", "Baik", 25000, 2, 36),
    ("penjual@test.com", "Muffin Blueberry", "Muffin blueberry dengan topping buah asli", "1 Buah", "Sangat Baik", 10000, 6, 48),
    ("kantin@test.com", "Nasi Ayam Geprek", "Ayam geprek sambal bawang plus nasi hangat", "1 Porsi", "Hangat", 17000, 7, 6),
    ("kantin@test.com", "Paket Nasi Rames", "Nasi rames lauk ayam suwir dan sayur bening", "1 Porsi", "Hangat", 14000, 5, 10),
    ("kantin@test.com", "Sate Ayam Madang", "Sate ayam bumbu kacang, sepuluh tusuk", "10 Tusuk", "Baik", 20000, 4, 20),
    ("kantin@test.com", "Gado-Gado Segar", "Salad Indonesia dengan saus kacang segar", "1 Porsi", "Sangat Baik", 13000, 8, 24),
    ("warung@test.com", "Ayam Goreng Kremes", "Ayam goreng dengan kremes gurih melimpah", "1 Potong", "Hangat", 11000, 6, 12),
    ("warung@test.com", "Tempe & Tahu Bacem", "Tempe dan tahu bacem manis, dagingnya masih kenyal", "5 Potong", "Baik", 8000, 10, 48),
    ("warung@test.com", "Es Teh Manis Jumbo", "Es teh manis racikan warung, ukuran jumbo", "1 Gelas", "Sangat Baik", 5000, 12, 3),
]

# Fixture skenario alternatif DPPL: tidak tersedia karena stok habis,
# sudah kedaluwarsa, atau dinonaktifkan penjual.
LISTING_EDGE = [
    ("penjual@test.com", "Uji Stok Habis", "Listing uji dengan stok nol", "1 Porsi", "Baik", 9000, 0, 72, 1),
    ("kantin@test.com", "Uji Kedaluwarsa", "Listing uji yang sudah lewat batas waktu", "1 Porsi", "Baik", 11000, 4, -24, 1),
    ("warung@test.com", "Uji Listing Nonaktif", "Listing uji yang dinonaktifkan penjual", "1 Porsi", "Baik", 8000, 3, 72, 0),
]


def main(reset: bool) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Skema tabel (sama dengan models.CREATE_TABLES_SQL agar bisa dijalankan berdiri sendiri).
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS pengguna (
            id_pengguna INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS penjual (
            id_pengguna INTEGER PRIMARY KEY,
            nama_toko TEXT NOT NULL,
            alamat_toko TEXT NOT NULL,
            FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS pembeli (
            id_pengguna INTEGER PRIMARY KEY,
            nama_akun TEXT NOT NULL,
            FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS listing_makanan (
            id_listing INTEGER PRIMARY KEY AUTOINCREMENT,
            id_penjual INTEGER NOT NULL,
            nama_makanan TEXT NOT NULL,
            deskripsi TEXT,
            porsi TEXT NOT NULL,
            kondisi TEXT NOT NULL,
            foto TEXT,
            harga INTEGER NOT NULL CHECK (harga >= 0),
            stok INTEGER NOT NULL CHECK (stok >= 0),
            batas_kedaluwarsa DATETIME NOT NULL,
            aktif BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (id_penjual) REFERENCES penjual(id_pengguna) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS reward_login (
            id_reward INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pembeli INTEGER UNIQUE NOT NULL,
            poin_terkumpul INTEGER NOT NULL DEFAULT 0 CHECK (poin_terkumpul >= 0),
            tanggal_login_terakhir DATE,
            FOREIGN KEY (id_pembeli) REFERENCES pembeli(id_pengguna) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS auth_session (
            token TEXT PRIMARY KEY,
            id_pengguna INTEGER NOT NULL,
            dibuat_pada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            kedaluwarsa_pada DATETIME NOT NULL,
            FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna) ON DELETE CASCADE
        );
    """)

    # Hash password default untuk pengujian
    hashed = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        # 4. Reset katalog jika diminta (hapus semua listing; item terkait terhapus otomatis).
        if reset:
            cursor.execute("DELETE FROM listing_makanan;")
            print("✓ Katalog dikosongkan untuk disemai ulang.")

        # 5. Semai akun pengguna & perannya.
        # SETIAP akun PENJUAL disemai bersama data toko awalnya (nama_toko, alamat_toko),
        # yang tampil di katalog pembeli dan bisa diubah lewat halaman akun penjual.
        id_per_email = {}
        for nama, email, peran, extra in AKUN:
            cursor.execute("SELECT id_pengguna FROM pengguna WHERE email = ?", (email,))
            baris = cursor.fetchone()
            if baris:
                id_per_email[email] = baris[0]
                # Sehat diri: akun sudah ada tetapi baris toko/profilnya belum ada (idempoten).
                if peran == "PENJUAL" and not cursor.execute(
                    "SELECT 1 FROM penjual WHERE id_pengguna = ?", (baris[0],)
                ).fetchone():
                    nama_toko, alamat_toko = extra
                    cursor.execute(
                        "INSERT INTO penjual (id_pengguna, nama_toko, alamat_toko) VALUES (?, ?, ?)",
                        (baris[0], nama_toko, alamat_toko),
                    )
                    print(f"✓ Data toko awal untuk {email} dilengkapi.")
                elif peran == "PENJUAL":
                    nama_toko, alamat_toko = extra
                    toko = cursor.execute(
                        "SELECT nama_toko, alamat_toko FROM penjual WHERE id_pengguna = ?",
                        (baris[0],),
                    ).fetchone()
                    # Legacy DB guard: jika profil toko ada tapi kolomnya kosong, isi dengan nilai awal seed.
                    if toko and (not str(toko[0]).strip() or not str(toko[1]).strip()):
                        cursor.execute(
                            "UPDATE penjual SET nama_toko = ?, alamat_toko = ? WHERE id_pengguna = ?",
                            (nama_toko, alamat_toko, baris[0]),
                        )
                        print(f"✓ Data toko awal untuk {email} diperbaiki.")
                elif peran != "PENJUAL" and not cursor.execute(
                    "SELECT 1 FROM pembeli WHERE id_pengguna = ?", (baris[0],)
                ).fetchone():
                    (nama_akun,) = extra
                    cursor.execute(
                        "INSERT INTO pembeli (id_pengguna, nama_akun) VALUES (?, ?)",
                        (baris[0], nama_akun),
                    )
                    cursor.execute(
                        "INSERT INTO reward_login (id_pembeli, poin_terkumpul) VALUES (?, ?)",
                        (baris[0], 0),
                    )
                    print(f"✓ Data profil untuk {email} dilengkapi.")
                continue

            cursor.execute(
                "INSERT INTO pengguna (nama, email, password) VALUES (?, ?, ?)",
                (nama, email, hashed),
            )
            id_pengguna = cursor.lastrowid
            if peran == "PENJUAL":
                nama_toko, alamat_toko = extra
                cursor.execute(
                    "INSERT INTO penjual (id_pengguna, nama_toko, alamat_toko) VALUES (?, ?, ?)",
                    (id_pengguna, nama_toko, alamat_toko),
                )
            else:
                (nama_akun,) = extra
                cursor.execute(
                    "INSERT INTO pembeli (id_pengguna, nama_akun) VALUES (?, ?)",
                    (id_pengguna, nama_akun),
                )
                cursor.execute(
                    "INSERT INTO reward_login (id_pembeli, poin_terkumpul) VALUES (?, ?)",
                    (id_pengguna, 0),
                )
            id_per_email[email] = id_pengguna
            print(f"✓ Akun {email} berhasil dibuat.")

        # 6. Semai data dummy katalog (dilewati bila katalog sudah terisi).
        jumlah_listing = cursor.execute("SELECT COUNT(*) FROM listing_makanan").fetchone()[0]
        if jumlah_listing > 0:
            print(f"ℹ Katalog sudah berisi {jumlah_listing} listing; seeding katalog dilewati.")
        else:
            for i, (email, nama, deskripsi, porsi, kondisi, harga, stok, jam) in enumerate(LISTING_DUMMY):
                cursor.execute(
                    """
                    INSERT INTO listing_makanan
                        (id_penjual, nama_makanan, deskripsi, porsi, kondisi, foto,
                         harga, stok, batas_kedaluwarsa, aktif)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        id_per_email[email],
                        nama,
                        deskripsi,
                        porsi,
                        kondisi,
                        "/" + FOTO_TERSEDIA[i % len(FOTO_TERSEDIA)],
                        harga,
                        stok,
                        batas_kedaluwarsa(jam),
                    ),
                )
            print(f"✓ {len(LISTING_DUMMY)} listing dummy berhasil ditambahkan.")

        # Pastikan fixture edge case tersedia juga pada basis data yang sebelumnya
        # sudah berisi listing normal (seeding tetap idempoten).
        for i, (email, nama, deskripsi, porsi, kondisi, harga, stok, jam, aktif) in enumerate(LISTING_EDGE):
            id_penjual = id_per_email[email]
            sudah_ada = cursor.execute(
                "SELECT 1 FROM listing_makanan WHERE id_penjual = ? AND nama_makanan = ?",
                (id_penjual, nama),
            ).fetchone()
            if sudah_ada:
                continue
            cursor.execute(
                """
                INSERT INTO listing_makanan
                    (id_penjual, nama_makanan, deskripsi, porsi, kondisi, foto,
                     harga, stok, batas_kedaluwarsa, aktif)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_penjual, nama, deskripsi, porsi, kondisi,
                    "/" + FOTO_TERSEDIA[(len(LISTING_DUMMY) + i) % len(FOTO_TERSEDIA)],
                    harga, stok, batas_kedaluwarsa(jam), aktif,
                ),
            )
        print(f"✓ {len(LISTING_EDGE)} listing skenario alternatif tersedia.")

        # Akun demo pembeli perlu bisa langsung menguji klaim reward (100 poin).
        id_pembeli = id_per_email["pembeli@test.com"]
        cursor.execute(
            "INSERT OR IGNORE INTO reward_login (id_pembeli, poin_terkumpul) VALUES (?, 100)",
            (id_pembeli,),
        )
        cursor.execute(
            "UPDATE reward_login SET poin_terkumpul = CASE "
            "WHEN poin_terkumpul < 100 THEN 100 ELSE poin_terkumpul END "
            "WHERE id_pembeli = ?",
            (id_pembeli,),
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal menyemai data: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seeding basis data SaveBite")
    parser.add_argument("--reset", "-r", action="store_true", help="Hapus katalog lalu semai ulang")
    args = parser.parse_args()
    main(args.reset)
