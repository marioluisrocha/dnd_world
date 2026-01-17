from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Quest as QuestModel, User
from ...schemas import Quest, QuestCreate, QuestUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=Quest, status_code=status.HTTP_201_CREATED)
def create_quest(
    quest_in: QuestCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new quest."""
    check_campaign_access(quest_in.campaign_id, current_user, db)
    quest = QuestModel(**quest_in.dict())
    db.add(quest)
    db.commit()
    db.refresh(quest)
    return quest


@router.get("/campaign/{campaign_id}", response_model=List[Quest])
def list_campaign_quests(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all quests in a campaign."""
    check_campaign_access(campaign_id, current_user, db)
    return db.query(QuestModel).filter(QuestModel.campaign_id == campaign_id).all()


@router.get("/{quest_id}", response_model=Quest)
def get_quest(
    quest_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific quest."""
    quest = db.query(QuestModel).filter(QuestModel.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    check_campaign_access(quest.campaign_id, current_user, db)
    return quest


@router.put("/{quest_id}", response_model=Quest)
def update_quest(
    quest_id: int,
    quest_update: QuestUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a quest."""
    quest = db.query(QuestModel).filter(QuestModel.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    check_campaign_access(quest.campaign_id, current_user, db)

    for field, value in quest_update.dict(exclude_unset=True).items():
        setattr(quest, field, value)

    db.commit()
    db.refresh(quest)
    return quest


@router.delete("/{quest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quest(
    quest_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a quest."""
    quest = db.query(QuestModel).filter(QuestModel.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    check_campaign_access(quest.campaign_id, current_user, db)
    db.delete(quest)
    db.commit()
    return None
