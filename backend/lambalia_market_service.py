import math
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from lambalia_market_models import (
    MarketItemCreate, MarketItemResponse, MarketItemType, MarketItemStatus,
    MarketSubscriptionRequest, MarketSubscriptionResponse, FulfillmentType,
    MarketSearchRequest, MarketDashboardResponse, GeoLocation
)

class LambaliaMarketService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.offers_collection = db.market_offers
        self.demands_collection = db.market_demands
        self.subscriptions_collection = db.market_subscriptions
        self.locations_collection = db.geo_locations

    async def create_offer(self, user_id: str, user_name: str, offer_data: MarketItemCreate) -> MarketItemResponse:
        """Create a new food offer"""
        offer_dict = offer_data.dict()
        offer_dict.update({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "user_name": user_name,
            "item_type": MarketItemType.OFFER,
            "status": MarketItemStatus.ACTIVE,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_locked": False
        })
        
        # Set expiration if not provided (default 24 hours)
        if not offer_dict.get("expires_at"):
            offer_dict["expires_at"] = datetime.utcnow() + timedelta(hours=24)
        
        await self.offers_collection.insert_one(offer_dict)
        return MarketItemResponse(**offer_dict)

    async def create_demand(self, user_id: str, user_name: str, demand_data: MarketItemCreate) -> MarketItemResponse:
        """Create a new food demand"""
        demand_dict = demand_data.dict()
        demand_dict.update({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "user_name": user_name,
            "item_type": MarketItemType.DEMAND,
            "status": MarketItemStatus.ACTIVE,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_locked": False
        })
        
        # Set expiration if not provided (default 48 hours for demands)
        if not demand_dict.get("expires_at"):
            demand_dict["expires_at"] = datetime.utcnow() + timedelta(hours=48)
        
        await self.demands_collection.insert_one(demand_dict)
        return MarketItemResponse(**demand_dict)

    async def get_offers_by_location(self, postal_code: Optional[str] = None, radius_miles: float = 10) -> List[MarketItemResponse]:
        """Get food offers by geographic location"""
        query = {
            "status": MarketItemStatus.ACTIVE,
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        if postal_code:
            # In production, implement proper geocoding and distance calculation
            query["postal_code"] = postal_code
        
        cursor = self.offers_collection.find(query).sort("created_at", -1)
        offers = await cursor.to_list(100)
        
        # Calculate mock distances and add user ratings
        import random
        result = []
        for offer in offers:
            offer["distance_miles"] = round(random.random() * radius_miles, 1)
            offer["user_rating"] = round(4.0 + random.random() * 1.0, 1)  # Mock rating 4.0-5.0
            result.append(MarketItemResponse(**offer))
        
        return result

    async def get_demands_by_location(self, postal_code: Optional[str] = None, radius_miles: float = 10) -> List[MarketItemResponse]:
        """Get food demands by geographic location"""
        query = {
            "status": MarketItemStatus.ACTIVE,
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        if postal_code:
            query["postal_code"] = postal_code
        
        cursor = self.demands_collection.find(query).sort("created_at", -1)
        demands = await cursor.to_list(100)
        
        # Calculate mock distances
        import random
        result = []
        for demand in demands:
            demand["distance_miles"] = round(random.random() * radius_miles, 1)
            result.append(MarketItemResponse(**demand))
        
        return result

    async def subscribe_to_offer(self, user_id: str, subscription_request: MarketSubscriptionRequest) -> MarketSubscriptionResponse:
        """Subscribe to a food offer (user wants to buy)"""
        # Get the offer
        offer = await self.offers_collection.find_one({"id": subscription_request.item_id})
        if not offer:
            raise ValueError("Offer not found")
        
        if offer["is_locked"]:
            raise ValueError("Offer is already locked")
        
        if offer["user_id"] == user_id:
            raise ValueError("Cannot subscribe to your own offer")
        
        # Calculate pricing
        total_amount = offer["price_per_person"] * offer["quantity_people"]
        platform_commission = total_amount * 0.15  # 15%
        user_earnings = total_amount - platform_commission
        
        # Create subscription
        subscription_dict = {
            "id": str(uuid.uuid4()),
            "item_id": subscription_request.item_id,
            "subscriber_user_id": user_id,
            "item_owner_user_id": offer["user_id"],
            "fulfillment_type": subscription_request.fulfillment_type,
            "total_amount": total_amount,
            "platform_commission": platform_commission,
            "user_earnings": user_earnings,
            "status": "pending",
            "notes": subscription_request.notes,
            "created_at": datetime.utcnow(),
            "estimated_completion_time": datetime.utcnow() + timedelta(hours=offer["preparation_time_hours"])
        }
        
        # Lock the offer
        await self.offers_collection.update_one(
            {"id": subscription_request.item_id},
            {
                "$set": {
                    "is_locked": True,
                    "locked_by_user_id": user_id,
                    "locked_at": datetime.utcnow(),
                    "status": MarketItemStatus.LOCKED
                }
            }
        )
        
        # Save subscription
        await self.subscriptions_collection.insert_one(subscription_dict)
        
        return MarketSubscriptionResponse(**subscription_dict)

    async def subscribe_to_demand(self, user_id: str, subscription_request: MarketSubscriptionRequest) -> MarketSubscriptionResponse:
        """Subscribe to a food demand (user wants to fulfill/cook)"""
        # Get the demand
        demand = await self.demands_collection.find_one({"id": subscription_request.item_id})
        if not demand:
            raise ValueError("Demand not found")
        
        if demand["is_locked"]:
            raise ValueError("Demand is already locked")
        
        if demand["user_id"] == user_id:
            raise ValueError("Cannot subscribe to your own demand")
        
        # Calculate pricing
        total_amount = demand["price_per_person"] * demand["quantity_people"]
        platform_commission = total_amount * 0.15  # 15%
        user_earnings = total_amount - platform_commission
        
        # Create subscription
        subscription_dict = {
            "id": str(uuid.uuid4()),
            "item_id": subscription_request.item_id,
            "subscriber_user_id": user_id,  # The cook
            "item_owner_user_id": demand["user_id"],  # The person who wants the food
            "fulfillment_type": subscription_request.fulfillment_type,
            "total_amount": total_amount,
            "platform_commission": platform_commission,
            "user_earnings": user_earnings,
            "status": "pending",
            "notes": subscription_request.notes,
            "created_at": datetime.utcnow(),
            "estimated_completion_time": datetime.utcnow() + timedelta(hours=demand["preparation_time_hours"])
        }
        
        # Lock the demand
        await self.demands_collection.update_one(
            {"id": subscription_request.item_id},
            {
                "$set": {
                    "is_locked": True,
                    "locked_by_user_id": user_id,
                    "locked_at": datetime.utcnow(),
                    "status": MarketItemStatus.LOCKED
                }
            }
        )
        
        # Save subscription
        await self.subscriptions_collection.insert_one(subscription_dict)
        
        return MarketSubscriptionResponse(**subscription_dict)

    async def get_user_dashboard(self, user_id: str) -> MarketDashboardResponse:
        """Get user's market dashboard data"""
        # Count user's active offers and demands
        my_active_offers = await self.offers_collection.count_documents({
            "user_id": user_id,
            "status": {"$in": [MarketItemStatus.ACTIVE, MarketItemStatus.LOCKED]}
        })
        
        my_active_demands = await self.demands_collection.count_documents({
            "user_id": user_id,
            "status": {"$in": [MarketItemStatus.ACTIVE, MarketItemStatus.LOCKED]}
        })
        
        # Count total market activity
        total_offers = await self.offers_collection.count_documents({
            "status": MarketItemStatus.ACTIVE,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        total_demands = await self.demands_collection.count_documents({
            "status": MarketItemStatus.ACTIVE,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        # Get user's completed transactions
        completed_subscriptions = await self.subscriptions_collection.find({
            "$or": [
                {"subscriber_user_id": user_id},
                {"item_owner_user_id": user_id}
            ],
            "status": "completed"
        }).to_list(100)
        
        my_completed_transactions = len(completed_subscriptions)
        total_earnings = sum(sub["user_earnings"] for sub in completed_subscriptions if sub["item_owner_user_id"] == user_id)
        
        # Get recent activity
        recent_activity = []
        recent_subs = await self.subscriptions_collection.find({
            "$or": [
                {"subscriber_user_id": user_id},
                {"item_owner_user_id": user_id}
            ]
        }).sort("created_at", -1).limit(5).to_list(5)
        
        for sub in recent_subs:
            activity = {
                "type": "subscription",
                "description": f"{'Sold' if sub['item_owner_user_id'] == user_id else 'Bought'} {sub.get('item_name', 'item')}",
                "amount": sub["total_amount"],
                "date": sub["created_at"],
                "status": sub["status"]
            }
            recent_activity.append(activity)
        
        return MarketDashboardResponse(
            total_offers=total_offers,
            total_demands=total_demands,
            my_active_offers=my_active_offers,
            my_active_demands=my_active_demands,
            my_completed_transactions=my_completed_transactions,
            total_earnings=total_earnings,
            recent_activity=recent_activity
        )

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in miles using Haversine formula"""
        R = 3959  # Earth's radius in miles
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c