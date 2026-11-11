from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemCheckoutRequest(BaseModel):
    id_listing: int
    jumlah: int            # validated in the controller so you get the DPPL error message


class CheckoutRequest(BaseModel):
    # Bentuk lama (satu listing): id_listing + jumlah.
    # Bentuk baru (dari keranjang): items = daftar {id_listing, jumlah}.
    # kode_kupon (opsional): kupon reward yang ingin dipakai pembeli (UC05).
    id_listing: int | None = None
    jumlah: int | None = None
    items: list[ItemCheckoutRequest] | None = None
    kode_kupon: str | None = None

    def daftar_pesanan(self) -> list[tuple[int, int]]:
        """Menyatukan kedua bentuk request menjadi daftar (id_listing, jumlah)."""
        if self.items:
            return [(i.id_listing, i.jumlah) for i in self.items]
        if self.id_listing is not None and self.jumlah is not None:
            return [(self.id_listing, self.jumlah)]
        return []   # controller raises 400 "Pesanan tidak boleh kosong"


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_listing: int
    jumlah: int
    harga_satuan: int
    nama_makanan: str

class TransaksiOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_transaksi: int
    status: str
    total_harga: int
    batas_waktu_bayar: datetime
    kode_pengambilan: str | None = None
    items: list[ItemOut]
    kode_qris: str | None = None
    url_scan: str | None = None
