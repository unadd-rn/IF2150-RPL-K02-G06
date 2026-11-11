"""Unit test PembayaranController.checkout_banyak dari sudut pandang Pembeli (UC05).

Mencakup:
1. Flow test   : checkout sukses (satu / beberapa listing, bentuk keranjang).
2. Exception   : pesanan kosong, jumlah tidak valid, listing tidak tersedia,
                 stok tidak mencukupi.
3. Alternatif  : penggabungan item yang sama, harga mengikuti saat checkout,
                 token unik, transaksi keseluruhan dibatalkan bila insert gagal.

Unit level: controller dipanggil langsung dengan koneksi sqlite ke basis data sementara.
"""
import sqlite3
from datetime import datetime, timedelta

import pytest

from backend.adapters.metode_pembayaran import MetodePembayaran
from backend.controllers.pembayaran_controller import (
    BATAS_WAKTU_BAYAR,
    PembayaranController,
)
from backend.errors import PembayaranError


@pytest.fixture
def conn(db_path):
    """Koneksi langsung ke basis data uji + listing tambahan untuk skenario alternatif."""
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    c.executescript("""
        INSERT INTO listing_makanan
            (id_listing, id_penjual, nama_makanan, porsi, kondisi, harga, stok,
             batas_kedaluwarsa, aktif)
            VALUES (3, 1, 'Kue Kedaluwarsa', '1 porsi', 'Baik', 10000, 3, '2000-01-01 00:00:00', 1),
                   (4, 1, 'Donat Nonaktif', '1 box', 'Baik', 8000, 3, '2999-12-31 23:59:59', 0),
                   (5, 1, 'Brownis Draft', '1 potong', 'Baik', 9000, 3, '2999-12-31 23:59:59', 1),
                   (6, 1, 'Puding Stok Habis', '1 cup', 'Baik', 7000, 0, '2999-12-31 23:59:59', 1);
        UPDATE listing_makanan SET draft = 1 WHERE id_listing = 5;
    """)
    c.commit()
    yield c
    c.close()


class MetodePalsu(MetodePembayaran):
    """Metode pembayaran palsu agar unit test tidak memakai gateway beneran."""
    def buat_tagihan(self, transaksi) -> str:
        return "tagihan-palsu"

    def cek_status(self, id_transaksi: int) -> str:
        return "BELUM"


@pytest.fixture
def ctl(conn):
    return PembayaranController(metode=MetodePalsu())


def _transaksi_semua(conn):
    return conn.execute("SELECT id_transaksi, status, total_harga FROM transaksi").fetchall()


# ---------- 1. Flow test: checkout sukses ----------

def test_checkout_satu_listing_sukses(ctl, conn):
    trx, items, nama, tagihan = ctl.checkout_banyak(conn, 2, [(1, 2)])

    assert trx.id_pembeli == 2
    assert trx.status == "MENUNGGU_BAYAR"
    assert trx.total_harga == 2 * 12000
    assert [(i.id_listing, i.jumlah, i.harga_satuan) for i in items] == [(1, 2, 12000)]
    assert nama == {1: "Roti"}
    assert tagihan == "tagihan-palsu"
    assert trx.token_bayar            # token pembayaran tidak null
    assert trx.kode_pengambilan is None          # masih belum bayar
    assert trx.waktu_diambil is None


def test_checkout_keranjang_multi_listing(ctl, conn):
    trx, items, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1), (2, 1)])

    assert trx.total_harga == 12000 + 15000
    assert {i.id_listing for i in items} == {1, 2}


def test_checkout_menyimpan_batas_waktu_15_menit(ctl, conn):
    sebelum = datetime.now().replace(microsecond=0)
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)])
    sesudah = datetime.now().replace(microsecond=0)

    batas = datetime.fromisoformat(str(trx.batas_waktu_bayar))
    assert sebelum + BATAS_WAKTU_BAYAR <= batas <= sesudah + BATAS_WAKTU_BAYAR


def test_checkout_tidak_mengurangi_stok(ctl, conn, db_path):
    ctl.checkout_banyak(conn, 2, [(1, 2)])

    stok = sqlite3.connect(db_path).execute(
        "SELECT stok FROM listing_makanan WHERE id_listing = 1").fetchone()[0]
    assert stok == 5


