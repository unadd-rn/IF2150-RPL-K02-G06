import sqlite3
import os
import secrets
from dataclasses import asdict
from fastapi import APIRouter, Depends

from ..models import DATABASE_NAME
from ..errors import PembayaranError
from ..routers.auth import require_roles
from ..schemas.pembayaran import CheckoutRequest, ItemOut, TransaksiOut
from ..controllers.pembayaran_controller import PembayaranController, ambil_transaksi

router = APIRouter(prefix="/api/pembayaran", tags=["pembayaran"])


def get_conn():
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def get_controller() -> PembayaranController:
    return PembayaranController()


def _keluaran(trx, items, nama, kode_qris=None) -> TransaksiOut:
    web_url = os.getenv("SAVEBITE_PUBLIC_WEB_URL", "http://localhost:3000").rstrip("/")
    return TransaksiOut(
        **asdict(trx),
        items=[ItemOut(**asdict(i), nama_makanan=nama.get(i.id_listing, "")) for i in items],
        kode_qris=kode_qris,
        url_scan=f"{web_url}/pembayaran/scan/{trx.token_bayar}" if trx.token_bayar else None,
    )


@router.post("/checkout", response_model=TransaksiOut)
def checkout(body: CheckoutRequest, conn=Depends(get_conn),
             ctl: PembayaranController = Depends(get_controller),
             user=Depends(require_roles(["PEMBELI"]))):
    pesanan = body.daftar_pesanan()
    trx, items, nama, kode_qris = ctl.checkout_banyak(
        conn, user["id_pengguna"], pesanan, body.kode_kupon)
    return _keluaran(trx, items, nama, kode_qris)


@router.get("/{id_transaksi}", response_model=TransaksiOut)
def detail(id_transaksi: int, conn=Depends(get_conn),
           ctl: PembayaranController = Depends(get_controller),
           user=Depends(require_roles(["PEMBELI"]))):
    trx, items, nama = ambil_transaksi(conn, id_transaksi)
    if trx is None or trx.id_pembeli != user["id_pengguna"]:
        raise PembayaranError("Transaksi tidak ditemukan", 404)
    if trx.status == "MENUNGGU_BAYAR" and not trx.token_bayar:
        trx.token_bayar = secrets.token_urlsafe(32)
        conn.execute(
            "UPDATE transaksi SET token_bayar = ? WHERE id_transaksi = ? AND token_bayar IS NULL",
            (trx.token_bayar, id_transaksi),
        )
        conn.commit()
        trx, items, nama = ambil_transaksi(conn, id_transaksi)
    return _keluaran(trx, items, nama, ctl.metode.buat_tagihan(trx))


@router.post("/scan/{token_bayar}", include_in_schema=False)
def konfirmasi_scan_qr(token_bayar: str, conn=Depends(get_conn),
                       ctl: PembayaranController = Depends(get_controller)):
    """Confirms only the pending transaction identified by the QR capability token."""
    row = conn.execute(
        "SELECT id_transaksi, id_pembeli, status FROM transaksi WHERE token_bayar = ?",
        (token_bayar,),
    ).fetchone()
    if row is None:
        raise PembayaranError("QR pembayaran tidak valid", 404)
    if row["status"] == "LUNAS":
        return {"status": "LUNAS"}
    if row["status"] != "MENUNGGU_BAYAR":
        raise PembayaranError("Transaksi sudah tidak dapat dibayar", 409)
    try:
        trx, _, _ = ctl.konfirmasi_bayar(
            conn, row["id_transaksi"], row["id_pembeli"], scan_dikonfirmasi=True
        )
    except PembayaranError:
        # A repeated browser request may race with the first confirmation.
        refreshed = conn.execute(
            "SELECT status FROM transaksi WHERE id_transaksi = ?", (row["id_transaksi"],)
        ).fetchone()
        if refreshed is not None and refreshed["status"] == "LUNAS":
            return {"status": "LUNAS"}
        raise
    return {"status": trx.status}

@router.post("/{id_transaksi}/bayar", response_model=TransaksiOut)
def bayar(id_transaksi: int, conn=Depends(get_conn),
          ctl: PembayaranController = Depends(get_controller),
          user=Depends(require_roles(["PEMBELI"]))):
    # This endpoint can only confirm a status received from the payment adapter.
    # The dummy adapter returns BELUM; QR scan is the explicit confirmation path.
    trx, items, nama = ctl.konfirmasi_bayar(conn, id_transaksi, user["id_pengguna"])
    return _keluaran(trx, items, nama)
