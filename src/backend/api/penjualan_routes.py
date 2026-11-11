import sqlite3
from datetime import datetime
from typing import Iterator

from fastapi import APIRouter, Depends, HTTPException

from ..models import DATABASE_NAME
from ..routers.auth import require_roles

router = APIRouter(prefix="/api/penjualan", tags=["Penjualan Penjual"])

FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"


def get_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


@router.get("/pesanan")
def daftar_pesanan_terbayar(
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    """Daftar pesanan untuk listing milik penjual ini yang SUDAH DIBAYAR (status LUNAS).

    Item transaksi yang masih MENUNGGU_BAYAR atau BATAL tidak ditampilkan, karena
    penjual baru perlu menyiapkan makanan setelah pembayaran diterima. Setiap pesanan
    membawa flag waktu_diambil milik toko ini saja (None = belum diambil pembeli),
    karena satu transaksi bisa berisi item dari beberapa toko sekaligus.
    """
    id_penjual = current_user["id_pengguna"]
    rows = conn.execute(
        """
        SELECT t.id_transaksi, t.tanggal, t.status, t.total_harga,
               t.kode_pengambilan, pp.waktu_diambil AS waktu_diambil_toko,
               i.id_listing, l.nama_makanan, l.porsi, l.foto,
               i.jumlah, i.harga_satuan
        FROM transaksi t
        JOIN item_transaksi i ON i.id_transaksi = t.id_transaksi
        JOIN listing_makanan l ON l.id_listing = i.id_listing
        LEFT JOIN pengambilan_penjual pp
               ON pp.id_transaksi = t.id_transaksi AND pp.id_penjual = ?
        WHERE t.status = 'LUNAS' AND l.id_penjual = ?
        ORDER BY (pp.waktu_diambil IS NULL) DESC, datetime(t.tanggal) DESC, i.id_item ASC
        """,
        (id_penjual, id_penjual),
    ).fetchall()

    pesanan: dict[int, dict] = {}
    for row in rows:
        trx = pesanan.setdefault(
            row["id_transaksi"],
            {
                "id_transaksi": row["id_transaksi"],
                "tanggal": row["tanggal"],
                "total_harga": row["total_harga"],
                "kode_pengambilan": row["kode_pengambilan"],
                "waktu_diambil": row["waktu_diambil_toko"],
                "items": [],
            },
        )
        trx["items"].append(
            {
                "id_listing": row["id_listing"],
                "nama_makanan": row["nama_makanan"],
                "porsi": row["porsi"],
                "foto": row["foto"],
                "jumlah": row["jumlah"],
                "harga_satuan": row["harga_satuan"],
            }
        )
    for trx in pesanan.values():
        # Subtotal khusus listing milik penjual ini (total_harga transaksi bisa
        # memuat item dari penjual lain bila pembeli checkout campur toko).
        trx["subtotal"] = sum(i["jumlah"] * i["harga_satuan"] for i in trx["items"])
    return list(pesanan.values())


@router.post("/{id_transaksi}/ambil")
def tandai_sudah_diambil(
    id_transaksi: int,
    current_user: dict = Depends(require_roles(["PENJUAL"])),
    conn: sqlite3.Connection = Depends(get_conn),
):
    """Tandai pesanan sebagai 'Sudah diambil / Selesai' saat pembeli mengambil
    makanannya di toko. Hanya transaksi yang sudah LUNAS milik penjual ini
    yang dapat ditandai. Pengambilan dicatat per toko (pengambilan_penjual):
    bila satu transaksi memuat item dari beberapa toko, toko lain tetap
    menunggu pembeli mengambil bagiannya sendiri."""
    id_penjual = current_user["id_pengguna"]
    row = conn.execute(
        """
        SELECT t.id_transaksi, t.status
        FROM transaksi t
        WHERE t.id_transaksi = ?
          AND EXISTS (
              SELECT 1
              FROM item_transaksi i
              JOIN listing_makanan l ON l.id_listing = i.id_listing
              WHERE i.id_transaksi = t.id_transaksi AND l.id_penjual = ?
          )
        """,
        (id_transaksi, id_penjual),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    if row["status"] != "LUNAS":
        raise HTTPException(status_code=409, detail="Pesanan belum dibayar sehingga tidak dapat ditandai diambil")
    sudah = conn.execute(
        "SELECT 1 FROM pengambilan_penjual WHERE id_transaksi = ? AND id_penjual = ?",
        (id_transaksi, id_penjual),
    ).fetchone()
    if sudah is not None:
        raise HTTPException(status_code=409, detail="Pesanan sudah ditandai selesai")

    waktu = datetime.now().strftime(FORMAT_WAKTU)
    try:
        conn.execute("BEGIN IMMEDIATE")   # take SQLite's write lock first, so two sellers marking the same order run one after the other
        conn.execute(
            "INSERT INTO pengambilan_penjual (id_transaksi, id_penjual, waktu_diambil) "
            "VALUES (?, ?, ?)",
            (id_transaksi, id_penjual, waktu),
        )
        # Bila seluruh toko dalam transaksi ini sudah menandai diambil, transaksi
        # dianggap selesai sepenuhnya (waktu_diambil level transaksi terisi).
        jumlah_toko = conn.execute(
            """
            SELECT COUNT(DISTINCT l.id_penjual)
            FROM item_transaksi i
            JOIN listing_makanan l ON l.id_listing = i.id_listing
            WHERE i.id_transaksi = ?
            """,
            (id_transaksi,),
        ).fetchone()[0]
        sudah_diambil = conn.execute(
            "SELECT COUNT(*) FROM pengambilan_penjual WHERE id_transaksi = ?",
            (id_transaksi,),
        ).fetchone()[0]
        if sudah_diambil >= jumlah_toko:
            conn.execute(
                "UPDATE transaksi SET waktu_diambil = ? WHERE id_transaksi = ?",
                (waktu, id_transaksi),
            )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()   # toko yang sama menandai dua kali secara bersamaan
        raise HTTPException(status_code=409, detail="Pesanan sudah ditandai selesai")
    except Exception:
        conn.rollback()
        raise
    return {
        "id_transaksi": id_transaksi,
        "waktu_diambil": waktu,
        "message": "Pesanan ditandai sudah diambil",
    }
