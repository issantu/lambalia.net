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

# Authentication Routes (keeping existing ones)
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
        application_date=application.application_date,
        documents_required=[
            "Kitchen Photo", "Dining Room Photo", "Front Door Photo",
            "Government ID", "Health Certificate (if required)", "Insurance Proof"
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
    restaurant = HomeRestaurant(
        vendor_id=current_user_id,
        application_id=application['id'],
        restaurant_name=restaurant_data['restaurant_name'],
        description=restaurant_data['description'],
        cuisine_type=restaurant_data.get('cuisine_type', []),
        dining_capacity=restaurant_data['dining_capacity'],
        address=application['address'],
        latitude=restaurant_data.get('latitude', 0.0),
        longitude=restaurant_data.get('longitude', 0.0),
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
    await db.home_restaurants.create_index("vendor_id")
    await db.home_restaurants.create_index([("latitude", "2dsphere"), ("longitude", "2dsphere")])
    await db.bookings.create_index("guest_id")
    await db.bookings.create_index("vendor_id")
    await db.bookings.create_index("booking_date")
    await db.reviews.create_index("restaurant_id")
    await db.payments.create_index("booking_id")
    
    # Existing indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.snippets.create_index([("created_at", -1)])
    await db.snippets.create_index("author_id")
    await db.snippet_interactions.create_index([("snippet_id", 1), ("user_id", 1)])
    
    logger.info("Lambalia Marketplace API started with comprehensive vetting and payment system")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()