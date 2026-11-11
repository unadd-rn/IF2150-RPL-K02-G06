"""E2E alur Pembeli (UC02–UC05, UC07, UC08) lewat seluruh aplikasi FastAPI.

Berbeda dengan test lain di folder ini, test di sini **tidak** menggantikan
dependency get_current_user: login, sesi cookie, role guard, katalog, checkout,
pembayaran QR, reward, sampai pesanan penjual berjalan penuh lewat endpoint
nyata semuanya diarahkan ke basis data sementara (tmp_path).

Cakupan:
1. Flow test   : login → katalog → checkout → bayar QR → LUNAS → penjual menandai
                 diambil; login → katalog → cari/nyaring.
2. Exception   : belum login, role penjual, validasi checkout, akses transaksi
                 orang lain, QR palsu.
3. Alternatif  : tidak membayar sampai tenggat → BATAL tidak bisa dibayar lagi,
                 bayar ganda idempoten, reward login & klaim kupon.
"""
import sqlite3

import bcrypt
import pytest
from fastapi.testclient import TestClient
from types import SimpleNamespace

from backend import main, models
from backend.api import pembayaran_routes, penjualan_routes, toko_routes
from backend.routers import auth

PASSWORD = "password123"
HASH = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt(10)).decode()

SUDAH_KEDALUWARSA = "2999-12-31 23:59:59"   # batas waktu bayar masih jauh
SUDAH_LEWAT = "2000-01-01 00:00:00"         # batas waktu bayar sudah lewat

# Modul yang memegang salinan DATABASE_NAME → semuanya diarahkan ke basis data uji
MODUL_DATABASE = (models, main, auth, pembayaran_routes, penjualan_routes, toko_routes)


@pytest.fixture
def e2e(monkeypatch, tmp_path):
    """Aplikasi utuh di atas basis data sementara + helper login/SQL/stok."""
    path = str(tmp_path / "e2e.db")
    models.init_db(path)

    c = None
    try:
        c = sqlite3.connect(path)
        c.executescript(f"""
            INSERT INTO pengguna (id_pengguna, nama, email, password)
                VALUES (1, 'Penjual', 'penjual@t.com', '{HASH}'),
                       (2, 'Pembeli Satu', 'b1@t.com', '{HASH}'),
                       (3, 'Pembeli Dua', 'b2@t.com', '{HASH}');
            INSERT INTO penjual VALUES (1, 'Toko Roti', 'Jl. A No. 1');
            INSERT INTO pembeli VALUES (2, 'akun1'), (3, 'akun2');

            INSERT INTO listing_makanan
                (id_listing, id_penjual, nama_makanan, deskripsi, porsi, kondisi,
                 harga, stok, batas_kedaluwarsa, aktif)
                VALUES (1, 1, 'Roti', 'roti kenyal', '1 pack', 'Baik', 12000, 5, '{SUDAH_KEDALUWARSA}', 1),
                       (2, 1, 'Nasi', 'nasi hangat', '1 porsi', 'Hangat', 15000, 1, '{SUDAH_KEDALUWARSA}', 1),
                       (3, 1, 'Kue', 'sudah lewat', '1 potong', 'Baik', 10000, 3, '2000-01-01 00:00:00', 1),
                       (4, 1, 'Donat', 'nonaktif', '1 box', 'Baik', 8000, 3, '{SUDAH_KEDALUWARSA}', 0),
                       (5, 1, 'Brownis', 'draft', '1 potong', 'Baik', 9000, 3, '{SUDAH_KEDALUWARSA}', 1);
            UPDATE listing_makanan SET draft = 1 WHERE id_listing = 5;
        """)
        c.commit()
    finally:
        if c is not None:
            c.close()

    for modul in MODUL_DATABASE:
        monkeypatch.setattr(modul, "DATABASE_NAME", path)

    def login(email: str, password: str = PASSWORD) -> TestClient:
        """Klien terpisah dengan sesi cookie milik akun tersebut."""
        client = TestClient(main.app)   # tanpa context manager: lifespan tidak jalan
        respons = client.post("/api/auth/login", json={"email": email, "password": password})
        assert respons.status_code == 200, respons.text
        return client

    def sql(query: str, params=()):
        koneksi = sqlite3.connect(path)
        try:
            hasil = koneksi.execute(query, params).fetchall()
            koneksi.commit()          # commit setelah eksekusi agar UPDATE tersimpan
            return hasil
        finally:
            koneksi.close()

    def stok(id_listing: int) -> int:
        return sql("SELECT stok FROM listing_makanan WHERE id_listing = ?", (id_listing,))[0][0]

    def batas(tid: int, waktu: str) -> None:
        """Mundurkan batas waktu bayar transaksi (simulasi tidak dibayar sampai tenggat)."""
        sql("UPDATE transaksi SET batas_waktu_bayar = ? WHERE id_transaksi = ?", (waktu, tid))

    pembeli = login("b1@t.com")      # klien aktif yang dipakai kebanyakan test
    return SimpleNamespace(pembeli=pembeli, login=login, sql=sql, stok=stok, batas=batas)


