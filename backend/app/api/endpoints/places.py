from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Place as PlaceModel, User
from ...schemas import Place, PlaceCreate, PlaceUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=Place, status_code=status.HTTP_201_CREATED)
def create_place(
    place_in: PlaceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new place."""
    check_campaign_access(place_in.campaign_id, current_user, db)

    place = PlaceModel(**place_in.dict())
    db.add(place)
    db.commit()
    db.refresh(place)
    return place


@router.get("/campaign/{campaign_id}", response_model=List[Place])
def list_campaign_places(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all places in a campaign."""
    check_campaign_access(campaign_id, current_user, db)
    return db.query(PlaceModel).filter(PlaceModel.campaign_id == campaign_id).all()


@router.get("/{place_id}", response_model=Place)
def get_place(
    place_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific place."""
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    check_campaign_access(place.campaign_id, current_user, db)
    return place


@router.put("/{place_id}", response_model=Place)
def update_place(
    place_id: int,
    place_update: PlaceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a place."""
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    check_campaign_access(place.campaign_id, current_user, db)

    for field, value in place_update.dict(exclude_unset=True).items():
        setattr(place, field, value)

    db.commit()
    db.refresh(place)
    return place


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place(
    place_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a place."""
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    check_campaign_access(place.campaign_id, current_user, db)

    db.delete(place)
    db.commit()
    return None
