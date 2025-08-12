from fastapi import FastAPI, APIRouter, HTTPException, Depends, File, UploadFile, Form
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

# Import our extended models
from models_extension import (
    ReferenceRecipe, RecipeSnippet, GroceryStore, IngredientAvailability,
    UserGroceryPreference, SnippetCreate, SnippetResponse, GrocerySearchRequest,
    GrocerySearchResponse, SnippetType, VideoQuality
)
from reference_recipes import REFERENCE_RECIPES, get_recipes_by_country, get_featured_recipes

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Lambalia API Enhanced", description="Advanced Recipe Sharing Platform with Snippets & Grocery Integration")
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(days=7)

# Existing models (keeping the same as before)
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
    snippets_count: int = 0  # New field
    credits: float = 0.0
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    ingredients: List[Dict[str, Any]]
    steps: List[Dict[str, str]]
    cooking_time_minutes: Optional[int] = None
    difficulty_level: int = Field(ge=1, le=5, default=3)
    servings: Optional[int] = None
    cuisine_type: Optional[str] = None
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    dietary_preferences: List[DietaryPreference] = []
    tags: List[str] = []
    main_image: Optional[str] = None
    additional_images: List[str] = []
    author_id: str
    status: RecipeStatus = RecipeStatus.PUBLISHED
    is_premium: bool = False
    premium_price: float = 0.0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
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
    is_verified: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Utility functions
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

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

# Authentication Routes (same as before)
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

# Reference Recipes Routes
@api_router.get("/reference-recipes", response_model=List[ReferenceRecipe])
async def get_reference_recipes(
    country_id: Optional[str] = None,
    featured_only: bool = False,
    category: Optional[str] = None
):
    """Get reference recipes with optional filtering"""
    recipes = REFERENCE_RECIPES.copy()
    
    if country_id:
        recipes = [r for r in recipes if r.country_id == country_id]
    
    if featured_only:
        recipes = [r for r in recipes if r.is_featured]
    
    if category:
        recipes = [r for r in recipes if r.category == category]
    
    # Sort by popularity
    recipes.sort(key=lambda x: x.popularity_score, reverse=True)
    
    return recipes

@api_router.get("/reference-recipes/{recipe_id}", response_model=ReferenceRecipe)
async def get_reference_recipe(recipe_id: str):
    """Get a specific reference recipe"""
    recipe = next((r for r in REFERENCE_RECIPES if r.id == recipe_id), None)
    if not recipe:
        raise HTTPException(status_code=404, detail="Reference recipe not found")
    return recipe

@api_router.get("/countries/{country_id}/reference-recipes", response_model=List[ReferenceRecipe])
async def get_country_reference_recipes(country_id: str):
    """Get all reference recipes for a specific country"""
    recipes = get_recipes_by_country(country_id)
    return sorted(recipes, key=lambda x: x.popularity_score, reverse=True)

# Recipe Snippets Routes
@api_router.post("/snippets", response_model=SnippetResponse)
async def create_snippet(
    snippet_data: SnippetCreate,
    current_user_id: str = Depends(get_current_user)
):
    """Create a new recipe snippet"""
    snippet_dict = snippet_data.dict()
    snippet_dict['author_id'] = current_user_id
    
    # Get user's country for context
    user = await db.users.find_one({"id": current_user_id})
    if user:
        snippet_dict['country_id'] = user.get('country_id')
        snippet_dict['region_id'] = user.get('region_id')
    
    # Determine playlist order
    user_snippets_count = await db.snippets.count_documents({"author_id": current_user_id})
    snippet_dict['playlist_order'] = user_snippets_count + 1
    
    snippet = RecipeSnippet(**snippet_dict)
    await db.snippets.insert_one(snippet.dict())
    
    # Update user's snippet count
    await db.users.update_one(
        {"id": current_user_id},
        {"$inc": {"snippets_count": 1}}
    )
    
    # Get author info
    author = await db.users.find_one({"id": current_user_id})
    
    response_dict = snippet.dict()
    response_dict['author_username'] = author['username'] if author else None
    
    return SnippetResponse(**response_dict)

