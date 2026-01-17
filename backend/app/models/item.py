from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class ItemRarity(str, enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"


class ItemType(str, enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    SCROLL = "scroll"
    WONDROUS = "wondrous"
    TOOL = "tool"
    GEAR = "gear"
    TREASURE = "treasure"
    OTHER = "other"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    item_type = Column(Enum(ItemType), default=ItemType.OTHER, nullable=False)
    rarity = Column(Enum(ItemRarity), default=ItemRarity.COMMON, nullable=False)

    description = Column(Text)
    properties = Column(Text)  # Special properties or abilities

    # Mechanical info
    weight = Column(Float)  # in pounds
    value = Column(Integer)  # in gold pieces
    damage = Column(String)  # e.g., "1d8 slashing"
    ac_bonus = Column(Integer)  # for armor

    # Flags
    requires_attunement = Column(Boolean, default=False)
    is_magical = Column(Boolean, default=False)
    is_cursed = Column(Boolean, default=False)

    # External reference
    dndbeyond_url = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="items")
    character_items = relationship("CharacterItem", back_populates="item", cascade="all, delete-orphan")
