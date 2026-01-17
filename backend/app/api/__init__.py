from fastapi import APIRouter
from .endpoints import auth, users, campaigns, characters, places, items, quests, sessions, notes, dndbeyond

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(dndbeyond.router, prefix="/dndbeyond", tags=["dndbeyond"])
