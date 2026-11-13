"""RewardController (C19): UC08 mengklaim reward login.

GET  /api/reward        -> lihatProgres (Algo-C19-01) + daftar kupon Pembeli
POST /api/reward/klaim  -> klaimReward  (Algo-C19-02)
"""
import secrets
import sqlite3
import string
from datetime import date, timedelta
from typing import Iterator

from fastapi import APIRouter, Depends, HTTPException

from ..models import Kupon, RewardLogin
from ..routers.auth import require_roles
from ..schemas.reward import KuponOut, ProgresReward

NILAI_POTONGAN = 10_000      # rupiah per kupon
MASA_BERLAKU_HARI = 7
_HURUF_KODE = string.ascii_uppercase + string.digits


def get_conn() -> Iterator[sqlite3.Connection]:
    from ..main import get_db_connection  # import di sini agar tidak melingkar
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


router = APIRouter(prefix="/api/reward", tags=["reward"])
hanya_pembeli = require_roles(["PEMBELI"])


def buatKodeUnik() -> str:
    """Kode kupon acak, mis. SB-7KQ2M9XA."""
    return "SB-" + "".join(secrets.choice(_HURUF_KODE) for _ in range(8))


def lihatProgres(conn: sqlite3.Connection, id_pembeli: int) -> RewardLogin:
    """Algo-C19-01"""
    reward = RewardLogin.cariByPembeli(conn, id_pembeli)  # Q-C19-01
    if reward is None:
        raise HTTPException(status_code=404, detail="Data reward tidak ditemukan")
    return reward


def klaimReward(conn: sqlite3.Connection, id_pembeli: int) -> Kupon:
    """Algo-C19-02: kurangi poin dan terbitkan kupon dalam satu transaksi."""
    try:
        conn.execute("BEGIN IMMEDIATE")  # pengganti FOR UPDATE (Q-C19-02)
        reward = RewardLogin.cariByPembeli(conn, id_pembeli)
        if reward is None:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Data reward tidak ditemukan")
        if not reward.cukupUntukKlaim():
            conn.rollback()
            raise HTTPException(status_code=400, detail="Poin tidak mencukupi")

        reward.kurangiPoin(RewardLogin.POIN_PER_KLAIM)
        conn.execute(
            "UPDATE reward_login SET poin_terkumpul = ? WHERE id_pembeli = ?",
            (reward.poin_terkumpul, id_pembeli),
        )  # Q-C19-03

        kupon = Kupon(
            kode_kupon=buatKodeUnik(),
            id_pembeli=id_pembeli,
            nilai_potongan=NILAI_POTONGAN,
            berlaku_sampai=(date.today() + timedelta(days=MASA_BERLAKU_HARI)).isoformat(),
        )
        kupon.simpan(conn)  # Q-C19-04
        conn.commit()
        return kupon
    except HTTPException:
        raise
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Sistem gagal memproses klaim reward")


def _kupon_out(kupon: Kupon) -> KuponOut:
    return KuponOut(
        kode_kupon=kupon.kode_kupon,
        nilai_potongan=kupon.nilai_potongan,
        berlaku_sampai=kupon.berlaku_sampai,
        terpakai=kupon.terpakai,
        berlaku=kupon.is_berlaku(date.today().isoformat()),
    )


@router.get("", response_model=ProgresReward)
def get_progres(user=Depends(hanya_pembeli), conn: sqlite3.Connection = Depends(get_conn)):
    reward = lihatProgres(conn, user["id_pengguna"])
    return ProgresReward(
        poin_terkumpul=reward.poin_terkumpul,
        poin_per_klaim=RewardLogin.POIN_PER_KLAIM,
        poin_per_login=RewardLogin.POIN_PER_LOGIN,
        bisa_klaim=reward.cukupUntukKlaim(),
        tanggal_login_terakhir=reward.tanggal_login_terakhir,
        nilai_potongan=NILAI_POTONGAN,
        kupon=[_kupon_out(k) for k in Kupon.cariByPembeli(conn, user["id_pengguna"])],
    )


@router.post("/klaim", response_model=KuponOut, status_code=201)
def post_klaim(user=Depends(hanya_pembeli), conn: sqlite3.Connection = Depends(get_conn)):
    return _kupon_out(klaimReward(conn, user["id_pengguna"]))
