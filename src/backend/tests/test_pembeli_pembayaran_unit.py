"""Unit test PembayaranController.konfirmasi_bayar dari sudut pandang Pembeli (UC05).

Mencakup:
1. Flow test   : bayar via scan QR sukses; bayar via status gateway sukses;
                 kode pengambilan dibuat.
2. Exception   : transaksi milik pembeli lain, ditolak, sudah bayar, tidak ada.
3. Alternatif  : tidak membayar sampai batas waktu → BATAL (stok kembali aman),
                 bayar ganda idempoten, dua transaksi berebut stok terakhir,
                 rollback menyeluruh bila satu item gagal.

Satu adapter palsu dipakai supaya status gateway jelas ('LUNAS'/'BELUM').
"""
import sqlite3

import pytest

from backend.adapters.metode_pembayaran import MetodePembayaran
from backend.controllers.pembayaran_controller import PembayaranController
from backend.errors import PembayaranError


@pytest.fixture
def conn(db_path):
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    c.commit()
    yield c
    c.close()


class MetodePalsu(MetodePembayaran):
    def __init__(self, status="BELUM"):
        self.status = status

    def buat_tagihan(self, transaksi) -> str:
        return "tagihan-palsu"

    def cek_status(self, id_transaksi: int) -> str:
        return self.status


@pytest.fixture
def trx(db_path):
    """Buat transaksi MENUNGGU_BAYAR item listing 1 (stok 5, harga 12000) x2."""
    def _buat(items, batas="2999-12-31 23:59:59"):
        c = sqlite3.connect(db_path)
        cur = c.execute(
            "INSERT INTO transaksi (id_pembeli, batas_waktu_bayar) VALUES (2, ?)", (batas,))
        tid = cur.lastrowid
        for id_listing, jumlah in items:
            c.execute(
                "INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan) "
                "VALUES (?, ?, ?, 12000)", (tid, id_listing, jumlah))
        c.commit()
        c.close()
        return tid
    return _buat


@pytest.fixture
def stok(db_path):
    def _stok(id_listing):
        c = sqlite3.connect(db_path)
        try:
            return c.execute(
                "SELECT stok FROM listing_makanan WHERE id_listing = ?", (id_listing,)
            ).fetchone()[0]
        finally:
            c.close()
    return _stok


def _spot(conn, tid):
    baris = conn.execute(
        "SELECT status, kode_pengambilan, waktu_diambil, token_bayar, total_harga "
        "FROM transaksi WHERE id_transaksi = ?", (tid,)).fetchone()
    return baris


# ---------- 1. Flow test: bayar sukses ----------

def test_bayar_via_scan_qr_sukses(conn, db_path, trx, stok):
    tid = trx([(1, 2)])
    ctl = PembayaranController(metode=MetodePalsu(status="BELUM"))

    hasil, items, _ = ctl.konfirmasi_bayar(conn, tid, 2, scan_dikonfirmasi=True)

    assert hasil.status == "LUNAS"
    assert hasil.kode_pengambilan.startswith("SB-")
    assert items[0].jumlah == 2 and items[0].harga_satuan == 12000
    assert stok(1) == 3                       # stok dikurangi tepat setelah bayar
    spot = _spot(conn, tid)
    assert spot["waktu_diambil"] is None      # pengambilan menyusul di UC penjual


def test_bayar_via_status_gateway_lunas(conn, trx, stok):
    """Alternatif: gateway memang sudah tercatat LUNAS, tanpa scan pun bisa."""
    tid = trx([(1, 1)])
    ctl = PembayaranController(metode=MetodePalsu(status="LUNAS"))

    hasil, _, _ = ctl.konfirmasi_bayar(conn, tid, 2, scan_dikonfirmasi=False)

    assert hasil.status == "LUNAS"
    assert stok(1) == 4


# ---------- 2. Exception test ----------

def test_bayar_transaksi_tidak_ada(conn, trx):
    ctl = PembayaranController(metode=MetodePalsu())
    with pytest.raises(PembayaranError) as e:
        ctl.konfirmasi_bayar(conn, 999, 2)
    assert e.value.status_code == 409
    assert e.value.detail == "Transaksi tidak dapat dibayar"


