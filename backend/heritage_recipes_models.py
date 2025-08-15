# Heritage Recipes & Specialty Ingredients - Afro-Caribbean Cultural Preservation
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid

class CountryRegion(str, Enum):
    # Caribbean Islands
    JAMAICA = "jamaica"
    TRINIDAD_TOBAGO = "trinidad_tobago"
    BARBADOS = "barbados"
    HAITI = "haiti"
    DOMINICAN_REPUBLIC = "dominican_republic"
    PUERTO_RICO = "puerto_rico"
    CUBA = "cuba"
    GRENADA = "grenada"
    ST_LUCIA = "st_lucia"
    MARTINIQUE = "martinique"
    GUADELOUPE = "guadeloupe"
    ANTIGUA_BARBUDA = "antigua_barbuda"
    ST_VINCENT_GRENADINES = "st_vincent_grenadines"
    DOMINICA = "dominica"
    ST_KITTS_NEVIS = "st_kitts_nevis"
    
    # African Heritage Regions
    WEST_AFRICA = "west_africa"
    NIGERIA = "nigeria"
    GHANA = "ghana"
    SENEGAL = "senegal"
    MALI = "mali"
    BURKINA_FASO = "burkina_faso"
    IVORY_COAST = "ivory_coast"
    CENTRAL_AFRICA = "central_africa"
    CAMEROON = "cameroon"
    CONGO = "congo"
    EAST_AFRICA = "east_africa"
    ETHIOPIA = "ethiopia"
    SUDAN = "sudan"
    KENYA = "kenya"
    TANZANIA = "tanzania"
    UGANDA = "uganda"
    ERITREA = "eritrea"
    SOMALIA = "somalia"
    
    # Asian Heritage Regions
    CHINA = "china"
    JAPAN = "japan"
    KOREA = "korea"
    VIETNAM = "vietnam"
    THAILAND = "thailand"
    CAMBODIA = "cambodia"
    LAOS = "laos"
    MYANMAR = "myanmar"
    PHILIPPINES = "philippines"
    INDONESIA = "indonesia"
    MALAYSIA = "malaysia"
    SINGAPORE = "singapore"
    INDIA = "india"
    PAKISTAN = "pakistan"
    BANGLADESH = "bangladesh"
    SRI_LANKA = "sri_lanka"
    NEPAL = "nepal"
    BHUTAN = "bhutan"
    
    # Middle Eastern & Central Asian
    TURKEY = "turkey"
    IRAN = "iran"
    IRAQ = "iraq"
    SYRIA = "syria"
    LEBANON = "lebanon"
    JORDAN = "jordan"
    AFGHANISTAN = "afghanistan"
    UZBEKISTAN = "uzbekistan"
    KAZAKHSTAN = "kazakhstan"
    ARMENIA = "armenia"
    GEORGIA = "georgia"
    AZERBAIJAN = "azerbaijan"
    
    # Latin American
    MEXICO = "mexico"
    GUATEMALA = "guatemala"
    HONDURAS = "honduras"
    EL_SALVADOR = "el_salvador"
    NICARAGUA = "nicaragua"
    COSTA_RICA = "costa_rica"
    PANAMA = "panama"
    COLOMBIA = "colombia"
    VENEZUELA = "venezuela"
    ECUADOR = "ecuador"
    PERU = "peru"
    BOLIVIA = "bolivia"
    CHILE = "chile"
    ARGENTINA = "argentina"
    URUGUAY = "uruguay"
    PARAGUAY = "paraguay"
    BRAZIL = "brazil"
    
    # European Heritage
    ITALY = "italy"
    SPAIN = "spain"
    PORTUGAL = "portugal"
    FRANCE = "france"
    GERMANY = "germany"
    POLAND = "poland"
    RUSSIA = "russia"
    UKRAINE = "ukraine"
    GREECE = "greece"
    ROMANIA = "romania"
    HUNGARY = "hungary"
    CZECH_REPUBLIC = "czech_republic"
    SLOVAKIA = "slovakia"
    CROATIA = "croatia"
    SERBIA = "serbia"
    BOSNIA = "bosnia"
    ALBANIA = "albania"
    BULGARIA = "bulgaria"
    LITHUANIA = "lithuania"
    LATVIA = "latvia"
    ESTONIA = "estonia"
    FINLAND = "finland"
    SWEDEN = "sweden"
    NORWAY = "norway"
    DENMARK = "denmark"
    NETHERLANDS = "netherlands"
    BELGIUM = "belgium"
    SWITZERLAND = "switzerland"
    AUSTRIA = "austria"
    IRELAND = "ireland"
    SCOTLAND = "scotland"
    WALES = "wales"
    
    # Pacific & Oceania
    AUSTRALIA = "australia"
    NEW_ZEALAND = "new_zealand"
    FIJI = "fiji"
    SAMOA = "samoa"
    TONGA = "tonga"
    HAWAII = "hawaii"
    
    # Diaspora Communities
    USA_SOUTH = "usa_south"
    USA_SOUTHWEST = "usa_southwest"
    USA_NORTHEAST = "usa_northeast"
    USA_MIDWEST = "usa_midwest"
    USA_PACIFIC = "usa_pacific"
    CANADA = "canada"
    UK = "uk"

