from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class MarketItemType(str, Enum):
    OFFER = "offer"
    DEMAND = "demand"

class FulfillmentType(str, Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"
    SERVICING = "servicing"

class SpiceLevel(str, Enum):
    MILD = "mild"
    MEDIUM = "medium"
    HOT = "hot"
    VERY_HOT = "very_hot"

class MarketItemStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    COMPLETED = "completed"
    EXPIRED = "expired"

# Base models for offers and demands
class MarketItemBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1000)
    dish_name: str = Field(..., max_length=100)
    cuisine_type: str = Field(..., max_length=50)
    quantity_people: int = Field(..., ge=1, le=50)
    price_per_person: float = Field(..., ge=0)
    postal_code: str = Field(..., max_length=20)
    pickup_available: bool = True
    delivery_available: bool = False
    preparation_time_hours: float = Field(1.0, ge=0.5, le=48)
    dietary_restrictions: List[str] = Field(default_factory=list)
    spice_level: SpiceLevel = SpiceLevel.MILD
    expires_at: Optional[datetime] = None

class MarketItemCreate(MarketItemBase):
    pass

class MarketItemResponse(MarketItemBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    user_rating: Optional[float] = None
    item_type: MarketItemType
    status: MarketItemStatus = MarketItemStatus.ACTIVE
    distance_miles: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_locked: bool = False
    locked_by_user_id: Optional[str] = None
    locked_at: Optional[datetime] = None

class MarketItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price_per_person: Optional[float] = None
    pickup_available: Optional[bool] = None
    delivery_available: Optional[bool] = None
    status: Optional[MarketItemStatus] = None

# Subscription models
class MarketSubscriptionRequest(BaseModel):
    item_id: str
    fulfillment_type: FulfillmentType
    notes: Optional[str] = None

class MarketSubscriptionResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    subscriber_user_id: str
    item_owner_user_id: str
    fulfillment_type: FulfillmentType
    total_amount: float
    platform_commission: float = Field(default=0.15)  # 15% commission
    user_earnings: float
    status: str = "pending"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_completion_time: Optional[datetime] = None

# Geographic search models
class LocationSearchRequest(BaseModel):
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_miles: float = Field(default=10, ge=1, le=50)

class MarketSearchFilters(BaseModel):
    cuisine_type: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    spice_level: Optional[SpiceLevel] = None
    pickup_only: bool = False
    delivery_only: bool = False
    available_now: bool = False

class MarketSearchRequest(LocationSearchRequest, MarketSearchFilters):
    pass

class MarketDashboardResponse(BaseModel):
    total_offers: int
    total_demands: int
    my_active_offers: int
    my_active_demands: int
    my_completed_transactions: int
    total_earnings: float
    recent_activity: List[Dict[str, Any]]

# Location and distance calculation models
class GeoLocation(BaseModel):
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None