from fastapi import APIRouter, Cookie, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
from datetime import date, datetime, timedelta
import bcrypt
import secrets
from typing import Iterable
from backend.validation import Validasi
from backend.models import DATABASE_NAME, RewardLogin

router = APIRouter(prefix="/api/auth", tags=["Auth"])
SESSION_DURATION_HOURS = 24

class LoginRequest(BaseModel):
    email: str
    password: str


def _ambil_pengguna_dari_sesi(token: str):
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT p.id_pengguna, p.nama, p.email,
                   CASE WHEN pb.id_pengguna IS NOT NULL THEN 'PEMBELI' ELSE 'PENJUAL' END AS peran,
                   s.kedaluwarsa_pada
            FROM auth_session s
            JOIN pengguna p ON p.id_pengguna = s.id_pengguna
            LEFT JOIN pembeli pb ON pb.id_pengguna = p.id_pengguna
            WHERE s.token = ?
            """,
            (token,),
        )
        row = cursor.fetchone()

        if not row:
            return None

        exp = datetime.fromisoformat(row["kedaluwarsa_pada"])
        if datetime.now() >= exp:
            cursor.execute("DELETE FROM auth_session WHERE token = ?", (token,))
            conn.commit()
            return None

        return {
            "id_pengguna": row["id_pengguna"],
            "nama": row["nama"],
            "email": row["email"],
            "peran": row["peran"],
        }
    finally:
        conn.close()


def get_current_user(
    session_token: str | None = Cookie(default=None),
    authorization: str | None = Header(default=None),
):
    token = session_token
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(status_code=401, detail="Sesi tidak ditemukan")

    user = _ambil_pengguna_dari_sesi(token)
    if not user:
        raise HTTPException(status_code=401, detail="Sesi tidak valid atau sudah kedaluwarsa")

    return user


def require_roles(allowed_roles: Iterable[str]):
    allowed = set(allowed_roles)

    def _role_guard(user=Depends(get_current_user)):
        if user["peran"] not in allowed:
            raise HTTPException(status_code=403, detail="Anda tidak memiliki akses ke endpoint ini")
        return user

    return _role_guard

@router.post("/login")
def login(req: LoginRequest):
    # 1. Validasi Format Input
    errors = Validasi.validasiKredensial(req.email, req.password)
    if errors:
        raise HTTPException(status_code=400, detail=", ".join(errors))

    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Q-C15-01: Cari pengguna
        cursor.execute("""
            SELECT p.id_pengguna, p.nama, p.email, p.password, 
            CASE WHEN pb.id_pengguna IS NOT NULL THEN 'PEMBELI' ELSE 'PENJUAL' END AS peran 
            FROM pengguna p 
            LEFT JOIN pembeli pb ON pb.id_pengguna = p.id_pengguna 
            WHERE p.email = ?;
        """, (req.email,))
        user = cursor.fetchone()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail="Sistem gagal memproses login")

    # 2. Verifikasi Kredensial di luar blok try-catch utama agar 401 tidak terdistorsi menjadi 500
    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="Email atau password salah")

    if not bcrypt.checkpw(req.password.encode('utf-8'), user['password'].encode('utf-8')):
        conn.close()
        raise HTTPException(status_code=401, detail="Email atau password salah")

    peran = user['peran']
    id_pengguna = user['id_pengguna']

    # 3. Transaksi Reward Login khusus Pembeli (catat login harian lewat RewardLogin)
    if peran == 'PEMBELI':
        try:
            conn.execute("BEGIN IMMEDIATE")  # pengganti FOR UPDATE di SQLite (Q-C15-02)
            reward = RewardLogin.cariByPembeli(conn, id_pengguna)
            if reward is None:
                # Pembeli lama yang belum punya baris reward: buatkan dulu
                cursor.execute("INSERT INTO reward_login (id_pembeli) VALUES (?)", (id_pengguna,))
                reward = RewardLogin.cariByPembeli(conn, id_pengguna)

            if reward.catatLogin(date.today().isoformat()):
                cursor.execute(
                    "UPDATE reward_login SET poin_terkumpul = ?, tanggal_login_terakhir = ? "
                    "WHERE id_pembeli = ?",
                    (reward.poin_terkumpul, reward.tanggal_login_terakhir, id_pengguna),
                )  # Q-C15-03
            conn.commit()
        except Exception:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=500, detail="Sistem gagal memproses reward login")

    session_token = secrets.token_urlsafe(32)
    expired_at = (datetime.now() + timedelta(hours=SESSION_DURATION_HOURS)).strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute(
            """
            INSERT INTO auth_session (token, id_pengguna, kedaluwarsa_pada)
            VALUES (?, ?, ?)
            """,
            (session_token, id_pengguna, expired_at),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Sistem gagal membuat sesi login")

    conn.close()

    response = JSONResponse({"id_pengguna": id_pengguna, "nama": user['nama'], "peran": peran})
    response.set_cookie(
        key="session_token", value=session_token,
        max_age=SESSION_DURATION_HOURS * 3600,
        httponly=True, samesite="lax", path="/",
    )
    response.set_cookie(
        key="role", value=peran,
        max_age=SESSION_DURATION_HOURS * 3600,
        httponly=True, samesite="lax", path="/",
    )
    return response


@router.post("/logout")
def logout(session_token: str | None = Cookie(default=None)):
    """Hapus sesi aktif (baris auth_session) lalu hapus cookie sesi dari peramban.
    Dilakukan di server karena cookie session_token bertanda httpOnly."""
    if session_token:
        conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        try:
            conn.execute("DELETE FROM auth_session WHERE token = ?", (session_token,))
            conn.commit()
        finally:
            conn.close()

    response = JSONResponse({"message": "Berhasil keluar"})
    response.delete_cookie(key="session_token", path="/")
    response.delete_cookie(key="role", path="/")
    return response