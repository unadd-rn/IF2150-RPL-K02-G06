"""Pengujian endpoint /api/penjualan — daftar pesanan terbayar milik penjual
dan penandaan 'Sudah diambil / Selesai' (pengambilan di tempat)."""
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models import init_db
from backend.api.penjualan_routes import get_conn
from backend.routers.auth import get_current_user


@pytest.fixture
def penjualan_db(tmp_path):
    """Basis data uji: 1 penjual, 1 pembeli, 2 listing, dan 3 transaksi
    (LUNAS / MENUNGGU_BAYAR / BATAL) dari pembeli yang sama."""
    path = str(tmp_path / "test.db")
    init_db(path)
    c = sqlite3.connect(path)
    c.executescript("""
        INSERT INTO pengguna (id_pengguna, nama, email, password)
            VALUES (1, 'Penjual', 'p@t.com', 'x'), (2, 'Pembeli', 'b@t.com', 'x');
        INSERT INTO penjual VALUES (1, 'Toko', 'Jl. A');
        INSERT INTO pembeli VALUES (2, 'akun');
        INSERT INTO listing_makanan
            (id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok, batas_kedaluwarsa, aktif)
            VALUES (1, 1, 'Roti', '1 pack', 'Baik', 12000, 5, '2999-12-31 23:59:59', 1),
                   (2, 1, 'Nasi', '1 porsi', 'Hangat', 15000, 1, '2999-12-31 23:59:59', 1);
        INSERT INTO transaksi (id_transaksi, id_pembeli, tanggal, batas_waktu_bayar, total_harga, status, kode_pengambilan)
            VALUES (1, 2, '2026-11-09 10:00:00', '2999-01-01 00:00:00', 24000, 'LUNAS', 'SB-AAAAAA'),
                   (2, 2, '2026-11-09 10:05:00', '2999-01-01 00:00:00', 15000, 'MENUNGGU_BAYAR', NULL),
                   (3, 2, '2026-11-09 10:06:00', '2999-01-01 00:00:00', 15000, 'BATAL', NULL);
        INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan)
            VALUES (1, 1, 2, 12000), (2, 2, 1, 15000), (3, 2, 1, 15000);
    """)
    c.commit()
    c.close()
    return path


@pytest.fixture
def client_penjual(penjualan_db):
    """API client termasuk sebagai penjual (id 1), mengarah ke basis data uji."""
    def _conn():
        conn = sqlite3.connect(penjualan_db, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_conn] = _conn
    app.dependency_overrides[get_current_user] = lambda: {
        "id_pengguna": 1, "nama": "Penjual", "email": "p@t.com", "peran": "PENJUAL"}
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_hanya_menampilkan_pesanan_lunas(client_penjual):
    """Produk hanya muncul di halaman penjual ketika pembeli SUDAH membayar:
    MENUNGGU_BAYAR dan BATAL tidak ikut, LUNAS tampil beserta itemnya."""
    data = client_penjual.get("/api/penjualan/pesanan").json()
    assert [p["id_transaksi"] for p in data] == [1]
    p = data[0]
    assert p["kode_pengambilan"] == "SB-AAAAAA"
    assert p["waktu_diambil"] is None
    assert p["subtotal"] == 24000
    assert [(i["nama_makanan"], i["jumlah"]) for i in p["items"]] == [("Roti", 2)]


def test_tandai_sudah_diambil_lalu_selesai(client_penjual):
    """Penjual menandai 'Sudah diambil / Selesai' → waktu_diambil terisi dan
    pesanan tidak dapat ditandai dua kali."""
    res = client_penjual.post("/api/penjualan/1/ambil")
    assert res.status_code == 200
    assert res.json()["waktu_diambil"] is not None

    data = client_penjual.get("/api/penjualan/pesanan").json()
    assert data[0]["waktu_diambil"] is not None

    res = client_penjual.post("/api/penjualan/1/ambil")
    assert res.status_code == 409


def test_tidak_lunas_tidak_bisa_ditandai(client_penjual):
    assert client_penjual.post("/api/penjualan/2/ambil").status_code == 409
    assert client_penjual.post("/api/penjualan/3/ambil").status_code == 409


def test_transaksi_tak_atau_milik_penjual_lain(client_penjual):
    assert client_penjual.post("/api/penjualan/99/ambil").status_code == 404


