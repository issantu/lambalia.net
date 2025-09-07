# Automated Grocery Store Ad Service
import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from geopy.distance import geodesic
from pydantic import BaseModel, Field

class GroceryStoreChain(BaseModel):
    chain_id: str
    name: str
    website: str
    ad_api_endpoint: Optional[str] = None
    affiliate_program: Optional[str] = None
    logo_url: str
    primary_color: str
    categories: List[str] = []
    commission_rate: float = 0.0  # For affiliate programs
    
class GroceryStoreLocation(BaseModel):
    store_id: str
    chain_id: str
    name: str
    address: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    hours: Dict[str, str] = {}
    services: List[str] = []  # pickup, delivery, pharmacy, etc.
    distance_km: Optional[float] = None

class GroceryAd(BaseModel):
    ad_id: str = Field(default_factory=lambda: f"grocery_ad_{int(datetime.now().timestamp())}")
    chain_id: str
    store_location: Optional[GroceryStoreLocation] = None
    ad_type: str  # banner, ingredient_match, weekly_special, new_store
    title: str
    description: str
    image_url: str
    cta_text: str  # Call to action
    cta_url: str
    ingredients_keywords: List[str] = []  # For ingredient matching
    weekly_deals: List[Dict[str, Any]] = []
    target_postal_codes: List[str] = []
    target_radius_km: float = 25.0
    priority: int = 1  # Higher = more likely to show
    active: bool = True
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    impression_count: int = 0
    click_count: int = 0
    estimated_ctr: float = 0.02  # Click-through rate
    revenue_per_click: float = 0.50  # Estimated revenue per click

