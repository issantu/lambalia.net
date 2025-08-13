# Local Farm Ecosystem Models - Phase 4: Community Rooting
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid

class FarmVendorType(str, Enum):
    LOCAL_FARM = "local_farm"
    BACKYARD_GARDENER = "backyard_gardener"     # Home gardeners with excess produce
    ORGANIC_GROWER = "organic_grower" 
    HOBBY_FARMER = "hobby_farmer"               # Small-scale enthusiasts
    LIVESTOCK_RANCH = "livestock_ranch"
    SPECIALTY_PRODUCER = "specialty_producer"   # honey, cheese, herbs, etc.
    COMMUNITY_GARDEN = "community_garden"       # Community garden participants
    URBAN_FARMER = "urban_farmer"               # Urban farming specialists
    FARMERS_MARKET = "farmers_market"

class ProductCategory(str, Enum):
    FRESH_VEGETABLES = "fresh_vegetables"
    ORGANIC_PRODUCE = "organic_produce"
    FRUITS = "fruits"
    HERBS_SPICES = "herbs_spices"
    MICROGREENS = "microgreens"                # For small-scale growers
    LEAFY_GREENS = "leafy_greens"             # Lettuce, spinach, kale
    TOMATOES = "tomatoes"                      # Popular backyard crop
    PEPPERS = "peppers"                        # Hot and sweet varieties
    CUCUMBERS = "cucumbers"                    # Easy garden crop
    SQUASH_ZUCCHINI = "squash_zucchini"       # High-yield crops
    BERRIES = "berries"                        # Strawberries, raspberries
    DAIRY_PRODUCTS = "dairy_products"
    FRESH_MEAT = "fresh_meat"
    POULTRY = "poultry"
    EGGS = "eggs"
    HONEY = "honey"
    GRAINS = "grains"
    NUTS = "nuts"
    PRESERVED_FOODS = "preserved_foods"        # Jams, pickles, canned goods
    BAKED_GOODS = "baked_goods"               # Using garden ingredients
    STARTER_PLANTS = "starter_plants"          # Seedlings and plants
    SEEDS = "seeds"                           # Heirloom and specialty seeds
    SPECIALTY_ITEMS = "specialty_items"

class ProductAvailability(str, Enum):
    YEAR_ROUND = "year_round"
    SEASONAL = "seasonal"
    LIMITED_HARVEST = "limited_harvest"
    PRE_ORDER_ONLY = "pre_order_only"

class CertificationType(str, Enum):
    USDA_ORGANIC = "usda_organic"
    NON_GMO = "non_gmo"
    GRASS_FED = "grass_fed"
    FREE_RANGE = "free_range"
    PASTURE_RAISED = "pasture_raised"
    SUSTAINABLE = "sustainable"
    LOCAL_GROWN = "local_grown"
    BIODYNAMIC = "biodynamic"

class FarmDiningVenueType(str, Enum):
    OUTDOOR_DINING = "outdoor_dining"
    BARN_DINING = "barn_dining"
    GREENHOUSE_DINING = "greenhouse_dining"
    ORCHARD_PICNIC = "orchard_picnic"
    VINEYARD_DINING = "vineyard_dining"
    GARDEN_DINING = "garden_dining"

