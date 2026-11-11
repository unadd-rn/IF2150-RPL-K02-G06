"""Unit test penebusan kupon reward pada checkout Pembeli (UC05 + UC08).

Mencakup:
1. Flow test   : kupon dipakai → total_harga dikurangi, kupon ditandai terpakai,
                 potongan melebihi subtotal dibatasi ke 0.
2. Exception   : kupon tak ditemukan, milik pembeli lain, sudah terpakai,
                 kedaluwarsa → transaksi tidak dibuat.
3. Alternatif  : checkout tanpa kupon, harga satuan item tetap penuh, transaksi
                 BATAL karena lewat batas waktu → kupon dikembalikan dan bisa
                 dipakai lagi pembeli yang sama.
"""
import sqlite3
from datetime import date, timedelta

import pytest

from backend.controllers.pembayaran_controller import PembayaranController
from backend.errors import PembayaranError


KUPON_AKTIF = (date.today() + timedelta(days=7)).isoformat()
KUPON_LALU = (date.today() - timedelta(days=1)).isoformat()


@pytest.fixture
def conn(db_path):
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    yield c
    c.close()


@pytest.fixture
def ctl(conn):
    return PembayaranController()


def _semai_kupon(conn, kode="E2E1234", id_pembeli=2, nilai=10_000,
                 berlaku_sampai=KUPON_AKTIF, terpakai=False):
    conn.execute(
        "INSERT INTO kupon (kode_kupon, id_pembeli, nilai_potongan, berlaku_sampai, terpakai) "
        "VALUES (?, ?, ?, ?, ?)", (kode, id_pembeli, nilai, berlaku_sampai, terpakai))
    conn.commit()


def _kupon(conn, kode="E2E1234"):
    return conn.execute("SELECT terpakai FROM kupon WHERE kode_kupon = ?", (kode,)).fetchone()[0]


# ---------- 1. Flow test: kupon dipakai ----------

def test_checkout_dengan_kupon_mengurangi_total(ctl, conn):
    _semai_kupon(conn)
    trx, items, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon="E2E1234")

    assert trx.total_harga == 12_000 - 10_000            # diskon diterapkan
    assert trx.kode_kupon == "E2E1234"
    assert items[0].harga_satuan == 12_000               # harga item tetap penuh
    assert _kupon(conn) == 1                             # kupon tercatat terpakai


def test_checkout_multi_item_dengan_kupon(ctl, conn):
    _semai_kupon(conn)
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 2), (2, 1)], kode_kupon="E2E1234")

    assert trx.total_harga == (2 * 12_000 + 15_000) - 10_000


def test_potongan_lebih_besar_dari_subtotal_dibatasi_nol(ctl, conn):
    _semai_kupon(conn, kode="GEDE12", nilai=999_999)
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon="GEDE12")

    assert trx.total_harga == 0                          # tidak pernah negatif


def test_checkout_tanpa_kupon_tetap_sama(ctl, conn):
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 2)], kode_kupon=None)

    assert trx.total_harga == 2 * 12_000
    assert trx.kode_kupon is None


# ---------- 2. Exception test ----------

@pytest.mark.parametrize("semaikan, kode, status, pesan", [
    (False, "TAKADA12", 404, "Kupon tidak ditemukan"),          # kode tak pernah ada
    (True, "MILIK03", 404, "Kupon tidak ditemukan"),            # milik pembeli lain
    (True, "PAKAIL1", 400, "Kupon sudah terpakai"),
    (True, "LALUS12", 400, "Kupon sudah kedaluwarsa"),
], ids=["tidak-ada", "milik-orang", "sudah-terpakai", "kedaluwarsa"])
def test_checkout_kupon_ditolak(ctl, conn, semaikan, kode, status, pesan):
    if semaikan:
        if kode == "MILIK03":
            _semai_kupon(conn, kode=kode, id_pembeli=3)
        elif kode == "PAKAIL1":
            _semai_kupon(conn, kode=kode, terpakai=True)
        else:
            _semai_kupon(conn, kode=kode, berlaku_sampai=KUPON_LALU)   # kedaluwarsa

    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon=kode)

    assert e.value.status_code == status
    assert e.value.detail == pesan
    # tidak ada transaksi yang tersimpan dan kupon tidak ikut berubah
    assert conn.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0] == 0


def test_kupon_sudah_terpakai_tidak_dikembalikan_oleh_checkout_gagal(ctl, conn):
    _semai_kupon(conn, terpakai=True)
    with pytest.raises(PembayaranError):
        ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon="E2E1234")

    assert _kupon(conn) == 1     # tetap terpakai, tidak dikembalikan oleh checkout gagal


# ---------- 3. Alternatif test ----------

def test_transaksi_batal_bawa_kupon_kembali(ctl, conn):
    """Checkout dengan kupon → lupa bayar sampai batas → BATAL → kupon bisa dipakai lagi."""
    _semai_kupon(conn)
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon="E2E1234")
    assert _kupon(conn) == 1

    conn.execute("UPDATE transaksi SET batas_waktu_bayar = '2000-01-01 00:00:00' WHERE id_transaksi = ?",
                 (trx.id_transaksi,))
    conn.commit()
    hasil, _, _ = ctl.konfirmasi_bayar(conn, trx.id_transaksi, 2, scan_dikonfirmasi=True)
    assert hasil.status == "BATAL"
    assert _kupon(conn) == 0                              # dikembalikan otomatis

    trx_lagi, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)], kode_kupon="E2E1234")
    assert trx_lagi.total_harga == 2_000                  # bisa ditebus ulang


def test_kupon_tidak_dikembalikan_bila_punya_pembeli_lain(ctl, conn):
    """Pembeli lain tidak bisa menyalahgunakan kupon untuk mengembalikan milik orang lain."""
    _semai_kupon(conn, kode="MILIK03", id_pembeli=3)
    trx, _, _, _ = ctl.checkout_banyak(conn, 3, [(1, 1)], kode_kupon="MILIK03")

    conn.execute("UPDATE transaksi SET id_pembeli = 2, batas_waktu_bayar = '2000-01-01 00:00:00' "
                 "WHERE id_transaksi = ?", (trx.id_transaksi,))
    conn.commit()
    hasil, _, _ = ctl.konfirmasi_bayar(conn, trx.id_transaksi, 2, scan_dikonfirmasi=True)
    assert hasil.status == "BATAL"
    assert _kupon(conn, "MILIK03") == 1                   # kupon milik orang lain tak tersentuh
