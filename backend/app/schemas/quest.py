from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.quest import QuestStatus


class QuestBase(BaseModel):
    name: str
    description: Optional[str] = None
    objectives: Optional[str] = None
    rewards: Optional[str] = None
    quest_giver: Optional[str] = None
    location: Optional[str] = None
    status: QuestStatus = QuestStatus.NOT_STARTED


class QuestCreate(QuestBase):
    campaign_id: int


class QuestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    objectives: Optional[str] = None
    rewards: Optional[str] = None
    quest_giver: Optional[str] = None
    location: Optional[str] = None
    status: Optional[QuestStatus] = None


class Quest(QuestBase):
    id: int
    campaign_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
