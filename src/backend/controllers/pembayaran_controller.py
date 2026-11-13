import sqlite3
import secrets
from datetime import date, datetime, timedelta

from ..adapters.metode_pembayaran import MetodePembayaran
from ..adapters.payment_gateway_adapter import PaymentGatewayAdapter
from ..errors import PembayaranError
from ..models import ItemTransaksi, Kupon, ListingMakanan, Transaksi

BATAS_WAKTU_BAYAR = timedelta(minutes=15)
FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"


def _sahkan_kupon(conn: sqlite3.Connection, id_pembeli: int, kode_kupon: str) -> Kupon:
    """Validasi kupon reward yang akan ditebus (Algo-C05-kupon): milik pembeli,
    belum terpakai, dan masih berlaku. Kupon milik pembeli lain dilaporkan
    sama dengan kupon yang tidak ada agar tidak bocor."""
    kupon = Kupon.carikanByKode(conn, kode_kupon)
    if kupon is None or kupon.id_pembeli != id_pembeli:
        raise PembayaranError("Kupon tidak ditemukan", 404)
    if kupon.terpakai:
        raise PembayaranError("Kupon sudah terpakai", 400)
    if not kupon.is_berlaku(date.today().isoformat()):
        raise PembayaranError("Kupon sudah kedaluwarsa", 400)
    return kupon


def ambil_transaksi(conn: sqlite3.Connection, id_transaksi: int):
    """Returns (Transaksi, [ItemTransaksi], {id_listing: nama_makanan})."""
    baris = conn.execute(
        "SELECT * FROM transaksi WHERE id_transaksi = ?", (id_transaksi,)
    ).fetchone()
    if baris is None:
        return None, [], {}
    rows = conn.execute(
        "SELECT i.*, l.nama_makanan FROM item_transaksi i "
        "JOIN listing_makanan l ON l.id_listing = i.id_listing "
        "WHERE i.id_transaksi = ?", (id_transaksi,)
    ).fetchall()
    items = [ItemTransaksi(r["id_item"], r["id_transaksi"], r["id_listing"],
                           r["jumlah"], r["harga_satuan"]) for r in rows]
    nama = {r["id_listing"]: r["nama_makanan"] for r in rows}
    return Transaksi(**dict(baris)), items, nama


