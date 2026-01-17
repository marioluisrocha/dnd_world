from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Character as CharacterModel, User
from ...schemas import Character, CharacterCreate, CharacterUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_character(
    character_in: CharacterCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new character."""
    # Check campaign access
    check_campaign_access(character_in.campaign_id, current_user, db)

    character = CharacterModel(**character_in.dict(), creator_id=current_user.id)
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


@router.get("/campaign/{campaign_id}", response_model=List[Character])
def list_campaign_characters(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    include_npcs: bool = True
):
    """List all characters in a campaign."""
    # Check campaign access
    check_campaign_access(campaign_id, current_user, db)

    query = db.query(CharacterModel).filter(CharacterModel.campaign_id == campaign_id)
    if not include_npcs:
        query = query.filter(CharacterModel.is_npc == False)

    return query.all()


@router.get("/{character_id}", response_model=Character)
def get_character(
    character_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific character."""
    character = db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Check campaign access
    check_campaign_access(character.campaign_id, current_user, db)
    return character


@router.put("/{character_id}", response_model=Character)
def update_character(
    character_id: int,
    character_update: CharacterUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a character."""
    character = db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Check campaign access
    check_campaign_access(character.campaign_id, current_user, db)

    # Only creator or DM can update
    # TODO: Add DM check
    if character.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this character")

    for field, value in character_update.dict(exclude_unset=True).items():
        setattr(character, field, value)

    db.commit()
    db.refresh(character)
    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a character."""
    character = db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Check campaign access
    check_campaign_access(character.campaign_id, current_user, db)

    # Only creator can delete
    if character.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this character")

    db.delete(character)
    db.commit()
    return None
