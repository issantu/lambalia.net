# Lambalia Eats - Real-time Food Marketplace Models (Uber for Home Cooking)
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid

class ServiceType(str, Enum):
    PICKUP = "pickup"           # Eater picks up, pays meal only
    DELIVERY = "delivery"       # Eater pays meal + delivery, cook/3rd party delivers  
    DINE_IN = "dine_in"        # Eater dines at cook's place
    DINE_IN_TRANSPORT = "dine_in_transport"  # Dine-in + pickup/dropoff service

class RequestStatus(str, Enum):
    POSTED = "posted"           # Food request posted by eater
    MATCHED = "matched"         # Cook accepted the request
    PREPARING = "preparing"     # Cook is preparing the meal
    READY = "ready"            # Meal ready for pickup/delivery
    IN_TRANSIT = "in_transit"  # Being delivered or eater on way
    DELIVERED = "delivered"     # Meal delivered/picked up
    DINING = "dining"          # Eater is dining (for dine-in)
    COMPLETED = "completed"     # Transaction completed
    CANCELLED = "cancelled"     # Request cancelled

class OfferStatus(str, Enum):
    AVAILABLE = "available"     # Meal available for order
    RESERVED = "reserved"       # Someone ordering but not paid
    SOLD = "sold"              # Meal sold and being prepared
    READY = "ready"            # Ready for pickup/delivery
    IN_TRANSIT = "in_transit"  # Being delivered
    COMPLETED = "completed"     # Transaction completed
    EXPIRED = "expired"        # Offer expired

class TransportationMethod(str, Enum):
    COOK_DELIVERY = "cook_delivery"        # Cook delivers personally
    THIRD_PARTY = "third_party_delivery"   # External delivery service
    EATER_PICKUP = "eater_pickup"         # Eater picks up
    PLATFORM_TRANSPORT = "platform_transport"  # Lambalia transport service

class CuisineCategory(str, Enum):
    AMERICAN = "american"
    MEXICAN = "mexican"
    ITALIAN = "italian"
    CHINESE = "chinese"
    INDIAN = "indian"
    JAPANESE = "japanese"
    THAI = "thai"
    MEDITERRANEAN = "mediterranean"
    AFRICAN = "african"
    MIDDLE_EASTERN = "middle_eastern"
    CARIBBEAN = "caribbean"
    FUSION = "fusion"
    COMFORT_FOOD = "comfort_food"
    HEALTHY = "healthy"
    VEGAN = "vegan"
    DESSERTS = "desserts"

# EATER REQUESTS - "I want to eat X"
class FoodRequest(BaseModel):
    """Food request posted by hungry eaters"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    eater_id: str
    
    # Request Details
    dish_name: str = Field(..., min_length=3, max_length=100)
    cuisine_type: CuisineCategory
    description: str = Field(..., max_length=500)
    dietary_restrictions: List[str] = []  # ["vegetarian", "gluten_free", "nut_free"]
    spice_level: str = "medium"  # "mild", "medium", "hot", "extra_hot"
    
    # Service Preferences
    preferred_service_types: List[ServiceType] = []
    max_price: float = Field(..., gt=0, le=500)  # Maximum willing to pay
    max_delivery_fee: float = Field(default=15.0, ge=0, le=50)
    max_wait_time_minutes: int = Field(default=90, ge=15, le=300)  # Max wait time
    
    # Location & Timing
    eater_location: Dict[str, float] = {}  # {"lat": 40.7128, "lng": -74.0060}
    eater_address: str
    preferred_pickup_time: Optional[datetime] = None
    flexible_timing: bool = True
    
    # Preferences
    preferred_cook_rating: float = Field(default=3.0, ge=1.0, le=5.0)
    cook_gender_preference: Optional[str] = None  # "any", "female", "male"
    language_preferences: List[str] = []  # ["english", "spanish"]
    
    # Status & Matching
    status: RequestStatus = RequestStatus.POSTED
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=4))
    matched_offer_id: Optional[str] = None
    matched_cook_id: Optional[str] = None
    
    # Real-time Tracking
    estimated_ready_time: Optional[datetime] = None
    actual_ready_time: Optional[datetime] = None
    tracking_updates: List[Dict[str, Any]] = []
    
    # Financial
    agreed_price: Optional[float] = None
    delivery_fee: Optional[float] = None
    service_fee: Optional[float] = None  # Lambalia's commission
    total_amount: Optional[float] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# COOK OFFERS - "I have X ready to serve"
class FoodOffer(BaseModel):
    """Food offer posted by cooks with ready meals"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cook_id: str
    
    # Dish Details
    dish_name: str = Field(..., min_length=3, max_length=100)
    cuisine_type: CuisineCategory
    description: str = Field(..., max_length=500)
    ingredients: List[str] = []
    dietary_info: List[str] = []  # ["vegetarian", "gluten_free"]
    spice_level: str = "medium"
    
    # Availability
    quantity_available: int = Field(..., ge=1, le=50)
    quantity_remaining: int = Field(..., ge=0)
    serving_size: str = "regular"  # "small", "regular", "large"
    
    # Pricing
    price_per_serving: float = Field(..., gt=0, le=200)
    
    # Service Options Available
    available_service_types: List[ServiceType] = []
    delivery_radius_km: float = Field(default=15.0, ge=1.0, le=50.0)
    delivery_fee: float = Field(default=5.0, ge=0, le=30)
    pickup_instructions: str = ""
    dine_in_capacity: int = Field(default=0, ge=0, le=20)  # How many can dine-in
    
    # Location
    cook_location: Dict[str, float] = {}  # {"lat": 40.7128, "lng": -74.0060}
    cook_address: str
    pickup_address: Optional[str] = None  # Different pickup location if needed
    
    # Timing
    ready_at: datetime  # When meal will be ready
    available_until: datetime  # When offer expires
    preparation_time_minutes: int = Field(default=30, ge=5, le=180)
    
    # Status
    status: OfferStatus = OfferStatus.AVAILABLE
    
    # Media
    food_photos: List[str] = []  # URLs to food images
    
    # Cook Info (for standalone app users)
    cook_name: str = ""
    cook_rating: float = Field(default=5.0, ge=1.0, le=5.0)
    cook_photo_url: Optional[str] = None
    cook_specialties: List[str] = []
    
    # Real-time Updates
    preparation_updates: List[Dict[str, Any]] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ACTIVE ORDERS - Real-time Order Tracking
