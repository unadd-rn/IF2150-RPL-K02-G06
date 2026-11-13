"""UC08 mengklaim reward login: Algo-C19-01 dan Algo-C19-02."""
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.routers.auth import get_current_user
from backend.controllers import reward_controller

PEMBELI = {"id_pengguna": 2, "nama": "Pembeli", "email": "b@t.com", "peran": "PEMBELI"}


@pytest.fixture
def api(db_path):
    def _conn():
        c = sqlite3.connect(db_path, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON;")
        try:
            yield c
        finally:
            c.close()

    app.dependency_overrides[reward_controller.get_conn] = _conn
    app.dependency_overrides[get_current_user] = lambda: PEMBELI
    yield TestClient(app)
    app.dependency_overrides.clear()


def _query(db_path, sql, params=()):
    c = sqlite3.connect(db_path)
    try:
        hasil = c.execute(sql, params).fetchall()
        c.commit()
        return hasil
    finally:
        c.close()


def _set_poin(db_path, poin):
    _query(db_path, "INSERT INTO reward_login (id_pembeli, poin_terkumpul) VALUES (2, ?)", (poin,))


def test_progres_tanpa_data_reward_404(api):
    assert api.get("/api/reward").status_code == 404


def test_progres_poin_kurang(api, db_path):
    _set_poin(db_path, 40)
    data = api.get("/api/reward").json()
    assert data["poin_terkumpul"] == 40
    assert data["bisa_klaim"] is False
    assert data["kupon"] == []


def test_klaim_berhasil(api, db_path):
    _set_poin(db_path, 120)
    r = api.post("/api/reward/klaim")
    assert r.status_code == 201
    kupon = r.json()
    assert kupon["kode_kupon"].startswith("SB-")
    assert kupon["nilai_potongan"] == 10_000
    assert kupon["berlaku"] is True

    assert _query(db_path, "SELECT poin_terkumpul FROM reward_login WHERE id_pembeli = 2")[0][0] == 20
    progres = api.get("/api/reward").json()
    assert [k["kode_kupon"] for k in progres["kupon"]] == [kupon["kode_kupon"]]


def test_klaim_poin_tidak_mencukupi(api, db_path):
    _set_poin(db_path, 90)
    r = api.post("/api/reward/klaim")
    assert r.status_code == 400
    assert r.json()["detail"] == "Poin tidak mencukupi"
    assert _query(db_path, "SELECT poin_terkumpul FROM reward_login WHERE id_pembeli = 2")[0][0] == 90
    assert _query(db_path, "SELECT COUNT(*) FROM kupon")[0][0] == 0


def test_penjual_ditolak(api):
    app.dependency_overrides[get_current_user] = lambda: {**PEMBELI, "id_pengguna": 1, "peran": "PENJUAL"}
    assert api.get("/api/reward").status_code == 403
    assert api.post("/api/reward/klaim").status_code == 403