class IngredientRarity(str, Enum):
    COMMON = "common"                    # Available in regular stores
    SPECIALTY = "specialty"              # Ethnic grocery stores only
    RARE = "rare"                       # Hard to find, specific suppliers
    SEASONAL = "seasonal"               # Available certain times of year
    IMPORTED_ONLY = "imported_only"     # Must be imported, very specialized
    ENDANGERED = "endangered"           # Traditional varieties at risk

class CulturalSignificance(str, Enum):
    EVERYDAY = "everyday"               # Regular family meals
    CELEBRATION = "celebration"         # Special occasions, holidays
    CEREMONIAL = "ceremonial"          # Religious or cultural ceremonies
    HERITAGE = "heritage"              # Passed down through generations
    SEASONAL_TRADITION = "seasonal"    # Specific seasons or festivals
    DIASPORA_COMFORT = "diaspora"      # Comfort food for diaspora communities

class AuthenticityLevel(str, Enum):
    TRADITIONAL = "traditional"         # Original, unchanged recipe
    ADAPTED = "adapted"                # Modified for available ingredients
    FUSION = "fusion"                  # Combined with other cuisines
    MODERN = "modern"                  # Contemporary interpretation
    DIASPORA_VERSION = "diaspora"      # Adapted for diaspora communities

# HERITAGE RECIPE MODELS