def test_bayar_transaksi_milik_pembeli_lain(conn, trx):
    tid = trx([(1, 1)])
    ctl = PembayaranController(metode=MetodePalsu())
    before = _spot(conn, tid)

    with pytest.raises(PembayaranError) as e:
        ctl.konfirmasi_bayar(conn, tid, 3)          # pembeli 3 mencoba membayar
    assert e.value.status_code == 409
    after = _spot(conn, tid)
    assert dict(before) == dict(after)              # tidak ada perubahan


def test_bayar_ganda_ditolak_di_controller(conn, trx):
    tid = trx([(1, 1)])
    ctl = PembayaranController(metode=MetodePalsu(status="LUNAS"))
    ctl.konfirmasi_bayar(conn, tid, 2)

    with pytest.raises(PembayaranError) as e:
        ctl.konfirmasi_bayar(conn, tid, 2)
    assert e.value.status_code == 409
    assert e.value.detail == "Transaksi tidak dapat dibayar"


# ---------- 3. Alternatif test ----------

def test_tidak_membayar_sampai_batas_waktu_transaksi_jadi_batal(conn, db_path, trx, stok):
    tid = trx([(1, 2)], batas="2000-01-01 00:00:00")
    ctl = PembayaranController(metode=MetodePalsu())

    hasil, _, _ = ctl.konfirmasi_bayar(conn, tid, 2, scan_dikonfirmasi=True)

    assert hasil.status == "BATAL"                  # expasi → pembatalan otomatis
    assert stok(1) == 5                             # stok tidak pernah berkurang
    spot = _spot(conn, tid)
    assert spot["kode_pengambilan"] is None

    # Transaksi BATAL tidak dapat dibayar lagi
    with pytest.raises(PembayaranError) as e:
        ctl.konfirmasi_bayar(conn, tid, 2, scan_dikonfirmasi=True)
    assert e.value.status_code == 409


def test_rollback_menyeluruh_bila_satu_item_gagal(conn, db_path, trx, stok):
    """Listing 1 cukup, listing 2 habis → seluruh pembayaran dibatalkan, tanpa potongan sebagian."""
    tid = trx([(1, 2), (2, 3)])                     # listing 2 hanya stok 1
    ctl = PembayaranController(metode=MetodePalsu(status="LUNAS"))

    with pytest.raises(PembayaranError) as e:
        ctl.konfirmasi_bayar(conn, tid, 2)
    assert e.value.status_code == 409
    assert e.value.detail == "Stok tidak mencukupi"

    assert stok(1) == 5 and stok(2) == 1            # tidak ada stok yang berpindah
    spot = _spot(conn, tid)
    assert spot["status"] == "MENUNGGU_BAYAR"       # masih bisa dibayar ulang setelah stok diisi

    # Simulasikan seller menambah stok → bayar ulang berhasil
    c = sqlite3.connect(db_path)
    c.execute("UPDATE listing_makanan SET stok = 5 WHERE id_listing = 2")
    c.commit()
    c.close()
    hasil, _, _ = PembayaranController(metode=MetodePalsu(status="LUNAS")).konfirmasi_bayar(
        conn, tid, 2)
    assert hasil.status == "LUNAS"


def test_stok_terakhir_berebut_hanya_satu_berhasil(conn, db_path, trx, stok):
    """Dua pembeli membayar transaksi dengan item tersisa 1 → hanya yang pertama LUNAS."""
    t1 = trx([(2, 1)])
    t2 = trx([(2, 1)])
    ctl = PembayaranController(metode=MetodePalsu(status="LUNAS"))

    ok, _, _ = ctl.konfirmasi_bayar(conn, t1, 2)
    with pytest.raises(PembayaranError):
        ctl.konfirmasi_bayar(conn, t2, 2)

    assert ok.status == "LUNAS"
    assert stok(2) == 0                             # tidak menjadi negatif
    assert _spot(conn, t2)["status"] == "MENUNGGU_BAYAR"
