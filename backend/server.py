from fastapi import FastAPI, APIRouter, HTTPException, Depends, File, UploadFile, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
import base64
from enum import Enum
import math
import json
import asyncio

# Import existing models and new marketplace models
from models_extension import (
    ReferenceRecipe, RecipeSnippet, GroceryStore, IngredientAvailability,
    UserGroceryPreference, SnippetCreate, SnippetResponse, GrocerySearchRequest,
    GrocerySearchResponse, SnippetType, VideoQuality
)
from expanded_reference_recipes import (
    COMPREHENSIVE_REFERENCE_RECIPES, NATIVE_RECIPES_BY_COUNTRY,
    get_recipes_by_country, get_featured_recipes, get_recipe_by_name,
    get_all_countries_with_recipes, get_recipes_by_category, search_recipes,
    get_native_recipes_json
)
from marketplace_models import (
    VendorApplication, HomeRestaurant, TraditionalRestaurantProfile, MenuOffering, 
    SpecialOrder, Booking, Payment, Review, VendorPayout, VendorApplicationRequest, 
    BookingRequest, ReviewRequest, SpecialOrderRequest, TraditionalRestaurantRequest,
    VendorApplicationResponse, HomeRestaurantResponse, TraditionalRestaurantResponse,
    SpecialOrderResponse, BookingResponse, PaymentIntentResponse, VendorStatus, 
    VendorType, BookingStatus, OrderStatus, PaymentStatus, DocumentType
)
from payment_service import payment_service, pricing_engine
from translation_service import get_translation_service
from daily_marketplace_service import DailyMarketplaceService
from marketplace_daily_models import (
    CookingOfferRequest, EatingRequestRequest, AppointmentRequest,
    CookingOfferResponse, EatingRequestResponse, AppointmentResponse,
    MealCategory, CookingOfferStatus, EatingRequestStatus
)
from ad_monetization_service import (
    AdPlacementService, PremiumMembershipService, SurgePricingService, 
    RevenueAnalyticsService, EngagementAnalysisService
)
from ad_monetization_models import (
    AdCreationRequest, PremiumUpgradeRequest, AdPlacementResponse,
    RevenueReportResponse, PremiumTier, AdPlacement, AdType
)
from farm_ecosystem_service import FarmEcosystemService, LocalFarmMatchingService
from farm_ecosystem_models import (
    FarmVendorApplicationRequest, FarmProductRequest, FarmProductOrderRequest,
    FarmDiningBookingRequest, FarmProfileResponse, FarmProductResponse,
    FarmDiningVenueResponse, ProductCategory, CertificationType, FarmVendorType
)
from charity_program_service import CharityProgramService, CharityImpactCalculator
from charity_program_models import (
    CharityProgramRegistrationRequest, CharityActivitySubmissionRequest,
    PremiumMembershipUpgradeRequest, CharityActivityResponse, CommunityImpactResponse,
    PremiumBenefitsResponse, CharityType, VerificationStatus, PremiumTier
)
from lambalia_eats_service import LambaliaEatsService
from lambalia_eats_api import create_lambalia_eats_router
from heritage_recipes_service import HeritageRecipesService
from heritage_recipes_api import create_heritage_recipes_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Lambalia Marketplace API", description="Complete Home Restaurant Marketplace with Vetting & Payments")
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(days=7)

