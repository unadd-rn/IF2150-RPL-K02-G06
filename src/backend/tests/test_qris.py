import sqlite3
from backend.adapters.metode_pembayaran import MetodePembayaran
from backend.adapters.payment_gateway_adapter import PaymentGatewayAdapter
from backend.controllers.pembayaran_controller import PembayaranController

def test_cek_status_belum_lunas_sebelum_scan():
    assert PaymentGatewayAdapter().cek_status(1) == "BELUM"

def test_buat_tagihan_membuat_qr_png():
    from types import SimpleNamespace
    data = PaymentGatewayAdapter().buat_tagihan(SimpleNamespace(token_bayar="token-aman"))
    assert data.startswith("data:image/png;base64,")

def test_checkout_dan_detail_punya_kode_qris(client):
    t = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 1}).json()
    assert t["kode_qris"].startswith("data:image/png;base64,")
    assert "/pembayaran/scan/" in t["url_scan"]
    assert ":8000" not in t["url_scan"]
    assert client.get(f"/api/pembayaran/{t['id_transaksi']}").json()["kode_qris"].startswith("data:image/png;base64,")

def test_scan_qr_mengonfirmasi_bayar_dan_mengurangi_stok(client, stok):
    t = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 2}).json()
    token = t["url_scan"].rsplit("/", 1)[-1]
    response = client.post(f"/api/pembayaran/scan/{token}")
    assert response.status_code == 200
    assert response.json() == {"status": "LUNAS"}
    assert client.post(f"/api/pembayaran/scan/{token}").json() == {"status": "LUNAS"}
    assert client.get(f"/api/pembayaran/{t['id_transaksi']}").json()["status"] == "LUNAS"
    assert stok(1) == 3

def test_get_scan_tidak_mengubah_status(client, stok):
    t = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 1}).json()
    token = t["url_scan"].rsplit("/", 1)[-1]
    response = client.get(f"/api/pembayaran/scan/{token}")
    assert response.status_code == 405
    assert client.get(f"/api/pembayaran/{t['id_transaksi']}").json()["status"] == "MENUNGGU_BAYAR"
    assert stok(1) == 5

def test_endpoint_bayar_tidak_bisa_melewati_scan(client, stok):
    t = client.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 1}).json()
    response = client.post(f"/api/pembayaran/{t['id_transaksi']}/bayar")
    assert response.status_code == 402
    assert client.get(f"/api/pembayaran/{t['id_transaksi']}").json()["status"] == "MENUNGGU_BAYAR"
    assert stok(1) == 5

def test_controller_bergantung_pada_interface(db_path):
    class Palsu(MetodePembayaran):
        def buat_tagihan(self, transaksi): return "palsu.png"
        def cek_status(self, id_transaksi): return "BELUM"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _, _, _, qris = PembayaranController(Palsu()).checkout(conn, 2, 1, 1)
    assert qris == "palsu.png"          # proves the adapter is swappable
