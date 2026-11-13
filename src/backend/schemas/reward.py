from typing import List

from pydantic import BaseModel


class KuponOut(BaseModel):
    """Kupon untuk RewardView.tampilkanKupon. nilai_potongan dalam rupiah."""
    kode_kupon: str
    nilai_potongan: int
    berlaku_sampai: str
    terpakai: bool
    berlaku: bool


class ProgresReward(BaseModel):
    """Data untuk RewardView.tampilkanProgres(poin, bisaKlaim) + daftar kupon Pembeli."""
    poin_terkumpul: int
    poin_per_klaim: int
    poin_per_login: int
    bisa_klaim: bool
    tanggal_login_terakhir: str | None
    nilai_potongan: int
    kupon: List[KuponOut]