# ---------- 1. Flow test ----------

def test_e2e_beli_bayar_dikodekan_dan_diambil(e2e):
    """Seluruh perjalanan pembaharu: katalog → checkout → QR → LUNAS → penjual menandai diambil."""
    pembeli = e2e.pembeli

    # Katalog untuk pembeli (UC02)
    daftar = pembeli.get("/api/katalog").json()
    aktif = [l for l in daftar if l["id_listing"] in (1, 2)]
    assert {(l["id_listing"], l["nama_makanan"], l["nama_toko"]) for l in aktif} == {
        (1, "Roti", "Toko Roti"), (2, "Nasi", "Toko Roti")}
    assert pembeli.get("/api/katalog/1").json()["harga"] == 12000   # UC03

    # Checkout dari keranjang (UC05)
    checkout = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 2}, {"id_listing": 2, "jumlah": 1}]})
    assert checkout.status_code == 200, checkout.text
    trx = checkout.json()
    assert trx["status"] == "MENUNGGU_BAYAR"
    assert trx["total_harga"] == 2 * 12000 + 15000
    assert trx["kode_pengambilan"] is None
    assert trx["url_scan"].endswith(f"/pembayaran/scan/{trx['url_scan'].rsplit('/', 1)[-1]}")

    # Detail halaman pembayaran: token tidak berubah-ubah antar pemanggilan
    d1 = pembeli.get(f"/api/pembayaran/{trx['id_transaksi']}").json()
    d2 = pembeli.get(f"/api/pembayaran/{trx['id_transaksi']}").json()
    token = d1["url_scan"].rsplit("/", 1)[-1]
    assert token == d2["url_scan"].rsplit("/", 1)[-1]

    # Pembayaran dengan scan QR
    scan = pembeli.post(f"/api/pembayaran/scan/{token}")
    assert scan.status_code == 200 and scan.json() == {"status": "LUNAS"}

    # Segmen setelah bayar: kode pengambilan muncul, stok berkurang
    hasil = pembeli.get(f"/api/pembayaran/{trx['id_transaksi']}").json()
    assert hasil["status"] == "LUNAS"
    assert hasil["kode_pengambilan"].startswith("SB-")
    assert e2e.stok(1) == 3 and e2e.stok(2) == 0

    # Penjual melihat pesanan terbayar lalu menandai sudah diambil
    penjual = e2e.login("penjual@t.com")
    pesanan = penjual.get("/api/penjualan/pesanan").json()
    assert len(pesanan) == 1 and pesanan[0]["id_transaksi"] == trx["id_transaksi"]
    assert pesanan[0]["kode_pengambilan"] == hasil["kode_pengambilan"]
    pilih = penjual.post(f"/api/penjualan/{trx['id_transaksi']}/ambil")
    assert pilih.status_code == 200 and pilih.json()["waktu_diambil"]


