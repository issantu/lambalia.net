"""
Lambalia User Types System
Multi-role user system with state-based compliance
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class UserType(str, Enum):
    """User types with different platform capabilities"""
    FOOD_ENTHUSIAST = "food_enthusiast"  # Buyer only
    HOME_CHEF = "home_chef"  # Cottage food seller
    HOME_RESTAURANT = "home_restaurant"  # Dining service provider
    RECIPE_CREATOR = "recipe_creator"  # Content creator
    FOOD_REVIEWER = "food_reviewer"  # Reviews and ratings
    FARM_VENDOR = "farm_vendor"  # Farm-to-table seller


class StateCategory(str, Enum):
    """State regulatory categories"""
    FOOD_FREEDOM = "food_freedom"  # WY, ND, UT, ME, OK, AK
    PERMISSIVE = "permissive"  # TX, CO, FL, MO, TN, etc.
    MODERATE = "moderate"  # IL, CA, NY, VA, etc.
    RESTRICTIVE = "restrictive"  # HI, KS


class UserTypeProfile(BaseModel):
    """User's selected types and compliance status"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Selected user types (can have multiple)
    user_types: List[UserType] = [UserType.FOOD_ENTHUSIAST]
    primary_type: UserType = UserType.FOOD_ENTHUSIAST
    
    # Location
    state_code: str
    state_name: str
    state_category: StateCategory
    zip_code: str
    
    # Disclaimer acceptance
    disclaimer_accepted: bool = False
    disclaimer_accepted_at: Optional[datetime] = None
    disclaimer_version: str = "1.0"
    
    # Compliance status per type
    compliance_status: Dict[str, str] = {}  # {user_type: "active"|"pending"|"suspended"}
    
    # Quick access flags
    can_sell_packaged_foods: bool = False  # Home chef capability
    can_serve_meals: bool = False  # Home restaurant capability
    can_create_content: bool = True  # Recipe creator
    can_review: bool = True  # Food reviewer
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StateRegulation(BaseModel):
    """State-specific regulations"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    state_code: str
    state_name: str
    state_category: StateCategory
    
    # Requirements by user type
    home_chef_requirements: Dict[str, Any] = {}
    home_restaurant_requirements: Dict[str, Any] = {}
    farm_vendor_requirements: Dict[str, Any] = {}
    
    # Quick reference
    cottage_food_allowed: bool = True
    home_dining_allowed: bool = False
    sales_cap: Optional[int] = None  # Annual sales limit
    
    # Resources
    health_dept_url: Optional[str] = None
    resources: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UniversalDisclaimer(BaseModel):
    """Universal platform disclaimer"""
    version: str = "1.0"
    title: str = "Lambalia Platform Disclaimer"
    content: str = """
    IMPORTANT - PLEASE READ CAREFULLY
    
    By using Lambalia, you acknowledge and agree that:
    
    1. INDEPENDENT TRANSACTIONS: All food sales, purchases, and services occur directly between independent users. Lambalia is a marketplace platform only and is not a party to any transaction.
    
    2. FOOD SAFETY RESPONSIBILITY: Food safety, quality, preparation standards, and compliance with all applicable health codes and food safety regulations are the sole responsibility of food providers (Home Chefs, Home Restaurants, Farm Vendors).
    
    3. LEGAL COMPLIANCE: Users are solely responsible for compliance with all federal, state, and local laws, including but not limited to:
       - Cottage food laws and permits
       - Commercial kitchen licensing
       - Food handler certifications
       - Business licenses
       - Tax obligations
       - Zoning regulations
    
    4. NO GUARANTEES: Lambalia makes no representations or warranties regarding:
       - Food safety or quality
       - Accuracy of user-provided information
       - Compliance with applicable laws
       - Availability of products or services
    
    5. ASSUMPTION OF RISK: Users acknowledge that consuming food prepared by others carries inherent risks, including but not limited to foodborne illness, allergic reactions, and food contamination.
    
    6. LIABILITY RELEASE: You agree to release, indemnify, and hold harmless Lambalia, its officers, directors, employees, and agents from any and all claims, damages, liabilities, costs, and expenses (including attorney fees) arising from:
       - Use of the platform
       - Food transactions between users
       - Food safety incidents
       - Non-compliance with applicable laws
       - User-generated content
    
    7. DISPUTE RESOLUTION: Any disputes between users must be resolved directly between the parties. Lambalia is not responsible for mediating or resolving user disputes.
    
    8. USER VERIFICATION: While Lambalia may provide tools for document verification and compliance tracking, users are solely responsible for verifying the credentials, permits, and compliance status of other users.
    
    BY CLICKING "I ACCEPT" OR USING THE PLATFORM, YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTOOD, AND AGREE TO BE BOUND BY THIS DISCLAIMER.
    """
    effective_date: datetime = Field(default_factory=datetime.utcnow)


class UserTypeChangeRequest(BaseModel):
    """Request to add/change user types"""
    user_id: str
    add_types: List[UserType] = []
    remove_types: List[UserType] = []
    new_primary_type: Optional[UserType] = None


class UserTypeResponse(BaseModel):
    """Response with user type info and requirements"""
    user_id: str
    user_types: List[UserType]
    primary_type: UserType
    state_code: str
    state_name: str
    state_category: StateCategory
    
    # Capabilities
    can_sell_packaged_foods: bool
    can_serve_meals: bool
    can_create_content: bool
    can_review: bool
    
    # Requirements by type
    requirements: Dict[str, List[str]]  # {user_type: [list of requirements]}
    
    # Compliance status
    compliance_status: Dict[str, str]
    
    # Warnings
    warnings: List[str] = []