class HeritageRecipe(BaseModel):
    """Traditional heritage recipes from all global communities with cultural context"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Recipe Identity
    recipe_name: str = Field(..., min_length=3, max_length=150)
    recipe_name_local: Optional[str] = None  # In local language/dialect
    recipe_name_pronunciation: Optional[str] = None  # Phonetic pronunciation
    
    # Cultural Context
    country_region: CountryRegion
    cultural_significance: CulturalSignificance
    authenticity_level: AuthenticityLevel
    historical_context: Optional[str] = None  # Story behind the dish
    family_story: Optional[str] = None        # Personal/family connection
    
    # Recipe Details
    description: str = Field(..., max_length=1000)
    description_local: Optional[str] = None   # In local language
    traditional_occasion: Optional[str] = None # When it's traditionally made
    regional_variations: List[str] = []       # Different ways it's made
    
    # Ingredients with Specialty Focus
    traditional_ingredients: List[Dict[str, Any]] = []  # Original recipe ingredients
    substitute_ingredients: List[Dict[str, Any]] = []   # Modern substitutions
    specialty_ingredients: List[str] = []               # Hard-to-find ingredients
    
    # Cooking Instructions
    preparation_steps: List[str] = []
    cooking_method: str = ""                  # Traditional cooking method
    modern_adaptations: List[str] = []        # Modern kitchen adaptations
    special_techniques: List[str] = []        # Traditional techniques
    
    # Nutritional & Serving Info
    servings: int = Field(default=4, ge=1, le=20)
    prep_time_minutes: int = Field(default=30, ge=5, le=480)
    cook_time_minutes: int = Field(default=60, ge=5, le=480)
    difficulty_level: int = Field(default=3, ge=1, le=5)
    
    # Cultural Preservation
    contributor_info: Dict[str, str] = {}     # Who shared this recipe
    source_verification: Optional[str] = None # How authenticity was verified
    elder_approved: bool = False              # Approved by community elders
    community_ratings: Dict[str, float] = {} # Authenticity ratings
    
    # Ingredient Sourcing
    where_to_buy_ingredients: List[Dict[str, str]] = []  # Store recommendations
    ingredient_alternatives: Dict[str, str] = {}         # Substitution guide
    seasonal_availability: Dict[str, str] = {}           # When ingredients available
    
    # Media & Documentation  
    recipe_photos: List[str] = []
    preparation_videos: List[str] = []
    cultural_context_media: List[str] = []    # Historical photos, stories
    
    # Community Engagement
    likes_count: int = 0
    saves_count: int = 0
    shares_count: int = 0
    comments_count: int = 0
    tried_count: int = 0                      # How many people tried it
    
    # Metadata
    created_by: str                           # User ID who contributed
    verified_by: Optional[str] = None         # Cultural expert verification
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_public: bool = True
    preservation_priority: int = Field(default=3, ge=1, le=5)  # How important to preserve

class SpecialtyIngredient(BaseModel):
    """Database of hard-to-find heritage ingredients from all global communities"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Ingredient Identity
    ingredient_name: str = Field(..., min_length=2, max_length=100)
    ingredient_name_local: Optional[str] = None  # Local/traditional name
    scientific_name: Optional[str] = None        # Botanical/scientific name
    alternative_names: List[str] = []            # Other names it's known by
    
    # Origin & Cultural Context
    origin_countries: List[CountryRegion] = []
    cultural_uses: List[str] = []                # How it's used culturally
    traditional_preparation: List[str] = []       # Traditional prep methods
    
    # Availability & Sourcing
    rarity_level: IngredientRarity
    typical_price_range: Dict[str, float] = {}   # Price ranges by location
    seasonal_availability: Dict[str, str] = {}   # When available by region
    shelf_life: Optional[str] = None             # How long it lasts
    storage_requirements: List[str] = []         # How to store properly
    
    # Substitutions & Alternatives
    common_substitutes: List[Dict[str, str]] = [] # What can replace it
    substitution_ratio: Dict[str, str] = {}      # How much to use instead
    flavor_profile: List[str] = []               # Taste characteristics
    
    # Sourcing Information
    available_at_stores: List[str] = []          # Store IDs where found
    online_suppliers: List[Dict[str, str]] = []  # Online sources
    import_requirements: Optional[str] = None     # If needs special import
    
    # Nutritional & Health
    nutritional_benefits: List[str] = []
    traditional_medicinal_uses: List[str] = []
    allergen_information: List[str] = []
    
    # Media & Documentation
    ingredient_photos: List[str] = []
    preparation_videos: List[str] = []
    
    # Community Data
    recipes_using: List[str] = []                # Recipe IDs that use this
    user_reviews: List[Dict[str, Any]] = []      # User experiences
    difficulty_to_find: float = Field(default=3.0, ge=1.0, le=5.0)
    
    # Metadata
    added_by: str                                # User who added this ingredient
    verified_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EthnicGroceryStore(BaseModel):
    """Specialty grocery stores serving Afro-Caribbean communities"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Store Information
    store_name: str = Field(..., min_length=2, max_length=100)
    store_type: str = "ethnic_grocery"  # "ethnic_grocery", "caribbean_market", "african_store", "specialty_importer"
    specialties: List[CountryRegion] = []        # Which cuisines they focus on
    
    # Contact & Location
    address: str
    city: str
    state_province: str
    country: str
    postal_code: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Geographic Data
    location: Dict[str, float] = {}              # {"lat": x, "lng": y}
    service_radius_km: float = Field(default=50.0, ge=1.0, le=200.0)
    
    # Store Details
    operating_hours: Dict[str, str] = {}         # Daily hours
    languages_spoken: List[str] = []             # Languages staff speaks
    payment_methods: List[str] = []              # Accepted payments
    
    # Inventory & Services
    specialty_ingredients: List[str] = []         # Ingredient IDs they carry
    available_products: List[Dict[str, Any]] = [] # Current inventory
    seasonal_items: Dict[str, List[str]] = {}    # Seasonal availability
    special_orders: bool = False                 # Can they special order items
    shipping_available: bool = False             # Do they ship
    
    # Community Connection
    community_events: List[Dict[str, str]] = []  # Cultural events they host
    cooking_classes: bool = False                # Do they offer classes
    recipe_consultations: bool = False           # Help with traditional recipes
    elder_connections: List[str] = []            # Community elders who shop there
    
    # Platform Integration
    verified_by_community: bool = False
    community_rating: float = Field(default=5.0, ge=1.0, le=5.0)
    reviews: List[Dict[str, Any]] = []
    recommended_by: List[str] = []               # User IDs who recommended
    
    # Business Info
    owner_background: Optional[str] = None       # Owner's cultural background
    years_in_business: Optional[int] = None
    family_owned: bool = False
    community_involvement: List[str] = []
    
    # Metadata
    added_by: str
    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class CulturalContributor(BaseModel):
    """Community members who contribute authentic recipes and knowledge"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Cultural Background
    cultural_heritage: List[CountryRegion] = []
    generation_in_diaspora: int = Field(default=1, ge=1, le=5)  # 1st, 2nd gen, etc.
    languages_spoken: List[str] = []
    
    # Expertise
    specialty_cuisines: List[CountryRegion] = []
    family_recipes_count: int = 0
    verified_recipes: int = 0
    community_recognition: str = "contributor"  # "contributor", "expert", "elder", "cultural_keeper"
    
    # Contributions
    recipes_contributed: List[str] = []          # Recipe IDs
    ingredients_documented: List[str] = []       # Ingredient IDs
    stores_recommended: List[str] = []           # Store IDs
    
    # Verification
    community_vouchers: List[str] = []           # Other contributors who vouch
    elder_endorsement: bool = False
    cultural_organization_member: Optional[str] = None
    
    # Recognition
    contribution_score: float = 0.0
    badges_earned: List[str] = []
    featured_contributor: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HeritageCollection(BaseModel):
    """Curated collections of recipes by theme, country, or occasion"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Collection Info
    collection_name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., max_length=500)
    theme: str  # "country_spotlight", "holiday_traditions", "endangered_recipes", "diaspora_comfort"
    
    # Cultural Context
    featured_country: Optional[CountryRegion] = None
    cultural_significance: CulturalSignificance
    historical_period: Optional[str] = None
    
    # Content
    recipe_ids: List[str] = []
    featured_ingredients: List[str] = []
    recommended_stores: List[str] = []
    cultural_context_articles: List[Dict[str, str]] = []
    
    # Curation
    curated_by: str                              # User ID of curator
    community_approved: bool = False
    elder_reviewed: bool = False
    
    # Engagement
    followers: int = 0
    saves: int = 0
    shares: int = 0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_featured: bool = False

# REQUEST/RESPONSE MODELS

class HeritageRecipeSubmission(BaseModel):
    recipe_name: str = Field(..., min_length=3, max_length=150)
    recipe_name_local: Optional[str] = None
    country_region: str
    cultural_significance: str
    description: str = Field(..., max_length=1000)
    traditional_ingredients: List[Dict[str, Any]] = []
    preparation_steps: List[str] = []
    family_story: Optional[str] = None
    historical_context: Optional[str] = None
    contributor_background: str = ""

class IngredientSourceRequest(BaseModel):
    ingredient_name: str
    user_location: Dict[str, float]
    search_radius_km: float = 50.0
    include_online: bool = True
    preferred_price_range: Optional[Dict[str, float]] = None

class StoreRecommendationRequest(BaseModel):
    country_cuisine: CountryRegion
    user_location: Dict[str, float] 
    search_radius_km: float = 25.0
    specialties_needed: List[str] = []

class CulturalVerificationRequest(BaseModel):
    recipe_id: str
    verifier_credentials: str
    authenticity_rating: float = Field(ge=1.0, le=5.0)
    verification_notes: str
    suggested_corrections: List[str] = []

# RESPONSE MODELS

class HeritageRecipeResponse(BaseModel):
    id: str
    recipe_name: str
    recipe_name_local: Optional[str]
    country_region: str
    cultural_significance: str
    description: str
    ingredient_availability: Dict[str, str]  # Where to find each ingredient
    nearby_stores: List[Dict[str, Any]]      # Stores that have ingredients
    authenticity_score: float
    community_rating: float
    contributor_info: Dict[str, str]

class IngredientAvailabilityResponse(BaseModel):
    ingredient_name: str
    rarity_level: str
    nearest_stores: List[Dict[str, Any]]
    online_sources: List[Dict[str, str]]
    average_price: float
    substitutes: List[Dict[str, str]]
    seasonal_info: str

class CulturalCollectionResponse(BaseModel):
    collection_name: str
    description: str
    recipe_count: int
    featured_recipes: List[HeritageRecipeResponse]
    cultural_context: str
    difficulty_to_complete: str  # How hard to make all recipes
    estimated_cost: float        # Cost to buy all ingredients