from typing import Optional

from pydantic import BaseModel, ConfigDict


class ListingKatalog(BaseModel):
    """Data listing yang dikirim ke KatalogView (UC02 kartu, UC03 detail).
    Nama & alamat toko asal listing ikut dikirim agar pembeli tahu toko mana
    yang menjual dan di mana makanan diambil."""

    model_config = ConfigDict(from_attributes=True)

    id_listing: int
    id_penjual: int
    nama_toko: str
    alamat_toko: str
    nama_makanan: str
    deskripsi: Optional[str] = None
    porsi: str
    kondisi: str
    # Path relatif, mis. "uploads/listing/<uuid>.jpg". Frontend: NEXT_PUBLIC_API_URL + "/" + foto
    foto: Optional[str] = None
    harga: int
    stok: int
    batas_kedaluwarsa: str
