"""
Database initialization script.
Creates tables and optionally seeds sample data.
"""

import sys
from app.core import Base, engine, get_db, get_password_hash
from app.models import (
    User, Campaign, CampaignMember, CampaignRole,
    Character, Place, PlaceType, Item, ItemType, ItemRarity,
    Quest, QuestStatus, Session, Note
)


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def seed_sample_data():
    """Seed database with sample data for testing."""
    print("\nSeeding sample data...")

    db = next(get_db())

    try:
        # Check if data already exists
        if db.query(User).first():
            print("⚠ Database already contains data. Skipping seed.")
            return

        # Create sample user
        user = User(
            email="dm@example.com",
            username="dungeon_master",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✓ Created user: {user.username}")

        # Create sample campaign
        campaign = Campaign(
            name="Lost Mine of Phandelver",
            description="A classic D&D 5e starter adventure",
            setting="Forgotten Realms",
            owner_id=user.id
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        print(f"✓ Created campaign: {campaign.name}")

        # Create sample character
        character = Character(
            name="Thorin Ironshield",
            campaign_id=campaign.id,
            creator_id=user.id,
            race="Mountain Dwarf",
            character_class="Fighter",
            level=3,
            background="Soldier",
            alignment="Lawful Good",
            stats={"str": 16, "dex": 12, "con": 15, "int": 10, "wis": 13, "cha": 8},
            backstory="A veteran soldier seeking redemption...",
            is_npc=False
        )
        db.add(character)
        print(f"✓ Created character: {character.name}")

        # Create sample NPC
        npc = Character(
            name="Sildar Hallwinter",
            campaign_id=campaign.id,
            creator_id=user.id,
            race="Human",
            character_class="Fighter",
            level=5,
            alignment="Lawful Good",
            backstory="A member of the Lords' Alliance",
            is_npc=True
        )
        db.add(npc)
        print(f"✓ Created NPC: {npc.name}")

        # Create sample place
        place = Place(
            name="Phandalin",
            campaign_id=campaign.id,
            place_type=PlaceType.TOWN,
            description="A small frontier town built on the ruins of an older settlement",
            population=1000,
            notable_npcs="Toblen Stonehill (innkeeper), Sildar Hallwinter",
            secrets="The Redbrands are causing trouble in town"
        )
        db.add(place)
        print(f"✓ Created place: {place.name}")

        # Create nested place
        inn = Place(
            name="Stonehill Inn",
            campaign_id=campaign.id,
            place_type=PlaceType.BUILDING,
            parent_place_id=None,  # Will be set after place is committed
            description="A modest inn with clean rooms and good food"
        )
        db.add(inn)
        db.commit()
        db.refresh(place)
        inn.parent_place_id = place.id
        print(f"✓ Created building: {inn.name}")

        # Create sample item
        item = Item(
            name="Longsword +1",
            campaign_id=campaign.id,
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.UNCOMMON,
            description="A finely crafted longsword with a +1 bonus to attack and damage rolls",
            damage="1d8 slashing",
            weight=3.0,
            value=500,
            is_magical=True
        )
        db.add(item)
        print(f"✓ Created item: {item.name}")

        # Create sample quest
        quest = Quest(
            name="Rescue Gundren Rockseeker",
            campaign_id=campaign.id,
            description="Find and rescue Gundren from the goblins",
            objectives="1. Track goblin trail\n2. Find Cragmaw Hideout\n3. Rescue Gundren",
            rewards="100 gold pieces and Gundren's gratitude",
            quest_giver="Sildar Hallwinter",
            location="Cragmaw Hideout",
            status=QuestStatus.IN_PROGRESS
        )
        db.add(quest)
        print(f"✓ Created quest: {quest.name}")

        # Create sample session
        session = Session(
            campaign_id=campaign.id,
            session_number=1,
            title="The Adventure Begins",
            summary="The party met in Neverwinter and accepted a job to escort supplies to Phandalin. On the road, they encountered a goblin ambush.",
            notes="Players enjoyed the combat. Need to emphasize the mystery of Gundren's disappearance next session.",
            duration_minutes=180
        )
        db.add(session)
        print(f"✓ Created session: {session.title}")

        # Create sample note
        note = Note(
            campaign_id=campaign.id,
            title="Black Spider's Identity",
            content="The Black Spider is Nezznar, a drow wizard seeking the Forge of Spells beneath Wave Echo Cave.",
            category="Plot",
            tags="villain,main-plot,spoiler",
            is_dm_only=True
        )
        db.add(note)
        print(f"✓ Created note: {note.title}")

        db.commit()
        print("\n✓ Sample data seeded successfully!")
        print(f"\nTest credentials:")
        print(f"  Username: {user.username}")
        print(f"  Password: password123")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("D&D Campaign Manager - Database Initialization")
    print("=" * 50)

    create_tables()

    if len(sys.argv) > 1 and sys.argv[1] == "--seed":
        seed_sample_data()
    else:
        print("\nTo seed sample data, run: python init_db.py --seed")

    print("\nDatabase initialization complete!")
