# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table, Text, Enum
from sqlalchemy.orm import declarative_base, relationship  # Updated import
from datetime import datetime
import enum

# Updated declarative_base usage
Base = declarative_base()

# Enum types
class FoodCategory(enum.Enum):
    PRODUCE = "produce"
    DAIRY = "dairy"
    BAKERY = "bakery"
    MEAT = "meat"
    PREPARED = "prepared"
    CANNED = "canned"
    DRY_GOODS = "dry_goods"
    FROZEN = "frozen"
    BEVERAGES = "beverages"
    OTHER = "other"

class StorageType(enum.Enum):
    ROOM_TEMP = "room_temperature"
    REFRIGERATED = "refrigerated"
    FROZEN = "frozen"

class AllergenType(enum.Enum):
    MILK = "milk"
    EGGS = "eggs"
    FISH = "fish"
    SHELLFISH = "shellfish"
    TREE_NUTS = "tree_nuts"
    PEANUTS = "peanuts"
    WHEAT = "wheat"
    SOYBEANS = "soybeans"
    SESAME = "sesame"

# Association tables
organization_food_category = Table(
    'organization_food_category', 
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('food_category', String)
)

organization_dietary_restrictions = Table(
    'organization_dietary_restrictions', 
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('restriction', String)
)

organization_allergen_restrictions = Table(
    'organization_allergen_restrictions', 
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('allergen', String)
)

donation_allergens = Table(
    'donation_allergens',
    Base.metadata,
    Column('donation_id', Integer, ForeignKey('donations.id')),
    Column('allergen', String)
)

# Main tables
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # donor, recipient, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organizations = relationship("Organization", back_populates="user")

class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    phone = Column(String)
    org_type = Column(String, nullable=False)  # food_bank, shelter, community_kitchen, etc.
    description = Column(Text)
    
    # Operational details
    operating_hours = Column(String)
    has_refrigeration = Column(Boolean, default=False)
    has_freezer = Column(Boolean, default=False)
    has_dry_storage = Column(Boolean, default=False)
    has_transportation = Column(Boolean, default=False)
    storage_capacity_kg = Column(Float)
    
    # Preferences
    preferred_notification_method = Column(String, default="email")
    notification_email = Column(String)
    notification_phone = Column(String)
    max_pickup_distance_km = Column(Float, default=20.0)
    
    # AI-related fields
    acceptance_rate = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.0)
    last_activity = Column(DateTime)
    
    # Relationships
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="organizations")
    donations = relationship("Donation", back_populates="donor_organization", foreign_keys="Donation.donor_organization_id")
    claims = relationship("Claim", back_populates="recipient_organization")
    
    # Many-to-many relationships
    accepted_food_categories = relationship("FoodCategoryPreference", back_populates="organization")
    dietary_restrictions = relationship("DietaryRestriction", back_populates="organization")
    allergen_restrictions = relationship("AllergenRestriction", back_populates="organization")

class FoodCategoryPreference(Base):
    __tablename__ = 'food_category_preferences'
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    category = Column(String, nullable=False)
    preference_level = Column(Integer, default=5)  # 1-10 scale
    
    # Relationship
    organization = relationship("Organization", back_populates="accepted_food_categories")

class DietaryRestriction(Base):
    __tablename__ = 'dietary_restrictions'
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    restriction = Column(String, nullable=False)  # vegetarian, vegan, kosher, halal, etc.
    
    # Relationship
    organization = relationship("Organization", back_populates="dietary_restrictions")

class AllergenRestriction(Base):
    __tablename__ = 'allergen_restrictions'
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    allergen = Column(String, nullable=False)
    
    # Relationship
    organization = relationship("Organization", back_populates="allergen_restrictions")

class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # kg, items, servings, etc.
    category = Column(String, nullable=False)
    subcategory = Column(String)
    expiration_date = Column(DateTime)
    is_perishable = Column(Boolean, default=True)
    storage_requirements = Column(String)
    pickup_instructions = Column(Text)
    
    # Timeframes
    created_at = Column(DateTime, default=datetime.utcnow)
    available_from = Column(DateTime, nullable=False)
    available_until = Column(DateTime, nullable=False)
    
    # Status
    status = Column(String, default="available")  # available, claimed, completed, expired
    
    # Relationships
    donor_organization_id = Column(Integer, ForeignKey('organizations.id'))
    donor_organization = relationship("Organization", back_populates="donations", foreign_keys=[donor_organization_id])
    
    claims = relationship("Claim", back_populates="donation")
    allergens = relationship("DonationAllergen", back_populates="donation")
    
    # AI-related fields
    priority_score = Column(Float, default=0.0)  # Calculated based on perishability, time left, etc.
    matching_score = Column(Float, default=0.0)  # Updated by the AI

class DonationAllergen(Base):
    __tablename__ = 'donation_allergen_items'
    
    id = Column(Integer, primary_key=True)
    donation_id = Column(Integer, ForeignKey('donations.id'))
    allergen = Column(String, nullable=False)
    
    # Relationship
    donation = relationship("Donation", back_populates="allergens")

class Claim(Base):
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True)
    donation_id = Column(Integer, ForeignKey('donations.id'))
    recipient_organization_id = Column(Integer, ForeignKey('organizations.id'))
    
    # Status and timing
    status = Column(String, default="pending")  # pending, accepted, completed, canceled
    claimed_at = Column(DateTime, default=datetime.utcnow)
    pickup_time = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Feedback
    feedback_rating = Column(Integer)  # 1-5 scale
    feedback_comments = Column(Text)
    
    # Relationships
    donation = relationship("Donation", back_populates="claims")
    recipient_organization = relationship("Organization", back_populates="claims")
    
    # AI-related fields
    match_confidence = Column(Float)  # How confident the system was about this match

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    donation_id = Column(Integer, ForeignKey('donations.id'))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    notification_type = Column(String)  # match, reminder, confirmation, etc.
    
    # AI-related fields
    relevance_score = Column(Float)  # How relevant this notification is to the recipient
    
    from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    preferred_cuisines = Column(JSON)  # ["Italian", "Mexican", ...]
    dietary_restrictions = Column(JSON)  # ["vegetarian", "gluten-free", ...]
    favorite_ingredients = Column(JSON)
    disliked_items = Column(JSON)
    notification_preferences = Column(JSON)  # {"email": True, "push": False, ...}
    last_active = Column(DateTime)
