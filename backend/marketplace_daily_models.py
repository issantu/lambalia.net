# Daily Marketplace Models for Dynamic Offer & Demand System
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CookingOfferStatus(str, Enum):
    ACTIVE = "active"
    FULLY_BOOKED = "fully_booked"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class EatingRequestStatus(str, Enum):
    ACTIVE = "active"
    MATCHED = "matched"
    FULFILLED = "fulfilled"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class MealCategory(str, Enum):
    QUICK_MEALS = "quick_meals"
    FAMILY_DINNER = "family_dinner"
    CULTURAL_SPECIALTIES = "cultural_specialties"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    BRUNCH = "brunch"
    SNACKS = "snacks"
    DESSERTS = "desserts"
    JULY_4TH = "july_4th"
    CINCO_DE_MAYO = "cinco_de_mayo"
    THANKSGIVING = "thanksgiving"
    CHRISTMAS = "christmas"
    NEW_YEAR = "new_year"
    VALENTINES_DAY = "valentines_day"
    MOTHERS_DAY = "mothers_day"
    FATHERS_DAY = "fathers_day"
    EASTER = "easter"
    HALLOWEEN = "halloween"
    DIWALI = "diwali"
    CHINESE_NEW_YEAR = "chinese_new_year"
    RAMADAN = "ramadan"
    EID = "eid"
    HANUKKAH = "hanukkah"
    KWANZAA = "kwanzaa"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    GRADUATION = "graduation"
    BABY_SHOWER = "baby_shower"
    WEDDING = "wedding"
    CASUAL = "casual"
    FORMAL = "formal"
    COMFORT_FOOD = "comfort_food"
    HEALTHY = "healthy"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    GLUTEN_FREE = "gluten_free"
    KETO = "keto"
    PALEO = "paleo"

class CookingOffer(BaseModel):
    """
    Daily cooking offer posted by home cooks
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cook_id: str
    
    # Offer Details
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    dish_name: str = Field(..., min_length=2, max_length=80)  # Preserve native names
    cuisine_type: str
    category: MealCategory
    
    # Availability & Capacity
    cooking_date: datetime
    available_time_start: str = Field(..., pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')  # HH:MM format
    available_time_end: str = Field(..., pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    max_servings: int = Field(..., ge=1, le=20)
    remaining_servings: int
    
    # Location (for local matching)
    location: Dict[str, Any] = Field(default_factory=lambda: {"type": "Point", "coordinates": [0.0, 0.0]})
    address: str
    postal_code: str
    city: str
    country: str = "US"
    
    # Pricing (platform-determined)
    price_per_serving: float = Field(..., ge=8.0, le=50.0)
    platform_commission: float = 0.15
    cook_payout_per_serving: float = 0.0  # Calculated
    
    # Dietary & Preferences
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = False
    is_kosher: bool = False
    allergen_info: List[str] = []
    spice_level: Optional[str] = None  # "mild", "medium", "hot", "very_hot"
    
    # Media
    photos: List[str] = []  # URLs to photos
    
    # Status & Metadata
    status: CookingOfferStatus = CookingOfferStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=3))
    view_count: int = 0
    interest_count: int = 0
    booking_count: int = 0
    
    # Special Requirements
    pickup_available: bool = True
    delivery_available: bool = False
    dine_in_available: bool = True  # Eat at cook's home
    special_instructions: str = ""
    
    @validator('cook_payout_per_serving', always=True)
    def calculate_cook_payout(cls, v, values):
        if 'price_per_serving' in values and 'platform_commission' in values:
            return round(values['price_per_serving'] * (1 - values['platform_commission']), 2)
        return v
    
    @validator('remaining_servings', always=True)
    def set_remaining_servings(cls, v, values):
        if v == 0 and 'max_servings' in values:
            return values['max_servings']
        return v

class EatingRequest(BaseModel):
    """
    Eating request posted by food lovers looking for specific meals
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    eater_id: str
    
    # Request Details
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    desired_cuisine: Optional[str] = None
    desired_dish: Optional[str] = None
    category: Optional[MealCategory] = None
    
    # Preferences
    preferred_date: Optional[datetime] = None
    flexible_dates: bool = True
    preferred_time_start: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    preferred_time_end: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    number_of_servings: int = Field(..., ge=1, le=8)
    
    # Location (for matching)
    location: Dict[str, Any] = Field(default_factory=lambda: {"type": "Point", "coordinates": [0.0, 0.0]})
    address: str
    postal_code: str
    city: str
    country: str = "US"
    max_distance_km: float = Field(default=20.0, le=50.0)
    
    # Budget & Pricing
    max_price_per_serving: float = Field(..., ge=5.0, le=100.0)
    
    # Dietary Requirements
    dietary_restrictions: List[str] = []
    allergen_concerns: List[str] = []
    spice_tolerance: Optional[str] = None  # "mild", "medium", "hot", "very_hot"
    
    # Service Preferences
    pickup_preferred: bool = False
    delivery_preferred: bool = False
    dine_in_preferred: bool = True
    
    # Status & Metadata
    status: EatingRequestStatus = EatingRequestStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=3))
    view_count: int = 0
    match_count: int = 0
    
    # Matching
    matched_offers: List[str] = []  # List of offer IDs that match this request
    selected_offer_id: Optional[str] = None

