# Local Farm Ecosystem Service - Phase 4: Community Rooting
import math
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from farm_ecosystem_models import (
    FarmProfile, FarmProduct, FarmProductOrder, FarmDiningVenue, FarmDiningBooking,
    FarmVendorApplication, ProductCategory, CertificationType, FarmVendorType,
    ProductAvailability
)

class LocalFarmMatchingService:
    """Service for matching local farms with cooks and diners based on location and needs"""
    
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
        """Check if two US ZIP codes are in the same general area"""
        if len(zip1) >= 3 and len(zip2) >= 3:
            return zip1[:3] == zip2[:3]
        return zip1 == zip2
    
    async def find_local_farms(self, user_location: Dict[str, Any], postal_code: str, 
                              country: str = "US", max_distance_km: float = 50.0,
                              filters: Optional[Dict] = None) -> List[Dict]:
        """Find local farms based on location and filters"""
        
        query = {
            "is_active": True,
            "is_accepting_orders": True
        }
        
        # Apply filters
        if filters:
            if filters.get('vendor_type'):
                query['vendor_type'] = filters['vendor_type']
            if filters.get('certifications'):
                query['certifications'] = {"$in": filters['certifications']}
            if filters.get('farming_methods'):
                query['farming_methods'] = {"$in": filters['farming_methods']}
            if filters.get('has_farm_dining'):
                query['offers_farm_dining'] = True
        
        farms_cursor = self.db.farm_profiles.find(query, {"_id": 0}).limit(50)
        farms = await farms_cursor.to_list(length=50)
        
        # Filter by location and add distance
        local_farms = []
        for farm in farms:
            if country == "US" and farm["country"] == "US":
                # US ZIP code area matching for farms
                if self.is_within_us_zip_code_area(postal_code, farm["postal_code"]):
                    distance = self.calculate_distance(
                        user_location["coordinates"], farm["location"]["coordinates"]
                    )
                    if distance <= max_distance_km:
                        farm["distance_km"] = round(distance, 1)
                        local_farms.append(farm)
            else:
                # International distance-based matching
                distance = self.calculate_distance(
                    user_location["coordinates"], farm["location"]["coordinates"]
                )
                if distance <= max_distance_km:
                    farm["distance_km"] = round(distance, 1)
                    local_farms.append(farm)
        
        # Sort by distance
        local_farms.sort(key=lambda x: x["distance_km"])
        
        return local_farms
    
    async def find_seasonal_products(self, user_location: Dict[str, Any], postal_code: str,
                                   season: str = None, product_categories: List[str] = None,
                                   max_distance_km: float = 50.0) -> List[Dict]:
        """Find seasonal products from local farms"""
        
        if not season:
            # Determine current season based on month
            current_month = datetime.utcnow().strftime('%B')
            season_map = {
                'December': 'winter', 'January': 'winter', 'February': 'winter',
                'March': 'spring', 'April': 'spring', 'May': 'spring',
                'June': 'summer', 'July': 'summer', 'August': 'summer',
                'September': 'fall', 'October': 'fall', 'November': 'fall'
            }
            season = season_map.get(current_month, 'summer')
        
        # Build product query
        query = {
            "is_active": True,
            "is_available": True,
            "$or": [
                {"availability_type": "year_round"},
                {"seasonal_months": {"$in": [datetime.utcnow().strftime('%B')]}}
            ]
        }
        
        if product_categories:
            query["category"] = {"$in": product_categories}
        
        products_cursor = self.db.farm_products.find(query, {"_id": 0}).limit(100)
        products = await products_cursor.to_list(length=100)
        
        # Get farm info and filter by location
        local_products = []
        for product in products:
            farm = await self.db.farm_profiles.find_one({"id": product["farm_id"]}, {"_id": 0})
            if farm and farm.get("is_active"):
                distance = self.calculate_distance(
                    user_location["coordinates"], farm["location"]["coordinates"]
                )
                if distance <= max_distance_km:
                    product["farm_name"] = farm["farm_name"]
                    product["farm_certifications"] = farm.get("certifications", [])
                    product["distance_km"] = round(distance, 1)
                    local_products.append(product)
        
        # Sort by distance and seasonality
        local_products.sort(key=lambda x: (x["distance_km"], x.get("seasonal_months") and datetime.utcnow().strftime('%B') not in x["seasonal_months"]))
        
        return local_products
    
    async def match_ingredients_to_recipes(self, recipe_ingredients: List[str], 
                                         user_location: Dict[str, Any], postal_code: str,
                                         max_distance_km: float = 30.0) -> Dict[str, List[Dict]]:
        """Match recipe ingredients to local farm products"""
        
        ingredient_matches = {}
        
        for ingredient in recipe_ingredients:
            # Search for products that match the ingredient
            query = {
                "$or": [
                    {"product_name": {"$regex": ingredient, "$options": "i"}},
                    {"variety": {"$regex": ingredient, "$options": "i"}},
                    {"description": {"$regex": ingredient, "$options": "i"}}
                ],
                "is_active": True,
                "is_available": True
            }
            
            products_cursor = self.db.farm_products.find(query, {"_id": 0}).limit(10)
            products = await products_cursor.to_list(length=10)
            
            local_matches = []
            for product in products:
                farm = await self.db.farm_profiles.find_one({"id": product["farm_id"]}, {"_id": 0})
                if farm:
                    distance = self.calculate_distance(
                        user_location["coordinates"], farm["location"]["coordinates"]
                    )
                    if distance <= max_distance_km:
                        product["farm_name"] = farm["farm_name"]
                        product["distance_km"] = round(distance, 1)
                        local_matches.append(product)
            
            if local_matches:
                local_matches.sort(key=lambda x: x["distance_km"])
                ingredient_matches[ingredient] = local_matches
        
        return ingredient_matches

