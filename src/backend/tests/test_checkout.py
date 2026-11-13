import sqlite3
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models import init_db
from backend.routers.auth import get_current_user
from backend.api.pembayaran_routes import get_conn

# FIXTURES
@pytest.fixture
def db_path(tmp_path):
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
        "id_pengguna": 2, "nama": "Pembeli", "email": "b@t.com", "peran": "PEMBELI"
    }
    
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def stok(db_path):
    def _stok(id_listing):
        c = sqlite3.connect(db_path)
        try:
            return c.execute("SELECT stok FROM listing_makanan WHERE id_listing = ?", (id_listing,)).fetchone()[0]
        finally:
            c.close()
    return _stok

# TESTS
def test_checkout_valid(client, stok):
    r = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 2})
    assert r.status_code == 200
    d = r.json()
    assert d["status"] == "MENUNGGU_BAYAR"
    assert d["total_harga"] == 24000
    assert d["items"][0]["nama_makanan"] == "Roti"
    assert stok(1) == 5  # stock NOT reduced at checkout

def test_jumlah_tidak_valid(client):
    r = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 0})
    assert r.status_code == 400
    assert r.json()["detail"] == "Jumlah porsi tidak valid"

def test_stok_tidak_cukup(client):
    r = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 99})
    assert r.status_code == 409
    assert r.json()["detail"] == "Stok tidak mencukupi"

def test_listing_tidak_ada(client):
    r = client.post("/api/pembayaran/checkout", json={"id_listing": 999, "jumlah": 1})
    assert r.status_code == 404
    assert r.json()["detail"] == "Listing tidak tersedia"

def test_harga_satuan_disalin(client, db_path):
    t = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 1}).json()
    
    c = sqlite3.connect(db_path)
    c.execute("UPDATE listing_makanan SET harga = 99999 WHERE id_listing = 1")
    c.commit()
    c.close()
    
    d = client.get(f"/api/pembayaran/{t['id_transaksi']}").json()
    assert d["items"][0]["harga_satuan"] == 12000