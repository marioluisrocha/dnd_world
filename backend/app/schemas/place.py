from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.place import PlaceType


class PlaceBase(BaseModel):
    name: str
    place_type: PlaceType = PlaceType.OTHER
    description: Optional[str] = None
    history: Optional[str] = None
    notable_npcs: Optional[str] = None
    secrets: Optional[str] = None
    population: Optional[int] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    map_image_url: Optional[str] = None
    map_coordinates: Optional[str] = None
    parent_place_id: Optional[int] = None


class PlaceCreate(PlaceBase):
    campaign_id: int


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    place_type: Optional[PlaceType] = None
    description: Optional[str] = None
    history: Optional[str] = None
    notable_npcs: Optional[str] = None
    secrets: Optional[str] = None
    population: Optional[int] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    map_image_url: Optional[str] = None
    map_coordinates: Optional[str] = None
    parent_place_id: Optional[int] = None


class Place(PlaceBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
