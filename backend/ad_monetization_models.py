# Enhanced Ad System & Monetization Models
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid

class AdType(str, Enum):
    BANNER = "banner"
    SPONSORED_RECIPE = "sponsored_recipe"
    PROMOTED_COOKING_OFFER = "promoted_cooking_offer"
    VIDEO_AD = "video_ad"
    NATIVE_CONTENT = "native_content"
    INTERSTITIAL = "interstitial"

class AdStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    REJECTED = "rejected"
    PENDING = "pending"

class AdPlacement(str, Enum):
    FEED_TOP = "feed_top"
    FEED_MIDDLE = "feed_middle"
    FEED_BOTTOM = "feed_bottom"
    BETWEEN_SNIPPETS = "between_snippets"
    SIDEBAR = "sidebar"
    COOKING_OFFERS_LIST = "cooking_offers_list"
    RECIPE_DETAIL = "recipe_detail"
    HOMEPAGE_HERO = "homepage_hero"

class UserEngagementLevel(str, Enum):
    LOW = "low"          # 0-25th percentile
    MEDIUM = "medium"    # 25-75th percentile
    HIGH = "high"        # 75-95th percentile
    POWER_USER = "power_user"  # 95th+ percentile

class PremiumTier(str, Enum):
    FREE = "free"
    COOK_PLUS = "cook_plus"      # $4.99/month - Enhanced cook features
    FOODIE_PRO = "foodie_pro"    # $7.99/month - Premium eater experience
    CULINARY_VIP = "culinary_vip" # $12.99/month - Full premium experience

class Advertisement(BaseModel):
    """Advertisement model for dynamic ad placement"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Ad Content
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=300)
    ad_type: AdType
    creative_url: str  # Image, video, or content URL
    click_url: str     # Where user goes when clicking
    
    # Targeting
    target_demographics: List[str] = []  # ["age_25_34", "food_enthusiast", "home_cook"]
    target_locations: List[str] = []     # ["US", "CA", "NYC", "10001"]
    target_cuisines: List[str] = []      # ["italian", "mexican", "asian"]
    target_dietary: List[str] = []       # ["vegetarian", "vegan", "gluten_free"]
    
    # Placement & Frequency
    placement_types: List[AdPlacement] = []
    max_impressions_per_user_day: int = Field(default=5, ge=1, le=20)
    min_seconds_between_shows: int = Field(default=300, ge=60)  # 5 minutes default
    
    # Pricing & Budget
    cost_per_impression: float = Field(default=0.01, ge=0.001, le=1.0)  # CPM basis
    cost_per_click: float = Field(default=0.50, ge=0.05, le=10.0)
    daily_budget: float = Field(default=100.0, ge=10.0)
    total_budget: float = Field(default=1000.0, ge=50.0)
    spent_amount: float = Field(default=0.0, ge=0.0)
    
    # Performance Metrics
    total_impressions: int = Field(default=0, ge=0)
    total_clicks: int = Field(default=0, ge=0)
    click_through_rate: float = Field(default=0.0, ge=0.0)
    conversion_rate: float = Field(default=0.0, ge=0.0)
    
    # Scheduling
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    active_hours_start: str = Field(default="00:00", pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    active_hours_end: str = Field(default="23:59", pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    active_days: List[str] = Field(default=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    
    # Status & Metadata
    status: AdStatus = AdStatus.PENDING
    advertiser_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('click_through_rate', always=True)
    def calculate_ctr(cls, v, values):
        if 'total_impressions' in values and 'total_clicks' in values:
            impressions = values['total_impressions']
            clicks = values['total_clicks']
            if impressions > 0:
                return round((clicks / impressions) * 100, 2)
        return 0.0

class UserEngagementProfile(BaseModel):
    """User engagement tracking for ad frequency optimization"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Activity Metrics (last 30 days)
    total_sessions: int = Field(default=0, ge=0)
    total_time_spent_minutes: int = Field(default=0, ge=0)
    recipes_viewed: int = Field(default=0, ge=0)
    snippets_created: int = Field(default=0, ge=0)
    cooking_offers_created: int = Field(default=0, ge=0)
    eating_requests_created: int = Field(default=0, ge=0)
    appointments_booked: int = Field(default=0, ge=0)
    messages_sent: int = Field(default=0, ge=0)
    
    # Engagement Quality
    average_session_duration_minutes: float = Field(default=0.0, ge=0.0)
    recipe_completion_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    social_interaction_score: float = Field(default=0.0, ge=0.0)  # likes, comments, follows
    
    # Ad Interaction History
    ads_viewed_today: int = Field(default=0, ge=0)
    ads_clicked_today: int = Field(default=0, ge=0)
    ads_viewed_this_week: int = Field(default=0, ge=0)
    last_ad_shown: Optional[datetime] = None
    ad_fatigue_score: float = Field(default=0.0, ge=0.0, le=1.0)  # 0=no fatigue, 1=high fatigue
    
    # Calculated Metrics
    engagement_level: UserEngagementLevel = UserEngagementLevel.LOW
    optimal_ads_per_day: int = Field(default=3, ge=1, le=15)
    premium_eligibility_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Temporal Data
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    calculation_date: datetime = Field(default_factory=datetime.utcnow)

