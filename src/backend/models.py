import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List, Optional
import bcrypt
from pathlib import Path

DATABASE_NAME = str(Path(__file__).resolve().parent.parent / "savebite.db")

CREATE_TABLES_SQL = """
PRAGMA foreign_keys = ON;

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
    FOREIGN KEY (id_pengguna) REFERENCES pengguna (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pembeli (
    id_pengguna INTEGER PRIMARY KEY,
    nama_akun TEXT NOT NULL,
    FOREIGN KEY (id_pengguna) REFERENCES pengguna (id_pengguna) ON DELETE CASCADE
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
    draft BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (id_penjual) REFERENCES penjual (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pembeli INTEGER NOT NULL,
    tanggal DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    batas_waktu_bayar DATETIME NOT NULL,
    total_harga INTEGER NOT NULL DEFAULT 0 CHECK (total_harga >= 0),
    status TEXT NOT NULL CHECK (status IN ('MENUNGGU_BAYAR', 'LUNAS', 'BATAL')) DEFAULT 'MENUNGGU_BAYAR',
    kode_pengambilan TEXT,
    waktu_diambil DATETIME,
    token_bayar TEXT UNIQUE,
    kode_kupon TEXT,
    FOREIGN KEY (id_pembeli) REFERENCES pembeli (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS item_transaksi (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER NOT NULL,
    id_listing INTEGER NOT NULL,
    jumlah INTEGER NOT NULL CHECK (jumlah > 0),
    harga_satuan INTEGER NOT NULL CHECK (harga_satuan >= 0),
    FOREIGN KEY (id_transaksi) REFERENCES transaksi (id_transaksi) ON DELETE CASCADE,
    FOREIGN KEY (id_listing) REFERENCES listing_makanan (id_listing) ON DELETE CASCADE
);

-- Waktu pengambilan per penjual: satu transaksi bisa berisi item dari beberapa
-- toko (checkout campur), sehingga tiap toko menandai pengambilan secara mandiri
-- (transaksi.waktu_diambil hanya terisi saat SEMUA toko sudah menandai diambil).
CREATE TABLE IF NOT EXISTS pengambilan_penjual (
    id_transaksi INTEGER NOT NULL,
    id_penjual INTEGER NOT NULL,
    waktu_diambil DATETIME NOT NULL,
    PRIMARY KEY (id_transaksi, id_penjual),
    FOREIGN KEY (id_transaksi) REFERENCES transaksi (id_transaksi) ON DELETE CASCADE,
    FOREIGN KEY (id_penjual) REFERENCES penjual (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reward_login (
    id_reward INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pembeli INTEGER UNIQUE NOT NULL,
    poin_terkumpul INTEGER NOT NULL DEFAULT 0 CHECK (poin_terkumpul >= 0),
    tanggal_login_terakhir DATE,
    FOREIGN KEY (id_pembeli) REFERENCES pembeli (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS kupon (
    kode_kupon TEXT PRIMARY KEY,
    id_pembeli INTEGER NOT NULL,
    nilai_potongan INTEGER NOT NULL CHECK (nilai_potongan >= 0),
    berlaku_sampai DATE NOT NULL,
    terpakai BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (id_pembeli) REFERENCES pembeli (id_pengguna) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS auth_session (
    token TEXT PRIMARY KEY,
    id_pengguna INTEGER NOT NULL,
    dibuat_pada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    kedaluwarsa_pada DATETIME NOT NULL,
    FOREIGN KEY (id_pengguna) REFERENCES pengguna (id_pengguna) ON DELETE CASCADE
);
"""

def init_db(db_path: str = DATABASE_NAME):
    """Menginisialisasi basis data SQLite dan membuat seluruh tabel."""
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(CREATE_TABLES_SQL)
        # Migrasi ringan untuk basis data lama: tambahkan kolom waktu_diambil
        # pada transaksi jika belum ada (basis data lama dibuat sebelum kolom ini).
        kolom = [baris[1] for baris in conn.execute("PRAGMA table_info(transaksi)").fetchall()]
        if "waktu_diambil" not in kolom:
            conn.execute("ALTER TABLE transaksi ADD COLUMN waktu_diambil DATETIME")
        kolom_listing = [baris[1] for baris in conn.execute("PRAGMA table_info(listing_makanan)").fetchall()]
        if "draft" not in kolom_listing:
            conn.execute("ALTER TABLE listing_makanan ADD COLUMN draft BOOLEAN NOT NULL DEFAULT 0")
        kolom_transaksi = [baris[1] for baris in conn.execute("PRAGMA table_info(transaksi)").fetchall()]
        if "token_bayar" not in kolom_transaksi:
            conn.execute("ALTER TABLE transaksi ADD COLUMN token_bayar TEXT")
        if "kode_kupon" not in kolom_transaksi:
            conn.execute("ALTER TABLE transaksi ADD COLUMN kode_kupon TEXT")
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_transaksi_token_bayar "
            "ON transaksi(token_bayar)"
        )
        conn.commit()

