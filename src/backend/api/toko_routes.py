import sqlite3
from typing import Iterator

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..models import DATABASE_NAME
from ..routers.auth import require_roles
from ..validation import Validasi

router = APIRouter(prefix="/api/toko", tags=["Profil Toko Penjual"])


class DataToko(BaseModel):
    nama_toko: str
    alamat_toko: str


def get_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


@router.get("")
def lihat_profil_toko(
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    """Profil toko milik penjual yang sedang login (nama akun, nama toko, alamat pickup)."""
    row = conn.execute(
        """
        SELECT p.nama AS nama_akun, s.nama_toko, s.alamat_toko
        FROM penjual s
        JOIN pengguna p ON p.id_pengguna = s.id_pengguna
        WHERE s.id_pengguna = ?
        """,
        (current_user["id_pengguna"],),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Profil toko tidak ditemukan")
    return {
        "nama_akun": row["nama_akun"],
        "nama_toko": row["nama_toko"],
        "alamat_toko": row["alamat_toko"],
    }


@router.put("")
def ubah_profil_toko(
    data: DataToko,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    """Penjual memperbarui nama toko dan alamat (lokasi pengambilan makanan)."""
    errors = Validasi.validasiToko(data.nama_toko, data.alamat_toko)
    if errors:
        raise HTTPException(status_code=400, detail=", ".join(errors))

    cursor = conn.execute(
        "UPDATE penjual SET nama_toko = ?, alamat_toko = ? WHERE id_pengguna = ?",
        (data.nama_toko.strip(), data.alamat_toko.strip(), current_user["id_pengguna"]),
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Profil toko tidak ditemukan")
    conn.commit()
    return {
        "message": "Profil toko berhasil diperbarui",
        "nama_toko": data.nama_toko.strip(),
        "alamat_toko": data.alamat_toko.strip(),
    }