class FarmVendorApplication(BaseModel):
    """Application for local farmers/growers to become vendors"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    vendor_type: FarmVendorType = FarmVendorType.LOCAL_FARM
    
    # Farm/Business Information
    farm_name: str = Field(..., min_length=2, max_length=100)
    business_name: str = Field(..., min_length=2, max_length=100)
    farm_description: str = Field(..., min_length=50, max_length=1000)
    established_year: int = Field(..., ge=1990, le=2025)   # Updated for hobbyists
    
    # Growing Experience Level
    growing_experience_level: str = "hobbyist"  # "hobbyist", "experienced", "professional"
    primary_motivation: str = "share_excess"    # "share_excess", "supplement_income", "build_community"
    
    # Contact & Location
    legal_name: str
    phone_number: str
    email: str
    farm_address: str
    city: str
    state: str
    postal_code: str
    country: str = "US"
    
    # Farm Specifications
    total_acres: float = Field(..., ge=0.01, le=10000.0)  # Allow smaller plots (0.01 acres = ~436 sq ft)
    growing_area_type: str = "backyard"  # "backyard", "community_plot", "rooftop", "greenhouse", "farm_field"
    farming_methods: List[str] = []  # ["organic", "sustainable", "conventional", "permaculture", "hydroponic"]
    primary_products: List[ProductCategory] = []
    
    # Certifications
    certifications: List[CertificationType] = []
    certifying_bodies: List[str] = []  # ["USDA", "Oregon Tilth", etc.]
    certification_numbers: Dict[str, str] = {}
    
    # Farm Operations
    growing_seasons: Dict[str, List[str]] = {}  # {"spring": ["lettuce", "peas"], "summer": ["tomatoes"]}
    harvest_calendar: Dict[str, Dict[str, str]] = {}  # {"tomatoes": {"start": "July", "end": "September"}}
    distribution_radius_km: float = Field(default=50.0, le=200.0)
    
    # Facilities & Services
    has_storage_facilities: bool = False
    has_processing_facilities: bool = False
    offers_farm_tours: bool = False
    offers_u_pick: bool = False
    has_farm_stand: bool = False
    
    # Dining Venue (optional)
    offers_farm_dining: bool = False
    dining_venue_types: List[FarmDiningVenueType] = []
    max_dining_capacity: Optional[int] = Field(None, ge=10, le=200)
    dining_seasons: List[str] = []  # ["spring", "summer", "fall"]
    
    # Verification Documents
    documents: List[Dict[str, str]] = []
    # {"type": "farm_photos", "urls": [...], "status": "pending"}
    # {"type": "certification_documents", "urls": [...], "status": "verified"}
    # {"type": "business_license", "urls": [...], "status": "pending"}
    
    # Business Details
    years_farming_experience: int = Field(default=0, ge=0)
    has_business_insurance: bool = False
    has_food_handler_license: bool = False  # For direct sales
    tax_id_number: Optional[str] = None
    
    # Application Status
    status: str = "pending"  # pending, under_review, approved, rejected
    application_date: datetime = Field(default_factory=datetime.utcnow)
    review_notes: Optional[str] = None
    reviewer_id: Optional[str] = None
    approval_date: Optional[datetime] = None
    
    # Terms & Compliance
    terms_accepted: bool = False
    food_safety_training: bool = False
    commission_rate_accepted: float = 0.15  # 15% platform fee for farm products
    dining_commission_rate: float = 0.15    # 15% for farm dining experiences

class FarmProfile(BaseModel):
    """Approved farm vendor profile"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vendor_id: str
    application_id: str
    
    # Farm Identity
    farm_name: str
    business_name: str
    description: str
    established_year: int
    vendor_type: FarmVendorType
    
    # Location & Contact
    location: Dict[str, Any] = Field(default_factory=lambda: {"type": "Point", "coordinates": [0.0, 0.0]})
    address: str
    city: str
    state: str
    postal_code: str
    phone_number: str
    website: Optional[str] = None
    
    # Farm Details
    total_acres: float
    farming_methods: List[str]
    certifications: List[CertificationType]
    certification_details: Dict[str, Dict[str, str]] = {}  # {"usda_organic": {"number": "12345", "expiry": "2025-12-31"}}
    
    # Products & Inventory
    product_catalog: List[Dict[str, Any]] = []
    # [{"name": "Organic Tomatoes", "category": "organic_produce", "unit": "lb", "price_per_unit": 4.50, "availability": "seasonal"}]
    
    seasonal_availability: Dict[str, List[str]] = {}  # {"summer": ["tomatoes", "corn"], "fall": ["apples"]}
    
    # Media & Marketing
    farm_photos: List[Dict[str, str]] = []  # [{"type": "main", "url": "...", "caption": "Our organic tomato fields"}]
    story: str = ""  # Farm's story and mission
    sustainability_practices: List[str] = []
    
    # Distribution & Services
    distribution_radius_km: float
    delivery_available: bool = True
    pickup_available: bool = True
    ships_products: bool = False
    minimum_order_amount: float = Field(default=25.0, ge=10.0)
    
    # Farm Experiences
    offers_farm_tours: bool = False
    tour_price_per_person: Optional[float] = None
    offers_u_pick: bool = False
    u_pick_seasons: List[str] = []
    
    # Performance Metrics
    average_rating: float = 0.0
    total_reviews: int = 0
    total_orders: int = 0
    reliability_score: float = 100.0  # Percentage of orders fulfilled on time
    
    # Status & Activity
    is_active: bool = True
    is_accepting_orders: bool = True
    last_harvest_update: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FarmDiningVenue(BaseModel):
    """Farm dining venue for outdoor/farm-to-table experiences"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    farm_id: str
    vendor_id: str
    
    # Venue Details
    venue_name: str
    venue_type: FarmDiningVenueType
    description: str
    
    # Capacity & Setup
    max_capacity: int = Field(..., ge=10, le=200)
    table_configurations: List[Dict[str, Any]] = []  # [{"type": "family_style", "seats": 8, "count": 5}]
    
    # Seasonal Operation
    operating_seasons: List[str] = []  # ["spring", "summer", "fall"]
    seasonal_hours: Dict[str, Dict[str, str]] = {}  # {"summer": {"start": "17:00", "end": "21:00"}}
    
    # Amenities & Features
    amenities: List[str] = []  # ["outdoor_heaters", "covered_area", "restrooms", "parking", "live_music"]
    weather_contingency: str = ""  # Plans for rain/bad weather
    
    # Farm-to-Table Experience
    featured_ingredients: List[str] = []  # Ingredients grown on the farm
    seasonal_menus: Dict[str, List[Dict[str, Any]]] = {}
    # {"summer": [{"dish": "Heirloom Tomato Salad", "ingredients_from_farm": ["tomatoes", "basil"], "price": 18}]}
    
    # Booking & Pricing
    base_price_per_person: float = Field(..., ge=25.0, le=150.0)
    includes_farm_tour: bool = False
    advance_booking_days: int = Field(default=7, ge=3, le=30)
    
    # Photos & Media
    venue_photos: List[Dict[str, str]] = []
    virtual_tour_url: Optional[str] = None
    
    # Status
    is_active: bool = True
    is_accepting_bookings: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FarmProduct(BaseModel):
    """Individual farm product listing"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    farm_id: str
    vendor_id: str
    
    # Product Details
    product_name: str
    category: ProductCategory
    variety: Optional[str] = None  # "Heirloom", "Cherry", etc.
    description: str
    
    # Pricing & Units
    unit_type: str = "lb"  # "lb", "bunch", "dozen", "each", "pint", "gallon"
    price_per_unit: float = Field(..., ge=0.50, le=100.0)
    minimum_order_quantity: int = Field(default=1, ge=1)
    bulk_pricing: List[Dict[str, float]] = []  # [{"quantity": 10, "price_per_unit": 4.00}]
    
    # Availability
    availability_type: ProductAvailability
    seasonal_months: List[str] = []  # ["June", "July", "August"] for seasonal items
    estimated_harvest_date: Optional[datetime] = None
    quantity_available: Optional[int] = None  # Current stock
    
    # Quality & Certifications
    certifications: List[CertificationType] = []
    growing_method: str = "organic"  # "organic", "conventional", "biodynamic"
    harvest_method: str = "hand_picked"  # "hand_picked", "machine_harvested"
    storage_method: str = ""  # Storage and handling information
    
    # Nutrition & Details
    nutritional_info: Optional[Dict[str, str]] = None
    allergen_info: List[str] = []
    shelf_life_days: Optional[int] = None
    
    # Photos & Media
    product_photos: List[str] = []
    
    # Performance
    total_orders: int = 0
    average_rating: float = 0.0
    total_reviews: int = 0
    
    # Status
    is_active: bool = True
    is_available: bool = True
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FarmProductOrder(BaseModel):
    """Order for farm products"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    farm_id: str
    vendor_id: str
    
    # Order Items
    items: List[Dict[str, Any]] = []
    # [{"product_id": "...", "product_name": "...", "quantity": 5, "unit_price": 4.50, "total_price": 22.50}]
    
    # Pricing
    subtotal: float
    platform_commission: float  # 10% of subtotal
    delivery_fee: float = 0.0
    total_amount: float
    farmer_payout: float
    
    # Delivery Details
    delivery_method: str = "pickup"  # "pickup", "delivery", "shipping"
    delivery_address: Optional[str] = None
    preferred_delivery_date: datetime
    delivery_time_window: Optional[str] = None  # "9AM-12PM"
    
    # Special Instructions
    customer_notes: str = ""
    handling_instructions: str = ""
    
    # Status & Timeline
    status: str = "pending"  # pending, confirmed, harvesting, ready, delivered, completed, cancelled
    order_date: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    # Payment
    payment_id: Optional[str] = None
    payment_status: str = "pending"

class FarmDiningBooking(BaseModel):
    """Booking for farm dining experiences"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    venue_id: str
    farm_id: str
    customer_id: str
    vendor_id: str
    
    # Booking Details
    dining_date: datetime
    number_of_guests: int = Field(..., ge=1, le=50)
    seating_preference: Optional[str] = None
    
    # Experience Options
    includes_farm_tour: bool = False
    special_dietary_requests: List[str] = []
    occasion: Optional[str] = None  # "birthday", "anniversary", "corporate"
    
    # Pricing
    price_per_person: float
    farm_tour_fee: float = 0.0
    total_amount: float
    platform_commission: float  # 15% for dining experiences
    farmer_payout: float
    
    # Customer Details
    customer_notes: str = ""
    contact_phone: str = ""
    
    # Status
    status: str = "pending"  # pending, confirmed, in_progress, completed, cancelled
    booking_date: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    
    # Payment
    payment_id: Optional[str] = None
    payment_status: str = "pending"
    confirmation_code: str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())

