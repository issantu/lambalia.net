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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="CulinaryConnect API", description="Social Media Platform for Recipe Sharing")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(days=7)

# Enums
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

# Models
class Country(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str  # ISO country code
    regions: List[Dict[str, str]] = []  # [{"id": "uuid", "name": "region_name"}]
    languages: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    password_hash: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_photo: Optional[str] = None  # base64 or URL
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    location: Optional[Dict[str, float]] = None  # {"lat": 0.0, "lng": 0.0}
    postal_code: Optional[str] = None
    preferred_language: str = "en"
    dietary_preferences: List[DietaryPreference] = []
    followers_count: int = 0
    following_count: int = 0
    recipes_count: int = 0
    credits: float = 0.0
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    ingredients: List[Dict[str, Any]]  # [{"name": "tomato", "amount": "2", "unit": "pcs", "local_price": 0.0}]
    steps: List[Dict[str, str]]  # [{"step_number": 1, "description": "Cut tomatoes", "image": ""}]
    cooking_time_minutes: Optional[int] = None
    difficulty_level: int = Field(ge=1, le=5, default=3)
    servings: Optional[int] = None
    cuisine_type: Optional[str] = None
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    dietary_preferences: List[DietaryPreference] = []
    tags: List[str] = []
    main_image: Optional[str] = None  # base64 or URL
    additional_images: List[str] = []
    author_id: str
    status: RecipeStatus = RecipeStatus.PUBLISHED
    is_premium: bool = False  # True if ingredients are hidden
    premium_price: float = 0.0  # Credits needed to unlock ingredients
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RecipeInteraction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recipe_id: str
    user_id: str
    interaction_type: str  # "like", "comment", "share", "view", "purchase"
    content: Optional[str] = None  # For comments
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserFollow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    follower_id: str
    following_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    country_id: Optional[str] = None
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
    preferred_language: str
    followers_count: int
    following_count: int
    recipes_count: int
    credits: float
    is_verified: bool
    created_at: datetime

class RecipeCreate(BaseModel):
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
    is_premium: bool = False
    premium_price: float = 0.0

class RecipeResponse(BaseModel):
    id: str
    title: str
    description: str
    ingredients: Optional[List[Dict[str, Any]]] = None  # Hidden if premium and not purchased
    steps: List[Dict[str, str]]
    cooking_time_minutes: Optional[int] = None
    difficulty_level: int
    servings: Optional[int] = None
    cuisine_type: Optional[str] = None
    dietary_preferences: List[DietaryPreference]
    tags: List[str]
    main_image: Optional[str] = None
    author_id: str
    author_username: Optional[str] = None
    is_premium: bool
    premium_price: float
    is_purchased: bool = False
    likes_count: int
    comments_count: int
    shares_count: int
    views_count: int
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
        
        # Verify user exists
        user = await db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Authentication Routes
@api_router.post("/auth/register", response_model=TokenResponse)
async def register_user(user_data: UserRegistration):
    # Check if user already exists
    existing_user = await db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user
    user_dict = user_data.dict()
    user_dict['password_hash'] = hash_password(user_data.password)
    del user_dict['password']
    
    user = UserProfile(**user_dict)
    await db.users.insert_one(user.dict())
    
    # Create token
    token = create_jwt_token(user.id)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user.dict())
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin):
    # Find user
    user_doc = await db.users.find_one({"email": login_data.email})
    if not user_doc or not verify_password(login_data.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_jwt_token(user_doc['id'])
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user_doc)
    )

# User Routes
@api_router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user_id: str = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user_doc)