@api_router.get("/snippets", response_model=List[SnippetResponse])
async def get_snippets(
    skip: int = 0,
    limit: int = 20,
    author_id: Optional[str] = None,
    country_id: Optional[str] = None,
    snippet_type: Optional[SnippetType] = None
):
    """Get snippets with optional filtering"""
    query = {}
    
    if author_id:
        query["author_id"] = author_id
    if country_id:
        query["country_id"] = country_id
    if snippet_type:
        query["snippet_type"] = snippet_type
    
    snippets_cursor = db.snippets.find(query).sort("created_at", -1).skip(skip).limit(limit)
    snippets = await snippets_cursor.to_list(length=limit)
    
    # Get author info for each snippet
    result = []
    for snippet in snippets:
        author = await db.users.find_one({"id": snippet["author_id"]})
        snippet_response = SnippetResponse(**snippet)
        snippet_response.author_username = author['username'] if author else None
        result.append(snippet_response)
    
    return result

@api_router.get("/users/{user_id}/snippets/playlist", response_model=List[SnippetResponse])
async def get_user_snippets_playlist(user_id: str):
    """Get user's snippets organized as a playlist"""
    snippets_cursor = db.snippets.find({
        "author_id": user_id,
        "is_featured_in_profile": True
    }).sort("playlist_order", 1)
    
    snippets = await snippets_cursor.to_list(length=100)
    
    # Get author info
    author = await db.users.find_one({"id": user_id})
    
    result = []
    for snippet in snippets:
        snippet_response = SnippetResponse(**snippet)
        snippet_response.author_username = author['username'] if author else None
        result.append(snippet_response)
    
    return result

@api_router.post("/snippets/{snippet_id}/like")
async def like_snippet(snippet_id: str, current_user_id: str = Depends(get_current_user)):
    """Like or unlike a snippet"""
    snippet = await db.snippets.find_one({"id": snippet_id})
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    # Check if already liked
    existing_like = await db.snippet_interactions.find_one({
        "snippet_id": snippet_id,
        "user_id": current_user_id,
        "interaction_type": "like"
    })
    
    if existing_like:
        # Unlike
        await db.snippet_interactions.delete_one({"id": existing_like["id"]})
        await db.snippets.update_one({"id": snippet_id}, {"$inc": {"likes_count": -1}})
        return {"liked": False}
    else:
        # Like
        interaction = {
            "id": str(uuid.uuid4()),
            "snippet_id": snippet_id,
            "user_id": current_user_id,
            "interaction_type": "like",
            "created_at": datetime.utcnow()
        }
        await db.snippet_interactions.insert_one(interaction)
        await db.snippets.update_one({"id": snippet_id}, {"$inc": {"likes_count": 1}})
        return {"liked": True}

