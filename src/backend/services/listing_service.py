import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB dalam bytes

MAGIC_BYTES_PNG = b"\x89PNG\r\n\x1a\n"
MAGIC_BYTES_JPG = b"\xff\xd8\xff"


async def simpan_foto_listing(file: UploadFile) -> str:
    """
    Memvalidasi dan menyimpan foto listing makanan.
    - Format: PNG / JPG
    - Maksimal ukuran: 10 MB
    - Pengecekan Magic Bytes
    
    Mengembalikan path relatif URL foto, misal: '/uploads/listing/<uuid>.<ext>'
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Berkas foto wajib diunggah"
        )

    # 1. Pengecekan Ekstensi Nama File
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ["png", "jpg", "jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format file tidak didukung. Gunakan ekstensi PNG atau JPG/JPEG"
        )

    # 2. Baca Konten File untuk Pengecekan Ukuran & Magic Bytes
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ukuran foto melebihi batas maksimal 10 MB"
        )

    # 3. Pengecekan Magic Bytes (Header File Asli)
    is_png = content.startswith(MAGIC_BYTES_PNG)
    is_jpg = content.startswith(MAGIC_BYTES_JPG)

    if not (is_png or is_jpg):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Berkas bukan merupakan gambar PNG atau JPG yang valid"
        )

    # 4. Simpan Berkas dengan Nama UUID Unique
    file_ext = "png" if is_png else "jpg"
    filename = f"{uuid.uuid4()}.{file_ext}"

    base_dir = Path(__file__).resolve().parent.parent
    upload_dir = base_dir / "uploads" / "listing"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(content)

    # Kembalikan path relatif untuk disimpan di DB
    return f"/uploads/listing/{filename}"