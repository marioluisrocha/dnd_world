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
            raise ValueError("Cobalt token required for API access")

        url = f"{self.CHARACTER_API_URL}/{character_id}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching character: {e}")
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
            stat_name = stat.get("name", "").lower()[:3]
            stats[stat_name] = stat.get("value", 10)

        # Get class info (handle multiclassing)
        classes = char_data.get("classes", [])
        character_class = ", ".join([c.get("definition", {}).get("name", "") for c in classes])
        level = sum([c.get("level", 0) for c in classes])

        return {
            "name": char_data.get("name", ""),
            "race": char_data.get("race", {}).get("fullName", ""),
            "character_class": character_class,
            "level": level,
            "background": char_data.get("background", {}).get("definition", {}).get("name", ""),
            "alignment": char_data.get("alignmentId"),  # You'd map this to alignment name
            "stats": stats,
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
        Note: This only works for public character sheets.

        Args:
            character_url: Full URL to character sheet

        Returns:
            Basic character data or None if failed
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(character_url, headers=self.headers, timeout=10.0)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # This is a simplified example - actual scraping would be more complex
                name_elem = soup.find("div", class_="ddbc-character-name")
                name = name_elem.text.strip() if name_elem else "Unknown"

                return {
                    "name": name,
                    # Add more scraping logic here
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
    service = DNDBeyondService(cobalt_token)
    character_id = service.extract_character_id_from_url(character_url)

    if not character_id:
        return None

    # Try API first (requires token)
    if cobalt_token:
        raw_data = await service.get_character_data(character_id)
        if raw_data:
            return service.parse_character_data(raw_data)

    # Fallback to scraping for public sheets
    return await service.scrape_character_sheet(character_url)
