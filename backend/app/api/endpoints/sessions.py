from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Session as SessionModel, User
from ...schemas import Session as SessionSchema, SessionCreate, SessionUpdate
from ...api.deps import get_current_active_user
from .campaigns import check_campaign_access

router = APIRouter()


@router.post("", response_model=SessionSchema, status_code=status.HTTP_201_CREATED)
def create_session(
    session_in: SessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new session."""
    check_campaign_access(session_in.campaign_id, current_user, db)
    session = SessionModel(**session_in.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/campaign/{campaign_id}", response_model=List[SessionSchema])
def list_campaign_sessions(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all sessions in a campaign."""
    check_campaign_access(campaign_id, current_user, db)
    return db.query(SessionModel).filter(
        SessionModel.campaign_id == campaign_id
    ).order_by(SessionModel.session_number.desc()).all()


@router.get("/{session_id}", response_model=SessionSchema)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific session."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    check_campaign_access(session.campaign_id, current_user, db)
    return session


@router.put("/{session_id}", response_model=SessionSchema)
def update_session(
    session_id: int,
    session_update: SessionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a session."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    check_campaign_access(session.campaign_id, current_user, db)

    for field, value in session_update.dict(exclude_unset=True).items():
        setattr(session, field, value)

    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a session."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    check_campaign_access(session.campaign_id, current_user, db)
    db.delete(session)
    db.commit()
    return None
