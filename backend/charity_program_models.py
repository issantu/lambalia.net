# Charity Program & Premium Membership Models - Social Impact Integration
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CharityType(str, Enum):
    FOOD_BANK = "food_bank"
    HOMELESS_SHELTER = "homeless_shelter"
    COMMUNITY_KITCHEN = "community_kitchen"
    SENIORS_CENTER = "seniors_center"
    SCHOOL_PROGRAM = "school_program"
    EMERGENCY_RELIEF = "emergency_relief"
    LOCAL_CHARITY = "local_charity"

class VerificationDocumentType(str, Enum):
    FOOD_BANK_LETTER = "food_bank_letter"
    CHARITY_RECOGNITION = "charity_recognition"
    VOLUNTEER_CERTIFICATE = "volunteer_certificate"
    DONATION_RECEIPT = "donation_receipt"
    VIDEO_EVIDENCE = "video_evidence"
    PHOTO_EVIDENCE = "photo_evidence"
    COMMUNITY_REFERENCE = "community_reference"

class VerificationStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_MORE_INFO = "requires_more_info"

class PremiumTier(str, Enum):
    COMMUNITY_HELPER = "community_helper"       # Free through charity work
    GARDEN_SUPPORTER = "garden_supporter"       # $4.99/month or charity work
    LOCAL_CHAMPION = "local_champion"           # $9.99/month or significant charity work

class ImpactMetricType(str, Enum):
    FOOD_DONATED_LBS = "food_donated_lbs"
    MEALS_PROVIDED = "meals_provided"
    PEOPLE_HELPED = "people_helped"
    VOLUNTEER_HOURS = "volunteer_hours"
    COMMUNITY_EVENTS = "community_events"

class CharityProgram(BaseModel):
    """Charity program for earning premium membership through community service"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Program Details
    program_name: str = "Community Food Sharing Program"
    description: str = "Transform food waste into community support by sharing excess produce and meals with local food banks, homeless shelters, and community kitchens."
    
    # User's Commitment
    committed_hours_per_month: int = Field(default=4, ge=2, le=40)
    preferred_charity_types: List[CharityType] = []
    preferred_locations: List[str] = []  # ZIP codes or city names
    
    # Current Status
    is_active: bool = True
    current_tier: PremiumTier = PremiumTier.COMMUNITY_HELPER
    tier_earned_through_charity: bool = False
    
    # Impact Tracking
    total_impact_score: float = 0.0
    monthly_impact_goal: float = 50.0  # Points needed per month
    current_month_impact: float = 0.0
    
    # Requirements & Guidelines
    monthly_requirements: Dict[str, Any] = Field(default_factory=lambda: {
        "minimum_donations": 2,        # Minimum charity activities per month
        "minimum_food_lbs": 10.0,     # Minimum pounds of food donated
        "verification_required": True,
        "committee_review": True
    })
    
    # Timeline
    enrolled_date: datetime = Field(default_factory=datetime.utcnow)
    last_activity_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CharityActivity(BaseModel):
    """Individual charity activity record"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    charity_program_id: str
    
    # Activity Details
    activity_type: CharityType
    charity_organization_name: str
    activity_description: str
    activity_date: datetime
    
    # Impact Metrics
    food_donated_lbs: Optional[float] = None
    meals_provided: Optional[int] = None
    people_helped: Optional[int] = None
    volunteer_hours: Optional[float] = None
    
    # Location
    location_address: str
    city: str
    state: str
    postal_code: str
    
    # Verification
    verification_documents: List[Dict[str, str]] = []  # [{"type": "food_bank_letter", "url": "...", "description": "..."}]
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verification_notes: Optional[str] = None
    verified_by: Optional[str] = None  # Committee member ID
    verified_at: Optional[datetime] = None
    
    # Impact Calculation
    calculated_impact_score: float = 0.0
    bonus_multiplier: float = 1.0  # For exceptional contributions
    
    # Evidence
    photo_urls: List[str] = []
    video_urls: List[str] = []
    witness_contacts: List[Dict[str, str]] = []  # [{"name": "...", "phone": "...", "role": "charity coordinator"}]
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

