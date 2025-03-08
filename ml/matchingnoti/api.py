# api.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import logging
import json
from geopy.distance import geodesic
from matching_engine import MatchingEngine

# Database setup
from database import SessionLocal, engine
from models import Base, User, Organization, Donation, Claim, Notification, \
    FoodCategoryPreference, DietaryRestriction, AllergenRestriction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FoodBridge API",
    description="API for Food Donation Matching Marketplace",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------
# Pydantic Schemas
# --------------------------

class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str
    city: str
    state: str
    zip_code: str
    location: Coordinates
    org_type: str = Field(..., regex="^(shelter|food_bank|community_center|school|other)$")
    capacity_kg: float = Field(..., gt=0)
    operating_hours: Dict[str, str]  # {"monday": "9am-5pm", ...}
    storage_options: Dict[str, bool] = {
        "refrigeration": False,
        "freezer": False,
        "dry_storage": False
    }
    transportation_available: bool = False

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class FoodCategoryPreferenceBase(BaseModel):
    category: str
    priority: int = Field(1, ge=1, le=10)

class DietaryRestrictionBase(BaseModel):
    restriction: str

class AllergenRestrictionBase(BaseModel):
    allergen: str

class DonationBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str]
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., regex="^(kg|lb|items|liters)$")
    category: str
    expiration_date: Optional[datetime]
    storage_requirements: str = Field(..., regex="^(ambient|refrigerated|frozen)$")
    pickup_window_start: datetime
    pickup_window_end: datetime
    location: Coordinates
    allergens: List[str] = []

    @validator("pickup_window_end")
    def validate_pickup_window(cls, v, values):
        if "pickup_window_start" in values and v <= values["pickup_window_start"]:
            raise ValueError("Pickup window end must be after start")
        return v

class DonationCreate(DonationBase):
    pass

class DonationResponse(DonationBase):
    id: int
    status: str = Field(..., regex="^(available|claimed|expired|picked_up)$")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ClaimBase(BaseModel):
    donation_id: int
    scheduled_pickup_time: datetime
    notes: Optional[str]

class ClaimResponse(ClaimBase):
    id: int
    status: str = Field(..., regex="^(pending|confirmed|completed|cancelled)$")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    message: str
    notification_type: str = Field(..., regex="^(match|reminder|system|alert)$")
    donation_id: Optional[int]
    urgency_level: int = Field(1, ge=1, le=3)

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True

class MatchResult(BaseModel):
    donation: DonationResponse
    organization: OrganizationResponse
    match_score: float
    score_details: Dict[str, float]

# --------------------------
# Background Tasks
# --------------------------

def process_donation_matches(donation_id: int, db: Session):
    try:
        engine = MatchingEngine(db)
        engine.process_new_donation(donation_id)
        logger.info(f"Processed matches for donation {donation_id}")
    except Exception as e:
        logger.error(f"Error processing donation {donation_id}: {str(e)}")

def expire_donations(db: Session):
    try:
        now = datetime.utcnow()
        expired = db.query(Donation).filter(
            Donation.status == "available",
            Donation.pickup_window_end < now
        ).update({"status": "expired"})
        db.commit()
        logger.info(f"Expired {expired} donations")
    except Exception as e:
        logger.error(f"Error expiring donations: {str(e)}")
        db.rollback()

# --------------------------
# API Endpoints
# --------------------------

@app.post("/organizations/", 
         response_model=OrganizationResponse,
         status_code=status.HTTP_201_CREATED,
         summary="Create new organization",
         tags=["Organizations"])
async def create_organization(
    organization: OrganizationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new organization profile with storage capabilities and preferences"""
    try:
        db_org = Organization(**organization.dict())
        db.add(db_org)
        db.commit()
        db.refresh(db_org)
        
        # Schedule initial matching
        background_tasks.add_task(
            MatchingEngine(db).match_existing_donations,
            db_org.id
        )
        
        return db_org
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating organization"
        )

@app.get("/organizations/{org_id}",
        response_model=OrganizationResponse,
        tags=["Organizations"])
def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Get organization details by ID"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org

@app.post("/donations/",
         response_model=DonationResponse,
         status_code=status.HTTP_201_CREATED,
         tags=["Donations"])
async def create_donation(
    donation: DonationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new food donation listing"""
    try:
        db_donation = Donation(**donation.dict(), status="available")
        db.add(db_donation)
        db.commit()
        db.refresh(db_donation)
        
        # Trigger matching and expiration checks
        background_tasks.add_task(process_donation_matches, db_donation.id, db)
        background_tasks.add_task(expire_donations, db)
        
        return db_donation
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating donation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating donation"
        )

