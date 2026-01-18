from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core import get_db
from ...models import Character as CharacterModel, User
from ...schemas import Character
from ...api.deps import get_current_active_user
from ...services import import_character_from_dndbeyond
from .campaigns import check_campaign_access

router = APIRouter()


class DNDBeyondImport(BaseModel):
    campaign_id: int
    character_url: str
    cobalt_token: str = None


@router.post("/import", response_model=Character, status_code=status.HTTP_201_CREATED)
async def import_character(
    import_data: DNDBeyondImport,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import a character from D&D Beyond.

    Requires:
    - campaign_id: The campaign to add the character to
    - character_url: Full D&D Beyond character URL
    - cobalt_token: (Optional) Your D&D Beyond Cobalt session token for private sheets

    To get your Cobalt token:
    1. Log in to D&D Beyond
    2. Open browser DevTools (F12)
    3. Go to Application/Storage > Cookies
    4. Find 'CobaltSession' cookie and copy its value
    """
    # Check campaign access
    check_campaign_access(import_data.campaign_id, current_user, db)

    # Import character data
    character_data = await import_character_from_dndbeyond(
        import_data.character_url,
        import_data.cobalt_token
    )

    if not character_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to import character from D&D Beyond. "
                   "D&D Beyond character sheets require JavaScript to load data, which prevents web scraping. "
                   "Please provide your Cobalt session token to access the character via D&D Beyond's API. "
                   "To get your token: Log in to D&D Beyond → Open DevTools (F12) → Application → Cookies → "
                   "Copy the 'CobaltSession' value."
        )

    # Create character in database
    character = CharacterModel(
        **character_data,
        campaign_id=import_data.campaign_id,
        creator_id=current_user.id,
        dndbeyond_url=import_data.character_url
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    return character
