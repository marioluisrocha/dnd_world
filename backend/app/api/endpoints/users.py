from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import User as UserModel
from ...schemas import User, UserUpdate
from ...api.deps import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=User)
def read_current_user(current_user: UserModel = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    if user_update.email:
        # Check if email is taken
        existing = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = user_update.email

    if user_update.username:
        # Check if username is taken
        existing = db.query(UserModel).filter(
            UserModel.username == user_update.username,
            UserModel.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use"
            )
        current_user.username = user_update.username

    if user_update.password:
        from ...core import get_password_hash
        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/search", response_model=List[User])
def search_users(
    q: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Search for users by email or username."""
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters"
        )

    search_pattern = f"%{q}%"
    users = db.query(UserModel).filter(
        (UserModel.email.ilike(search_pattern)) |
        (UserModel.username.ilike(search_pattern))
    ).limit(limit).all()

    return users