# Grocery Store Integration Routes
@api_router.post("/grocery/search", response_model=GrocerySearchResponse)
async def search_grocery_stores(
    search_request: GrocerySearchRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Search for grocery stores and ingredient availability based on user location"""
    
    # This is a mock implementation - in production, you'd integrate with actual grocery APIs
    # like Instacart, Amazon Fresh, or regional grocery chains
    
    # Mock grocery stores data
    mock_stores = [
        {
            "id": "store_1",
            "name": "Fresh Market",
            "chain": "Independent",
            "address": "123 Main St",
            "distance_km": 2.5,
            "supports_delivery": True,
            "estimated_total": 25.99,
            "commission_rate": 0.05
        },
        {
            "id": "store_2", 
            "name": "Whole Foods",
            "chain": "Whole Foods Market",
            "address": "456 Oak Ave",
            "distance_km": 4.2,
            "supports_delivery": True,
            "estimated_total": 32.50,
            "commission_rate": 0.08
        },
        {
            "id": "store_3",
            "name": "Kroger",
            "chain": "Kroger",
            "address": "789 Pine St",
            "distance_km": 3.1,
            "supports_delivery": True,
            "estimated_total": 22.75,
            "commission_rate": 0.06
        }
    ]
    
    # Mock ingredient availability
    mock_availability = {}
    for ingredient in search_request.ingredients:
        mock_availability[ingredient] = [
            {
                "store_id": "store_1",
                "brand": "Generic",
                "price": 2.99,
                "in_stock": True,
                "package_size": "1 lb"
            },
            {
                "store_id": "store_2",
                "brand": "Organic",
                "price": 4.99,
                "in_stock": True,
                "package_size": "1 lb"
            }
        ]
    
    # Mock delivery options
    delivery_options = [
        {
            "type": "pickup",
            "fee": 0.0,
            "time_estimate": "Ready in 2 hours"
        },
        {
            "type": "delivery",
            "fee": 5.99,
            "time_estimate": "Delivered in 1-2 hours"
        }
    ]
    
    return GrocerySearchResponse(
        stores=mock_stores,
        ingredient_availability=mock_availability,
        total_estimated_cost=25.99,
        delivery_options=delivery_options,
        recommended_store_id="store_1"
    )

@api_router.get("/grocery/stores/nearby")
async def get_nearby_stores(
    postal_code: str,
    radius_km: float = 10.0,
    current_user_id: str = Depends(get_current_user)
):
    """Get grocery stores near a postal code"""
    
    # Mock nearby stores - in production, use geospatial queries
    nearby_stores = [
        {
            "id": "store_1",
            "name": "Fresh Market",
            "address": "123 Main St",
            "distance_km": 2.5,
            "phone": "(555) 123-4567",
            "supports_delivery": True,
            "is_partner": True
        },
        {
            "id": "store_2",
            "name": "Whole Foods",
            "address": "456 Oak Ave", 
            "distance_km": 4.2,
            "phone": "(555) 987-6543",
            "supports_delivery": True,
            "is_partner": True
        }
    ]
    
    return {"stores": nearby_stores, "search_radius_km": radius_km}

# User preferences for grocery shopping
@api_router.post("/users/grocery-preferences")
async def update_grocery_preferences(
    preferences: UserGroceryPreference,
    current_user_id: str = Depends(get_current_user)
):
    """Update user's grocery shopping preferences"""
    preferences.user_id = current_user_id
    preferences.updated_at = datetime.utcnow()
    
    # Upsert preferences
    await db.user_grocery_preferences.update_one(
        {"user_id": current_user_id},
        {"$set": preferences.dict()},
        upsert=True
    )
    
    return {"message": "Grocery preferences updated successfully"}

@api_router.get("/users/me/grocery-preferences", response_model=UserGroceryPreference)
async def get_grocery_preferences(current_user_id: str = Depends(get_current_user)):
    """Get user's grocery shopping preferences"""
    preferences = await db.user_grocery_preferences.find_one({"user_id": current_user_id})
    
    if not preferences:
        # Return default preferences
        return UserGroceryPreference(user_id=current_user_id)
    
    return UserGroceryPreference(**preferences)

# Enhanced user profile
@api_router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user_id: str = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user_doc)

# Countries endpoint (same as before)
@api_router.get("/countries", response_model=List[Country])
async def get_countries():
    countries = await db.countries.find().to_list(1000)
    return [Country(**country) for country in countries]

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow(), "version": "2.0-enhanced"}

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
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.snippets.create_index([("created_at", -1)])
    await db.snippets.create_index("author_id")
    await db.snippets.create_index([("author_id", 1), ("playlist_order", 1)])
    await db.snippet_interactions.create_index([("snippet_id", 1), ("user_id", 1)])
    
    # Insert sample countries if none exist
    countries_count = await db.countries.count_documents({})
    if countries_count == 0:
        sample_countries = [
            Country(
                name="United States", code="US",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "California"},
                    {"id": str(uuid.uuid4()), "name": "Texas"},
                    {"id": str(uuid.uuid4()), "name": "New York"}
                ],
                languages=["en", "es"]
            ),
            Country(
                name="Italy", code="IT",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Tuscany"},
                    {"id": str(uuid.uuid4()), "name": "Sicily"},
                    {"id": str(uuid.uuid4()), "name": "Lombardy"}
                ],
                languages=["it"]
            ),
            Country(
                name="Mexico", code="MX", 
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Oaxaca"},
                    {"id": str(uuid.uuid4()), "name": "Yucatan"},
                    {"id": str(uuid.uuid4()), "name": "Mexico City"}
                ],
                languages=["es"]
            ),
            Country(
                name="Japan", code="JP",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Tokyo"},
                    {"id": str(uuid.uuid4()), "name": "Osaka"},
                    {"id": str(uuid.uuid4()), "name": "Kyoto"}
                ],
                languages=["ja"]
            ),
            Country(
                name="India", code="IN",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Punjab"},
                    {"id": str(uuid.uuid4()), "name": "Kerala"},
                    {"id": str(uuid.uuid4()), "name": "Rajasthan"}
                ],
                languages=["hi", "en"]
            )
        ]
        
        for country in sample_countries:
            await db.countries.insert_one(country.dict())

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()