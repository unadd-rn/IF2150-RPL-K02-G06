"""Skenario alternatif KatalogController (UC02, UC03, UC04) — DPPL 3.2.2, 3.3.2, 3.4.2, 3.4.3."""
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from fastapi import HTTPException

# Controller memakai import paket "backend.*", jadi folder src/ harus ada di sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.controllers.katalog_controller import (  # noqa: E402
    ambilDetail,
    ambilListingTersedia,
    cariListing,
)
from backend.models import CREATE_TABLES_SQL  # noqa: E402


def _waktu(jam: int) -> str:
    return (datetime.now() + timedelta(hours=jam)).strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript(CREATE_TABLES_SQL)
    c.execute("INSERT INTO pengguna (id_pengguna, nama, email, password) VALUES (1, 'Kantin', 'k@x.id', 'x')")
    c.execute("INSERT INTO penjual (id_pengguna, nama_toko, alamat_toko) VALUES (1, 'Kantin', 'Gedung A')")
    yield c
    c.close()


def _tambah(conn, nama="Nasi Goreng", harga=15000, stok=5, jam=3, aktif=1) -> int:
    cur = conn.execute(
        "INSERT INTO listing_makanan (id_penjual, nama_makanan, porsi, kondisi, harga, stok, batas_kedaluwarsa, aktif) "
        "VALUES (1, ?, '1 porsi', 'Baik', ?, ?, ?, ?)",
        (nama, harga, stok, _waktu(jam), aktif),
    )
    return cur.lastrowid


# ---------- UC02 Alt 1: tidak ada listing tersedia ----------

def test_katalog_kosong_mengembalikan_daftar_kosong(conn):
    assert ambilListingTersedia(conn) == []


def test_katalog_hanya_berisi_listing_tidak_tersedia_dianggap_kosong(conn):
    _tambah(conn, stok=0)
    _tambah(conn, jam=-1)
    _tambah(conn, aktif=0)
    assert ambilListingTersedia(conn) == []


# ---------- UC03 Alt 1: listing yang dipilih tiba-tiba dihapus ----------

@pytest.mark.parametrize("ubah", [
    "DELETE FROM listing_makanan WHERE id_listing = ?",
    "UPDATE listing_makanan SET aktif = 0 WHERE id_listing = ?",
    "UPDATE listing_makanan SET stok = 0 WHERE id_listing = ?",
])
def test_detail_listing_yang_sudah_tidak_tersedia_404(conn, ubah):
    id_listing = _tambah(conn)
    assert ambilDetail(conn, id_listing).id_listing == id_listing
    conn.execute(ubah, (id_listing,))
    with pytest.raises(HTTPException) as e:
        ambilDetail(conn, id_listing)
    assert e.value.status_code == 404
    assert e.value.detail == "Listing sudah tidak tersedia"


def test_detail_listing_kedaluwarsa_404(conn):
    id_listing = _tambah(conn, jam=-1)
    with pytest.raises(HTTPException) as e:
        ambilDetail(conn, id_listing)
    assert e.value.status_code == 404


# ---------- UC04 Alt 1 & 2: hasil cari / filter kosong ----------

def test_kata_kunci_tidak_ada_mengembalikan_daftar_kosong(conn):
    _tambah(conn, nama="Nasi Goreng")
    assert cariListing(conn, "rendang", None, None) == []


def test_rentang_harga_tidak_ada_mengembalikan_daftar_kosong(conn):
    _tambah(conn, harga=15000)
    assert cariListing(conn, None, 50000, 60000) == []


# ---------- UC04: validasi rentang harga ----------

@pytest.mark.parametrize("harga_min, harga_maks", [(20000, 10000), (-1, None), (None, -5)])
def test_rentang_harga_tidak_valid_400(conn, harga_min, harga_maks):
    with pytest.raises(HTTPException) as e:
        cariListing(conn, None, harga_min, harga_maks)
    assert e.value.status_code == 400
    assert e.value.detail == "Rentang harga tidak valid"


def test_harga_min_sama_dengan_maks_valid(conn):
    _tambah(conn, harga=10000)
    assert len(cariListing(conn, None, 10000, 10000)) == 1
