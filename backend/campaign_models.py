"""
Lambalia Campaign System Models
Promotional campaigns with promo codes and geographic targeting
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid


class CampaignType(str, Enum):
    """Types of promotional campaigns"""
    FREE_MEAL = "free_meal"
    REFERRAL = "referral"
    DISCOUNT = "discount"
    FIRST_ORDER = "first_order"
    SEASONAL = "seasonal"


class CampaignStatus(str, Enum):
    """Campaign status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PromoCodeStatus(str, Enum):
    """Promo code status"""
    ACTIVE = "active"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


# Campaign Models
class Campaign(BaseModel):
    """Promotional campaign"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    campaign_name: str
    campaign_type: CampaignType
    description: str
    
    # Discount settings
    discount_type: str  # percentage, fixed_amount, free
    discount_value: float  # 0 for free, 5 for $5 off, 20 for 20% off
    
    # Quota and limits
    total_quota: int  # Total codes to generate (e.g., 150)
    codes_generated: int = 0
    codes_redeemed: int = 0
    codes_remaining: int = 0
    
    # Per-user limits
    codes_per_user: int = 1  # How many codes can one user get
    redemptions_per_code: int = 1  # Usually 1 for single-use
    
    # Geographic targeting
    target_cities: List[str] = []  # ["Champaign"]
    target_states: List[str] = []  # ["IL"]
    valid_zip_codes: List[str] = []  # ["61820", "61821", ...]
    
    # Date restrictions
    start_date: datetime
    end_date: datetime
    valid_days_of_week: List[int] = [0, 1, 2, 3, 4, 5, 6]  # 0=Monday, 6=Sunday
    valid_hours: Optional[Dict[str, str]] = None  # {"start": "09:00", "end": "21:00"}
    
    # Participation
    participating_chef_ids: List[str] = []  # Specific chefs for campaign
    all_chefs_eligible: bool = True  # If true, all active chefs can participate
    
    # Campaign rules
    minimum_order_amount: float = 0.0
    maximum_discount_amount: Optional[float] = None
    applicable_product_categories: List[str] = []  # Empty = all categories
    new_users_only: bool = False
    
    # Status
    status: CampaignStatus = CampaignStatus.DRAFT
    
    # Analytics
    total_orders: int = 0
    total_revenue: float = 0.0
    total_discount_given: float = 0.0
    average_order_value: float = 0.0
    conversion_rate: float = 0.0  # % of codes that were redeemed
    
    # Admin
    created_by: str  # Admin user ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    launched_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class PromoCode(BaseModel):
    """Individual promotional code"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str  # LMB150-A1B2C3
    campaign_id: str
    
    # User assignment
    user_id: Optional[str] = None  # Assigned to user (auto-generate on registration)
    user_email: Optional[str] = None
    user_zip_code: Optional[str] = None
    
    # Status
    status: PromoCodeStatus = PromoCodeStatus.ACTIVE
    
    # Redemption tracking
    redemptions_count: int = 0
    max_redemptions: int = 1
    redeemed_order_ids: List[str] = []
    
    # Timestamps
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_at: Optional[datetime] = None
    first_redeemed_at: Optional[datetime] = None
    last_redeemed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class PromoCodeRedemption(BaseModel):
    """Record of promo code redemption"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    promo_code_id: str
    code: str
    campaign_id: str
    
    # Order details
    order_id: str
    user_id: str
    chef_id: str
    
    # Discount applied
    original_amount: float
    discount_amount: float
    final_amount: float
    
    # Metadata
    redeemed_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


# Request/Response Models
class CampaignRequest(BaseModel):
    """Request to create campaign"""
    campaign_name: str
    campaign_type: CampaignType
    description: str
    discount_type: str
    discount_value: float
    total_quota: int
    target_cities: List[str] = []
    target_states: List[str] = []
    valid_zip_codes: List[str] = []
    start_date: datetime
    end_date: datetime
    participating_chef_ids: List[str] = []
    all_chefs_eligible: bool = True
    minimum_order_amount: float = 0.0
    new_users_only: bool = False


class CampaignResponse(BaseModel):
    """Campaign details response"""
    id: str
    campaign_name: str
    campaign_type: CampaignType
    description: str
    discount_type: str
    discount_value: float
    total_quota: int
    codes_generated: int
    codes_redeemed: int
    codes_remaining: int
    status: CampaignStatus
    start_date: datetime
    end_date: datetime
    valid_zip_codes: List[str]
    conversion_rate: float
    total_orders: int
    total_revenue: float
    created_at: datetime


class PromoCodeResponse(BaseModel):
    """Promo code response for user"""
    code: str
    campaign_name: str
    discount_description: str  # "Free meal", "$5 off", "20% off"
    valid_until: datetime
    status: PromoCodeStatus
    redemptions_remaining: int
    instructions: str
    participating_chefs: List[Dict[str, str]] = []  # [{"name": "...", "address": "..."}]


class PromoCodeValidationRequest(BaseModel):
    """Request to validate promo code at checkout"""
    code: str
    user_id: str
    cart_total: float
    chef_id: str
    user_zip_code: str


class PromoCodeValidationResponse(BaseModel):
    """Promo code validation result"""
    valid: bool
    code: str
    discount_amount: float
    final_amount: float
    message: str
    errors: List[str] = []


class CampaignAnalytics(BaseModel):
    """Campaign performance analytics"""
    campaign_id: str
    campaign_name: str
    
    # Code statistics
    total_codes: int
    codes_assigned: int
    codes_redeemed: int
    codes_expired: int
    redemption_rate: float
    
    # Financial
    total_orders: int
    total_revenue: float
    total_discount_given: float
    average_order_value: float
    roi: float  # Return on investment
    
    # Geographic
    orders_by_zip: Dict[str, int]
    top_zip_codes: List[Dict[str, Any]]
    
    # Temporal
    orders_by_day: Dict[str, int]
    peak_redemption_day: str
    
    # User behavior
    new_users_acquired: int
    repeat_orders: int
    average_time_to_redeem: float  # Days from code generation to redemption


class CampaignStatsResponse(BaseModel):
    """Real-time campaign statistics"""
    campaign_id: str
    campaign_name: str
    status: CampaignStatus
    
    # Progress
    total_quota: int
    codes_generated: int
    codes_redeemed: int
    codes_remaining: int
    progress_percentage: float
    
    # Timeline
    days_remaining: int
    start_date: datetime
    end_date: datetime
    
    # Performance
    redemption_rate: float
    average_order_value: float
    total_revenue: float
