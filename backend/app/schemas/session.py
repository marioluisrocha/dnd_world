from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class SessionBase(BaseModel):
    session_number: int
    title: Optional[str] = None
    summary: Optional[str] = None
    notes: Optional[str] = None
    session_date: Optional[date] = None
    duration_minutes: Optional[int] = None


class SessionCreate(SessionBase):
    campaign_id: int


class SessionUpdate(BaseModel):
    session_number: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    notes: Optional[str] = None
    session_date: Optional[date] = None
    duration_minutes: Optional[int] = None


class Session(SessionBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