def test_e2e_katalog_cari_dan_saring(e2e):
    """UC04: pencarian dan filter harga pada katalog tersedia."""
    pembeli = e2e.pembeli

    def nama(hasil):
        return [l["nama_makanan"] for l in hasil.json()]

    assert nama(pembeli.get("/api/katalog", params={"kata_kunci": "roti"})) == ["Roti"]
    assert nama(pembeli.get("/api/katalog", params={"kata_kunci": "   "})) == ["Roti", "Nasi"]
    hasil = pembeli.get("/api/katalog", params={"nilai_tak_ada": "x"}).json()   # argumen asing diabaikan
    assert all("nama_makanan" in l for l in hasil)

    kosong = pembeli.get("/api/katalog", params={"kata_kunci": "rendang"})
    assert kosong.status_code == 200 and kosong.json() == []

    assert nama(pembeli.get("/api/katalog", params={"harga_min": 12000, "harga_maks": 12000})) == ["Roti"]
    assert e2e.pembeli.get("/api/katalog", params={"harga_min": 20000, "harga_maks": 10000}).status_code == 400
    assert e2e.pembeli.get("/api/katalog", params={"harga_min": -1}).status_code == 400

    # Detil listing yang tidak layak jual → 404
    for id_listing in (999, 3, 4, 5):
        assert pembeli.get(f"/api/katalog/{id_listing}").status_code == 404, id_listing


def test_e2e_bayar_ganda_idempoten(e2e):
    pembeli = e2e.pembeli
    trx = pembeli.post("/api/pembayaran/checkout", json={"id_listing": 1, "jumlah": 2}).json()
    token = trx["url_scan"].rsplit("/", 1)[-1]

    scan = pembeli.post(f"/api/pembayaran/scan/{token}")
    asal = pembeli.post(f"/api/pembayaran/scan/{token}")     # tabrakan dobel tetap LUNAS
    assert scan.json() == {"status": "LUNAS"}
    assert asal.json() == {"status": "LUNAS"}

    # Pay button lewat gateway dummy nyaris sesudah LUNAS → 409
    ulang = pembeli.post(f"/api/pembayaran/{trx['id_transaksi']}/bayar")
    assert ulang.status_code == 409 and ulang.json()["detail"] == "Transaksi tidak dapat dibayar"
    assert e2e.stok(1) == 3                                   # potongan hanya satu kali


# ---------- 2. Exception test ----------

def test_e2e_belum_login_ditolak(tmp_path, monkeypatch, e2e):
    """Pembeli yang belum login tidak bisa memakai endpoint pembeli."""
    anonim = TestClient(main.app)
    assert anonim.get("/api/katalog").status_code == 401
    assert anonim.post("/api/pembayaran/checkout", json={"items": []}).status_code == 401
    assert anonim.get("/api/reward").status_code == 401


def test_e2e_penjual_diblok_endpoint_pembeli(e2e):
    """Role guard: penjual tidak bisa memakai endpoint milik pembeli."""
    penjual = e2e.login("penjual@t.com")
    assert penjual.get("/api/katalog").status_code == 403
    assert penjual.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}]}).status_code == 403
    assert penjual.get("/api/reward").status_code == 403


def test_e2e_login_password_salah(e2e):
    client = TestClient(main.app)
    salah = client.post("/api/auth/login", json={"email": "b1@t.com", "password": "salah-banget"})
    assert salah.status_code == 401


