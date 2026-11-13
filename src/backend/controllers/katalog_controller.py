"""KatalogController (C16): UC02 melihat daftar listing, UC03 melihat detail listing,
UC04 mencari & menyaring listing berdasarkan kata kunci dan rentang harga.

Kriteria "tersedia" tidak ditulis di sini; semuanya lewat ListingMakanan
(ambilSemuaTersedia / cariById + is_tersedia).
"""
import sqlite3
from dataclasses import asdict
from typing import Iterator, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..models import ListingMakanan
from ..routers.auth import require_roles
from ..schemas.katalog import ListingKatalog


def get_conn() -> Iterator[sqlite3.Connection]:
    # Import di dalam fungsi untuk menghindari import melingkar (main.py meng-include router ini)
    from ..main import get_db_connection

    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


# Hanya pembeli yang login (sesi dari P1: cookie session_token / Bearer) yang boleh akses
router = APIRouter(
    prefix="/api/katalog",
    tags=["katalog"],
    dependencies=[Depends(require_roles(["PEMBELI"]))],
)


def ambilListingTersedia(conn: sqlite3.Connection) -> List[ListingMakanan]:
    """Algo-C16-01"""
    return ListingMakanan.ambilSemuaTersedia(conn)


def daftar_toko(conn: sqlite3.Connection) -> dict[int, tuple[str, str]]:
    """Nama & alamat setiap toko (id_penjual → (nama_toko, alamat_toko))."""
    rows = conn.execute("SELECT id_pengguna, nama_toko, alamat_toko FROM penjual").fetchall()
    return {r["id_pengguna"]: (r["nama_toko"], r["alamat_toko"]) for r in rows}


def _dengan_toko(conn: sqlite3.Connection, listings: List[ListingMakanan]) -> List[ListingKatalog]:
    """Melengkapi tiap listing dengan nama toko & alamatnya untuk katalog pembeli."""
    toko = daftar_toko(conn)
    hasil = []
    for listing in listings:
        nama_toko, alamat_toko = toko.get(listing.id_penjual, ("", ""))
        hasil.append(
            ListingKatalog.model_validate(
                {**asdict(listing), "nama_toko": nama_toko, "alamat_toko": alamat_toko}
            )
        )
    return hasil


def ambilDetail(conn: sqlite3.Connection, id_listing: int) -> ListingMakanan:
    """Algo-C16-02"""
    listing = ListingMakanan.cariById(conn, id_listing)
    if listing is None or not listing.is_tersedia():
        raise HTTPException(status_code=404, detail="Listing sudah tidak tersedia")
    return listing


def cariListing(
    conn: sqlite3.Connection,
    kata_kunci: Optional[str],
    harga_min: Optional[int],
    harga_maks: Optional[int],
) -> List[ListingMakanan]:
    """Algo-C16-03"""
    if kata_kunci is not None and not kata_kunci.strip():
        kata_kunci = None
    if (harga_min is not None and harga_min < 0) or (harga_maks is not None and harga_maks < 0):
        raise HTTPException(status_code=400, detail="Rentang harga tidak valid")
    if harga_min is not None and harga_maks is not None and harga_min > harga_maks:
        raise HTTPException(status_code=400, detail="Rentang harga tidak valid")
    # Daftar kosong berarti tidak ada listing yang cocok (bukan error)
    return ListingMakanan.cariDaftar(conn, kata_kunci=kata_kunci, harga_min=harga_min, harga_maks=harga_maks)


@router.get("", response_model=List[ListingKatalog])
def get_daftar_listing(
    kata_kunci: Optional[str] = Query(None, description="Kata kunci nama makanan (UC04)"),
    harga_min: Optional[int] = Query(None, description="Harga minimum dalam rupiah (UC04)"),
    harga_maks: Optional[int] = Query(None, description="Harga maksimum dalam rupiah (UC04)"),
    conn: sqlite3.Connection = Depends(get_conn),
):
    # Tanpa parameter pencarian → UC02 (semua listing tersedia); selain itu → UC04
    if kata_kunci is None and harga_min is None and harga_maks is None:
        return _dengan_toko(conn, ambilListingTersedia(conn))
    return _dengan_toko(conn, cariListing(conn, kata_kunci, harga_min, harga_maks))


@router.get("/{id_listing}", response_model=ListingKatalog)
def get_detail_listing(id_listing: int, conn: sqlite3.Connection = Depends(get_conn)):
    return _dengan_toko(conn, [ambilDetail(conn, id_listing)])[0]