class GroceryAdService:
    """Service for managing automated grocery store advertisements"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.grocery_chains = self._initialize_grocery_chains()
        
    def _initialize_grocery_chains(self) -> Dict[str, GroceryStoreChain]:
        """Initialize major grocery store chains database"""
        chains = {
            "walmart": GroceryStoreChain(
                chain_id="walmart",
                name="Walmart",
                website="https://www.walmart.com",
                affiliate_program="walmart_affiliate",
                logo_url="https://logos-world.net/wp-content/uploads/2020/09/Walmart-Logo.png",
                primary_color="#0071ce",
                categories=["grocery", "organic", "international", "bulk"],
                commission_rate=0.04
            ),
            "kroger": GroceryStoreChain(
                chain_id="kroger",
                name="Kroger",
                website="https://www.kroger.com",
                affiliate_program="kroger_affiliate",
                logo_url="https://logos-world.net/wp-content/uploads/2021/08/Kroger-Logo.png",
                primary_color="#004c91",
                categories=["grocery", "organic", "pharmacy", "fuel"],
                commission_rate=0.03
            ),
            "costco": GroceryStoreChain(
                chain_id="costco",
                name="Costco",
                website="https://www.costco.com",
                logo_url="https://logos-world.net/wp-content/uploads/2020/09/Costco-Logo.png",
                primary_color="#e31837",
                categories=["bulk", "organic", "international", "premium"],
                commission_rate=0.02
            ),
            "target": GroceryStoreChain(
                chain_id="target",
                name="Target",
                website="https://www.target.com",
                affiliate_program="target_affiliate",
                logo_url="https://logos-world.net/wp-content/uploads/2020/04/Target-Logo.png",
                primary_color="#cc0000",
                categories=["grocery", "organic", "pantry"],
                commission_rate=0.05
            ),
            "hmart": GroceryStoreChain(
                chain_id="hmart",
                name="H Mart",
                website="https://www.hmart.com",
                logo_url="https://www.hmart.com/images/hmart_logo.png",
                primary_color="#ff6b35",
                categories=["asian", "korean", "international", "specialty"],
                commission_rate=0.06
            ),
            "meijer": GroceryStoreChain(
                chain_id="meijer",
                name="Meijer",
                website="https://www.meijer.com",
                logo_url="https://logos-world.net/wp-content/uploads/2021/03/Meijer-Logo.png",
                primary_color="#ff6900",
                categories=["grocery", "organic", "pharmacy", "general"],
                commission_rate=0.035
            ),
            "schnucks": GroceryStoreChain(
                chain_id="schnucks",
                name="Schnucks",
                website="https://www.schnucks.com",
                logo_url="https://www.schnucks.com/images/schnucks-logo.png",
                primary_color="#006633",
                categories=["grocery", "local", "pharmacy"],
                commission_rate=0.04
            ),
            "save_a_lot": GroceryStoreChain(
                chain_id="save_a_lot",
                name="Save-A-Lot",
                website="https://www.save-a-lot.com",
                logo_url="https://www.save-a-lot.com/images/logo.png",
                primary_color="#ed1c24",
                categories=["discount", "grocery", "budget"],
                commission_rate=0.05
            ),
            "sams_club": GroceryStoreChain(
                chain_id="sams_club",
                name="Sam's Club",
                website="https://www.samsclub.com",
                affiliate_program="sams_affiliate",
                logo_url="https://logos-world.net/wp-content/uploads/2020/09/Sams-Club-Logo.png",
                primary_color="#004c91",
                categories=["bulk", "membership", "business"],
                commission_rate=0.025
            )
        }
        return chains
    
    async def initialize_grocery_store_locations(self):
        """Initialize grocery store locations database - mock data for now"""
        locations = []
        
        # Major cities and their grocery stores (sample data)
        cities_data = [
            {"city": "New York", "state": "NY", "postal_codes": ["10001", "10002", "10003"], "lat": 40.7128, "lng": -74.0060},
            {"city": "Los Angeles", "state": "CA", "postal_codes": ["90210", "90211", "90212"], "lat": 34.0522, "lng": -118.2437},
            {"city": "Chicago", "state": "IL", "postal_codes": ["60601", "60602", "60603"], "lat": 41.8781, "lng": -87.6298},
            {"city": "Houston", "state": "TX", "postal_codes": ["77001", "77002", "77003"], "lat": 29.7604, "lng": -95.3698},
            {"city": "Phoenix", "state": "AZ", "postal_codes": ["85001", "85002", "85003"], "lat": 33.4484, "lng": -112.0740},
            {"city": "Philadelphia", "state": "PA", "postal_codes": ["19101", "19102", "19103"], "lat": 39.9526, "lng": -75.1652},
            {"city": "San Antonio", "state": "TX", "postal_codes": ["78201", "78202", "78203"], "lat": 29.4241, "lng": -98.4936},
            {"city": "San Diego", "state": "CA", "postal_codes": ["92101", "92102", "92103"], "lat": 32.7157, "lng": -117.1611},
            {"city": "Dallas", "state": "TX", "postal_codes": ["75201", "75202", "75203"], "lat": 32.7767, "lng": -96.7970},
            {"city": "San Jose", "state": "CA", "postal_codes": ["95101", "95102", "95103"], "lat": 37.3382, "lng": -121.8863}
        ]
        
        store_counter = 1
        for city_data in cities_data:
            for postal_code in city_data["postal_codes"]:
                for chain_id, chain in self.grocery_chains.items():
                    # Create 1-3 stores per chain per postal area
                    num_stores = random.randint(1, 3)
                    for i in range(num_stores):
                        location = GroceryStoreLocation(
                            store_id=f"{chain_id}_{store_counter}",
                            chain_id=chain_id,
                            name=f"{chain.name} #{store_counter}",
                            address=f"{random.randint(100, 9999)} Main St",
                            city=city_data["city"],
                            state=city_data["state"],
                            postal_code=postal_code,
                            latitude=city_data["lat"] + random.uniform(-0.1, 0.1),
                            longitude=city_data["lng"] + random.uniform(-0.1, 0.1),
                            phone=f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                            hours={
                                "monday": "6:00 AM - 11:00 PM",
                                "tuesday": "6:00 AM - 11:00 PM", 
                                "wednesday": "6:00 AM - 11:00 PM",
                                "thursday": "6:00 AM - 11:00 PM",
                                "friday": "6:00 AM - 11:00 PM",
                                "saturday": "6:00 AM - 11:00 PM",
                                "sunday": "7:00 AM - 10:00 PM"
                            },
                            services=["grocery", "pharmacy", "pickup", "delivery"] if chain_id in ["walmart", "kroger", "target"] else ["grocery", "pickup"]
                        )
                        locations.append(location)
                        store_counter += 1
        
        # Store in database
        await self.db.grocery_store_locations.drop()  # Reset for fresh data
        await self.db.grocery_store_locations.insert_many([loc.dict() for loc in locations])
        
        return locations
    
    async def get_nearby_stores(self, postal_code: str, radius_km: float = 25.0) -> List[GroceryStoreLocation]:
        """Get nearby grocery stores by postal code"""
        # For demo, we'll use approximate lat/lng for postal codes
        # In production, use a postal code to lat/lng service
        
        # Mock postal code to coordinates mapping
        postal_coords = {
            "10001": (40.7589, -73.9851), "10002": (40.7589, -73.9851), "10003": (40.7589, -73.9851),
            "90210": (34.0901, -118.4065), "90211": (34.0901, -118.4065), "90212": (34.0901, -118.4065),
            "60601": (41.8825, -87.6441), "60602": (41.8825, -87.6441), "60603": (41.8825, -87.6441),
            "77001": (29.7499, -95.3827), "77002": (29.7499, -95.3827), "77003": (29.7499, -95.3827),
        }
        
        user_coords = postal_coords.get(postal_code)
        if not user_coords:
            user_coords = (40.7589, -73.9851)  # Default to NYC
        
        # Get all stores from database
        stores_cursor = self.db.grocery_store_locations.find({})
        stores_data = await stores_cursor.to_list(length=None)
        
        nearby_stores = []
        for store_data in stores_data:
            store_coords = (store_data["latitude"], store_data["longitude"])
            distance = geodesic(user_coords, store_coords).kilometers
            
            if distance <= radius_km:
                store = GroceryStoreLocation(**store_data)
                store.distance_km = round(distance, 2)
                nearby_stores.append(store)
        
        # Sort by distance
        nearby_stores.sort(key=lambda x: x.distance_km)
        return nearby_stores[:15]  # Return top 15 nearest stores
    
    async def generate_contextual_grocery_ads(self, user_postal_code: str, recipe_ingredients: List[str] = None, placement: str = "banner") -> List[GroceryAd]:
        """Generate contextual grocery store ads based on user location and recipe ingredients"""
        
        # Get nearby stores
        nearby_stores = await self.get_nearby_stores(user_postal_code)
        
        ads = []
        chains_used = set()
        
        # Create ads for nearby stores
        for store in nearby_stores[:5]:  # Top 5 nearest stores
            if store.chain_id in chains_used:
                continue  # Avoid duplicate chain ads
                
            chain = self.grocery_chains[store.chain_id]
            chains_used.add(store.chain_id)
            
            # Generate contextual ad content
            if recipe_ingredients:
                ad = self._create_ingredient_based_ad(chain, store, recipe_ingredients, placement)
            else:
                ad = self._create_general_store_ad(chain, store, placement)
            
            ads.append(ad)
        
        # Add special deals and promotions
        special_ads = await self._generate_weekly_specials(user_postal_code, placement)
        ads.extend(special_ads[:2])  # Add top 2 special deals
        
        # Sort by priority and estimated revenue
        ads.sort(key=lambda x: (x.priority, x.revenue_per_click), reverse=True)
        
        return ads[:3]  # Return top 3 ads
    
    def _create_ingredient_based_ad(self, chain: GroceryStoreChain, store: GroceryStoreLocation, ingredients: List[str], placement: str) -> GroceryAd:
        """Create ad based on recipe ingredients"""
        
        # Match ingredients to store specialties
        matched_categories = []
        specialty_ingredients = []
        
        ingredient_keywords = [ing.lower() for ing in ingredients]
        
        # Check for specialty ingredients
        asian_ingredients = ["soy sauce", "sesame oil", "rice vinegar", "miso", "kimchi", "gochujang", "curry", "coconut milk"]
        if any(keyword in " ".join(ingredient_keywords) for keyword in asian_ingredients) and chain.chain_id == "hmart":
            specialty_ingredients = [ing for ing in ingredients if any(ai in ing.lower() for ai in asian_ingredients)]
            
        # Generate ad content
        if specialty_ingredients and chain.chain_id == "hmart":
            title = f"Find Authentic Asian Ingredients at {chain.name}"
            description = f"Get {', '.join(specialty_ingredients[:3])} and more authentic ingredients. Only {store.distance_km}km away!"
            cta_text = "Shop Asian Ingredients"
        elif "organic" in chain.categories:
            title = f"Fresh Organic Ingredients at {chain.name}"
            description = f"Quality ingredients for your recipe. Store pickup or delivery available. {store.distance_km}km away"
            cta_text = "Shop Organic"
        else:
            title = f"Get Recipe Ingredients at {chain.name}"
            description = f"Everything you need for cooking. Convenient location {store.distance_km}km from you!"
            cta_text = "Shop Now"
        
        return GroceryAd(
            chain_id=chain.chain_id,
            store_location=store,
            ad_type="ingredient_match",
            title=title,
            description=description,
            image_url=chain.logo_url,
            cta_text=cta_text,
            cta_url=f"{chain.website}/store-locator?zip={store.postal_code}",
            ingredients_keywords=ingredient_keywords,
            target_postal_codes=[store.postal_code],
            target_radius_km=25.0,
            priority=3,  # High priority for ingredient matching
            revenue_per_click=0.75  # Higher revenue for targeted ads
        )
    
    def _create_general_store_ad(self, chain: GroceryStoreChain, store: GroceryStoreLocation, placement: str) -> GroceryAd:
        """Create general store advertisement"""
        
        ad_templates = [
            {
                "title": f"Fresh Groceries at {chain.name}",
                "description": f"Quality ingredients for all your cooking needs. Visit us {store.distance_km}km away!",
                "cta_text": "Visit Store"
            },
            {
                "title": f"Weekly Savings at {chain.name}",
                "description": f"Great deals on fresh produce and pantry essentials. Store #{store.store_id[-3:]}",
                "cta_text": "View Deals" 
            },
            {
                "title": f"Convenient Shopping at {chain.name}",
                "description": f"Pickup and delivery available. Open 6 AM - 11 PM daily. {store.distance_km}km from you",
                "cta_text": "Shop Online"
            }
        ]
        
        template = random.choice(ad_templates)
        
        return GroceryAd(
            chain_id=chain.chain_id,
            store_location=store,
            ad_type="general_store",
            title=template["title"],
            description=template["description"],
            image_url=chain.logo_url,
            cta_text=template["cta_text"],
            cta_url=f"{chain.website}/stores/{store.store_id}",
            target_postal_codes=[store.postal_code],
            priority=2,
            revenue_per_click=0.50
        )
    
    async def _generate_weekly_specials(self, postal_code: str, placement: str) -> List[GroceryAd]:
        """Generate weekly special deals ads"""
        
        specials = [
            {
                "chain_id": "walmart",
                "title": "Weekly Grocery Specials at Walmart",
                "description": "Save on fresh produce, pantry staples, and international foods. This week only!",
                "deals": ["Fresh Bananas $0.58/lb", "Ground Beef $3.99/lb", "Organic Milk $3.49"],
                "cta_text": "View Weekly Ad"
            },
            {
                "chain_id": "kroger", 
                "title": "Kroger Digital Coupons Available",
                "description": "Clip digital coupons and save on your favorite brands. Free Kroger Plus membership!",
                "deals": ["Digital Coupons", "$5 off $50", "Fuel Points Rewards"],
                "cta_text": "Get Coupons"
            },
            {
                "chain_id": "target",
                "title": "Target Circle Weekly Deals",
                "description": "Exclusive deals for Target Circle members. Join free and start saving today!",
                "deals": ["Buy 2 Get 1 Free", "Extra 10% off", "Free Same-Day Delivery"],
                "cta_text": "Join Circle"
            }
        ]
        
        ads = []
        for special in specials[:2]:  # Limit to 2 specials
            chain = self.grocery_chains[special["chain_id"]]
            
            ad = GroceryAd(
                chain_id=special["chain_id"],
                ad_type="weekly_special",
                title=special["title"],
                description=special["description"],
                image_url=chain.logo_url,
                cta_text=special["cta_text"],
                cta_url=f"{chain.website}/weekly-ad",
                weekly_deals=[{"description": deal} for deal in special["deals"]],
                target_postal_codes=[postal_code],
                priority=2,
                revenue_per_click=0.60
            )
            ads.append(ad)
        
        return ads
    
    async def track_ad_impression(self, ad_id: str, user_id: str, placement: str):
        """Track ad impression for analytics"""
        impression = {
            "ad_id": ad_id,
            "user_id": user_id,
            "placement": placement,
            "timestamp": datetime.utcnow(),
            "action": "impression"
        }
        
        await self.db.grocery_ad_impressions.insert_one(impression)
        
        # Update ad impression count
        await self.db.grocery_ads.update_one(
            {"ad_id": ad_id},
            {"$inc": {"impression_count": 1}}
        )
    
    async def track_ad_click(self, ad_id: str, user_id: str, placement: str):
        """Track ad click for analytics and revenue"""
        click = {
            "ad_id": ad_id,
            "user_id": user_id,
            "placement": placement,
            "timestamp": datetime.utcnow(),
            "action": "click"
        }
        
        await self.db.grocery_ad_clicks.insert_one(click)
        
        # Update ad click count
        await self.db.grocery_ads.update_one(
            {"ad_id": ad_id},
            {"$inc": {"click_count": 1}}
        )
    
    async def get_ad_performance_metrics(self, chain_id: str = None, days: int = 30) -> Dict[str, Any]:
        """Get ad performance metrics for revenue tracking"""
        
        date_filter = {"timestamp": {"$gte": datetime.utcnow() - timedelta(days=days)}}
        
        # Get impressions and clicks
        impressions = await self.db.grocery_ad_impressions.count_documents(date_filter)
        clicks = await self.db.grocery_ad_clicks.count_documents(date_filter)
        
        # Calculate metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        estimated_revenue = clicks * 0.55  # Average revenue per click
        
        # Get top performing ads
        pipeline = [
            {"$match": date_filter},
            {"$group": {
                "_id": "$ad_id",
                "impressions": {"$sum": 1},
                "clicks": {"$sum": {"$cond": [{"$eq": ["$action", "click"]}, 1, 0]}}
            }},
            {"$sort": {"clicks": -1}},
            {"$limit": 10}
        ]
        
        top_ads = await self.db.grocery_ad_impressions.aggregate(pipeline).to_list(length=10)
        
        return {
            "total_impressions": impressions,
            "total_clicks": clicks,
            "ctr_percentage": round(ctr, 2),
            "estimated_revenue": round(estimated_revenue, 2),
            "top_performing_ads": top_ads,
            "revenue_per_day": round(estimated_revenue / days, 2)
        }