def test_subtotal_hanya_item_milik_penjual_terkait(tmp_path):
    """Satu transaksi checkout campur dua toko: tiap penjual melihat transaksi
    yang sama, tetapi hanya item listing miliknya yang ditampilkan, dan
    subtotal hanya item milik penjual itu (bukan total seluruh transaksi)."""
    path = str(tmp_path / "test.db")
    init_db(path)
    c = sqlite3.connect(path)
    c.executescript("""
        INSERT INTO pengguna (id_pengguna, nama, email, password)
            VALUES (1, 'Penjual', 'p@t.com', 'x'), (2, 'Pembeli', 'b@t.com', 'x'),
                   (3, 'Penjual Lain', 'pl@t.com', 'x');
        INSERT INTO penjual VALUES (1, 'Toko A', 'Jl. A'), (3, 'Toko B', 'Jl. B');
        INSERT INTO pembeli VALUES (2, 'akun');
        INSERT INTO listing_makanan
            (id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok, batas_kedaluwarsa, aktif)
            VALUES (1, 1, 'Roti', '1 pack', 'Baik', 12000, 5, '2999-12-31 23:59:59', 1),
                   (2, 3, 'Bubur', '1 porsi', 'Hangat', 10000, 3, '2999-12-31 23:59:59', 1);
        INSERT INTO transaksi (id_transaksi, id_pembeli, tanggal, batas_waktu_bayar, total_harga, status)
            VALUES (1, 2, '2026-11-09 10:00:00', '2999-01-01 00:00:00', 22000, 'LUNAS');
        INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan)
            VALUES (1, 1, 1, 12000), (1, 2, 1, 10000);
    """)
    c.commit()
    c.close()

    def _conn():
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn

    app.dependency_overrides[get_conn] = _conn

    def _penjual(id_pengguna, nama):
        return lambda: {"id_pengguna": id_pengguna, "nama": nama, "peran": "PENJUAL"}

    # Penjual Lain (id 3): melihat transaksi 1, tapi hanya item Bubur miliknya
    app.dependency_overrides[get_current_user] = _penjual(3, "Penjual Lain")
    data = TestClient(app).get("/api/penjualan/pesanan").json()
    assert [p["id_transaksi"] for p in data] == [1]
    assert [(i["nama_makanan"], i["jumlah"]) for i in data[0]["items"]] == [("Bubur", 1)]
    assert data[0]["subtotal"] == 10000

    # Penjual (id 1): transaksi yang sama, hanya item Roti miliknya
    app.dependency_overrides[get_current_user] = _penjual(1, "Penjual")
    data = TestClient(app).get("/api/penjualan/pesanan").json()
    assert [(i["nama_makanan"], i["jumlah"]) for i in data[0]["items"]] == [("Roti", 1)]
    assert data[0]["subtotal"] == 12000
    # Penjual tanpa listing yang dibeli sama sekali tidak melihat apa pun
    app.dependency_overrides[get_current_user] = _penjual(99, "Penjual Tak Terkait")
    assert TestClient(app).get("/api/penjualan/pesanan").json() == []
    app.dependency_overrides.clear()


def test_pengambilan_per_toko_pada_transaksi_campur(tmp_path):
    """Satu transaksi checkout campur dua toko: toko A menandai 'Sudah diambil'
    tidak boleh menyelesaikan pesanan milik toko B — status pengambilan
    dikelola per toko, dan transaksi selesai hanya setelah SEMUA toko menandai."""
    path = str(tmp_path / "test.db")
    init_db(path)
    c = sqlite3.connect(path)
    c.executescript("""
        INSERT INTO pengguna (id_pengguna, nama, email, password)
            VALUES (1, 'Penjual', 'p@t.com', 'x'), (2, 'Pembeli', 'b@t.com', 'x'),
                   (3, 'Penjual Lain', 'pl@t.com', 'x');
        INSERT INTO penjual VALUES (1, 'Toko A', 'Jl. A'), (3, 'Toko B', 'Jl. B');
        INSERT INTO pembeli VALUES (2, 'akun');
        INSERT INTO listing_makanan
            (id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok, batas_kedaluwarsa, aktif)
            VALUES (1, 1, 'Roti', '1 pack', 'Baik', 12000, 5, '2999-12-31 23:59:59', 1),
                   (2, 3, 'Bubur', '1 porsi', 'Hangat', 10000, 3, '2999-12-31 23:59:59', 1);
        INSERT INTO transaksi (id_transaksi, id_pembeli, tanggal, batas_waktu_bayar, total_harga, status, kode_pengambilan)
            VALUES (1, 2, '2026-11-09 10:00:00', '2999-01-01 00:00:00', 22000, 'LUNAS', 'SB-AAAAAA');
        INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan)
            VALUES (1, 1, 1, 12000), (1, 2, 1, 10000);
    """)
    c.commit()
    c.close()

    def _conn():
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn

    app.dependency_overrides[get_conn] = _conn

    def _penjual(id_pengguna, nama):
        return lambda: {"id_pengguna": id_pengguna, "nama": nama, "peran": "PENJUAL"}

    # Toko A menandai pesanan sudah diambil
    app.dependency_overrides[get_current_user] = _penjual(1, "Penjual")
    client_a = TestClient(app)
    res_a = client_a.post("/api/penjualan/1/ambil")
    assert res_a.status_code == 200 and res_a.json()["waktu_diambil"]

    # Toko B melihat pesanan yang sama TETAP "Ready for Pickup" (belum diambil)
    app.dependency_overrides[get_current_user] = _penjual(3, "Penjual Lain")
    data_b = TestClient(app).get("/api/penjualan/pesanan").json()
    assert len(data_b) == 1 and data_b[0]["id_transaksi"] == 1
    assert data_b[0]["waktu_diambil"] is None

    # Toko B masih bisa menandai pesanannya sendiri, dengan waktunya sendiri
    res_b = TestClient(app).post("/api/penjualan/1/ambil")
    assert res_b.status_code == 200
    assert res_b.json()["waktu_diambil"] is not None

    # Transaksi level: selesai hanya setelah kedua toko menandai
    dengan_c = sqlite3.connect(path)
    transaksi = dengan_c.execute(
        "SELECT waktu_diambil FROM transaksi WHERE id_transaksi = 1").fetchone()
    assert transaksi[0] is not None
    dengan_c.close()

    # Masing-masing toko tidak dapat menandai dua kali
    assert client_a.post("/api/penjualan/1/ambil").status_code == 409
    assert TestClient(app).post("/api/penjualan/1/ambil").status_code == 409
    app.dependency_overrides.clear()
