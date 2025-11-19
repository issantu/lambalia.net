"""
Lambalia Compliance System Models
State-specific cottage food law compliance for all 50 US states
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid


class ChefTier(str, Enum):
    """Chef certification tiers with order limits"""
    FULLY_CERTIFIED = "fully_certified"  # Cert + Insurance = Unlimited
    CERTIFIED_NO_INSURANCE = "certified_no_insurance"  # Cert only = 1-2 plates/day
    PENDING = "pending"  # No cert = No sales


class ComplianceStatus(str, Enum):
    """Chef compliance status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    PENDING_REVIEW = "pending_review"


class DocumentType(str, Enum):
    """Types of compliance documents"""
    FOOD_HANDLER_CERT = "food_handler_cert"
    COTTAGE_PERMIT = "cottage_permit"
    COMMERCIAL_LICENSE = "commercial_license"
    INSURANCE = "insurance"
    BUSINESS_LICENSE = "business_license"
    GOVERNMENT_ID = "government_id"
    PROOF_OF_ADDRESS = "proof_of_address"
    PRODUCT_LABEL = "product_label"
    RECIPE_TESTING = "recipe_testing"


# State Requirements Models
class StateRequirements(BaseModel):
    """Cottage food law requirements by state"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    state_code: str  # IL, CA, NY, etc.
    state_name: str  # Illinois, California, New York, etc.
    
    # Sales and registration
    sales_limit: Optional[int] = None  # Annual sales cap (None = unlimited)
    registration_required: bool = True
    registration_cost_range: str = "$0-250"
    
    # Training requirements
    training_required: bool = True
    training_type: str = "CFPM"  # CFPM, Food Handler Card, etc.
    training_validity_years: int = 5
    
    # Allowed/prohibited foods
    allowed_foods: List[str] = []
    prohibited_foods: List[str] = []
    
    # Labeling requirements
    labeling_requirements: Dict[str, Any] = {}
    disclaimer_text: str = ""
    
    # Additional requirements
    insurance_required: bool = False
    home_inspection_required: bool = False
    kitchen_requirements: List[str] = []
    
    # Sales venues
    direct_sales_allowed: bool = True
    online_sales_allowed: bool = True
    wholesale_allowed: bool = False
    
    # Resources
    health_dept_url: Optional[str] = None
    application_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Compliance Document Models
class ComplianceDocument(BaseModel):
    """Uploaded compliance document"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chef_id: str
    user_id: str
    document_type: DocumentType
    
    # File information
    filename: str
    file_path: str  # Path to stored file
    file_size: int  # Bytes
    content_type: str  # image/png, application/pdf, etc.
    
    # Document details
    document_number: Optional[str] = None  # Permit number, policy number, etc.
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    issuing_authority: Optional[str] = None
    
    # Verification
    verified: bool = False
    verified_by: Optional[str] = None  # Admin user ID
    verified_at: Optional[datetime] = None
    verification_notes: Optional[str] = None
    
    # Status
    status: str = "pending"  # pending, approved, rejected, expired
    rejection_reason: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChefCompliance(BaseModel):
    """Chef compliance profile"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chef_id: str  # Unique chef ID
    user_id: str  # Reference to users collection
    
    # State information
    state_code: str  # IL, CA, etc.
    state_name: str  # Illinois, California, etc.
    zip_code: str
    
    # Tier and limits
    tier: ChefTier = ChefTier.PENDING
    daily_order_limit: Optional[int] = None  # None = unlimited, 2 = max 2 orders/day
    
    # Compliance documents
    food_handler_cert_id: Optional[str] = None
    cottage_permit_id: Optional[str] = None
    insurance_id: Optional[str] = None
    business_license_id: Optional[str] = None
    government_id_id: Optional[str] = None
    proof_of_address_id: Optional[str] = None
    
    # Verification status
    food_handler_verified: bool = False
    cottage_permit_verified: bool = False
    insurance_verified: bool = False
    
    # Sales tracking
    annual_sales: float = 0.0
    current_year: int = Field(default_factory=lambda: datetime.utcnow().year)
    
    # Compliance status
    compliance_status: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
    status_reason: Optional[str] = None
    
    # Additional info
    cuisine_specialties: List[str] = []
    product_categories: List[str] = []  # baked_goods, jams, etc.
    
    # Admin notes
    admin_notes: Optional[str] = None
    last_reviewed_by: Optional[str] = None
    last_reviewed_at: Optional[datetime] = None
    
    # Expiration tracking
    next_expiration_date: Optional[date] = None  # Earliest expiring document
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Request/Response Models
class ChefComplianceRequest(BaseModel):
    """Request to create/update chef compliance profile"""
    state_code: str
    zip_code: str
    cuisine_specialties: List[str] = []
    product_categories: List[str] = []


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    document_id: str
    message: str
    status: str


class ChefComplianceResponse(BaseModel):
    """Chef compliance profile response"""
    chef_id: str
    user_id: str
    state_code: str
    state_name: str
    tier: ChefTier
    daily_order_limit: Optional[int]
    compliance_status: ComplianceStatus
    
    # Badge information
    badges: List[str] = []  # ["Certified Chef", "Insured", "Verified"]
    
    # Document status
    documents_required: List[str] = []
    documents_uploaded: List[str] = []
    documents_verified: List[str] = []
    
    # Sales info
    annual_sales: float
    sales_limit: Optional[int]
    sales_remaining: Optional[float]
    
    # Warnings
    expiring_soon: List[Dict[str, Any]] = []  # Documents expiring in 30 days
    warnings: List[str] = []
    
    created_at: datetime
    updated_at: datetime


class ChefDashboardStats(BaseModel):
    """Chef dashboard statistics"""
    chef_id: str
    tier: ChefTier
    compliance_status: ComplianceStatus
    
    # Order limits
    daily_order_limit: Optional[int]
    orders_today: int
    orders_remaining_today: Optional[int]
    
    # Sales
    annual_sales: float
    sales_limit: Optional[int]
    sales_percentage: float  # Percentage of limit used
    
    # Compliance
    compliance_percentage: int  # Overall compliance completion
    documents_pending: int
    documents_expiring_soon: int
    
    # Earnings
    total_earnings: float
    pending_payouts: float


class AdminReviewQueue(BaseModel):
    """Admin document review queue item"""
    document_id: str
    chef_id: str
    chef_name: str
    document_type: DocumentType
    uploaded_at: datetime
    days_pending: int
    priority: str  # high, medium, low
