from abc import ABC, abstractmethod
from ..models import Transaksi


class MetodePembayaran(ABC):
    @abstractmethod
    def buat_tagihan(self, transaksi: Transaksi) -> str: ...

    @abstractmethod
    def cek_status(self, id_transaksi: int) -> str: ...