@dataclass
class Pengguna:
    def __init__(self, id_pengguna: int, nama: str, email: str, password_hash: str):
        self.__idPengguna = id_pengguna 
        self.__nama = nama 
        self.__email = email 
        self.__password = password_hash 

    @staticmethod
    def hash_password(password_plain: str) -> str:
        """Menghasilkan hash bcrypt untuk kata sandi baru sebelum disimpan ke basis data"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_plain.encode('utf-8'), salt).decode('utf-8')

    def verifikasiPassword(self, password: str) -> bool:
        """Mengecek apakah password yang didapat saat login sama dengan hash bcrypt di atribut password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.__password.encode('utf-8'))

    def getPeran(self) -> str:
        """Operasi abstrak untuk mengembalikan peran pengguna"""
        raise NotImplementedError("Metode ini harus diimplementasikan oleh kelas turunan (Penjual/Pembeli)")

    def bukaListing(self):
        """Mengambil listing milik pengguna penjual"""
        pass

@dataclass
class Penjual(Pengguna):
    nama_toko: str = ""
    alamat_toko: str = ""

    def get_peran(self) -> str:
        return "PENJUAL"

    def memiliki_listing(self, id_penjual_listing: int) -> bool:
        return self.id_pengguna == id_penjual_listing

@dataclass
class Pembeli(Pengguna):
    nama_akun: str = ""

    def get_peran(self) -> str:
        return "PEMBELI"

@dataclass
class ListingMakanan:
    id_listing: Optional[int]
    id_penjual: int
    nama_makanan: str
    porsi: str
    kondisi: str
    harga: int
    stok: int
    batas_kedaluwarsa: str
    deskripsi: Optional[str] = None
    foto: Optional[str] = None
    aktif: bool = True
    draft: bool = False

    # Satu-satunya definisi kriteria "tersedia" di level query (UC02, UC04):
    # aktif, stok > 0, dan belum melewati batas kedaluwarsa.
    # datetime() menyamakan format "YYYY-MM-DD HH:MM:SS" dan "YYYY-MM-DDTHH:MM:SS".
    KONDISI_TERSEDIA: ClassVar[str] = (
        "aktif = 1 AND draft = 0 AND stok > 0 "
        "AND datetime(batas_kedaluwarsa) > datetime(:waktu)"
    )

    def is_tersedia(self, waktu_sekarang=None) -> bool:
        """Kriteria yang sama dengan KONDISI_TERSEDIA, untuk mengecek satu objek (UC03, UC05).
        waktu_sekarang boleh str ISO, datetime, atau None (= sekarang)."""
        waktu = self._ke_datetime(waktu_sekarang or datetime.now())
        return (
            bool(self.aktif)
            and not bool(self.draft)
            and self.stok > 0
            and waktu < self._ke_datetime(self.batas_kedaluwarsa)
        )

    @staticmethod
    def _ke_datetime(nilai) -> datetime:
        # fromisoformat menerima "YYYY-MM-DD HH:MM:SS" maupun "YYYY-MM-DDTHH:MM:SS"
        return nilai if isinstance(nilai, datetime) else datetime.fromisoformat(nilai)

    @staticmethod
    def _waktu_sekarang() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def cariById(cls, conn: sqlite3.Connection, id_listing: int) -> Optional["ListingMakanan"]:
        """Mengambil satu listing berdasarkan id (Q-C04-01). None jika tidak ada."""
        cursor = conn.execute(
            "SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok, "
            "batas_kedaluwarsa, deskripsi, foto, aktif, draft "
            "FROM listing_makanan WHERE id_listing = ?",
            (id_listing,),
        )
        baris = cursor.fetchone()
        if baris is None:
            return None
        return cls._dari_baris([d[0] for d in cursor.description], tuple(baris))

    @classmethod
    def _dari_baris(cls, kolom: List[str], baris: tuple) -> "ListingMakanan":
        data = dict(zip(kolom, baris))
        data["aktif"] = bool(data["aktif"])
        return cls(**data)

    @classmethod
    def ambilSemuaTersedia(
        cls, conn: sqlite3.Connection, waktu: Optional[str] = None
    ) -> List["ListingMakanan"]:
        """Mengambil seluruh listing yang aktif, berstok > 0, dan belum kedaluwarsa (UC02)."""
        return cls.cariDaftar(conn, waktu=waktu)

    @classmethod
    def cariDaftar(
        cls,
        conn: sqlite3.Connection,
        kata_kunci: Optional[str] = None,
        harga_min: Optional[int] = None,
        harga_maks: Optional[int] = None,
        waktu: Optional[str] = None,
    ) -> List["ListingMakanan"]:
        """Mengambil listing tersedia yang namanya memuat kata kunci dan harganya
        berada dalam rentang (UC04). Parameter None berarti filter tidak dipakai."""
        kata_kunci = kata_kunci.strip() if kata_kunci else None
        pola = None
        if kata_kunci:
            # Escape karakter wildcard LIKE agar input pengguna dicari apa adanya
            pola = "%" + kata_kunci.lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"

        query = (
            "SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok, "
            "batas_kedaluwarsa, deskripsi, foto, aktif, draft "
            "FROM listing_makanan "
            f"WHERE {cls.KONDISI_TERSEDIA} "
            "AND (:pola IS NULL OR LOWER(nama_makanan) LIKE :pola ESCAPE '\\') "
            "AND (:harga_min IS NULL OR harga >= :harga_min) "
            "AND (:harga_maks IS NULL OR harga <= :harga_maks) "
            "ORDER BY datetime(batas_kedaluwarsa) ASC"
        )
        cursor = conn.execute(
            query,
            {
                "waktu": waktu or cls._waktu_sekarang(),
                "pola": pola,
                "harga_min": harga_min,
                "harga_maks": harga_maks,
            },
        )
        kolom = [d[0] for d in cursor.description]
        return [cls._dari_baris(kolom, baris) for baris in cursor.fetchall()]