@pytest.mark.parametrize("isi, kode, pesan", [
    ({"items": []}, 400, "Pesanan tidak boleh kosong"),
    ({"id_listing": 1}, 400, "Pesanan tidak boleh kosong"),
    ({"items": [{"id_listing": 1, "jumlah": 0}]}, 400, "Jumlah porsi tidak valid"),
    ({"items": [{"id_listing": 999, "jumlah": 1}]}, 404, "Listing tidak tersedia"),
    ({"items": [{"id_listing": 3, "jumlah": 1}]}, 404, "Listing tidak tersedia"),
    ({"items": [{"id_listing": 4, "jumlah": 1}]}, 404, "Listing tidak tersedia"),
    ({"items": [{"id_listing": 5, "jumlah": 1}]}, 404, "Listing tidak tersedia"),
    ({"items": [{"id_listing": 2, "jumlah": 2}]}, 409, "Stok tidak mencukupi"),
])
def test_e2e_checkout_validasi(e2e, isi, kode, pesan):
    respons = e2e.pembeli.post("/api/pembayaran/checkout", json=isi)
    assert respons.status_code == kode
    assert respons.json()["detail"] == pesan
    assert e2e.sql("SELECT COUNT(*) FROM transaksi")[0][0] == 0


def test_e2e_transaksi_orang_lain_tak_bisa_disentuh(e2e):
    """IDOR: pembeli dua tidak boleh melihat/membayar transaksi pembeli satu."""
    pembeli1 = e2e.pembeli
    trx = pembeli1.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}]}).json()

    pembeli2 = e2e.login("b2@t.com")
    assert pembeli2.get(f"/api/pembayaran/{trx['id_transaksi']}").status_code == 404
    bayar = pembeli2.post(f"/api/pembayaran/{trx['id_transaksi']}/bayar")
    assert bayar.status_code == 409
    assert e2e.stok(1) == 5                       # stok tetap, transaksi tetap aman

    assert pembeli1.get(f"/api/pembayaran/{trx['id_transaksi']}").status_code == 200


def test_e2e_qr_palsu_ditolak(e2e):
    respons = e2e.pembeli.post("/api/pembayaran/scan/bukan-token-asli")
    assert respons.status_code == 404
    assert respons.json()["detail"] == "QR pembayaran tidak valid"


# ---------- 3. Alternatif test ----------

def test_e2e_tidak_membayar_sampai_tenggat_karena_pembatalan(e2e):
    """Pembeli tak pernah bayar: tombol bayar/scan setelah tenggat otomatis BATAL."""
    pembeli = e2e.pembeli
    trx = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 2}]}).json()
    tid = trx["id_transaksi"]
    e2e.batas(tid, SUDAH_LEWAT)

    # Lewat tombol bayar (gateway dummy)
    lewat = pembeli.post(f"/api/pembayaran/{tid}/bayar")
    assert lewat.status_code == 200 and lewat.json()["status"] == "BATAL"

    # Pembayaran lewat QR scan berakhir sama
    trx2 = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}]}).json()
    e2e.batas(trx2["id_transaksi"], SUDAH_LEWAT)
    token = trx2["url_scan"].rsplit("/", 1)[-1]
    scan = pembeli.post(f"/api/pembayaran/scan/{token}")
    assert scan.status_code == 200 and scan.json() == {"status": "BATAL"}

    # Transaksi BATAL tidak bisa dibayar lagi
    ulang = pembeli.post(f"/api/pembayaran/scan/{token}")
    assert ulang.status_code == 409 and ulang.json()["detail"] == "Transaksi sudah tidak dapat dibayar"

    # Stok tak pernah berkurang dan penjual tidak melihat pesanan apapun
    assert e2e.stok(1) == 5
    penjual = e2e.login("penjual@t.com")
    assert penjual.get("/api/penjualan/pesanan").json() == []