@app.get("/donations/available",
        response_model=List[DonationResponse],
        tags=["Donations"])
def get_available_donations(
    category: Optional[str] = None,
    min_quantity: Optional[float] = None,
    max_distance: Optional[float] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get available donations with optional filters"""
    query = db.query(Donation).filter(Donation.status == "available")
    
    if category:
        query = query.filter(Donation.category == category)
        
    if min_quantity:
        query = query.filter(Donation.quantity >= min_quantity)
        
    if max_distance and lat and lon:
        # Simple distance filtering (for demonstration)
        donations = query.all()
        filtered = []
        for donation in donations:
            donor_loc = (donation.location["latitude"], donation.location["longitude"])
            org_loc = (lat, lon)
            distance = geodesic(donor_loc, org_loc).kilometers
            if distance <= max_distance:
                filtered.append(donation)
        return filtered
        
    return query.offset(skip).limit(limit).all()

@app.post("/claims/",
         response_model=ClaimResponse,
         status_code=status.HTTP_201_CREATED,
         tags=["Claims"])
def create_claim(claim: ClaimBase, db: Session = Depends(get_db)):
    """Claim a donation"""
    donation = db.query(Donation).get(claim.donation_id)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    
    if donation.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation is no longer available"
        )
    
    try:
        db_claim = Claim(**claim.dict(), status="pending")
        donation.status = "claimed"
        db.add(db_claim)
        db.commit()
        db.refresh(db_claim)
        return db_claim
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating claim: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating claim"
        )

@app.get("/organizations/{org_id}/matches",
        response_model=List[MatchResult],
        tags=["Matching"])
def get_organization_matches(
    org_id: int,
    db: Session = Depends(get_db),
    min_score: float = 0.5,
    limit: int = 20
):
    """Get best matches for an organization"""
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    engine = MatchingEngine(db)
    matches = engine.get_organization_matches(org_id, min_score, limit)
    
    return [{
        "donation": match.donation,
        "organization": org,
        "match_score": match.score,
        "score_details": {
            "category": match.category_score,
            "capacity": match.capacity_score,
            "timing": match.timing_score,
            "distance": match.distance_score
        }
    } for match in matches]

@app.get("/organizations/{org_id}/notifications",
        response_model=List[NotificationResponse],
        tags=["Notifications"])
def get_notifications(
    org_id: int,
    unread_only: bool = True,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get organization notifications"""
    query = db.query(Notification).filter(
        Notification.organization_id == org_id
    )
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
        
    return query.order_by(Notification.created_at.desc()
                         ).offset(skip).limit(limit).all()

@app.put("/notifications/{notification_id}/read",
        status_code=status.HTTP_204_NO_CONTENT,
        tags=["Notifications"])
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """Mark notification as read"""
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_read = True
    db.commit()
    return

# --------------------------
# Maintenance Endpoints
# --------------------------

@app.post("/maintenance/expire-donations",
         tags=["Maintenance"])
async def trigger_expiration(background_tasks: BackgroundTasks,
                           db: Session = Depends(get_db)):
    """Manually trigger donation expiration check"""
    background_tasks.add_task(expire_donations, db)
    return {"status": "Expiration process started"}

@app.post("/maintenance/match-all",
         tags=["Maintenance"])
async def trigger_full_matching(background_tasks: BackgroundTasks,
                              db: Session = Depends(get_db)):
    """Trigger full matching process for all donations"""
    donations = db.query(Donation).filter(
        Donation.status == "available"
    ).all()
    
    for donation in donations:
        background_tasks.add_task(process_donation_matches, donation.id, db)
    
    return {"status": f"Matching triggered for {len(donations)} donations"}

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import APIRouter

router = APIRouter()

@router.post("/notifications/generate")
async def generate_notifications(background_tasks: BackgroundTasks):
    """Trigger notification generation"""
    background_tasks.add_task(NotificationEngine(SessionLocal()).generate_notifications)
    return {"status": "Notification generation started"}

@router.get("/users/{user_id}/notifications", response_model=List[NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    """Get personalized notifications for user"""
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).order_by(Notification.relevance_score.desc()).all()

@router.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """Mark notification as read"""
    notification = db.query(Notification).get(notification_id)
    if notification:
        notification.is_read = True
        db.commit()
    return {"status": "success"}