@dataclass
class Transaksi:
    id_transaksi: Optional[int]
    id_pembeli: int
    tanggal: str
    batas_waktu_bayar: str
    total_harga: int = 0
    status: str = "MENUNGGU_BAYAR"
    kode_pengambilan: Optional[str] = None
    waktu_diambil: Optional[str] = None
    token_bayar: Optional[str] = None
    kode_kupon: Optional[str] = None

@dataclass
class ItemTransaksi:
    id_item: Optional[int]
    id_transaksi: int
    id_listing: int
    jumlah: int
    harga_satuan: int

    def hitung_subtotal(self) -> int:
        return self.jumlah * self.harga_satuan

@dataclass
class RewardLogin:
    """C07 RewardLogin: poin login harian milik Pembeli (UC07, UC08)."""
    id_reward: Optional[int]
    id_pembeli: int
    poin_terkumpul: int = 0
    tanggal_login_terakhir: Optional[str] = None
    POIN_PER_LOGIN: ClassVar[int] = 10
    POIN_PER_KLAIM: ClassVar[int] = 100

    def catatLogin(self, tanggal: str) -> bool:
        """Algo-C07-01: tambah poin jika belum login pada tanggal ini."""
        if self.tanggal_login_terakhir is not None and self.tanggal_login_terakhir == tanggal:
            return False  # sudah login hari ini, poin tidak ditambah
        self.poin_terkumpul += self.POIN_PER_LOGIN
        self.tanggal_login_terakhir = tanggal
        return True

    def cukupUntukKlaim(self) -> bool:
        """Algo-C07-02"""
        return self.poin_terkumpul >= self.POIN_PER_KLAIM

    def kurangiPoin(self, jumlah: int) -> None:
        """Algo-C07-03"""
        if jumlah <= 0 or jumlah > self.poin_terkumpul:
            raise ValueError("Poin tidak mencukupi")
        self.poin_terkumpul -= jumlah

    @classmethod
    def cariByPembeli(cls, conn: sqlite3.Connection, id_pembeli: int) -> Optional["RewardLogin"]:
        """Q-C19-01: ambil RewardLogin milik Pembeli. None jika tidak ada."""
        baris = conn.execute(
            "SELECT id_reward, id_pembeli, poin_terkumpul, tanggal_login_terakhir "
            "FROM reward_login WHERE id_pembeli = ?",
            (id_pembeli,),
        ).fetchone()
        return None if baris is None else cls(*baris)

@dataclass
class Kupon:
    kode_kupon: str
    id_pembeli: int
    nilai_potongan: int
    berlaku_sampai: str
    terpakai: bool = False

    def is_berlaku(self, tanggal_sekarang: str) -> bool:
        return not self.terpakai and tanggal_sekarang <= self.berlaku_sampai
    
    def simpan(self, conn: sqlite3.Connection) -> None:
        """Q-C19-04: simpan kupon baru hasil klaim reward."""
        conn.execute(
            "INSERT INTO kupon (kode_kupon, id_pembeli, nilai_potongan, berlaku_sampai, terpakai) "
            "VALUES (?, ?, ?, ?, 0)",
            (self.kode_kupon, self.id_pembeli, self.nilai_potongan, self.berlaku_sampai),
        )

    @classmethod
    def cariByPembeli(cls, conn: sqlite3.Connection, id_pembeli: int) -> List["Kupon"]:
        """Daftar kupon milik Pembeli, berlaku paling lama lebih dulu."""
        rows = conn.execute(
            "SELECT kode_kupon, id_pembeli, nilai_potongan, berlaku_sampai, terpakai "
            "FROM kupon WHERE id_pembeli = ? ORDER BY berlaku_sampai DESC, kode_kupon",
            (id_pembeli,),
        ).fetchall()
        return [cls(r[0], r[1], r[2], r[3], bool(r[4])) for r in rows]

    @classmethod
    def carikanByKode(cls, conn: sqlite3.Connection, kode_kupon: str) -> Optional["Kupon"]:
        """Ambil satu kupon berdasarkan kodenya (Q-C19-05). None jika tidak ada."""
        baris = conn.execute(
            "SELECT kode_kupon, id_pembeli, nilai_potongan, berlaku_sampai, terpakai "
            "FROM kupon WHERE kode_kupon = ?",
            (kode_kupon,),
        ).fetchone()
        return None if baris is None else cls(baris[0], baris[1], baris[2], baris[3], bool(baris[4]))
