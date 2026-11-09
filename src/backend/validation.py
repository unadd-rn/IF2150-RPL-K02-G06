import re
from typing import Any, Dict, List
from datetime import datetime
from typing import List, Dict, Any

from .schemas.listing_schema import DataListing

class Validasi:
    @staticmethod
    def validasiKredensial(email: str, password: str) -> List[str]:
        daftarError = []
        
        if not email:
            daftarError.append("Email wajib diisi")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            daftarError.append("Format email tidak valid")
            
        if not password:
            daftarError.append("Password wajib diisi")
            
        return daftarError

    @staticmethod
    def validasiListing(data: Dict[str, Any] | DataListing) -> List[str]:
        daftar_error: List[str] = []
        
        # Konversi ke dict jika input berupa pydantic model
        payload = data.model_dump() if isinstance(data, DataListing) else data

        # Validasi Field Wajib & String Kosong
        for field, label in [
            ("nama_makanan", "Nama makanan"),
            ("porsi", "Porsi"),
            ("kondisi", "Kondisi makanan"),
        ]:
            val = payload.get(field)
            if not val or not str(val).strip():
                daftar_error.append(f"{label} wajib diisi")

        # Validasi Harga
        harga = payload.get("harga")
        if harga is None:
            daftar_error.append("Harga wajib diisi")
        elif isinstance(harga, (int, float)) and harga < 0:
            daftar_error.append("Harga tidak boleh negatif")

        # Validasi Stok
        stok = payload.get("stok")
        if stok is None:
            daftar_error.append("Stok wajib diisi")
        elif isinstance(stok, int) and stok < 0:
            daftar_error.append("Stok tidak boleh negatif")

        # Validasi Batas Kedaluwarsa
        batas_kedaluwarsa = payload.get("batas_kedaluwarsa")
        if not batas_kedaluwarsa:
            daftar_error.append("Batas kedaluwarsa wajib diisi")
        else:
            if isinstance(batas_kedaluwarsa, str):
                try:
                    batas_kedaluwarsa = datetime.fromisoformat(batas_kedaluwarsa)
                except ValueError:
                    daftar_error.append("Format batas kedaluwarsa tidak valid")
                    batas_kedaluwarsa = None

            if isinstance(batas_kedaluwarsa, datetime) and batas_kedaluwarsa <= datetime.now():
                daftar_error.append("Batas kedaluwarsa harus lebih dari waktu sekarang")

        return daftar_error