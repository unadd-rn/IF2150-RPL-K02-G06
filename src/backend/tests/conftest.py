import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models import init_db
from backend.routers.auth import get_current_user
from backend.api.pembayaran_routes import get_conn


@pytest.fixture
def db_path(tmp_path):
    """A throwaway database file with 1 seller, 1 buyer (id 2) and 2 listings."""
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
    """)
    c.commit()
    c.close()
    return path


@pytest.fixture
def client(db_path):
    """API client logged in as the buyer, pointed at the throwaway database."""
    def _conn():
        c = sqlite3.connect(db_path, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON;")
        try:
            yield c
        finally:
            c.close()

    app.dependency_overrides[get_conn] = _conn
    app.dependency_overrides[get_current_user] = lambda: {
        "id_pengguna": 2, "nama": "Pembeli", "email": "b@t.com", "peran": "PEMBELI"}
    yield TestClient(app)      # no `with`, so the lifespan (and the #17 scheduler) never starts
    app.dependency_overrides.clear()


@pytest.fixture
def stok(db_path):
    def _stok(id_listing):
        c = sqlite3.connect(db_path)
        try:
            return c.execute(
                "SELECT stok FROM listing_makanan WHERE id_listing = ?", (id_listing,)
            ).fetchone()[0]
        finally:
            c.close()
    return _stok


@pytest.fixture
def buat_trx(db_path):
    """Insert a MENUNGGU_BAYAR transaction directly. items = [(id_listing, jumlah), ...]."""
    def _buat(items, batas="2999-12-31 23:59:59"):
        c = sqlite3.connect(db_path)
        cur = c.execute(
            "INSERT INTO transaksi (id_pembeli, batas_waktu_bayar) VALUES (2, ?)", (batas,)
        )
        tid = cur.lastrowid
        for id_listing, jumlah in items:
            c.execute(
                "INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan) "
                "VALUES (?, ?, ?, 12000)", (tid, id_listing, jumlah))
        c.commit()
        c.close()
        return tid
    return _buat

@pytest.fixture
def buat_trx(db_path):
    def _buat(items, batas="2999-12-31 23:59:59"):
        c = sqlite3.connect(db_path)
        cur = c.execute("INSERT INTO transaksi (id_pembeli, batas_waktu_bayar) VALUES (2, ?)", (batas,))