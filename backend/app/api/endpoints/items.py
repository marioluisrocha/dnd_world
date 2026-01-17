from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Item as ItemModel, User
from ...schemas import Item, ItemCreate, ItemUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new item."""
    check_campaign_access(item_in.campaign_id, current_user, db)

    item = ItemModel(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/campaign/{campaign_id}", response_model=List[Item])
def list_campaign_items(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all items in a campaign."""
    check_campaign_access(campaign_id, current_user, db)
    return db.query(ItemModel).filter(ItemModel.campaign_id == campaign_id).all()


@router.get("/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific item."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    check_campaign_access(item.campaign_id, current_user, db)
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an item."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    check_campaign_access(item.campaign_id, current_user, db)

    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an item."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    check_campaign_access(item.campaign_id, current_user, db)

    db.delete(item)
    db.commit()
    return None
