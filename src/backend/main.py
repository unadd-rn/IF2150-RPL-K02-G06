import sqlite3
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .models import DATABASE_NAME, init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import auth
from .api import routes as api_routes
from .controllers.katalog_controller import router as katalog_router
from .api.listing_routes import router as listing_router
from .api.pembayaran_routes import router as pembayaran_router
from .api.penjualan_routes import router as penjualan_router
from .api.toko_routes import router as toko_router
from .controllers.reward_controller import router as reward_router

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads" / "listing"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    """Helper untuk mendapatkan koneksi basis data SQLite dengan foreign key aktif."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(DATABASE_NAME)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=BASE_DIR / "uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(api_routes.router, prefix="/api", tags=["API"])
app.include_router(katalog_router)  # P3: UC02/UC03 katalog
app.include_router(listing_router) #P2 : idk ini uc berapa antara 1 6 9
app.include_router(pembayaran_router)   # P4: UC05 pembayaran
app.include_router(penjualan_router)    # P2: pesanan terbayar & pengambilan oleh penjual
app.include_router(reward_router)       # P5: UC08 klaim reward login
app.include_router(toko_router)         # P2: profil toko penjual (nama & alamat)

@app.get("/")
def read_root():
    return {"message": "Database SQLite SaveBite berhasil diinisialisasi!"}
