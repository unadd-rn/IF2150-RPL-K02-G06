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
        "deskripsi": "Masih layak makan",
        "porsi": "1 Porsi",
        "kondisi": "Hangat",
        "harga": 15000,
        "stok": 10,
        "batas_kedaluwarsa": (datetime.now() + timedelta(hours=5)).isoformat(),
        "foto": "/uploads/listing/nasi.jpg",
    }
    data = DataListing(**payload)
    assert data.nama_makanan == "Nasi Goreng"
    assert data.harga == 15000

def test_pydantic_schema_harga_negatif_gagal():
    with pytest.raises(Exception):
        DataListing(
            nama_makanan="Nasi Goreng",
            deskripsi="Masih layak makan",
            porsi="1 Porsi",
            kondisi="Hangat",
            harga=-1000, # Harus error
            stok=5,
            batas_kedaluwarsa=(datetime.now() + timedelta(hours=5)).isoformat(),
            foto="/uploads/listing/nasi.jpg",
        )

def test_pydantic_schema_batas_deskripsi_3000_karakter():
    payload = {
        "nama_makanan": "Roti",
        "deskripsi": "a" * 3000,
        "porsi": "1 pack",
        "kondisi": "Baik",
        "harga": 10000,
        "stok": 1,
        "batas_kedaluwarsa": (datetime.now() + timedelta(hours=5)).isoformat(),
        "foto": "/uploads/listing/roti.jpg",
    }
    assert len(DataListing(**payload).deskripsi) == 3000

    with pytest.raises(Exception):
        DataListing(**{**payload, "deskripsi": "a" * 3001})

# -------------------------------------------------------------------
# Test Fungsi Validasi (Validasi.validasiListing)
# -------------------------------------------------------------------

def test_validasi_listing_sukses():
    data = {
        "nama_makanan": "Donat Cokelat",
        "deskripsi": "Donat isi cokelat",
        "porsi": "1 Box",
        "kondisi": "Baik",
        "harga": 20000,
        "stok": 5,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat(),
        "foto": "/uploads/listing/donat.jpg",
    }
    errors = Validasi.validasiListing(data)
    assert len(errors) == 0

def test_validasi_listing_field_kosong():
    data = {
        "nama_makanan": "",
        "deskripsi": "   ",
        "porsi": "  ",
        "kondisi": "",
        "harga": 10000,
        "stok": 2,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat(),
        "foto": "",
    }
    errors = Validasi.validasiListing(data)
    assert "Nama makanan wajib diisi" in errors
    assert "Deskripsi wajib diisi" in errors
    assert "Porsi wajib diisi" in errors
    assert "Kondisi makanan wajib diisi" in errors
    assert "Foto makanan wajib diisi" in errors

def test_validasi_listing_harga_stok_negatif():
    data = {
        "nama_makanan": "Roti",
        "deskripsi": "Roti tawar",
        "porsi": "1 Pcs",
        "kondisi": "Baik",
        "harga": -5000,
        "stok": -3,
        "batas_kedaluwarsa": (datetime.now() + timedelta(days=1)).isoformat(),
        "foto": "/uploads/listing/roti.jpg",
    }
    errors = Validasi.validasiListing(data)
    assert "Harga tidak boleh negatif" in errors
    assert "Stok tidak boleh negatif" in errors

def test_validasi_listing_kedaluwarsa_lewat():
    waktu_lalu = (datetime.now() - timedelta(hours=2)).isoformat()
    data = {
        "nama_makanan": "Susu Segar",
        "deskripsi": "Susu segar",
        "porsi": "1 Liter",
        "kondisi": "Dingin",
        "harga": 12000,
        "stok": 1,
        "batas_kedaluwarsa": waktu_lalu,
        "foto": "/uploads/listing/susu.jpg",
    }
    errors = Validasi.validasiListing(data)
    assert "Batas kedaluwarsa harus lebih dari waktu sekarang" in errors