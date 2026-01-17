from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class CharacterBase(BaseModel):
    name: str
    race: Optional[str] = None
    character_class: Optional[str] = None
    level: int = 1
    background: Optional[str] = None
    alignment: Optional[str] = None
    stats: Optional[Dict[str, int]] = None
    backstory: Optional[str] = None
    personality_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    flaws: Optional[str] = None
    appearance: Optional[str] = None
    is_npc: bool = False
    is_active: bool = True


class CharacterCreate(CharacterBase):
    campaign_id: int


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    race: Optional[str] = None
    character_class: Optional[str] = None
    level: Optional[int] = None
    background: Optional[str] = None
    alignment: Optional[str] = None
    stats: Optional[Dict[str, int]] = None
    backstory: Optional[str] = None
    personality_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    flaws: Optional[str] = None
    appearance: Optional[str] = None
    is_npc: Optional[bool] = None
    is_active: Optional[bool] = None


class Character(CharacterBase):
    id: int
    campaign_id: int
    creator_id: int
    dndbeyond_url: Optional[str] = None
    dndbeyond_id: Optional[str] = None
    last_synced: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CharacterItemBase(BaseModel):
    item_id: int
    quantity: int = 1
    is_equipped: bool = False
    notes: Optional[str] = None


class CharacterItemCreate(CharacterItemBase):
    character_id: int


class CharacterItem(CharacterItemBase):
    id: int
    character_id: int
    added_at: datetime

    class Config:
        from_attributes = True
