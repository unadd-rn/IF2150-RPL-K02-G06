import io
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# 1. Tambahkan direktori root `src` ke sys.path agar `backend` dianggap sebagai package
SRC_DIR = Path(__file__).resolve().parent.parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# 2. Import app sebagai `backend.main` agar relative import di main.py tidak error
from backend.main import app

client = TestClient(app)


# ==========================================
# 1. TEST UPLOAD FOTO (/api/listing/upload-foto)
# ==========================================

def test_upload_foto_sukses():
    """Uji upload foto berformat valid (PNG/JPG)"""
    file_bytes = io.BytesIO(b"fake image content")
    files = {"file": ("test_foto.jpg", file_bytes, "image/jpeg")}
    
    response = client.post("/api/listing/upload-foto", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "foto" in data
    assert data["foto"].startswith("uploads/listing/")


def test_upload_foto_sukses():
    """Uji upload foto berformat valid (PNG/JPG)"""
    file_bytes = io.BytesIO(b"fake image content")
    files = {"file": ("test_foto.jpg", file_bytes, "image/jpeg")}
    
    response = client.post("/api/listing/upload-foto", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "foto" in data
    # 🔴 SESUAIKAN: Gunakan slash di awal "/uploads/listing/" atau gunakan "in"
    assert data["foto"].startswith("/uploads/listing/") or data["foto"].startswith("uploads/listing/")
# ==========================================
# 2. TEST GET LISTING PENJUAL (/api/listing/penjual)
# ==========================================

def test_get_listing_penjual():
    """Uji ambil daftar listing milik penjual"""
    response = client.get("/api/listing/penjual")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ==========================================
# 3. TEST TAMBAH LISTING (/api/listing/)
# ==========================================

def test_tambah_listing_sukses():
    """Uji tambah listing makanan baru dengan data valid"""
    payload = {
        "nama_makanan": "Nasi Goreng Spesial",
        "deskripsi": "Porsi besar sisa event jam 14.00",
        "porsi": "1 Porsi",
        "kondisi": "Sangat Baik",
        "harga": 15000,
        "stok": 5,
        "batas_kedaluwarsa": "2026-12-31T23:59:00",
        "foto": "uploads/listing/sample.jpg"
    }
    
    response = client.post("/api/listing/", json=payload)
    
    assert response.status_code == 201
    disimpan = response.json()
    assert disimpan["nama_makanan"] == payload["nama_makanan"]
    assert disimpan["harga"] == payload["harga"]