"""
D&D Beyond Integration Service

Note: D&D Beyond does not have an official public API. This service provides
a framework for integration that can work with:
1. Unofficial APIs (like the one used by browser extensions)
2. Web scraping (requires user's session token)
3. Manual import via exported JSON

For production use, you'll need:
- User's D&D Beyond Cobalt session token (from browser cookies)
- Or implement web scraping with Beautiful Soup
"""

import httpx
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from ..core.config import settings


class DNDBeyondService:
    """Service for integrating with D&D Beyond."""

    BASE_URL = "https://www.dndbeyond.com"
    CHARACTER_API_URL = "https://character-service.dndbeyond.com/character/v5/character"

    def __init__(self, cobalt_token: Optional[str] = None):
        """Initialize with optional Cobalt session token."""
        self.cobalt_token = cobalt_token or settings.DNDBEYOND_COBALT_TOKEN
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        if self.cobalt_token:
            self.headers["Cookie"] = f"CobaltSession={self.cobalt_token}"

    async def get_character_data(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch character data from D&D Beyond API.

        Args:
            character_id: The D&D Beyond character ID

        Returns:
            Character data dictionary or None if failed
        """
        if not self.cobalt_token:
            print("No Cobalt token provided - cannot fetch from API")
            return None

        url = f"{self.CHARACTER_API_URL}/{character_id}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                print(f"Successfully fetched character data from D&D Beyond API")
                return data
            except httpx.HTTPError as e:
                print(f"Error fetching character from API: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response body: {e.response.text[:200]}")
                return None

    def parse_character_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse D&D Beyond API response into our character format.

        Args:
            data: Raw D&D Beyond character data

        Returns:
            Parsed character data matching our schema
        """
        if not data or "data" not in data:
            return {}

        char_data = data["data"]

        # Extract ability scores
        stats = {}
        for stat in char_data.get("stats", []):
            stat_name = stat.get("name") or ""
            if stat_name:
                stat_name = stat_name.lower()[:3]
                stats[stat_name] = stat.get("value", 10)

        # Get class info (handle multiclassing)
        classes = char_data.get("classes", [])
        character_class = ", ".join([c.get("definition", {}).get("name", "") for c in classes])
        level = sum([c.get("level", 0) for c in classes])

        # Extract saving throws
        saving_throws = {}
        for mod in char_data.get("modifiers", {}).get("class", []):
            mod_type = mod.get("type") or ""
            mod_subtype = mod.get("subType") or ""
            if mod_subtype and "saving-throws" in mod_type:
                ability = mod_subtype.lower()[:3]
                saving_throws[ability] = {
                    "proficient": True,
                    "value": mod.get("value", 0)
                }

        # Extract skills
        skills = {}
        skill_mapping = {
            1: "acrobatics", 2: "animal-handling", 3: "arcana", 4: "athletics",
            5: "deception", 6: "history", 7: "insight", 8: "intimidation",
            9: "investigation", 10: "medicine", 11: "nature", 12: "perception",
            13: "performance", 14: "persuasion", 15: "religion", 16: "sleight-of-hand",
            17: "stealth", 18: "survival"
        }
        for mod in char_data.get("modifiers", {}).get("class", []):
            if mod.get("type") == "proficiency" and mod.get("subType") == "ability-checks":
                skill_id = mod.get("entityId")
                if skill_id in skill_mapping:
                    skills[skill_mapping[skill_id]] = {
                        "proficient": True,
                        "expertise": False
                    }

        # Extract languages
        languages = []
        for lang in char_data.get("languages", []):
            lang_name = lang.get("definition", {}).get("name") or lang.get("name")
            if lang_name:
                languages.append(lang_name)

        # Extract features and traits
        features = []
        for feature in char_data.get("feats", []) + char_data.get("racialTraits", []):
            features.append({
                "name": feature.get("definition", {}).get("name", feature.get("name", "")),
                "description": feature.get("definition", {}).get("description", feature.get("description", "")),
                "source": feature.get("definition", {}).get("sourcePageNumber", "")
            })

        # Extract class features
        for cls in classes:
            for feature in cls.get("classFeatures", []):
                features.append({
                    "name": feature.get("definition", {}).get("name", ""),
                    "description": feature.get("definition", {}).get("description", ""),
                    "source": f"{cls.get('definition', {}).get('name', '')} Level {feature.get('requiredLevel', 1)}"
                })

        # Extract spells
        spells_by_level = {"cantrips": []}
        for i in range(1, 10):
            spells_by_level[str(i)] = []

        for spell in char_data.get("spells", {}).get("class", []):
            spell_obj = {
                "name": spell.get("definition", {}).get("name", ""),
                "level": spell.get("definition", {}).get("level", 0),
                "school": spell.get("definition", {}).get("school", ""),
                "castingTime": spell.get("definition", {}).get("castingTime", ""),
                "range": spell.get("definition", {}).get("range", {}).get("rangeValue", 0),
                "duration": spell.get("definition", {}).get("duration", {}).get("durationValue", ""),
                "description": spell.get("definition", {}).get("description", ""),
                "prepared": spell.get("prepared", False)
            }
            spell_level = spell.get("definition", {}).get("level", 0)
            if spell_level == 0:
                spells_by_level["cantrips"].append(spell_obj)
            else:
                spells_by_level[str(spell_level)].append(spell_obj)

        # Extract spell slots
        spell_slots = {}
        for slot in char_data.get("spellSlots", []):
            level = slot.get("level", 0)
            spell_slots[str(level)] = {
                "max": slot.get("available", 0),
                "used": slot.get("used", 0)
            }

        # Alignment mapping
        alignment_map = {
            1: "Lawful Good", 2: "Neutral Good", 3: "Chaotic Good",
            4: "Lawful Neutral", 5: "True Neutral", 6: "Chaotic Neutral",
            7: "Lawful Evil", 8: "Neutral Evil", 9: "Chaotic Evil"
        }
        alignment = alignment_map.get(char_data.get("alignmentId"), "")

        return {
            "name": char_data.get("name", ""),
            "race": char_data.get("race", {}).get("fullName", ""),
            "character_class": character_class,
            "level": level,
            "background": char_data.get("background", {}).get("definition", {}).get("name", ""),
            "alignment": alignment,
            "stats": stats,
            "saving_throws": saving_throws,
            "skills": skills,
            "armor_class": char_data.get("armorClass") or 10,
            "initiative": char_data.get("initiative") or 0,
            "speed": char_data.get("speed", {}).get("walk") or 30,
            "hit_points_max": (char_data.get("baseHitPoints") or 0) + (char_data.get("bonusHitPoints") or 0),
            "hit_points_current": (char_data.get("baseHitPoints") or 0) + (char_data.get("bonusHitPoints") or 0) - (char_data.get("removedHitPoints") or 0),
            "hit_points_temp": char_data.get("temporaryHitPoints") or 0,
            "hit_dice": f"{level}d{classes[0].get('definition', {}).get('hitDice', 8) if classes else 8}",
            "languages": languages,
            "features": features,
            "spells": spells_by_level,
            "spell_slots": spell_slots,
            "spellcasting_ability": char_data.get("preferences", {}).get("abilityScoreDisplayType", ""),
            "backstory": char_data.get("notes", {}).get("backstory", ""),
            "personality_traits": char_data.get("traits", {}).get("personalityTraits", ""),
            "ideals": char_data.get("traits", {}).get("ideals", ""),
            "bonds": char_data.get("traits", {}).get("bonds", ""),
            "flaws": char_data.get("traits", {}).get("flaws", ""),
            "appearance": char_data.get("notes", {}).get("appearance", ""),
        }

    async def scrape_character_sheet(self, character_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape character data from public D&D Beyond character sheet.
        Note: This only works for public character sheets and is very limited.

        Args:
            character_url: Full URL to character sheet

        Returns:
            Basic character data or None if failed
        """
        print(f"Attempting to scrape character from: {character_url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(character_url, headers=self.headers, timeout=10.0)
                response.raise_for_status()

                print(f"Got response status: {response.status_code}")
                soup = BeautifulSoup(response.text, 'html.parser')

                # This is a simplified example - actual scraping would be more complex
                # D&D Beyond's character sheets are heavily JavaScript-based, making scraping difficult
                name_elem = soup.find("div", class_="ddbc-character-name")
                name = name_elem.text.strip() if name_elem else "Unknown"

                print(f"Scraped character name: {name}")
                print("WARNING: Scraping is very limited. For full character data, provide a Cobalt token.")

                return {
                    "name": name,
                    # Scraping cannot reliably get other fields without executing JavaScript
                    # D&D Beyond loads character data via API calls after page load
                }
            except Exception as e:
                print(f"Error scraping character sheet: {e}")
                return None

    @staticmethod
    def extract_character_id_from_url(url: str) -> Optional[str]:
        """
        Extract character ID from D&D Beyond URL.

        Args:
            url: D&D Beyond character URL

        Returns:
            Character ID or None
        """
        import re
        match = re.search(r'/characters/(\d+)', url)
        return match.group(1) if match else None


# Example usage function for the API endpoint
async def import_character_from_dndbeyond(
    character_url: str,
    cobalt_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Import character from D&D Beyond.

    Args:
        character_url: D&D Beyond character URL
        cobalt_token: Optional Cobalt session token for private sheets

    Returns:
        Parsed character data ready for database insertion
    """
    print(f"\n=== Starting D&D Beyond Import ===")
    print(f"URL: {character_url}")
    print(f"Has Cobalt Token: {bool(cobalt_token)}")

    service = DNDBeyondService(cobalt_token)
    character_id = service.extract_character_id_from_url(character_url)

    if not character_id:
        print(f"ERROR: Could not extract character ID from URL: {character_url}")
        return None

    print(f"Extracted character ID: {character_id}")

    # Try API first (requires token)
    if cobalt_token:
        print("Attempting to fetch via D&D Beyond API...")
        raw_data = await service.get_character_data(character_id)
        if raw_data:
            parsed = service.parse_character_data(raw_data)
            print(f"Successfully parsed character: {parsed.get('name', 'Unknown')}")
            return parsed
        else:
            print("API fetch failed, falling back to scraping...")

    # Fallback to scraping for public sheets
    print("Attempting to scrape character sheet...")
    scraped_data = await service.scrape_character_sheet(character_url)

    if scraped_data and scraped_data.get("name") and scraped_data.get("name") != "Unknown":
        print(f"Scraping completed: {scraped_data}")
        return scraped_data
    else:
        print("ERROR: Scraping failed or returned incomplete data")
        print("D&D Beyond character sheets require JavaScript to load character data.")
        print("Without a Cobalt token, we cannot access the full character information.")
        return None
