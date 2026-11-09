from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class DataListing(BaseModel):
    nama_makanan: str = Field(..., min_length=1, description="Nama makanan wajib diisi")
    deskripsi: Optional[str] = None
    porsi: str = Field(..., min_length=1, description="Informasi porsi wajib diisi")
    kondisi: str = Field(..., min_length=1, description="Kondisi makanan wajib diisi")
    harga: int = Field(..., ge=0, description="Harga tidak boleh negatif")
    stok: int = Field(..., ge=0, description="Stok tidak boleh negatif")
    batas_kedaluwarsa: datetime = Field(..., description="Waktu kedaluwarsa")
    foto: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_makanan": "Nasi Goreng Spesial",
                "deskripsi": "Masih hangat dan layak makan",
                "porsi": "1 Porsi",
                "kondisi": "Baik",
                "harga": 15000,
                "stok": 5,
                "batas_kedaluwarsa": "2026-12-31T23:59:59",
                "foto": "/uploads/nasi_goreng.jpg"
            }
        }
    )