def test_e2e_reward_login_dan_klaim_kupon(e2e):
    """UC07/UC08: poin didapat tiap login harian, klaim Kupon memerlukan 100 poin."""
    pembeli3 = e2e.login("b2@t.com")       # login pertama → +10
    progres = pembeli3.get("/api/reward").json()
    assert progres["poin_terkumpul"] == 10
    assert progres["bisa_klaim"] is False

    pembeli3_lagi = e2e.login("b2@t.com")  # login lagi hari ini → poin tidak tambah
    progres = pembeli3_lagi.get("/api/reward").json()
    assert progres["poin_terkumpul"] == 10

    poin_kurang = pembeli3.post("/api/reward/klaim")
    assert poin_kurang.status_code == 400 and poin_kurang.json()["detail"] == "Poin tidak mencukupi"

    # Perbanyak poin (simulasi pengumpulan) lalu klaim
    e2e.sql("UPDATE reward_login SET poin_terkumpul = 100 WHERE id_pembeli = 3")
    kupon = pembeli3.post("/api/reward/klaim")
    assert kupon.status_code == 201 and kupon.json()["nilai_potongan"] == 10_000
    kode = kupon.json()["kode_kupon"]

    # Poin habis, klaim kedua ditolak
    assert pembeli3.post("/api/reward/klaim").status_code == 400
    progres = pembeli3.get("/api/reward").json()
    assert progres["poin_terkumpul"] == 0
    assert [k["kode_kupon"] for k in progres["kupon"]] == [kode]


def test_e2e_logout_menghapus_sesi(e2e):
    pembeli = e2e.pembeli
    assert pembeli.post("/api/auth/logout").status_code == 200
    assert pembeli.get("/api/katalog").status_code == 401


def test_e2e_login_beda_hari_menumpuk_poin_dan_diskon_kupon(e2e):
    """UC07/UC08: login pada hari yang berbeda mendapat 10 poin; sepuluh hari
    berbeda = 100 poin, cukup untuk mengklaim kupon diskon 10.000.

    "Hari berbeda" disimulasikan dengan memundurkan tanggal_login_terakhir
    pada basis data uji menjadi hari sebelumnya setiap siklus, karena endpoint
    login memakai date.today() dan poin hanya diberi pada hari yang belum dikunjungi.
    """
    pembeli3 = e2e.login("b2@t.com")                 # login hari 1: reward baris baru → +10
    progres = pembeli3.get("/api/reward").json()
    assert progres["poin_terkumpul"] == 10
    assert progres["nilai_potongan"] == 10_000       # diskon yang akan didapat

    # Login-lagi-tetap-hari-yang-sama → poin tidak bertambah
    e2e.login("b2@t.com")
    assert pembeli3.get("/api/reward").json()["poin_terkumpul"] == 10

    # Simulasi login pada 9 hari berikutnya: mundurkan tanggal login terakhir
    # setiap "hari baru", lakukan login, lalu cek poin menumpuk +10.
    pembeli_hari_baru = pembeli3
    for hari_baru in range(9):
        e2e.sql("UPDATE reward_login SET tanggal_login_terakhir = date('now', '-1 day') "
                "WHERE id_pembeli = 3")
        pembeli_hari_baru = e2e.login("b2@t.com")
        progres = pembeli_hari_baru.get("/api/reward").json()
        assert progres["poin_terkumpul"] == 10 * (2 + hari_baru), f"hari ke-{2 + hari_baru}"

        # dan login sekali lagi pada hari barunya tetap tidak menambah poin
        e2e.login("b2@t.com")
        assert pembeli_hari_baru.get("/api/reward").json()["poin_terkumpul"] == 10 * (2 + hari_baru)

    assert e2e.sql("SELECT poin_terkumpul FROM reward_login WHERE id_pembeli = 3")[0][0] == 100

    # 10 hari penuh → bisa klaim → kupon potongan 10.000 terbit (dipakai di checkout)
    klaim = pembeli_hari_baru.post("/api/reward/klaim")
    assert klaim.status_code == 201, klaim.text
    kupon = klaim.json()
    assert kupon["nilai_potongan"] == 10_000
    assert kupon["terpakai"] is False and kupon["berlaku"] is True
    assert e2e.sql("SELECT poin_terkumpul FROM reward_login WHERE id_pembeli = 3")[0][0] == 0

    # Setelah poin terkuras, klaim kedua hari sama ditolak
    assert pembeli_hari_baru.post("/api/reward/klaim").status_code == 400


