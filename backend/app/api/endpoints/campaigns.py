from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core import get_db
from ...models import Campaign as CampaignModel, User, CampaignMember, CampaignRole
from ...schemas import Campaign, CampaignCreate, CampaignUpdate, CampaignDetail, CampaignMemberCreate
from ...api.deps import get_current_active_user

router = APIRouter()


def check_campaign_access(campaign_id: int, user: User, db: Session, required_role: CampaignRole = None):
    """Check if user has access to campaign and optionally verify role."""
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Owner has all access
    if campaign.owner_id == user.id:
        return campaign

    # Check membership
    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == user.id
    ).first()

    if not member:
        raise HTTPException(status_code=403, detail="Access denied")

    if required_role and member.role != required_role and campaign.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return campaign


@router.post("", response_model=Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_in: CampaignCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new campaign."""
    campaign = CampaignModel(**campaign_in.dict(), owner_id=current_user.id)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("", response_model=List[Campaign])
def list_campaigns(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all campaigns user has access to."""
    # Get campaigns owned by user
    owned = db.query(CampaignModel).filter(CampaignModel.owner_id == current_user.id).all()

    # Get campaigns user is a member of
    memberships = db.query(CampaignMember).filter(CampaignMember.user_id == current_user.id).all()
    member_campaign_ids = [m.campaign_id for m in memberships]
    member_campaigns = db.query(CampaignModel).filter(CampaignModel.id.in_(member_campaign_ids)).all()

    # Combine and return
    all_campaigns = list(set(owned + member_campaigns))
    return all_campaigns[skip:skip + limit]


@router.get("/{campaign_id}", response_model=CampaignDetail)
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific campaign with details."""
    campaign = check_campaign_access(campaign_id, current_user, db)
    return campaign


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a campaign (owner or DM only)."""
    campaign = check_campaign_access(campaign_id, current_user, db, CampaignRole.DM)

    # Only owner can update
    if campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only campaign owner can update")

    for field, value in campaign_update.dict(exclude_unset=True).items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a campaign (owner only)."""
    campaign = check_campaign_access(campaign_id, current_user, db)

    if campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only campaign owner can delete")

    db.delete(campaign)
    db.commit()
    return None


@router.post("/{campaign_id}/members", status_code=status.HTTP_201_CREATED)
def add_campaign_member(
    campaign_id: int,
    member_in: CampaignMemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a member to campaign (owner or DM only)."""
    campaign = check_campaign_access(campaign_id, current_user, db, CampaignRole.DM)

    # Check if user exists
    user = db.query(User).filter(User.id == member_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already a member
    existing = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == member_in.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a member")

    member = CampaignMember(campaign_id=campaign_id, **member_in.dict())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{campaign_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_campaign_member(
    campaign_id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a member from campaign (owner or DM only)."""
    campaign = check_campaign_access(campaign_id, current_user, db, CampaignRole.DM)

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()
    return None