def test_checkout_merekam_harga_listing_saat_checkout(ctl, conn):
    """Harga di-snapshot: perubahan harga listing setelah checkout tidak mengubah item harga lama."""
    trx_lama, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)])
    conn.execute("UPDATE listing_makanan SET harga = 9999 WHERE id_listing = 1")
    trx_baru, items_baru, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)])

    assert items_baru[0].harga_satuan == 9999           # harga terbaru dipakai
    assert trx_lama.total_harga == 12000                # transaksi lama tetap


def test_token_bayar_berbeda_antar_transaksi(ctl, conn):
    t1, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)])
    t2, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 1)])

    assert t1.token_bayar != t2.token_bayar


# ---------- 2. Exception test ----------

@pytest.mark.parametrize("pesanan, pesan", [
    ([], "Pesanan tidak boleh kosong"),
    ([(1, 0)], "Jumlah porsi tidak valid"),
    ([(1, -2)], "Jumlah porsi tidak valid"),
    ([(1, 1), (2, 0)], "Jumlah porsi tidak valid"),
])
def test_checkout_pesanan_tidak_valid(ctl, conn, pesanan, pesan):
    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, pesanan)
    assert e.value.status_code == 400
    assert e.value.detail == pesan
    assert _transaksi_semua(conn) == []          # tidak ada transaksi tersimpan


def test_checkout_listing_tidak_ada(ctl, conn):
    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, [(999, 1)])
    assert e.value.status_code == 404
    assert e.value.detail == "Listing tidak tersedia"


@pytest.mark.parametrize("id_listing", [3, 4, 5, 6], ids=["kedaluwarsa", "nonaktif", "draft", "stok-habis"])
def test_checkout_listing_tidak_tersedia(ctl, conn, id_listing):
    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, [(id_listing, 1)])
    assert e.value.status_code == 404
    assert e.value.detail == "Listing tidak tersedia"


def test_checkout_stok_tidak_mencukupi(ctl, conn):
    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, [(2, 2)])   # listing 2 hanya stok 1
    assert e.value.status_code == 409
    assert e.value.detail == "Stok tidak mencukupi"


def test_checkout_pesanan_valid_dibatalkan_menyeluruh(ctl, conn):
    """Item pertama valid, item kedua gagal → seluruh transaksi tidak dibuat."""
    with pytest.raises(PembayaranError):
        ctl.checkout_banyak(conn, 2, [(1, 1), (999, 1)])

    assert _transaksi_semua(conn) == []
    # stok juga tidak berubah
    stok = conn.execute("SELECT stok FROM listing_makanan WHERE id_listing = 1").fetchone()[0]
    assert stok == 5


# ---------- 3. Alternatif test ----------

def test_checkout_jumlah_item_sama_digabung_sebelum_validasi(ctl, conn):
    """(1,3) + (1,3) = 6 > stok 5 → ditolak walaupun masing-masing cukup."""
    with pytest.raises(PembayaranError) as e:
        ctl.checkout_banyak(conn, 2, [(1, 3), (1, 3)])
    assert e.value.status_code == 409
    assert e.value.detail == "Stok tidak mencukupi"


def test_checkout_gabungan_tepat_sama_dengan_stok_diperbolehkan(ctl, conn):
    trx, items, _, _ = ctl.checkout_banyak(conn, 2, [(1, 3), (1, 2)])

    assert trx.total_harga == 5 * 12000
    # digabung jadi satu item agar porsi dikurangi sekaligus
    assert [(i.jumlah, i.harga_satuan) for i in items] == [(5, 12000)]


def test_checkout_tepat_sama_dengan_stok_satu_beberapa_item(ctl, conn):
    trx, _, _, _ = ctl.checkout_banyak(conn, 2, [(1, 5)])
    assert trx.total_harga == 5 * 12000


def test_checkout_bentuk_lama_satu_listing_setara_checkout_banyak(ctl, conn):
    trx, items, nama, tagihan = ctl.checkout(conn, 2, 1, 2)

    assert trx.total_harga == 2 * 12000
    assert [(i.id_listing, i.jumlah, i.harga_satuan) for i in items] == [(1, 2, 12000)]
    assert nama == {1: "Roti"}
    assert tagihan == "tagihan-palsu"


def test_transaksi_beberapa_pembeli_terpisah(ctl, conn, db_path):
    """Pembeli lain tidak melihat transaksi milik pembeli 2 saat ambil ulang lewat controller."""
    ctl.checkout_banyak(conn, 2, [(1, 1)])

    baris = conn.execute("SELECT id_pembeli FROM transaksi").fetchall()
    assert [b["id_pembeli"] for b in baris] == [2]
