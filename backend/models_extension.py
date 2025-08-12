# Extended models for Lambalia enhanced features
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

class SnippetType(str, Enum):
    QUICK_RECIPE = "quick_recipe"
    COOKING_TIP = "cooking_tip"
    INGREDIENT_SPOTLIGHT = "ingredient_spotlight"
    TRADITIONAL_METHOD = "traditional_method"

class VideoQuality(str, Enum):
    LOW = "360p"
    MEDIUM = "720p"
    HIGH = "1080p"

class ReferenceRecipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name_english: str
    name_local: str
    local_language: str
    country_id: str
    region_id: Optional[str] = None
    description: str
    category: str  # "appetizer", "main", "dessert", "beverage"
    difficulty_level: int = Field(ge=1, le=5)
    estimated_time: int  # minutes
    serving_size: str
    key_ingredients: List[str]
    cultural_significance: str
    image_url: Optional[str] = None
    is_featured: bool = False
    popularity_score: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RecipeSnippet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    title_local: Optional[str] = None
    local_language: Optional[str] = None
    description: str
    snippet_type: SnippetType = SnippetType.QUICK_RECIPE
    
    # Reference to template (if based on reference recipe)
    reference_recipe_id: Optional[str] = None
    
    # Media content
    main_image: Optional[str] = None  # base64 or URL
    video_url: Optional[str] = None   # Short video of finished product
    video_duration: Optional[int] = None  # seconds
    video_quality: VideoQuality = VideoQuality.MEDIUM
    
    # Recipe content
    ingredients: List[Dict[str, Any]]
    preparation_steps: List[Dict[str, str]]  # Brief, numbered steps
    cooking_time_minutes: int
    difficulty_level: int = Field(ge=1, le=5)
    servings: int
    
    # User and location
    author_id: str
    country_id: Optional[str] = None
    region_id: Optional[str] = None
    
    # Engagement metrics
    views_count: int = 0
    likes_count: int = 0
    saves_count: int = 0
    shares_count: int = 0
    
    # Playlist and organization
    playlist_order: int = 0
    is_featured_in_profile: bool = True
    tags: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GroceryStore(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    chain: Optional[str] = None  # e.g., "Walmart", "Kroger"
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    
    # Location data
    latitude: float
    longitude: float
    
    # Contact and operations
    phone: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Dict[str, str] = {}  # {"monday": "8:00-22:00", ...}
    
    # Services
    supports_delivery: bool = False
    supports_pickup: bool = True
    delivery_radius_km: Optional[float] = None
    average_delivery_time: Optional[int] = None  # minutes
    
    # Lambalia integration
    is_partner: bool = False
    commission_rate: float = 0.0  # Percentage for monetization
    api_endpoint: Optional[str] = None
    last_inventory_update: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class IngredientAvailability(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ingredient_name: str
    grocery_store_id: str
    
    # Product details
    brand: Optional[str] = None
    package_size: str
    unit_price: float
    currency: str = "USD"
    
    # Availability
    in_stock: bool = True
    stock_level: str = "high"  # high, medium, low, out_of_stock
    estimated_restock: Optional[datetime] = None
    
    # Alternative suggestions
    substitute_ingredients: List[str] = []
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserGroceryPreference(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    preferred_stores: List[str] = []  # List of grocery store IDs
    max_distance_km: float = 10.0
    budget_preference: str = "medium"  # "low", "medium", "high"
    dietary_restrictions: List[str] = []
    preferred_brands: List[str] = []
    
    # Shopping behavior
    prefers_organic: bool = False
    prefers_local: bool = False
    delivery_preference: str = "pickup"  # "pickup", "delivery", "either"
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models for new features
class SnippetCreate(BaseModel):
    title: str
    title_local: Optional[str] = None
    local_language: Optional[str] = None
    description: str
    snippet_type: SnippetType = SnippetType.QUICK_RECIPE
    reference_recipe_id: Optional[str] = None
    ingredients: List[Dict[str, Any]]
    preparation_steps: List[Dict[str, str]]
    cooking_time_minutes: int
    difficulty_level: int = Field(ge=1, le=5)
    servings: int
    tags: List[str] = []
    video_duration: Optional[int] = None

class SnippetResponse(BaseModel):
    id: str
    title: str
    title_local: Optional[str] = None
    local_language: Optional[str] = None
    description: str
    snippet_type: SnippetType
    main_image: Optional[str] = None
    video_url: Optional[str] = None
    video_duration: Optional[int] = None
    ingredients: List[Dict[str, Any]]
    preparation_steps: List[Dict[str, str]]
    cooking_time_minutes: int
    difficulty_level: int
    servings: int
    author_id: str
    author_username: Optional[str] = None
    views_count: int
    likes_count: int
    saves_count: int
    playlist_order: int
    tags: List[str]
    created_at: datetime

class GrocerySearchRequest(BaseModel):
    ingredients: List[str]
    user_postal_code: str
    max_distance_km: Optional[float] = 10.0
    budget_preference: Optional[str] = "medium"
    delivery_preference: Optional[str] = "either"

class GrocerySearchResponse(BaseModel):
    stores: List[Dict[str, Any]]
    ingredient_availability: Dict[str, List[Dict[str, Any]]]
    total_estimated_cost: float
    delivery_options: List[Dict[str, Any]]
    recommended_store_id: str