class CharityVerificationCommittee(BaseModel):
    """Committee member for reviewing charity activities"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Committee Details
    committee_role: str = "volunteer_reviewer"  # volunteer_reviewer, senior_reviewer, coordinator
    specialization: List[CharityType] = []
    geographic_coverage: List[str] = []  # ZIP codes or regions they cover
    
    # Qualifications
    years_charity_experience: int = Field(default=0, ge=0)
    certifications: List[str] = []
    background_check_completed: bool = False
    training_completed: bool = False
    
    # Performance
    reviews_completed: int = 0
    average_review_time_hours: float = 24.0
    accuracy_rating: float = 100.0
    
    # Status
    is_active: bool = True
    capacity_per_month: int = Field(default=20, ge=5, le=100)  # Max activities they can review
    current_month_reviews: int = 0
    
    # Contact
    preferred_contact_method: str = "email"
    availability_hours: Dict[str, str] = {}  # {"monday": "9-17", "tuesday": "10-14"}
    
    appointed_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: datetime = Field(default_factory=datetime.utcnow)

class PremiumMembership(BaseModel):
    """Enhanced premium membership with charity-based earning"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Membership Details
    tier: PremiumTier
    earned_through: str = "charity_work"  # "charity_work", "payment", "both"
    
    # Benefits
    benefits: Dict[str, Any] = Field(default_factory=lambda: {
        "commission_reduction": 0.02,      # 2% reduction (15% -> 13%)
        "priority_support": True,
        "featured_listings": True,
        "advanced_analytics": True,
        "social_impact_badge": True,
        "community_recognition": True,
        "exclusive_events": True
    })
    
    # Payment & Charity Balance
    monthly_payment: float = 0.0          # If partially paid
    charity_requirement_met: bool = False
    charity_score_current_month: float = 0.0
    charity_score_required: float = 50.0
    
    # Status
    is_active: bool = True
    auto_renew: bool = True
    grace_period_ends: Optional[datetime] = None
    
    # Timeline
    start_date: datetime = Field(default_factory=datetime.utcnow)
    current_period_end: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=30))
    last_charity_verification: Optional[datetime] = None
    
    # Recognition
    community_impact_level: str = "Rising Helper"  # "Rising Helper", "Community Champion", "Local Hero"
    recognition_badges: List[str] = []
    public_recognition: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CommunityImpactMetrics(BaseModel):
    """Track overall community impact across platform"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Aggregate Metrics
    total_food_donated_lbs: float = 0.0
    total_meals_provided: int = 0
    total_people_helped: int = 0
    total_volunteer_hours: float = 0.0
    
    # Geographic Impact
    cities_served: List[str] = []
    states_served: List[str] = []
    zip_codes_served: List[str] = []
    
    # Participating Organizations
    partner_food_banks: List[str] = []
    partner_shelters: List[str] = []
    partner_community_kitchens: List[str] = []
    
    # Platform Growth
    active_charity_participants: int = 0
    premium_members_via_charity: int = 0
    charity_activities_this_month: int = 0
    
    # Recognition
    featured_success_stories: List[Dict[str, str]] = []
    community_champions: List[str] = []  # User IDs of top contributors
    
    # Calculations
    food_waste_diverted_lbs: float = 0.0
    estimated_environmental_impact: Dict[str, float] = {}
    economic_value_created: float = 0.0
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class LocalPartnerOrganization(BaseModel):
    """Local charity organizations partnered with platform"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Organization Details
    organization_name: str
    charity_type: CharityType
    description: str
    mission_statement: str
    
    # Contact Information
    contact_person: str
    contact_email: str
    contact_phone: str
    website_url: Optional[str] = None
    
    # Location
    address: str
    city: str
    state: str
    postal_code: str
    service_area_radius_km: float = 25.0
    
    # Services
    services_provided: List[str] = []
    operating_hours: Dict[str, str] = {}
    capacity_people_served: int = 100
    special_requirements: List[str] = []
    
    # Partnership Details
    partnership_agreement_date: datetime
    verification_documents: List[str] = []
    tax_exempt_number: Optional[str] = None
    
    # Performance
    donations_received_via_platform: int = 0
    total_food_received_lbs: float = 0.0
    average_response_time_hours: float = 8.0
    satisfaction_rating: float = 5.0
    
    # Status
    is_active: bool = True
    is_accepting_donations: bool = True
    current_capacity_percentage: float = 75.0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models

class CharityProgramRegistrationRequest(BaseModel):
    committed_hours_per_month: int = Field(default=4, ge=2, le=40)
    preferred_charity_types: List[CharityType] = []
    preferred_locations: List[str] = []
    monthly_impact_goal: float = Field(default=50.0, ge=20.0, le=200.0)

class CharityActivitySubmissionRequest(BaseModel):
    activity_type: CharityType
    charity_organization_name: str
    activity_description: str
    activity_date: str  # ISO format
    food_donated_lbs: Optional[float] = None
    meals_provided: Optional[int] = None
    people_helped: Optional[int] = None
    volunteer_hours: Optional[float] = None
    location_address: str
    city: str
    state: str
    postal_code: str
    photo_urls: List[str] = []
    video_urls: List[str] = []
    witness_contacts: List[Dict[str, str]] = []

class PremiumMembershipUpgradeRequest(BaseModel):
    tier: PremiumTier
    payment_method: str = "charity_work"  # "charity_work", "payment", "both"
    monthly_payment_amount: float = 0.0
    charity_commitment: bool = True

class CharityActivityResponse(BaseModel):
    id: str
    activity_type: str
    charity_organization_name: str
    activity_description: str
    activity_date: datetime
    calculated_impact_score: float
    verification_status: str
    food_donated_lbs: Optional[float]
    meals_provided: Optional[int]
    people_helped: Optional[int]
    volunteer_hours: Optional[float]
    location: str
    submitted_at: datetime

class CommunityImpactResponse(BaseModel):
    user_total_impact: float
    user_monthly_impact: float
    platform_total_food_donated: float
    platform_total_meals_provided: int
    platform_total_people_helped: int
    user_rank_in_community: int
    recognition_level: str
    next_tier_requirement: float
    impact_badges: List[str]

class PremiumBenefitsResponse(BaseModel):
    tier: str
    tier_name: str
    monthly_cost: float
    charity_alternative: bool
    benefits: List[Dict[str, Any]]
    current_savings: float
    community_impact_level: str
    recognition_badges: List[str]