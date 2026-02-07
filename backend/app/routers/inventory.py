from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_roles
from ..models import InventoryItem, RoleEnum
from ..schemas import InventoryCreate, InventoryRead, InventoryUpdate

router = APIRouter()


@router.get("/", response_model=list[InventoryRead])
def list_inventory(
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.ESTHETICIAN)),
):
    return db.query(InventoryItem).all()


@router.post("/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    payload: InventoryCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=InventoryRead)
def update_inventory_item(
    item_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.RECEPTIONIST)),
):
    item = db.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_roles(RoleEnum.ADMIN)),
):
    item = db.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")
    db.delete(item)
    db.commit()
