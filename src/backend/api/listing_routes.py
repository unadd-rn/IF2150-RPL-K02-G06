import uuid
import shutil
from pathlib import Path
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status

from ..schemas.listing_schema import DataListing

router = APIRouter(
    prefix="/api/listing",
    tags=["Listing Penjual"]
)

# Menentukan lokasi direktori uploads/listing relatif dari folder backend
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads" / "listing"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# Mock Dependency Auth Sementara (Menunggu P1)
def get_current_penjual():
    return {
        "idPengguna": 1,
        "nama": "Penjual Dummy",
        "email": "penjual@example.com",
        "peran": "penjual"
    }


# Storage sementara di memori server (sebelum full SQLite DB)
DB_LISTINGS: List[Dict[str, Any]] = [
    {
        "id_listing": 1,
        "id_penjual": 1,
        "nama_makanan": "Nasi Goreng Dummy",
        "deskripsi": "Masih hangat dan layak makan",
        "porsi": "1 Porsi",
        "kondisi": "Baik",
        "harga": 15000,
        "stok": 5,
        "batas_kedaluwarsa": "2026-12-31T23:59:59",
        "foto": None,
        "aktif": True,
    }
]


# PENTING: "/penjual" harus didefinisikan SEBELUM "/{id_listing}"
@router.get("/penjual")
def get_daftar_listing_penjual(current_user: dict = Depends(get_current_penjual)):
    """UC01 / UC06 / UC09: Ambil semua listing milik penjual aktif yang masih aktif"""
    user_id = current_user["idPengguna"]
    # Hanya kembalikan listing milik penjual ini yang belum di-soft delete (aktif == True)
    return [item for item in DB_LISTINGS if item["id_penjual"] == user_id and item.get("aktif", True)]


@router.get("/{id_listing}")
def get_detail_listing(id_listing: int, current_user: dict = Depends(get_current_penjual)):
    """UC06: Ambil detail satu listing untuk halaman edit"""
    for item in DB_LISTINGS:
        if item["id_listing"] == id_listing:
            return item
    raise HTTPException(status_code=404, detail="Listing tidak ditemukan")


@router.post("/", status_code=status.HTTP_201_CREATED)
def tambah_listing(data: DataListing, current_user: dict = Depends(get_current_penjual)):
    """UC01: Tambah listing baru dan simpan ke DB"""
    new_id = len(DB_LISTINGS) + 1
    new_item = {
        **data.model_dump(mode="json"),
        "id_listing": new_id,
        "id_penjual": current_user["idPengguna"],
        "aktif": True
    }
    DB_LISTINGS.append(new_item)
    return new_item


@router.put("/{id_listing}")
def ubah_listing(
    id_listing: int,
    data: DataListing,
    current_user: dict = Depends(get_current_penjual),
):
    """UC06: Ubah listing yang sudah ada"""
    for index, item in enumerate(DB_LISTINGS):
        if item["id_listing"] == id_listing:
            updated_item = {
                **item,
                **data.model_dump(mode="json"),
                "id_listing": id_listing,
                "id_penjual": current_user["idPengguna"]
            }
            DB_LISTINGS[index] = updated_item
            return updated_item
            
    raise HTTPException(status_code=404, detail="Listing tidak ditemukan")


@router.delete("/{id_listing}")
def hapus_listing(id_listing: int, current_user: dict = Depends(get_current_penjual)):
    """UC09: Soft delete listing"""
    for item in DB_LISTINGS:
        if item["id_listing"] == id_listing:
            item["aktif"] = False  # Soft delete
            return {"message": "Listing berhasil dinonaktifkan", "id_listing": id_listing}
            
    raise HTTPException(status_code=404, detail="Listing tidak ditemukan")


@router.post("/upload-foto")
async def upload_foto(file: UploadFile = File(...)):
    """UC01 / UC06: Upload foto listing makanan (Maks 10MB, JPG/PNG)"""
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format file harus berupa PNG atau JPG"
        )

    extension = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = UPLOADS_DIR / unique_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal menyimpan foto di server"
        )

    # Leading slash agar cocok dengan http://localhost:8000${foto} di frontend
    return {"foto": f"/uploads/listing/{unique_filename}"}