def _semai_kupon_e2e(e2e, kode, id_pembeli=2, terakhir="2999-12-31", terpakai=0):
    e2e.sql("INSERT INTO kupon (kode_kupon, id_pembeli, nilai_potongan, berlaku_sampai, terpakai) "
            "VALUES (?, ?, 10000, ?, ?)", (kode, id_pembeli, terakhir, terpakai))


def test_e2e_checkout_pakai_kupon_dan_lunas(e2e):
    """Kupon reward yang diklaim benar-benar dipakai di checkout (UC05 + UC08):
    total untuk pembeli berkurang, harga untuk penjual tetap penuh."""
    pembeli = e2e.pembeli
    _semai_kupon_e2e(e2e, "E2EKUPN1", terakhir="2999-12-31")

    checkout = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 2}, {"id_listing": 2, "jumlah": 1}],
        "kode_kupon": "E2EKUPN1"})
    assert checkout.status_code == 200, checkout.text
    trx = checkout.json()
    assert trx["total_harga"] == (2 * 12_000 + 15_000) - 10_000     # 29.000

    # Kupon tercatat terpakai di sisi pembeli
    kupon = pembeli.get("/api/reward").json()["kupon"][0]
    assert kupon["kode_kupon"] == "E2EKUPN1" and kupon["terpakai"] is True

    # Bayar lewat QR → LUNAS, harga item untuk penjual tetap penuh
    token = trx["url_scan"].rsplit("/", 1)[-1]
    assert pembeli.post(f"/api/pembayaran/scan/{token}").json() == {"status": "LUNAS"}
    assert e2e.stok(1) == 3 and e2e.stok(2) == 0

    penjual = e2e.login("penjual@t.com")
    pesanan = penjual.get("/api/penjualan/pesanan").json()
    assert pesanan[0]["subtotal"] == 2 * 12_000 + 15_000            # potongan hanya milik pembeli

    # Kupon yang sudah terpakai tidak bisa ditebus lagi
    ulang = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "E2EKUPN1"})
    assert ulang.status_code == 400 and ulang.json()["detail"] == "Kupon sudah terpakai"


def test_e2e_kupon_ditolak_dan_dikembalikan_bila_pembatalan(e2e):
    pembeli = e2e.pembeli

    # Kode tidak ada → 404
    kosong = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "TAKADA01"})
    assert kosong.status_code == 404 and kosong.json()["detail"] == "Kupon tidak ditemukan"

    # Kupon milik pembeli lain dilaporkan sama dengan tidak ada
    _semai_kupon_e2e(e2e, "MILIK031", id_pembeli=3)
    milik = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "MILIK031"})
    assert milik.status_code == 404 and milik.json()["detail"] == "Kupon tidak ditemukan"

    # Kupon kedaluwarsa → 400
    _semai_kupon_e2e(e2e, "LALUS001", terakhir="2000-01-01")
    lalu = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "LALUS001"})
    assert lalu.status_code == 400 and lalu.json()["detail"] == "Kupon sudah kedaluwarsa"

    # Checkout dengan kupon valid, tidak dibayar sampai batas waktu → BATAL,
    # lalu kupon otomatis kembali bisa dipakai.
    _semai_kupon_e2e(e2e, "E2EBATL")
    trx = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "E2EBATL"}).json()
    assert trx["total_harga"] == 2_000
    e2e.batas(trx["id_transaksi"], SUDAH_LEWAT)

    batal = pembeli.post(f"/api/pembayaran/{trx['id_transaksi']}/bayar")
    assert batal.status_code == 200 and batal.json()["status"] == "BATAL"
    kupon = pembeli.get("/api/reward").json()["kupon"][0]
    assert kupon["kode_kupon"] == "E2EBATL" and kupon["terpakai"] is False and kupon["berlaku"] is True

    trx_lagi = pembeli.post("/api/pembayaran/checkout", json={
        "items": [{"id_listing": 1, "jumlah": 1}], "kode_kupon": "E2EBATL"})
    assert trx_lagi.status_code == 200
    assert trx_lagi.json()["total_harga"] == 2_000