class CookOfferMatch(BaseModel):
    """
    Match between a cooking offer and eating request
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    offer_id: str
    request_id: str
    cook_id: str
    eater_id: str
    
    # Match Details
    compatibility_score: float = Field(..., ge=0.0, le=1.0)  # Algorithm-calculated
    distance_km: float
    price_match: bool
    dietary_match: bool
    time_match: bool
    category_match: bool
    
    # Match Status  
    is_visible_to_eater: bool = True
    is_selected: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Additional Info
    match_reasons: List[str] = []  # Why this is a good match
    potential_concerns: List[str] = []  # Any potential issues

class CookingAppointment(BaseModel):
    """
    Confirmed appointment between cook and eater
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    offer_id: str
    request_id: Optional[str] = None  # May be direct booking without request
    cook_id: str
    eater_id: str
    
    # Appointment Details
    scheduled_date: datetime
    scheduled_time_start: str
    scheduled_time_end: str
    number_of_servings: int
    service_type: str  # "pickup", "delivery", "dine_in"
    
    # Location Details
    service_address: str  # Where the service happens
    cook_address: str
    eater_address: Optional[str] = None
    
    # Pricing
    total_amount: float
    platform_commission_amount: float
    cook_payout_amount: float
    
    # Communication
    eater_notes: str = ""
    cook_notes: str = ""
    special_requests: str = ""
    
    # Status & Timeline
    status: AppointmentStatus = AppointmentStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    # Payment
    payment_id: Optional[str] = None
    payment_status: str = "pending"
    
    # Follow-up
    cook_rating: Optional[float] = None
    eater_rating: Optional[float] = None
    cook_review: Optional[str] = None
    eater_review: Optional[str] = None

# Request/Response Models for API

class CookingOfferRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    dish_name: str = Field(..., min_length=2, max_length=80)
    cuisine_type: str
    category: MealCategory
    cooking_date: str  # ISO format
    available_time_start: str = Field(..., regex=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    available_time_end: str = Field(..., regex=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    max_servings: int = Field(..., ge=1, le=20)
    postal_code: str
    city: str
    country: str = "US"
    price_per_serving: float = Field(..., ge=8.0, le=50.0)
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = False
    is_kosher: bool = False
    allergen_info: List[str] = []
    spice_level: Optional[str] = None
    photos: List[str] = []
    pickup_available: bool = True
    delivery_available: bool = False
    dine_in_available: bool = True
    special_instructions: str = ""

class EatingRequestRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    desired_cuisine: Optional[str] = None
    desired_dish: Optional[str] = None
    category: Optional[MealCategory] = None
    preferred_date: Optional[str] = None  # ISO format
    flexible_dates: bool = True
    preferred_time_start: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    preferred_time_end: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    number_of_servings: int = Field(..., ge=1, le=8)
    postal_code: str
    city: str
    country: str = "US"
    max_distance_km: float = Field(default=20.0, le=50.0)
    max_price_per_serving: float = Field(..., ge=5.0, le=100.0)
    dietary_restrictions: List[str] = []
    allergen_concerns: List[str] = []
    spice_tolerance: Optional[str] = None
    pickup_preferred: bool = False
    delivery_preferred: bool = False
    dine_in_preferred: bool = True

class AppointmentRequest(BaseModel):
    offer_id: str
    request_id: Optional[str] = None
    scheduled_date: str  # ISO format
    scheduled_time_start: str
    scheduled_time_end: str
    number_of_servings: int = Field(..., ge=1, le=20)
    service_type: str  # "pickup", "delivery", "dine_in"
    service_address: str
    eater_notes: str = ""
    special_requests: str = ""

class CookingOfferResponse(BaseModel):
    id: str
    cook_id: str
    cook_name: str
    cook_rating: float
    title: str
    description: str
    dish_name: str
    cuisine_type: str
    category: str
    cooking_date: datetime
    available_time_start: str
    available_time_end: str
    max_servings: int
    remaining_servings: int
    price_per_serving: float
    cook_payout_per_serving: float
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool
    allergen_info: List[str]
    spice_level: Optional[str]
    photos: List[str]
    pickup_available: bool
    delivery_available: bool
    dine_in_available: bool
    status: str
    view_count: int
    interest_count: int
    distance_km: Optional[float] = None
    created_at: datetime

class EatingRequestResponse(BaseModel):
    id: str
    eater_id: str
    eater_name: str
    title: str
    description: str
    desired_cuisine: Optional[str]
    desired_dish: Optional[str]
    category: Optional[str]
    preferred_date: Optional[datetime]
    number_of_servings: int
    max_price_per_serving: float
    dietary_restrictions: List[str]
    service_preferences: List[str]
    status: str
    match_count: int
    distance_km: Optional[float] = None
    created_at: datetime

class AppointmentResponse(BaseModel):
    id: str
    offer_title: str
    cook_name: str
    eater_name: str
    scheduled_date: datetime
    scheduled_time_start: str
    scheduled_time_end: str
    number_of_servings: int
    service_type: str
    total_amount: float
    status: str
    created_at: datetime
    confirmation_code: str