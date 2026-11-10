from .metode_pembayaran import MetodePembayaran
from ..errors import PembayaranError
from io import BytesIO
import base64
import qrcode


class PaymentGatewayAdapter(MetodePembayaran):
    def __init__(self, url_gateway: str = "dummy://qris"):
        self.url_gateway = url_gateway

    def buat_tagihan(self, transaksi) -> str:
        if not self.url_gateway:
            raise PembayaranError("Gagal membuat tagihan pembayaran", 502)
        if not getattr(transaksi, "token_bayar", None):
            raise PembayaranError("Token pembayaran tidak tersedia", 500)
        # This QR is a visual demo only. It must never encode a URL that can
        # confirm payment when scanned; confirmation is an explicit UI action.
        image = qrcode.make("SAVEBITE-DEMO-PAYMENT")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    def cek_status(self, id_transaksi: int) -> str:
        # QR scan/callback is the only event that confirms this dummy payment.
        return "BELUM"
