# Daily Marketplace Service - Dynamic Offer & Demand System
import math
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from marketplace_daily_models import (
    CookingOffer, EatingRequest, CookOfferMatch, CookingAppointment,
    CookingOfferStatus, EatingRequestStatus, AppointmentStatus, MealCategory
)

class LocalMatchingService:
    """Service for matching cooks and eaters based on location and preferences"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    def calculate_distance(self, coord1: List[float], coord2: List[float]) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
        lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Earth's radius in kilometers
        
        return r * c
    
    def is_within_us_zip_code_area(self, zip1: str, zip2: str) -> bool:
        """Check if two US ZIP codes are in the same general area (simplified)"""
        if len(zip1) >= 3 and len(zip2) >= 3:
            # Same first 3 digits generally means same metropolitan area
            return zip1[:3] == zip2[:3]
        return zip1 == zip2
    
    async def find_matching_offers(self, eating_request: EatingRequest) -> List[CookOfferMatch]:
        """Find cooking offers that match an eating request"""
        matches = []
        
        # Build query for potential offers
        query = {
            "status": CookingOfferStatus.ACTIVE,
            "remaining_servings": {"$gte": eating_request.number_of_servings},
            "price_per_serving": {"$lte": eating_request.max_price_per_serving},
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        # Add dietary filters
        if "vegetarian" in eating_request.dietary_restrictions:
            query["is_vegetarian"] = True
        if "vegan" in eating_request.dietary_restrictions:
            query["is_vegan"] = True
        if "gluten_free" in eating_request.dietary_restrictions:
            query["is_gluten_free"] = True
        if "halal" in eating_request.dietary_restrictions:
            query["is_halal"] = True
        if "kosher" in eating_request.dietary_restrictions:
            query["is_kosher"] = True
        
        # Category filter
        if eating_request.category:
            query["category"] = eating_request.category
        
        # Cuisine filter
        if eating_request.desired_cuisine:
            query["cuisine_type"] = {"$regex": eating_request.desired_cuisine, "$options": "i"}
        
        offers_cursor = self.db.cooking_offers.find(query, {"_id": 0})
        offers = await offers_cursor.to_list(length=100)
        
        for offer_doc in offers:
            offer = CookingOffer(**offer_doc)
            
            # Calculate distance
            distance_km = self.calculate_distance(
                eating_request.location["coordinates"],
                offer.location["coordinates"]
            )
            
            # Apply location-based filtering
            is_within_area = False
            if eating_request.country == "US" and offer.country == "US":
                # US: Check ZIP code area
                is_within_area = self.is_within_us_zip_code_area(
                    eating_request.postal_code, offer.postal_code
                ) or distance_km <= eating_request.max_distance_km
            else:
                # International: Use distance
                is_within_area = distance_km <= eating_request.max_distance_km
            
            if not is_within_area:
                continue
            
            # Calculate compatibility score
            compatibility_score = self.calculate_compatibility_score(eating_request, offer, distance_km)
            
            # Check time compatibility if specified
            time_match = self.check_time_compatibility(eating_request, offer)
            
            # Create match
            match = CookOfferMatch(
                offer_id=offer.id,
                request_id=eating_request.id,
                cook_id=offer.cook_id,
                eater_id=eating_request.eater_id,
                compatibility_score=compatibility_score,
                distance_km=distance_km,
                price_match=offer.price_per_serving <= eating_request.max_price_per_serving,
                dietary_match=self.check_dietary_compatibility(eating_request, offer),
                time_match=time_match,
                category_match=eating_request.category == offer.category if eating_request.category else True,
                match_reasons=self.generate_match_reasons(eating_request, offer, distance_km),
                potential_concerns=self.generate_potential_concerns(eating_request, offer)
            )
            
            matches.append(match)
        
        # Sort by compatibility score (highest first)
        matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return matches[:20]  # Return top 20 matches
    
    def calculate_compatibility_score(self, request: EatingRequest, offer: CookingOffer, distance_km: float) -> float:
        """Calculate compatibility score between request and offer (0.0 to 1.0)"""
        score = 0.0
        factors = 0
        
        # Distance factor (closer is better)
        if distance_km <= 5:
            score += 0.3
        elif distance_km <= 15:
            score += 0.2
        elif distance_km <= 30:
            score += 0.1
        factors += 0.3
        
        # Price factor (lower price gets higher score)
        price_ratio = offer.price_per_serving / request.max_price_per_serving
        if price_ratio <= 0.7:
            score += 0.2
        elif price_ratio <= 0.9:
            score += 0.15
        elif price_ratio <= 1.0:
            score += 0.1
        factors += 0.2
        
        # Category match
        if request.category and request.category == offer.category:
            score += 0.15
        factors += 0.15
        
        # Cuisine match
        if request.desired_cuisine:
            if request.desired_cuisine.lower() in offer.cuisine_type.lower():
                score += 0.15
        factors += 0.15
        
        # Dietary compatibility
        dietary_score = 0
        if "vegetarian" in request.dietary_restrictions and offer.is_vegetarian:
            dietary_score += 0.05
        if "vegan" in request.dietary_restrictions and offer.is_vegan:
            dietary_score += 0.05
        if "gluten_free" in request.dietary_restrictions and offer.is_gluten_free:
            dietary_score += 0.05
        score += dietary_score
        factors += 0.15
        
        # Normalize score
        return min(score / factors, 1.0) if factors > 0 else 0.0
    
    def check_time_compatibility(self, request: EatingRequest, offer: CookingOffer) -> bool:
        """Check if request and offer time preferences are compatible"""
        if not request.preferred_date or not request.preferred_time_start:
            return True  # No specific time preference
        
        # Check if dates match (simplified - could be more flexible)
        request_date = request.preferred_date
        offer_date = offer.cooking_date
        
        if request_date.date() != offer_date.date():
            return False
        
        # Check time overlap
        if request.preferred_time_start and request.preferred_time_end:
            req_start = datetime.strptime(request.preferred_time_start, "%H:%M").time()
            req_end = datetime.strptime(request.preferred_time_end, "%H:%M").time()
            offer_start = datetime.strptime(offer.available_time_start, "%H:%M").time()
            offer_end = datetime.strptime(offer.available_time_end, "%H:%M").time()
            
            # Check for overlap
            return not (req_end <= offer_start or req_start >= offer_end)
        
        return True
    
    def check_dietary_compatibility(self, request: EatingRequest, offer: CookingOffer) -> bool:
        """Check if offer meets dietary requirements"""
        if "vegetarian" in request.dietary_restrictions and not offer.is_vegetarian:
            return False
        if "vegan" in request.dietary_restrictions and not offer.is_vegan:
            return False
        if "gluten_free" in request.dietary_restrictions and not offer.is_gluten_free:
            return False
        if "halal" in request.dietary_restrictions and not offer.is_halal:
            return False
        if "kosher" in request.dietary_restrictions and not offer.is_kosher:
            return False
        
        # Check allergen compatibility
        for allergen in request.allergen_concerns:
            if allergen.lower() in [a.lower() for a in offer.allergen_info]:
                return False
        
        return True
    
    def generate_match_reasons(self, request: EatingRequest, offer: CookingOffer, distance_km: float) -> List[str]:
        """Generate reasons why this is a good match"""
        reasons = []
        
        if distance_km <= 5:
            reasons.append("Very close location (under 5km)")
        elif distance_km <= 15:
            reasons.append("Convenient location")
        
        if offer.price_per_serving <= request.max_price_per_serving * 0.8:
            reasons.append("Great price value")
        
        if request.category and request.category == offer.category:
            reasons.append("Exact category match")
        
        if request.desired_cuisine and request.desired_cuisine.lower() in offer.cuisine_type.lower():
            reasons.append("Cuisine preference match")
        
        if "vegetarian" in request.dietary_restrictions and offer.is_vegetarian:
            reasons.append("Vegetarian-friendly")
        
        if "vegan" in request.dietary_restrictions and offer.is_vegan:
            reasons.append("Vegan-friendly")
        
        if offer.rating and offer.rating >= 4.5:
            reasons.append("Highly rated cook")
        
        return reasons
    
    def generate_potential_concerns(self, request: EatingRequest, offer: CookingOffer) -> List[str]:
        """Generate potential concerns or considerations"""
        concerns = []
        
        if offer.spice_level == "very_hot" and request.spice_tolerance != "hot":
            concerns.append("Very spicy dish - check if suitable")
        
        if offer.allergen_info:
            concerns.append(f"Contains allergens: {', '.join(offer.allergen_info)}")
        
        if not offer.dine_in_available and request.dine_in_preferred:
            concerns.append("Dine-in not available")
        
        if not offer.pickup_available and request.pickup_preferred:
            concerns.append("Pickup not available")
        
        if not offer.delivery_available and request.delivery_preferred:
            concerns.append("Delivery not available")
        
        return concerns

class DailyMarketplaceService:
    """Main service for managing daily marketplace operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.matching_service = LocalMatchingService(db)
    
    async def create_cooking_offer(self, offer_data: Dict[str, Any], cook_id: str) -> CookingOffer:
        """Create a new cooking offer"""
        # Calculate cook payout
        platform_commission = 0.15
        cook_payout = round(offer_data['price_per_serving'] * (1 - platform_commission), 2)
        
        offer = CookingOffer(
            cook_id=cook_id,
            cook_payout_per_serving=cook_payout,
            remaining_servings=offer_data['max_servings'],
            **offer_data
        )
        
        await self.db.cooking_offers.insert_one(offer.dict())
        return offer
    
    async def create_eating_request(self, request_data: Dict[str, Any], eater_id: str) -> EatingRequest:
        """Create a new eating request"""
        request = EatingRequest(eater_id=eater_id, **request_data)
        await self.db.eating_requests.insert_one(request.dict())
        
        # Automatically find matches
        matches = await self.matching_service.find_matching_offers(request)
        
        # Save matches
        if matches:
            for match in matches:
                await self.db.cook_offer_matches.insert_one(match.dict())
            
            # Update request with match IDs
            match_ids = [match.offer_id for match in matches]
            await self.db.eating_requests.update_one(
                {"id": request.id},
                {"$set": {"matched_offers": match_ids, "match_count": len(match_ids)}}
            )
        
        return request
    
    async def book_cooking_offer(self, appointment_data: Dict[str, Any], eater_id: str) -> CookingAppointment:
        """Book a cooking offer directly"""
        offer = await self.db.cooking_offers.find_one({"id": appointment_data["offer_id"]}, {"_id": 0})
        if not offer:
            raise ValueError("Cooking offer not found")
        
        if offer["remaining_servings"] < appointment_data["number_of_servings"]:
            raise ValueError("Not enough servings available")
        
        # Calculate pricing
        total_amount = offer["price_per_serving"] * appointment_data["number_of_servings"]
        platform_commission = total_amount * 0.15
        cook_payout = total_amount - platform_commission
        
        appointment = CookingAppointment(
            cook_id=offer["cook_id"],
            eater_id=eater_id,
            total_amount=total_amount,
            platform_commission_amount=platform_commission,
            cook_payout_amount=cook_payout,
            cook_address=offer.get("address", "Cook's location"),  # Add cook address
            **appointment_data
        )
        
        # Save appointment
        await self.db.cooking_appointments.insert_one(appointment.dict())
        
        # Update offer availability
        new_remaining = offer["remaining_servings"] - appointment_data["number_of_servings"]
        update_data = {"remaining_servings": new_remaining}
        if new_remaining == 0:
            update_data["status"] = CookingOfferStatus.FULLY_BOOKED
        
        await self.db.cooking_offers.update_one(
            {"id": appointment_data["offer_id"]},
            {"$set": update_data, "$inc": {"booking_count": 1}}
        )
        
        return appointment
    
    async def get_local_cooking_offers(self, user_location: Dict[str, Any], postal_code: str, 
                                     country: str = "US", max_distance_km: float = 20.0,
                                     filters: Optional[Dict] = None) -> List[Dict]:
        """Get cooking offers in the local area"""
        query = {
            "status": CookingOfferStatus.ACTIVE,
            "remaining_servings": {"$gt": 0},
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        # Apply filters
        if filters:
            if filters.get("category"):
                query["category"] = filters["category"]
            if filters.get("cuisine_type"):
                query["cuisine_type"] = {"$regex": filters["cuisine_type"], "$options": "i"}
            if filters.get("max_price"):
                query["price_per_serving"] = {"$lte": filters["max_price"]}
            if filters.get("is_vegetarian"):
                query["is_vegetarian"] = True
            if filters.get("is_vegan"):
                query["is_vegan"] = True
            if filters.get("is_gluten_free"):
                query["is_gluten_free"] = True
        
        offers_cursor = self.db.cooking_offers.find(query, {"_id": 0}).sort("created_at", -1).limit(50)
        offers = await offers_cursor.to_list(length=50)
        
        # Filter by location and add distance
        local_offers = []
        for offer in offers:
            if country == "US" and offer["country"] == "US":
                # US ZIP code area matching
                if self.matching_service.is_within_us_zip_code_area(postal_code, offer["postal_code"]):
                    distance = self.matching_service.calculate_distance(
                        user_location["coordinates"], offer["location"]["coordinates"]
                    )
                    if distance <= max_distance_km:
                        offer["distance_km"] = round(distance, 1)
                        local_offers.append(offer)
            else:
                # International distance-based matching
                distance = self.matching_service.calculate_distance(
                    user_location["coordinates"], offer["location"]["coordinates"]
                )
                if distance <= max_distance_km:
                    offer["distance_km"] = round(distance, 1)
                    local_offers.append(offer)
        
        # Sort by distance
        local_offers.sort(key=lambda x: x["distance_km"])
        
        return local_offers
    
    async def get_local_eating_requests(self, user_location: Dict[str, Any], postal_code: str,
                                      country: str = "US", max_distance_km: float = 20.0) -> List[Dict]:
        """Get eating requests in the local area for cooks to see"""
        query = {
            "status": EatingRequestStatus.ACTIVE,
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        requests_cursor = self.db.eating_requests.find(query, {"_id": 0}).sort("created_at", -1).limit(50)
        requests = await requests_cursor.to_list(length=50)
        
        # Filter by location and add distance
        local_requests = []
        for request in requests:
            if country == "US" and request["country"] == "US":
                # US ZIP code area matching
                if self.matching_service.is_within_us_zip_code_area(postal_code, request["postal_code"]):
                    distance = self.matching_service.calculate_distance(
                        user_location["coordinates"], request["location"]["coordinates"]
                    )
                    if distance <= max_distance_km:
                        request["distance_km"] = round(distance, 1)
                        local_requests.append(request)
            else:
                # International distance-based matching
                distance = self.matching_service.calculate_distance(
                    user_location["coordinates"], request["location"]["coordinates"]
                )
                if distance <= max_distance_km:
                    request["distance_km"] = round(distance, 1)
                    local_requests.append(request)
        
        # Sort by distance
        local_requests.sort(key=lambda x: x["distance_km"])
        
        return local_requests
    
    async def cleanup_expired_items(self):
        """Clean up expired offers and requests"""
        now = datetime.utcnow()
        
        # Mark expired offers
        await self.db.cooking_offers.update_many(
            {"expires_at": {"$lt": now}, "status": CookingOfferStatus.ACTIVE},
            {"$set": {"status": CookingOfferStatus.EXPIRED}}
        )
        
        # Mark expired requests
        await self.db.eating_requests.update_many(
            {"expires_at": {"$lt": now}, "status": EatingRequestStatus.ACTIVE},
            {"$set": {"status": EatingRequestStatus.EXPIRED}}
        )
        
        logging.info("Cleaned up expired cooking offers and eating requests")
    
    async def get_user_cooking_offers(self, cook_id: str) -> List[Dict]:
        """Get all cooking offers for a specific cook"""
        offers_cursor = self.db.cooking_offers.find({"cook_id": cook_id}, {"_id": 0}).sort("created_at", -1)
        return await offers_cursor.to_list(length=100)
    
    async def get_user_eating_requests(self, eater_id: str) -> List[Dict]:
        """Get all eating requests for a specific eater"""
        requests_cursor = self.db.eating_requests.find({"eater_id": eater_id}, {"_id": 0}).sort("created_at", -1)
        return await requests_cursor.to_list(length=100)
    
    async def get_user_appointments(self, user_id: str) -> List[Dict]:
        """Get all appointments for a user (as cook or eater)"""
        appointments_cursor = self.db.cooking_appointments.find({
            "$or": [{"cook_id": user_id}, {"eater_id": user_id}]
        }, {"_id": 0}).sort("scheduled_date", -1)
        return await appointments_cursor.to_list(length=100)