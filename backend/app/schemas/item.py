from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.item import ItemType, ItemRarity


class ItemBase(BaseModel):
    name: str
    item_type: ItemType = ItemType.OTHER
    rarity: ItemRarity = ItemRarity.COMMON
    description: Optional[str] = None
    properties: Optional[str] = None
    weight: Optional[float] = None
    value: Optional[int] = None
    damage: Optional[str] = None
    ac_bonus: Optional[int] = None
    requires_attunement: bool = False
    is_magical: bool = False
    is_cursed: bool = False
    dndbeyond_url: Optional[str] = None


class ItemCreate(ItemBase):
    campaign_id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    item_type: Optional[ItemType] = None
    rarity: Optional[ItemRarity] = None
    description: Optional[str] = None
    properties: Optional[str] = None
    weight: Optional[float] = None
    value: Optional[int] = None
    damage: Optional[str] = None
    ac_bonus: Optional[int] = None
    requires_attunement: Optional[bool] = None
    is_magical: Optional[bool] = None
    is_cursed: Optional[bool] = None
    dndbeyond_url: Optional[str] = None


class Item(ItemBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
