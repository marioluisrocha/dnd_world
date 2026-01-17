from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Note as NoteModel, User
from ...schemas import Note, NoteCreate, NoteUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new note."""
    check_campaign_access(note_in.campaign_id, current_user, db)
    note = NoteModel(**note_in.dict())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/campaign/{campaign_id}", response_model=List[Note])
def list_campaign_notes(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all notes in a campaign."""
    check_campaign_access(campaign_id, current_user, db)
    # TODO: Filter DM-only notes based on user role
    return db.query(NoteModel).filter(NoteModel.campaign_id == campaign_id).all()


@router.get("/{note_id}", response_model=Note)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific note."""
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    check_campaign_access(note.campaign_id, current_user, db)
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a note."""
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    check_campaign_access(note.campaign_id, current_user, db)

    for field, value in note_update.dict(exclude_unset=True).items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a note."""
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    check_campaign_access(note.campaign_id, current_user, db)
    db.delete(note)
    db.commit()
    return None