# Request/Response Models

class FarmVendorApplicationRequest(BaseModel):
    vendor_type: FarmVendorType = FarmVendorType.LOCAL_FARM
    farm_name: str = Field(..., min_length=2, max_length=100)
    business_name: str = Field(..., min_length=2, max_length=100)
    farm_description: str = Field(..., min_length=50, max_length=1000)
    established_year: int = Field(..., ge=1800, le=2025)
    legal_name: str
    phone_number: str
    email: str
    farm_address: str
    city: str
    state: str
    postal_code: str
    country: str = "US"
    total_acres: float = Field(..., ge=0.1, le=10000.0)
    farming_methods: List[str] = []
    primary_products: List[ProductCategory] = []
    certifications: List[CertificationType] = []
    distribution_radius_km: float = Field(default=50.0, le=200.0)
    offers_farm_dining: bool = False
    dining_venue_types: List[FarmDiningVenueType] = []
    max_dining_capacity: Optional[int] = Field(None, ge=10, le=200)
    years_farming_experience: int = Field(default=0, ge=0)
    has_business_insurance: bool = False
    has_food_handler_license: bool = False
    terms_accepted: bool = True
    food_safety_training: bool = False

class FarmProductRequest(BaseModel):
    product_name: str
    category: ProductCategory
    variety: Optional[str] = None
    description: str
    unit_type: str = "lb"
    price_per_unit: float = Field(..., ge=0.50, le=100.0)
    minimum_order_quantity: int = Field(default=1, ge=1)
    availability_type: ProductAvailability
    seasonal_months: List[str] = []
    quantity_available: Optional[int] = None
    certifications: List[CertificationType] = []
    growing_method: str = "organic"
    harvest_method: str = "hand_picked"
    shelf_life_days: Optional[int] = None
    product_photos: List[str] = []