@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str):
    user_doc = await db.users.find_one({"id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user_doc)

# Recipe Routes
@api_router.post("/recipes", response_model=RecipeResponse)
async def create_recipe(
    recipe_data: RecipeCreate,
    current_user_id: str = Depends(get_current_user)
):
    recipe_dict = recipe_data.dict()
    recipe_dict['author_id'] = current_user_id
    
    recipe = Recipe(**recipe_dict)
    await db.recipes.insert_one(recipe.dict())
    
    # Update user's recipe count
    await db.users.update_one(
        {"id": current_user_id},
        {"$inc": {"recipes_count": 1}}
    )
    
    # Get author info
    author = await db.users.find_one({"id": current_user_id})
    
    response_dict = recipe.dict()
    response_dict['author_username'] = author['username'] if author else None
    response_dict['is_purchased'] = False
    
    return RecipeResponse(**response_dict)

@api_router.get("/recipes", response_model=List[RecipeResponse])
async def get_recipes(
    skip: int = 0,
    limit: int = 20,
    country_id: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    dietary_preference: Optional[str] = None,
    current_user_id: str = None
):
    # Build query
    query = {"status": RecipeStatus.PUBLISHED}
    if country_id:
        query["country_id"] = country_id
    if cuisine_type:
        query["cuisine_type"] = cuisine_type
    if dietary_preference:
        query["dietary_preferences"] = {"$in": [dietary_preference]}
    
    # Get recipes
    recipes_cursor = db.recipes.find(query).sort("created_at", -1).skip(skip).limit(limit)
    recipes = await recipes_cursor.to_list(length=limit)
    
    # Get author info and check purchase status
    result = []
    for recipe in recipes:
        author = await db.users.find_one({"id": recipe["author_id"]})
        recipe_response = RecipeResponse(**recipe)
        recipe_response.author_username = author['username'] if author else None
        
        # Check if premium ingredients should be hidden
        if recipe_response.is_premium and current_user_id:
            # Check if user has purchased this recipe
            purchase = await db.recipe_interactions.find_one({
                "recipe_id": recipe["id"],
                "user_id": current_user_id,
                "interaction_type": "purchase"
            })
            recipe_response.is_purchased = purchase is not None
            
            if not recipe_response.is_purchased:
                recipe_response.ingredients = None
        elif recipe_response.is_premium:
            recipe_response.ingredients = None
            
        result.append(recipe_response)
    
    return result

@api_router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: str, current_user_id: Optional[str] = Depends(lambda: None)):
    recipe_doc = await db.recipes.find_one({"id": recipe_id})
    if not recipe_doc:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Increment view count
    await db.recipes.update_one({"id": recipe_id}, {"$inc": {"views_count": 1}})
    
    # Get author info
    author = await db.users.find_one({"id": recipe_doc["author_id"]})
    
    recipe_response = RecipeResponse(**recipe_doc)
    recipe_response.author_username = author['username'] if author else None
    
    # Check premium access
    if recipe_response.is_premium and current_user_id:
        purchase = await db.recipe_interactions.find_one({
            "recipe_id": recipe_id,
            "user_id": current_user_id,
            "interaction_type": "purchase"
        })
        recipe_response.is_purchased = purchase is not None
        
        if not recipe_response.is_purchased:
            recipe_response.ingredients = None
    elif recipe_response.is_premium:
        recipe_response.ingredients = None
    
    return recipe_response

@api_router.post("/recipes/{recipe_id}/like")
async def like_recipe(recipe_id: str, current_user_id: str = Depends(get_current_user)):
    # Check if recipe exists
    recipe = await db.recipes.find_one({"id": recipe_id})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if already liked
    existing_like = await db.recipe_interactions.find_one({
        "recipe_id": recipe_id,
        "user_id": current_user_id,
        "interaction_type": "like"
    })
    
    if existing_like:
        # Unlike
        await db.recipe_interactions.delete_one({"id": existing_like["id"]})
        await db.recipes.update_one({"id": recipe_id}, {"$inc": {"likes_count": -1}})
        return {"liked": False}
    else:
        # Like
        interaction = RecipeInteraction(
            recipe_id=recipe_id,
            user_id=current_user_id,
            interaction_type="like"
        )
        await db.recipe_interactions.insert_one(interaction.dict())
        await db.recipes.update_one({"id": recipe_id}, {"$inc": {"likes_count": 1}})
        return {"liked": True}

@api_router.post("/recipes/{recipe_id}/purchase")
async def purchase_recipe(recipe_id: str, current_user_id: str = Depends(get_current_user)):
    # Get recipe and user
    recipe = await db.recipes.find_one({"id": recipe_id})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if not recipe.get("is_premium"):
        raise HTTPException(status_code=400, detail="Recipe is not premium")
    
    user = await db.users.find_one({"id": current_user_id})
    if user["credits"] < recipe["premium_price"]:
        raise HTTPException(status_code=400, detail="Insufficient credits")
    
    # Check if already purchased
    existing_purchase = await db.recipe_interactions.find_one({
        "recipe_id": recipe_id,
        "user_id": current_user_id,
        "interaction_type": "purchase"
    })
    
    if existing_purchase:
        return {"message": "Recipe already purchased"}
    
    # Process purchase
    await db.users.update_one(
        {"id": current_user_id},
        {"$inc": {"credits": -recipe["premium_price"]}}
    )
    
    # Add credits to recipe author (90% of price, 10% platform fee)
    author_share = recipe["premium_price"] * 0.9
    await db.users.update_one(
        {"id": recipe["author_id"]},
        {"$inc": {"credits": author_share}}
    )
    
    # Record purchase
    purchase = RecipeInteraction(
        recipe_id=recipe_id,
        user_id=current_user_id,
        interaction_type="purchase"
    )
    await db.recipe_interactions.insert_one(purchase.dict())
    
    return {"message": "Recipe purchased successfully"}

# Country Routes  
@api_router.get("/countries", response_model=List[Country])
async def get_countries():
    countries = await db.countries.find().to_list(1000)
    return [Country(**country) for country in countries]

# Health Check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
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
    await db.recipes.create_index([("created_at", -1)])
    await db.recipes.create_index("author_id")
    await db.recipe_interactions.create_index([("recipe_id", 1), ("user_id", 1)])
    
    # Insert sample countries if none exist
    countries_count = await db.countries.count_documents({})
    if countries_count == 0:
        sample_countries = [
            Country(
                name="United States",
                code="US",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "California"},
                    {"id": str(uuid.uuid4()), "name": "Texas"},
                    {"id": str(uuid.uuid4()), "name": "New York"}
                ],
                languages=["en", "es"]
            ),
            Country(
                name="Italy", 
                code="IT",
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Tuscany"},
                    {"id": str(uuid.uuid4()), "name": "Sicily"},
                    {"id": str(uuid.uuid4()), "name": "Lombardy"}
                ],
                languages=["it"]
            ),
            Country(
                name="Mexico",
                code="MX", 
                regions=[
                    {"id": str(uuid.uuid4()), "name": "Oaxaca"},
                    {"id": str(uuid.uuid4()), "name": "Yucatan"},
                    {"id": str(uuid.uuid4()), "name": "Mexico City"}
                ],
                languages=["es"]
            )
        ]
        
        for country in sample_countries:
            await db.countries.insert_one(country.dict())

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()