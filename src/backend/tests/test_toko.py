"""Pengujian profil toko penjual (/api/toko) dan katalog pembeli yang menampilkan
nama toko & alamat pengambilan."""
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models import init_db
from backend.routers.auth import get_current_user
from backend.api.toko_routes import get_conn as toko_conn
from backend.controllers.katalog_controller import get_conn as katalog_conn


@pytest.fixture
def db_uji(tmp_path):
    """Basis data uji: 1 penjual, 1 pembeli, 1 listing dengan data toko awal."""
    path = str(tmp_path / "test.db")
    init_db(path)
    c = sqlite3.connect(path)
    c.executescript("""
        INSERT INTO pengguna (id_pengguna, nama, email, password)
            VALUES (1, 'Warung Bu Sari', 'p@t.com', 'x'), (2, 'Pembeli', 'b@t.com', 'x');
        INSERT INTO penjual (id_pengguna, nama_toko, alamat_toko)
            VALUES (1, 'Toko Awal', 'Jl. Awal No. 1');
        INSERT INTO pembeli VALUES (2, 'akun');
        INSERT INTO listing_makanan
            (id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
             batas_kedaluwarsa, aktif)
            VALUES (1, 1, 'Roti', '1 pack', 'Baik', 12000, 5, '2999-12-31 23:59:59', 1);
    """)
    c.commit()
    c.close()
    return path


def _sambungkan(db_path):
    def _conn():
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()
    return _conn


@pytest.fixture
def client(db_uji):
    """API client termasuk penjual (untuk /api/toko) dan pembeli (untuk /api/katalog)."""
    connect = _sambungkan(db_uji)
    app.dependency_overrides[toko_conn] = connect
    app.dependency_overrides[katalog_conn] = connect

    def _sebagai(peran):
        app.dependency_overrides[get_current_user] = lambda: {
            "id_pengguna": 1 if peran == "PENJUAL" else 2,
            "nama": "Warung Bu Sari" if peran == "PENJUAL" else "Pembeli",
            "peran": peran,
        }
        return TestClient(app)

    yield _sebagai
    app.dependency_overrides.clear()


def test_lihat_profil_toko(client):
    data = client("PENJUAL").get("/api/toko").json()
    assert data["nama_toko"] == "Toko Awal"
    assert data["alamat_toko"] == "Jl. Awal No. 1"
    assert data["nama_akun"] == "Warung Bu Sari"


def test_ubah_profil_toko_lalu_terlihat_di_katalog(client):
    res = client("PENJUAL").put("/api/toko", json={"nama_toko": "Toko Baru", "alamat_toko": "Jl. Baru No. 2"})
    assert res.status_code == 200

    katalog = client("PEMBELI").get("/api/katalog").json()
    assert katalog[0]["nama_toko"] == "Toko Baru"
    assert katalog[0]["alamat_toko"] == "Jl. Baru No. 2"


def test_katalog_membawa_nama_dan_alamat_toko(client):
    katalog = client("PEMBELI").get("/api/katalog").json()
    assert katalog[0]["nama_toko"] == "Toko Awal"
    assert katalog[0]["alamat_toko"] == "Jl. Awal No. 1"

    detail = client("PEMBELI").get("/api/katalog/1").json()
    assert detail["nama_toko"] == "Toko Awal"
    assert detail["alamat_toko"] == "Jl. Awal No. 1"


def test_validasi_profil_toko(client):
    penjual = client("PENJUAL")
    for payload in (
        {"nama_toko": "", "alamat_toko": "x"},
        {"nama_toko": "Toko", "alamat_toko": "   "},
        {"nama_toko": "T" * 101, "alamat_toko": "x"},
    ):
        res = penjual.put("/api/toko", json=payload)
        assert res.status_code == 400, payload


def test_hanya_penjual_yang_boleh_ubah_profil(client):
    assert client("PEMBELI").get("/api/toko").status_code == 403
    assert client("PEMBELI").put("/api/toko", json={"nama_toko": "x", "alamat_toko": "y"}).status_code == 403
