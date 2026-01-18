from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from ..models.campaign import CampaignRole


class UserSimple(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    setting: Optional[str] = None
    is_active: bool = True


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    setting: Optional[str] = None
    is_active: Optional[bool] = None


class CampaignMemberBase(BaseModel):
    user_id: int
    role: CampaignRole


class CampaignMemberCreate(CampaignMemberBase):
    pass


class CampaignMember(CampaignMemberBase):
    id: int
    campaign_id: int
    joined_at: datetime
    user: UserSimple

    class Config:
        from_attributes = True


class Campaign(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CampaignDetail(Campaign):
    members: List[CampaignMember] = []
    owner: UserSimple
