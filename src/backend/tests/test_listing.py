import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

SRC_DIR = Path(__file__).resolve().parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from backend import main  # noqa: E402
from backend.api import listing_routes  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models import CREATE_TABLES_SQL  # noqa: E402
from backend.routers.auth import get_current_user  # noqa: E402


@pytest.fixture
def listing_client(tmp_path, monkeypatch):
    database_path = tmp_path / "listing-tests.db"
    with sqlite3.connect(database_path) as conn:
        conn.executescript(CREATE_TABLES_SQL)
        conn.executemany(
            "INSERT INTO pengguna (id_pengguna, nama, email, password) VALUES (?, ?, ?, ?)",
            [
                (1, "Seller One", "one@example.test", "hash"),
                (2, "Seller Two", "two@example.test", "hash"),
            ],
        )
        conn.executemany(
            "INSERT INTO penjual (id_pengguna, nama_toko, alamat_toko) VALUES (?, ?, ?)",
            [(1, "One Shop", "Address One"), (2, "Two Shop", "Address Two")],
        )

    def connect_test_database():
        conn = sqlite3.connect(database_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    monkeypatch.setattr(main, "get_db_connection", connect_test_database)
    monkeypatch.setattr(listing_routes, "UPLOADS_DIR", tmp_path / "uploads")
    listing_routes.UPLOADS_DIR.mkdir()
    (listing_routes.UPLOADS_DIR / "roti.jpg").write_bytes(b"test photo")
    current_user = {"id_pengguna": 1, "nama": "Seller One", "peran": "PENJUAL"}
    monkeypatch.setitem(app.dependency_overrides, get_current_user, lambda: current_user)
    client = TestClient(app)
    yield client, current_user, database_path
    client.close()
    app.dependency_overrides.pop(get_current_user, None)


def _payload(**changes):
    payload = {
        "nama_makanan": "Roti Surplus",
        "deskripsi": "Roti yang masih layak dikonsumsi",
        "porsi": "1 pack",
        "kondisi": "Baik",
        "harga": 12000,
        "stok": 5,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=2)).isoformat(),
        "foto": "/uploads/listing/roti.jpg",
    }
    return payload | changes


def test_listing_memerlukan_penjual_login(listing_client):
    client, current_user, _ = listing_client
    app.dependency_overrides.pop(get_current_user)
    try:
        response = client.get("/api/listing/penjual")
    finally:
        app.dependency_overrides[get_current_user] = lambda: current_user
    assert response.status_code == 401


def test_listing_menolak_peran_pembeli(listing_client):
    client, current_user, _ = listing_client
    current_user["peran"] = "PEMBELI"
    response = client.get("/api/listing/penjual")
    assert response.status_code == 403


def test_tambah_dan_ambil_listing_dari_sqlite(listing_client):
    client, _, _ = listing_client

    response = client.post("/api/listing/", json=_payload())
    assert response.status_code == 201
    created = response.json()
    assert created["nama_makanan"] == "Roti Surplus"
    assert created["tersedia"] is True

    daftar = client.get("/api/listing/penjual")
    assert daftar.status_code == 200
    assert [item["id_listing"] for item in daftar.json()] == [created["id_listing"]]
    detail = client.get(f"/api/listing/{created['id_listing']}")
    assert detail.status_code == 200
    assert detail.json()["foto"] == "/uploads/listing/roti.jpg"


def test_tambah_listing_tanpa_slash_di_akhir(listing_client):
    client, _, _ = listing_client
    response = client.post("/api/listing", json=_payload(draft=True))
    assert response.status_code == 201
    assert response.json()["draft"] is True


def test_listing_dengan_timestamp_utc_tetap_terbaca_katalog(listing_client):
    client, current_user, _ = listing_client
    batas_kedaluwarsa = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    created = client.post(
        "/api/listing/",
        json=_payload(batas_kedaluwarsa=batas_kedaluwarsa),
    ).json()

    assert not created["batas_kedaluwarsa"].endswith("+00:00")
    current_user["peran"] = "PEMBELI"
    katalog = client.get("/api/katalog")
    assert katalog.status_code == 200
    assert [item["id_listing"] for item in katalog.json()] == [created["id_listing"]]


def test_draf_tidak_muncul_di_katalog_dan_bisa_diterbitkan(listing_client):
    client, current_user, _ = listing_client
    draf = client.post("/api/listing/", json=_payload(draft=True)).json()
    assert draf["draft"] is True
    assert draf["tersedia"] is False
    assert client.get("/api/listing/penjual").json()[0]["draft"] is True

    current_user["peran"] = "PEMBELI"
    assert client.get("/api/katalog").json() == []
    current_user["peran"] = "PENJUAL"

    diterbitkan = client.put(
        f"/api/listing/{draf['id_listing']}", json=_payload(draft=False)
    )
    assert diterbitkan.status_code == 200
    assert diterbitkan.json()["draft"] is False
    assert diterbitkan.json()["tersedia"] is True


def test_listing_menolak_deskripsi_kosong_tanggal_lampau_dan_foto_kosong(listing_client):
    client, _, _ = listing_client
    invalid_payloads = [
        _payload(deskripsi="   "),
        _payload(batas_kedaluwarsa=(datetime.now() - timedelta(minutes=1)).isoformat()),
        _payload(foto=""),
    ]

    for payload in invalid_payloads:
        response = client.post("/api/listing/", json=payload)
        assert response.status_code in (400, 422)

def test_listing_menolak_path_foto_yang_tidak_diunggah(listing_client):
    client, _, _ = listing_client
    response = client.post(
        "/api/listing/",
        json=_payload(foto="/uploads/listing/not-uploaded.jpg"),
    )
    assert response.status_code == 400


def test_listing_hanya_bisa_diedit_atau_dihapus_pemiliknya(listing_client):
    client, current_user, _ = listing_client
    created = client.post("/api/listing/", json=_payload()).json()
    current_user["id_pengguna"] = 2
    updated_payload = _payload(nama_makanan="Diubah pihak lain")

    assert client.get(f"/api/listing/{created['id_listing']}").status_code == 404
    assert client.put(f"/api/listing/{created['id_listing']}", json=updated_payload).status_code == 404
    assert client.delete(f"/api/listing/{created['id_listing']}").status_code == 404

    with sqlite3.connect(listing_client[2]) as conn:
        row = conn.execute(
            "SELECT nama_makanan, aktif FROM listing_makanan WHERE id_listing = ?",
            (created["id_listing"],),
        ).fetchone()
    assert row == ("Roti Surplus", 1)


def test_hapus_listing_menonaktifkan_tanpa_menghapus_riwayat(listing_client):
    client, _, database_path = listing_client
    created = client.post("/api/listing/", json=_payload()).json()

    response = client.delete(f"/api/listing/{created['id_listing']}")
    assert response.status_code == 200
    assert client.get("/api/listing/penjual").json() == []

    with sqlite3.connect(database_path) as conn:
        row = conn.execute(
            "SELECT aktif FROM listing_makanan WHERE id_listing = ?",
            (created["id_listing"],),
        ).fetchone()
    assert row == (0,)


def test_upload_foto_route_memakai_service_dan_mewajibkan_auth(listing_client, monkeypatch):
    client, _, _ = listing_client

    async def fake_save_photo(_file):
        return "/uploads/listing/test.png"

    monkeypatch.setattr(listing_routes, "simpan_foto_listing", fake_save_photo)
    response = client.post(
        "/api/listing/upload-foto",
        files={"file": ("test.png", b"image content", "image/png")},
    )
    assert response.status_code == 200
    assert response.json() == {"foto": "/uploads/listing/test.png"}
