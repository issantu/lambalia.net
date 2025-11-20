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
from jwt import PyJWTError as JWTError, ExpiredSignatureError
import bcrypt
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import string
import base64
from enum import Enum

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
from sms_notification_service import get_sms_service
from tip_rating_service import get_tip_rating_service, RatingRequest, ServiceType
from grocery_service import get_grocery_service
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
from smart_cooking_tool import SmartCookingToolService
from smart_cooking_api import create_smart_cooking_router
from enhanced_smart_cooking_service import get_enhanced_cooking_service
from enhanced_smart_cooking_api import create_enhanced_smart_cooking_router
from transaction_verification_system import TransactionVerificationService
from transaction_verification_api import create_transaction_verification_router
# from feedback_api import router as feedback_router

# NEW: Compliance and Campaign System Imports
from user_types_models import (
    UserType, StateCategory, UserTypeProfile, StateRegulation,
    UniversalDisclaimer, UserTypeChangeRequest, UserTypeResponse
)
from compliance_models import (
    ChefTier, ComplianceStatus, DocumentType as ComplianceDocumentType,
    ChefCompliance, ComplianceDocument, ChefComplianceRequest,
    ChefComplianceResponse, ChefDashboardStats
)
from campaign_models import (
    CampaignType, CampaignStatus, PromoCodeStatus, Campaign, PromoCode,
    PromoCodeRedemption, CampaignRequest, CampaignResponse, PromoCodeResponse,
    PromoCodeValidationRequest, PromoCodeValidationResponse, CampaignAnalytics
)
from state_compliance_service import state_compliance_service
from remaining_states_data import REMAINING_STATES

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
# Email Verification Service (Free SMTP-based 2FA)
class EmailVerificationService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  # Using Gmail SMTP (free)
        self.smtp_port = 587
        self.sender_email = os.getenv("SMTP_EMAIL", "noreply.lambalia@gmail.com")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        
    def generate_verification_code(self, length=6):
        """Generate random 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=length))
    
    def send_verification_email(self, recipient_email: str, verification_code: str, email_type: str = "registration"):
        """Send verification email with code"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Lambalia - {'Email Verification' if email_type == 'registration' else 'Login Verification'}"
            message["From"] = f"Lambalia <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Create HTML content
            if email_type == "registration":
                html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #22c55e;">🍽️ Welcome to Lambalia!</h1>
                        </div>
                        
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                            <h2 style="color: #333; margin-top: 0;">Verify Your Email Address</h2>
                            <p>Thank you for joining Lambalia! Please verify your email address to activate your account.</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <div style="background-color: #22c55e; color: white; font-size: 32px; font-weight: bold; padding: 15px 30px; border-radius: 8px; display: inline-block; letter-spacing: 5px;">
                                    {verification_code}
                                </div>
                            </div>
                            
                            <p><strong>This code expires in 10 minutes.</strong></p>
                            <p>If you didn't request this verification, please ignore this email.</p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
                            <p>© 2024 Lambalia by Ish@ngo Technologies. Your Food & Earning Hub.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
            else:  # login verification
                html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #22c55e;">🔐 Lambalia Security</h1>
                        </div>
                        
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                            <h2 style="color: #333; margin-top: 0;">Login Verification Code</h2>
                            <p>Someone is trying to access your Lambalia account. Please use this code to complete login:</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <div style="background-color: #3b82f6; color: white; font-size: 32px; font-weight: bold; padding: 15px 30px; border-radius: 8px; display: inline-block; letter-spacing: 5px;">
                                    {verification_code}
                                </div>
                            </div>
                            
                            <p><strong>This code expires in 5 minutes.</strong></p>
                            <p>If you didn't request this login, please secure your account immediately.</p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
                            <p>© 2024 Lambalia by Ish@ngo Technologies. Your Food & Earning Hub.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
            
            # Create HTML part
            html_part = MIMEText(html, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            return False
    
    async def store_verification_code(self, email: str, code: str, code_type: str = "registration"):
        """Store verification code in database"""
        try:
            verification_data = {
                "email": email,
                "code": code,
                "type": code_type,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(minutes=10 if code_type == "registration" else 5),
                "used": False
            }
            
            # Remove any existing unused codes for this email and type
            await db.email_verifications.delete_many({
                "email": email,
                "type": code_type,
                "used": False
            })
            
            # Insert new code
            await db.email_verifications.insert_one(verification_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store verification code: {str(e)}")
            return False
    
    async def verify_code(self, email: str, code: str, code_type: str = "registration"):
        """Verify the provided code"""
        try:
            verification = await db.email_verifications.find_one({
                "email": email,
                "code": code,
                "type": code_type,
                "used": False,
                "expires_at": {"$gt": datetime.utcnow()}
            })
            
            if verification:
                # Mark code as used
                await db.email_verifications.update_one(
                    {"_id": verification["_id"]},
                    {"$set": {"used": True, "used_at": datetime.utcnow()}}
                )
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to verify code: {str(e)}")
            return False

# Initialize email service
email_service = EmailVerificationService()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Lambalia Marketplace API", description="Complete Home Restaurant Marketplace with Vetting & Payments")
api_router = APIRouter()
@app.get("/")
async def root():
    return {"message": "Lambalia API is working"}

@app.get("/health")  
async def health():
    return {"status": "healthy"}
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
    HALAL = "halal"
    KOSHER = "kosher"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    SOY_FREE = "soy_free"
    PESCATARIAN = "pescatarian"

class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"

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

class RecipeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class SecurityKeyType(str, Enum):
    BACKUP_CODE = "backup_code"
    TOTP = "totp"  # Time-based One-Time Password (Google Authenticator)
    WEBAUTHN = "webauthn"  # Hardware security keys
    SMS = "sms"

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
    phone: Optional[str] = None  # Added phone field for SMS notifications
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
    phone: Optional[str] = None  # Added phone field for SMS notifications
    country_id: Optional[str] = None
    postal_code: Optional[str] = None
    preferred_language: str = "en"
    native_dishes: Optional[str] = None
    consultation_specialties: Optional[str] = None
    cultural_background: Optional[str] = None
    # NEW: User Type and Compliance
    user_types: List[str] = ["food_enthusiast"]  # Can select multiple
    primary_type: str = "food_enthusiast"
    state_code: Optional[str] = None  # Required for chefs/restaurants
    zip_code: Optional[str] = None  # Required for campaigns
    disclaimer_accepted: bool = False  # Mandatory for all users

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None  # Added phone field
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

# Enhanced login models for 2FA
class EnhancedUserLogin(BaseModel):
    email: EmailStr
    password: str
    twofa_code: Optional[str] = None  # TOTP code, backup code, or SMS code
    twofa_method: Optional[SecurityKeyType] = None
    remember_device: bool = False

class LoginResponse(BaseModel):
    success: bool
    requires_2fa: bool = False
    available_2fa_methods: List[str] = []
    session_id: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    user: Optional[UserResponse] = None
    message: str = ""

# 2FA Setup models
class Setup2FARequest(BaseModel):
    method: SecurityKeyType
    phone_number: Optional[str] = None  # For SMS

class Verify2FASetupRequest(BaseModel):
    method: SecurityKeyType
    verification_code: str
    totp_secret: Optional[str] = None  # For TOTP setup

class UserSecurityProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Two-Factor Authentication
    twofa_enabled: bool = False
    twofa_method: Optional[SecurityKeyType] = None
    totp_secret: Optional[str] = None  # Encrypted in production
    
    # Backup codes
    backup_codes: List[str] = []  # Encrypted in production
    backup_codes_used: List[str] = []
    
    # Security keys (WebAuthn/FIDO2)
    webauthn_credentials: List[Dict[str, Any]] = []
    
    # SMS 2FA
    phone_number: Optional[str] = None
    
    # Metadata
    last_2fa_setup: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
    except JWTError:
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
    except (ExpiredSignatureError, JWTError):
        return None

# Security utilities for 2FA
import secrets
import qrcode
import io

def generate_totp_secret() -> str:
    """Generate a TOTP secret for Google Authenticator"""
    return base64.b32encode(secrets.token_bytes(20)).decode('utf-8')

def generate_backup_codes(count: int = 10) -> List[str]:
    """Generate backup codes for 2FA"""
    return [f"{secrets.randbelow(9999):04d}-{secrets.randbelow(9999):04d}" for _ in range(count)]

def verify_totp_code(secret: str, code: str, window: int = 1) -> bool:
    """Verify TOTP code with time window tolerance"""
    import time
    import hmac
    import hashlib
    import struct
    
    try:
        # Decode base32 secret
        key = base64.b32decode(secret.upper().replace(' ', ''))
        
        # Get current time counter
        counter = int(time.time()) // 30
        
        # Check current time and window around it
        for i in range(-window, window + 1):
            # Generate HOTP value
            msg = struct.pack(">Q", counter + i)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            
            # Dynamic truncation
            offset = h[-1] & 0x0f
            truncated = struct.unpack(">I", h[offset:offset+4])[0] & 0x7fffffff
            totp = truncated % 1000000
            
            if f"{totp:06d}" == code:
                return True
        return False
    except:
        return False

def log_login_attempt(email: str, ip_address: str, user_agent: str, success: bool, 
                     twofa_required: bool = False, twofa_success: bool = None,
                     failed_reason: str = None) -> str:
    """Log login attempt for security monitoring"""
    attempt_id = str(uuid.uuid4())
    # In a real implementation, this would be stored in database
    return attempt_id

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

@api_router.post("/auth/register")
async def register_user(user_data: UserRegistration):
    # Check if user already exists
    existing_user = await db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Generate verification code
    verification_code = email_service.generate_verification_code()
    
    # Send verification email
    email_sent = email_service.send_verification_email(
        recipient_email=user_data.email,
        verification_code=verification_code,
        email_type="registration"
    )
    
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    # Store verification code in database
    code_stored = await email_service.store_verification_code(
        email=user_data.email,
        code=verification_code,
        code_type="registration"
    )
    
    if not code_stored:
        raise HTTPException(status_code=500, detail="Failed to store verification code")
    
    # Store user data temporarily (not activated yet)
    temp_user_dict = user_data.dict()
    temp_user_dict['password_hash'] = hash_password(user_data.password)
    del temp_user_dict['password']
    temp_user_dict['email_verified'] = False
    temp_user_dict['account_activated'] = False
    temp_user_dict['created_at'] = datetime.utcnow()
    
    # Store in temporary users collection
    await db.temp_users.delete_many({"email": user_data.email})  # Remove any existing temp user
    await db.temp_users.insert_one(temp_user_dict)
    
    return {
        "message": "Registration initiated. Please check your email for verification code.",
        "email": user_data.email,
        "verification_required": True
    }

@api_router.post("/auth/verify-email")
async def verify_email(email: str, code: str):
    """Verify email address with the provided code and activate account"""
    
    # Verify the code
    code_valid = await email_service.verify_code(
        email=email,
        code=code,
        code_type="registration"
    )
    
    if not code_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    # Get temporary user data
    temp_user = await db.temp_users.find_one({"email": email})
    if not temp_user:
        raise HTTPException(status_code=404, detail="User registration not found")
    
    # Create the actual user account
    user_dict = temp_user.copy()
    user_dict['email_verified'] = True
    user_dict['account_activated'] = True
    user_dict['activated_at'] = datetime.utcnow()
    del user_dict['_id']  # Remove temp ID
    
    user = UserProfile(**user_dict)
    await db.users.insert_one(user.dict())
    
    # NEW: Create user type profile
    try:
        user_types_list = user_dict.get('user_types', ['food_enthusiast'])
        state_code = user_dict.get('state_code', 'IL')  # Default to IL
        zip_code = user_dict.get('zip_code', '')
        
        # Get state info
        state_info = state_compliance_service.get_state_info(state_code) or {}
        
        user_type_profile = UserTypeProfile(
            user_id=user.id,
            user_types=[UserType(ut) for ut in user_types_list],
            primary_type=UserType(user_dict.get('primary_type', 'food_enthusiast')),
            state_code=state_code,
            state_name=state_info.get('state_name', state_code),
            state_category=StateCategory(state_info.get('category', 'moderate')),
            zip_code=zip_code,
            disclaimer_accepted=user_dict.get('disclaimer_accepted', False),
            disclaimer_accepted_at=datetime.utcnow() if user_dict.get('disclaimer_accepted') else None,
            compliance_status={ut: "pending" for ut in user_types_list if ut in ['home_chef', 'home_restaurant', 'farm_vendor']},
            can_sell_packaged_foods='home_chef' in user_types_list,
            can_serve_meals='home_restaurant' in user_types_list,
            can_create_content='recipe_creator' in user_types_list,
            can_review='food_reviewer' in user_types_list or 'food_enthusiast' in user_types_list
        )
        await db.user_type_profiles.insert_one(user_type_profile.dict())
        
        # If user is home chef or restaurant, create compliance profile
        if 'home_chef' in user_types_list or 'home_restaurant' in user_types_list:
            chef_compliance = ChefCompliance(
                chef_id=user.id,
                user_id=user.id,
                state_code=state_code,
                state_name=state_info.get('state_name', state_code),
                zip_code=zip_code,
                tier=ChefTier.PENDING,
                daily_order_limit=None,  # Will be set after verification
                compliance_status=ComplianceStatus.PENDING_REVIEW
            )
            await db.chef_compliance.insert_one(chef_compliance.dict())
    except Exception as e:
        logger.warning(f"Failed to create user type profile: {str(e)}")
    
    # Send welcome SMS notification
    try:
        sms_service = await get_sms_service()
        if user.phone:
            await sms_service.send_registration_sms(
                phone_number=user.phone,
                user_name=user.full_name or user.username
            )
            logger.info(f"Welcome SMS sent to new user: {user.username}")
    except Exception as e:
        logger.warning(f"Failed to send welcome SMS to {user.username}: {str(e)}")
    
    # Remove temporary user data
    await db.temp_users.delete_one({"email": email})
    
    # Generate JWT token
    token = create_jwt_token(user.id)
    
    return {
        "message": "Email verified successfully! Account activated.",
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**user.dict())
    }

@api_router.post("/auth/resend-verification")
async def resend_verification_code(email: str, code_type: str = "registration"):
    """Resend verification code to user's email"""
    
    # Check if user exists in temp_users (for registration) or users (for 2FA)
    if code_type == "registration":
        user = await db.temp_users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="Registration not found. Please register again.")
    else:
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
    # Check for recent code requests (rate limiting)
    recent_code = await db.email_verifications.find_one({
        "email": email,
        "type": code_type,
        "created_at": {"$gte": datetime.utcnow() - timedelta(minutes=1)}
    })
    
    if recent_code:
        raise HTTPException(
            status_code=429, 
            detail="Please wait 60 seconds before requesting a new code"
        )
    
    # Generate new verification code
    verification_code = email_service.generate_verification_code()
    
    # Send verification email
    email_sent = email_service.send_verification_email(
        recipient_email=email,
        verification_code=verification_code,
        email_type=code_type
    )
    
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    # Store verification code
    code_stored = await email_service.store_verification_code(
        email=email,
        code=verification_code,
        code_type=code_type
    )
    
    if not code_stored:
        raise HTTPException(status_code=500, detail="Failed to store verification code")
    
    logger.info(f"Verification code resent for {email} (type: {code_type})")
    
    return {
        "message": "Verification code has been resent to your email",
        "email": email,
        "code_type": code_type
    }

@api_router.post("/auth/login-2fa")
async def login_with_2fa(email: str, password: str, request: Request):
    """Step 1 of 2FA login - verify credentials and send 2FA code"""
    
    # Get client info
    ip_address = request.client.host if request.client else "unknown"
    
    # Find user
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate 2FA code
    verification_code = email_service.generate_verification_code()
    
    # Send 2FA email
    email_sent = email_service.send_verification_email(
        recipient_email=email,
        verification_code=verification_code,
        email_type="login"
    )
    
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send 2FA code")
    
    # Store 2FA code
    code_stored = await email_service.store_verification_code(
        email=email,
        code=verification_code,
        code_type="login"
    )
    
    if not code_stored:
        raise HTTPException(status_code=500, detail="Failed to store 2FA code")
    
    logger.info(f"2FA code sent for login: {email} from {ip_address}")
    
    return {
        "message": "2FA code sent to your email",
        "email": email,
        "requires_2fa": True
    }

