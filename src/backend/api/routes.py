from fastapi import APIRouter, Depends
from backend.schemas.item import Item
from backend.routers.auth import require_roles

router = APIRouter()

@router.get("/items/{item_id}")
def read_item(
    item_id: int,
    q: str | None = None,
    user=Depends(require_roles(["PEMBELI", "PENJUAL"])),
):
    return {"item_id": item_id, "query": q}

@router.post("/items/")
def create_item(item: Item, user=Depends(require_roles(["PENJUAL"]))):
    return {"message": "Item created successfully", "item": item}