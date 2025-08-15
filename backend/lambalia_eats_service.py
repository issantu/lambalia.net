# Lambalia Eats Service - Real-time Food Marketplace (Uber for Home Cooking)
import asyncio
import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

# Simple distance calculation without geopy for now
def calculate_distance_km(loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
    """Calculate approximate distance between two locations in kilometers"""
    try:
        # Simple Haversine formula approximation
        lat1, lng1 = loc1["lat"], loc1["lng"]
        lat2, lng2 = loc2["lat"], loc2["lng"]
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers
        r = 6371
        return c * r
    except:
        return float('inf')

from lambalia_eats_models import (
    FoodRequest, FoodOffer, ActiveOrder, EatsCookProfile, EatsEaterProfile,
    MatchingResult, EatsAnalytics, ServiceType, RequestStatus, OfferStatus,
    CuisineCategory, TransportationMethod
)

class EatsMatchingEngine:
    """Advanced matching engine for connecting eaters with cooks"""
    
    @staticmethod
    def calculate_distance_km(loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """Calculate distance between two locations in kilometers"""
        return calculate_distance_km(loc1, loc2)
    
    @staticmethod
    def calculate_match_score(request: FoodRequest, offer: FoodOffer) -> Tuple[float, List[str]]:
        """Calculate match score between food request and offer"""
        score = 0.0
        reasons = []
        
        # Cuisine match (25 points)
        if request.cuisine_type == offer.cuisine_type:
            score += 25
            reasons.append(f"Perfect cuisine match: {offer.cuisine_type.value}")
        
        # Price compatibility (20 points)
        if offer.price_per_serving <= request.max_price:
            price_ratio = offer.price_per_serving / request.max_price
            price_score = 20 * (1 - price_ratio * 0.5)  # Better score for lower prices
            score += price_score
            reasons.append(f"Price within budget: ${offer.price_per_serving} <= ${request.max_price}")
        else:
            score -= 10
            reasons.append(f"Price over budget: ${offer.price_per_serving} > ${request.max_price}")
        
        # Service type compatibility (15 points)
        common_services = set(request.preferred_service_types) & set(offer.available_service_types)
        if common_services:
            score += 15
            reasons.append(f"Service options match: {', '.join(common_services)}")
        
        # Distance scoring (15 points)
        distance = EatsMatchingEngine.calculate_distance_km(request.eater_location, offer.cook_location)
        if distance <= 2:
            score += 15
            reasons.append("Very close location (< 2km)")
        elif distance <= 5:
            score += 12
            reasons.append("Close location (< 5km)")
        elif distance <= 10:
            score += 8
            reasons.append("Reasonable distance (< 10km)")
        elif distance <= offer.delivery_radius_km:
            score += 5
            reasons.append(f"Within delivery range ({distance:.1f}km)")
        else:
            score -= 5
            reasons.append(f"Outside delivery range ({distance:.1f}km > {offer.delivery_radius_km}km)")
        
        # Timing compatibility (10 points)
        time_until_ready = (offer.ready_at - datetime.utcnow()).total_seconds() / 60
        if time_until_ready <= request.max_wait_time_minutes:
            timing_score = 10 * (1 - time_until_ready / request.max_wait_time_minutes)
            score += timing_score
            reasons.append(f"Good timing: ready in {int(time_until_ready)} minutes")
        
        # Dietary restrictions compatibility (10 points)
        if request.dietary_restrictions:
            dietary_matches = len(set(request.dietary_restrictions) & set(offer.dietary_info))
            if dietary_matches == len(request.dietary_restrictions):
                score += 10
                reasons.append("All dietary restrictions satisfied")
            elif dietary_matches > 0:
                score += 5
                reasons.append("Some dietary restrictions satisfied")
            else:
                score -= 5
                reasons.append("Dietary restrictions not met")
        
        # Availability (5 points)
        if offer.quantity_remaining > 0:
            score += 5
            reasons.append(f"Available quantity: {offer.quantity_remaining}")
        else:
            score -= 10
            reasons.append("No quantity available")
        
        return max(0, score), reasons
    
    @staticmethod
    async def find_matches_for_request(request: FoodRequest, available_offers: List[FoodOffer]) -> List[Dict[str, Any]]:
        """Find and rank matching offers for a food request"""
        matches = []
        
        for offer in available_offers:
            if offer.status != OfferStatus.AVAILABLE or offer.quantity_remaining <= 0:
                continue
                
            score, reasons = EatsMatchingEngine.calculate_match_score(request, offer)
            
            if score > 30:  # Minimum viable match score
                distance = EatsMatchingEngine.calculate_distance_km(request.eater_location, offer.cook_location)
                
                matches.append({
                    "offer_id": offer.id,
                    "offer": offer,
                    "match_score": score,
                    "match_reasons": reasons,
                    "distance_km": distance,
                    "estimated_total_cost": offer.price_per_serving + offer.delivery_fee,
                    "estimated_ready_time": offer.ready_at
                })
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:10]  # Return top 10 matches

class LambaliaEatsService:
    """Main service for Lambalia Eats real-time food marketplace"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.matching_engine = EatsMatchingEngine()
        self.logger = logging.getLogger(__name__)
    
    # FOOD REQUEST MANAGEMENT
    
    async def create_food_request(self, request_data: Dict[str, Any], eater_id: str) -> FoodRequest:
        """Create a new food request from hungry eater"""
        
        # Parse datetime strings
        if request_data.get("preferred_pickup_time"):
            request_data["preferred_pickup_time"] = datetime.fromisoformat(
                request_data["preferred_pickup_time"].replace('Z', '+00:00')
            )
        
        food_request = FoodRequest(
            eater_id=eater_id,
            **request_data
        )
        
        await self.db.food_requests.insert_one(food_request.dict())
        
        # Immediately try to find matches
        await self._find_and_notify_matches(food_request)
        
        self.logger.info(f"Food request created: {food_request.id} by eater {eater_id}")
        return food_request
    
    async def create_food_offer(self, offer_data: Dict[str, Any], cook_id: str) -> FoodOffer:
        """Create a new food offer from cook"""
        
        # Parse datetime strings
        offer_data["ready_at"] = datetime.fromisoformat(offer_data["ready_at"].replace('Z', '+00:00'))
        offer_data["available_until"] = datetime.fromisoformat(offer_data["available_until"].replace('Z', '+00:00'))
        
        # Get cook info for standalone app users
        cook_profile = await self.db.eats_cook_profiles.find_one({"user_id": cook_id}, {"_id": 0})
        if cook_profile:
            offer_data.update({
                "cook_name": cook_profile["display_name"],
                "cook_rating": cook_profile["overall_rating"],
                "cook_photo_url": cook_profile.get("profile_photo_url"),
                "cook_specialties": cook_profile.get("specialties", [])
            })
        
        food_offer = FoodOffer(
            cook_id=cook_id,
            quantity_remaining=offer_data["quantity_available"],
            **offer_data
        )
        
        await self.db.food_offers.insert_one(food_offer.dict())
        
        # Find matching requests
        await self._find_matching_requests(food_offer)
        
        self.logger.info(f"Food offer created: {food_offer.id} by cook {cook_id}")
        return food_offer
    
    async def get_nearby_offers(self, eater_location: Dict[str, float], radius_km: float = 15, 
                              cuisine_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get nearby food offers for browsing"""
        
        # Build query
        query = {
            "status": OfferStatus.AVAILABLE,
            "quantity_remaining": {"$gt": 0},
            "available_until": {"$gt": datetime.utcnow()}
        }
        
        if cuisine_filter:
            query["cuisine_type"] = cuisine_filter
        
        offers = await self.db.food_offers.find(query, {"_id": 0}).to_list(length=50)
        
        # Filter by distance and add distance info
        nearby_offers = []
        for offer in offers:
            distance = self.matching_engine.calculate_distance_km(eater_location, offer["cook_location"])
            if distance <= radius_km:
                offer["distance_km"] = round(distance, 1)
                offer["estimated_delivery_time"] = self._calculate_delivery_time(distance, offer.get("ready_at"))
                nearby_offers.append(offer)
        
        # Sort by distance
        nearby_offers.sort(key=lambda x: x["distance_km"])
        return nearby_offers
    
    async def get_active_requests(self, cook_location: Dict[str, float], radius_km: float = 20) -> List[Dict[str, Any]]:
        """Get active food requests for cooks to respond to"""
        
        query = {
            "status": RequestStatus.POSTED,
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        requests = await self.db.food_requests.find(query, {"_id": 0}).to_list(length=30)
        
        # Filter by distance and add match info
        matching_requests = []
        for request in requests:
            distance = self.matching_engine.calculate_distance_km(cook_location, request["eater_location"])
            if distance <= radius_km:
                request["distance_km"] = round(distance, 1)
                expires_at = request["expires_at"]
                if isinstance(expires_at, str):
                    expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                request["time_until_expires"] = int((expires_at - datetime.utcnow()).total_seconds() / 60)
                matching_requests.append(request)
        
        # Sort by urgency (expiration time)
        matching_requests.sort(key=lambda x: x["time_until_expires"])
        return matching_requests
    
    # ORDER MANAGEMENT
    
    async def place_order(self, order_data: Dict[str, Any], eater_id: str) -> ActiveOrder:
        """Place an order (from offer or accepting a request)"""
        
        offer_id = order_data.get("offer_id")
        request_id = order_data.get("request_id")
        
        if offer_id:
            # Ordering from an available offer
            offer = await self.db.food_offers.find_one({"id": offer_id}, {"_id": 0})
            if not offer or offer["quantity_remaining"] <= 0:
                raise ValueError("Offer not available")
            
            # Update offer quantity
            await self.db.food_offers.update_one(
                {"id": offer_id},
                {"$inc": {"quantity_remaining": -order_data.get("quantity", 1)}}
            )
            
            # Handle datetime parsing for ready_at
            ready_at = offer["ready_at"]
            if isinstance(ready_at, str):
                ready_at = datetime.fromisoformat(ready_at.replace('Z', '+00:00'))
            
            order = ActiveOrder(
                eater_id=eater_id,
                cook_id=offer["cook_id"],
                offer_id=offer_id,
                dish_name=offer["dish_name"],
                quantity=order_data.get("quantity", 1),
                service_type=ServiceType(order_data["service_type"]),
                eater_location=order_data.get("eater_location", {}),
                cook_location=offer["cook_location"],
                delivery_address=order_data.get("delivery_address"),
                estimated_ready_time=ready_at,
                meal_price=offer["price_per_serving"] * order_data.get("quantity", 1),
                delivery_fee=offer.get("delivery_fee", 0) if order_data["service_type"] == "delivery" else 0,
                service_fee=self._calculate_service_fee(offer["price_per_serving"] * order_data.get("quantity", 1)),
                total_amount=self._calculate_total_amount(offer, order_data)
            )
            
        elif request_id:
            # Cook accepting a food request
            request = await self.db.food_requests.find_one({"id": request_id}, {"_id": 0})
            if not request or request["status"] != RequestStatus.POSTED:
                raise ValueError("Request not available")
            
            # Update request status
            await self.db.food_requests.update_one(
                {"id": request_id},
                {"$set": {"status": RequestStatus.MATCHED, "matched_cook_id": eater_id}}  # Note: eater_id is actually cook_id in this context
            )
            
            order = ActiveOrder(
                eater_id=request["eater_id"],
                cook_id=eater_id,  # In this case, eater_id is the cook accepting the request
                request_id=request_id,
                dish_name=request["dish_name"],
                quantity=1,
                service_type=ServiceType(order_data["service_type"]),
                eater_location=request["eater_location"],
                cook_location=order_data.get("cook_location", {}),
                delivery_address=order_data.get("delivery_address"),
                estimated_ready_time=datetime.utcnow() + timedelta(minutes=order_data.get("preparation_time", 45)),
                meal_price=order_data.get("agreed_price", request["max_price"]),
                delivery_fee=order_data.get("delivery_fee", 0),
                service_fee=self._calculate_service_fee(order_data.get("agreed_price", request["max_price"])),
                total_amount=order_data.get("agreed_price", request["max_price"]) + order_data.get("delivery_fee", 0)
            )
        else:
            raise ValueError("Either offer_id or request_id must be provided")
        
        # Calculate estimated delivery time for delivery orders
        if order.service_type == ServiceType.DELIVERY:
            distance = self.matching_engine.calculate_distance_km(order.cook_location, order.eater_location)
            order.estimated_delivery_time = order.estimated_ready_time + timedelta(minutes=self._calculate_delivery_time_minutes(distance))
        
        await self.db.active_orders.insert_one(order.dict())
        
        # Send real-time notification
        await self._send_order_notification(order)
        
        self.logger.info(f"Order placed: {order.id}")
        return order
    
    async def update_order_status(self, order_id: str, new_status: str, update_data: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Update order status with real-time tracking"""
        
        update_doc = {
            "current_status": new_status,
            "updated_at": datetime.utcnow(),
            **update_data
        }
        
        # Add status update to tracking history
        status_update = {
            "status": new_status,
            "timestamp": datetime.utcnow(),
            "message": update_data.get("message", f"Order status updated to {new_status}"),
            "location": update_data.get("location")
        }
        
        await self.db.active_orders.update_one(
            {"id": order_id},
            {
                "$set": update_doc,
                "$push": {"status_updates": status_update}
            }
        )
        
        # Send real-time update to both eater and cook
        await self._send_status_update(order_id, status_update)
        
        return {"success": True, "new_status": new_status}
    
    async def get_order_tracking(self, order_id: str) -> Dict[str, Any]:
        """Get real-time order tracking information"""
        
        order = await self.db.active_orders.find_one({"id": order_id}, {"_id": 0})
        if not order:
            raise ValueError("Order not found")
        
        # Calculate estimated times
        now = datetime.utcnow()
        estimated_ready = order["estimated_ready_time"]
        if isinstance(estimated_ready, str):
            estimated_ready = datetime.fromisoformat(estimated_ready.replace('Z', '+00:00'))
        
        tracking_info = {
            "order_id": order_id,
            "current_status": order["current_status"],
            "dish_name": order["dish_name"],
            "service_type": order["service_type"],
            "tracking_code": order["tracking_code"],
            "estimated_ready_time": order["estimated_ready_time"],
            "time_until_ready": max(0, int((estimated_ready - now).total_seconds() / 60)),
            "status_updates": order.get("status_updates", []),
            "cook_location": order.get("cook_location"),
            "eater_location": order.get("eater_location"),
            "driver_location": order.get("driver_location")
        }
        
        # Add delivery-specific info
        if order["service_type"] == "delivery" and order.get("estimated_delivery_time"):
            estimated_delivery = order["estimated_delivery_time"]
            if isinstance(estimated_delivery, str):
                estimated_delivery = datetime.fromisoformat(estimated_delivery.replace('Z', '+00:00'))
            tracking_info.update({
                "estimated_delivery_time": order["estimated_delivery_time"],
                "time_until_delivery": max(0, int((estimated_delivery - now).total_seconds() / 60))
            })
        
        return tracking_info
    
    # PROFILE MANAGEMENT
    
    async def create_cook_profile(self, profile_data: Dict[str, Any], user_id: str) -> EatsCookProfile:
        """Create cook profile for Lambalia Eats"""
        
        profile = EatsCookProfile(
            user_id=user_id,
            **profile_data
        )
        
        await self.db.eats_cook_profiles.insert_one(profile.dict())
        return profile
    
    async def create_eater_profile(self, profile_data: Dict[str, Any], user_id: Optional[str] = None) -> EatsEaterProfile:
        """Create eater profile for Lambalia Eats (can be standalone)"""
        
        profile = EatsEaterProfile(
            user_id=user_id,
            **profile_data
        )
        
        await self.db.eats_eater_profiles.insert_one(profile.dict())
        return profile
    
    # ANALYTICS & INSIGHTS
    
    async def get_platform_stats(self) -> Dict[str, Any]:
        """Get real-time platform statistics"""
        
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Active counts
        active_requests = await self.db.food_requests.count_documents({
            "status": RequestStatus.POSTED,
            "expires_at": {"$gt": now}
        })
        
        active_offers = await self.db.food_offers.count_documents({
            "status": OfferStatus.AVAILABLE,
            "quantity_remaining": {"$gt": 0},
            "available_until": {"$gt": now}
        })
        
        orders_in_progress = await self.db.active_orders.count_documents({
            "current_status": {"$in": ["confirmed", "preparing", "ready", "in_transit"]}
        })
        
        available_cooks = await self.db.eats_cook_profiles.count_documents({
            "is_currently_available": True,
            "is_active": True
        })
        
        # Popular cuisines today
        cuisine_pipeline = [
            {"$match": {"created_at": {"$gte": today_start}}},
            {"$group": {"_id": "$cuisine_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        
        popular_cuisines = await self.db.food_offers.aggregate(cuisine_pipeline).to_list(length=5)
        
        # Revenue today
        revenue_pipeline = [
            {"$match": {
                "ordered_at": {"$gte": today_start},
                "current_status": "completed"
            }},
            {"$group": {
                "_id": None,
                "total_commission": {"$sum": "$service_fee"}
            }}
        ]
        
        revenue_result = await self.db.active_orders.aggregate(revenue_pipeline).to_list(length=1)
        commission_today = revenue_result[0]["total_commission"] if revenue_result else 0.0
        
        return {
            "active_requests": active_requests,
            "active_offers": active_offers,
            "orders_in_progress": orders_in_progress,
            "available_cooks": available_cooks,
            "average_match_time_minutes": 3.5,  # Mock data - would calculate from actual matches
            "popular_cuisines": [{"cuisine": c["_id"], "count": c["count"]} for c in popular_cuisines],
            "platform_commission_today": commission_today
        }
    
    # PRIVATE HELPER METHODS
    
    async def _find_and_notify_matches(self, request: FoodRequest):
        """Find matching offers for a new request and notify cooks"""
        
        # Get available offers
        offers = await self.db.food_offers.find({
            "status": OfferStatus.AVAILABLE,
            "quantity_remaining": {"$gt": 0},
            "available_until": {"$gt": datetime.utcnow()}
        }, {"_id": 0}).to_list(length=50)
        
        offer_objects = [FoodOffer(**offer) for offer in offers]
        matches = await self.matching_engine.find_matches_for_request(request, offer_objects)
        
        if matches:
            # Store matching results
            matching_result = MatchingResult(
                request_id=request.id,
                matched_offers=[m for m in matches[:5]],  # Top 5 matches
                match_score=matches[0]["match_score"] if matches else 0
            )
            await self.db.matching_results.insert_one(matching_result.dict())
            
            # TODO: Send real-time notifications to matched cooks
            self.logger.info(f"Found {len(matches)} matches for request {request.id}")
    
    async def _find_matching_requests(self, offer: FoodOffer):
        """Find matching requests for a new offer"""
        
        requests = await self.db.food_requests.find({
            "status": RequestStatus.POSTED,
            "expires_at": {"$gt": datetime.utcnow()}
        }, {"_id": 0}).to_list(length=30)
        
        # Find compatible requests
        compatible_requests = []
        for request_data in requests:
            request = FoodRequest(**request_data)
            score, reasons = self.matching_engine.calculate_match_score(request, offer)
            
            if score > 40:  # Higher threshold for offer-to-request matching
                compatible_requests.append({
                    "request_id": request.id,
                    "match_score": score,
                    "eater_id": request.eater_id
                })
        
        if compatible_requests:
            # TODO: Send notifications to compatible eaters
            self.logger.info(f"Offer {offer.id} matches {len(compatible_requests)} requests")
    
    def _calculate_service_fee(self, meal_price: float) -> float:
        """Calculate Lambalia's service fee (commission)"""
        return meal_price * 0.15  # 15% commission
    
    def _calculate_total_amount(self, offer: Dict[str, Any], order_data: Dict[str, Any]) -> float:
        """Calculate total order amount"""
        meal_price = offer["price_per_serving"] * order_data.get("quantity", 1)
        delivery_fee = offer.get("delivery_fee", 0) if order_data["service_type"] == "delivery" else 0
        service_fee = self._calculate_service_fee(meal_price)
        transport_fee = 0  # TODO: Calculate transport fee for dine-in transport
        
        return meal_price + delivery_fee + service_fee + transport_fee
    
    def _calculate_delivery_time_minutes(self, distance_km: float) -> int:
        """Calculate estimated delivery time based on distance"""
        if distance_km <= 2:
            return 15
        elif distance_km <= 5:
            return 25
        elif distance_km <= 10:
            return 35
        else:
            return 45
    
    def _calculate_delivery_time(self, distance_km: float, ready_at: datetime) -> datetime:
        """Calculate estimated delivery time"""
        delivery_minutes = self._calculate_delivery_time_minutes(distance_km)
        return ready_at + timedelta(minutes=delivery_minutes)
    
    async def _send_order_notification(self, order: ActiveOrder):
        """Send real-time order notification"""
        # TODO: Implement WebSocket notifications
        pass
    
    async def _send_status_update(self, order_id: str, status_update: Dict[str, Any]):
        """Send real-time status update"""
        # TODO: Implement WebSocket status updates
        pass