class ActiveOrder(BaseModel):
    """Active order being tracked in real-time"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Participants
    eater_id: str
    cook_id: str
    request_id: Optional[str] = None  # If from food request
    offer_id: Optional[str] = None    # If from food offer
    
    # Order Details
    dish_name: str
    quantity: int = 1
    service_type: ServiceType
    
    # Location Tracking
    eater_location: Dict[str, float] = {}
    cook_location: Dict[str, float] = {}
    delivery_address: Optional[str] = None
    
    # Timing
    ordered_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_ready_time: datetime
    estimated_delivery_time: Optional[datetime] = None
    actual_ready_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    
    # Status Tracking
    current_status: str = "confirmed"  # "confirmed", "preparing", "ready", "in_transit", "delivered"
    status_updates: List[Dict[str, Any]] = []
    
    # Real-time Tracking (for delivery/pickup)
    driver_location: Optional[Dict[str, float]] = None  # Current driver location
    estimated_arrival: Optional[datetime] = None
    tracking_code: str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    
    # Financial
    meal_price: float
    delivery_fee: float = 0.0
    service_fee: float = 0.0  # Platform commission
    transport_fee: float = 0.0  # For dine-in transport
    total_amount: float
    
    # Communication
    chat_messages: List[Dict[str, Any]] = []
    
    # Completion
    completed_at: Optional[datetime] = None
    rating_by_eater: Optional[float] = None
    rating_by_cook: Optional[float] = None
    feedback_eater: Optional[str] = None
    feedback_cook: Optional[str] = None

# COOK PROFILES - For Standalone App
class EatsCookProfile(BaseModel):
    """Cook profile specifically for Lambalia Eats app"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str  # Links to main Lambalia user
    
    # Public Profile
    display_name: str
    bio: str = Field(default="", max_length=300)
    profile_photo_url: Optional[str] = None
    
    # Cooking Info
    specialties: List[CuisineCategory] = []
    cooking_experience_years: int = Field(default=1, ge=0, le=50)
    signature_dishes: List[str] = []
    
    # Service Capabilities
    available_service_types: List[ServiceType] = []
    max_delivery_radius_km: float = Field(default=10.0, ge=1.0, le=50.0)
    max_daily_orders: int = Field(default=10, ge=1, le=100)
    dine_in_available: bool = False
    kitchen_capacity: int = Field(default=2, ge=1, le=20)  # Max simultaneous orders
    
    # Location
    base_location: Dict[str, float] = {}
    service_address: str
    pickup_instructions: str = ""
    
    # Availability
    operating_hours: Dict[str, Dict[str, str]] = {}  # {"monday": {"start": "09:00", "end": "21:00"}}
    available_days: List[str] = []  # ["monday", "tuesday", ...]
    is_currently_available: bool = True
    next_available_slot: Optional[datetime] = None
    
    # Ratings & Reviews
    overall_rating: float = Field(default=5.0, ge=1.0, le=5.0)
    total_orders: int = 0
    total_reviews: int = 0
    recent_reviews: List[Dict[str, Any]] = []
    
    # Financial
    earnings_this_month: float = 0.0
    preferred_payment_methods: List[str] = ["cash", "card", "digital"]
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    verification_documents: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)