class PembayaranController:
    def __init__(self, metode: MetodePembayaran | None = None):
        # Adapter metode pembayaran (default: QRIS dummy gateway).
        self.metode = metode if metode is not None else PaymentGatewayAdapter()

    def checkout(self, conn: sqlite3.Connection, id_pembeli: int, id_listing: int, jumlah: int):
        """Membuat transaksi untuk satu listing (UC05)."""
        return self.checkout_banyak(conn, id_pembeli, [(id_listing, jumlah)])

    def checkout_banyak(self, conn: sqlite3.Connection, id_pembeli: int, pesanan: list[tuple[int, int]],
                        kode_kupon: str | None = None):
        """Membuat satu transaksi dari daftar pesanan [(id_listing, jumlah), ...] (UC05).
        Mendukung satu maupun beberapa listing (dari keranjang) sekaligus, dan
        kode_kupon kupon reward pembeli yang ditebus pada subtotal."""
        if not pesanan:
            raise PembayaranError("Pesanan tidak boleh kosong")
        if any(jumlah <= 0 for _, jumlah in pesanan):
            raise PembayaranError("Jumlah porsi tidak valid")

        # Gabungkan jumlah untuk listing yang sama agar stok divalidasi satu kali
        gabungan: dict[int, int] = {}
        for id_listing, jumlah in pesanan:
            gabungan[id_listing] = gabungan.get(id_listing, 0) + jumlah

        sekarang = datetime.now()
        dipilih: list[tuple[ListingMakanan, int]] = []
        for id_listing, jumlah in gabungan.items():
            listing = ListingMakanan.cariById(conn, id_listing)
            if listing is None or not listing.is_tersedia(sekarang):
                raise PembayaranError("Listing tidak tersedia", 404)
            if listing.stok < jumlah:
                raise PembayaranError("Stok tidak mencukupi", 409)
            dipilih.append((listing, jumlah))

        # Kupon reward (opsional): tapis validasi sebelum transaksi dibuat,
        # dipotongkan dari subtotal dan ditandai terpakai bersama transaksi.
        kupon = _sahkan_kupon(conn, id_pembeli, kode_kupon) if kode_kupon else None
        subtotal = sum(listing.harga * jumlah for listing, jumlah in dipilih)
        total_harga = subtotal
        if kupon is not None:
            total_harga = subtotal - min(kupon.nilai_potongan, subtotal)   # tidak pernah negatif

        try:
            cur = conn.execute(
                "INSERT INTO transaksi (id_pembeli, tanggal, batas_waktu_bayar, token_bayar, kode_kupon) "
                "VALUES (?, ?, ?, ?, ?)",
                (id_pembeli, sekarang.strftime(FORMAT_WAKTU),
                 (sekarang + BATAS_WAKTU_BAYAR).strftime(FORMAT_WAKTU), secrets.token_urlsafe(32),
                 kupon.kode_kupon if kupon is not None else None),
            )
            id_transaksi = cur.lastrowid
            for listing, jumlah in dipilih:
                item = ItemTransaksi(None, id_transaksi, listing.id_listing, jumlah, listing.harga)
                conn.execute(
                    "INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan) "
                    "VALUES (?, ?, ?, ?)",
                    (id_transaksi, item.id_listing, item.jumlah, item.harga_satuan),
                )
            # Tandai kupon terpakai bersama transaksi (dikembalikan bila transaksi BATAL)
            if kupon is not None:
                conn.execute(
                    "UPDATE kupon SET terpakai = 1 WHERE kode_kupon = ? AND id_pembeli = ? AND terpakai = 0",
                    (kupon.kode_kupon, id_pembeli),
                )
            conn.execute(
                "UPDATE transaksi SET total_harga = ? WHERE id_transaksi = ?",
                (total_harga, id_transaksi),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise

        trx, items, nama = ambil_transaksi(conn, id_transaksi)
        return trx, items, nama, self.metode.buat_tagihan(trx)


    def konfirmasi_bayar(self, conn: sqlite3.Connection, id_transaksi: int, id_pembeli: int,
                         scan_dikonfirmasi: bool = False):
        sekarang = datetime.now()
        waktu = sekarang.strftime(FORMAT_WAKTU)
        try:
            conn.execute("BEGIN IMMEDIATE")   # take SQLite's write lock first, so two payments run one after the other
            trx, items, _ = ambil_transaksi(conn, id_transaksi)
            if trx is None or trx.id_pembeli != id_pembeli or trx.status != "MENUNGGU_BAYAR":
                raise PembayaranError("Transaksi tidak dapat dibayar", 409)

            if sekarang > datetime.fromisoformat(trx.batas_waktu_bayar):   # expired: cancel, return BATAL
                conn.execute("UPDATE transaksi SET status = 'BATAL' WHERE id_transaksi = ?", (id_transaksi,))
                if trx.kode_kupon:
                    # Kupon yang ditebus untuk transaksi yang batal dikembalikan
                    conn.execute(
                        "UPDATE kupon SET terpakai = 0 "
                        "WHERE kode_kupon = ? AND id_pembeli = ? AND terpakai = 1",
                        (trx.kode_kupon, trx.id_pembeli),
                    )
                conn.commit()
                return ambil_transaksi(conn, id_transaksi)

            if not scan_dikonfirmasi and self.metode.cek_status(id_transaksi) != "LUNAS":
                raise PembayaranError("Pembayaran belum diterima", 402)

            kode = "SB-" + secrets.token_hex(3).upper()
            conn.execute(
                "UPDATE transaksi SET status = 'LUNAS', kode_pengambilan = ? WHERE id_transaksi = ?",
                (kode, id_transaksi),
            )
            for item in items:      # every item, or none (rollback below)
                cur = conn.execute(
                    "UPDATE listing_makanan SET stok = stok - :jumlah "
                    f"WHERE id_listing = :id AND stok >= :jumlah AND {ListingMakanan.KONDISI_TERSEDIA}",
                    {"jumlah": item.jumlah, "id": item.id_listing, "waktu": waktu},
                )
                if cur.rowcount != 1:
                    raise PembayaranError("Stok tidak mencukupi", 409)
            conn.commit()
        except Exception:
            conn.rollback()          # undoes LUNAS and any stock already reduced
            raise
        return ambil_transaksi(conn, id_transaksi)
