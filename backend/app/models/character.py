from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    race = Column(String)
    character_class = Column(String)  # 'class' is reserved keyword
    level = Column(Integer, default=1)
    background = Column(String)
    alignment = Column(String)

    # Stats
    stats = Column(JSON)  # {str: 10, dex: 14, con: 12, int: 8, wis: 13, cha: 16}

    # Details
    backstory = Column(Text)
    personality_traits = Column(Text)
    ideals = Column(Text)
    bonds = Column(Text)
    flaws = Column(Text)
    appearance = Column(Text)

    # External Integration
    dndbeyond_url = Column(String)
    dndbeyond_id = Column(String)
    last_synced = Column(DateTime(timezone=True))

    # Status
    is_npc = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="characters")
    creator = relationship("User", back_populates="characters")
    inventory = relationship("CharacterItem", back_populates="character", cascade="all, delete-orphan")


class CharacterItem(Base):
    __tablename__ = "character_items"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    is_equipped = Column(Boolean, default=False)
    notes = Column(Text)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    character = relationship("Character", back_populates="inventory")
    item = relationship("Item", back_populates="character_items")