class FarmProductOrderRequest(BaseModel):
    farm_id: str
    items: List[Dict[str, Any]] = []
    delivery_method: str = "pickup"
    delivery_address: Optional[str] = None
    preferred_delivery_date: str  # ISO format
    delivery_time_window: Optional[str] = None
    customer_notes: str = ""

class FarmDiningBookingRequest(BaseModel):
    venue_id: str
    dining_date: str  # ISO format
    number_of_guests: int = Field(..., ge=1, le=50)
    includes_farm_tour: bool = False
    special_dietary_requests: List[str] = []
    occasion: Optional[str] = None
    customer_notes: str = ""
    contact_phone: str = ""

class FarmProfileResponse(BaseModel):
    id: str
    farm_name: str
    business_name: str
    description: str
    vendor_type: str
    established_year: int
    total_acres: float
    certifications: List[str]
    farming_methods: List[str]
    distance_km: Optional[float] = None
    average_rating: float
    total_reviews: int
    product_count: int
    offers_farm_dining: bool
    is_accepting_orders: bool
    sustainability_practices: List[str]

class FarmProductResponse(BaseModel):
    id: str
    farm_name: str
    product_name: str
    category: str
    variety: Optional[str]
    description: str
    unit_type: str
    price_per_unit: float
    availability_type: str
    seasonal_months: List[str]
    certifications: List[str]
    growing_method: str
    quantity_available: Optional[int]
    average_rating: float
    is_available: bool
    distance_km: Optional[float] = None

class FarmDiningVenueResponse(BaseModel):
    id: str
    farm_name: str
    venue_name: str
    venue_type: str
    description: str
    max_capacity: int
    base_price_per_person: float
    includes_farm_tour: bool
    operating_seasons: List[str]
    amenities: List[str]
    featured_ingredients: List[str]
    average_rating: float
    is_accepting_bookings: bool
    distance_km: Optional[float] = None