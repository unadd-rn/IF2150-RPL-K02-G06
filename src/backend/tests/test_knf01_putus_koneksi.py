"""KNF01-TC04: tidak ada data tersangkut bila koneksi/proses putus di tengah transaksi.

Pengganti `kill -9` yang portabel (Windows/macOS/Linux):
1. Proses mati : konfirmasi_bayar dijalankan di subprocess yang dihentikan paksa
                 (`os._exit`, tanpa rollback/close/flush) tepat setelah stok dikurangi
                 dan status diubah LUNAS, sebelum COMMIT.
2. Koneksi error: koneksi melempar sqlite3.OperationalError di tengah transaksi
                 (setelah item pertama dikurangi), meniru I/O/koneksi gagal.

Keduanya diperiksa dari koneksi baru: stok dan status tidak berubah, basis data tidak
terkunci, dan transaksi masih bisa dibayar ulang.
"""
import os
import sqlite3
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from backend.adapters.metode_pembayaran import MetodePembayaran
from backend.controllers.pembayaran_controller import PembayaranController

SRC_DIR = Path(__file__).resolve().parents[2]      # folder yang berisi paket `backend`


class MetodeLunas(MetodePembayaran):
    def buat_tagihan(self, transaksi) -> str:
        return "tagihan-palsu"

    def cek_status(self, id_transaksi: int) -> str:
        return "LUNAS"


@pytest.fixture
def buat_trx(db_path):
    """Transaksi MENUNGGU_BAYAR milik pembeli 2. items = [(id_listing, jumlah), ...]."""
    def _buat(items):
        c = sqlite3.connect(db_path)
        tid = c.execute(
            "INSERT INTO transaksi (id_pembeli, batas_waktu_bayar) VALUES (2, '2999-12-31 23:59:59')"
        ).lastrowid
        for id_listing, jumlah in items:
            c.execute(
                "INSERT INTO item_transaksi (id_transaksi, id_listing, jumlah, harga_satuan) "
                "VALUES (?, ?, ?, 12000)", (tid, id_listing, jumlah))
        c.commit()
        c.close()
        return tid
    return _buat


def _status(db_path, tid):
    c = sqlite3.connect(db_path)
    try:
        return c.execute(
            "SELECT status, kode_pengambilan FROM transaksi WHERE id_transaksi = ?", (tid,)
        ).fetchone()
    finally:
        c.close()


def _bayar_ulang(db_path, tid):
    c = sqlite3.connect(db_path, timeout=1)
    c.row_factory = sqlite3.Row
    try:
        hasil, _, _ = PembayaranController(metode=MetodeLunas()).konfirmasi_bayar(c, tid, 2)
        return hasil.status
    finally:
        c.close()


SKRIP_PROSES_MATI = textwrap.dedent("""
    import os, sqlite3, sys
    from backend.adapters.metode_pembayaran import MetodePembayaran
    from backend.controllers.pembayaran_controller import PembayaranController

    db_path, tid = sys.argv[1], int(sys.argv[2])

    class MetodeLunas(MetodePembayaran):
        def buat_tagihan(self, transaksi): return "x"
        def cek_status(self, id_transaksi): return "LUNAS"

    class KoneksiMatiSebelumCommit:
        # Meneruskan semua pemanggilan ke koneksi asli, tetapi mematikan proses
        # sesaat sebelum COMMIT dikirim.
        def __init__(self, c): self._c = c
        def __getattr__(self, nama): return getattr(self._c, nama)
        def execute(self, *a, **k): return self._c.execute(*a, **k)
        def commit(self):
            print("MATI_SEBELUM_COMMIT", flush=True)
            os._exit(9)

    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    PembayaranController(metode=MetodeLunas()).konfirmasi_bayar(KoneksiMatiSebelumCommit(c), tid, 2)
    print("TIDAK_BOLEH_SAMPAI_SINI", flush=True)
""")


def test_proses_mati_sebelum_commit_tidak_meninggalkan_data(db_path, buat_trx, stok):
    tid = buat_trx([(1, 2), (2, 1)])

    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    hasil = subprocess.run(
        [sys.executable, "-c", SKRIP_PROSES_MATI, db_path, str(tid)],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert "MATI_SEBELUM_COMMIT" in hasil.stdout, hasil.stderr
    assert hasil.returncode == 9                      # proses benar-benar mati di tengah transaksi

    # Dari koneksi baru: tidak ada perubahan yang tersimpan
    assert stok(1) == 5 and stok(2) == 1
    status, kode = _status(db_path, tid)
    assert status == "MENUNGGU_BAYAR" and kode is None

    # Kunci tulis sudah lepas dan transaksi bisa dibayar ulang
    assert _bayar_ulang(db_path, tid) == "LUNAS"
    assert stok(1) == 3 and stok(2) == 0


class KoneksiPutusDiTengah:
    """Melempar OperationalError saat UPDATE stok kedua, meniru koneksi/I-O gagal."""

    def __init__(self, c):
        self._c = c
        self.update_stok = 0

    def __getattr__(self, nama):
        return getattr(self._c, nama)

    def execute(self, sql, *a, **k):
        if sql.lstrip().startswith("UPDATE listing_makanan"):
            self.update_stok += 1
            if self.update_stok == 2:
                raise sqlite3.OperationalError("disk I/O error (simulasi koneksi putus)")
        return self._c.execute(sql, *a, **k)


def test_koneksi_error_di_tengah_transaksi_dirollback(db_path, buat_trx, stok):
    tid = buat_trx([(1, 2), (2, 1)])
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    koneksi = KoneksiPutusDiTengah(c)

    with pytest.raises(sqlite3.OperationalError):
        PembayaranController(metode=MetodeLunas()).konfirmasi_bayar(koneksi, tid, 2)
    assert koneksi.update_stok == 2                   # item pertama sempat dikurangi
    c.close()

    assert stok(1) == 5 and stok(2) == 1              # potongan item pertama ikut dibatalkan
    status, kode = _status(db_path, tid)
    assert status == "MENUNGGU_BAYAR" and kode is None
    assert _bayar_ulang(db_path, tid) == "LUNAS"
