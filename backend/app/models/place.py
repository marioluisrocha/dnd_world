from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class PlaceType(str, enum.Enum):
    CONTINENT = "continent"
    REGION = "region"
    CITY = "city"
    TOWN = "town"
    VILLAGE = "village"
    DUNGEON = "dungeon"
    BUILDING = "building"
    LANDMARK = "landmark"
    OTHER = "other"


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    parent_place_id = Column(Integer, ForeignKey("places.id"), nullable=True)

    place_type = Column(Enum(PlaceType), default=PlaceType.OTHER, nullable=False)
    description = Column(Text)
    history = Column(Text)
    notable_npcs = Column(Text)
    secrets = Column(Text)  # DM-only information

    # Geography
    population = Column(Integer)
    climate = Column(String)
    terrain = Column(String)

    # Map data
    map_image_url = Column(String)
    map_coordinates = Column(String)  # JSON string for lat/lng or x/y coordinates

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="places")
    parent_place = relationship("Place", remote_side=[id], backref="sub_places")