# EATER PROFILES - For Standalone App
class EatsEaterProfile(BaseModel):
    """Eater profile for Lambalia Eats app"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None  # Links to main Lambalia user (optional for standalone)
    
    # Profile
    display_name: str
    profile_photo_url: Optional[str] = None
    phone_number: str
    
    # Preferences
    favorite_cuisines: List[CuisineCategory] = []
    dietary_restrictions: List[str] = []
    spice_tolerance: str = "medium"
    price_range_preference: str = "moderate"  # "budget", "moderate", "premium"
    
    # Location
    default_location: Dict[str, float] = {}
    saved_addresses: List[Dict[str, str]] = []  # [{"name": "Home", "address": "123 Main St"}]
    
    # Order History
    total_orders: int = 0
    favorite_cooks: List[str] = []  # Cook IDs
    recent_orders: List[str] = []   # Order IDs
    
    # Ratings
    average_rating_given: float = 5.0
    
    # Status
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_order_date: Optional[datetime] = None

# MATCHING & ANALYTICS
class MatchingResult(BaseModel):
    """Result from matching algorithm"""
    request_id: str
    matched_offers: List[Dict[str, Any]] = []  # Ranked offers
    match_score: float = 0.0
    match_reasons: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EatsAnalytics(BaseModel):
    """Analytics for Lambalia Eats platform"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = Field(default_factory=datetime.utcnow)
    
    # Order Metrics
    total_orders: int = 0
    successful_orders: int = 0
    cancelled_orders: int = 0
    average_order_value: float = 0.0
    
    # Service Type Distribution
    pickup_orders: int = 0
    delivery_orders: int = 0
    dine_in_orders: int = 0
    
    # Revenue Metrics
    total_revenue: float = 0.0
    platform_commission: float = 0.0
    average_commission_rate: float = 0.15
    
    # Performance Metrics
    average_preparation_time: float = 0.0
    average_delivery_time: float = 0.0
    customer_satisfaction_rating: float = 0.0
    
    # Geographic Data
    top_neighborhoods: List[Dict[str, Any]] = []
    delivery_heatmap_data: List[Dict[str, Any]] = []

# API REQUEST/RESPONSE MODELS

class FoodRequestSubmission(BaseModel):
    dish_name: str = Field(..., min_length=3, max_length=100)
    cuisine_type: str
    description: str = Field(..., max_length=500)
    dietary_restrictions: List[str] = []
    preferred_service_types: List[str] = []
    max_price: float = Field(..., gt=0, le=500)
    max_delivery_fee: float = Field(default=15.0, ge=0)
    max_wait_time_minutes: int = Field(default=90, ge=15, le=300)
    eater_location: Dict[str, float]
    eater_address: str
    preferred_pickup_time: Optional[str] = None
    flexible_timing: bool = True

class FoodOfferSubmission(BaseModel):
    dish_name: str = Field(..., min_length=3, max_length=100)
    cuisine_type: str
    description: str = Field(..., max_length=500)
    ingredients: List[str] = []
    dietary_info: List[str] = []
    quantity_available: int = Field(..., ge=1, le=50)
    price_per_serving: float = Field(..., gt=0, le=200)
    available_service_types: List[str] = []
    delivery_radius_km: float = Field(default=15.0, ge=1.0, le=50.0)
    delivery_fee: float = Field(default=5.0, ge=0)
    ready_at: str  # ISO datetime string
    available_until: str  # ISO datetime string
    cook_location: Dict[str, float]
    cook_address: str
    food_photos: List[str] = []

class OrderPlacementRequest(BaseModel):
    offer_id: Optional[str] = None
    request_id: Optional[str] = None
    service_type: str
    quantity: int = Field(default=1, ge=1, le=10)
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    payment_method: str = "card"

class RealTimeUpdate(BaseModel):
    order_id: str
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[Dict[str, float]] = None
    estimated_time: Optional[int] = None  # Minutes

class EatsStatsResponse(BaseModel):
    active_requests: int
    active_offers: int
    orders_in_progress: int
    available_cooks: int
    average_match_time_minutes: float
    popular_cuisines: List[Dict[str, int]]
    platform_commission_today: float