class FarmEcosystemService:
    """Main service for managing farm ecosystem operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.matching_service = LocalFarmMatchingService(db)
    
    async def create_farm_vendor_application(self, application_data: Dict[str, Any], user_id: str) -> FarmVendorApplication:
        """Create a new farm vendor application"""
        
        application = FarmVendorApplication(
            user_id=user_id,
            **application_data
        )
        
        await self.db.farm_vendor_applications.insert_one(application.dict())
        return application
    
    async def approve_farm_vendor(self, application_id: str, reviewer_id: str) -> FarmProfile:
        """Approve farm vendor application and create profile"""
        
        application = await self.db.farm_vendor_applications.find_one({"id": application_id}, {"_id": 0})
        if not application:
            raise ValueError("Farm vendor application not found")
        
        # Create farm profile from approved application
        farm_profile = FarmProfile(
            vendor_id=application["user_id"],
            application_id=application_id,
            farm_name=application["farm_name"],
            business_name=application["business_name"],
            description=application["farm_description"],
            established_year=application["established_year"],
            vendor_type=FarmVendorType(application["vendor_type"]),
            address=application["farm_address"],
            city=application["city"],
            state=application["state"],
            postal_code=application["postal_code"],
            phone_number=application["phone_number"],
            total_acres=application["total_acres"],
            farming_methods=application["farming_methods"],
            certifications=application["certifications"],
            distribution_radius_km=application["distribution_radius_km"],
            location={
                "type": "Point",
                "coordinates": [-73.935242, 40.730610]  # Default coordinates (would use geocoding)
            }
        )
        
        await self.db.farm_profiles.insert_one(farm_profile.dict())
        
        # Update application status
        await self.db.farm_vendor_applications.update_one(
            {"id": application_id},
            {
                "$set": {
                    "status": "approved",
                    "reviewer_id": reviewer_id,
                    "approval_date": datetime.utcnow()
                }
            }
        )
        
        # Update user as farm vendor
        await self.db.users.update_one(
            {"id": application["user_id"]},
            {"$set": {"is_farm_vendor": True, "vendor_type": "farm"}}
        )
        
        return farm_profile
    
    async def create_farm_product(self, product_data: Dict[str, Any], vendor_id: str) -> FarmProduct:
        """Create a new farm product listing"""
        
        # Get farm profile
        farm = await self.db.farm_profiles.find_one({"vendor_id": vendor_id}, {"_id": 0})
        if not farm:
            raise ValueError("Farm profile not found for this vendor")
        
        product = FarmProduct(
            farm_id=farm["id"],
            vendor_id=vendor_id,
            **product_data
        )
        
        await self.db.farm_products.insert_one(product.dict())
        
        # Update farm's product catalog
        await self.db.farm_profiles.update_one(
            {"id": farm["id"]},
            {
                "$push": {
                    "product_catalog": {
                        "product_id": product.id,
                        "name": product.product_name,
                        "category": product.category,
                        "price_per_unit": product.price_per_unit,
                        "availability": product.availability_type
                    }
                }
            }
        )
        
        return product
    
    async def create_farm_dining_venue(self, venue_data: Dict[str, Any], vendor_id: str) -> FarmDiningVenue:
        """Create a farm dining venue"""
        
        # Verify farm vendor has dining approved
        farm = await self.db.farm_profiles.find_one({"vendor_id": vendor_id}, {"_id": 0})
        if not farm:
            raise ValueError("Farm profile not found")
        
        application = await self.db.farm_vendor_applications.find_one({"user_id": vendor_id}, {"_id": 0})
        if not application or not application.get("offers_farm_dining"):
            raise ValueError("Farm is not approved for dining services")
        
        venue = FarmDiningVenue(
            farm_id=farm["id"],
            vendor_id=vendor_id,
            **venue_data
        )
        
        await self.db.farm_dining_venues.insert_one(venue.dict())
        return venue
    
    async def order_farm_products(self, order_data: Dict[str, Any], customer_id: str) -> FarmProductOrder:
        """Create order for farm products"""
        
        farm = await self.db.farm_profiles.find_one({"id": order_data["farm_id"]}, {"_id": 0})
        if not farm:
            raise ValueError("Farm not found")
        
        # Calculate pricing
        subtotal = sum(item["total_price"] for item in order_data["items"])
        platform_commission = subtotal * 0.15  # 15% commission for farm products
        delivery_fee = order_data.get("delivery_fee", 0.0)
        total_amount = subtotal + delivery_fee
        farmer_payout = subtotal - platform_commission
        
        order = FarmProductOrder(
            customer_id=customer_id,
            farm_id=order_data["farm_id"],
            vendor_id=farm["vendor_id"],
            items=order_data["items"],
            subtotal=subtotal,
            platform_commission=platform_commission,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            farmer_payout=farmer_payout,
            delivery_method=order_data.get("delivery_method", "pickup"),
            delivery_address=order_data.get("delivery_address"),
            preferred_delivery_date=datetime.fromisoformat(order_data["preferred_delivery_date"].replace('Z', '+00:00')),
            delivery_time_window=order_data.get("delivery_time_window"),
            customer_notes=order_data.get("customer_notes", "")
        )
        
        await self.db.farm_product_orders.insert_one(order.dict())
        
        # Update product quantities (if tracked)
        for item in order_data["items"]:
            await self.db.farm_products.update_one(
                {"id": item["product_id"], "quantity_available": {"$gte": item["quantity"]}},
                {"$inc": {"quantity_available": -item["quantity"], "total_orders": 1}}
            )
        
        return order
    
    async def book_farm_dining(self, booking_data: Dict[str, Any], customer_id: str) -> FarmDiningBooking:
        """Book farm dining experience"""
        
        venue = await self.db.farm_dining_venues.find_one({"id": booking_data["venue_id"]}, {"_id": 0})
        if not venue:
            raise ValueError("Farm dining venue not found")
        
        farm = await self.db.farm_profiles.find_one({"id": venue["farm_id"]}, {"_id": 0})
        if not farm:
            raise ValueError("Farm not found")
        
        # Calculate pricing
        price_per_person = venue.get("base_price_per_person", 50.0)
        farm_tour_fee = 15.0 if booking_data.get("includes_farm_tour") else 0.0
        subtotal = (price_per_person * booking_data["number_of_guests"]) + farm_tour_fee
        platform_commission = subtotal * 0.15  # 15% commission for dining experiences
        farmer_payout = subtotal - platform_commission
        
        booking = FarmDiningBooking(
            venue_id=booking_data["venue_id"],
            farm_id=venue["farm_id"],
            customer_id=customer_id,
            vendor_id=venue["vendor_id"],
            dining_date=datetime.fromisoformat(booking_data["dining_date"].replace('Z', '+00:00')),
            number_of_guests=booking_data["number_of_guests"],
            includes_farm_tour=booking_data.get("includes_farm_tour", False),
            special_dietary_requests=booking_data.get("special_dietary_requests", []),
            occasion=booking_data.get("occasion"),
            price_per_person=price_per_person,
            farm_tour_fee=farm_tour_fee,
            total_amount=subtotal,
            platform_commission=platform_commission,
            farmer_payout=farmer_payout,
            customer_notes=booking_data.get("customer_notes", ""),
            contact_phone=booking_data.get("contact_phone", "")
        )
        
        await self.db.farm_dining_bookings.insert_one(booking.dict())
        return booking
    
    async def get_local_farms(self, user_location: Dict[str, Any], postal_code: str, 
                            country: str = "US", max_distance_km: float = 50.0,
                            filters: Optional[Dict] = None) -> List[Dict]:
        """Get local farms with enhanced information"""
        
        farms = await self.matching_service.find_local_farms(
            user_location, postal_code, country, max_distance_km, filters
        )
        
        # Enrich with additional information
        enriched_farms = []
        for farm in farms:
            # Get product count
            product_count = await self.db.farm_products.count_documents({
                "farm_id": farm["id"],
                "is_active": True
            })
            
            # Get dining venues count
            dining_venues = await self.db.farm_dining_venues.count_documents({
                "farm_id": farm["id"],
                "is_active": True
            })
            
            farm["product_count"] = product_count
            farm["dining_venues_count"] = dining_venues
            farm["offers_farm_dining"] = dining_venues > 0
            
            enriched_farms.append(farm)
        
        return enriched_farms
    
    async def get_seasonal_harvest_calendar(self, user_location: Dict[str, Any], postal_code: str,
                                          max_distance_km: float = 50.0) -> Dict[str, List[Dict]]:
        """Get seasonal harvest calendar from local farms"""
        
        farms = await self.matching_service.find_local_farms(
            user_location, postal_code, "US", max_distance_km
        )
        
        seasonal_calendar = {
            "spring": [],
            "summer": [],
            "fall": [],
            "winter": []
        }
        
        for farm in farms:
            products_cursor = self.db.farm_products.find({
                "farm_id": farm["id"],
                "is_active": True,
                "availability_type": {"$in": ["seasonal", "limited_harvest"]}
            }, {"_id": 0})
            
            products = await products_cursor.to_list(length=100)
            
            for product in products:
                for month in product.get("seasonal_months", []):
                    season = self._month_to_season(month)
                    seasonal_calendar[season].append({
                        "farm_name": farm["farm_name"],
                        "product_name": product["product_name"],
                        "category": product["category"],
                        "price_per_unit": product["price_per_unit"],
                        "unit_type": product["unit_type"],
                        "certifications": product.get("certifications", []),
                        "distance_km": farm["distance_km"],
                        "harvest_month": month
                    })
        
        return seasonal_calendar
    
    def _month_to_season(self, month: str) -> str:
        """Convert month name to season"""
        season_map = {
            'December': 'winter', 'January': 'winter', 'February': 'winter',
            'March': 'spring', 'April': 'spring', 'May': 'spring',
            'June': 'summer', 'July': 'summer', 'August': 'summer',
            'September': 'fall', 'October': 'fall', 'November': 'fall'
        }
        return season_map.get(month, 'summer')
    
    async def get_recipe_ingredient_sourcing(self, recipe_ingredients: List[str], 
                                           user_location: Dict[str, Any], postal_code: str,
                                           max_distance_km: float = 30.0) -> Dict[str, Any]:
        """Get local sourcing options for recipe ingredients"""
        
        ingredient_matches = await self.matching_service.match_ingredients_to_recipes(
            recipe_ingredients, user_location, postal_code, max_distance_km
        )
        
        # Calculate sourcing statistics
        total_ingredients = len(recipe_ingredients)
        locally_available = len(ingredient_matches)
        local_sourcing_percentage = (locally_available / total_ingredients) * 100 if total_ingredients > 0 else 0
        
        # Find farms that have multiple ingredients
        farm_ingredient_counts = {}
        for ingredient, matches in ingredient_matches.items():
            for match in matches:
                farm_name = match["farm_name"]
                if farm_name not in farm_ingredient_counts:
                    farm_ingredient_counts[farm_name] = []
                farm_ingredient_counts[farm_name].append(ingredient)
        
        # Recommend farms with most ingredients
        recommended_farms = sorted(
            farm_ingredient_counts.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:3]
        
        return {
            "total_ingredients": total_ingredients,
            "locally_sourced_count": locally_available,
            "local_sourcing_percentage": round(local_sourcing_percentage, 1),
            "ingredient_matches": ingredient_matches,
            "recommended_farms": [
                {
                    "farm_name": farm_name,
                    "ingredient_count": len(ingredients),
                    "ingredients": ingredients
                }
                for farm_name, ingredients in recommended_farms
            ],
            "sustainability_impact": self._calculate_sustainability_impact(locally_available, total_ingredients)
        }
    
    def _calculate_sustainability_impact(self, local_count: int, total_count: int) -> Dict[str, Any]:
        """Calculate environmental impact of local sourcing"""
        
        local_percentage = (local_count / total_count) * 100 if total_count > 0 else 0
        
        # Simplified calculations for impact
        estimated_miles_saved = local_count * 1500  # Average food miles saved per ingredient
        estimated_co2_reduction = estimated_miles_saved * 0.89  # lbs CO2 per mile for food transport
        
        return {
            "local_sourcing_percentage": round(local_percentage, 1),
            "estimated_food_miles_saved": estimated_miles_saved,
            "estimated_co2_reduction_lbs": round(estimated_co2_reduction, 1),
            "community_economic_impact": f"${local_count * 15:.2f} supporting local farmers",
            "sustainability_score": min(local_percentage / 10, 10)  # Scale to 10
        }
    
    async def get_farm_analytics(self, vendor_id: str) -> Dict[str, Any]:
        """Get analytics for farm vendor"""
        
        farm = await self.db.farm_profiles.find_one({"vendor_id": vendor_id}, {"_id": 0})
        if not farm:
            raise ValueError("Farm profile not found")
        
        # Product analytics
        total_products = await self.db.farm_products.count_documents({"farm_id": farm["id"]})
        active_products = await self.db.farm_products.count_documents({
            "farm_id": farm["id"],
            "is_active": True,
            "is_available": True
        })
        
        # Order analytics (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_orders = await self.db.farm_product_orders.count_documents({
            "farm_id": farm["id"],
            "order_date": {"$gte": thirty_days_ago}
        })
        
        # Revenue analytics
        revenue_pipeline = [
            {
                "$match": {
                    "farm_id": farm["id"],
                    "order_date": {"$gte": thirty_days_ago},
                    "status": {"$in": ["delivered", "completed"]}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$farmer_payout"},
                    "total_orders": {"$sum": 1},
                    "avg_order_value": {"$avg": "$subtotal"}
                }
            }
        ]
        
        revenue_results = await self.db.farm_product_orders.aggregate(revenue_pipeline).to_list(length=1)
        revenue_data = revenue_results[0] if revenue_results else {
            "total_revenue": 0, "total_orders": 0, "avg_order_value": 0
        }
        
        # Dining analytics
        dining_bookings = await self.db.farm_dining_bookings.count_documents({
            "farm_id": farm["id"],
            "booking_date": {"$gte": thirty_days_ago}
        })
        
        return {
            "farm_name": farm["farm_name"],
            "total_acres": farm["total_acres"],
            "products": {
                "total_products": total_products,
                "active_products": active_products,
                "product_categories": len(set(p.get("category") for p in farm.get("product_catalog", [])))
            },
            "orders_last_30_days": recent_orders,
            "revenue_last_30_days": revenue_data["total_revenue"],
            "average_order_value": revenue_data["avg_order_value"],
            "dining_bookings_last_30_days": dining_bookings,
            "customer_rating": farm.get("average_rating", 0),
            "total_reviews": farm.get("total_reviews", 0),
            "certifications": farm.get("certifications", []),
            "sustainability_practices": farm.get("sustainability_practices", [])
        }