import asyncio
import pytest
from io import BytesIO
from fastapi import UploadFile, HTTPException
from services.listing_service import simpan_foto_listing

# Header asli (magic bytes) untuk file dummy
DUMMY_PNG_HEADER = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
DUMMY_JPG_HEADER = b"\xff\xd8\xff" + b"\x00" * 100
INVALID_HEADER = b"GIF89a" + b"\x00" * 100


def test_upload_foto_png_sukses():
    file = UploadFile(filename="test.png", file=BytesIO(DUMMY_PNG_HEADER))
    path = asyncio.run(simpan_foto_listing(file))
    assert path.startswith("/uploads/listing/")
    assert path.endswith(".png")


def test_upload_foto_jpg_sukses():
    file = UploadFile(filename="test.jpg", file=BytesIO(DUMMY_JPG_HEADER))
    path = asyncio.run(simpan_foto_listing(file))
    assert path.startswith("/uploads/listing/")
    assert path.endswith(".jpg")


def test_upload_foto_magic_bytes_invalid():
    file = UploadFile(filename="palsu.png", file=BytesIO(INVALID_HEADER))
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(simpan_foto_listing(file))
    assert exc_info.value.status_code == 400
    assert "bukan merupakan gambar PNG atau JPG" in exc_info.value.detail


def test_upload_foto_ukuran_melebihi_batas():
    ukuran_besar = 11 * 1024 * 1024
    content_besar = b"\x89PNG\r\n\x1a\n" + b"\x00" * (ukuran_besar - 8)
    file = UploadFile(filename="besar.png", file=BytesIO(content_besar))

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(simpan_foto_listing(file))
    assert exc_info.value.status_code == 400
    assert "melebihi batas maksimal 10 MB" in exc_info.value.detail