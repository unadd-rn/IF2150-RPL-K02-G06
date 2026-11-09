import sys
from pathlib import Path

import pytest
from datetime import datetime, timedelta

# validation.py memakai import paket "backend.*", jadi folder src/ harus ada di sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.validation import Validasi  # noqa: E402
from backend.schemas.listing_schema import DataListing  # noqa: E402

# -------------------------------------------------------------------
# Test Schema Pydantic (DataListing)
# -------------------------------------------------------------------

def test_pydantic_schema_valid():
    payload = {
        "nama_makanan": "Nasi Goreng",
        "porsi": "1 Porsi",
        "kondisi": "Hangat",
        "harga": 15000,
        "stok": 10,
        "batas_kedaluwarsa": (datetime.now() + timedelta(hours=5)).isoformat()
    }
    data = DataListing(**payload)
    assert data.nama_makanan == "Nasi Goreng"
    assert data.harga == 15000

def test_pydantic_schema_harga_negatif_gagal():
    with pytest.raises(Exception):
        DataListing(
            nama_makanan="Nasi Goreng",
            porsi="1 Porsi",
            kondisi="Hangat",
            harga=-1000, # Harus error
            stok=5,
            batas_kedaluwarsa=(datetime.now() + timedelta(hours=5)).isoformat()
        )

# -------------------------------------------------------------------
# Test Fungsi Validasi (Validasi.validasiListing)
# -------------------------------------------------------------------

def test_validasi_listing_sukses():
    data = {
        "nama_makanan": "Donat Cokelat",
        "porsi": "1 Box",
        "kondisi": "Baik",
        "harga": 20000,
        "stok": 5,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat()
    }
    errors = Validasi.validasiListing(data)
    assert len(errors) == 0

def test_validasi_listing_field_kosong():
    data = {
        "nama_makanan": "",
        "porsi": "  ",
        "kondisi": "",
        "harga": 10000,
        "stok": 2,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat()
    }
    errors = Validasi.validasiListing(data)
    assert "Nama makanan wajib diisi" in errors
    assert "Porsi wajib diisi" in errors
    assert "Kondisi makanan wajib diisi" in errors

def test_validasi_listing_harga_stok_negatif():
    data = {
        "nama_makanan": "Roti",
        "porsi": "1 Pcs",
        "kondisi": "Baik",
        "harga": -5000,
        "stok": -3,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat()
    }
    errors = Validasi.validasiListing(data)
    assert "Harga tidak boleh negatif" in errors
    assert "Stok tidak boleh negatif" in errors

def test_validasi_listing_kedaluwarsa_lewat():
    waktu_lalu = (datetime.now() - timedelta(hours=2)).isoformat()
    data = {
        "nama_makanan": "Susu Segar",
        "porsi": "1 Liter",
        "kondisi": "Dingin",
        "harga": 12000,
        "stok": 1,
        "batas_kedaluwarsa": waktu_lalu
    }
    errors = Validasi.validasiListing(data)
    assert "Batas kedaluwarsa harus lebih dari waktu sekarang" in errors