class PremiumSubscription(BaseModel):
    """Premium membership subscription model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Subscription Details
    tier: PremiumTier = PremiumTier.FREE
    monthly_price: float = Field(default=0.0, ge=0.0)
    annual_discount: float = Field(default=0.0, ge=0.0, le=0.5)  # Up to 50% discount
    
    # Billing
    billing_cycle: str = "monthly"  # "monthly" or "annual"
    next_billing_date: Optional[datetime] = None
    last_payment_date: Optional[datetime] = None
    payment_method_id: Optional[str] = None
    
    # Premium Features Access
    features: Dict[str, bool] = Field(default_factory=lambda: {
        "ad_free_experience": False,
        "priority_customer_support": False,
        "advanced_analytics": False,
        "premium_recipe_access": False,
        "priority_booking": False,
        "enhanced_profile": False,
        "unlimited_cooking_offers": False,
        "video_calling": False,
        "custom_dietary_filters": False,
        "bulk_translation": False
    })
    
    # Usage & Benefits
    total_savings_usd: float = Field(default=0.0, ge=0.0)  # Money saved on ads, commissions, etc.
    premium_features_used: int = Field(default=0, ge=0)
    satisfaction_score: Optional[float] = Field(None, ge=1.0, le=5.0)
    
    # Status & Timeline
    is_active: bool = Field(default=False)
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdImpression(BaseModel):
    """Track individual ad impressions for analytics"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ad_id: str
    user_id: str
    
    # Impression Details
    placement: AdPlacement
    page_context: str  # "feed", "recipe_detail", "cooking_offers", etc.
    position_in_content: int = Field(default=1, ge=1)  # Position in feed/list
    
    # User Context
    user_engagement_level: UserEngagementLevel
    is_premium_user: bool = Field(default=False)
    user_location: Optional[str] = None
    device_type: str = "web"  # "web", "mobile", "tablet"
    
    # Interaction
    was_clicked: bool = Field(default=False)
    view_duration_seconds: float = Field(default=0.0, ge=0.0)
    click_timestamp: Optional[datetime] = None
    
    # Performance
    revenue_generated: float = Field(default=0.0, ge=0.0)
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SurgePricing(BaseModel):
    """Dynamic pricing based on demand"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Scope
    applies_to: str  # "cooking_offers", "messaging", "bookings"
    category: Optional[str] = None  # Specific category if applicable
    location: Optional[str] = None  # Specific location if applicable
    
    # Surge Conditions
    demand_threshold: float = Field(default=1.5, ge=1.0, le=5.0)  # Multiplier trigger
    time_window_hours: int = Field(default=2, ge=1, le=24)
    min_active_offers: int = Field(default=5, ge=1)
    
    # Pricing Adjustments
    base_commission_rate: float = Field(default=0.15, ge=0.05, le=0.30)
    surge_commission_rate: float = Field(default=0.18, ge=0.10, le=0.35)
    surge_multiplier: float = Field(default=1.2, ge=1.0, le=3.0)
    
    # Status & Timing
    is_active: bool = Field(default=False)
    activated_at: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None
    duration_minutes: int = Field(default=60, ge=15, le=480)  # Max 8 hours
    
    # Performance
    additional_revenue: float = Field(default=0.0, ge=0.0)
    affected_transactions: int = Field(default=0, ge=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RevenueAnalytics(BaseModel):
    """Revenue analytics and reporting"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Time Period
    date: datetime
    period_type: str = "daily"  # "daily", "weekly", "monthly"
    
    # Ad Revenue
    ad_impressions: int = Field(default=0, ge=0)
    ad_clicks: int = Field(default=0, ge=0)
    ad_revenue: float = Field(default=0.0, ge=0.0)
    
    # Marketplace Revenue
    cooking_offers_revenue: float = Field(default=0.0, ge=0.0)
    messaging_revenue: float = Field(default=0.0, ge=0.0)
    booking_revenue: float = Field(default=0.0, ge=0.0)
    
    # Premium Subscriptions
    premium_subscription_revenue: float = Field(default=0.0, ge=0.0)
    new_premium_subscribers: int = Field(default=0, ge=0)
    churned_premium_subscribers: int = Field(default=0, ge=0)
    
    # Commission Revenue
    platform_commission_total: float = Field(default=0.0, ge=0.0)
    average_commission_rate: float = Field(default=0.15, ge=0.0, le=1.0)
    surge_pricing_bonus: float = Field(default=0.0, ge=0.0)
    
    # User Metrics
    active_users: int = Field(default=0, ge=0)
    premium_users: int = Field(default=0, ge=0)
    revenue_per_user: float = Field(default=0.0, ge=0.0)
    
    # Totals
    total_revenue: float = Field(default=0.0, ge=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models

class AdCreationRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=300)
    ad_type: AdType
    creative_url: str
    click_url: str
    target_demographics: List[str] = []
    target_locations: List[str] = []
    target_cuisines: List[str] = []
    placement_types: List[AdPlacement] = []
    cost_per_impression: float = Field(default=0.01, ge=0.001, le=1.0)
    cost_per_click: float = Field(default=0.50, ge=0.05, le=10.0)
    daily_budget: float = Field(default=100.0, ge=10.0)
    total_budget: float = Field(default=1000.0, ge=50.0)
    start_date: Optional[str] = None  # ISO format
    end_date: Optional[str] = None

class PremiumUpgradeRequest(BaseModel):
    tier: PremiumTier
    billing_cycle: str = "monthly"  # "monthly" or "annual"
    payment_method_id: str

class AdPlacementResponse(BaseModel):
    ad_id: str
    ad_type: str
    title: str
    description: str
    creative_url: str
    click_url: str
    placement: str
    position: int
    targeting_score: float  # How well this ad matches the user

class RevenueReportResponse(BaseModel):
    period: str
    total_revenue: float
    ad_revenue: float
    marketplace_revenue: float
    premium_revenue: float
    commission_revenue: float
    revenue_breakdown: Dict[str, float]
    growth_metrics: Dict[str, float]
    top_performing_ads: List[Dict[str, Any]]