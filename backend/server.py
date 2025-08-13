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

# Include router
app.include_router(api_router)

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
    
    # Existing indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.snippets.create_index([("created_at", -1)])
    await db.snippets.create_index("author_id")
    await db.snippet_interactions.create_index([("snippet_id", 1), ("user_id", 1)])
    
    logger.info("Lambalia Marketplace API started with comprehensive vetting and payment system including traditional restaurants and daily marketplace")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()