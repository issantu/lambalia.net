# Heritage Recipes Service - Global Cultural Preservation & Specialty Ingredients
import asyncio
import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from heritage_recipes_models import (
    HeritageRecipe, SpecialtyIngredient, EthnicGroceryStore, CulturalContributor,
    HeritageCollection, CountryRegion, IngredientRarity, CulturalSignificance,
    AuthenticityLevel
)

class CulturalPreservationEngine:
    """Engine for cultural recipe preservation and authenticity verification"""
    
    @staticmethod
    def calculate_authenticity_score(recipe: HeritageRecipe, community_feedback: List[Dict]) -> float:
        """Calculate authenticity score based on community feedback and verification"""
        base_score = 3.0  # Start with neutral score
        
        # Elder approval adds significant weight
        if recipe.elder_approved:
            base_score += 1.5
        
        # Community ratings
        if recipe.community_ratings:
            avg_rating = sum(recipe.community_ratings.values()) / len(recipe.community_ratings)
            base_score = (base_score + avg_rating) / 2
        
        # Contributor credibility
        if recipe.source_verification:
            base_score += 0.5
        
        # Historical context adds authenticity
        if recipe.historical_context and len(recipe.historical_context) > 100:
            base_score += 0.3
        
        # Family story adds personal authenticity
        if recipe.family_story and len(recipe.family_story) > 50:
            base_score += 0.2
        
        return min(5.0, max(1.0, base_score))
    
    @staticmethod
    def assess_ingredient_rarity(ingredient_name: str, availability_data: Dict) -> IngredientRarity:
        """Assess how rare/hard to find an ingredient is"""
        store_count = availability_data.get('store_count', 0)
        online_availability = availability_data.get('online_sources', 0)
        price_premium = availability_data.get('price_premium', 1.0)
        
        if store_count == 0 and online_availability == 0:
            return IngredientRarity.ENDANGERED
        elif store_count <= 2 and price_premium > 3.0:
            return IngredientRarity.RARE
        elif store_count <= 5 and online_availability <= 2:
            return IngredientRarity.IMPORTED_ONLY
        elif store_count <= 10:
            return IngredientRarity.SPECIALTY
        else:
            return IngredientRarity.COMMON
    
    @staticmethod
    def calculate_distance_km(loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """Calculate distance between two geographic points"""
        try:
            lat1, lng1 = loc1["lat"], loc1["lng"]
            lat2, lng2 = loc2["lat"], loc2["lng"]
            
            # Haversine formula
            lat1_rad = math.radians(lat1)
            lng1_rad = math.radians(lng1)
            lat2_rad = math.radians(lat2)
            lng2_rad = math.radians(lng2)
            
            dlat = lat2_rad - lat1_rad
            dlng = lng2_rad - lng1_rad
            a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return c * 6371  # Earth radius in km
        except:
            return float('inf')

class HeritageRecipesService:
    """Main service for global heritage recipe preservation and specialty ingredient sourcing"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.preservation_engine = CulturalPreservationEngine()
        self.logger = logging.getLogger(__name__)
    
    # HERITAGE RECIPE MANAGEMENT
    
    async def submit_heritage_recipe(self, recipe_data: Dict[str, Any], contributor_id: str) -> HeritageRecipe:
        """Submit a traditional heritage recipe from any global community for preservation"""
        
        # Validate cultural contributor
        contributor = await self.db.cultural_contributors.find_one({"user_id": contributor_id}, {"_id": 0})
        if not contributor:
            # Create basic contributor profile
            contributor_profile = CulturalContributor(
                user_id=contributor_id,
                cultural_heritage=[CountryRegion(recipe_data["country_region"])],
                specialty_cuisines=[CountryRegion(recipe_data["country_region"])]
            )
            await self.db.cultural_contributors.insert_one(contributor_profile.dict())
        
        # Create heritage recipe
        heritage_recipe = HeritageRecipe(
            created_by=contributor_id,
            **recipe_data
        )
        
        # Analyze ingredient rarity
        specialty_ingredients = []
        for ingredient in heritage_recipe.traditional_ingredients:
            ingredient_name = ingredient.get("name", "")
            if ingredient_name:
                # Check if ingredient exists in specialty database
                specialty_data = await self.db.specialty_ingredients.find_one(
                    {"ingredient_name": {"$regex": ingredient_name, "$options": "i"}}, {"_id": 0}
                )
                if specialty_data and specialty_data.get("rarity_level") in ["rare", "specialty", "imported_only"]:
                    specialty_ingredients.append(ingredient_name)
        
        heritage_recipe.specialty_ingredients = specialty_ingredients
        
        await self.db.heritage_recipes.insert_one(heritage_recipe.dict())
        
        # Update contributor stats
        await self.db.cultural_contributors.update_one(
            {"user_id": contributor_id},
            {
                "$inc": {"family_recipes_count": 1},
                "$push": {"recipes_contributed": heritage_recipe.id}
            }
        )
        
        self.logger.info(f"Heritage recipe submitted: {heritage_recipe.id} from {heritage_recipe.country_region}")
        return heritage_recipe
    
    async def get_recipes_by_country(self, country_region: CountryRegion, limit: int = 20) -> List[Dict[str, Any]]:
        """Get heritage recipes from specific country/region"""
        
        recipes = await self.db.heritage_recipes.find(
            {"country_region": country_region, "is_public": True},
            {"_id": 0}
        ).sort("preservation_priority", -1).limit(limit).to_list(length=limit)
        
        # Enhance with availability data
        enhanced_recipes = []
        for recipe in recipes:
            # Calculate authenticity score
            recipe["authenticity_score"] = self.preservation_engine.calculate_authenticity_score(
                HeritageRecipe(**recipe), []
            )
            
            # Add ingredient sourcing info
            ingredient_availability = await self._get_ingredient_availability(recipe["specialty_ingredients"])
            recipe["ingredient_sourcing"] = ingredient_availability
            
            enhanced_recipes.append(recipe)
        
        return enhanced_recipes
    
    async def search_heritage_recipes(self, query: str, filters: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """Search heritage recipes with cultural context"""
        
        # Build search query
        search_conditions = []
        
        # Text search
        if query:
            search_conditions.append({
                "$or": [
                    {"recipe_name": {"$regex": query, "$options": "i"}},
                    {"recipe_name_local": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"traditional_ingredients.name": {"$regex": query, "$options": "i"}},
                    {"historical_context": {"$regex": query, "$options": "i"}}
                ]
            })
        
        # Filter by country/region
        if filters.get("country_region"):
            search_conditions.append({"country_region": filters["country_region"]})
        
        # Filter by cultural significance
        if filters.get("cultural_significance"):
            search_conditions.append({"cultural_significance": filters["cultural_significance"]})
        
        # Filter by ingredient availability
        if filters.get("ingredients_available_locally"):
            # Only show recipes where ingredients can be found locally
            available_recipes = await self._filter_by_ingredient_availability(
                filters.get("user_location", {}), filters.get("search_radius_km", 50)
            )
            if available_recipes:
                search_conditions.append({"id": {"$in": available_recipes}})
        
        # Execute search
        final_query = {"$and": search_conditions} if search_conditions else {}
        final_query["is_public"] = True
        
        recipes = await self.db.heritage_recipes.find(final_query, {"_id": 0}).limit(50).to_list(length=50)
        
        # Sort by relevance and authenticity
        for recipe in recipes:
            recipe["authenticity_score"] = self.preservation_engine.calculate_authenticity_score(
                HeritageRecipe(**recipe), []
            )
        
        recipes.sort(key=lambda x: (x["authenticity_score"], x["preservation_priority"]), reverse=True)
        return recipes
    
    # SPECIALTY INGREDIENT MANAGEMENT
    
    async def add_specialty_ingredient(self, ingredient_data: Dict[str, Any], contributor_id: str) -> SpecialtyIngredient:
        """Add a hard-to-find heritage ingredient from any global community to the database"""
        
        ingredient = SpecialtyIngredient(
            added_by=contributor_id,
            **ingredient_data
        )
        
        await self.db.specialty_ingredients.insert_one(ingredient.dict())
        
        # Update contributor stats
        await self.db.cultural_contributors.update_one(
            {"user_id": contributor_id},
            {"$push": {"ingredients_documented": ingredient.id}}
        )
        
        self.logger.info(f"Specialty ingredient added: {ingredient.ingredient_name}")
        return ingredient
    
    async def find_ingredient_sources(self, ingredient_name: str, user_location: Dict[str, float], 
                                    radius_km: float = 50) -> Dict[str, Any]:
        """Find where to buy a specific specialty ingredient"""
        
        # Get ingredient details
        ingredient = await self.db.specialty_ingredients.find_one(
            {"ingredient_name": {"$regex": ingredient_name, "$options": "i"}}, {"_id": 0}
        )
        
        if not ingredient:
            return {"error": "Ingredient not found in specialty database"}
        
        # Find nearby stores that carry this ingredient
        nearby_stores = await self._find_stores_with_ingredient(ingredient_name, user_location, radius_km)
        
        # Get online sources
        online_sources = ingredient.get("online_suppliers", [])
        
        # Calculate average price
        price_data = ingredient.get("typical_price_range", {})
        avg_price = sum(price_data.values()) / len(price_data) if price_data else 0
        
        return {
            "ingredient_name": ingredient["ingredient_name"],
            "ingredient_name_local": ingredient.get("ingredient_name_local"),
            "alternative_names": ingredient.get("alternative_names", []),
            "rarity_level": ingredient["rarity_level"],
            "nearby_stores": nearby_stores,
            "online_sources": online_sources,
            "average_price": avg_price,
            "substitutes": ingredient.get("common_substitutes", []),
            "seasonal_info": ingredient.get("seasonal_availability", {}),
            "storage_tips": ingredient.get("storage_requirements", []),
            "cultural_uses": ingredient.get("cultural_uses", [])
        }
    
    async def get_ingredient_substitutions(self, ingredient_name: str) -> Dict[str, Any]:
        """Get substitution suggestions for hard-to-find ingredients"""
        
        ingredient = await self.db.specialty_ingredients.find_one(
            {"ingredient_name": {"$regex": ingredient_name, "$options": "i"}}, {"_id": 0}
        )
        
        if not ingredient:
            return {"error": "Ingredient not found"}
        
        return {
            "original_ingredient": ingredient["ingredient_name"],
            "common_substitutes": ingredient.get("common_substitutes", []),
            "substitution_ratios": ingredient.get("substitution_ratio", {}),
            "flavor_impact": "Check flavor profile - substitutes may alter taste",
            "availability_comparison": await self._compare_substitute_availability(ingredient["common_substitutes"]),
            "authenticity_note": "Using substitutes will modify the traditional recipe"
        }
    
    # ETHNIC GROCERY STORE MANAGEMENT
    
    async def register_ethnic_store(self, store_data: Dict[str, Any], contributor_id: str) -> EthnicGroceryStore:
        """Register a specialty grocery store serving Afro-Caribbean communities"""
        
        store = EthnicGroceryStore(
            added_by=contributor_id,
            **store_data
        )
        
        await self.db.ethnic_grocery_stores.insert_one(store.dict())
        
        # Update contributor stats
        await self.db.cultural_contributors.update_one(
            {"user_id": contributor_id},
            {"$push": {"stores_recommended": store.id}}
        )
        
        self.logger.info(f"Ethnic grocery store registered: {store.store_name}")
        return store
    
    async def find_nearby_ethnic_stores(self, user_location: Dict[str, float], 
                                      country_specialty: Optional[CountryRegion] = None,
                                      radius_km: float = 25) -> List[Dict[str, Any]]:
        """Find ethnic grocery stores near user location"""
        
        # Build query
        query = {"is_active": True}
        if country_specialty:
            query["specialties"] = country_specialty
        
        stores = await self.db.ethnic_grocery_stores.find(query, {"_id": 0}).to_list(length=100)
        
        # Filter by distance and add distance info
        nearby_stores = []
        for store in stores:
            if store.get("location"):
                distance = self.preservation_engine.calculate_distance_km(user_location, store["location"])
                if distance <= radius_km:
                    store["distance_km"] = round(distance, 1)
                    store["estimated_travel_time"] = self._estimate_travel_time(distance)
                    nearby_stores.append(store)
        
        # Sort by distance and community rating
        nearby_stores.sort(key=lambda x: (x["distance_km"], -x.get("community_rating", 0)))
        return nearby_stores
    
    # CULTURAL COLLECTIONS & CURATION
    
    async def create_heritage_collection(self, collection_data: Dict[str, Any], curator_id: str) -> HeritageCollection:
        """Create curated collection of heritage recipes"""
        
        collection = HeritageCollection(
            curated_by=curator_id,
            **collection_data
        )
        
        await self.db.heritage_collections.insert_one(collection.dict())
        
        self.logger.info(f"Heritage collection created: {collection.collection_name}")
        return collection
    
    async def get_featured_collections(self) -> List[Dict[str, Any]]:
        """Get featured heritage recipe collections"""
        
        collections = await self.db.heritage_collections.find(
            {"is_featured": True}, {"_id": 0}
        ).sort("created_at", -1).limit(10).to_list(length=10)
        
        # Enhance with recipe previews
        for collection in collections:
            if collection["recipe_ids"]:
                # Get sample recipes from collection
                sample_recipes = await self.db.heritage_recipes.find(
                    {"id": {"$in": collection["recipe_ids"][:3]}}, {"_id": 0}
                ).to_list(length=3)
                collection["sample_recipes"] = sample_recipes
        
        return collections
    
    async def get_diaspora_recommendations(self, user_heritage: List[CountryRegion], 
                                        user_location: Dict[str, float]) -> Dict[str, Any]:
        """Get personalized recommendations for diaspora community members"""
        
        recommendations = {
            "comfort_recipes": [],
            "seasonal_traditions": [],
            "nearby_stores": [],
            "rare_ingredients_available": [],
            "community_events": []
        }
        
        # Get comfort food recipes from user's heritage
        for heritage in user_heritage:
            comfort_recipes = await self.db.heritage_recipes.find({
                "country_region": heritage,
                "cultural_significance": CulturalSignificance.DIASPORA_COMFORT,
                "is_public": True
            }, {"_id": 0}).limit(5).to_list(length=5)
            recommendations["comfort_recipes"].extend(comfort_recipes)
        
        # Find nearby ethnic stores
        nearby_stores = await self.find_nearby_ethnic_stores(user_location, user_heritage[0] if user_heritage else None)
        recommendations["nearby_stores"] = nearby_stores[:5]
        
        # Check for rare ingredients currently available
        for store in nearby_stores[:3]:
            if store.get("specialty_ingredients"):
                rare_items = await self.db.specialty_ingredients.find({
                    "id": {"$in": store["specialty_ingredients"]},
                    "rarity_level": {"$in": ["rare", "imported_only"]}
                }, {"_id": 0}).limit(3).to_list(length=3)
                if rare_items:
                    recommendations["rare_ingredients_available"].extend([
                        {**item, "available_at": store["store_name"]} for item in rare_items
                    ])
        
        return recommendations
    
    # COMMUNITY VERIFICATION & AUTHENTICITY
    
    async def submit_cultural_verification(self, recipe_id: str, verifier_id: str, 
                                         verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit cultural verification for a heritage recipe"""
        
        # Check verifier credentials
        verifier = await self.db.cultural_contributors.find_one({"user_id": verifier_id}, {"_id": 0})
        if not verifier or verifier.get("community_recognition") not in ["expert", "elder", "cultural_keeper"]:
            return {"error": "Insufficient verification credentials"}
        
        # Update recipe with verification
        verification_entry = {
            f"community_ratings.{verifier_id}": verification_data["authenticity_rating"],
            "verified_by": verifier_id,
            "updated_at": datetime.utcnow()
        }
        
        if verification_data.get("elder_verification"):
            verification_entry["elder_approved"] = True
        
        await self.db.heritage_recipes.update_one(
            {"id": recipe_id},
            {"$set": verification_entry}
        )
        
        # Update verifier stats
        await self.db.cultural_contributors.update_one(
            {"user_id": verifier_id},
            {"$inc": {"verified_recipes": 1}}
        )
        
        return {"success": True, "verification_submitted": True}
    
    # ANALYTICS & INSIGHTS
    
    async def get_preservation_insights(self) -> Dict[str, Any]:
        """Get insights about cultural preservation efforts"""
        
        # Recipe preservation stats
        total_recipes = await self.db.heritage_recipes.count_documents({"is_public": True})
        recipes_by_country = await self.db.heritage_recipes.aggregate([
            {"$match": {"is_public": True}},
            {"$group": {"_id": "$country_region", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]).to_list(length=10)
        
        # Ingredient rarity distribution
        ingredient_rarity = await self.db.specialty_ingredients.aggregate([
            {"$group": {"_id": "$rarity_level", "count": {"$sum": 1}}}
        ]).to_list(length=10)
        
        # Active contributors
        active_contributors = await self.db.cultural_contributors.count_documents({
            "family_recipes_count": {"$gt": 0}
        })
        
        # Store coverage
        store_coverage = await self.db.ethnic_grocery_stores.aggregate([
            {"$match": {"is_active": True}},
            {"$group": {"_id": "$country", "store_count": {"$sum": 1}}},
            {"$sort": {"store_count": -1}}
        ]).to_list(length=20)
        
        return {
            "total_recipes_preserved": total_recipes,
            "recipes_by_country": recipes_by_country,
            "ingredient_rarity_distribution": ingredient_rarity,
            "active_cultural_contributors": active_contributors,
            "store_coverage_by_country": store_coverage,
            "preservation_priority_recipes": await self._get_priority_preservation_recipes(),
            "community_engagement_stats": await self._get_community_engagement_stats()
        }
    
    # PRIVATE HELPER METHODS
    
    async def _get_ingredient_availability(self, ingredient_list: List[str]) -> Dict[str, str]:
        """Check availability of specialty ingredients"""
        availability = {}
        for ingredient_name in ingredient_list:
            ingredient_data = await self.db.specialty_ingredients.find_one(
                {"ingredient_name": {"$regex": ingredient_name, "$options": "i"}}, {"_id": 0}
            )
            if ingredient_data:
                rarity = ingredient_data.get("rarity_level", "unknown")
                store_count = len(ingredient_data.get("available_at_stores", []))
                if store_count > 10:
                    availability[ingredient_name] = "widely_available"
                elif store_count > 3:
                    availability[ingredient_name] = "specialty_stores"
                elif rarity in ["rare", "imported_only"]:
                    availability[ingredient_name] = "very_limited"
                else:
                    availability[ingredient_name] = "limited"
            else:
                availability[ingredient_name] = "unknown"
        
        return availability
    
    async def _find_stores_with_ingredient(self, ingredient_name: str, user_location: Dict[str, float], 
                                         radius_km: float) -> List[Dict[str, Any]]:
        """Find stores that carry a specific ingredient"""
        
        # Get ingredient ID
        ingredient = await self.db.specialty_ingredients.find_one(
            {"ingredient_name": {"$regex": ingredient_name, "$options": "i"}}, {"_id": 0}
        )
        
        if not ingredient:
            return []
        
        # Find stores that carry this ingredient
        stores = await self.db.ethnic_grocery_stores.find({
            "specialty_ingredients": ingredient["id"],
            "is_active": True
        }, {"_id": 0}).to_list(length=50)
        
        # Filter by distance
        nearby_stores = []
        for store in stores:
            if store.get("location"):
                distance = self.preservation_engine.calculate_distance_km(user_location, store["location"])
                if distance <= radius_km:
                    store["distance_km"] = round(distance, 1)
                    nearby_stores.append(store)
        
        return sorted(nearby_stores, key=lambda x: x["distance_km"])
    
    async def _compare_substitute_availability(self, substitutes: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Compare availability of substitute ingredients"""
        comparison = []
        for substitute in substitutes:
            substitute_name = substitute.get("substitute", "")
            if substitute_name:
                availability_data = await self.find_ingredient_sources(substitute_name, {"lat": 0, "lng": 0}, 1000)
                comparison.append({
                    "substitute": substitute_name,
                    "availability": "available" if not availability_data.get("error") else "limited",
                    "rarity": availability_data.get("rarity_level", "unknown")
                })
        return comparison
    
    def _estimate_travel_time(self, distance_km: float) -> str:
        """Estimate travel time based on distance"""
        if distance_km <= 5:
            return "10-15 minutes"
        elif distance_km <= 15:
            return "20-30 minutes"
        elif distance_km <= 30:
            return "30-45 minutes"
        else:
            return "45+ minutes"
    
    async def _get_priority_preservation_recipes(self) -> List[Dict[str, Any]]:
        """Get recipes that are high priority for preservation"""
        return await self.db.heritage_recipes.find({
            "preservation_priority": {"$gte": 4},
            "elder_approved": False
        }, {"_id": 0}).limit(10).to_list(length=10)
    
    async def _get_community_engagement_stats(self) -> Dict[str, int]:
        """Get community engagement statistics"""
        total_likes = await self.db.heritage_recipes.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$likes_count"}}}
        ]).to_list(length=1)
        
        total_shares = await self.db.heritage_recipes.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$shares_count"}}}
        ]).to_list(length=1)
        
        return {
            "total_recipe_likes": total_likes[0]["total"] if total_likes else 0,
            "total_recipe_shares": total_shares[0]["total"] if total_shares else 0,
            "recipes_tried": await self.db.heritage_recipes.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$tried_count"}}}
            ]).to_list(length=1)
        }