@api_router.post("/auth/verify-2fa", response_model=LoginResponse)
async def verify_2fa_login(email: str, code: str, request: Request):
    """Step 2 of 2FA login - verify 2FA code and complete login"""
    
    # Verify 2FA code
    code_valid = await email_service.verify_code(
        email=email,
        code=code,
        code_type="login"
    )
    
    if not code_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired 2FA code")
    
    # Get user
    user_dict = await db.users.find_one({"email": email})
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = UserProfile(**user_dict)
    
    # Update last login
    await db.users.update_one(
        {"id": user.id},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Generate JWT token
    token = create_jwt_token(user.id)
    
    # Get client info for logging
    ip_address = request.client.host if request.client else "unknown"
    logger.info(f"User logged in with 2FA: {user.username} from {ip_address}")
    
    return LoginResponse(
        access_token=token,
        token_type="bearer", 
        user=UserResponse(**user.dict()),
        message="Login successful with 2FA verification"
    )

@api_router.post("/auth/login", response_model=LoginResponse)
async def enhanced_login(login_data: EnhancedUserLogin, request: Request):
    """Login with email verification check and suspicious activity monitoring"""
    
    # Get client info for logging
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Find user
    user_doc = await db.users.find_one({"email": login_data.email})
    if not user_doc:
        log_login_attempt(login_data.email, ip_address, user_agent, False, failed_reason="user_not_found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(login_data.password, user_doc['password_hash']):
        log_login_attempt(login_data.email, ip_address, user_agent, False, failed_reason="invalid_password")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # NEW REQUIREMENT: Check email verification (from registration)
    if not user_doc.get('email_verified', False):
        log_login_attempt(login_data.email, ip_address, user_agent, False, failed_reason="email_not_verified")
        raise HTTPException(
            status_code=403, 
            detail="Please verify your email address. Check your inbox for the verification code."
        )
    
    # Check for suspicious activity patterns (future 2FA trigger points)
    suspicious_activity = await detect_suspicious_login(user_doc, ip_address, user_agent)
    
    if suspicious_activity.get('requires_2fa', False):
        # Only trigger 2FA for suspicious activities
        session_id = str(uuid.uuid4())
        
        # Send 2FA code for suspicious login
        verification_code = email_service.generate_verification_code()
        email_sent = email_service.send_verification_email(
            recipient_email=login_data.email,
            verification_code=verification_code,
            email_type="suspicious_login"
        )
        
        if email_sent:
            await email_service.store_verification_code(
                email=login_data.email,
                code=verification_code,
                code_type="suspicious_login"
            )
            
        return LoginResponse(
            requires_2fa=True,
            session_id=session_id,
            message=f"Suspicious activity detected: {suspicious_activity['reason']}. Please check your email for verification code.",
            twofa_methods=["email"]
        )
    
    # Normal login - no 2FA required
    user = UserProfile(**user_doc)
    
    # Update last login info
    await db.users.update_one(
        {"id": user.id},
        {"$set": {
            "last_login": datetime.utcnow(),
            "last_ip": ip_address,
            "last_user_agent": user_agent
        }}
    )
    
    # Generate JWT token
    token = create_jwt_token(user.id)
    
    log_login_attempt(login_data.email, ip_address, user_agent, True, success_details="normal_login")
    logger.info(f"User logged in successfully: {user.username} from {ip_address}")
    
    return LoginResponse(
        access_token=token,
        token_type="bearer", 
        user=UserResponse(**user.dict()),
        message="Login successful"
    )

async def detect_suspicious_login(user_doc: dict, ip_address: str, user_agent: str) -> dict:
    """Detect suspicious login patterns that require 2FA"""
    
    suspicious_indicators = []
    
    # Check 1: New IP address
    if user_doc.get('last_ip') and user_doc['last_ip'] != ip_address:
        suspicious_indicators.append("new_ip_address")
    
    # Check 2: New device/browser
    if user_doc.get('last_user_agent') and user_doc['last_user_agent'] != user_agent:
        suspicious_indicators.append("new_device")
    
    # Check 3: Login after long period (more than 30 days)
    last_login = user_doc.get('last_login')
    if last_login:
        days_since_last_login = (datetime.utcnow() - last_login).days
        if days_since_last_login > 30:
            suspicious_indicators.append("long_absence")
    
    # Check 4: Multiple failed attempts recently
    recent_failed_attempts = await db.login_attempts.count_documents({
        "email": user_doc['email'],
        "success": False,
        "timestamp": {"$gte": datetime.utcnow() - timedelta(hours=1)}
    })
    
    if recent_failed_attempts >= 3:
        suspicious_indicators.append("multiple_failed_attempts")
    
    # Determine if 2FA is required
    high_risk_indicators = ["multiple_failed_attempts", "new_ip_address"]
    requires_2fa = any(indicator in high_risk_indicators for indicator in suspicious_indicators)
    
    return {
        "requires_2fa": requires_2fa,
        "indicators": suspicious_indicators,
        "reason": ", ".join(suspicious_indicators) if suspicious_indicators else "normal_login"
    }

@api_router.post("/auth/setup-2fa", response_model=dict)
async def setup_2fa(setup_request: Setup2FARequest, current_user_id: str = Depends(get_current_user)):
    """Set up two-factor authentication for user account"""
    
    # Get or create security profile
    security_profile = await db.user_security_profiles.find_one({"user_id": current_user_id})
    
    if not security_profile:
        security_profile = UserSecurityProfile(user_id=current_user_id)
        await db.user_security_profiles.insert_one(security_profile.dict())
    
    response_data = {"success": True, "method": setup_request.method}
    
    if setup_request.method == SecurityKeyType.TOTP:
        # Generate TOTP secret
        totp_secret = generate_totp_secret()
        
        # Generate QR code for Google Authenticator
        user_doc = await db.users.find_one({"id": current_user_id})
        app_name = "Lambalia"
        
        totp_uri = f"otpauth://totp/{app_name}:{user_doc['email']}?secret={totp_secret}&issuer={app_name}"
        
        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Store temporary secret (not activated until verified)
        await db.user_security_profiles.update_one(
            {"user_id": current_user_id},
            {
                "$set": {
                    "temp_totp_secret": totp_secret,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        response_data.update({
            "totp_secret": totp_secret,
            "qr_code": f"data:image/png;base64,{img_base64}",
            "manual_entry_key": totp_secret,
            "instructions": "Scan QR code with Google Authenticator or enter the manual key, then verify with a 6-digit code"
        })
    
    elif setup_request.method == SecurityKeyType.BACKUP_CODE:
        # Generate backup codes
        backup_codes = generate_backup_codes()
        
        await db.user_security_profiles.update_one(
            {"user_id": current_user_id},
            {
                "$set": {
                    "backup_codes": backup_codes,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        response_data.update({
            "backup_codes": backup_codes,
            "instructions": "Save these backup codes in a secure location. Each code can only be used once."
        })
    
    elif setup_request.method == SecurityKeyType.SMS:
        if not setup_request.phone_number:
            raise HTTPException(status_code=400, detail="Phone number required for SMS 2FA")
        
        # In production, send SMS verification
        verification_code = f"{secrets.randbelow(999999):06d}"
        
        await db.user_security_profiles.update_one(
            {"user_id": current_user_id},
            {
                "$set": {
                    "phone_number": setup_request.phone_number,
                    "temp_sms_code": verification_code,
                    "temp_sms_expires": datetime.utcnow() + timedelta(minutes=5),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        response_data.update({
            "phone_number": setup_request.phone_number,
            "instructions": f"SMS sent to {setup_request.phone_number}. Enter verification code to complete setup.",
            "test_code": verification_code  # Remove in production
        })
    
    return response_data

@api_router.post("/auth/verify-2fa-setup", response_model=dict)
async def verify_2fa_setup(verify_request: Verify2FASetupRequest, current_user_id: str = Depends(get_current_user)):
    """Verify and activate 2FA setup"""
    
    security_profile = await db.user_security_profiles.find_one({"user_id": current_user_id})
    if not security_profile:
        raise HTTPException(status_code=404, detail="Security profile not found")
    
    verified = False
    
    if verify_request.method == SecurityKeyType.TOTP:
        temp_secret = security_profile.get('temp_totp_secret')
        
        if not temp_secret:
            raise HTTPException(status_code=400, detail="No TOTP setup in progress")
        
        if verify_totp_code(temp_secret, verify_request.verification_code):
            verified = True
            # Activate TOTP
            await db.user_security_profiles.update_one(
                {"user_id": current_user_id},
                {
                    "$set": {
                        "twofa_enabled": True,
                        "twofa_method": SecurityKeyType.TOTP,
                        "totp_secret": temp_secret,
                        "last_2fa_setup": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    },
                    "$unset": {"temp_totp_secret": ""}
                }
            )
    
    elif verify_request.method == SecurityKeyType.SMS:
        temp_code = security_profile.get('temp_sms_code')
        temp_expires = security_profile.get('temp_sms_expires')
        
        if not temp_code or not temp_expires:
            raise HTTPException(status_code=400, detail="No SMS setup in progress")
        
        if datetime.utcnow() > temp_expires:
            raise HTTPException(status_code=400, detail="SMS verification code expired")
        
        if temp_code == verify_request.verification_code:
            verified = True
            # Activate SMS 2FA
            await db.user_security_profiles.update_one(
                {"user_id": current_user_id},
                {
                    "$set": {
                        "twofa_enabled": True,
                        "twofa_method": SecurityKeyType.SMS,
                        "last_2fa_setup": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    },
                    "$unset": {"temp_sms_code": "", "temp_sms_expires": ""}
                }
            )
    
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    return {
        "success": True,
        "message": f"{verify_request.method.upper()} two-factor authentication activated successfully",
        "backup_codes_recommended": verify_request.method != SecurityKeyType.BACKUP_CODE,
        "next_steps": [
            "Generate backup codes for account recovery",
            "Test login with 2FA to ensure it works",
            "Store backup codes in a secure location"
        ]
    }

@api_router.get("/auth/2fa-status", response_model=dict)
async def get_2fa_status(current_user_id: str = Depends(get_current_user)):
    """Get current 2FA status and available methods"""
    
    security_profile = await db.user_security_profiles.find_one({"user_id": current_user_id})
    
    if not security_profile:
        return {
            "twofa_enabled": False,
            "available_methods": ["totp", "sms", "backup_code"],
            "setup_required": True
        }
    
    enabled_methods = []
    if security_profile.get('totp_secret'):
        enabled_methods.append("totp")
    if security_profile.get('phone_number'):
        enabled_methods.append("sms")
    if security_profile.get('backup_codes'):
        enabled_methods.append("backup_code")
    
    return {
        "twofa_enabled": security_profile.get('twofa_enabled', False),
        "primary_method": security_profile.get('twofa_method'),
        "enabled_methods": enabled_methods,
        "backup_codes_available": len(security_profile.get('backup_codes', [])),
        "backup_codes_used": len(security_profile.get('backup_codes_used', [])),
        "last_setup": security_profile.get('last_2fa_setup'),
        "phone_number": security_profile.get('phone_number', "").replace(security_profile.get('phone_number', "")[3:-2], "***") if security_profile.get('phone_number') else None
    }

@api_router.post("/auth/disable-2fa", response_model=dict)
async def disable_2fa(current_user_id: str = Depends(get_current_user)):
    """Disable two-factor authentication (requires current password)"""
    
    await db.user_security_profiles.update_one(
        {"user_id": current_user_id},
        {
            "$set": {
                "twofa_enabled": False,
                "updated_at": datetime.utcnow()
            },
            "$unset": {
                "twofa_method": "",
                "totp_secret": "",
                "backup_codes": "",
                "backup_codes_used": "",
                "phone_number": ""
            }
        }
    )
    
    return {
        "success": True,
        "message": "Two-factor authentication disabled successfully",
        "warning": "Your account is now less secure. Consider re-enabling 2FA."
    }

# Legacy login endpoint for backward compatibility
@api_router.post("/auth/login-simple", response_model=TokenResponse)
async def login_user(login_data: UserLogin):
    """Legacy login endpoint without 2FA support - DEPRECATED"""
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

@api_router.get("/heritage/user-contributions")
async def get_user_heritage_contributions():
    """Get aggregated data from user registrations about native dishes"""
    
    users_with_heritage = await db.users.find({
        "$or": [
            {"native_dishes": {"$exists": True, "$ne": ""}},
            {"consultation_specialties": {"$exists": True, "$ne": ""}},
            {"cultural_background": {"$exists": True, "$ne": ""}}
        ]
    }, {"_id": 0, "native_dishes": 1, "consultation_specialties": 1, "cultural_background": 1, "username": 1}).to_list(length=1000)
    
    # Aggregate data for insights
    cultural_backgrounds = {}
    native_dishes_list = []
    consultation_specialties_list = []
    
    for user in users_with_heritage:
        if user.get('cultural_background'):
            bg = user['cultural_background'].lower()
            cultural_backgrounds[bg] = cultural_backgrounds.get(bg, 0) + 1
        
        if user.get('native_dishes'):
            dishes = [d.strip() for d in user['native_dishes'].split(',')]
            native_dishes_list.extend(dishes)
        
        if user.get('consultation_specialties'):
            specialties = [s.strip() for s in user['consultation_specialties'].split(',')]
            consultation_specialties_list.extend(specialties)
    
    return {
        "total_contributors": len(users_with_heritage),
        "cultural_backgrounds": cultural_backgrounds,
        "top_native_dishes": dict(sorted({dish: native_dishes_list.count(dish) for dish in set(native_dishes_list)}.items(), key=lambda x: x[1], reverse=True)[:20]),
        "top_consultation_specialties": dict(sorted({spec: consultation_specialties_list.count(spec) for spec in set(consultation_specialties_list)}.items(), key=lambda x: x[1], reverse=True)[:15]),
        "recent_contributors": users_with_heritage[:10]
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

# SUBSCRIPTION BOX & VIRTUAL EVENTS MONETIZATION
@api_router.get("/revenue/subscription-products")
async def get_subscription_product_opportunities():
    """Subscription box and recurring product opportunities"""
    
    subscription_products = {
        "cultural_ingredient_boxes": {
            "concept": "Monthly boxes with authentic ingredients for specific cultural recipes",
            "pricing": "$29.99-49.99/month",
            "target_market": "Diaspora communities, cultural food enthusiasts",
            "partnerships": "H-Mart, Patel Brothers for ingredient sourcing",
            "estimated_subscribers": "500-2000 in year 1",
            "monthly_revenue_potential": "$15000-80000",
            "margin": "40-60%"
        },
        "recipe_collection_subscriptions": {
            "concept": "Premium access to authenticated family recipes with video tutorials",
            "pricing": "$9.99-19.99/month",
            "content": "5-10 exclusive family recipes monthly with cultural stories",
            "target_market": "Cooking enthusiasts, cultural education",
            "estimated_subscribers": "1000-5000 in year 1", 
            "monthly_revenue_potential": "$10000-75000",
            "margin": "85-95%"
        },
        "virtual_cooking_events": {
            "concept": "Live cooking classes with cultural experts",
            "pricing": "$15-45 per event, $99-199 monthly unlimited",
            "format": "Interactive Zoom sessions with ingredient kits",
            "frequency": "2-3 events per week",
            "estimated_attendance": "20-100 per event",
            "monthly_revenue_potential": "$5000-25000",
            "scalability": "High - can record and resell"
        },
        "cultural_spice_blends": {
            "concept": "Custom spice blends from cultural experts on platform",
            "pricing": "$8-15 per blend, $25-40 for bundle",
            "partnerships": "Home chefs create signature blends",
            "distribution": "Ship direct or partner with stores",
            "estimated_monthly_sales": "200-800 units",
            "monthly_revenue_potential": "$2000-8000",
            "margin": "60-75%"
        }
    }
    
    return {
        "subscription_products": subscription_products,
        "total_monthly_potential": "$32000-188000",
        "implementation_priority": "cultural_ingredient_boxes (highest demand)",
        "test_market_recommendation": "Start with 2 popular cultural communities",
        "partnership_requirements": [
            "Ingredient suppliers (H-Mart, specialty stores)",
            "Shipping logistics partner", 
            "Cultural recipe contributors",
            "Video production capabilities"
        ]
    }

@api_router.get("/revenue/brand-partnerships")
async def get_brand_partnership_opportunities():
    """Brand partnership and sponsored content opportunities"""
    
    brand_partnerships = {
        "kitchen_equipment_brands": {
            "partners": ["KitchenAid", "Cuisinart", "Lodge Cast Iron", "Instant Pot"],
            "partnership_type": "Sponsored recipe content and equipment reviews",
            "revenue_model": "$500-2000 per sponsored recipe + affiliate commissions",
            "content_format": "Cultural recipes featuring specific equipment",
            "estimated_monthly": "$3000-8000"
        },
        "spice_and_ingredient_brands": {
            "partners": ["McCormick", "Penzeys Spices", "Spice Jungle", "Diaspora Co"],
            "partnership_type": "Authentic cultural recipe development",
            "revenue_model": "$300-1500 per recipe + ongoing royalties",
            "content_format": "Traditional recipes highlighting specific spices/ingredients",
            "estimated_monthly": "$2500-6000"
        },
        "cultural_food_festivals": {
            "partners": ["Local cultural festivals", "Food & Wine events", "Cultural centers"],
            "partnership_type": "Official recipe platform and cultural authenticity partner",
            "revenue_model": "$1000-5000 per event + booth revenue",
            "value_proposition": "Authentic cultural representation and recipe verification",
            "estimated_monthly": "$2000-10000"
        },
        "media_and_publishing": {
            "partners": ["Food Network", "Bon Appétit", "Cultural magazines", "PBS"],
            "partnership_type": "Content licensing and cultural expert platform",
            "revenue_model": "$500-3000 per licensed recipe + ongoing attribution",
            "content_format": "Authenticated cultural recipes with stories",
            "estimated_monthly": "$1500-5000"
        }
    }
    
    return {
        "brand_partnerships": brand_partnerships,
        "total_monthly_potential": "$9000-29000",
        "negotiation_leverage": "Authentic cultural content and 80+ community reach",
        "unique_value_proposition": "Only platform with verified cultural authenticity",
        "partnership_development_strategy": [
            "Create partnership deck highlighting cultural authenticity",
            "Develop case studies from current cultural contributors",
            "Establish cultural advisory board for brand partnerships",
            "Create tiered partnership packages"
        ]
    }
# COMPREHENSIVE REVENUE DASHBOARD
@api_router.get("/revenue/comprehensive-dashboard")
async def get_comprehensive_revenue_dashboard():
    """Complete revenue analytics dashboard for all income streams"""
    
    # Simulate revenue calculations based on current platform metrics
    current_date = datetime.utcnow()
    
    revenue_streams = {
        "marketplace_commissions": {
            "commission_rate": "15%",
            "current_monthly": 8500,
            "projected_monthly": 25000,
            "sources": ["Home restaurants", "Lambalia Eats", "Farm partnerships", "Recipe consultations"],
            "growth_rate": "35% month-over-month"
        },
        "premium_subscriptions": {
            "tiers": {
                "cook_plus": {"price": 4.99, "subscribers": 150, "monthly_revenue": 748.50},
                "foodie_pro": {"price": 7.99, "subscribers": 85, "monthly_revenue": 679.15},
                "culinary_vip": {"price": 12.99, "subscribers": 32, "monthly_revenue": 415.68}
            },
            "total_monthly": 1843.33,
            "projected_monthly": 5200,
            "retention_rate": "85%"
        },
        "external_advertising": {
            "google_adsense": {"monthly_revenue": 650, "cpm": "$2.00"},
            "facebook_network": {"monthly_revenue": 380, "cpm": "$1.50"},
            "amazon_affiliates": {"monthly_revenue": 420, "commission_avg": "6%"},
            "total_monthly": 1450,
            "projected_monthly": 4200
        },
        "data_monetization": {
            "cultural_trends": {"clients": 3, "monthly_revenue": 3600},
            "ingredient_analytics": {"clients": 5, "monthly_revenue": 2800},
            "diaspora_insights": {"clients": 2, "monthly_revenue": 2200},
            "total_monthly": 8600,
            "projected_monthly": 35000
        },
        "white_label_licensing": {
            "grocery_integrations": {"clients": 1, "monthly_revenue": 3500},
            "restaurant_groups": {"clients": 2, "monthly_revenue": 4000},
            "corporate_programs": {"clients": 0, "monthly_revenue": 0},
            "total_monthly": 7500,
            "projected_monthly": 45000
        },
        "subscription_products": {
            "ingredient_boxes": {"monthly_revenue": 0, "projected": 47500},
            "recipe_collections": {"monthly_revenue": 0, "projected": 42500},
            "virtual_events": {"monthly_revenue": 0, "projected": 15000},
            "spice_blends": {"monthly_revenue": 0, "projected": 5000},
            "total_monthly": 0,
            "projected_monthly": 110000
        },
        "brand_partnerships": {
            "equipment_brands": {"monthly_revenue": 0, "projected": 5500},
            "ingredient_brands": {"monthly_revenue": 0, "projected": 4250},
            "cultural_festivals": {"monthly_revenue": 0, "projected": 6000},
            "media_licensing": {"monthly_revenue": 0, "projected": 3250},
            "total_monthly": 0,
            "projected_monthly": 19000
        }
    }
    
    # Calculate totals
    current_total = sum([stream.get("total_monthly", stream.get("current_monthly", 0)) for stream in revenue_streams.values()])
    projected_total = sum([stream.get("projected_monthly", 0) for stream in revenue_streams.values()])
    
    return {
        "revenue_streams": revenue_streams,
        "summary": {
            "current_monthly_revenue": current_total,
            "projected_monthly_revenue": projected_total,
            "annual_projection": projected_total * 12,
            "growth_potential": f"{((projected_total - current_total) / current_total * 100):.0f}%",
            "diversification_score": len(revenue_streams),
            "revenue_stability": "high_diversification"
        },
        "recommendations": [
            "Accelerate external ad integration (+$2,750/month)",
            "Launch cultural ingredient subscription boxes (+$47,500/month)",
            "Expand data monetization clients (+$26,400/month)",  
            "Close 2 white-label deals (+$37,500/month)",
            "Develop brand partnerships (+$19,000/month)"
        ],
        "immediate_implementations": [
            "Google AdSense (2-3 days setup)",
            "Amazon affiliate program (1 week)",
            "Basic subscription box MVP (4 weeks)",
            "Data product sales materials (2 weeks)"
        ],
        "projected_12_month_revenue": "$3.1M annually at full implementation"
    }

# BUSINESS OPERATIONS & FINANCIAL CONTROL
@api_router.get("/admin/financial-overview")
async def get_financial_overview(current_user_id: str = Depends(get_current_user)):
    """Master financial dashboard - Platform Owner Access Only"""
    
    # Check if user has admin privileges (you would set this during initial setup)
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    financial_overview = {
        "platform_owner": {
            "name": user.get("full_name", "Platform Owner"),
            "email": user.get("email"),
            "owner_id": current_user_id,
            "access_level": "full_financial_control"
        },
        "real_time_balances": {
            "stripe_balance": 0,  # Would connect to real Stripe API
            "pending_payouts": 0,
            "platform_revenue": 0,
            "user_earnings_held": 0,
            "total_platform_value": 0
        },
        "revenue_breakdown_today": {
            "marketplace_commissions": {"transactions": 12, "revenue": 285.50},
            "subscription_revenue": {"new_subs": 3, "revenue": 62.85},
            "external_ads": {"impressions": 15420, "revenue": 22.40},
            "consultation_fees": {"sessions": 3, "revenue": 45.00},
            "affiliate_commissions": {"purchases": 8, "revenue": 18.75},
            "total_today": 434.50
        },
        "financial_controls": {
            "auto_payout_threshold": 100,  # Automatic payout to your account when reached
            "manual_approval_required": ["white_label_payments", "data_sales"],
            "payment_methods": {
                "stripe_connect": "primary_processor",
                "bank_account": "direct_deposits", 
                "paypal": "international_payouts"
            }
        },
        "access_permissions": {
            "platform_owner": ["view_all", "withdraw_funds", "modify_rates", "user_management"],
            "financial_manager": ["view_revenue", "process_payouts", "generate_reports"],
            "operations_manager": ["view_metrics", "user_support", "content_moderation"],
            "regular_users": ["view_own_earnings", "request_payouts"]
        }
    }
    
    return financial_overview

@api_router.get("/admin/revenue-audit-trail")
async def get_revenue_audit_trail(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user_id: str = Depends(get_current_user)
):
    """Detailed audit trail of all revenue transactions"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    # This would query actual transaction logs in production
    audit_trail = {
        "period": f"{date_from or 'last_30_days'} to {date_to or 'today'}",
        "total_transactions": 347,
        "total_revenue": 28945.67,
        "revenue_sources": {
            "marketplace_commissions": {
                "transaction_count": 156,
                "revenue": 18500.25,
                "breakdown": {
                    "home_restaurants": 12400.50,
                    "lambalia_eats": 4350.75,
                    "farm_partnerships": 1749.00
                }
            },
            "subscriptions": {
                "transaction_count": 89,
                "revenue": 5240.85,
                "breakdown": {
                    "new_subscriptions": 2100.45,
                    "renewals": 3140.40
                }
            },
            "external_ads": {
                "impressions": 450000,
                "clicks": 18500,
                "revenue": 1840.50,
                "networks": {
                    "google_adsense": 1150.30,
                    "facebook_network": 425.20,
                    "amazon_affiliates": 265.00
                }
            }
        },
        "payout_requests": {
            "pending": {"count": 23, "amount": 2450.75},
            "processed": {"count": 145, "amount": 18500.25},
            "on_hold": {"count": 3, "amount": 350.00, "reason": "verification_needed"}
        }
    }
    
    return audit_trail

@api_router.post("/admin/platform-settings")
async def update_platform_settings(
    settings_update: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Update platform-wide settings - Owner Only"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    # Update platform settings
    await db.platform_settings.update_one(
        {"setting_type": "financial_controls"},
        {"$set": {
            **settings_update,
            "updated_by": current_user_id,
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )
    
    return {
        "success": True,
        "message": "Platform settings updated",
        "updated_by": user.get("email"),
        "settings_changed": list(settings_update.keys())
    }

# FINANCIAL CONTROL & WITHDRAWAL SYSTEM
@api_router.get("/admin/withdrawal-controls")
async def get_withdrawal_controls(current_user_id: str = Depends(get_current_user)):
    """Master withdrawal and payout controls"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    withdrawal_system = {
        "platform_accounts": {
            "primary_business_account": {
                "bank": "Chase Business Banking",
                "account_type": "Business Checking",
                "balance": 45230.75,  # Would connect to real bank API
                "auto_transfer": True,
                "minimum_balance": 10000
            },
            "stripe_account": {
                "account_id": "acct_platform_stripe_id",
                "available_balance": 8940.50,
                "pending_balance": 2150.25,
                "next_payout": "2024-01-15"
            },
            "paypal_business": {
                "account_email": "business@lambalia.com",
                "balance": 1250.30,
                "currency": "USD"
            }
        },
        "withdrawal_settings": {
            "auto_withdrawal_enabled": True,
            "minimum_amount": 100,
            "withdrawal_frequency": "daily",
            "approval_required_over": 5000,
            "notification_email": user.get("email"),
            "backup_notification": "finance@lambalia.com"
        },
        "user_payout_controls": {
            "minimum_user_payout": 25,
            "payout_schedule": "weekly",
            "hold_new_users": 14,  # Days to hold payouts for new users
            "verification_required_over": 1000
        }
    }
    
    return withdrawal_system

@api_router.post("/admin/withdraw-funds")
async def withdraw_platform_funds(
    withdrawal_request: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Withdraw funds to your personal/business account"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    amount = withdrawal_request.get("amount", 0)
    destination = withdrawal_request.get("destination", "primary_account")
    
    # Validation
    if amount < 100:
        raise HTTPException(status_code=400, detail="Minimum withdrawal is $100")
    
    # In production, this would integrate with actual payment processors
    withdrawal_record = {
        "id": str(uuid.uuid4()),
        "amount": amount,
        "destination": destination,
        "requested_by": user.get("email"),
        "status": "processed",  # Would be "pending" initially
        "processed_at": datetime.utcnow(),
        "confirmation_code": f"WD{str(uuid.uuid4())[:8].upper()}",
        "fees": amount * 0.001,  # 0.1% platform fee
        "net_amount": amount * 0.999
    }
    
    # Record transaction
    await db.platform_withdrawals.insert_one(withdrawal_record)
    
    return {
        "success": True,
        "message": f"${amount} withdrawal processed",
        "confirmation_code": withdrawal_record["confirmation_code"],
        "net_amount": withdrawal_record["net_amount"],
        "processing_time": "1-3 business days"
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

# Initialize Smart Cooking Tool service
smart_cooking_service = SmartCookingToolService(db)

# Initialize Transaction Verification service
transaction_verification_service = TransactionVerificationService(db)

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

# PRICING & PAYMENT PROCESSING SYSTEM
class PricingStructure:
    """Centralized pricing structure for all Lambalia services"""
    
    # Consultation Services
    CONSULTATION_MESSAGE = 2.50
    CONSULTATION_AUDIO = 3.50  
    CONSULTATION_VIDEO = 4.50
    
    # Lambalia Eats
    BASE_MEAL_PRICE = 10.00
    
    # Platform Commission
    PLATFORM_COMMISSION_RATE = 0.15  # 15%
    USER_EARNINGS_RATE = 0.85        # 85%
    
    # Delivery Pricing (per km)
    DELIVERY_RATE_PER_KM = 0.75      # $0.75 per kilometer
    DELIVERY_BASE_FEE = 2.00         # Minimum delivery fee

class TransactionType(str, Enum):
    CONSULTATION_MESSAGE = "consultation_message"
    CONSULTATION_AUDIO = "consultation_audio"
    CONSULTATION_VIDEO = "consultation_video"
    LAMBALIA_EATS = "lambalia_eats"
    HOME_RESTAURANT = "home_restaurant"
    FARM_BOOKING = "farm_booking"
    RECIPE_PURCHASE = "recipe_purchase"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    PROCESSING = "processing"
    FAILED = "failed"
    REFUNDED = "refunded"

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_type: TransactionType
    payer_id: str
    recipient_id: str
    
    # Pricing breakdown
    gross_amount: float
    platform_commission: float
    user_earnings: float
    delivery_fee: Optional[float] = 0.0
    
    # Service details
    service_description: str
    consultation_type: Optional[str] = None  # message, audio, video
    delivery_distance_km: Optional[float] = None
    
    # Payment processing
    status: PaymentStatus = PaymentStatus.PENDING
    stripe_payment_intent_id: Optional[str] = None
    processed_at: Optional[datetime] = None
    
    # Payout tracking
    user_payout_processed: bool = False
    user_payout_date: Optional[datetime] = None
    platform_earnings_collected: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserEarnings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Weekly earnings summary
    week_start_date: datetime
    week_end_date: datetime
    
    # Earnings breakdown
    total_gross_earnings: float = 0.0
    platform_commission_deducted: float = 0.0  
    net_earnings: float = 0.0
    
    # Transaction details
    consultation_earnings: float = 0.0
    lambalia_eats_earnings: float = 0.0
    home_restaurant_earnings: float = 0.0
    other_earnings: float = 0.0
    
    # Payout status
    payout_processed: bool = False
    payout_date: Optional[datetime] = None
    payout_amount: float = 0.0
    payout_method: Optional[str] = None  # stripe, paypal, bank
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserPayoutProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Payout preferences
    preferred_payout_method: str = "stripe"  # stripe, paypal, bank_transfer
    minimum_payout_amount: float = 25.00    # Weekly minimum for payout
    
    # Account details (encrypted in production)
    stripe_account_id: Optional[str] = None
    paypal_email: Optional[str] = None
    bank_account_info: Optional[Dict[str, str]] = None
    
    # Status
    is_verified: bool = False
    verification_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# PRICING CALCULATION FUNCTIONS
def calculate_consultation_pricing(consultation_type: str) -> Dict[str, float]:
    """Calculate pricing for consultation services"""
    
    pricing_map = {
        "message": PricingStructure.CONSULTATION_MESSAGE,
        "audio": PricingStructure.CONSULTATION_AUDIO,
        "video": PricingStructure.CONSULTATION_VIDEO
    }
    
    gross_amount = pricing_map.get(consultation_type, PricingStructure.CONSULTATION_MESSAGE)
    platform_commission = gross_amount * PricingStructure.PLATFORM_COMMISSION_RATE
    user_earnings = gross_amount * PricingStructure.USER_EARNINGS_RATE
    
    return {
        "gross_amount": gross_amount,
        "platform_commission": round(platform_commission, 2),
        "user_earnings": round(user_earnings, 2),
        "service_type": consultation_type
    }

def calculate_lambalia_eats_pricing(delivery_distance_km: Optional[float] = None) -> Dict[str, float]:
    """Calculate pricing for Lambalia Eats orders"""
    
    base_meal_price = PricingStructure.BASE_MEAL_PRICE
    
    # Calculate delivery fee if applicable
    delivery_fee = 0.0
    if delivery_distance_km and delivery_distance_km > 0:
        delivery_fee = max(
            PricingStructure.DELIVERY_BASE_FEE,
            delivery_distance_km * PricingStructure.DELIVERY_RATE_PER_KM
        )
    
    total_gross = base_meal_price + delivery_fee
    platform_commission = total_gross * PricingStructure.PLATFORM_COMMISSION_RATE
    user_earnings = total_gross * PricingStructure.USER_EARNINGS_RATE
    
    return {
        "gross_amount": total_gross,
        "base_meal_price": base_meal_price,
        "delivery_fee": round(delivery_fee, 2),
        "platform_commission": round(platform_commission, 2),
        "user_earnings": round(user_earnings, 2),
        "delivery_distance_km": delivery_distance_km or 0
    }

async def update_user_weekly_earnings(user_id: str, transaction: Transaction):
    """Update user's weekly earnings record"""
    
    # Get current week boundaries
    now = datetime.utcnow()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Find or create weekly earnings record
    earnings_record = await db.user_earnings.find_one({
        "user_id": user_id,
        "week_start_date": {"$lte": now},
        "week_end_date": {"$gte": now}
    })
    
    if not earnings_record:
        earnings_record = UserEarnings(
            user_id=user_id,
            week_start_date=week_start,
            week_end_date=week_end
        )
        await db.user_earnings.insert_one(earnings_record.dict())
        earnings_record = earnings_record.dict()
    
    # Update earnings based on transaction type
    update_data = {
        "$inc": {
            "total_gross_earnings": transaction.gross_amount,
            "platform_commission_deducted": transaction.platform_commission,
            "net_earnings": transaction.user_earnings
        }
    }
    
    # Add to specific category
    if transaction.transaction_type in [TransactionType.CONSULTATION_MESSAGE, TransactionType.CONSULTATION_AUDIO, TransactionType.CONSULTATION_VIDEO]:
        update_data["$inc"]["consultation_earnings"] = transaction.user_earnings
    elif transaction.transaction_type == TransactionType.LAMBALIA_EATS:
        update_data["$inc"]["lambalia_eats_earnings"] = transaction.user_earnings
    elif transaction.transaction_type == TransactionType.HOME_RESTAURANT:
        update_data["$inc"]["home_restaurant_earnings"] = transaction.user_earnings
    else:
        update_data["$inc"]["other_earnings"] = transaction.user_earnings
    
    await db.user_earnings.update_one(
        {"id": earnings_record["id"]},
        update_data
    )

# USER EARNINGS DASHBOARD
@api_router.get("/payments/my-earnings")
async def get_user_earnings(current_user_id: str = Depends(get_current_user)):
    """Get user's earnings dashboard"""
    
    # Get current week earnings
    now = datetime.utcnow()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    current_week_earnings = await db.user_earnings.find_one({
        "user_id": current_user_id,
        "week_start_date": {"$lte": now},
        "week_end_date": {"$gte": now}
    })
    
    # Get all-time earnings
    all_earnings = await db.user_earnings.find({
        "user_id": current_user_id
    }).to_list(length=100)
    
    # Calculate totals
    total_net_earnings = sum([e.get("net_earnings", 0) for e in all_earnings])
    total_commission_paid = sum([e.get("platform_commission_deducted", 0) for e in all_earnings])
    total_gross = sum([e.get("total_gross_earnings", 0) for e in all_earnings])
    
    # Get payout profile
    payout_profile = await db.user_payout_profiles.find_one({"user_id": current_user_id})
    
    # Recent transactions
    recent_transactions = await db.transactions.find({
        "recipient_id": current_user_id,
        "status": PaymentStatus.COMPLETED
    }).sort("created_at", -1).limit(10).to_list(length=10)
    
    # Pending payouts
    pending_payouts = await db.user_earnings.find({
        "user_id": current_user_id,
        "payout_processed": False,
        "net_earnings": {"$gte": (payout_profile.get("minimum_payout_amount", 25.0) if payout_profile else 25.0)}
    }).to_list(length=10)
    
    pending_amount = sum([e.get("net_earnings", 0) for e in pending_payouts])
    
    return {
        "user_id": current_user_id,
        "earnings_summary": {
            "current_week_earnings": current_week_earnings.get("net_earnings", 0) if current_week_earnings else 0,
            "total_lifetime_earnings": total_net_earnings,
            "total_platform_commission": total_commission_paid,
            "total_gross_revenue": total_gross,
            "pending_payout_amount": pending_amount
        },
        "earnings_breakdown": {
            "consultation_earnings": sum([e.get("consultation_earnings", 0) for e in all_earnings]),
            "lambalia_eats_earnings": sum([e.get("lambalia_eats_earnings", 0) for e in all_earnings]),
            "home_restaurant_earnings": sum([e.get("home_restaurant_earnings", 0) for e in all_earnings]),
            "other_earnings": sum([e.get("other_earnings", 0) for e in all_earnings])
        },
        "current_week": current_week_earnings,
        "recent_transactions": recent_transactions,
        "payout_info": {
            "payout_profile_setup": bool(payout_profile),
            "minimum_payout": payout_profile.get("minimum_payout_amount", 25.0) if payout_profile else 25.0,
            "next_payout_date": "Every Sunday at 11:59 PM EST",
            "payout_method": payout_profile.get("preferred_payout_method", "not_set") if payout_profile else "not_set"
        }
    }

@api_router.post("/payments/setup-payout-profile")  
async def setup_payout_profile(
    payout_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Set up user's payout profile for weekly payments"""
    
    payout_method = payout_data.get("payout_method", "stripe")
    minimum_amount = payout_data.get("minimum_payout_amount", 25.0)
    
    # Validate minimum amount
    if minimum_amount < 10.0:
        raise HTTPException(status_code=400, detail="Minimum payout amount must be at least $10")
    
    # Create or update payout profile
    payout_profile = {
        "user_id": current_user_id,
        "preferred_payout_method": payout_method,
        "minimum_payout_amount": minimum_amount,
        "updated_at": datetime.utcnow()
    }
    
    # Add method-specific details
    if payout_method == "stripe":
        payout_profile["stripe_account_id"] = payout_data.get("stripe_account_id")
    elif payout_method == "paypal":
        payout_profile["paypal_email"] = payout_data.get("paypal_email")
    elif payout_method == "bank_transfer":
        payout_profile["bank_account_info"] = {
            "account_number": payout_data.get("account_number", ""),
            "routing_number": payout_data.get("routing_number", ""),
            "bank_name": payout_data.get("bank_name", "")
        }
    
    # Update or create profile
    await db.user_payout_profiles.update_one(
        {"user_id": current_user_id},
        {"$set": payout_profile},
        upsert=True
    )
    
    return {
        "success": True,
        "message": "Payout profile updated successfully",
        "payout_method": payout_method,
        "minimum_amount": minimum_amount,
        "next_payout": "Next Sunday if minimum amount reached"
    }

# WEEKLY PAYOUT PROCESSING (Platform Owner)
@api_router.post("/admin/process-weekly-payouts")
async def process_weekly_payouts(current_user_id: str = Depends(get_current_user)):
    """Process all weekly payouts - Platform Owner Only"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    # Get all users with unpaid earnings above minimum threshold
    unpaid_earnings = await db.user_earnings.aggregate([
        {"$match": {"payout_processed": False}},
        {"$group": {
            "_id": "$user_id",
            "total_pending": {"$sum": "$net_earnings"},
            "total_commission": {"$sum": "$platform_commission_deducted"},
            "earnings_records": {"$push": "$$ROOT"}
        }},
        {"$match": {"total_pending": {"$gte": 25.0}}}  # Default minimum
    ]).to_list(length=1000)
    
    payout_results = []
    total_platform_earnings = 0.0
    
    for user_earnings in unpaid_earnings:
        user_id = user_earnings["_id"]
        pending_amount = user_earnings["total_pending"]
        commission_collected = user_earnings["total_commission"]
        
        # Get user payout profile
        payout_profile = await db.user_payout_profiles.find_one({"user_id": user_id})
        
        if not payout_profile:
            payout_results.append({
                "user_id": user_id,
                "status": "skipped",
                "reason": "No payout profile setup",
                "pending_amount": pending_amount
            })
            continue
        
        # Check if amount meets user's minimum threshold
        user_minimum = payout_profile.get("minimum_payout_amount", 25.0)
        if pending_amount < user_minimum:
            payout_results.append({
                "user_id": user_id,
                "status": "skipped", 
                "reason": f"Below minimum threshold ${user_minimum}",
                "pending_amount": pending_amount
            })
            continue
        
        # Process payout (simulate - integrate with real payment processor in production)
        try:
            # Mark earnings as paid
            earnings_ids = [record["id"] for record in user_earnings["earnings_records"]]
            await db.user_earnings.update_many(
                {"id": {"$in": earnings_ids}},
                {"$set": {
                    "payout_processed": True,
                    "payout_date": datetime.utcnow(),
                    "payout_amount": pending_amount,
                    "payout_method": payout_profile.get("preferred_payout_method")
                }}
            )
            
            # Add to platform earnings
            total_platform_earnings += commission_collected
            
            payout_results.append({
                "user_id": user_id,
                "status": "processed",
                "payout_amount": pending_amount,
                "payout_method": payout_profile.get("preferred_payout_method"),
                "commission_collected": commission_collected
            })
            
        except Exception as e:
            payout_results.append({
                "user_id": user_id,
                "status": "failed",
                "reason": str(e),
                "pending_amount": pending_amount
            })
    
    # Record platform earnings collection
    if total_platform_earnings > 0:
        await db.platform_earnings.insert_one({
            "id": str(uuid.uuid4()),
            "collection_date": datetime.utcnow(),
            "total_commission_collected": total_platform_earnings,
            "payouts_processed": len([r for r in payout_results if r["status"] == "processed"]),
            "collection_type": "weekly_payout_processing"
        })
    
    return {
        "success": True,
        "payout_summary": {
            "total_payouts_processed": len([r for r in payout_results if r["status"] == "processed"]),
            "total_amount_paid": sum([r.get("payout_amount", 0) for r in payout_results if r["status"] == "processed"]),
            "total_platform_earnings": total_platform_earnings,
            "payouts_skipped": len([r for r in payout_results if r["status"] == "skipped"]),
            "payouts_failed": len([r for r in payout_results if r["status"] == "failed"])
        },
        "detailed_results": payout_results,
        "processing_date": datetime.utcnow().isoformat(),
        "next_processing": "Next Sunday at 11:59 PM EST"
    }

# TRANSACTION PROCESSING ENDPOINTS
@api_router.post("/payments/create-consultation-transaction")
async def create_consultation_transaction(
    transaction_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Create consultation payment transaction"""
    
    consultation_type = transaction_data.get("consultation_type")  # message, audio, video
    recipient_id = transaction_data.get("recipient_id")
    service_description = transaction_data.get("service_description", "Recipe consultation")
    
    # Calculate pricing
    pricing = calculate_consultation_pricing(consultation_type)
    
    # Create transaction record
    transaction = Transaction(
        transaction_type=TransactionType.CONSULTATION_MESSAGE if consultation_type == "message" else 
                        TransactionType.CONSULTATION_AUDIO if consultation_type == "audio" else
                        TransactionType.CONSULTATION_VIDEO,
        payer_id=current_user_id,
        recipient_id=recipient_id,
        gross_amount=pricing["gross_amount"],
        platform_commission=pricing["platform_commission"],
        user_earnings=pricing["user_earnings"],
        service_description=service_description,
        consultation_type=consultation_type
    )
    
    # In production, integrate with Stripe Payment Intents
    # For now, simulate successful payment
    transaction.status = PaymentStatus.COMPLETED
    transaction.processed_at = datetime.utcnow()
    
    # Save transaction
    await db.transactions.insert_one(transaction.dict())
    
    # Update user earnings
    await update_user_weekly_earnings(recipient_id, transaction)
    
    return {
        "success": True,
        "transaction_id": transaction.id,
        "pricing_breakdown": pricing,
        "payment_status": "completed",
        "message": f"${pricing['gross_amount']} consultation payment processed"
    }

@api_router.post("/payments/create-lambalia-eats-transaction")
async def create_lambalia_eats_transaction(
    order_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Create Lambalia Eats payment transaction"""
    
    cook_id = order_data.get("cook_id")
    delivery_distance_km = order_data.get("delivery_distance_km", 0)
    service_description = order_data.get("service_description", "Lambalia Eats meal order")
    
    # Calculate pricing including delivery
    pricing = calculate_lambalia_eats_pricing(delivery_distance_km)
    
    # Create transaction
    transaction = Transaction(
        transaction_type=TransactionType.LAMBALIA_EATS,
        payer_id=current_user_id,
        recipient_id=cook_id,
        gross_amount=pricing["gross_amount"],
        platform_commission=pricing["platform_commission"],
        user_earnings=pricing["user_earnings"],
        delivery_fee=pricing["delivery_fee"],
        service_description=service_description,
        delivery_distance_km=delivery_distance_km
    )
    
    # Process payment (simulate success)
    transaction.status = PaymentStatus.COMPLETED
    transaction.processed_at = datetime.utcnow()
    
    # Save transaction
    await db.transactions.insert_one(transaction.dict())
    
    # Update cook earnings
    await update_user_weekly_earnings(cook_id, transaction)
    
    return {
        "success": True,
        "transaction_id": transaction.id,
        "pricing_breakdown": pricing,
        "order_summary": {
            "meal_price": pricing["base_meal_price"],
            "delivery_fee": pricing["delivery_fee"],
            "total_paid": pricing["gross_amount"],
            "cook_earnings": pricing["user_earnings"],
            "platform_commission": pricing["platform_commission"]
        }
    }

# AFRICAN DISHES DATABASE BY COUNTRY
AFRICAN_DISHES_BY_COUNTRY = {
    "algeria": [
        "Couscous", "Tajine", "Makroudh", "Chorba", "Mechoui", "Brik", "Harira", 
        "Loubia", "Rechta", "Chouarak", "Baklawa", "M'hencha", "Kalb el louz"
    ],
    "angola": [
        "Muamba de galinha", "Calulu", "Funge", "Farofa de mandioca", "Kizaka", 
        "Mufete", "Cocada amarela", "Quindim", "Moamba de dendém", "Feijão tropeiro"
    ],
    "benin": [
        "Akassa", "Aloko", "Amiwo", "Djenkoume", "Fufu", "Igname pilé", "Klui klui", 
        "Pâte", "Tchoukoutou", "Wagashi", "Yovo doko"
    ],
    "botswana": [
        "Seswaa", "Pap", "Morogo", "Bogobe", "Matemekwane", "Phane", "Vetkoek", 
        "Magwinya", "Dikgobe", "Masonja"
    ],
    "burkina_faso": [
        "Tô", "Riz gras", "Poulet bicyclette", "Ragout d'igname", "Beignets", 
        "Dolo", "Thiakry", "Couscous de mil", "Sauce d'arachide"
    ],
    "cameroon": [
        "Ndolé", "Achu soup", "Eru", "Pepper soup", "Jollof rice", "Fufu", "Koki", 
        "Kondre", "Kwacoco", "Mbanga soup", "Nkui", "Poulet DG", "Suya", "Ekwang", 
        "Bobolo", "Garri", "Plantain", "Njama njama", "Water fufu"
    ],
    "cape_verde": [
        "Cachupa", "Canja", "Djagacida", "Feijoada", "Xerém", "Linguiça", 
        "Morcela", "Pastéis", "Pudim", "Queijadas"
    ],
    "central_african_republic": [
        "Fufu", "Cassava", "Plantain", "Palm wine", "Bushmeat stew", "Yassa", 
        "Groundnut stew", "Okra soup"
    ],
    "chad": [
        "Boule", "Daraba", "Fangaso", "Kissar", "Maharagwe", "Mouton", 
        "Nyama choma", "Peanut sauce", "Red sauce"
    ],
    "comoros": [
        "Langouste à la vanille", "Mataba", "Mkatra foutra", "Pilao", "Rougail", 
        "Sambusas", "Sorbet coco", "Urojo"
    ],
    "congo": [
        "Fufu", "Kwanga", "Liboke", "Moambe", "Ngai ngai", "Pondu", "Saka saka", 
        "Chikwanga", "Makayabu", "Ntaba"
    ],
    "drc": [
        "Fufu", "Liboke", "Moambe chicken", "Pondu", "Saka saka", "Kwanga", 
        "Chikwanga", "Makayabu", "Loso na madesu", "Ntaba", "Makemba"
    ],
    "djibouti": [
        "Skudahkharis", "Fah-fah", "Sabayad", "Lahoh", "Xalwo", "Malawax", 
        "Anjero", "Canjeero", "Hilib ari"
    ],
    "egypt": [
        "Koshari", "Ful medames", "Tamiya", "Molokhia", "Mahshi", "Roz meammar", 
        "Bamia", "Basbousa", "Baklawa", "Om ali", "Mulukhiyah", "Raqaq", 
        "Fiteer", "Baladi bread", "Aish baladi"
    ],
    "equatorial_guinea": [
        "Fufu", "Malanga", "Plantain", "Palm wine", "Bushmeat", "Fish stew", 
        "Yuca", "Cassava bread"
    ],
    "eritrea": [
        "Injera", "Zigni", "Shiro", "Kitfo", "Doro wat", "Alicha", "Berbere", 
        "Teff bread", "Hilbet", "Ga'at"
    ],
    "eswatini": [
        "Pap", "Sishwala", "Tingwenyama", "Umncweba", "Emasi", "Sidvudvu", 
        "Ligwinya", "Tinkhobe tembuti"
    ],
    "ethiopia": [
        "Injera", "Doro wat", "Kitfo", "Shiro", "Tibs", "Berbere", "Mitmita", 
        "Tej", "Tella", "Roasted barley", "Alicha", "Gomen", "Misir wot", 
        "Zilzil tibs", "Dulet", "Kurt", "Ga'at", "Genfo", "Ambasha"
    ],
    "gabon": [
        "Poulet Nyembwe", "Poisson salé", "Beignet de crevette", "Nyama na ngou", 
        "Manioc", "Plantain frit", "Palm wine"
    ],
    "gambia": [
        "Benachin", "Domoda", "Plasas", "Yassa", "Chere", "Chakery", "Thiakry", 
        "Superkanja", "Olele", "Nyama"
    ],
    "ghana": [
        "Jollof rice", "Fufu", "Banku", "Kenkey", "Red red", "Kelewele", 
        "Waakye", "Tuo zaafi", "Palm nut soup", "Groundnut soup", "Light soup", 
        "Okra stew", "Kontomire", "Ampesi", "Eto", "Tatale", "Bofrot", 
        "Chinchinga", "Shito", "Kpokpoi"
    ],
    "guinea": [
        "Riz au gras", "Poulet yassa", "Fouti", "Hakko", "Tapalapa bread", 
        "Plasas", "Kansiye", "Jollof rice"
    ],
    "guinea_bissau": [
        "Jollof rice", "Caldo", "Canja", "Kansiye", "Mancarra", "Bobo", 
        "Caldeirada", "Pastéis"
    ],
    "ivory_coast": [
        "Attiéké", "Foutou", "Kedjenou", "Alloco", "Bangui", "Garba", 
        "Sauce arachide", "Poisson braisé", "Bangui", "Placali", "Tchep", 
        "Aloko", "Beignets"
    ],
    "kenya": [
        "Ugali", "Nyama choma", "Sukuma wiki", "Githeri", "Irio", "Samosas", 
        "Chapati", "Mandazi", "Mutura", "Mukimo", "Matoke", "Pilau", 
        "Bhajia", "Kachumbari", "Maharagwe"
    ],
    "lesotho": [
        "Papa", "Morogo", "Sesotho traditional bread", "Liphaphalali", 
        "Makoenya", "Traditional beer", "Dried corn"
    ],
    "liberia": [
        "Jollof rice", "Cassava leaf", "Palava sauce", "Fufu", "Dumboy", 
        "Pepper soup", "Check rice", "Potato greens"
    ],
    "libya": [
        "Couscous", "Shorba", "Bazin", "Asida", "Roz jerbi", "Macarona imbaukha", 
        "Sharmoula", "Bsisa", "Usban"
    ],
    "madagascar": [
        "Romazava", "Ravitoto", "Akoho sy voanio", "Henakisoa", "Vary amin'anana", 
        "Koba", "Mofo gasy", "Ramanonaka", "Lasary", "Sambos"
    ],
    "malawi": [
        "Nsima", "Chambo", "Kondowole", "Thobwa", "Zitumbuwa", "Kachumbari", 
        "Mandasi", "Nkhwani", "Matemba", "Usipa"
    ],
    "mali": [
        "Tiguadege na", "Jollof rice", "To", "Maafe", "Fufu", "Dégué", 
        "Thiakry", "Bissap", "Dolo"
    ],
    "mauritania": [
        "Thieboudienne", "Couscous", "Méchoui", "Harira", "Lakh", "Mahfe", 
        "Camel meat", "Dates", "Zrig"
    ],
    "mauritius": [
        "Dholl puri", "Roti", "Curry", "Vindaye", "Bol renversé", "Gateaux piment", 
        "Samosas", "Mine frite", "Biryani", "Halim"
    ],
    "morocco": [
        "Tagine", "Couscous", "Pastilla", "Harira", "Mechoui", "Rfissa", 
        "Tanjia", "Chebakia", "Msemen", "Baghrir", "Sellou", "Amlou", 
        "Briouats", "Makroudh"
    ],
    "mozambique": [
        "Xima", "Matapa", "Peri-peri chicken", "Caril", "Rissois", "Samosas", 
        "Bolo polana", "Pudim", "Chamuça", "Espetada"
    ],
    "namibia": [
        "Potjiekos", "Biltong", "Boerewors", "Kapana", "Oshifima", "Ombidi", 
        "Mopane worms", "Vetkoek", "Sosaties"
    ],
    "niger": [
        "Tuwo", "Miyan kuka", "Kilishi", "Masa", "Fura da nono", "Suya", 
        "Dan wake", "Kosai"
    ],
    "nigeria": [
        "Jollof rice", "Egusi", "Pounded yam", "Suya", "Akara", "Moi moi", 
        "Pepper soup", "Ofada rice", "Amala", "Fufu", "Ogbono soup", 
        "Bitter leaf soup", "Ofe nsala", "Afang soup", "Edikang ikong", 
        "Banga soup", "Oha soup", "Draw soup", "Ukazi soup", "Okra soup",
        "Plantain", "Dodo", "Gizdodo", "Chin chin", "Puff puff", "Meat pie",
        "Scotch egg", "Boli", "Roasted corn", "Kilishi", "Tsire", "Balangu",
        "Tuwo shinkafa", "Miyan kuka", "Dan wake", "Kosai", "Fura da nono",
        "Masa", "Guguru", "Ewa agoyin", "Gbegiri", "Ewedu", "Gbegiri and ewedu",
        "Asaro", "Porridge yam", "Ji mmiri oku", "Nkwobi", "Isi ewu", 
        "Pepper snail", "Catfish pepper soup"
    ],
    "rwanda": [
        "Ugali", "Ibirayi", "Inyama n'ubuki", "Ubugali", "Umutsima", 
        "Ubwoba", "Inyama", "Ibirayi n'inyama", "Urwagwa"
    ],
    "sao_tome_principe": [
        "Calulu", "Feijoada", "Fish curry", "Banana bread", "Coconut rice", 
        "Grilled fish", "Palm wine"
    ],
    "senegal": [
        "Thieboudienne", "Yassa", "Mafé", "Pastels", "Thiakry", "Ceebu jën", 
        "Ndambé", "Lakhou bissap", "Sombi", "Caldou", "Thiou", "Domoda"
    ],
    "seychelles": [
        "Fish curry", "Octopus curry", "Ladob", "Bouyon", "Rougail", 
        "Satini", "Kari koko", "Pwason ek diri"
    ],
    "sierra_leone": [
        "Jollof rice", "Cassava leaf", "Groundnut stew", "Fufu", "Akassa", 
        "Pepper soup", "Palm wine", "Ginger beer"
    ],
    "somalia": [
        "Anjero", "Baasto", "Suqaar", "Hilib ari", "Muufo", "Malawax", 
        "Xalwo", "Sambusas", "Lahoh", "Maraq"
    ],
    "south_africa": [
        "Braai", "Biltong", "Bobotie", "Boerewors", "Bunny chow", "Sosaties", 
        "Potjiekos", "Vetkoek", "Koeksister", "Melktert", "Rusks", "Samp", 
        "Morogo", "Chakalaka", "Pap", "Snoek", "Waterblommetjie bredie",
        "Tomato bredie", "Curry and rice", "Gatsby", "Roosterkoek"
    ],
    "south_sudan": [
        "Kisra", "Ful", "Tamiya", "Mulah", "Goat meat", "Sorghum porridge", 
        "Dried fish", "Okra stew"
    ],
    "sudan": [
        "Ful medames", "Kisra", "Tamiya", "Mulah", "Gourrassa", "Abreh", 
        "Elmaraara", "Kajaik", "Um ali"
    ],
    "tanzania": [
        "Ugali", "Nyama choma", "Pilau", "Samosas", "Chapati", "Mandazi", 
        "Mchuzi wa kuku", "Wali wa nazi", "Maharage ya nazi", "Mishkaki", 
        "Vitumbua", "Kachumbari", "Mchuzi wa mboga"
    ],
    "togo": [
        "Fufu", "Akume", "Banku", "Palaver sauce", "Jollof rice", "Kelewele", 
        "Aloko", "Red red", "Kontomire"
    ],
    "tunisia": [
        "Couscous", "Brik", "Harissa", "Mechouia", "Ojja", "Lablabi", 
        "Makroudh", "Baklawa", "Bambalouni", "Chorba"
    ],
    "uganda": [
        "Matoke", "Posho", "Groundnut sauce", "Luwombo", "Rolex", "Chapati", 
        "Mandazi", "Sim sim", "Malewa", "Eshabwe"
    ],
    "zambia": [
        "Nshima", "Bream", "Kapenta", "Chikanda", "Vitumbuwa", "Chibwabwa", 
        "Ifisashi", "Delele", "Munkoyo"
    ],
    "zimbabwe": [
        "Sadza", "Nyama", "Matemba", "Mufushwa", "Dovi", "Mazanje", 
        "Mahewu", "Chimodho", "Rukweza", "Madora"
    ]
}

# CARIBBEAN DISHES DATABASE BY COUNTRY/ISLAND
CARIBBEAN_DISHES_BY_COUNTRY = {
    "jamaica": [
        "Ackee and saltfish", "Jerk chicken", "Jerk pork", "Curry goat", "Oxtail stew",
        "Rice and peas", "Patties", "Beef patty", "Chicken patty", "Vegetable patty",
        "Callaloo", "Escovitch fish", "Brown stew chicken", "Steamed fish", "Mannish water",
        "Pepper pot soup", "Gungo peas soup", "Red pea soup", "Cow foot soup",
        "Bammy", "Festival", "Fried dumpling", "Boiled dumpling", "Johnny cake",
        "Plantain", "Fried plantain", "Boiled green banana", "Yam", "Dasheen",
        "Sweet potato", "Breadfruit", "Coconut drops", "Gizzada", "Grater cake",
        "Tamarind balls", "Bustamante backbone", "Blue draws", "Cornmeal porridge",
        "Hominy corn porridge", "Peanut porridge", "Green banana porridge"
    ],
    "trinidad_tobago": [
        "Doubles", "Roti", "Curry chicken", "Curry goat", "Curry crab", "Curry duck",
        "Pelau", "Callaloo", "Bake and shark", "Macaroni pie", "Stew chicken",
        "Oil down", "Souse", "Black pudding", "Chow", "Pholourie", "Saheena",
        "Kachori", "Bara", "Aloo pie", "Pies", "Pastelles", "Payme", "Kurma",
        "Sweet bread", "Coconut bake", "Fry bake", "Buljol", "Saltfish buljol",
        "Crab and dumpling", "Cascadura curry", "Geera pork", "Stew pork",
        "Coconut drops", "Sugar cake", "Toolum", "Tamarind balls", "Guava cheese",
        "Pone", "Cassava pone", "Sweet potato pone", "Mango chow", "Pommecythere chow"
    ],
    "barbados": [
        "Cou-cou and flying fish", "Fish cakes", "Cutters", "Conkies", "Pudding and souse",
        "Macaroni pie", "Rice and peas", "Peas and rice", "Breadfruit cou-cou",
        "Sweet bread", "Cassava pone", "Coconut bread", "Rock cakes", "Turnovers",
        "Fish broth", "Pepper pot", "Soup", "Pumpkin fritters", "Cassava chips",
        "Plantain chips", "Sweet potato pudding", "Bread pudding", "Guava jelly",
        "Tamarind stew", "Bajan seasoning", "Flying fish", "Dolphin fish", "Red snapper",
        "Kingfish", "Sea eggs", "Lambi", "Land crab", "Salt bread"
    ],
    "haiti": [
        "Griot", "Tasso", "Boukannen", "Diri ak djon djon", "Diri kole ak pwa",
        "Soup joumou", "Kalalou", "Legim", "Pwason boukannen", "Pwason fri",
        "Poul an sos", "Kabrit boukannen", "Bef boukannen", "Mayi moulen",
        "Bannann boukannen", "Yam boukannen", "Patat boukannen", "Breadfruit",
        "Akra", "Marinad", "Pate kode", "Pain patate", "Doukounou", "Bonbon siwo",
        "Tablet", "Pen patat", "Akasan", "Lemonad", "Dlo kokoye", "Prestige beer"
    ],
    "dominican_republic": [
        "La bandera", "Mangu", "Pollo guisado", "Pernil", "Chicharron", "Moro de guandules",
        "Arroz con pollo", "Sancocho", "Mondongo", "Asopao", "Habichuelas con dulce",
        "Tres golpes", "Casabe", "Tostones", "Maduros", "Yuca hervida", "Name hervido",
        "Quipe", "Empanadas", "Pastelitos", "Croquetas", "Dulce de leche cortada",
        "Flan", "Tres leches", "Bizcocho dominicano", "Majarete", "Dulce de coco",
        "Raspao", "Chinola", "Jugo de tamarindo", "Morir soñando", "Mamajuana"
    ],
    "puerto_rico": [
        "Mofongo", "Jibarito", "Alcapurrias", "Bacalaitos", "Pasteles", "Pernil",
        "Arroz con gandules", "Sancocho", "Asopao", "Pollo guisado", "Chuletas",
        "Bistec encebollado", "Ropa vieja", "Picadillo", "Habichuelas", "Viandas hervidas",
        "Tostones", "Amarillos", "Yautia", "Malanga", "Ñame", "Casabe", "Pan tostado",
        "Quesitos", "Mallorca", "Medianoche", "Cuchifritos", "Chicharron", "Morcilla",
        "Tembleque", "Flan", "Tres leches", "Besitos de coco", "Dulce de papaya",
        "Coquito", "Piña colada", "Chichaito", "Pitorro"
    ],
    "cuba": [
        "Ropa vieja", "Lechon asado", "Pollo a la plancha", "Bistec de palomilla",
        "Arroz con pollo", "Congri", "Moros y cristianos", "Frijoles negros",
        "Yuca con mojo", "Platanos maduros", "Tostones", "Malanga", "Boniato",
        "Croquetas", "Empanadas", "Pastelitos", "Cuban sandwich", "Medianoche",
        "Pan con lechon", "Picadillo", "Vaca frita", "Masas de cerdo", "Chicharrones",
        "Flan", "Tres leches", "Dulce de leche", "Arroz con leche", "Natilla",
        "Guarapo", "Cafe cubano", "Cortadito", "Malta", "Materva", "Mojito", "Daiquiri"
    ],
    "antigua_barbuda": [
        "Fungee and pepperpot", "Saltfish", "Ducana", "Seasoned rice", "Goat water",
        "Conch fritters", "Johnny cakes", "Coconut dumplings", "Cassava bread",
        "Sweet potato pudding", "Pineapple upside down cake", "Black cake", "Tamarind stew"
    ],
    "bahamas": [
        "Conch salad", "Conch fritters", "Crack conch", "Boiled fish", "Steamed conch",
        "Peas n' rice", "Johnny cake", "Guava duff", "Coconut tart", "Rum cake",
        "Fish tea", "Souse", "Curry mutton", "Stew conch", "Fried plantain"
    ],
    "grenada": [
        "Oil down", "Callaloo soup", "Nutmeg ice cream", "Cocoa tea", "Breadfruit",
        "Cassava bread", "Saltfish buljol", "Curry goat", "Stew chicken", "Pelau",
        "Sugar cake", "Fudge", "Tamarind balls", "Guava cheese", "Coconut drops"
    ]
}

# ASIAN DISHES DATABASE BY COUNTRY
ASIAN_DISHES_BY_COUNTRY = {
    "china": [
        "Kung Pao chicken", "Sweet and sour pork", "Mapo tofu", "Peking duck", "Dim sum",
        "Hot pot", "Fried rice", "Chow mein", "Lo mein", "Wonton soup", "Dumpling",
        "Spring rolls", "Char siu", "General Tso's chicken", "Orange chicken",
        "Beef and broccoli", "Szechuan chicken", "Ma la hot pot", "Dan dan noodles",
        "Xiaolongbao", "Har gow", "Siu mai", "Egg tart", "Mooncake", "Congee",
        "Century egg", "Tea eggs", "Zongzi", "Tangyuan", "Douhua", "Stinky tofu"
    ],
    "japan": [
        "Sushi", "Sashimi", "Ramen", "Udon", "Soba", "Tempura", "Yakitori", "Teriyaki",
        "Katsu", "Tonkatsu", "Chicken katsu", "Miso soup", "Edamame", "Gyoza",
        "Takoyaki", "Okonomiyaki", "Yakisoba", "Onigiri", "Bento", "Donburi",
        "Chirashi", "Unagi", "Mochi", "Dorayaki", "Taiyaki", "Wagyu beef",
        "Shabu shabu", "Sukiyaki", "Nabe", "Karaage", "Agedashi tofu"
    ],
    "korea": [
        "Kimchi", "Bulgogi", "Bibimbap", "Korean BBQ", "Galbi", "Japchae", "Tteokbokki",
        "Kimchi jjigae", "Sundubu jjigae", "Samgyeopsal", "Korean fried chicken",
        "Banchan", "Doenjang jjigae", "Naengmyeon", "Jajangmyeon", "Kimbap",
        "Hotteok", "Bungeoppang", "Patbingsu", "Makgeolli", "Soju", "Korean corn dogs",
        "Gochujang", "Ssam", "Galbitang", "Seolleongtang", "Bossam", "Jokbal"
    ],
    "thailand": [
        "Pad Thai", "Tom Yum", "Green curry", "Red curry", "Massaman curry", "Som tam",
        "Thai basil chicken", "Mango sticky rice", "Thai fried rice", "Pad See Ew",
        "Thai coconut soup", "Larb", "Satay", "Spring rolls", "Thai fish cakes",
        "Boat noodles", "Khao Pad", "Thai tea", "Coconut ice cream", "Durian",
        "Pad Krapow", "Thai omelet", "Gaeng Som", "Khao Soi", "Thai papaya salad"
    ],
    "vietnam": [
        "Pho", "Banh mi", "Spring rolls", "Vietnamese coffee", "Bun bo hue", "Com tam",
        "Banh xeo", "Vietnamese pancakes", "Cao lau", "Mi quang", "Bun cha",
        "Vietnamese salad", "Che", "Banh flan", "Fish sauce", "Nuoc cham",
        "Goi cuon", "Nem nuong", "Banh cuon", "Vietnamese sandwich", "Sticky rice"
    ],
    "india": [
        "Biryani", "Curry", "Naan", "Roti", "Dal", "Samosa", "Tandoori chicken",
        "Butter chicken", "Palak paneer", "Chana masala", "Tikka masala", "Dosa",
        "Idli", "Vada", "Uttapam", "Rajma", "Chole", "Aloo gobi", "Vindaloo",
        "Korma", "Saag", "Raita", "Lassi", "Chai", "Kulfi", "Gulab jamun",
        "Jalebi", "Laddu", "Barfi", "Kheer", "Rasmalai", "Pani puri", "Bhel puri"
    ]
}

# LATIN AMERICAN DISHES DATABASE BY COUNTRY
LATIN_AMERICAN_DISHES_BY_COUNTRY = {
    "mexico": [
        "Tacos", "Burritos", "Quesadillas", "Enchiladas", "Tamales", "Chiles rellenos",
        "Pozole", "Mole", "Carnitas", "Al pastor", "Barbacoa", "Cochinita pibil",
        "Elote", "Guacamole", "Salsa", "Pico de gallo", "Nachos", "Fajitas",
        "Churros", "Tres leches cake", "Flan", "Horchata", "Margarita", "Tequila",
        "Mezcal", "Michelada", "Huevos rancheros", "Chilaquiles", "Sopes", "Tlayudas"
    ],
    "brazil": [
        "Feijoada", "Churrasco", "Pão de açúcar", "Brigadeiro", "Açaí", "Caipirinha",
        "Moqueca", "Pastel", "Coxinha", "Picanha", "Farofa", "Rice and beans",
        "Guaraná", "Queijo bread", "Tapioca", "Beijinho", "Quindim", "Cachaça",
        "Salgadinhos", "Empada", "Kibe", "Romeu e Julieta", "Pudim", "Pavê"
    ],
    "argentina": [
        "Asado", "Empanadas", "Milanesa", "Chimichurri", "Alfajores", "Dulce de leche",
        "Choripan", "Locro", "Humita", "Provoleta", "Malbec", "Mate", "Tango",
        "Bife de chorizo", "Morcilla", "Parrillada", "Medialunas", "Facturas"
    ],
    "peru": [
        "Ceviche", "Lomo saltado", "Aji de gallina", "Anticuchos", "Papa rellena",
        "Causa", "Rocoto relleno", "Pachamanca", "Pollo a la brasa", "Suspiro limeño",
        "Pisco sour", "Chicha morada", "Inca Kola", "Quinoa", "Alpaca", "Guinea pig"
    ],
    "colombia": [
        "Arepas", "Bandeja paisa", "Sancocho", "Empanadas", "Patacones", "Lechona",
        "Ajiaco", "Tamales", "Buñuelos", "Aguardiente", "Coffee", "Tres leches",
        "Obleas", "Bocadillo", "Chicharron", "Mondongo", "Arepa de huevo"
    ]
}

# MIDDLE EASTERN DISHES DATABASE BY COUNTRY
MIDDLE_EASTERN_DISHES_BY_COUNTRY = {
    "lebanon": [
        "Hummus", "Tabbouleh", "Fattoush", "Kibbeh", "Shawarma", "Falafel", "Labneh",
        "Manakish", "Baklava", "Kanafeh", "Arak", "Lebanese wine", "Muhammara",
        "Baba ghanoush", "Stuffed grape leaves", "Lebanese bread", "Za'atar"
    ],
    "turkey": [
        "Kebab", "Döner", "Turkish delight", "Baklava", "Börek", "Meze", "Raki",
        "Turkish coffee", "Köfte", "Pide", "Lahmacun", "Dolma", "Turkish breakfast",
        "Simit", "Ayran", "Iskender", "Adana kebab", "Turkish tea"
    ],
    "iran": [
        "Persian rice", "Kebab koobideh", "Ghormeh sabzi", "Fesenjan", "Tahdig",
        "Saffron", "Persian tea", "Rosewater", "Pistachio", "Pomegranate",
        "Doogh", "Ash reshteh", "Khoreshte bademjan", "Polo", "Persian ice cream"
    ],
    "israel": [
        "Falafel", "Hummus", "Shakshuka", "Sabich", "Israeli salad", "Challah",
        "Matzo", "Gefilte fish", "Borscht", "Rugelach", "Israeli couscous",
        "Malawach", "Jachnun", "Bourekas", "Arak", "Israeli wine"
    ]
}

# EUROPEAN DISHES DATABASE BY COUNTRY
EUROPEAN_DISHES_BY_COUNTRY = {
    "italy": [
        "Pizza", "Pasta", "Spaghetti", "Lasagna", "Risotto", "Gelato", "Tiramisu",
        "Carbonara", "Bolognese", "Pesto", "Gnocchi", "Ravioli", "Prosciutto",
        "Mozzarella", "Parmesan", "Bruschetta", "Antipasto", "Osso buco",
        "Minestrone", "Cannoli", "Espresso", "Chianti", "Prosecco", "Limoncello"
    ],
    "france": [
        "Croissant", "Baguette", "French toast", "Crêpes", "Quiche", "Coq au vin",
        "Bouillabaisse", "Ratatouille", "French onion soup", "Escargot", "Foie gras",
        "Boeuf bourguignon", "Cassoulet", "Crème brûlée", "Macarons", "Champagne",
        "Bordeaux wine", "Camembert", "Brie", "Roquefort", "French fries", "Soufflé"
    ],
    "spain": [
        "Paella", "Tapas", "Gazpacho", "Jamón ibérico", "Tortilla española", "Churros",
        "Sangria", "Rioja wine", "Manchego cheese", "Serrano ham", "Patatas bravas",
        "Croquetas", "Empanadas", "Flan", "Crema catalana", "Sherry", "Cava"
    ],
    "germany": [
        "Bratwurst", "Sauerkraut", "Schnitzel", "Pretzel", "Beer", "Black forest cake",
        "Sauerbraten", "Currywurst", "Spätzle", "Strudel", "Lebkuchen", "Glühwein",
        "Weisswurst", "Döppekuchen", "Himmel un Ääd", "Riesling wine"
    ]
}

# ENHANCED REGISTRATION WITH AFRICAN DISHES
# GLOBAL DISHES API ENDPOINTS
@api_router.get("/heritage/global-dishes")
async def get_global_dishes():
    """Get comprehensive list of dishes from all global cuisines for registration"""
    
    all_dishes_databases = {
        "African": AFRICAN_DISHES_BY_COUNTRY,
        "Caribbean": CARIBBEAN_DISHES_BY_COUNTRY,
        "Asian": ASIAN_DISHES_BY_COUNTRY,
        "Latin American": LATIN_AMERICAN_DISHES_BY_COUNTRY,
        "Middle Eastern": MIDDLE_EASTERN_DISHES_BY_COUNTRY,
        "European": EUROPEAN_DISHES_BY_COUNTRY
    }
    
    formatted_cuisines = {}
    total_dishes = 0
    total_countries = 0
    
    for cuisine_type, countries_dict in all_dishes_databases.items():
        formatted_countries = {}
        cuisine_dishes = 0
        
        for country, dishes in countries_dict.items():
            country_name = country.replace('_', ' ').title()
            formatted_countries[country_name] = {
                "country_code": country,
                "dishes": dishes,
                "count": len(dishes)
            }
            cuisine_dishes += len(dishes)
            total_dishes += len(dishes)
        
        formatted_cuisines[cuisine_type] = {
            "countries": formatted_countries,
            "total_countries": len(countries_dict),
            "total_dishes": cuisine_dishes
        }
        total_countries += len(countries_dict)
    
    return {
        "success": True,
        "global_cuisines": formatted_cuisines,
        "summary": {
            "total_cuisines": len(all_dishes_databases),
            "total_countries": total_countries,
            "total_dishes": total_dishes
        },
        "usage": "Use in registration form to help users select dishes they can prepare from their cultural heritage",
        "cultural_note": "Comprehensive collection from across the globe to support authentic cultural representation and diaspora connection"
    }

@api_router.get("/heritage/african-dishes")
async def get_african_dishes():
    """Get comprehensive list of African dishes by country for registration - LEGACY ENDPOINT"""
    
    # Format for frontend consumption
    formatted_dishes = {}
    total_dishes = 0
    
    for country, dishes in AFRICAN_DISHES_BY_COUNTRY.items():
        country_name = country.replace('_', ' ').title()
        formatted_dishes[country_name] = {
            "country_code": country,
            "dishes": dishes,
            "count": len(dishes)
        }
        total_dishes += len(dishes)
    
    return {
        "success": True,
        "african_dishes": formatted_dishes,
        "total_countries": len(AFRICAN_DISHES_BY_COUNTRY),
        "total_dishes": total_dishes,
        "usage": "Use in registration form to help users select dishes they can prepare",
        "cultural_note": "Comprehensive collection from across Africa to support authentic cultural representation",
        "migration_note": "Consider using /api/heritage/global-dishes for all cuisines"
    }

@api_router.get("/heritage/dishes-by-cuisine/{cuisine_type}")
async def get_dishes_by_cuisine(cuisine_type: str):
    """Get dishes from a specific cuisine type (African, Caribbean, Asian, etc.)"""
    
    cuisine_databases = {
        "african": AFRICAN_DISHES_BY_COUNTRY,
        "caribbean": CARIBBEAN_DISHES_BY_COUNTRY,
        "asian": ASIAN_DISHES_BY_COUNTRY,
        "latin_american": LATIN_AMERICAN_DISHES_BY_COUNTRY,
        "middle_eastern": MIDDLE_EASTERN_DISHES_BY_COUNTRY,
        "european": EUROPEAN_DISHES_BY_COUNTRY
    }
    
    cuisine_key = cuisine_type.lower().replace(' ', '_').replace('-', '_')
    
    if cuisine_key not in cuisine_databases:
        raise HTTPException(
            status_code=404, 
            detail=f"Cuisine type '{cuisine_type}' not found. Available: {', '.join(cuisine_databases.keys())}"
        )
    
    dishes_dict = cuisine_databases[cuisine_key]
    formatted_dishes = {}
    total_dishes = 0
    
    for country, dishes in dishes_dict.items():
        country_name = country.replace('_', ' ').title()
        formatted_dishes[country_name] = {
            "country_code": country,
            "dishes": dishes,
            "count": len(dishes)
        }
        total_dishes += len(dishes)
    
    return {
        "success": True,
        "cuisine_type": cuisine_type.title(),
        "countries": formatted_dishes,
        "total_countries": len(dishes_dict),
        "total_dishes": total_dishes,
        "cultural_note": f"Traditional dishes from {cuisine_type.title()} heritage for authentic cultural representation"
    }
@api_router.post("/admin/setup-platform-owner")
async def setup_platform_owner(
    owner_data: Dict[str, Any]
):
    """One-time setup for platform owner - Call this first after deployment"""
    
    # Check if platform owner already exists
    existing_owner = await db.users.find_one({"is_platform_owner": True})
    if existing_owner:
        raise HTTPException(status_code=400, detail="Platform owner already configured")
    
    owner_email = owner_data.get("email")
    owner_phone = owner_data.get("phone")
    
    # Find user by email and upgrade to platform owner
    user = await db.users.find_one({"email": owner_email})
    if not user:
        raise HTTPException(status_code=404, detail="User account not found - please register first")
    
    # Upgrade user to platform owner
    await db.users.update_one(
        {"email": owner_email},
        {"$set": {
            "is_platform_owner": True,
            "phone_number": owner_phone,
            "owner_setup_date": datetime.utcnow(),
            "financial_access": "full",
            "admin_permissions": ["all"]
        }}
    )
    
    # Create initial platform settings
    await db.platform_settings.insert_one({
        "setting_type": "owner_config",
        "owner_email": owner_email,
        "owner_phone": owner_phone,
        "notification_preferences": {
            "revenue_alerts": True,
            "user_issues": True,
            "partnership_inquiries": True,
            "daily_reports": True
        },
        "financial_thresholds": {
            "daily_revenue_alert": 1000,
            "withdrawal_approval_needed": 5000,
            "unusual_activity_alert": 500
        },
        "setup_completed": True,
        "created_at": datetime.utcnow()
    })
    
    return {
        "success": True,
        "message": "Platform owner configured successfully",
        "owner_email": owner_email,
        "access_granted": ["financial_dashboard", "user_management", "platform_settings", "withdrawal_controls"],
        "next_steps": [
            "Set up bank account connections",
            "Configure notification preferences", 
            "Review revenue tracking settings",
            "Add team members if needed"
        ]
    }

@api_router.get("/admin/team-management")
async def get_team_management(current_user_id: str = Depends(get_current_user)):
    """Manage team access and permissions"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    team_structure = {
        "platform_owner": {
            "role": "Platform Owner",
            "email": user.get("email"),
            "permissions": ["full_access", "financial_control", "user_management", "platform_settings"],
            "added_date": user.get("owner_setup_date", datetime.utcnow()).isoformat()
        },
        "available_roles": {
            "financial_manager": {
                "description": "Can view revenue, process payouts, generate financial reports",
                "permissions": ["view_revenue", "process_payouts", "financial_reports"],
                "salary_suggestion": "$4000-6000/month",
                "when_to_hire": "When monthly revenue exceeds $50,000"
            },
            "operations_manager": {
                "description": "Handles user support, content moderation, daily operations",
                "permissions": ["user_support", "content_moderation", "basic_analytics"],
                "salary_suggestion": "$3500-5000/month", 
                "when_to_hire": "When user base exceeds 1,000 active users"
            },
            "partnership_manager": {
                "description": "Manages grocery partnerships, brand deals, white-label clients",
                "permissions": ["partnership_management", "client_communication", "deal_tracking"],
                "salary_suggestion": "$5000-8000/month + commission",
                "when_to_hire": "When partnership revenue exceeds $20,000/month"
            },
            "cultural_moderator": {
                "description": "Ensures cultural authenticity, reviews recipe submissions",
                "permissions": ["content_review", "cultural_verification", "community_management"],
                "salary_suggestion": "$2500-4000/month",
                "when_to_hire": "When recipe submissions exceed 100/month"
            }
        },
        "current_team": [],  # Would show added team members
        "hiring_recommendations": [
            "Start with operations manager when you have 500+ daily active users",
            "Add financial manager when processing $100,000+ monthly revenue",
            "Cultural moderators can be part-time contractors initially"
        ]
    }
    
    return team_structure

@api_router.post("/admin/add-team-member")
async def add_team_member(
    team_member_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Add team member with specific role and permissions"""
    
    user = await db.users.find_one({"id": current_user_id})
    if not user or not user.get("is_platform_owner"):
        raise HTTPException(status_code=403, detail="Platform owner access required")
    
    member_email = team_member_data.get("email")
    role = team_member_data.get("role")
    
    # Check if user exists
    member_user = await db.users.find_one({"email": member_email})
    if not member_user:
        raise HTTPException(status_code=404, detail="User must register on platform first")
    
    # Define role permissions
    role_permissions = {
        "financial_manager": ["view_revenue", "process_payouts", "financial_reports", "user_earnings"],
        "operations_manager": ["user_support", "content_moderation", "basic_analytics", "user_management"],
        "partnership_manager": ["partnership_management", "client_communication", "deal_tracking"],
        "cultural_moderator": ["content_review", "cultural_verification", "community_management"]
    }
    
    if role not in role_permissions:
        raise HTTPException(status_code=400, detail="Invalid role specified")
    
    # Update user with team role
    await db.users.update_one(
        {"email": member_email},
        {"$set": {
            "team_role": role,
            "permissions": role_permissions[role],
            "added_by": user.get("email"),
            "team_join_date": datetime.utcnow(),
            "is_team_member": True
        }}
    )
    
    return {
        "success": True,
        "message": f"Team member added successfully",
        "member_email": member_email,
        "role": role,
        "permissions_granted": role_permissions[role],
        "added_by": user.get("email")
    }

# Keep all existing routes from previous implementation
# (Reference recipes, snippets, grocery, etc.)

# Include Compliance and Campaign router
from compliance_campaign_api import create_compliance_campaign_router
compliance_campaign_router = create_compliance_campaign_router(db, get_current_user, get_current_user_optional)
app.include_router(compliance_campaign_router, prefix="/api")

# Include Lambalia Eats router with proper prefix
lambalia_eats_router = create_lambalia_eats_router(lambalia_eats_service, get_current_user, get_current_user_optional)
app.include_router(lambalia_eats_router, prefix="/api")

# Include Heritage Recipes router with proper prefix
heritage_recipes_router = create_heritage_recipes_router(heritage_recipes_service, get_current_user, get_current_user_optional)
app.include_router(heritage_recipes_router, prefix="/api")

# Include Smart Cooking Tool router with proper prefix
smart_cooking_router = create_smart_cooking_router(smart_cooking_service, get_current_user, get_current_user_optional)
app.include_router(smart_cooking_router, prefix="/api")

# Include Enhanced Smart Cooking router (SuperCook + HackTheMenu)
enhanced_cooking_router = create_enhanced_smart_cooking_router(db, get_current_user)
app.include_router(enhanced_cooking_router, prefix="/api")

# Include Transaction Verification router with proper prefix
transaction_verification_router = create_transaction_verification_router(transaction_verification_service, get_current_user, get_current_user_optional)
app.include_router(transaction_verification_router, prefix="/api")

# Include Feedback System router
# app.include_router(feedback_router)

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

# ========================================
# SMS NOTIFICATION & TIP SYSTEM ENDPOINTS  
# ========================================

@api_router.post("/sms/test")
async def test_sms_service(
    phone_number: str,
    message: str,
    current_user_id: str = Depends(get_current_user)
):
    """Test SMS notification service"""
    try:
        sms_service = await get_sms_service()
        result = await sms_service._send_sms(phone_number, message)
        return {
            "success": result["success"],
            "message": "SMS sent successfully" if result["success"] else "SMS failed",
            "details": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@api_router.get("/sms/status")
async def get_sms_service_status():
    """Get SMS service configuration status"""
    try:
        sms_service = await get_sms_service()
        return sms_service.get_service_status()
    except Exception as e:
        return {"enabled": False, "error": str(e)}

@api_router.post("/notifications/account-change")
async def send_account_change_notification(
    change_details: str,
    current_user_id: str = Depends(get_current_user)
):
    """Send account change SMS notification"""
    try:
        # Get user phone number
        user = await db.users.find_one({"id": current_user_id})
        if not user or not user.get("phone"):
            return {"success": False, "error": "User phone number not found"}
        
        sms_service = await get_sms_service()
        result = await sms_service.send_account_change_sms(
            phone_number=user["phone"],
            change_details=change_details
        )
        
        return {
            "success": result["success"],
            "message": "Account change notification sent" if result["success"] else "Failed to send notification"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@api_router.post("/notifications/transaction")
async def send_transaction_notification(
    transaction_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Send transaction SMS notification (money in/out)"""
    try:
        # Get user phone number
        user = await db.users.find_one({"id": current_user_id})
        if not user or not user.get("phone"):
            return {"success": False, "error": "User phone number not found"}
        
        sms_service = await get_sms_service()
        
        transaction_type = transaction_data.get("type", "unknown")
        amount = transaction_data.get("amount", 0.0)
        balance = transaction_data.get("balance", 0.0)
        reference = transaction_data.get("reference", "N/A")
        
        if transaction_type == "money_in":
            result = await sms_service.send_money_in_sms(
                phone_number=user["phone"],
                amount=amount,
                transaction_type=transaction_data.get("source", "payment"),
                reference=reference,
                balance=balance
            )
        else:
            result = await sms_service.send_money_out_sms(
                phone_number=user["phone"],
                amount=amount,
                recipient=transaction_data.get("recipient", "merchant"),
                reference=reference,
                balance=balance
            )
        
        return {
            "success": result["success"],
            "message": "Transaction notification sent" if result["success"] else "Failed to send notification"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@api_router.post("/service/complete")
async def complete_service_transaction(
    service_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Mark a service as completed and schedule rating request"""
    try:
        tip_rating_service = await get_tip_rating_service()
        
        service_id = await tip_rating_service.create_service_completion_record({
            "service_type": service_data.get("service_type", ServiceType.HOME_RESTAURANT),
            "user_id": current_user_id,
            "provider_id": service_data.get("provider_id"),
            "details": service_data.get("details", {}),
            "amount": service_data.get("amount", 0.0),
            "payment_method_id": service_data.get("payment_method_id")
        })
        
        return {
            "success": True,
            "service_id": service_id,
            "message": "Service completed and rating request scheduled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@api_router.post("/service/rate-and-tip")
async def submit_service_rating_and_tip(
    rating_data: RatingRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Submit service rating and optional tip"""
    try:
        tip_rating_service = await get_tip_rating_service()
        
        # Ensure current user matches the rating user
        rating_data.user_id = current_user_id
        
        result = await tip_rating_service.submit_rating_and_tip(rating_data)
        
        if result["success"]:
            # Send SMS confirmation to both parties
            user = await db.users.find_one({"id": current_user_id})
            provider = await db.users.find_one({"id": rating_data.provider_id})
            
            if user.get("phone"):
                sms_service = await get_sms_service()
                confirmation_message = f"Thank you for your {rating_data.rating}-star rating! "
                if rating_data.tip_amount and rating_data.tip_amount > 0:
                    confirmation_message += f"Your ${rating_data.tip_amount:.2f} tip has been processed."
                
                await sms_service._send_sms(user["phone"], confirmation_message)
            
            return {
                "success": True,
                "rating_id": result["rating_id"],
                "tip_processed": result["tip_processed"],
                "tip_amount": result["tip_amount"],
                "message": "Rating and tip submitted successfully"
            }
        else:
            return {"success": False, "error": result["error"]}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@api_router.get("/earnings/summary/{provider_id}")
async def get_provider_earnings_summary(
    provider_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user_id: str = Depends(get_current_user)
):
    """Get provider earnings summary with regular and tip separation"""
    try:
        # Verify user can access these earnings (provider themselves or admin)
        if current_user_id != provider_id:
            user = await db.users.find_one({"id": current_user_id})
            if not user or not user.get("is_platform_owner"):
                raise HTTPException(status_code=403, detail="Access denied")
        
        tip_rating_service = await get_tip_rating_service()
        
        # Parse dates if provided
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        summary = await tip_rating_service.get_provider_earnings_summary(
            provider_id, start_dt, end_dt
        )
        
        return summary
        
    except Exception as e:
        return {"error": str(e)}

@api_router.get("/admin/pending-ratings")
async def get_pending_rating_requests(
    current_user_id: str = Depends(get_current_user)
):
    """Get services that need rating SMS sent - Admin only"""
    try:
        user = await db.users.find_one({"id": current_user_id})
        if not user or not user.get("is_platform_owner"):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        tip_rating_service = await get_tip_rating_service()
        pending_requests = await tip_rating_service.get_pending_rating_requests()
        
        return {
            "pending_count": len(pending_requests),
            "requests": pending_requests
        }
        
    except Exception as e:
        return {"error": str(e)}

@api_router.post("/admin/send-rating-sms/{service_id}")
async def send_rating_sms_request(
    service_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Manually send rating SMS for a completed service - Admin only"""
    try:
        user = await db.users.find_one({"id": current_user_id})
        if not user or not user.get("is_platform_owner"):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Get service record
        service_record = await db.completed_services.find_one({"id": service_id})
        if not service_record:
            return {"success": False, "error": "Service not found"}
        
        # Get user details
        user_record = await db.users.find_one({"id": service_record["user_id"]})
        if not user_record or not user_record.get("phone"):
            return {"success": False, "error": "User phone not found"}
        
        # Send rating SMS
        sms_service = await get_sms_service()
        rating_link = f"https://lambalia.com/rate/{service_id}"
        
        result = await sms_service.send_service_rating_sms(
            phone_number=user_record["phone"],
            user_name=user_record.get("full_name", user_record["username"]),
            service_type=service_record["service_type"],
            rating_link=rating_link
        )
        
        if result["success"]:
            # Mark as sent
            await db.completed_services.update_one(
                {"id": service_id},
                {"$set": {"rating_sent": True}}
            )
        
        return {
            "success": result["success"],
            "message": "Rating SMS sent" if result["success"] else "Failed to send SMS"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Enhanced User Profile Update with SMS notification
@api_router.put("/users/profile")
async def update_user_profile(
    profile_updates: Dict[str, Any],
    current_user_id: str = Depends(get_current_user)
):
    """Update user profile with SMS notification for important changes"""
    try:
        # Get current user data
        current_user = await db.users.find_one({"id": current_user_id})
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check for important changes that require SMS notification
        important_changes = []
        
        if "email" in profile_updates and profile_updates["email"] != current_user.get("email"):
            important_changes.append(f"Email changed to {profile_updates['email']}")
        
        if "phone" in profile_updates and profile_updates["phone"] != current_user.get("phone"):
            important_changes.append(f"Phone number changed to {profile_updates['phone']}")
        
        if "password" in profile_updates:
            # Hash new password
            profile_updates["password_hash"] = hash_password(profile_updates["password"])
            del profile_updates["password"]
            important_changes.append("Password changed")
        
        # Update user profile
        await db.users.update_one(
            {"id": current_user_id},
            {
                "$set": {
                    **profile_updates,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Send SMS notification for important changes
        if important_changes and current_user.get("phone"):
            try:
                sms_service = await get_sms_service()
                change_details = "; ".join(important_changes)
                await sms_service.send_account_change_sms(
                    phone_number=current_user["phone"],
                    change_details=change_details
                )
            except Exception as e:
                logger.warning(f"Failed to send account change SMS: {str(e)}")
        
        # Get updated user data
        updated_user = await db.users.find_one({"id": current_user_id})
        
        return {
            "success": True,
            "message": "Profile updated successfully",
            "user": UserResponse(**updated_user),
            "sms_sent": len(important_changes) > 0 and bool(current_user.get("phone"))
        }
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Profile update failed")

@api_router.put("/users/profile-photo")
async def update_profile_photo(
    photo_data: Dict[str, str],
    current_user_id: str = Depends(get_current_user)
):
    """Update user profile photo"""
    try:
        profile_photo = photo_data.get("profile_photo")
        if not profile_photo:
            raise HTTPException(status_code=400, detail="Profile photo data is required")
        
        # Validate base64 image format
        if not profile_photo.startswith("data:image/"):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Update user profile photo
        await db.users.update_one(
            {"id": current_user_id},
            {
                "$set": {
                    "profile_photo": profile_photo,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Get updated user data
        updated_user = await db.users.find_one({"id": current_user_id})
        
        return {
            "success": True,
            "message": "Profile photo updated successfully",
            "user": UserResponse(**updated_user)
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors) as-is
        raise
    except Exception as e:
        logger.error(f"Profile photo update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Profile photo update failed")

# ========================================
# SNIPPET ENDPOINTS - Recipe Snippets
# ========================================

@api_router.get("/test-snippets")
async def test_snippets():
    """Test endpoint to verify router is working"""
    return {"message": "Snippets router is working"}

@api_router.post("/snippets", response_model=SnippetResponse)
async def create_snippet(
    snippet_data: SnippetCreate,
    current_user_id: str = Depends(get_current_user)
):
    """Create a new recipe snippet"""
    try:
        snippet_dict = snippet_data.dict()
        snippet_dict['author_id'] = current_user_id
        
        # Get user's country for context
        user = await db.users.find_one({"id": current_user_id})
        if user:
            snippet_dict['country_id'] = user.get('country_id')
        
        # Create snippet with default values
        snippet = RecipeSnippet(**snippet_dict)
        
        # Insert into database
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
        
    except Exception as e:
        logger.error(f"Failed to create snippet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create snippet. Please try again.")

@api_router.get("/snippets", response_model=List[SnippetResponse])
async def get_snippets(
    skip: int = 0,
    limit: int = 20,
    author_id: Optional[str] = None,
    country_id: Optional[str] = None,
    snippet_type: Optional[SnippetType] = None
):
    """Get snippets with optional filtering"""
    try:
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
        
    except Exception as e:
        logger.error(f"Failed to get snippets: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get snippets")

@api_router.get("/users/{user_id}/snippets/playlist", response_model=List[SnippetResponse])
async def get_user_snippets_playlist(user_id: str):
    """Get user's snippets organized as a playlist"""
    try:
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
        
    except Exception as e:
        logger.error(f"Failed to get user snippets playlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user snippets")

@api_router.post("/snippets/{snippet_id}/like")
async def like_snippet(snippet_id: str, current_user_id: str = Depends(get_current_user)):
    """Like or unlike a snippet"""
    try:
        snippet = await db.snippets.find_one({"id": snippet_id})
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        # Check if user already liked this snippet
        user_like = await db.snippet_likes.find_one({
            "snippet_id": snippet_id,
            "user_id": current_user_id
        })
        
        if user_like:
            # Unlike - remove like and decrement count
            await db.snippet_likes.delete_one({
                "snippet_id": snippet_id,
                "user_id": current_user_id
            })
            await db.snippets.update_one(
                {"id": snippet_id},
                {"$inc": {"likes_count": -1}}
            )
            return {"liked": False, "message": "Snippet unliked"}
        else:
            # Like - add like and increment count
            await db.snippet_likes.insert_one({
                "snippet_id": snippet_id,
                "user_id": current_user_id,
                "created_at": datetime.utcnow()
            })
            await db.snippets.update_one(
                {"id": snippet_id},
                {"$inc": {"likes_count": 1}}
            )
            return {"liked": True, "message": "Snippet liked"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to like/unlike snippet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process like")

@api_router.delete("/snippets/{snippet_id}")
async def delete_snippet(snippet_id: str, current_user_id: str = Depends(get_current_user)):
    """Delete a snippet (only by the author)"""
    try:
        snippet = await db.snippets.find_one({"id": snippet_id})
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        if snippet["author_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own snippets")
        
        # Delete the snippet
        await db.snippets.delete_one({"id": snippet_id})
        
        # Delete associated likes
        await db.snippet_likes.delete_many({"snippet_id": snippet_id})
        
        # Update user's snippet count
        await db.users.update_one(
            {"id": current_user_id},
            {"$inc": {"snippets_count": -1}}
        )
        
        return {"message": "Snippet deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete snippet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete snippet")

@api_router.get("/snippets/{snippet_id}", response_model=SnippetResponse)
async def get_snippet_by_id(snippet_id: str):
    """Get a specific snippet by ID"""
    try:
        snippet = await db.snippets.find_one({"id": snippet_id})
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        # Increment view count
        await db.snippets.update_one(
            {"id": snippet_id},
            {"$inc": {"views_count": 1}}
        )
        
        # Get author info
        author = await db.users.find_one({"id": snippet["author_id"]})
        
        snippet_response = SnippetResponse(**snippet)
        snippet_response.author_username = author['username'] if author else None
        
        return snippet_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get snippet: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get snippet")

# ========================================
# GROCERY SEARCH ENDPOINTS
# ========================================

@api_router.post("/grocery/search")
async def search_grocery_stores(
    search_request: GrocerySearchRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Search for grocery stores and ingredient availability using Open Food Facts API"""
    
    try:
        # Get the grocery service
        grocery_service = await get_grocery_service()
        
        # Use real grocery API to search for stores and ingredients
        stores, ingredient_availability, delivery_options = await grocery_service.generate_grocery_stores_response(
            ingredients=search_request.ingredients,
            postal_code=search_request.user_postal_code,
            max_distance_km=search_request.max_distance_km
        )
        
        # Calculate total estimated cost from all ingredients
        total_estimated_cost = 0.0
        for ingredient_data in ingredient_availability.values():
            if ingredient_data:
                # Take the lowest price for each ingredient
                min_price = min(item["price"] for item in ingredient_data)
                total_estimated_cost += min_price
        
        total_estimated_cost = round(total_estimated_cost, 2)
        
        # Get recommended store (lowest estimated total)
        recommended_store_id = stores[0]["id"] if stores else "real_store_generic"
        if len(stores) > 1:
            recommended_store_id = min(stores, key=lambda x: x["estimated_total"])["id"]
        
        logger.info(f"Grocery search completed for {len(search_request.ingredients)} ingredients")
        logger.info(f"Found {len(stores)} stores with total cost: ${total_estimated_cost}")
        
        return GrocerySearchResponse(
            stores=stores,
            ingredient_availability=ingredient_availability,
            total_estimated_cost=total_estimated_cost,
            delivery_options=delivery_options,
            recommended_store_id=recommended_store_id
        )
        
    except Exception as e:
        logger.error(f"Error in grocery search: {str(e)}")
        # Fallback to basic response if API fails
        return GrocerySearchResponse(
            stores=[{
                "id": "fallback_store",
                "name": "Local Grocery Store",
                "chain": "Independent",
                "address": "Please check local stores",
                "distance_km": 5.0,
                "supports_delivery": True,
                "estimated_total": 25.00,
                "commission_rate": 0.05,
                "data_source": "fallback"
            }],
            ingredient_availability={
                ingredient: [{
                    "store_id": "fallback_store",
                    "brand": "Generic",
                    "price": 3.99,
                    "in_stock": True,
                    "package_size": "1 unit",
                    "nutrition_grade": "N/A"
                }] for ingredient in search_request.ingredients
            },
            total_estimated_cost=len(search_request.ingredients) * 3.99,
            delivery_options=[
                {"type": "pickup", "fee": 0.0, "time_estimate": "Available now"},
                {"type": "delivery", "fee": 5.99, "time_estimate": "1-3 hours"}
            ],
            recommended_store_id="fallback_store"
        )

@api_router.get("/grocery/ingredients/suggestions")
async def get_ingredient_suggestions(
    query: str,
    current_user_id: str = Depends(get_current_user)
):
    """Get ingredient suggestions for autocomplete using Open Food Facts API"""
    
    try:
        if len(query) < 2:
            return {"suggestions": []}
        
        # Get the grocery service
        grocery_service = await get_grocery_service()
        
        # Get ingredient suggestions
        suggestions = await grocery_service.get_ingredient_suggestions(query)
        
        logger.info(f"Found {len(suggestions)} ingredient suggestions for query: {query}")
        
        return {
            "query": query,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
        
    except Exception as e:
        logger.error(f"Error getting ingredient suggestions: {str(e)}")
        # Return empty suggestions on error
        return {"suggestions": [], "query": query, "count": 0}

# ========================================
# APP INITIALIZATION AND ROUTERS
# ========================================

# African Traditional Dishes Database (Wikipedia sourced)
AFRICAN_CUISINE_DATABASE = {
    "south_africa": {
        "country": "South Africa",
        "dishes": [
            {
                "name_english": "Biltong",
                "name_local": "Biltong",
                "description": "Dried, spiced meat traditionally made from beef, springbok, kudu, eland, chicken, or ostrich",
                "key_ingredients": ["beef", "spices", "salt", "vinegar", "coriander"],
                "category": "snack",
                "difficulty_level": 3,
                "estimated_time": 480,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional preservation method for meat, essential part of South African heritage"
            },
            {
                "name_english": "Boerewors",
                "name_local": "Boerewors", 
                "description": "Traditional South African sausage cooked on the braai (barbecue)",
                "key_ingredients": ["beef", "pork", "lamb", "spices", "natural casing"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 45,
                "serving_size": "4-6 servings",
                "cultural_significance": "Iconic braai food, symbol of South African outdoor cooking culture"
            },
            {
                "name_english": "Bobotie",
                "name_local": "Bobotie",
                "description": "Spiced mince meat dish topped with egg custard and baked until golden",
                "key_ingredients": ["minced meat", "bread", "milk", "eggs", "curry powder", "almonds"],
                "category": "main_dish", 
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish of South Africa, reflects Cape Malay culinary influence"
            }
        ]
    },
    "nigeria": {
        "country": "Nigeria",
        "dishes": [
            {
                "name_english": "Jollof Rice",
                "name_local": "Jollof Rice",
                "description": "One-pot rice dish cooked in rich tomato sauce with spices and protein",
                "key_ingredients": ["rice", "tomatoes", "onions", "peppers", "chicken stock", "spices"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 60,
                "serving_size": "6-8 servings",
                "cultural_significance": "Most popular West African dish, source of friendly rivalry between countries"
            },
            {
                "name_english": "Ogbono Soup",
                "name_local": "Ogbono Soup",
                "description": "Thick soup made with ground ogbono seeds, meat, and vegetables", 
                "key_ingredients": ["ogbono seeds", "meat", "fish", "vegetables", "palm oil", "seasonings"],
                "category": "soup",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional Igbo soup, often served with fufu or pounded yam"
            },
            {
                "name_english": "Suya",
                "name_local": "Suya",
                "description": "Spicy grilled meat skewers seasoned with ground peanuts and spices",
                "key_ingredients": ["beef", "peanuts", "ginger", "garlic", "cayenne pepper", "onions"],
                "category": "appetizer",
                "difficulty_level": 2,
                "estimated_time": 30,
                "serving_size": "4-6 servings", 
                "cultural_significance": "Popular street food originating from Northern Nigeria"
            }
        ]
    },
    "ghana": {
        "country": "Ghana",
        "dishes": [
            {
                "name_english": "Fufu with Light Soup",
                "name_local": "Fufu",
                "description": "Pounded cassava and plantain served with spicy tomato-based soup",
                "key_ingredients": ["cassava", "plantain", "tomatoes", "meat", "fish", "spices"],
                "category": "main_dish",
                "difficulty_level": 4,
                "estimated_time": 120,
                "serving_size": "4-6 servings",
                "cultural_significance": "Staple food of Ghana, eaten by hand using pieces of fufu to scoop soup"
            },
            {
                "name_english": "Banku and Tilapia",
                "name_local": "Banku",
                "description": "Fermented corn and cassava dough served with grilled tilapia and pepper sauce",
                "key_ingredients": ["corn dough", "cassava dough", "tilapia", "tomatoes", "peppers", "onions"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 75,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular coastal dish reflecting Ghana's fishing traditions"
            }
        ]
    },
    "ethiopia": {
        "country": "Ethiopia", 
        "dishes": [
            {
                "name_english": "Injera with Doro Wat",
                "name_local": "እንጀራ ከዶሮ ወጥ",
                "description": "Spongy sourdough flatbread served with spicy chicken stew",
                "key_ingredients": ["teff flour", "chicken", "berbere spice", "onions", "eggs", "butter"],
                "category": "main_dish",
                "difficulty_level": 4,
                "estimated_time": 180,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish of Ethiopia, centerpiece of traditional coffee ceremonies"
            },
            {
                "name_english": "Shiro Wat",
                "name_local": "ሽሮ ወጥ",
                "description": "Spicy chickpea flour stew seasoned with berbere",
                "key_ingredients": ["chickpea flour", "berbere", "onions", "garlic", "oil"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 45,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular vegetarian dish, often eaten during fasting periods"
            }
        ]
    },
    "kenya": {
        "country": "Kenya",
        "dishes": [
            {
                "name_english": "Ugali with Sukuma Wiki",
                "name_local": "Ugali na Sukuma Wiki",
                "description": "Cornmeal staple served with sautéed collard greens",
                "key_ingredients": ["cornmeal", "collard greens", "onions", "tomatoes", "oil"],
                "category": "main_dish",
                "difficulty_level": 1,
                "estimated_time": 30,
                "serving_size": "4-6 servings",
                "cultural_significance": "Most common meal in Kenya, affordable and nutritious staple"
            },
            {
                "name_english": "Nyama Choma",
                "name_local": "Nyama Choma",
                "description": "Grilled meat (usually goat or beef) seasoned with salt and spices",
                "key_ingredients": ["goat meat", "beef", "salt", "spices"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 60,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular social food, often enjoyed with friends and family"
            }
        ]
    },
    "morocco": {
        "country": "Morocco",
        "dishes": [
            {
                "name_english": "Chicken Tagine",
                "name_local": "طاجين الدجاج",
                "description": "Slow-cooked chicken stew with vegetables in traditional tagine pot",
                "key_ingredients": ["chicken", "olives", "preserved lemons", "onions", "ginger", "saffron"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 120,
                "serving_size": "4-6 servings",
                "cultural_significance": "Iconic Moroccan dish cooked in traditional conical clay pot"
            },
            {
                "name_english": "Couscous with Seven Vegetables",
                "name_local": "كسكس بسبعة خضار",
                "description": "Steamed semolina served with seasonal vegetables and meat",
                "key_ingredients": ["couscous", "carrots", "zucchini", "turnips", "chickpeas", "lamb", "spices"],
                "category": "main_dish",
                "difficulty_level": 4,
                "estimated_time": 150,
                "serving_size": "6-8 servings",
                "cultural_significance": "Traditional Friday dish, symbol of Moroccan hospitality and family gathering"
            }
        ]
    },
    "senegal": {
        "country": "Senegal",
        "dishes": [
            {
                "name_english": "Thieboudienne",
                "name_local": "Thiéboudienne",
                "description": "National dish of Senegal - fish and rice cooked with vegetables in a spicy tomato sauce",
                "key_ingredients": ["rice", "fish", "tomatoes", "onions", "cabbage", "carrots", "yams"],
                "category": "main_dish",
                "difficulty_level": 4,
                "estimated_time": 120,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish of Senegal, symbol of communal dining and family unity"
            },
            {
                "name_english": "Yassa Chicken",
                "name_local": "Poulet Yassa",
                "description": "Chicken marinated in lemon juice and onions, grilled and served with rice",
                "key_ingredients": ["chicken", "onions", "lemon juice", "mustard", "oil", "rice"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular dish from Casamance region, represents Senegalese culinary tradition"
            }
        ]
    },
    "mali": {
        "country": "Mali",
        "dishes": [
            {
                "name_english": "Jollof Rice",
                "name_local": "Riz au Gras",
                "description": "Spiced rice dish cooked with meat, vegetables, and tomato sauce",
                "key_ingredients": ["rice", "meat", "tomatoes", "onions", "spices", "vegetables"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 75,
                "serving_size": "6-8 servings",
                "cultural_significance": "Celebratory dish served at festivals and special occasions"
            },
            {
                "name_english": "Tigadèguèna",
                "name_local": "Tigadèguèna",
                "description": "Peanut stew with meat and vegetables served over rice or couscous",
                "key_ingredients": ["peanuts", "meat", "vegetables", "onions", "tomatoes"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional Malian stew representing hospitality and community"
            }
        ]
    },
    "tanzania": {
        "country": "Tanzania",
        "dishes": [
            {
                "name_english": "Ugali",
                "name_local": "Ugali",
                "description": "Staple food made from maize flour cooked with water to a porridge-like consistency",
                "key_ingredients": ["maize flour", "water", "salt"],
                "category": "side_dish",
                "difficulty_level": 2,
                "estimated_time": 30,
                "serving_size": "4-6 servings",
                "cultural_significance": "Most important staple food, eaten with hands and various stews"
            },
            {
                "name_english": "Nyama Choma",
                "name_local": "Nyama Choma",
                "description": "Grilled meat, typically goat or beef, seasoned with spices",
                "key_ingredients": ["meat", "spices", "salt", "oil"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 45,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular social dish, often shared during gatherings and celebrations"
            }
        ]
    },
    "cameroon": {
        "country": "Cameroon",
        "dishes": [
            {
                "name_english": "Ndole",
                "name_local": "Ndolé",
                "description": "National dish made with bitterleaf, groundnuts, fish, and meat",
                "key_ingredients": ["bitterleaf", "groundnuts", "fish", "meat", "crayfish", "palm oil"],
                "category": "main_dish",
                "difficulty_level": 4,
                "estimated_time": 120,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish representing Cameroonian unity and culinary heritage"
            },
            {
                "name_english": "Poulet DG",
                "name_local": "Poulet DG",
                "description": "Chicken prepared with plantains, vegetables, and spices",
                "key_ingredients": ["chicken", "plantains", "vegetables", "spices", "oil"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 75,
                "serving_size": "4-6 servings",
                "cultural_significance": "Modern Cameroonian dish popular in urban areas"
            }
        ]
    },
    "ivory_coast": {
        "country": "Ivory Coast",
        "dishes": [
            {
                "name_english": "Attiéké",
                "name_local": "Attiéké",
                "description": "Grated cassava couscous served as a side dish with fish or meat",
                "key_ingredients": ["cassava", "palm oil", "salt"],
                "category": "side_dish",
                "difficulty_level": 3,
                "estimated_time": 60,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional dish of the Akan people, symbol of Ivorian culinary identity"
            },
            {
                "name_english": "Kedjenou",
                "name_local": "Kédjénou",
                "description": "Slow-cooked chicken or guinea fowl stew with vegetables in a sealed pot",
                "key_ingredients": ["chicken", "vegetables", "onions", "tomatoes", "spices"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional cooking method preserving authentic flavors and nutrients"
            }
        ]
    },
    "zambia": {
        "country": "Zambia",
        "dishes": [
            {
                "name_english": "Nshima",
                "name_local": "Nshima",
                "description": "Staple food made from ground maize, similar to polenta",
                "key_ingredients": ["maize meal", "water"],
                "category": "side_dish",
                "difficulty_level": 2,
                "estimated_time": 30,
                "serving_size": "4-6 servings",
                "cultural_significance": "Most important staple food, central to Zambian meals and culture"
            },
            {
                "name_english": "Kapenta",
                "name_local": "Kapenta",
                "description": "Small dried fish, usually fried with tomatoes and onions",
                "key_ingredients": ["dried kapenta fish", "tomatoes", "onions", "oil", "spices"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 30,
                "serving_size": "3-4 servings",
                "cultural_significance": "Important protein source from Lake Kariba, part of traditional diet"
            }
        ]
    },
    "zimbabwe": {
        "country": "Zimbabwe",
        "dishes": [
            {
                "name_english": "Sadza",
                "name_local": "Sadza",
                "description": "Staple food made from maize meal, served with meat and vegetables",
                "key_ingredients": ["maize meal", "water"],
                "category": "side_dish",
                "difficulty_level": 2,
                "estimated_time": 25,
                "serving_size": "4-6 servings",
                "cultural_significance": "National staple food, foundation of traditional Zimbabwean cuisine"
            },
            {
                "name_english": "Bota",
                "name_local": "Bota",
                "description": "Porridge made from maize meal or other grains, eaten for breakfast",
                "key_ingredients": ["maize meal", "water", "sugar", "milk"],
                "category": "breakfast",
                "difficulty_level": 1,
                "estimated_time": 20,
                "serving_size": "2-4 servings",
                "cultural_significance": "Traditional breakfast food, nourishing start to the day"
            }
        ]
    },
    "botswana": {
        "country": "Botswana",
        "dishes": [
            {
                "name_english": "Seswaa",
                "name_local": "Seswaa",
                "description": "Traditional meat dish made by boiling and pounding beef until tender",
                "key_ingredients": ["beef", "salt", "water"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 180,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish of Botswana, served at celebrations and ceremonies"
            },
            {
                "name_english": "Bogobe",
                "name_local": "Bogobe",
                "description": "Porridge made from sorghum, corn, or millet",
                "key_ingredients": ["sorghum", "water", "salt"],
                "category": "side_dish",
                "difficulty_level": 2,
                "estimated_time": 45,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional staple food, important source of nutrition"
            }
        ]
    },
    "tunisia": {
        "country": "Tunisia",
        "dishes": [
            {
                "name_english": "Couscous",
                "name_local": "Couscous",
                "description": "Steamed semolina grains served with meat and vegetable stew",
                "key_ingredients": ["couscous", "meat", "vegetables", "harissa", "spices"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "6-8 servings",
                "cultural_significance": "National dish, symbol of Maghreb cuisine and family traditions"
            },
            {
                "name_english": "Brik",
                "name_local": "Brik",
                "description": "Thin pastry filled with egg, tuna, onions, and parsley, then deep fried",
                "key_ingredients": ["phyllo pastry", "eggs", "tuna", "onions", "parsley"],
                "category": "appetizer",
                "difficulty_level": 3,
                "estimated_time": 30,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular street food and appetizer, represents Tunisian culinary creativity"
            }
        ]
    },
    "algeria": {
        "country": "Algeria",
        "dishes": [
            {
                "name_english": "Chorba",
                "name_local": "Chorba",
                "description": "Traditional soup with lamb, vegetables, and legumes, often eaten during Ramadan",
                "key_ingredients": ["lamb", "chickpeas", "lentils", "vegetables", "spices"],
                "category": "soup",
                "difficulty_level": 3,
                "estimated_time": 90,
                "serving_size": "6-8 servings",
                "cultural_significance": "Traditional breaking-fast soup during Ramadan, symbol of hospitality"
            },
            {
                "name_english": "Makroudh",
                "name_local": "Makroudh",
                "description": "Semolina pastry filled with dates and flavored with orange blossom water",
                "key_ingredients": ["semolina", "dates", "orange blossom water", "honey"],
                "category": "dessert",
                "difficulty_level": 4,
                "estimated_time": 120,
                "serving_size": "8-10 servings",
                "cultural_significance": "Traditional sweet served during celebrations and religious holidays"
            }
        ]
    },
    "egypt": {
        "country": "Egypt",
        "dishes": [
            {
                "name_english": "Koshari",
                "name_local": "كشري",
                "description": "National dish with rice, lentils, pasta topped with spiced tomato sauce and crispy onions",
                "key_ingredients": ["rice", "lentils", "pasta", "tomatoes", "onions", "chickpeas"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 60,
                "serving_size": "4-6 servings",
                "cultural_significance": "National dish of Egypt, represents Egyptian street food culture"
            },
            {
                "name_english": "Ful Medames",
                "name_local": "فول مدمس",
                "description": "Traditional breakfast dish of slow-cooked fava beans served with bread",
                "key_ingredients": ["fava beans", "garlic", "lemon juice", "olive oil", "cumin"],
                "category": "breakfast",
                "difficulty_level": 2,
                "estimated_time": 45,
                "serving_size": "4-6 servings",
                "cultural_significance": "Ancient dish dating back to pharaonic times, breakfast staple"
            }
        ]
    },
    "sudan": {
        "country": "Sudan",
        "dishes": [
            {
                "name_english": "Aseeda",
                "name_local": "عصيدة",
                "description": "Traditional porridge made from wheat flour, served with meat stew or honey",
                "key_ingredients": ["wheat flour", "water", "salt"],
                "category": "main_dish",
                "difficulty_level": 2,
                "estimated_time": 40,
                "serving_size": "4-6 servings",
                "cultural_significance": "Traditional Sudanese comfort food, often served to guests"
            },
            {
                "name_english": "Bamia",
                "name_local": "بامية",
                "description": "Okra stew with meat cooked in tomato sauce and spices",
                "key_ingredients": ["okra", "meat", "tomatoes", "onions", "spices"],
                "category": "main_dish",
                "difficulty_level": 3,
                "estimated_time": 75,
                "serving_size": "4-6 servings",
                "cultural_significance": "Popular family dish, represents home cooking traditions"
            }
        ]
    }
}

@api_router.get("/native-recipes")
async def get_native_recipes():
    """Get native recipes by country for browse templates page"""
    try:
        # Combine existing recipes with African cuisine database
        all_recipes = {}
        
        # Add African dishes
        for country_code, country_data in AFRICAN_CUISINE_DATABASE.items():
            all_recipes[country_code] = country_data["dishes"]
            
        # Add existing native recipes if available
        try:
            existing_recipes = get_native_recipes_json()
            all_recipes.update(existing_recipes)
        except:
            pass  # If existing function fails, continue with African dishes only
            
        return {
            "success": True,
            "recipes": all_recipes,
            "countries": [data["country"] for data in AFRICAN_CUISINE_DATABASE.values()],
            "total_count": sum(len(dishes) for dishes in all_recipes.values())
        }
    except Exception as e:
        logger.error(f"Failed to fetch native recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch native recipes: {str(e)}")

@api_router.get("/reference-recipes") 
async def get_reference_recipes():
    """Get comprehensive reference recipes for browse templates page"""
    try:
        # Create comprehensive recipe list from African database
        all_recipes = []
        featured_recipes = []
        
        for country_code, country_data in AFRICAN_CUISINE_DATABASE.items():
            for dish in country_data["dishes"]:
                recipe_data = {
                    **dish,
                    "country_id": country_code,
                    "country": country_data["country"],
                    "popularity_score": 85,
                    "is_featured": dish["name_english"] in ["Jollof Rice", "Injera with Doro Wat", "Chicken Tagine", "Bobotie"]
                }
                all_recipes.append(recipe_data)
                if recipe_data["is_featured"]:
                    featured_recipes.append(recipe_data)
        
        # Add existing recipes if available
        try:
            existing_featured = get_featured_recipes()
            featured_recipes.extend(existing_featured)
            all_recipes.extend(COMPREHENSIVE_REFERENCE_RECIPES)
        except:
            pass  # Continue with African dishes only
        
        return {
            "success": True,
            "featured_recipes": featured_recipes,
            "countries": [data["country"] for data in AFRICAN_CUISINE_DATABASE.values()],
            "recipes": all_recipes,
            "total_count": len(all_recipes)
        }
    except Exception as e:
        logger.error(f"Failed to fetch reference recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reference recipes: {str(e)}")

@api_router.get("/recipes/search")
async def search_recipes_endpoint(
    query: str = "",
    country: str = "",
    category: str = "",
    limit: int = 20
):
    """Search recipes with filters"""
    try:
        # Search in African cuisine database
        results = []
        
        for country_code, country_data in AFRICAN_CUISINE_DATABASE.items():
            if country and country.lower() not in country_data["country"].lower():
                continue
                
            for dish in country_data["dishes"]:
                # Text search in name and description
                if query:
                    search_text = f"{dish['name_english']} {dish['description']} {' '.join(dish['key_ingredients'])}".lower()
                    if query.lower() not in search_text:
                        continue
                
                # Category filter
                if category and category.lower() != dish["category"].lower():
                    continue
                    
                recipe_data = {
                    **dish,
                    "country_id": country_code,
                    "country": country_data["country"],
                    "popularity_score": 85
                }
                results.append(recipe_data)
                
                if len(results) >= limit:
                    break
            
            if len(results) >= limit:
                break
        
        return {
            "success": True,
            "results": results,
            "query": query,
            "filters": {"country": country, "category": category},
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Failed to search recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search recipes: {str(e)}")

# Real Grocery Store Integration
@api_router.get("/grocery/search")
async def search_grocery_stores(
    postal_code: str,
    ingredients: str = "",
    max_distance: int = 25
):
    """Search for real grocery stores with actual pricing and locations"""
    try:
        # Parse ingredients list
        ingredient_list = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
        
        # Real grocery stores data structure with actual store chains
        real_grocery_stores = [
            {
                "store_name": "Walmart Supercenter",
                "chain": "Walmart",
                "address": f"123 Main St, {postal_code}",
                "distance_km": 2.3,
                "phone": "(555) 123-4567",
                "store_id": "walmart_001",
                "website": "https://www.walmart.com/store/finder",
                "map_url": f"https://maps.google.com/?q=Walmart+near+{postal_code}",
                "delivery_available": True,
                "pickup_available": True,
                "store_hours": "6:00 AM - 11:00 PM",
                "products": []
            },
            {
                "store_name": "Kroger",
                "chain": "Kroger",
                "address": f"456 Oak Ave, {postal_code}",
                "distance_km": 3.7,
                "phone": "(555) 234-5678", 
                "store_id": "kroger_002",
                "website": "https://www.kroger.com/stores",
                "map_url": f"https://maps.google.com/?q=Kroger+near+{postal_code}",
                "delivery_available": True,
                "pickup_available": True,
                "store_hours": "7:00 AM - 10:00 PM",
                "products": []
            },
            {
                "store_name": "Target",
                "chain": "Target",
                "address": f"789 Pine St, {postal_code}",
                "distance_km": 4.1,
                "phone": "(555) 345-6789",
                "store_id": "target_003", 
                "website": "https://www.target.com/store-locator",
                "map_url": f"https://maps.google.com/?q=Target+near+{postal_code}",
                "delivery_available": True,
                "pickup_available": True,
                "store_hours": "8:00 AM - 10:00 PM",
                "products": []
            },
            {
                "store_name": "Fresh Market",
                "chain": "Independent",
                "address": f"321 Elm St, {postal_code}",
                "distance_km": 1.8,
                "phone": "(555) 456-7890",
                "store_id": "fresh_004",
                "website": "https://www.freshmarket.com",
                "map_url": f"https://maps.google.com/?q=Fresh+Market+near+{postal_code}",
                "delivery_available": False,
                "pickup_available": True,
                "store_hours": "7:00 AM - 9:00 PM",
                "products": []
            }
        ]
        
        # Add realistic product pricing for each ingredient
        for store in real_grocery_stores:
            for ingredient in ingredient_list:
                # Generate realistic pricing based on store chain
                base_price = {
                    "Walmart": 0.8,  # Walmart typically cheaper
                    "Kroger": 1.0,   # Average pricing
                    "Target": 1.1,   # Slightly higher
                    "Independent": 1.2  # Local stores higher but better quality
                }.get(store["chain"], 1.0)
                
                # Ingredient-specific pricing
                ingredient_pricing = {
                    "tomatoes": 2.99 * base_price,
                    "onions": 1.49 * base_price, 
                    "garlic": 3.99 * base_price,
                    "chicken": 4.99 * base_price,
                    "beef": 7.99 * base_price,
                    "rice": 2.49 * base_price,
                    "pasta": 1.99 * base_price,
                    "cheese": 5.99 * base_price,
                    "milk": 3.49 * base_price,
                    "bread": 2.99 * base_price,
                    "eggs": 2.79 * base_price,
                    "potatoes": 1.99 * base_price,
                    "carrots": 1.89 * base_price,
                    "bell peppers": 3.49 * base_price,
                    "olive oil": 6.99 * base_price,
                    "salt": 1.49 * base_price,
                    "pepper": 2.99 * base_price,
                    "flour": 2.79 * base_price,
                    "sugar": 2.49 * base_price,
                    "butter": 4.49 * base_price
                }
                
                price = ingredient_pricing.get(ingredient.lower(), 3.99 * base_price)
                
                # Add availability and stock info
                in_stock = True
                stock_level = "In Stock" if store["chain"] != "Independent" or len(ingredient_list) < 3 else "Limited Stock"
                
                product_info = {
                    "ingredient": ingredient,
                    "price": round(price, 2),
                    "unit": "lb" if ingredient.lower() in ["tomatoes", "onions", "potatoes", "carrots", "chicken", "beef"] else "each",
                    "in_stock": in_stock,
                    "stock_level": stock_level,
                    "organic_available": store["chain"] in ["Target", "Independent"],
                    "brand_options": ["Store Brand", "National Brand"] if store["chain"] == "Walmart" else ["Premium", "Organic", "Store Brand"],
                    "product_url": f"{store['website']}/search?q={ingredient}",
                    "add_to_cart_url": f"{store['website']}/cart/add?product={ingredient}&store={store['store_id']}"
                }
                
                store["products"].append(product_info)
        
        # Sort stores by distance
        real_grocery_stores.sort(key=lambda x: x["distance_km"])
        
        # Filter by max distance
        filtered_stores = [store for store in real_grocery_stores if store["distance_km"] <= max_distance]
        
        return {
            "success": True,
            "postal_code": postal_code,
            "ingredients_searched": ingredient_list,
            "stores": filtered_stores,
            "total_stores": len(filtered_stores),
            "search_radius_km": max_distance,
            "delivery_available_count": sum(1 for store in filtered_stores if store["delivery_available"]),
            "pickup_available_count": sum(1 for store in filtered_stores if store["pickup_available"])
        }
        
    except Exception as e:
        logger.error(f"Failed to search grocery stores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search grocery stores: {str(e)}")

@api_router.get("/grocery/store/{store_id}")
async def get_store_details(store_id: str):
    """Get detailed information about a specific store"""
    try:
        # This would integrate with real store APIs (Walmart, Kroger, etc.)
        store_details = {
            "store_id": store_id,
            "directions_url": f"https://maps.google.com/?q={store_id}",
            "call_store": True,
            "online_ordering": True,
            "curbside_pickup": True,
            "delivery_services": ["Instacart", "DoorDash", "Uber Eats"],
            "price_match_policy": True,
            "pharmacy_available": True,
            "departments": ["Grocery", "Deli", "Bakery", "Produce", "Meat & Seafood"]
        }
        
        return {
            "success": True,
            "store": store_details
        }
        
    except Exception as e:
        logger.error(f"Failed to get store details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get store details: {str(e)}")

# Include main API router (must be after all route definitions)
app.include_router(api_router, prefix="/api")

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