# Existing models (keeping all from previous implementation)
class DietaryPreference(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    KETO = "keto"
    PALEO = "paleo"
    ORGANIC = "organic"

class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"

class RecipeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Country(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str
    regions: List[Dict[str, str]] = []
    languages: List[str] = []
    native_recipes: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    password_hash: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_photo: Optional[str] = None
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    postal_code: Optional[str] = None
    preferred_language: str = "en"
    dietary_preferences: List[DietaryPreference] = []
    followers_count: int = 0
    following_count: int = 0
    recipes_count: int = 0
    snippets_count: int = 0
    credits: float = 0.0
    
    # Cultural heritage and consultation fields
    native_dishes: Optional[str] = None
    consultation_specialties: Optional[str] = None
    cultural_background: Optional[str] = None
    
    # New marketplace fields
    is_vendor: bool = False
    vendor_application_id: Optional[str] = None
    stripe_account_id: Optional[str] = None
    total_earnings: float = 0.0
    
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Request models
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    country_id: Optional[str] = None
    postal_code: Optional[str] = None
    preferred_language: str = "en"
    native_dishes: Optional[str] = None
    consultation_specialties: Optional[str] = None
    cultural_background: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_photo: Optional[str] = None
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    postal_code: Optional[str] = None
    preferred_language: str
    followers_count: int
    following_count: int
    recipes_count: int
    snippets_count: int
    credits: float
    is_vendor: bool
    total_earnings: float
    is_verified: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Utility functions (keeping existing ones)
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + JWT_EXPIRATION_DELTA
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> Optional[str]:
    """Optional authentication - returns user_id if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        
        user = await db.users.find_one({"id": user_id})
        if not user:
            return None
        
        return user_id
    except (jwt.ExpiredSignatureError, jwt.JWTError):
        return None

# Authentication Routes (keeping existing ones)
@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "lambalia-api", "timestamp": datetime.utcnow()}

@api_router.get("/countries")
async def get_countries():
    """Get all countries with native recipes"""
    return get_all_countries_with_recipes()

@api_router.get("/users/me")
async def get_current_user_profile(current_user_id: str = Depends(get_current_user)):
    """Get current user profile"""
    user = await db.users.find_one({"id": current_user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user)

@api_router.post("/auth/register", response_model=TokenResponse)
async def register_user(user_data: UserRegistration):
    existing_user = await db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_dict = user_data.dict()
    user_dict['password_hash'] = hash_password(user_data.password)
    del user_dict['password']
    
    user = UserProfile(**user_dict)
    await db.users.insert_one(user.dict())
    
    token = create_jwt_token(user.id)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user.dict())
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin):
    user_doc = await db.users.find_one({"email": login_data.email})
    if not user_doc or not verify_password(login_data.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token(user_doc['id'])
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user_doc)
    )

# CULTURAL HERITAGE DATA COLLECTION
# EXTERNAL AD REVENUE & AFFILIATE MARKETING
@api_router.get("/ads/external-placements")
async def get_external_ad_placements():
    """Get external ad placements for additional revenue"""
    
    # External ad network integrations
    ad_placements = {
        "google_adsense": {
            "enabled": True,
            "revenue_share": 68,  # Google AdSense revenue share
            "ad_units": [
                {
                    "placement": "recipe_header",
                    "size": "728x90",
                    "estimated_cpm": "$2.50",
                    "category": "food_cooking"
                },
                {
                    "placement": "sidebar_recipes", 
                    "size": "300x250",
                    "estimated_cpm": "$1.80",
                    "category": "specialty_ingredients"
                },
                {
                    "placement": "mobile_banner",
                    "size": "320x50", 
                    "estimated_cpm": "$1.20",
                    "category": "cultural_food"
                }
            ]
        },
        "facebook_audience_network": {
            "enabled": True,
            "revenue_share": 65,
            "targeting": ["cultural_food", "cooking", "recipes", "ethnic_ingredients"],
            "estimated_monthly_revenue": "$1200-3500"
        },
        "amazon_affiliates": {
            "enabled": True,
            "commission_rate": "4-8%",
            "categories": ["kitchen_equipment", "cookbooks", "ingredients", "spices"],
            "estimated_monthly_revenue": "$800-2200"
        }
    }
    
    # Calculate projected revenue
    daily_page_views = 5000  # Conservative estimate
    monthly_page_views = daily_page_views * 30
    
    projected_revenue = {
        "google_adsense_monthly": monthly_page_views * 0.002 * 2.0,  # $2 CPM
        "facebook_network_monthly": monthly_page_views * 0.0015 * 1.5,  # $1.50 CPM  
        "amazon_affiliate_monthly": 500,  # Conservative affiliate estimate
        "total_external_ads_monthly": 0
    }
    projected_revenue["total_external_ads_monthly"] = (
        projected_revenue["google_adsense_monthly"] + 
        projected_revenue["facebook_network_monthly"] + 
        projected_revenue["amazon_affiliate_monthly"]
    )
    
    return {
        "ad_placements": ad_placements,
        "projected_revenue": projected_revenue,
        "implementation_status": "ready_for_integration",
        "estimated_setup_time": "2-3 days"
    }

@api_router.get("/revenue/affiliate-opportunities")
async def get_affiliate_opportunities():
    """Identify affiliate marketing opportunities based on platform data"""
    
    # Analyze platform usage to identify affiliate opportunities
    affiliate_programs = {
        "kitchen_equipment": {
            "partners": ["Williams Sonoma", "Sur La Table", "Amazon", "Target"],
            "commission_rates": "3-8%",
            "integration_type": "contextual_product_placement",
            "estimated_conversion": "2-4%",
            "monthly_potential": "$800-1500"
        },
        "specialty_ingredients": {
            "partners": ["H-Mart Online", "Patel Brothers", "iGourmet", "Spice Jungle"],
            "commission_rates": "5-12%", 
            "integration_type": "ingredient_shopping_links",
            "estimated_conversion": "5-8%",
            "monthly_potential": "$1200-2500"
        },
        "cultural_cookbooks": {
            "partners": ["Amazon Books", "Barnes & Noble", "Book Depository"],
            "commission_rates": "4-10%",
            "integration_type": "recipe_related_books",
            "estimated_conversion": "3-6%",
            "monthly_potential": "$400-800"
        },
        "cooking_classes": {
            "partners": ["MasterClass", "Udemy", "Skillshare"],
            "commission_rates": "20-50%",
            "integration_type": "skill_building_recommendations", 
            "estimated_conversion": "1-3%",
            "monthly_potential": "$600-1200"
        }
    }
    
    return {
        "total_affiliate_programs": len(affiliate_programs),
        "programs": affiliate_programs,
        "total_monthly_potential": "$3000-6000",
        "implementation_priority": "high_roi_quick_setup"
    }

@api_router.get("/revenue/data-monetization")
async def get_data_monetization_opportunities():
    """Analyze data monetization opportunities"""
    
    # Cultural food trend data has significant commercial value
    data_products = {
        "cultural_food_trends": {
            "buyers": ["Food brands", "Grocery chains", "Market research firms"],
            "data_type": "Anonymized cultural food preferences and trends",
            "pricing": "$500-2000/month per client",
            "potential_clients": 15,
            "compliance": "GDPR and privacy compliant"
        },
        "ingredient_demand_analytics": {
            "buyers": ["Specialty grocery stores", "Import/export companies"],
            "data_type": "Regional ingredient demand and availability gaps",
            "pricing": "$300-800/month per client", 
            "potential_clients": 25,
            "value_proposition": "Inventory optimization for ethnic stores"
        },
        "diaspora_community_insights": {
            "buyers": ["Marketing agencies", "Cultural organizations", "Government agencies"],
            "data_type": "Cultural food consumption patterns and community needs",
            "pricing": "$800-1500/month per client",
            "potential_clients": 10,
            "use_cases": "Cultural program development, marketing strategies"
        }
    }
    
    total_potential = sum([
        product["pricing"].split("-")[1].replace("$", "").replace("/month per client", "") 
        for product in data_products.values()
    ])
    
    return {
        "data_products": data_products,
        "total_monthly_potential": "$15000-65000",
        "implementation_complexity": "medium",
        "privacy_compliance": "fully_anonymized_aggregate_data_only"
    }

@api_router.post("/revenue/white-label-licensing")
async def create_white_label_opportunity(licensing_request: Dict[str, Any]):
    """White-label licensing opportunities for grocery chains"""
    
    white_label_opportunities = {
        "grocery_chain_integration": {
            "target_clients": ["H-Mart", "Patel Brothers", "99 Ranch Market", "Wegmans"],
            "offering": "Branded cultural recipe platform for store websites",
            "pricing": "$2000-5000/month + setup fee",
            "value_proposition": "Increase customer engagement and cultural authenticity",
            "implementation": "4-6 weeks custom branding"
        },
        "restaurant_group_licensing": {
            "target_clients": ["Multi-location ethnic restaurants", "Hotel chains"],
            "offering": "Heritage recipe management and cultural menu optimization",
            "pricing": "$1000-3000/month per location group",
            "features": ["Cultural authenticity verification", "Seasonal menu optimization"]
        },
        "corporate_cultural_programs": {
            "target_clients": ["Tech companies", "Universities", "Healthcare systems"],
            "offering": "Employee cultural food programs and diversity initiatives",
            "pricing": "$500-1500/month per organization",
            "use_case": "Cultural diversity through authentic food experiences"
        }
    }
    
    return {
        "white_label_opportunities": white_label_opportunities,
        "total_potential_clients": 50,
        "estimated_monthly_recurring": "$25000-75000",
        "sales_cycle": "3-6 months",
        "profit_margin": "70-85%"
    }

@api_router.get("/heritage/dishes-by-culture/{cultural_background}")
async def get_dishes_by_culture(cultural_background: str):
    """Get native dishes from users of a specific cultural background"""
    
    users = await db.users.find({
        "cultural_background": {"$regex": cultural_background, "$options": "i"},
        "native_dishes": {"$exists": True, "$ne": ""}
    }, {"_id": 0, "native_dishes": 1, "username": 1, "consultation_specialties": 1}).to_list(length=100)
    
    dishes_data = []
    for user in users:
        if user.get('native_dishes'):
            dishes = [d.strip() for d in user['native_dishes'].split(',')]
            for dish in dishes:
                dishes_data.append({
                    "dish_name": dish,
                    "contributor": user['username'],
                    "consultation_available": bool(user.get('consultation_specialties')),
                    "specialties": user.get('consultation_specialties', '')
                })
    
    return {
        "cultural_background": cultural_background,
        "total_contributors": len(users),
        "dishes": dishes_data[:50],  # Limit to 50 for performance
        "total_dishes": len(dishes_data)
    }


# MARKETPLACE ROUTES - NEW VETTING AND PAYMENT SYSTEM

@api_router.post("/vendor/apply", response_model=VendorApplicationResponse)
async def submit_vendor_application(
    application_data: VendorApplicationRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Submit vendor application for home restaurant"""
    
    # Check if user already has an application
    existing_app = await db.vendor_applications.find_one({"user_id": current_user_id})
    if existing_app and existing_app['status'] in ['pending', 'under_review', 'approved']:
        raise HTTPException(status_code=400, detail="Application already exists")
    
    # Create application
    app_dict = application_data.dict()
    app_dict['user_id'] = current_user_id
    
    application = VendorApplication(**app_dict)
    await db.vendor_applications.insert_one(application.dict())
    
    # Update user status
    await db.users.update_one(
        {"id": current_user_id},
        {"$set": {"vendor_application_id": application.id}}
    )
    
    return VendorApplicationResponse(
        id=application.id,
        status=application.status,
        vendor_type=application.vendor_type,
        application_date=application.application_date,
        documents_required=[
            "Kitchen Photo", "Dining Room Photo", "Front Door Photo",
            "Government ID", "Health Certificate (if required)", "Insurance Proof"
        ] if application.vendor_type == VendorType.HOME_RESTAURANT else [
            "Restaurant Photos", "Business License", "Government ID",
            "Health Certificate", "Insurance Proof", "Menu Photos"
        ],
        next_steps="Upload required documents and wait for review"
    )

@api_router.post("/vendor/documents/upload/{application_id}")
async def upload_vendor_document(
    application_id: str,
    document_type: DocumentType,
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_user)
):
    """Upload verification documents for vendor application"""
    
    # Verify application ownership
    application = await db.vendor_applications.find_one({
        "id": application_id,
        "user_id": current_user_id
    })
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # In production, upload to AWS S3, Google Cloud Storage, etc.
    # For now, we'll simulate with base64 encoding
    contents = await file.read()
    file_base64 = base64.b64encode(contents).decode()
    
    # Mock file URL (in production, this would be the actual cloud storage URL)
    file_url = f"https://lambalia-storage.s3.amazonaws.com/vendor-docs/{application_id}/{document_type.value}/{file.filename}"
    
    # Update application with document
    document_entry = {
        "type": document_type.value,
        "url": file_url,
        "filename": file.filename,
        "uploaded_at": datetime.utcnow(),
        "status": "pending_review"
    }
    
    await db.vendor_applications.update_one(
        {"id": application_id},
        {
            "$push": {"documents": document_entry},
            "$set": {"status": VendorStatus.UNDER_REVIEW}
        }
    )
    
    return {
        "message": "Document uploaded successfully",
        "document_type": document_type.value,
        "status": "uploaded"
    }

@api_router.get("/vendor/application/{application_id}")
async def get_vendor_application(
    application_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Get vendor application status"""
    
    application = await db.vendor_applications.find_one({
        "id": application_id,
        "user_id": current_user_id
    })
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return VendorApplication(**application)

@api_router.post("/admin/vendor/approve/{application_id}")
async def approve_vendor_application(
    application_id: str,
    approval_notes: str = "",
    current_user_id: str = Depends(get_current_user)
):
    """Admin endpoint to approve vendor application"""
    
    # TODO: Add admin role verification
    
    application = await db.vendor_applications.find_one({"id": application_id})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update application status
    await db.vendor_applications.update_one(
        {"id": application_id},
        {
            "$set": {
                "status": VendorStatus.APPROVED,
                "approval_date": datetime.utcnow(),
                "reviewer_id": current_user_id,
                "review_notes": approval_notes
            }
        }
    )
    
    # Update user to vendor status
    await db.users.update_one(
        {"id": application['user_id']},
        {"$set": {"is_vendor": True}}
    )
    
    # Create Stripe Express account for vendor
    user = await db.users.find_one({"id": application['user_id']})
    vendor_info = {
        'email': user['email'],
        'first_name': application.get('legal_name', '').split(' ')[0],
        'last_name': ' '.join(application.get('legal_name', '').split(' ')[1:]),
        'phone': application.get('phone_number'),
        'address': application.get('address'),
        'city': application.get('city'),
        'state': application.get('state'),
        'postal_code': application.get('postal_code'),
        'country': application.get('country', 'US')
    }
    
    try:
        stripe_account = await payment_service.create_vendor_account(vendor_info)
        await db.users.update_one(
            {"id": application['user_id']},
            {"$set": {"stripe_account_id": stripe_account['account_id']}}
        )
    except Exception as e:
        logging.error(f"Failed to create Stripe account: {e}")
    
    return {"message": "Vendor application approved", "status": "approved"}

@api_router.post("/vendor/restaurant/create")
async def create_home_restaurant(
    restaurant_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Create home restaurant profile after vendor approval"""
    
    # Verify user is approved vendor
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get('is_vendor'):
        raise HTTPException(status_code=403, detail="User is not an approved vendor")
    
    # Get approved application
    application = await db.vendor_applications.find_one({
        "user_id": current_user_id,
        "status": VendorStatus.APPROVED
    })
    if not application:
        raise HTTPException(status_code=404, detail="No approved vendor application found")
    
    # Create restaurant profile
    location_data = {"type": "Point", "coordinates": [restaurant_data.get('longitude', 0.0), restaurant_data.get('latitude', 0.0)]}
    
    restaurant = HomeRestaurant(
        vendor_id=current_user_id,
        application_id=application['id'],
        restaurant_name=restaurant_data['restaurant_name'],
        description=restaurant_data['description'],
        cuisine_type=restaurant_data.get('cuisine_type', []),
        dining_capacity=restaurant_data['dining_capacity'],
        address=application['address'],
        location=location_data,
        base_price_per_person=restaurant_data['base_price_per_person'],
        operating_days=restaurant_data.get('operating_days', []),
        operating_hours=restaurant_data.get('operating_hours', {}),
        photos=restaurant_data.get('photos', [])
    )
    
    await db.home_restaurants.insert_one(restaurant.dict())
    
    return HomeRestaurantResponse(**restaurant.dict())

@api_router.get("/restaurants", response_model=List[HomeRestaurantResponse])
async def get_home_restaurants(
    city: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = 25.0
):
    """Get available home restaurants with filtering"""
    
    query = {"is_active": True, "is_accepting_bookings": True}
    
    if city:
        query["address"] = {"$regex": city, "$options": "i"}
    
    if cuisine_type:
        query["cuisine_type"] = {"$in": [cuisine_type]}
    
    if max_price:
        query["base_price_per_person"] = {"$lte": max_price}
    
    if min_rating:
        query["average_rating"] = {"$gte": min_rating}
    
    # TODO: Add geospatial queries for latitude/longitude
    
    restaurants_cursor = db.home_restaurants.find(query).limit(50)
    restaurants = await restaurants_cursor.to_list(length=50)
    
    return [HomeRestaurantResponse(**restaurant) for restaurant in restaurants]

@api_router.post("/bookings/create", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create a new booking for home restaurant"""
    
    # Get restaurant details
    restaurant = await db.home_restaurants.find_one({"id": booking_data.restaurant_id})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Parse booking date
    booking_date = datetime.fromisoformat(booking_data.booking_date.replace('Z', '+00:00'))
    
    # Calculate dynamic pricing
    pricing = pricing_engine.calculate_dynamic_price(
        base_price=restaurant['base_price_per_person'],
        booking_date=booking_date,
        demand_level='medium',  # TODO: Calculate based on actual demand
        vendor_rating=restaurant['average_rating'],
        location_premium=1.0
    )
    
    total_amount = pricing['dynamic_price'] * booking_data.number_of_guests
    platform_commission = pricing['platform_commission'] * booking_data.number_of_guests
    vendor_payout = pricing['vendor_payout'] * booking_data.number_of_guests
    
    # Create payment intent
    payment_intent = await payment_service.create_payment_intent(
        booking_id=str(uuid.uuid4()),
        amount=total_amount,
        vendor_id=restaurant['vendor_id']
    )
    
    # Create booking
    booking = Booking(
        guest_id=current_user_id,
        restaurant_id=booking_data.restaurant_id,
        vendor_id=restaurant['vendor_id'],
        booking_date=booking_date,
        number_of_guests=booking_data.number_of_guests,
        menu_offering_id=booking_data.menu_offering_id,
        price_per_person=pricing['dynamic_price'],
        total_amount=total_amount,
        platform_commission=platform_commission,
        vendor_payout=vendor_payout,
        dietary_restrictions=booking_data.dietary_restrictions,
        special_requests=booking_data.special_requests,
        guest_message=booking_data.guest_message,
        payment_id=payment_intent['payment_intent_id']
    )
    
    await db.bookings.insert_one(booking.dict())
    
    # Create payment record
    payment_record = Payment(
        booking_id=booking.id,
        amount=total_amount,
        platform_commission=platform_commission,
        vendor_payout=vendor_payout,
        stripe_payment_intent_id=payment_intent['payment_intent_id']
    )
    
    await db.payments.insert_one(payment_record.dict())
    
    return BookingResponse(
        id=booking.id,
        booking_date=booking_date,
        number_of_guests=booking_data.number_of_guests,
        total_amount=total_amount,
        status=booking.status,
        restaurant_name=restaurant['restaurant_name'],
        vendor_name="Host",  # TODO: Get actual vendor name
        payment_status=booking.payment_status,
        confirmation_code=booking.id[:8].upper()
    )

@api_router.post("/payments/create-intent/{booking_id}", response_model=PaymentIntentResponse)
async def create_payment_intent_endpoint(
    booking_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Create payment intent for booking"""
    
    booking = await db.bookings.find_one({
        "id": booking_id,
        "guest_id": current_user_id
    })
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Create payment intent
    payment_intent = await payment_service.create_payment_intent(
        booking_id=booking_id,
        amount=booking['total_amount'],
        vendor_id=booking['vendor_id']
    )
    
    return PaymentIntentResponse(
        client_secret=payment_intent['client_secret'],
        payment_intent_id=payment_intent['payment_intent_id'],
        amount=payment_intent['amount'],
        booking_id=booking_id
    )

@api_router.post("/bookings/{booking_id}/review", response_model=Dict[str, str])
async def create_review(
    booking_id: str,
    review_data: ReviewRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create review after completed booking"""
    
    # Verify booking exists and is completed
    booking = await db.bookings.find_one({
        "id": booking_id,
        "guest_id": current_user_id,
        "status": BookingStatus.COMPLETED
    })
    if not booking:
        raise HTTPException(status_code=404, detail="Completed booking not found")
    
    # Check if review already exists
    existing_review = await db.reviews.find_one({"booking_id": booking_id})
    if existing_review:
        raise HTTPException(status_code=400, detail="Review already exists for this booking")
    
    # Create review
    review = Review(
        booking_id=booking_id,
        guest_id=current_user_id,
        restaurant_id=booking['restaurant_id'],
        vendor_id=booking['vendor_id'],
        **review_data.dict()
    )
    
    await db.reviews.insert_one(review.dict())
    
    # Update restaurant rating
    await update_restaurant_rating(booking['restaurant_id'])
    
    return {"message": "Review created successfully", "review_id": review.id}

async def update_restaurant_rating(restaurant_id: str):
    """Update restaurant average rating based on reviews"""
    
    # Calculate average ratings
    pipeline = [
        {"$match": {"restaurant_id": restaurant_id}},
        {"$group": {
            "_id": "$restaurant_id",
            "avg_overall": {"$avg": "$overall_rating"},
            "avg_food": {"$avg": "$food_quality_rating"},
            "avg_hospitality": {"$avg": "$hospitality_rating"},
            "avg_cleanliness": {"$avg": "$cleanliness_rating"},
            "avg_value": {"$avg": "$value_rating"},
            "total_reviews": {"$sum": 1}
        }}
    ]
    
    result = await db.reviews.aggregate(pipeline).to_list(1)
    
    if result:
        stats = result[0]
        await db.home_restaurants.update_one(
            {"id": restaurant_id},
            {
                "$set": {
                    "average_rating": round(stats['avg_overall'], 1),
                    "total_reviews": stats['total_reviews']
                }
            }
        )

# TRADITIONAL RESTAURANT ROUTES

@api_router.post("/vendor/traditional-restaurant/create", response_model=TraditionalRestaurantResponse)
async def create_traditional_restaurant(
    restaurant_data: TraditionalRestaurantRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create traditional restaurant profile after vendor approval"""
    
    # Verify user is approved vendor
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get('is_vendor'):
        raise HTTPException(status_code=403, detail="User is not an approved vendor")
    
    # Get approved application
    application = await db.vendor_applications.find_one({
        "user_id": current_user_id,
        "vendor_type": VendorType.TRADITIONAL_RESTAURANT,
        "status": VendorStatus.APPROVED
    })
    if not application:
        raise HTTPException(status_code=404, detail="No approved traditional restaurant application found")
    
    # Create restaurant profile
    location_data = {"type": "Point", "coordinates": [restaurant_data.longitude or 0.0, restaurant_data.latitude or 0.0]}
    
    restaurant = TraditionalRestaurantProfile(
        vendor_id=current_user_id,
        application_id=application['id'],
        address=application['address'],
        location=location_data,
        **restaurant_data.dict()
    )
    
    await db.traditional_restaurants.insert_one(restaurant.dict())
    
    return TraditionalRestaurantResponse(**restaurant.dict())

@api_router.get("/traditional-restaurants", response_model=List[TraditionalRestaurantResponse])
async def get_traditional_restaurants(
    city: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_delivery_distance: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    """Get available traditional restaurants with filtering"""
    
    query = {"is_active": True, "is_accepting_orders": True}
    
    if city:
        query["address"] = {"$regex": city, "$options": "i"}
    
    if cuisine_type:
        query["cuisine_type"] = {"$in": [cuisine_type]}
    
    if min_rating:
        query["average_rating"] = {"$gte": min_rating}
    
    # TODO: Add geospatial queries for latitude/longitude and delivery distance
    
    restaurants_cursor = db.traditional_restaurants.find(query).limit(50)
    restaurants = await restaurants_cursor.to_list(length=50)
    
    return [TraditionalRestaurantResponse(**restaurant) for restaurant in restaurants]

@api_router.post("/special-orders/create", response_model=SpecialOrderResponse)
async def create_special_order(
    order_data: SpecialOrderRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create a special order proposal for traditional restaurant"""
    
    # Verify user is approved traditional restaurant vendor
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get('is_vendor'):
        raise HTTPException(status_code=403, detail="User is not an approved vendor")
    
    # Get traditional restaurant profile
    restaurant = await db.traditional_restaurants.find_one({"vendor_id": current_user_id})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Traditional restaurant profile not found")
    
    # Calculate platform pricing
    base_price = order_data.price_per_person
    platform_commission = base_price * 0.15  # 15% commission
    vendor_payout = base_price - platform_commission
    
    # Create special order
    order_dict = order_data.dict()
    order_dict['restaurant_id'] = restaurant['id']
    order_dict['vendor_id'] = current_user_id
    order_dict['platform_commission'] = platform_commission
    order_dict['vendor_payout_per_person'] = vendor_payout
    order_dict['status'] = OrderStatus.ACTIVE
    
    # Parse expires_at if provided
    if order_data.expires_at:
        order_dict['expires_at'] = datetime.fromisoformat(order_data.expires_at.replace('Z', '+00:00'))
    
    special_order = SpecialOrder(**order_dict)
    await db.special_orders.insert_one(special_order.dict())
    
    # Add restaurant name for response
    response_data = special_order.dict()
    response_data['restaurant_name'] = restaurant['restaurant_name']
    
    return SpecialOrderResponse(**response_data)

@api_router.get("/special-orders", response_model=List[SpecialOrderResponse])
async def get_special_orders(
    city: Optional[str] = None,
    cuisine_style: Optional[str] = None,
    occasion_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_people: Optional[int] = None,
    max_people: Optional[int] = None,
    delivery_available: Optional[bool] = None,
    pickup_available: Optional[bool] = None,
    vegetarian_options: Optional[bool] = None,
    vegan_options: Optional[bool] = None
):
    """Get available special orders with filtering"""
    
    query = {"status": OrderStatus.ACTIVE}
    
    if city:
        # Join with traditional restaurants to filter by city
        query["restaurant_id"] = {"$in": []}  # Will be populated by restaurant lookup
    
    if cuisine_style:
        query["cuisine_style"] = {"$regex": cuisine_style, "$options": "i"}
    
    if occasion_type:
        query["occasion_type"] = occasion_type
    
    if max_price:
        query["price_per_person"] = {"$lte": max_price}
    
    if min_people:
        query["maximum_people"] = {"$gte": min_people}
    
    if max_people:
        query["minimum_people"] = {"$lte": max_people}
    
    if delivery_available is not None:
        query["delivery_available"] = delivery_available
    
    if pickup_available is not None:
        query["pickup_available"] = pickup_available
    
    if vegetarian_options is not None:
        query["vegetarian_options"] = vegetarian_options
    
    if vegan_options is not None:
        query["vegan_options"] = vegan_options
    
    orders_cursor = db.special_orders.find(query).limit(50).sort("created_at", -1)
    orders = await orders_cursor.to_list(length=50)
    
    # Enrich with restaurant names
    for order in orders:
        restaurant = await db.traditional_restaurants.find_one({"id": order['restaurant_id']})
        order['restaurant_name'] = restaurant['restaurant_name'] if restaurant else "Unknown Restaurant"
    
    return [SpecialOrderResponse(**order) for order in orders]

@api_router.get("/special-orders/{order_id}", response_model=SpecialOrderResponse)
async def get_special_order(order_id: str):
    """Get detailed information about a special order"""
    
    order = await db.special_orders.find_one({"id": order_id, "status": OrderStatus.ACTIVE})
    if not order:
        raise HTTPException(status_code=404, detail="Special order not found")
    
    # Get restaurant info
    restaurant = await db.traditional_restaurants.find_one({"id": order['restaurant_id']})
    order['restaurant_name'] = restaurant['restaurant_name'] if restaurant else "Unknown Restaurant"
    
    # Increment views count
    await db.special_orders.update_one(
        {"id": order_id},
        {"$inc": {"views_count": 1}}
    )
    
    return SpecialOrderResponse(**order)

@api_router.post("/special-orders/{order_id}/book", response_model=BookingResponse)
async def book_special_order(
    order_id: str,
    booking_data: BookingRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Book a special order from traditional restaurant"""
    
    # Get special order details
    special_order = await db.special_orders.find_one({"id": order_id, "status": OrderStatus.ACTIVE})
    if not special_order:
        raise HTTPException(status_code=404, detail="Special order not found")
    
    # Get restaurant details
    restaurant = await db.traditional_restaurants.find_one({"id": special_order['restaurant_id']})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Validate number of guests
    if booking_data.number_of_guests < special_order['minimum_people'] or booking_data.number_of_guests > special_order['maximum_people']:
        raise HTTPException(
            status_code=400, 
            detail=f"Number of guests must be between {special_order['minimum_people']} and {special_order['maximum_people']}"
        )
    
    # Parse booking date
    booking_date = datetime.fromisoformat(booking_data.booking_date.replace('Z', '+00:00'))
    
    # Check if booking date is available
    if booking_date.strftime('%Y-%m-%d') not in special_order['available_dates']:
        raise HTTPException(status_code=400, detail="Selected date is not available for this special order")
    
    # Calculate pricing
    price_per_person = special_order['price_per_person']
    total_amount = price_per_person * booking_data.number_of_guests
    platform_commission = special_order['platform_commission'] * booking_data.number_of_guests
    vendor_payout = special_order['vendor_payout_per_person'] * booking_data.number_of_guests
    
    # Create payment intent
    payment_intent = await payment_service.create_payment_intent(
        booking_id=str(uuid.uuid4()),
        amount=total_amount,
        vendor_id=special_order['vendor_id']
    )
    
    # Create booking
    booking = Booking(
        guest_id=current_user_id,
        vendor_id=special_order['vendor_id'],
        booking_type="special_order",
        special_order_id=order_id,
        booking_date=booking_date,
        number_of_guests=booking_data.number_of_guests,
        service_type=booking_data.service_type,
        delivery_address=booking_data.delivery_address,
        price_per_person=price_per_person,
        total_amount=total_amount,
        platform_commission=platform_commission,
        vendor_payout=vendor_payout,
        dietary_restrictions=booking_data.dietary_restrictions,
        special_requests=booking_data.special_requests,
        guest_message=booking_data.guest_message,
        payment_id=payment_intent['payment_intent_id']
    )
    
    await db.bookings.insert_one(booking.dict())
    
    # Create payment record
    payment_record = Payment(
        booking_id=booking.id,
        amount=total_amount,
        platform_commission=platform_commission,
        vendor_payout=vendor_payout,
        stripe_payment_intent_id=payment_intent['payment_intent_id']
    )
    
    await db.payments.insert_one(payment_record.dict())
    
    # Update special order booking count
    await db.special_orders.update_one(
        {"id": order_id},
        {"$inc": {"total_bookings": 1}}
    )
    
    return BookingResponse(
        id=booking.id,
        booking_date=booking_date,
        number_of_guests=booking_data.number_of_guests,
        total_amount=total_amount,
        status=booking.status,
        restaurant_name=restaurant['restaurant_name'],
        vendor_name="Chef",  # TODO: Get actual vendor name
        payment_status=booking.payment_status,
        confirmation_code=booking.id[:8].upper()
    )

# DAILY MARKETPLACE ROUTES - Dynamic Offer & Demand System

# Initialize daily marketplace service
daily_marketplace = DailyMarketplaceService(db)

@api_router.post("/daily-marketplace/cooking-offers", response_model=dict)
async def create_cooking_offer(
    offer_data: CookingOfferRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create a daily cooking offer"""
    try:
        # Get user info for cook name/rating
        user = await db.users.find_one({"id": current_user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Parse cooking date
        offer_dict = offer_data.dict()
        offer_dict['cooking_date'] = datetime.fromisoformat(offer_data.cooking_date.replace('Z', '+00:00'))
        
        # Set location (simplified - in production would use geocoding)
        offer_dict['location'] = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]  # Default NYC coordinates
        }
        offer_dict['address'] = f"{offer_data.city}, {offer_data.country}"
        
        offer = await daily_marketplace.create_cooking_offer(offer_dict, current_user_id)
        
        return {
            "success": True,
            "offer_id": offer.id,
            "message": "Cooking offer created successfully",
            "expires_at": offer.expires_at.isoformat(),
            "cook_payout_per_serving": offer.cook_payout_per_serving
        }
        
    except Exception as e:
        logger.error(f"Failed to create cooking offer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/cooking-offers", response_model=List[dict])
async def get_local_cooking_offers(
    postal_code: str = "10001",
    country: str = "US",
    max_distance_km: float = 20.0,
    category: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    max_price: Optional[float] = None,
    is_vegetarian: Optional[bool] = None,
    is_vegan: Optional[bool] = None,
    is_gluten_free: Optional[bool] = None,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get local cooking offers based on location and preferences"""
    try:
        # Default location (NYC) - in production would get from user profile or geocoding
        user_location = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]
        }
        
        filters = {}
        if category:
            filters["category"] = category
        if cuisine_type:
            filters["cuisine_type"] = cuisine_type
        if max_price:
            filters["max_price"] = max_price
        if is_vegetarian:
            filters["is_vegetarian"] = is_vegetarian
        if is_vegan:
            filters["is_vegan"] = is_vegan
        if is_gluten_free:
            filters["is_gluten_free"] = is_gluten_free
        
        offers = await daily_marketplace.get_local_cooking_offers(
            user_location, postal_code, country, max_distance_km, filters
        )
        
        # Enrich with cook information
        enriched_offers = []
        for offer in offers:
            cook = await db.users.find_one({"id": offer["cook_id"]}, {"_id": 0})
            offer["cook_name"] = cook.get("full_name", "Chef") if cook else "Chef"
            offer["cook_rating"] = cook.get("rating", 0.0) if cook else 0.0
            enriched_offers.append(offer)
        
        return enriched_offers
        
    except Exception as e:
        logger.error(f"Failed to get cooking offers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/daily-marketplace/eating-requests", response_model=dict)
async def create_eating_request(
    request_data: EatingRequestRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create an eating request to find matching cooks"""
    try:
        # Get user info
        user = await db.users.find_one({"id": current_user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Parse preferred date if provided
        request_dict = request_data.dict()
        if request_data.preferred_date:
            request_dict['preferred_date'] = datetime.fromisoformat(request_data.preferred_date.replace('Z', '+00:00'))
        
        # Set location (simplified)
        request_dict['location'] = {
            "type": "Point", 
            "coordinates": [-73.935242, 40.730610]  # Default NYC coordinates
        }
        request_dict['address'] = f"{request_data.city}, {request_data.country}"
        
        eating_request = await daily_marketplace.create_eating_request(request_dict, current_user_id)
        
        return {
            "success": True,
            "request_id": eating_request.id,
            "message": "Eating request created successfully",
            "matches_found": eating_request.match_count,
            "expires_at": eating_request.expires_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to create eating request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/eating-requests", response_model=List[dict])
async def get_local_eating_requests(
    postal_code: str = "10001",
    country: str = "US",
    max_distance_km: float = 20.0,
    current_user_id: str = Depends(get_current_user)
):
    """Get local eating requests for cooks to see demand"""
    try:
        # Default location (NYC)
        user_location = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]
        }
        
        requests = await daily_marketplace.get_local_eating_requests(
            user_location, postal_code, country, max_distance_km
        )
        
        # Enrich with eater information
        enriched_requests = []
        for request in requests:
            eater = await db.users.find_one({"id": request["eater_id"]}, {"_id": 0})
            request["eater_name"] = eater.get("full_name", "Food Lover") if eater else "Food Lover"
            
            # Format service preferences for display
            preferences = []
            if request.get("pickup_preferred"):
                preferences.append("Pickup")
            if request.get("delivery_preferred"):
                preferences.append("Delivery")
            if request.get("dine_in_preferred"):
                preferences.append("Dine-in")
            request["service_preferences"] = preferences
            
            enriched_requests.append(request)
        
        return enriched_requests
        
    except Exception as e:
        logger.error(f"Failed to get eating requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/daily-marketplace/book-offer", response_model=dict)
async def book_cooking_offer(
    appointment_data: AppointmentRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Book a cooking offer directly"""
    try:
        # Parse scheduled date
        appointment_dict = appointment_data.dict()
        appointment_dict['scheduled_date'] = datetime.fromisoformat(appointment_data.scheduled_date.replace('Z', '+00:00'))
        
        appointment = await daily_marketplace.book_cooking_offer(appointment_dict, current_user_id)
        
        # Get cook and offer info for response
        offer = await db.cooking_offers.find_one({"id": appointment_data.offer_id}, {"_id": 0})
        cook = await db.users.find_one({"id": appointment.cook_id}, {"_id": 0})
        
        return {
            "success": True,
            "appointment_id": appointment.id,
            "confirmation_code": appointment.id[:8].upper(),
            "total_amount": appointment.total_amount,
            "cook_name": cook.get("full_name", "Chef") if cook else "Chef",
            "dish_name": offer.get("dish_name", "Delicious meal") if offer else "Delicious meal",
            "scheduled_date": appointment.scheduled_date.isoformat(),
            "message": "Cooking appointment booked successfully!"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to book cooking offer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/my-offers", response_model=List[dict])
async def get_my_cooking_offers(current_user_id: str = Depends(get_current_user)):
    """Get current user's cooking offers"""
    try:
        offers = await daily_marketplace.get_user_cooking_offers(current_user_id)
        return offers
    except Exception as e:
        logger.error(f"Failed to get user cooking offers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/my-requests", response_model=List[dict])
async def get_my_eating_requests(current_user_id: str = Depends(get_current_user)):
    """Get current user's eating requests"""
    try:
        requests = await daily_marketplace.get_user_eating_requests(current_user_id)
        return requests
    except Exception as e:
        logger.error(f"Failed to get user eating requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/my-appointments", response_model=List[dict])
async def get_my_appointments(current_user_id: str = Depends(get_current_user)):
    """Get current user's appointments (as cook or eater)"""
    try:
        appointments = await daily_marketplace.get_user_appointments(current_user_id)
        
        # Enrich with additional info
        enriched_appointments = []
        for appointment in appointments:
            # Get offer info
            offer = await db.cooking_offers.find_one({"id": appointment["offer_id"]}, {"_id": 0})
            if offer:
                appointment["offer_title"] = offer["title"]
                appointment["dish_name"] = offer["dish_name"]
            
            # Get cook and eater names
            cook = await db.users.find_one({"id": appointment["cook_id"]}, {"_id": 0})
            eater = await db.users.find_one({"id": appointment["eater_id"]}, {"_id": 0})
            
            appointment["cook_name"] = cook.get("full_name", "Chef") if cook else "Chef"
            appointment["eater_name"] = eater.get("full_name", "Food Lover") if eater else "Food Lover"
            appointment["confirmation_code"] = appointment["id"][:8].upper()
            
            enriched_appointments.append(appointment)
        
        return enriched_appointments
        
    except Exception as e:
        logger.error(f"Failed to get user appointments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daily-marketplace/categories", response_model=List[dict])
async def get_meal_categories():
    """Get available meal categories"""
    categories = [
        {"value": "quick_meals", "label": "Quick Meals", "icon": "⚡"},
        {"value": "family_dinner", "label": "Family Dinner", "icon": "👨‍👩‍👧‍👦"},
        {"value": "cultural_specialties", "label": "Cultural Specialties", "icon": "🌍"},
        {"value": "breakfast", "label": "Breakfast", "icon": "🌅"},
        {"value": "lunch", "label": "Lunch", "icon": "🥪"},
        {"value": "dinner", "label": "Dinner", "icon": "🍽️"},
        {"value": "brunch", "label": "Brunch", "icon": "🥐"},
        {"value": "desserts", "label": "Desserts", "icon": "🍰"},
        {"value": "july_4th", "label": "July 4th", "icon": "🇺🇸"},
        {"value": "cinco_de_mayo", "label": "Cinco de Mayo", "icon": "🇲🇽"},
        {"value": "thanksgiving", "label": "Thanksgiving", "icon": "🦃"},
        {"value": "christmas", "label": "Christmas", "icon": "🎄"},
        {"value": "new_year", "label": "New Year", "icon": "🎊"},
        {"value": "valentines_day", "label": "Valentine's Day", "icon": "💕"},
        {"value": "mothers_day", "label": "Mother's Day", "icon": "👩"},
        {"value": "fathers_day", "label": "Father's Day", "icon": "👨"},
        {"value": "easter", "label": "Easter", "icon": "🐰"},
        {"value": "halloween", "label": "Halloween", "icon": "🎃"},
        {"value": "diwali", "label": "Diwali", "icon": "🪔"},
        {"value": "chinese_new_year", "label": "Chinese New Year", "icon": "🐉"},
        {"value": "ramadan", "label": "Ramadan", "icon": "🌙"},
        {"value": "birthday", "label": "Birthday", "icon": "🎂"},
        {"value": "anniversary", "label": "Anniversary", "icon": "💒"},
        {"value": "comfort_food", "label": "Comfort Food", "icon": "🍲"},
        {"value": "healthy", "label": "Healthy", "icon": "🥗"},
        {"value": "vegan", "label": "Vegan", "icon": "🌱"},
        {"value": "vegetarian", "label": "Vegetarian", "icon": "🥕"}
    ]
    
    return categories

@api_router.get("/daily-marketplace/stats", response_model=dict)
async def get_daily_marketplace_stats():
    """Get daily marketplace statistics"""
    try:
        # Count active offers and requests
        active_offers = await db.cooking_offers.count_documents({"status": "active"})
        active_requests = await db.eating_requests.count_documents({"status": "active"})
        total_appointments = await db.cooking_appointments.count_documents({})
        completed_appointments = await db.cooking_appointments.count_documents({"status": "completed"})
        
        return {
            "active_cooking_offers": active_offers,
            "active_eating_requests": active_requests,
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "success_rate": round((completed_appointments / total_appointments * 100), 2) if total_appointments > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Failed to get marketplace stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# LOCAL FARM ECOSYSTEM ROUTES - Phase 4: Community Rooting

# Initialize farm ecosystem services
farm_ecosystem_service = FarmEcosystemService(db)
farm_matching_service = LocalFarmMatchingService(db)

# Initialize charity program service
charity_program_service = CharityProgramService(db)

# Initialize Lambalia Eats service
lambalia_eats_service = LambaliaEatsService(db)

# Initialize Heritage Recipes service
heritage_recipes_service = HeritageRecipesService(db)

@api_router.post("/farm-vendors/apply", response_model=dict)
async def apply_as_farm_vendor(
    application_data: FarmVendorApplicationRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Apply to become a farm vendor"""
    try:
        application = await farm_ecosystem_service.create_farm_vendor_application(
            application_data.dict(), current_user_id
        )
        
        return {
            "success": True,
            "application_id": application.id,
            "message": "Farm vendor application submitted successfully",
            "next_steps": "Upload required documents and wait for review",
            "estimated_review_time": "5-7 business days",
            "required_documents": [
                "Farm photos (fields, facilities, equipment)",
                "Business license or registration",
                "Certification documents (organic, etc.)",
                "Insurance proof",
                "Farm operation photos"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to submit farm vendor application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/local", response_model=List[dict])
async def get_local_farms(
    postal_code: str = "10001",
    country: str = "US",
    max_distance_km: float = 50.0,
    vendor_type: Optional[str] = None,
    certifications: Optional[str] = None,
    farming_methods: Optional[str] = None,
    has_farm_dining: Optional[bool] = None,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get local farms based on location and preferences"""
    try:
        # Default location (would use geocoding in production)
        user_location = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]  # Default NYC
        }
        
        filters = {}
        if vendor_type:
            filters["vendor_type"] = vendor_type
        if certifications:
            filters["certifications"] = certifications.split(",")
        if farming_methods:
            filters["farming_methods"] = farming_methods.split(",")
        if has_farm_dining is not None:
            filters["has_farm_dining"] = has_farm_dining
        
        farms = await farm_ecosystem_service.get_local_farms(
            user_location, postal_code, country, max_distance_km, filters
        )
        
        return farms
        
    except Exception as e:
        logger.error(f"Failed to get local farms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/{farm_id}/products", response_model=List[dict])
async def get_farm_products(
    farm_id: str,
    category: Optional[str] = None,
    availability_type: Optional[str] = None,
    in_season_only: bool = False
):
    """Get products from a specific farm"""
    try:
        query = {"farm_id": farm_id, "is_active": True}
        
        if category:
            query["category"] = category
        if availability_type:
            query["availability_type"] = availability_type
        
        if in_season_only:
            current_month = datetime.utcnow().strftime('%B')
            query["$or"] = [
                {"availability_type": "year_round"},
                {"seasonal_months": {"$in": [current_month]}}
            ]
        
        products_cursor = db.farm_products.find(query, {"_id": 0}).sort("product_name", 1)
        products = await products_cursor.to_list(length=100)
        
        # Get farm info
        farm = await db.farm_profiles.find_one({"id": farm_id}, {"_id": 0})
        farm_name = farm["farm_name"] if farm else "Unknown Farm"
        
        # Enrich products with farm name
        for product in products:
            product["farm_name"] = farm_name
        
        return products
        
    except Exception as e:
        logger.error(f"Failed to get farm products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/farms/{farm_id}/products", response_model=dict)
async def create_farm_product(
    farm_id: str,
    product_data: FarmProductRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create a new farm product (for farm vendors)"""
    try:
        # Verify user owns this farm
        farm = await db.farm_profiles.find_one({"id": farm_id, "vendor_id": current_user_id}, {"_id": 0})
        if not farm:
            raise HTTPException(status_code=403, detail="You don't have permission to add products to this farm")
        
        product = await farm_ecosystem_service.create_farm_product(
            product_data.dict(), current_user_id
        )
        
        return {
            "success": True,
            "product_id": product.id,
            "message": "Farm product created successfully",
            "product_name": product.product_name,
            "category": product.category.value,
            "price_per_unit": product.price_per_unit
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create farm product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/farms/products/order", response_model=dict)
async def order_farm_products(
    order_data: FarmProductOrderRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Order products from local farms"""
    try:
        order = await farm_ecosystem_service.order_farm_products(
            order_data.dict(), current_user_id
        )
        
        # Get farm info
        farm = await db.farm_profiles.find_one({"id": order_data.farm_id}, {"_id": 0})
        farm_name = farm["farm_name"] if farm else "Unknown Farm"
        
        return {
            "success": True,
            "order_id": order.id,
            "farm_name": farm_name,
            "total_amount": order.total_amount,
            "farmer_payout": order.farmer_payout,
            "platform_commission": order.platform_commission,
            "delivery_method": order.delivery_method,
            "preferred_delivery_date": order.preferred_delivery_date.isoformat(),
            "confirmation_code": order.id[:8].upper(),
            "message": "Farm product order placed successfully!"
        }
        
    except Exception as e:
        logger.error(f"Failed to order farm products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/seasonal-calendar", response_model=dict)
async def get_seasonal_harvest_calendar(
    postal_code: str = "10001",
    country: str = "US",
    max_distance_km: float = 50.0,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get seasonal harvest calendar from local farms"""
    try:
        user_location = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]
        }
        
        calendar = await farm_ecosystem_service.get_seasonal_harvest_calendar(
            user_location, postal_code, max_distance_km
        )
        
        # Add current season information
        current_month = datetime.utcnow().strftime('%B')
        current_season = farm_ecosystem_service._month_to_season(current_month)
        
        return {
            "success": True,
            "current_season": current_season,
            "current_month": current_month,
            "seasonal_calendar": calendar,
            "total_farms": len(set(item["farm_name"] for season_items in calendar.values() for item in season_items)),
            "message": f"Seasonal harvest calendar for {max_distance_km}km radius"
        }
        
    except Exception as e:
        logger.error(f"Failed to get seasonal harvest calendar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/farms/recipe-sourcing", response_model=dict)
async def get_recipe_ingredient_sourcing(
    request_data: dict,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get local sourcing options for recipe ingredients"""
    try:
        ingredients = request_data.get("ingredients", [])
        postal_code = request_data.get("postal_code", "10001")
        max_distance_km = request_data.get("max_distance_km", 30.0)
        
        if not ingredients:
            raise HTTPException(status_code=400, detail="Ingredients list is required")
        
        user_location = {
            "type": "Point", 
            "coordinates": [-73.935242, 40.730610]
        }
        
        sourcing_info = await farm_ecosystem_service.get_recipe_ingredient_sourcing(
            ingredients, user_location, postal_code, max_distance_km
        )
        
        return {
            "success": True,
            "recipe_ingredients": ingredients,
            **sourcing_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get recipe ingredient sourcing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/dining-venues", response_model=List[dict])
async def get_farm_dining_venues(
    postal_code: str = "10001",
    country: str = "US",
    max_distance_km: float = 50.0,
    venue_type: Optional[str] = None,
    max_capacity: Optional[int] = None,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get farm dining venues for outdoor farm-to-table experiences"""
    try:
        user_location = {
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]
        }
        
        # Get local farms first
        farms = await farm_matching_service.find_local_farms(
            user_location, postal_code, country, max_distance_km, {"has_farm_dining": True}
        )
        
        # Get dining venues for these farms
        farm_ids = [farm["id"] for farm in farms]
        
        query = {
            "farm_id": {"$in": farm_ids},
            "is_active": True,
            "is_accepting_bookings": True
        }
        
        if venue_type:
            query["venue_type"] = venue_type
        if max_capacity:
            query["max_capacity"] = {"$gte": max_capacity}
        
        venues_cursor = db.farm_dining_venues.find(query, {"_id": 0})
        venues = await venues_cursor.to_list(length=50)
        
        # Enrich with farm information and distance
        enriched_venues = []
        for venue in venues:
            farm = next((f for f in farms if f["id"] == venue["farm_id"]), None)
            if farm:
                venue["farm_name"] = farm["farm_name"]
                venue["distance_km"] = farm["distance_km"]
                venue["farm_certifications"] = farm.get("certifications", [])
                enriched_venues.append(venue)
        
        # Sort by distance
        enriched_venues.sort(key=lambda x: x["distance_km"])
        
        return enriched_venues
        
    except Exception as e:
        logger.error(f"Failed to get farm dining venues: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/farms/dining/book", response_model=dict)
async def book_farm_dining_experience(
    booking_data: FarmDiningBookingRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Book a farm dining experience"""
    try:
        booking = await farm_ecosystem_service.book_farm_dining(
            booking_data.dict(), current_user_id
        )
        
        # Get venue and farm info
        venue = await db.farm_dining_venues.find_one({"id": booking_data.venue_id}, {"_id": 0})
        farm = await db.farm_profiles.find_one({"id": venue["farm_id"]}, {"_id": 0}) if venue else None
        
        return {
            "success": True,
            "booking_id": booking.id,
            "confirmation_code": booking.confirmation_code,
            "farm_name": farm["farm_name"] if farm else "Unknown Farm",
            "venue_name": venue["venue_name"] if venue else "Farm Dining",
            "dining_date": booking.dining_date.isoformat(),
            "number_of_guests": booking.number_of_guests,
            "total_amount": booking.total_amount,
            "includes_farm_tour": booking.includes_farm_tour,
            "farmer_payout": booking.farmer_payout,
            "message": "Farm dining experience booked successfully!"
        }
        
    except Exception as e:
        logger.error(f"Failed to book farm dining experience: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/my-farm/analytics", response_model=dict)
async def get_my_farm_analytics(current_user_id: str = Depends(get_current_user)):
    """Get analytics for farm vendor"""
    try:
        analytics = await farm_ecosystem_service.get_farm_analytics(current_user_id)
        return {
            "success": True,
            "analytics": analytics
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get farm analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/farms/categories", response_model=List[dict])
async def get_farm_product_categories():
    """Get available farm product categories"""
    categories = [
        {"value": "fresh_vegetables", "label": "Fresh Vegetables", "icon": "🥬"},
        {"value": "organic_produce", "label": "Organic Produce", "icon": "🌱"},
        {"value": "fruits", "label": "Fruits", "icon": "🍎"},
        {"value": "herbs_spices", "label": "Herbs & Spices", "icon": "🌿"},
        {"value": "dairy_products", "label": "Dairy Products", "icon": "🥛"},
        {"value": "fresh_meat", "label": "Fresh Meat", "icon": "🥩"},
        {"value": "poultry", "label": "Poultry", "icon": "🐔"},
        {"value": "eggs", "label": "Fresh Eggs", "icon": "🥚"},
        {"value": "honey", "label": "Honey", "icon": "🍯"},
        {"value": "grains", "label": "Grains", "icon": "🌾"},
        {"value": "nuts", "label": "Nuts", "icon": "🥜"},
        {"value": "specialty_items", "label": "Specialty Items", "icon": "⭐"}
    ]
    
    return categories

@api_router.get("/farms/certifications", response_model=List[dict])
async def get_farm_certifications():
    """Get available farm certifications"""
    certifications = [
        {"value": "usda_organic", "label": "USDA Organic", "icon": "🌱"},
        {"value": "non_gmo", "label": "Non-GMO", "icon": "🚫"},
        {"value": "grass_fed", "label": "Grass Fed", "icon": "🌾"},
        {"value": "free_range", "label": "Free Range", "icon": "🐓"},
        {"value": "pasture_raised", "label": "Pasture Raised", "icon": "🌳"},
        {"value": "sustainable", "label": "Sustainable", "icon": "♻️"},
        {"value": "local_grown", "label": "Local Grown", "icon": "📍"},
        {"value": "biodynamic", "label": "Biodynamic", "icon": "🌙"}
    ]
    
    return certifications

@api_router.get("/farms/stats", response_model=dict)
async def get_farm_ecosystem_stats():
    """Get general farm ecosystem statistics"""
    try:
        # Public metrics
        total_farms = await db.farm_profiles.count_documents({"is_active": True})
        total_products = await db.farm_products.count_documents({"is_active": True, "is_available": True})
        total_dining_venues = await db.farm_dining_venues.count_documents({"is_active": True})
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_orders = await db.farm_product_orders.count_documents({"order_date": {"$gte": week_ago}})
        recent_dining_bookings = await db.farm_dining_bookings.count_documents({"booking_date": {"$gte": week_ago}})
        
        # Certification distribution
        cert_pipeline = [
            {"$unwind": "$certifications"},
            {"$group": {"_id": "$certifications", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        
        cert_results = await db.farm_profiles.aggregate(cert_pipeline).to_list(length=5)
        top_certifications = [{"certification": cert["_id"], "count": cert["count"]} for cert in cert_results]
        
        return {
            "success": True,
            "total_active_farms": total_farms,
            "total_available_products": total_products,
            "total_dining_venues": total_dining_venues,
            "recent_orders_7_days": recent_orders,
            "recent_dining_bookings_7_days": recent_dining_bookings,
            "top_certifications": top_certifications,
            "platform_commission_rates": {
                "farm_products": "10%",
                "farm_dining": "15%"
            },
            "message": "Lambalia Farm Ecosystem - Connecting communities through local agriculture"
        }
        
    except Exception as e:
        logger.error(f"Failed to get farm ecosystem stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ENHANCED AD SYSTEM & MONETIZATION ROUTES - Phase 3

# Initialize monetization services
ad_placement_service = AdPlacementService(db)
premium_service = PremiumMembershipService(db)
surge_pricing_service = SurgePricingService(db)
revenue_analytics_service = RevenueAnalyticsService(db)
engagement_service = EngagementAnalysisService(db)

@api_router.get("/ads/placement", response_model=dict)
async def get_targeted_ad(
    placement: str = "between_snippets",
    page_context: str = "feed",
    position: int = 1,
    cuisine_type: Optional[str] = None,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get targeted ad for specific placement"""
    try:
        if not current_user_id:
            return {"ad": None, "reason": "No user context"}
        
        # Convert placement string to enum
        try:
            placement_enum = AdPlacement(placement)
        except ValueError:
            placement_enum = AdPlacement.BETWEEN_SNIPPETS
        
        context = {
            "page_context": page_context,
            "position": position,
            "cuisine_type": cuisine_type,
            "device_type": "web"
        }
        
        ad_data = await ad_placement_service.get_targeted_ad(
            current_user_id, placement_enum, context
        )
        
        if ad_data:
            return {
                "success": True,
                "ad": ad_data,
                "placement": placement,
                "context": context
            }
        else:
            return {
                "success": True,
                "ad": None,
                "reason": "No suitable ads available or user limit reached"
            }
        
    except Exception as e:
        logger.error(f"Failed to get targeted ad: {str(e)}")
        return {"success": False, "error": str(e)}

@api_router.post("/ads/click/{ad_id}", response_model=dict)
async def record_ad_click(
    ad_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Record ad click and calculate revenue"""
    try:
        result = await ad_placement_service.record_ad_click(ad_id, current_user_id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to record ad click: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/ads/create", response_model=dict)
async def create_advertisement(
    ad_data: AdCreationRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Create new advertisement (for advertisers)"""
    try:
        # Parse dates if provided
        ad_dict = ad_data.dict()
        if ad_data.start_date:
            ad_dict['start_date'] = datetime.fromisoformat(ad_data.start_date.replace('Z', '+00:00'))
        if ad_data.end_date:
            ad_dict['end_date'] = datetime.fromisoformat(ad_data.end_date.replace('Z', '+00:00'))
        
        ad_dict['advertiser_id'] = current_user_id
        ad_dict['id'] = str(uuid.uuid4())
        
        await db.advertisements.insert_one(ad_dict)
        
        return {
            "success": True,
            "ad_id": ad_dict['id'],
            "message": "Advertisement created successfully",
            "status": "pending_review"
        }
        
    except Exception as e:
        logger.error(f"Failed to create advertisement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/premium/benefits", response_model=dict)
async def get_premium_benefits(current_user_id: str = Depends(get_current_user)):
    """Get premium membership benefits and recommendations"""
    try:
        benefits = await premium_service.get_premium_benefits_summary(current_user_id)
        return {
            "success": True,
            **benefits
        }
        
    except Exception as e:
        logger.error(f"Failed to get premium benefits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/premium/upgrade", response_model=dict)
async def upgrade_to_premium(
    upgrade_data: PremiumUpgradeRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Upgrade user to premium tier"""
    try:
        result = await premium_service.upgrade_to_premium(
            current_user_id, 
            upgrade_data.tier, 
            upgrade_data.billing_cycle
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Successfully upgraded to {upgrade_data.tier.value}",
                **result
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upgrade to premium: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/premium/tiers", response_model=List[dict])
async def get_premium_tiers():
    """Get available premium tiers and pricing"""
    tiers = [
        {
            "tier": "cook_plus",
            "name": "Cook Plus",
            "monthly_price": 4.99,
            "annual_price": 49.99,
            "savings_annual": "17%",
            "description": "Enhanced features for home cooks",
            "features": [
                "Ad-free experience",
                "Unlimited cooking offers",
                "Enhanced profile customization",
                "Priority customer support",
                "Advanced cooking analytics"
            ],
            "target_audience": "Active home cooks",
            "popular": False
        },
        {
            "tier": "foodie_pro",
            "name": "Foodie Pro",
            "monthly_price": 7.99,
            "annual_price": 79.99,
            "savings_annual": "17%",
            "description": "Premium experience for food lovers",
            "features": [
                "Ad-free experience",
                "Priority booking for popular meals",
                "Access to premium recipe collection",
                "Custom dietary filters",
                "Bulk translation capabilities",
                "Priority customer support"
            ],
            "target_audience": "Food enthusiasts",
            "popular": True
        },
        {
            "tier": "culinary_vip",
            "name": "Culinary VIP",
            "monthly_price": 12.99,
            "annual_price": 129.99,
            "savings_annual": "17%",
            "description": "Complete premium culinary experience",
            "features": [
                "All Cook Plus and Foodie Pro features",
                "Video calling with chefs",
                "Exclusive VIP events and tastings",
                "Personal culinary concierge",
                "Advanced recipe analytics",
                "Beta access to new features"
            ],
            "target_audience": "Culinary professionals and enthusiasts",
            "popular": False
        }
    ]
    
    return tiers

@api_router.get("/engagement/profile", response_model=dict)
async def get_user_engagement_profile(current_user_id: str = Depends(get_current_user)):
    """Get user engagement profile and ad frequency optimization"""
    try:
        profile = await engagement_service.calculate_user_engagement_level(current_user_id)
        
        return {
            "success": True,
            "engagement_level": profile.engagement_level,
            "optimal_ads_per_day": profile.optimal_ads_per_day,
            "premium_eligibility_score": profile.premium_eligibility_score,
            "activity_summary": {
                "snippets_created": profile.snippets_created,
                "cooking_offers_created": profile.cooking_offers_created,
                "eating_requests_created": profile.eating_requests_created,
                "appointments_booked": profile.appointments_booked
            },
            "ad_interaction": {
                "ads_viewed_today": profile.ads_viewed_today,
                "ads_clicked_today": profile.ads_clicked_today,
                "ad_fatigue_score": profile.ad_fatigue_score
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get engagement profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/surge-pricing/status", response_model=dict)
async def get_surge_pricing_status(
    service_type: str = "cooking_offers",
    category: Optional[str] = None
):
    """Get current surge pricing status"""
    try:
        multiplier = await surge_pricing_service.get_current_surge_multiplier(service_type, category)
        
        is_surge_active = multiplier > 1.0
        
        return {
            "success": True,
            "service_type": service_type,
            "category": category,
            "surge_multiplier": multiplier,
            "is_surge_active": is_surge_active,
            "message": f"{'Surge pricing active' if is_surge_active else 'Normal pricing'} - {multiplier}x multiplier"
        }
        
    except Exception as e:
        logger.error(f"Failed to get surge pricing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/surge-pricing/analyze", response_model=dict)
async def analyze_surge_pricing(current_user_id: str = Depends(get_current_user)):
    """Analyze demand and apply surge pricing (admin function)"""
    try:
        # Check if user has admin privileges (simplified)
        user = await db.users.find_one({"id": current_user_id}, {"_id": 0})
        if not user or not user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        surge_results = await surge_pricing_service.analyze_and_apply_surge_pricing()
        
        return {
            "success": True,
            "surge_applications": surge_results,
            "message": f"Applied surge pricing to {len(surge_results)} services"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to analyze surge pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/revenue/daily-report", response_model=dict)
async def get_daily_revenue_report(
    date: Optional[str] = None,
    current_user_id: str = Depends(get_current_user)
):
    """Get daily revenue report (admin function)"""
    try:
        # Check admin access
        user = await db.users.find_one({"id": current_user_id}, {"_id": 0})
        if not user or not user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        report_date = None
        if date:
            report_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        
        report = await revenue_analytics_service.generate_daily_revenue_report(report_date)
        
        return {
            "success": True,
            "report": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get daily revenue report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/revenue/trends", response_model=dict)
async def get_revenue_trends(
    days: int = 30,
    current_user_id: str = Depends(get_current_user)
):
    """Get revenue trends over specified period (admin function)"""
    try:
        # Check admin access
        user = await db.users.find_one({"id": current_user_id}, {"_id": 0})
        if not user or not user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        if days > 365:
            raise HTTPException(status_code=400, detail="Maximum 365 days allowed")
        
        trends = await revenue_analytics_service.get_revenue_trends(days)
        
        return {
            "success": True,
            "trends": trends
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get revenue trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/monetization/stats", response_model=dict)
async def get_monetization_stats():
    """Get general monetization statistics"""
    try:
        # Get general stats that don't require admin access
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        
        # Public metrics
        active_premium_users = await db.premium_subscriptions.count_documents({"is_active": True})
        total_cooking_offers = await db.cooking_offers.count_documents({"status": "active"})
        total_ads_today = await db.ad_impressions.count_documents({"timestamp": {"$gte": today}})
        
        # Current surge pricing status
        cooking_surge = await surge_pricing_service.get_current_surge_multiplier("cooking_offers")
        messaging_surge = await surge_pricing_service.get_current_surge_multiplier("messaging")
        
        return {
            "success": True,
            "platform_metrics": {
                "active_premium_users": active_premium_users,
                "active_cooking_offers": total_cooking_offers,
                "ads_shown_today": total_ads_today
            },
            "surge_pricing": {
                "cooking_offers_multiplier": cooking_surge,
                "messaging_multiplier": messaging_surge,
                "is_any_surge_active": max(cooking_surge, messaging_surge) > 1.0
            },
            "premium_tiers_available": 3,
            "ad_placements_available": len(AdPlacement),
            "message": "Lambalia monetization system active"
        }
        
    except Exception as e:
        logger.error(f"Failed to get monetization stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# TRANSLATION SERVICE ROUTES

@api_router.post("/translate")
async def translate_text(request: dict):
    """
    Translate text using AI-powered translation with cultural preservation
    """
    try:
        translation_service = await get_translation_service()
        
        text = request.get('text', '').strip()
        target_language = request.get('target_language', '').strip()
        source_language = request.get('source_language')
        preserve_cultural = request.get('preserve_cultural', True)
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        if not target_language:
            raise HTTPException(status_code=400, detail="Target language is required")
        
        result = await translation_service.translate_text(
            text=text,
            target_language=target_language,
            source_language=source_language,
            preserve_cultural=preserve_cultural
        )
        
        if result['success']:
            return {
                "success": True,
                "translated_text": result['translated_text'],
                "source_language": result.get('source_language') or result.get('detected_language'),
                "target_language": result['target_language'],
                "method": result['method'],
                "character_count": result['character_count'],
                "processing_time_ms": result['processing_time_ms'],
                "cache_hit": result['cache_hit'],
                "request_id": result['request_id']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service error")

@api_router.post("/translate/batch")
async def batch_translate_texts(request: dict):
    """
    Translate multiple texts in batch
    """
    try:
        translation_service = await get_translation_service()
        
        texts = request.get('texts', [])
        target_language = request.get('target_language', '').strip()
        source_language = request.get('source_language')
        preserve_cultural = request.get('preserve_cultural', True)
        
        if not texts or not isinstance(texts, list):
            raise HTTPException(status_code=400, detail="Texts array is required")
        
        if not target_language:
            raise HTTPException(status_code=400, detail="Target language is required")
        
        if len(texts) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 texts allowed per batch")
        
        result = await translation_service.batch_translate(
            texts=texts,
            target_language=target_language,
            source_language=source_language,
            preserve_cultural=preserve_cultural
        )
        
        return {
            "success": result['success'],
            "translations": result['translations'],
            "total_characters": result['total_characters'],
            "total_texts": result['total_texts'],
            "successful_translations": result['successful_translations'],
            "errors": result['errors']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch translation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service error")

@api_router.post("/translate/detect-language")
async def detect_text_language(request: dict):
    """
    Detect the language of provided text
    """
    try:
        translation_service = await get_translation_service()
        
        text = request.get('text', '').strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        result = await translation_service.detect_language(text)
        
        if result['success']:
            return {
                "success": True,
                "detected_language": result['detected_language'],
                "language_name": translation_service.supported_languages.get(result['detected_language'], result['detected_language']),
                "confidence": result['confidence'],
                "method": result['method']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Language detection endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Language detection service error")

@api_router.get("/translate/supported-languages")
async def get_supported_languages():
    """
    Get list of supported languages for translation
    """
    try:
        translation_service = await get_translation_service()
        supported_languages = translation_service.get_supported_languages()
        
        return {
            "success": True,
            "languages": [
                {"code": code, "name": name}
                for code, name in supported_languages.items()
            ],
            "total_languages": len(supported_languages)
        }
        
    except Exception as e:
        logger.error(f"Get supported languages error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service error")

@api_router.get("/translate/stats")
async def get_translation_stats():
    """
    Get translation service usage statistics
    """
    try:
        translation_service = await get_translation_service()
        stats = translation_service.get_usage_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Get translation stats error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service error")

# CHARITY PROGRAM & PREMIUM MEMBERSHIP ROUTES - Social Impact Integration

@api_router.post("/charity/register", response_model=dict)
async def register_for_charity_program(
    registration_data: CharityProgramRegistrationRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Register user for charity program to earn premium membership"""
    try:
        program = await charity_program_service.register_charity_program(
            registration_data.dict(), current_user_id
        )
        
        return {
            "success": True,
            "program_id": program.id,
            "message": "Successfully registered for charity program!",
            "benefits": [
                "Earn premium membership through community service",
                "Reduce platform commission rates",
                "Gain community recognition",
                "Make positive local impact"
            ],
            "next_steps": [
                "Start volunteering at local food banks",
                "Submit charity activities for verification",
                "Upload evidence of your community work",
                "Build your impact score for premium benefits"
            ],
            "monthly_goal": program.monthly_impact_goal,
            "premium_tier": "Community Helper",
            "commission_reduction": "14% (1% reduction from standard 15%)"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to register charity program: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/charity/submit-activity", response_model=dict)
async def submit_charity_activity(
    activity_data: CharityActivitySubmissionRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Submit charity activity for verification and impact scoring"""
    try:
        activity = await charity_program_service.submit_charity_activity(
            activity_data.dict(), current_user_id
        )
        
        return {
            "success": True,
            "activity_id": activity.id,
            "message": "Charity activity submitted successfully!",
            "impact_score": activity.calculated_impact_score,
            "verification_status": activity.verification_status,
            "review_process": {
                "status": "Submitted for committee review",
                "estimated_review_time": "2-5 business days",
                "next_steps": [
                    "Committee will verify your documents",
                    "Impact score will be confirmed",
                    "You'll receive email notification of results"
                ]
            },
            "activity_summary": {
                "type": activity.activity_type,
                "organization": activity.charity_organization_name,
                "date": activity.activity_date.isoformat(),
                "food_donated_lbs": activity.food_donated_lbs,
                "meals_provided": activity.meals_provided,
                "people_helped": activity.people_helped,
                "volunteer_hours": activity.volunteer_hours
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to submit charity activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/charity/dashboard", response_model=dict)
async def get_charity_dashboard(current_user_id: str = Depends(get_current_user)):
    """Get comprehensive charity dashboard for user"""
    try:
        dashboard = await charity_program_service.get_user_charity_dashboard(current_user_id)
        
        if "error" in dashboard:
            return {
                "success": False,
                "error": dashboard["error"],
                "registration_available": True,
                "message": "Register for charity program to start earning premium benefits through community service"
            }
        
        return {
            "success": True,
            **dashboard
        }
        
    except Exception as e:
        logger.error(f"Failed to get charity dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/charity/community-impact", response_model=dict)
async def get_community_impact_metrics():
    """Get platform-wide community impact metrics"""
    try:
        metrics = await charity_program_service.get_community_impact_metrics()
        
        return {
            "success": True,
            "community_impact": metrics,
            "message": "Lambalia community making a difference one meal at a time!"
        }
        
    except Exception as e:
        logger.error(f"Failed to get community impact metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/charity/premium-upgrade", response_model=dict)
async def upgrade_premium_via_charity(
    upgrade_data: PremiumMembershipUpgradeRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Upgrade premium membership through charity work or payment"""
    try:
        membership = await charity_program_service.upgrade_premium_membership(
            upgrade_data.dict(), current_user_id
        )
        
        tier_names = {
            PremiumTier.COMMUNITY_HELPER: "Community Helper",
            PremiumTier.GARDEN_SUPPORTER: "Garden Supporter", 
            PremiumTier.LOCAL_CHAMPION: "Local Champion"
        }
        
        commission_rates = {
            PremiumTier.COMMUNITY_HELPER: 14,  # 15% -> 14%
            PremiumTier.GARDEN_SUPPORTER: 13,  # 15% -> 13%
            PremiumTier.LOCAL_CHAMPION: 12    # 15% -> 12%
        }
        
        tier = PremiumTier(membership["tier"])
        
        return {
            "success": True,
            "membership_id": membership["id"],
            "tier": tier.value,
            "tier_name": tier_names[tier],
            "earned_through": membership["earned_through"],
            "commission_rate": f"{commission_rates[tier]}%",
            "monthly_payment": membership["monthly_payment"],
            "benefits_active": True,
            "message": f"Successfully upgraded to {tier_names[tier]}!",
            "key_benefits": [
                f"Commission reduced to {commission_rates[tier]}%",
                "Priority customer support",
                "Community recognition badge",
                "Advanced analytics dashboard"
            ]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to upgrade premium via charity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/charity/premium-benefits", response_model=dict)
async def get_charity_premium_benefits(current_user_id: str = Depends(get_current_user)):
    """Get detailed premium membership benefits earned through charity"""
    try:
        benefits = await charity_program_service.get_premium_membership_benefits(current_user_id)
        
        if "error" in benefits:
            return {
                "success": False,
                "error": benefits["error"],
                "available_tiers": [
                    {
                        "tier": "community_helper",
                        "name": "Community Helper",
                        "cost": "FREE through 4 hours monthly charity work",
                        "commission_rate": "14% (1% savings)",
                        "requirements": "2 charity activities, 5 lbs food donated monthly"
                    },
                    {
                        "tier": "garden_supporter", 
                        "name": "Garden Supporter",
                        "cost": "$4.99/month OR 8 hours monthly charity work",
                        "commission_rate": "13% (2% savings)",
                        "requirements": "3 charity activities, 15 lbs food donated monthly"
                    },
                    {
                        "tier": "local_champion",
                        "name": "Local Champion", 
                        "cost": "$9.99/month OR 12 hours monthly charity work",
                        "commission_rate": "12% (3% savings)",
                        "requirements": "5 charity activities, 30 lbs food donated monthly"
                    }
                ]
            }
        
        return {
            "success": True,
            **benefits
        }
        
    except Exception as e:
        logger.error(f"Failed to get charity premium benefits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/charity/local-organizations", response_model=List[dict])
async def get_local_charity_organizations(
    postal_code: str = "10001",
    charity_types: Optional[str] = None,
    current_user_id: str = Depends(get_current_user_optional)
):
    """Get local charity organizations for users to volunteer with"""
    try:
        # Parse charity types filter
        types_filter = []
        if charity_types:
            types_filter = charity_types.split(",")
        
        # Mock data for now - in production would query actual partner database
        organizations = [
            {
                "id": str(uuid.uuid4()),
                "name": "Downtown Food Bank",
                "type": "food_bank",
                "description": "Providing food assistance to families in need since 1985",
                "address": "123 Main St, Downtown",
                "phone": "(555) 123-4567",
                "email": "volunteer@downtownfoodbank.org",
                "website": "https://downtownfoodbank.org",
                "services": ["Food distribution", "Emergency meals", "Senior nutrition"],
                "volunteer_opportunities": [
                    "Food sorting and packing",
                    "Distribution assistance", 
                    "Delivery to seniors",
                    "Special events"
                ],
                "operating_hours": {
                    "monday": "9:00 AM - 5:00 PM",
                    "tuesday": "9:00 AM - 5:00 PM", 
                    "wednesday": "9:00 AM - 5:00 PM",
                    "thursday": "9:00 AM - 5:00 PM",
                    "friday": "9:00 AM - 5:00 PM",
                    "saturday": "9:00 AM - 2:00 PM",
                    "sunday": "Closed"
                },
                "current_needs": ["Volunteers for weekend distribution", "Food donations"],
                "impact_last_month": {
                    "people_served": 450,
                    "meals_provided": 1800,
                    "volunteer_hours": 320
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Community Shelter",
                "type": "homeless_shelter",
                "description": "Emergency shelter and support services for homeless individuals and families",
                "address": "456 Oak Ave, Midtown",
                "phone": "(555) 234-5678",
                "email": "help@communityshelter.org",
                "services": ["Emergency shelter", "Meals", "Case management", "Job training"],
                "volunteer_opportunities": [
                    "Meal preparation and serving",
                    "Clothing donations organization",
                    "Life skills workshops",
                    "Transportation assistance"
                ],
                "operating_hours": {
                    "daily": "24/7 Emergency Services"
                },
                "current_needs": ["Kitchen volunteers", "Meal donations", "Clothing donations"],
                "impact_last_month": {
                    "people_served": 125,
                    "meals_provided": 2400,
                    "volunteer_hours": 180
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Community Kitchen Network",
                "type": "community_kitchen",
                "description": "Community-operated kitchen providing free meals and cooking education",
                "address": "789 Pine St, Westside",
                "phone": "(555) 345-6789",
                "email": "info@communitykitchen.org",
                "services": ["Free community meals", "Cooking classes", "Nutrition education"],
                "volunteer_opportunities": [
                    "Cooking and meal prep",
                    "Teaching cooking classes",
                    "Garden maintenance",
                    "Event coordination"
                ],
                "operating_hours": {
                    "monday": "11:00 AM - 7:00 PM",
                    "wednesday": "11:00 AM - 7:00 PM",
                    "friday": "11:00 AM - 7:00 PM",
                    "saturday": "10:00 AM - 3:00 PM"
                },
                "current_needs": ["Cooking instructors", "Fresh produce", "Kitchen equipment"],
                "impact_last_month": {
                    "people_served": 300,
                    "meals_provided": 900,
                    "volunteer_hours": 240
                }
            }
        ]
        
        # Filter by charity types if specified
        if types_filter:
            organizations = [org for org in organizations if org["type"] in types_filter]
        
        return organizations
        
    except Exception as e:
        logger.error(f"Failed to get local charity organizations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/charity/activity-types", response_model=List[dict])
async def get_charity_activity_types():
    """Get available charity activity types for submissions"""
    types = [
        {
            "value": "food_bank",
            "label": "Food Bank",
            "icon": "🏪",
            "description": "Volunteering at local food banks",
            "typical_activities": ["Food sorting", "Distribution", "Inventory management"],
            "impact_multiplier": 1.2
        },
        {
            "value": "homeless_shelter", 
            "label": "Homeless Shelter",
            "icon": "🏠",
            "description": "Supporting homeless individuals and families",
            "typical_activities": ["Meal service", "Shelter support", "Case management"],
            "impact_multiplier": 1.3
        },
        {
            "value": "community_kitchen",
            "label": "Community Kitchen", 
            "icon": "👩‍🍳",
            "description": "Community meal preparation and service",
            "typical_activities": ["Cooking", "Meal prep", "Teaching cooking skills"],
            "impact_multiplier": 1.1
        },
        {
            "value": "seniors_center",
            "label": "Seniors Center",
            "icon": "👵",
            "description": "Supporting elderly community members",
            "typical_activities": ["Meal delivery", "Social activities", "Transportation"],
            "impact_multiplier": 1.1
        },
        {
            "value": "school_program",
            "label": "School Program",
            "icon": "🏫", 
            "description": "Supporting school nutrition programs",
            "typical_activities": ["Breakfast programs", "After-school snacks", "Nutrition education"],
            "impact_multiplier": 1.2
        },
        {
            "value": "emergency_relief",
            "label": "Emergency Relief",
            "icon": "🚨",
            "description": "Emergency disaster and crisis response",
            "typical_activities": ["Emergency meals", "Disaster relief", "Crisis support"],
            "impact_multiplier": 1.5
        },
        {
            "value": "local_charity",
            "label": "Local Charity",
            "icon": "❤️",
            "description": "Other local charitable organizations",
            "typical_activities": ["Community events", "Fundraising", "General volunteering"],
            "impact_multiplier": 1.0
        }
    ]
    
    return types

@api_router.get("/charity/impact-calculator", response_model=dict)
async def calculate_charity_impact(
    activity_type: str,
    food_donated_lbs: Optional[float] = None,
    meals_provided: Optional[int] = None,
    people_helped: Optional[int] = None,
    volunteer_hours: Optional[float] = None
):
    """Calculate potential impact score for charity activity (preview)"""
    try:
        # Create a mock activity for calculation
        from charity_program_models import CharityActivity
        
        mock_activity = CharityActivity(
            id="preview",
            user_id="preview",
            charity_program_id="preview",
            activity_type=CharityType(activity_type),
            charity_organization_name="Preview",
            activity_description="Impact calculation preview",
            activity_date=datetime.utcnow(),
            location_address="Preview",
            city="Preview",
            state="Preview", 
            postal_code="00000",
            food_donated_lbs=food_donated_lbs,
            meals_provided=meals_provided,
            people_helped=people_helped,
            volunteer_hours=volunteer_hours
        )
        
        impact_calculator = CharityImpactCalculator()
        impact_score = impact_calculator.calculate_activity_impact_score(mock_activity)
        
        # Determine tier progress
        tier_requirements = impact_calculator.calculate_tier_requirements()
        
        tier_progress = []
        for tier, requirements in tier_requirements.items():
            progress_percentage = min(100, (impact_score / requirements["monthly_impact_required"]) * 100)
            tier_progress.append({
                "tier": tier.value,
                "tier_name": tier.value.replace("_", " ").title(),
                "required_score": requirements["monthly_impact_required"],
                "progress_percentage": round(progress_percentage, 1),
                "this_activity_contribution": round(progress_percentage, 1)
            })
        
        return {
            "success": True,
            "estimated_impact_score": impact_score,
            "activity_breakdown": {
                "base_score": 10.0,
                "food_donation_points": (food_donated_lbs or 0) * 2.0,
                "meals_provided_points": (meals_provided or 0) * 5.0,
                "people_helped_points": (people_helped or 0) * 3.0,
                "volunteer_hours_points": (volunteer_hours or 0) * 8.0
            },
            "tier_progress": tier_progress,
            "next_tier_info": tier_progress[1] if len(tier_progress) > 1 else None,
            "monthly_activities_needed": f"With this impact level, you'd need {max(1, int(30/max(1, impact_score)))} similar activities per month for Community Helper tier"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid activity type: {activity_type}")
    except Exception as e:
        logger.error(f"Failed to calculate charity impact: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Webhook endpoint for Stripe
@api_router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    
    payload = await request.body()
    signature = request.headers.get('stripe-signature')
    
    try:
        event_data = await payment_service.handle_webhook(payload.decode(), signature)
        
        if event_data['event_type'] == 'payment_succeeded':
            # Update booking status
            await db.bookings.update_one(
                {"id": event_data['booking_id']},
                {
                    "$set": {
                        "payment_status": PaymentStatus.CAPTURED,
                        "status": BookingStatus.CONFIRMED,
                        "confirmed_at": datetime.utcnow()
                    }
                }
            )
            
            # Update payment record
            await db.payments.update_one(
                {"booking_id": event_data['booking_id']},
                {
                    "$set": {
                        "status": PaymentStatus.CAPTURED,
                        "processed_at": datetime.utcnow()
                    }
                }
            )
        
        elif event_data['event_type'] == 'payment_failed':
            # Update booking status
            await db.bookings.update_one(
                {"id": event_data['booking_id']},
                {
                    "$set": {
                        "payment_status": PaymentStatus.FAILED,
                        "status": BookingStatus.CANCELLED
                    }
                }
            )
        
        return {"status": "success"}
        
    except Exception as e:
        logging.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Keep all existing routes from previous implementation
# (Reference recipes, snippets, grocery, etc.)

# Include main API router
app.include_router(api_router)

# Include Lambalia Eats router with proper prefix
lambalia_eats_router = create_lambalia_eats_router(lambalia_eats_service, get_current_user, get_current_user_optional)
app.include_router(lambalia_eats_router, prefix="/api")

# Include Heritage Recipes router with proper prefix
heritage_recipes_router = create_heritage_recipes_router(heritage_recipes_service, get_current_user, get_current_user_optional)
app.include_router(heritage_recipes_router, prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Create indexes for marketplace
    await db.vendor_applications.create_index("user_id")
    await db.vendor_applications.create_index("status")
    await db.vendor_applications.create_index("vendor_type")
    await db.home_restaurants.create_index("vendor_id")
    await db.home_restaurants.create_index([("latitude", "2dsphere"), ("longitude", "2dsphere")])
    await db.traditional_restaurants.create_index("vendor_id")
    await db.traditional_restaurants.create_index([("latitude", "2dsphere"), ("longitude", "2dsphere")])
    await db.traditional_restaurants.create_index("cuisine_type")
    await db.special_orders.create_index("restaurant_id")
    await db.special_orders.create_index("vendor_id")
    await db.special_orders.create_index("status")
    await db.special_orders.create_index("cuisine_style")
    await db.special_orders.create_index("occasion_type")
    await db.bookings.create_index("guest_id")
    await db.bookings.create_index("vendor_id")
    await db.bookings.create_index("booking_date")
    await db.bookings.create_index("booking_type")
    await db.reviews.create_index("restaurant_id")
    await db.payments.create_index("booking_id")
    
    # Create indexes for daily marketplace
    await db.cooking_offers.create_index("cook_id")
    await db.cooking_offers.create_index("status")
    await db.cooking_offers.create_index("category")
    await db.cooking_offers.create_index("cuisine_type")
    await db.cooking_offers.create_index([("location", "2dsphere")])
    await db.cooking_offers.create_index("cooking_date")
    await db.cooking_offers.create_index("expires_at")
    await db.cooking_offers.create_index("postal_code")
    await db.eating_requests.create_index("eater_id")
    await db.eating_requests.create_index("status")
    await db.eating_requests.create_index([("location", "2dsphere")])
    await db.eating_requests.create_index("preferred_date")
    await db.eating_requests.create_index("expires_at")
    await db.eating_requests.create_index("postal_code")
    await db.cook_offer_matches.create_index("offer_id")
    await db.cook_offer_matches.create_index("request_id")
    await db.cook_offer_matches.create_index("cook_id")
    await db.cook_offer_matches.create_index("eater_id")
    await db.cooking_appointments.create_index("cook_id")
    await db.cooking_appointments.create_index("eater_id")
    await db.cooking_appointments.create_index("offer_id")
    await db.cooking_appointments.create_index("status")
    await db.cooking_appointments.create_index("scheduled_date")
    
    # Create indexes for enhanced monetization system
    await db.advertisements.create_index("advertiser_id")
    await db.advertisements.create_index("status")
    await db.advertisements.create_index("ad_type")
    await db.advertisements.create_index([("start_date", 1), ("end_date", 1)])
    await db.advertisements.create_index("placement_types")
    await db.user_engagement_profiles.create_index("user_id", unique=True)
    await db.user_engagement_profiles.create_index("engagement_level")
    await db.user_engagement_profiles.create_index("last_updated")
    await db.premium_subscriptions.create_index("user_id", unique=True)
    await db.premium_subscriptions.create_index("is_active")
    await db.premium_subscriptions.create_index("tier")
    await db.premium_subscriptions.create_index("next_billing_date")
    await db.ad_impressions.create_index("ad_id")
    await db.ad_impressions.create_index("user_id")
    await db.ad_impressions.create_index("timestamp")
    await db.ad_impressions.create_index("placement")
    await db.surge_pricing.create_index("applies_to")
    await db.surge_pricing.create_index("is_active")
    await db.surge_pricing.create_index([("activated_at", 1), ("duration_minutes", 1)])
    await db.revenue_analytics.create_index([("date", 1), ("period_type", 1)], unique=True)
    
    # Create indexes for farm ecosystem
    await db.farm_vendor_applications.create_index("user_id")
    await db.farm_vendor_applications.create_index("status")
    await db.farm_vendor_applications.create_index("vendor_type")
    await db.farm_profiles.create_index("vendor_id")
    await db.farm_profiles.create_index([("location", "2dsphere")])
    await db.farm_profiles.create_index("postal_code")
    await db.farm_profiles.create_index("certifications")
    await db.farm_profiles.create_index("farming_methods")
    await db.farm_profiles.create_index("is_active")
    await db.farm_products.create_index("farm_id")
    await db.farm_products.create_index("vendor_id")
    await db.farm_products.create_index("category")
    await db.farm_products.create_index("availability_type")
    await db.farm_products.create_index("seasonal_months")
    await db.farm_products.create_index("is_active")
    await db.farm_product_orders.create_index("customer_id")
    await db.farm_product_orders.create_index("farm_id")
    await db.farm_product_orders.create_index("vendor_id")
    await db.farm_product_orders.create_index("order_date")
    await db.farm_product_orders.create_index("status")
    await db.farm_dining_venues.create_index("farm_id")
    await db.farm_dining_venues.create_index("vendor_id")
    await db.farm_dining_venues.create_index("venue_type")
    await db.farm_dining_venues.create_index("is_active")
    await db.farm_dining_bookings.create_index("customer_id")
    await db.farm_dining_bookings.create_index("farm_id")
    await db.farm_dining_bookings.create_index("vendor_id")
    await db.farm_dining_bookings.create_index("dining_date")
    await db.farm_dining_bookings.create_index("status")
    
    # Create indexes for charity program
    await db.charity_programs.create_index("user_id", unique=True)
    await db.charity_programs.create_index("is_active")
    await db.charity_programs.create_index("current_tier")
    await db.charity_programs.create_index("total_impact_score")
    await db.charity_activities.create_index("user_id")
    await db.charity_activities.create_index("charity_program_id")
    await db.charity_activities.create_index("activity_type")
    await db.charity_activities.create_index("verification_status")
    await db.charity_activities.create_index("activity_date")
    await db.charity_activities.create_index("verified_by")
    await db.charity_committee.create_index("user_id")
    await db.charity_committee.create_index("is_active")
    await db.charity_committee.create_index("specialization")
    await db.premium_memberships.create_index("user_id", unique=True)
    await db.premium_memberships.create_index("tier")
    await db.premium_memberships.create_index("earned_through")
    await db.premium_memberships.create_index("is_active")
    await db.community_impact_metrics.create_index("last_updated")
    await db.local_partner_organizations.create_index("charity_type")
    await db.local_partner_organizations.create_index("postal_code")
    await db.local_partner_organizations.create_index("is_active")
    
    # Create indexes for Lambalia Eats
    await db.food_requests.create_index("eater_id")
    await db.food_requests.create_index("status")
    await db.food_requests.create_index("cuisine_type")
    await db.food_requests.create_index("expires_at")
    await db.food_requests.create_index([("eater_location.lat", 1), ("eater_location.lng", 1)])
    await db.food_offers.create_index("cook_id")
    await db.food_offers.create_index("status")
    await db.food_offers.create_index("cuisine_type")
    await db.food_offers.create_index("available_until")
    await db.food_offers.create_index("quantity_remaining")
    await db.food_offers.create_index([("cook_location.lat", 1), ("cook_location.lng", 1)])
    await db.active_orders.create_index("eater_id")
    await db.active_orders.create_index("cook_id")
    await db.active_orders.create_index("current_status")
    await db.active_orders.create_index("ordered_at")
    await db.active_orders.create_index("tracking_code")
    await db.eats_cook_profiles.create_index("user_id", unique=True)
    await db.eats_cook_profiles.create_index("is_currently_available")
    await db.eats_cook_profiles.create_index("specialties")
    await db.eats_eater_profiles.create_index("user_id")
    await db.matching_results.create_index("request_id")
    await db.matching_results.create_index("created_at")
    
    # Create indexes for Heritage Recipes system
    await db.heritage_recipes.create_index("created_by")
    await db.heritage_recipes.create_index("country_region") 
    await db.heritage_recipes.create_index("cultural_significance")
    await db.heritage_recipes.create_index("authenticity_level")
    await db.heritage_recipes.create_index("is_public")
    await db.heritage_recipes.create_index("preservation_priority")
    await db.heritage_recipes.create_index("elder_approved")
    await db.heritage_recipes.create_index("specialty_ingredients")
    await db.heritage_recipes.create_index("created_at")
    await db.specialty_ingredients.create_index("ingredient_name")
    await db.specialty_ingredients.create_index("rarity_level")
    await db.specialty_ingredients.create_index("origin_countries")
    await db.specialty_ingredients.create_index("added_by")
    await db.specialty_ingredients.create_index("available_at_stores")
    await db.ethnic_grocery_stores.create_index("store_name")
    await db.ethnic_grocery_stores.create_index("store_type")
    await db.ethnic_grocery_stores.create_index("specialties")
    await db.ethnic_grocery_stores.create_index([("location.lat", 1), ("location.lng", 1)])
    await db.ethnic_grocery_stores.create_index("postal_code")
    await db.ethnic_grocery_stores.create_index("is_active")
    await db.ethnic_grocery_stores.create_index("added_by")
    await db.cultural_contributors.create_index("user_id", unique=True)
    await db.cultural_contributors.create_index("cultural_heritage")
    await db.cultural_contributors.create_index("community_recognition")
    await db.cultural_contributors.create_index("contribution_score")
    await db.heritage_collections.create_index("curated_by")
    await db.heritage_collections.create_index("featured_country")
    await db.heritage_collections.create_index("cultural_significance")
    await db.heritage_collections.create_index("is_featured")
    await db.heritage_collections.create_index("created_at")
    await db.store_chains.create_index("chain_id", unique=True)
    await db.store_chains.create_index("specialties")
    await db.store_chains.create_index("integration_status")
    
    # Existing indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.snippets.create_index([("created_at", -1)])
    await db.snippets.create_index("author_id")
    await db.snippet_interactions.create_index([("snippet_id", 1), ("user_id", 1)])
    
    logger.info("Lambalia Marketplace API started with comprehensive vetting and payment system including traditional restaurants, daily marketplace, enhanced monetization system, local farm ecosystem, charity program, Lambalia Eats real-time food marketplace, and global heritage recipes preservation system")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()