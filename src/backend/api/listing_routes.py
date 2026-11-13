import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterator

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from ..models import ListingMakanan
from ..routers.auth import require_roles
from ..schemas.listing_schema import DataListing
from ..services.listing_service import UPLOADS_DIR, simpan_foto_listing
from ..validation import Validasi

router = APIRouter(prefix="/api/listing", tags=["Listing Penjual"])


def get_conn() -> Iterator[sqlite3.Connection]:
    from ..main import get_db_connection

    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


def _listing_from_row(row: sqlite3.Row) -> ListingMakanan:
    data = dict(row)
    data["aktif"] = bool(data["aktif"])
    data["draft"] = bool(data["draft"])
    return ListingMakanan(**data)


def _listing_response(listing: ListingMakanan) -> dict:
    result = asdict(listing)
    batas_kedaluwarsa = datetime.fromisoformat(listing.batas_kedaluwarsa)
    waktu_sekarang = datetime.now(batas_kedaluwarsa.tzinfo)
    result["tersedia"] = listing.is_tersedia(waktu_sekarang)
    return result


def _validasi(data: DataListing) -> None:
    errors = Validasi.validasiListing(data)
    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=", ".join(errors))


def _validasi_foto(foto: str) -> None:
    prefix = "/uploads/listing/"
    filename = foto[len(prefix):] if foto.startswith(prefix) else ""
    if not filename or Path(filename).name != filename or not (UPLOADS_DIR / filename).is_file():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foto harus diunggah melalui endpoint upload listing",
        )


@router.get("/penjual")
def get_daftar_listing_penjual(
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    rows = conn.execute(
        """
        SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
               batas_kedaluwarsa, deskripsi, foto, aktif, draft
        FROM listing_makanan
        WHERE id_penjual = ? AND aktif = 1
        ORDER BY id_listing DESC
        """,
        (current_user["id_pengguna"],),
    ).fetchall()
    return [_listing_response(_listing_from_row(row)) for row in rows]


@router.get("/{id_listing}")
def get_detail_listing(
    id_listing: int,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    row = conn.execute(
        """
        SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
               batas_kedaluwarsa, deskripsi, foto, aktif, draft
        FROM listing_makanan
        WHERE id_listing = ? AND id_penjual = ? AND aktif = 1
        """,
        (id_listing, current_user["id_pengguna"]),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Listing tidak ditemukan")
    return _listing_response(_listing_from_row(row))


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
def tambah_listing(
    data: DataListing,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    _validasi(data)
    _validasi_foto(data.foto)
    values = data.model_dump(mode="json")
    batas_kedaluwarsa = data.batas_kedaluwarsa
    if batas_kedaluwarsa.tzinfo is not None:
        batas_kedaluwarsa = batas_kedaluwarsa.astimezone().replace(tzinfo=None)
    values["batas_kedaluwarsa"] = batas_kedaluwarsa.isoformat(timespec="seconds")

    cursor = conn.execute(
        """
        INSERT INTO listing_makanan
            (id_penjual, nama_makanan, deskripsi, porsi, kondisi, foto, harga, stok,
             batas_kedaluwarsa, aktif, draft)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """,
        (
            current_user["id_pengguna"],
            values["nama_makanan"],
            values["deskripsi"],
            values["porsi"],
            values["kondisi"],
            values["foto"],
            values["harga"],
            values["stok"],
            values["batas_kedaluwarsa"],
            int(values["draft"]),
        ),
    )
    conn.commit()
    row = conn.execute(
        """
        SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
               batas_kedaluwarsa, deskripsi, foto, aktif, draft
        FROM listing_makanan WHERE id_listing = ?
        """,
        (cursor.lastrowid,),
    ).fetchone()
    return _listing_response(_listing_from_row(row))


@router.put("/{id_listing}")
def ubah_listing(
    id_listing: int,
    data: DataListing,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    _validasi(data)
    _validasi_foto(data.foto)
    batas_kedaluwarsa = data.batas_kedaluwarsa
    if batas_kedaluwarsa.tzinfo is not None:
        batas_kedaluwarsa = batas_kedaluwarsa.astimezone().replace(tzinfo=None)

    cursor = conn.execute(
        """
        UPDATE listing_makanan
        SET nama_makanan = ?, deskripsi = ?, porsi = ?, kondisi = ?, foto = ?,
            harga = ?, stok = ?, batas_kedaluwarsa = ?, draft = ?
        WHERE id_listing = ? AND id_penjual = ? AND aktif = 1
        """,
        (
            data.nama_makanan,
            data.deskripsi,
            data.porsi,
            data.kondisi,
            data.foto,
            data.harga,
            data.stok,
            batas_kedaluwarsa.isoformat(timespec="seconds"),
            int(data.draft),
            id_listing,
            current_user["id_pengguna"],
        ),
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Listing tidak ditemukan")
    conn.commit()
    row = conn.execute(
        """
        SELECT id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
               batas_kedaluwarsa, deskripsi, foto, aktif, draft
        FROM listing_makanan WHERE id_listing = ?
        """,
        (id_listing,),
    ).fetchone()
    return _listing_response(_listing_from_row(row))


@router.delete("/{id_listing}")
def hapus_listing(
    id_listing: int,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    cursor = conn.execute(
        """
        UPDATE listing_makanan SET aktif = 0
        WHERE id_listing = ? AND id_penjual = ? AND aktif = 1
        """,
        (id_listing, current_user["id_pengguna"]),
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Listing tidak ditemukan")
    conn.commit()
    return {"message": "Listing berhasil dinonaktifkan", "id_listing": id_listing}


@router.post("/upload-foto")
async def upload_foto(
    file: UploadFile = File(...),
    _: dict = Depends(require_roles(["PENJUAL"])),
):
    try:
        foto = await simpan_foto_listing(file)
    finally:
        await file.close()
    return {"foto": foto}
