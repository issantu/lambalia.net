# Marketplace Models for Home Restaurant and Traditional Restaurant Vetting System
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class VendorStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"

class VendorType(str, Enum):
    HOME_RESTAURANT = "home_restaurant"
    TRADITIONAL_RESTAURANT = "traditional_restaurant"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class OrderStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    FULFILLED = "fulfilled" 
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"

class DocumentType(str, Enum):
    KITCHEN_PHOTO = "kitchen_photo"
    DINING_ROOM_PHOTO = "dining_room_photo"
    FRONT_DOOR_PHOTO = "front_door_photo"
    ID_DOCUMENT = "id_document"
    HEALTH_CERTIFICATE = "health_certificate"
    INSURANCE_PROOF = "insurance_proof"
    BUSINESS_LICENSE = "business_license"
    RESTAURANT_PHOTOS = "restaurant_photos"

class VendorApplication(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    vendor_type: VendorType = VendorType.HOME_RESTAURANT
    
    # Personal Information
    legal_name: str
    phone_number: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    
    # Kitchen Information (for home restaurants)
    kitchen_description: Optional[str] = None
    dining_capacity: Optional[int] = Field(default=None, ge=2, le=20)
    
    # Restaurant Information (for traditional restaurants)
    restaurant_name: Optional[str] = None
    business_license_number: Optional[str] = None
    years_in_business: Optional[int] = 0
    
    # Common Information
    cuisine_specialties: List[str] = []
    dietary_accommodations: List[str] = []
    
    # Verification Documents
    documents: List[Dict[str, str]] = []  # {"type": "kitchen_photo", "url": "...", "status": "pending"}
    
    # Background Check Info
    background_check_consent: bool = False
    has_food_handling_experience: bool = False
    years_cooking_experience: int = 0
    
    # Safety & Insurance
    has_liability_insurance: bool = False
    emergency_contact_name: str
    emergency_contact_phone: str
    
    # Application Status
    status: VendorStatus = VendorStatus.PENDING
    application_date: datetime = Field(default_factory=datetime.utcnow)
    review_notes: Optional[str] = None
    reviewer_id: Optional[str] = None
    approval_date: Optional[datetime] = None
    
    # Terms Agreement
    terms_accepted: bool = False
    privacy_policy_accepted: bool = False
    commission_rate_accepted: float = 0.15  # 15% platform fee

class HomeRestaurant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vendor_id: str
    application_id: str
    
    # Restaurant Details
    restaurant_name: str
    description: str
    cuisine_type: List[str] = []
    dining_capacity: int
    
    # Location & Photos
    address: str
    latitude: float
    longitude: float
    photos: List[Dict[str, str]] = []  # {"type": "kitchen", "url": "...", "caption": "..."}
    
    # Pricing & Availability
    base_price_per_person: float = Field(ge=15.0, le=150.0)
    is_pricing_dynamic: bool = True  # Platform controls pricing
    
    # Operating Schedule
    operating_days: List[str] = []  # ["monday", "friday", "saturday"]
    operating_hours: Dict[str, Dict[str, str]] = {}  # {"monday": {"start": "18:00", "end": "22:00"}}
    advance_booking_days: int = 7  # How many days in advance bookings are accepted
    
    # Reviews & Ratings
    average_rating: float = 0.0
    total_reviews: int = 0
    total_bookings: int = 0
    
    # Status
    is_active: bool = True
    is_accepting_bookings: bool = True
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MenuOffering(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    restaurant_id: str
    
    # Menu Details
    menu_name: str
    description: str
    cuisine_style: str
    
    # Courses
    appetizers: List[Dict[str, str]] = []
    main_courses: List[Dict[str, str]] = []
    desserts: List[Dict[str, str]] = []
    beverages: List[Dict[str, str]] = []
    
    # Pricing (Platform Controlled)
    platform_price_per_person: float
    vendor_payout_per_person: float  # After commission
    
    # Dietary Info
    vegetarian_options: bool = False
    vegan_options: bool = False
    gluten_free_options: bool = False
    allergen_info: List[str] = []
    
    # Availability
    available_dates: List[str] = []  # ISO date strings
    max_guests_per_booking: int = 8
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Booking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Participants
    guest_id: str
    restaurant_id: str
    vendor_id: str
    
    # Booking Details
    booking_date: datetime
    number_of_guests: int
    menu_offering_id: str
    
    # Pricing
    price_per_person: float
    total_amount: float
    platform_commission: float
    vendor_payout: float
    
    # Special Requests
    dietary_restrictions: List[str] = []
    special_requests: str = ""
    guest_message: str = ""
    
    # Status & Timestamps
    status: BookingStatus = BookingStatus.PENDING
    booking_created: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    # Payment Info
    payment_id: str
    payment_status: PaymentStatus = PaymentStatus.PENDING
    
class Payment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    booking_id: str
    
    # Payment Details
    amount: float
    currency: str = "USD"
    platform_commission: float
    vendor_payout: float
    
    # Stripe Integration
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    
    # Status & Processing
    status: PaymentStatus = PaymentStatus.PENDING
    processed_at: Optional[datetime] = None
    payout_date: Optional[datetime] = None
    
    # Metadata
    payment_method: str = "card"  # card, bank_transfer, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    booking_id: str
    guest_id: str
    restaurant_id: str
    vendor_id: str
    
    # Review Content
    overall_rating: int = Field(ge=1, le=5)
    food_quality_rating: int = Field(ge=1, le=5)
    hospitality_rating: int = Field(ge=1, le=5)
    cleanliness_rating: int = Field(ge=1, le=5)
    value_rating: int = Field(ge=1, le=5)
    
    # Written Review
    title: str
    review_text: str
    pros: List[str] = []
    cons: List[str] = []
    
    # Metadata
    would_recommend: bool = True
    is_verified: bool = True  # Only guests who completed bookings can review
    is_public: bool = True
    
    # Moderation
    is_flagged: bool = False
    moderation_notes: Optional[str] = None
    
    # Vendor Response
    vendor_response: Optional[str] = None
    vendor_response_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VendorPayout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vendor_id: str
    
    # Payout Details
    total_amount: float
    booking_ids: List[str] = []  # Bookings included in this payout
    payout_period_start: datetime
    payout_period_end: datetime
    
    # Banking Info
    bank_account_id: str
    payout_method: str = "bank_transfer"  # bank_transfer, paypal, etc.
    
    # Status
    status: str = "pending"  # pending, processing, completed, failed
    initiated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # External References
    stripe_transfer_id: Optional[str] = None
    reference_number: str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())

# Request/Response Models

class VendorApplicationRequest(BaseModel):
    legal_name: str
    phone_number: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    kitchen_description: str
    dining_capacity: int = Field(ge=2, le=20)
    cuisine_specialties: List[str] = []
    dietary_accommodations: List[str] = []
    background_check_consent: bool = True
    has_food_handling_experience: bool = False
    years_cooking_experience: int = 0
    has_liability_insurance: bool = False
    emergency_contact_name: str
    emergency_contact_phone: str
    terms_accepted: bool = True
    privacy_policy_accepted: bool = True

class BookingRequest(BaseModel):
    restaurant_id: str
    booking_date: str  # ISO format
    number_of_guests: int = Field(ge=1, le=20)
    menu_offering_id: str
    dietary_restrictions: List[str] = []
    special_requests: str = ""
    guest_message: str = ""

class ReviewRequest(BaseModel):
    overall_rating: int = Field(ge=1, le=5)
    food_quality_rating: int = Field(ge=1, le=5)
    hospitality_rating: int = Field(ge=1, le=5)
    cleanliness_rating: int = Field(ge=1, le=5)
    value_rating: int = Field(ge=1, le=5)
    title: str
    review_text: str
    pros: List[str] = []
    cons: List[str] = []
    would_recommend: bool = True

class VendorApplicationResponse(BaseModel):
    id: str
    status: VendorStatus
    application_date: datetime
    documents_required: List[str]
    next_steps: str
    estimated_review_time: str = "3-5 business days"

class HomeRestaurantResponse(BaseModel):
    id: str
    restaurant_name: str
    description: str
    cuisine_type: List[str]
    dining_capacity: int
    address: str
    photos: List[Dict[str, str]]
    base_price_per_person: float
    average_rating: float
    total_reviews: int
    is_accepting_bookings: bool
    operating_days: List[str]
    advance_booking_days: int

class BookingResponse(BaseModel):
    id: str
    booking_date: datetime
    number_of_guests: int
    total_amount: float
    status: BookingStatus
    restaurant_name: str
    vendor_name: str
    payment_status: PaymentStatus
    confirmation_code: str

class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: float
    booking_id: str