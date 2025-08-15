# Heritage Recipes API - Global Cultural Preservation & Specialty Ingredients
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from heritage_recipes_service import HeritageRecipesService, CulturalPreservationEngine
from heritage_recipes_models import (
    HeritageRecipeSubmission, IngredientSourceRequest, StoreRecommendationRequest,
    CulturalVerificationRequest, HeritageRecipeResponse, IngredientAvailabilityResponse,
    CountryRegion, IngredientRarity, CulturalSignificance, AuthenticityLevel
)

def create_heritage_recipes_router(heritage_service: HeritageRecipesService, get_current_user, get_current_user_optional):
    """Create Heritage Recipes API router with dependency injection"""
    
    router = APIRouter(prefix="/heritage", tags=["Heritage Recipes & Global Cultural Preservation"])
    
    # HERITAGE RECIPE DISCOVERY
    
    @router.get("/countries", response_model=List[dict])
    async def get_supported_countries():
        """Get list of supported global heritage countries and regions"""
        countries = [
            # Caribbean Islands
            {"code": "jamaica", "name": "Jamaica", "flag": "🇯🇲", "type": "caribbean"},
            {"code": "trinidad_tobago", "name": "Trinidad & Tobago", "flag": "🇹🇹", "type": "caribbean"},
            {"code": "barbados", "name": "Barbados", "flag": "🇧🇧", "type": "caribbean"},
            {"code": "haiti", "name": "Haiti", "flag": "🇭🇹", "type": "caribbean"},
            {"code": "dominican_republic", "name": "Dominican Republic", "flag": "🇩🇴", "type": "caribbean"},
            {"code": "puerto_rico", "name": "Puerto Rico", "flag": "🇵🇷", "type": "caribbean"},
            {"code": "cuba", "name": "Cuba", "flag": "🇨🇺", "type": "caribbean"},
            
            # Asian Heritage
            {"code": "china", "name": "China", "flag": "🇨🇳", "type": "asian"},
            {"code": "japan", "name": "Japan", "flag": "🇯🇵", "type": "asian"},
            {"code": "korea", "name": "Korea", "flag": "🇰🇷", "type": "asian"},
            {"code": "vietnam", "name": "Vietnam", "flag": "🇻🇳", "type": "asian"},
            {"code": "thailand", "name": "Thailand", "flag": "🇹🇭", "type": "asian"},
            {"code": "cambodia", "name": "Cambodia", "flag": "🇰🇭", "type": "asian"},
            {"code": "laos", "name": "Laos", "flag": "🇱🇦", "type": "asian"},
            {"code": "philippines", "name": "Philippines", "flag": "🇵🇭", "type": "asian"},
            {"code": "indonesia", "name": "Indonesia", "flag": "🇮🇩", "type": "asian"},
            {"code": "malaysia", "name": "Malaysia", "flag": "🇲🇾", "type": "asian"},
            {"code": "india", "name": "India", "flag": "🇮🇳", "type": "asian"},
            {"code": "pakistan", "name": "Pakistan", "flag": "🇵🇰", "type": "asian"},
            {"code": "bangladesh", "name": "Bangladesh", "flag": "🇧🇩", "type": "asian"},
            {"code": "sri_lanka", "name": "Sri Lanka", "flag": "🇱🇰", "type": "asian"},
            
            # African Heritage
            {"code": "nigeria", "name": "Nigeria", "flag": "🇳🇬", "type": "african"},
            {"code": "ghana", "name": "Ghana", "flag": "🇬🇭", "type": "african"},
            {"code": "senegal", "name": "Senegal", "flag": "🇸🇳", "type": "african"},
            {"code": "mali", "name": "Mali", "flag": "🇲🇱", "type": "african"},
            {"code": "ivory_coast", "name": "Côte d'Ivoire", "flag": "🇨🇮", "type": "african"},
            {"code": "cameroon", "name": "Cameroon", "flag": "🇨🇲", "type": "african"},
            {"code": "congo", "name": "Congo", "flag": "🇨🇬", "type": "african"},
            {"code": "ethiopia", "name": "Ethiopia", "flag": "🇪🇹", "type": "african"},
            {"code": "kenya", "name": "Kenya", "flag": "🇰🇪", "type": "african"},
            
            # Latin American
            {"code": "mexico", "name": "Mexico", "flag": "🇲🇽", "type": "latin_american"},
            {"code": "guatemala", "name": "Guatemala", "flag": "🇬🇹", "type": "latin_american"},
            {"code": "honduras", "name": "Honduras", "flag": "🇭🇳", "type": "latin_american"},
            {"code": "el_salvador", "name": "El Salvador", "flag": "🇸🇻", "type": "latin_american"},
            {"code": "colombia", "name": "Colombia", "flag": "🇨🇴", "type": "latin_american"},
            {"code": "venezuela", "name": "Venezuela", "flag": "🇻🇪", "type": "latin_american"},
            {"code": "peru", "name": "Peru", "flag": "🇵🇪", "type": "latin_american"},
            {"code": "ecuador", "name": "Ecuador", "flag": "🇪🇨", "type": "latin_american"},
            {"code": "bolivia", "name": "Bolivia", "flag": "🇧🇴", "type": "latin_american"},
            {"code": "chile", "name": "Chile", "flag": "🇨🇱", "type": "latin_american"},
            {"code": "argentina", "name": "Argentina", "flag": "🇦🇷", "type": "latin_american"},
            {"code": "brazil", "name": "Brazil", "flag": "🇧🇷", "type": "latin_american"},
            
            # Middle Eastern
            {"code": "turkey", "name": "Turkey", "flag": "🇹🇷", "type": "middle_eastern"},
            {"code": "iran", "name": "Iran", "flag": "🇮🇷", "type": "middle_eastern"},
            {"code": "lebanon", "name": "Lebanon", "flag": "🇱🇧", "type": "middle_eastern"},
            {"code": "syria", "name": "Syria", "flag": "🇸🇾", "type": "middle_eastern"},
            {"code": "jordan", "name": "Jordan", "flag": "🇯🇴", "type": "middle_eastern"},
            {"code": "afghanistan", "name": "Afghanistan", "flag": "🇦🇫", "type": "middle_eastern"},
            
            # European Heritage
            {"code": "italy", "name": "Italy", "flag": "🇮🇹", "type": "european"},
            {"code": "spain", "name": "Spain", "flag": "🇪🇸", "type": "european"},
            {"code": "portugal", "name": "Portugal", "flag": "🇵🇹", "type": "european"},
            {"code": "france", "name": "France", "flag": "🇫🇷", "type": "european"},
            {"code": "germany", "name": "Germany", "flag": "🇩🇪", "type": "european"},
            {"code": "poland", "name": "Poland", "flag": "🇵🇱", "type": "european"},
            {"code": "russia", "name": "Russia", "flag": "🇷🇺", "type": "european"},
            {"code": "ukraine", "name": "Ukraine", "flag": "🇺🇦", "type": "european"},
            {"code": "greece", "name": "Greece", "flag": "🇬🇷", "type": "european"},
            
            # Diaspora Communities
            {"code": "usa_south", "name": "Southern United States", "flag": "🇺🇸", "type": "diaspora"},
            {"code": "canada", "name": "Canada", "flag": "🇨🇦", "type": "diaspora"},
            {"code": "uk", "name": "United Kingdom", "flag": "🇬🇧", "type": "diaspora"}
        ]
        
        return countries
    
    @router.get("/recipes/country/{country_code}", response_model=List[dict])
    async def get_recipes_by_country(
        country_code: str,
        limit: int = Query(20, ge=1, le=50),
        authenticity_min: float = Query(3.0, ge=1.0, le=5.0)
    ):
        """Get heritage recipes from specific country/region"""
        try:
            country_region = CountryRegion(country_code)
            recipes = await heritage_service.get_recipes_by_country(country_region, limit)
            
            # Filter by minimum authenticity score
            filtered_recipes = [r for r in recipes if r.get("authenticity_score", 0) >= authenticity_min]
            
            return {
                "success": True,
                "country": country_code,
                "total_recipes": len(filtered_recipes),
                "recipes": filtered_recipes,
                "preservation_note": f"These traditional {country_code.replace('_', ' ').title()} recipes are preserved by community members"
            }
            
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unsupported country: {country_code}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/recipes/search", response_model=List[dict])
    async def search_heritage_recipes(
        q: str = Query(..., min_length=2, description="Search query"),
        country: Optional[str] = None,
        significance: Optional[str] = None,
        ingredients_available: bool = False,
        user_lat: Optional[float] = None,
        user_lng: Optional[float] = None,
        radius_km: float = 50
    ):
        """Search heritage recipes with cultural context"""
        try:
            filters = {}
            
            if country:
                filters["country_region"] = country
            
            if significance:
                filters["cultural_significance"] = significance
            
            if ingredients_available and user_lat and user_lng:
                filters["ingredients_available_locally"] = True
                filters["user_location"] = {"lat": user_lat, "lng": user_lng}
                filters["search_radius_km"] = radius_km
            
            recipes = await heritage_service.search_heritage_recipes(q, filters)
            
            return {
                "success": True,
                "query": q,
                "total_found": len(recipes),
                "recipes": recipes,
                "search_suggestions": [
                    "Try searching by dish name (e.g., 'ackee', 'callaloo')",
                    "Search by ingredient (e.g., 'plantain', 'scotch bonnet')",
                    "Use local names or pronunciations"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/recipes/submit", response_model=dict)
    async def submit_heritage_recipe(
        recipe_data: HeritageRecipeSubmission,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Submit a traditional Afro-Caribbean recipe for cultural preservation"""
        try:
            if not current_user_id:
                current_user_id = f"heritage_contributor_{str(uuid.uuid4())[:8]}"
            
            recipe = await heritage_service.submit_heritage_recipe(recipe_data.dict(), current_user_id)
            
            return {
                "success": True,
                "recipe_id": recipe.id,
                "message": "Thank you for preserving this cultural treasure!",
                "status": "submitted_for_community_review",
                "next_steps": [
                    "Community members will review for authenticity",
                    "Cultural experts may provide feedback",
                    "Recipe will be featured once verified"
                ],
                "cultural_impact": {
                    "preservation_priority": recipe.preservation_priority,
                    "cultural_significance": recipe.cultural_significance,
                    "specialty_ingredients": len(recipe.specialty_ingredients)
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/recipes/{recipe_id}/verify", response_model=dict)
    async def verify_recipe_authenticity(
        recipe_id: str,
        verification_data: CulturalVerificationRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Submit cultural verification for a heritage recipe (community experts only)"""
        try:
            result = await heritage_service.submit_cultural_verification(
                recipe_id, current_user_id, verification_data.dict()
            )
            
            if result.get("error"):
                raise HTTPException(status_code=403, detail=result["error"])
            
            return {
                "success": True,
                "verification_submitted": True,
                "message": "Thank you for helping preserve cultural authenticity!",
                "impact": "Your verification helps maintain recipe integrity for future generations"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # SPECIALTY INGREDIENT SOURCING
    
    @router.get("/ingredients/search", response_model=dict)
    async def search_specialty_ingredients(
        ingredient: str = Query(..., min_length=2),
        user_lat: Optional[float] = None,
        user_lng: Optional[float] = None,
        radius_km: float = 50,
        include_substitutes: bool = True
    ):
        """Find where to buy specialty Afro-Caribbean ingredients"""
        try:
            if user_lat and user_lng:
                user_location = {"lat": user_lat, "lng": user_lng}
                source_info = await heritage_service.find_ingredient_sources(ingredient, user_location, radius_km)
            else:
                # Return general info without location-specific data
                source_info = await heritage_service.find_ingredient_sources(ingredient, {"lat": 0, "lng": 0}, 1000)
            
            if source_info.get("error"):
                return {
                    "success": False,
                    "error": source_info["error"],
                    "suggestion": f"Try searching for '{ingredient}' with alternative names or check our ingredient database"
                }
            
            response = {
                "success": True,
                "ingredient_info": source_info,
                "sourcing_tips": [
                    "Call stores ahead to confirm availability",
                    "Ask about special orders if not in stock",
                    "Check with store owners about seasonal availability"
                ]
            }
            
            if include_substitutes and source_info.get("substitutes"):
                substitute_info = await heritage_service.get_ingredient_substitutions(ingredient)
                response["substitution_guide"] = substitute_info
            
            return response
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/ingredients/rare", response_model=List[dict])
    async def get_rare_ingredients(
        country: Optional[str] = None,
        rarity_level: Optional[str] = None
    ):
        """Get list of rare/hard-to-find ingredients by country"""
        try:
            # Build query for rare ingredients
            query = {}
            if rarity_level:
                query["rarity_level"] = rarity_level
            if country:
                query["origin_countries"] = country
            
            ingredients = await heritage_service.db.specialty_ingredients.find(query, {"_id": 0}).limit(50).to_list(length=50)
            
            # Group by rarity level
            grouped_ingredients = {}
            for ingredient in ingredients:
                rarity = ingredient.get("rarity_level", "unknown")
                if rarity not in grouped_ingredients:
                    grouped_ingredients[rarity] = []
                grouped_ingredients[rarity].append({
                    "name": ingredient["ingredient_name"],
                    "local_name": ingredient.get("ingredient_name_local"),
                    "alternatives": ingredient.get("alternative_names", []),
                    "cultural_uses": ingredient.get("cultural_uses", []),
                    "substitutes": len(ingredient.get("common_substitutes", []))
                })
            
            return {
                "success": True,
                "ingredients_by_rarity": grouped_ingredients,
                "total_ingredients": len(ingredients),
                "sourcing_note": "Contact ethnic grocery stores for best availability"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/ingredients/add", response_model=dict)
    async def add_specialty_ingredient(
        ingredient_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Add a hard-to-find Afro-Caribbean ingredient to the community database"""
        try:
            if not current_user_id:
                current_user_id = f"ingredient_contributor_{str(uuid.uuid4())[:8]}"
            
            ingredient = await heritage_service.add_specialty_ingredient(ingredient_data, current_user_id)
            
            return {
                "success": True,
                "ingredient_id": ingredient.id,
                "message": "Thank you for adding this specialty ingredient!",
                "community_benefit": "This helps others in the diaspora find authentic ingredients",
                "ingredient_name": ingredient.ingredient_name,
                "rarity_level": ingredient.rarity_level
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ETHNIC GROCERY STORE NETWORK
    
    @router.get("/stores/nearby", response_model=List[dict])
    async def find_nearby_ethnic_stores(
        lat: float,
        lng: float,
        radius_km: float = 25,
        country_specialty: Optional[str] = None
    ):
        """Find ethnic grocery stores serving Afro-Caribbean communities"""
        try:
            user_location = {"lat": lat, "lng": lng}
            country_filter = CountryRegion(country_specialty) if country_specialty else None
            
            stores = await heritage_service.find_nearby_ethnic_stores(user_location, country_filter, radius_km)
            
            return {
                "success": True,
                "total_stores": len(stores),
                "stores": stores,
                "search_area": f"{radius_km}km radius",
                "community_note": "These stores are recommended by community members",
                "tips": [
                    "Call ahead for specialty items",
                    "Ask about weekly delivery schedules",
                    "Inquire about cultural events and cooking classes"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/stores/register", response_model=dict)
    async def register_ethnic_store(
        store_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Register a specialty grocery store serving Afro-Caribbean communities"""
        try:
            if not current_user_id:
                current_user_id = f"store_recommender_{str(uuid.uuid4())[:8]}"
            
            store = await heritage_service.register_ethnic_store(store_data, current_user_id)
            
            return {
                "success": True,
                "store_id": store.id,
                "message": "Thank you for connecting this store with the community!",
                "community_impact": "This helps diaspora members find authentic ingredients",
                "store_name": store.store_name,
                "specialties": store.specialties,
                "next_steps": [
                    "Store will be verified by community members",
                    "Store owner may be contacted for partnership opportunities",
                    "Store will appear in community searches once approved"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # CULTURAL COLLECTIONS & DIASPORA FEATURES
    
    @router.get("/collections/featured", response_model=List[dict])
    async def get_featured_collections():
        """Get curated collections of heritage recipes"""
        try:
            collections = await heritage_service.get_featured_collections()
            
            return {
                "success": True,
                "featured_collections": collections,
                "collection_themes": [
                    "Holiday Traditions by Country",
                    "Endangered Recipes (High Priority Preservation)",
                    "Diaspora Comfort Foods",
                    "Ceremonial & Celebration Dishes",
                    "Ingredients at Risk of Being Lost"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/diaspora/recommendations", response_model=dict)
    async def get_diaspora_recommendations(
        heritage_countries: str = Query(..., description="Comma-separated country codes"),
        lat: Optional[float] = None,
        lng: Optional[float] = None
    ):
        """Get personalized recommendations for diaspora community members"""
        try:
            # Parse heritage countries
            heritage_list = []
            for country_code in heritage_countries.split(","):
                try:
                    heritage_list.append(CountryRegion(country_code.strip()))
                except ValueError:
                    continue
            
            if not heritage_list:
                raise HTTPException(status_code=400, detail="Please provide valid heritage country codes")
            
            user_location = {"lat": lat or 40.7128, "lng": lng or -74.0060}  # Default NYC
            recommendations = await heritage_service.get_diaspora_recommendations(heritage_list, user_location)
            
            return {
                "success": True,
                "heritage_countries": [h.value for h in heritage_list],
                "personalized_recommendations": recommendations,
                "cultural_connection": "Recipes and ingredients that connect you to your heritage",
                "community_message": "You're part of a global community preserving these traditions"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/preservation/insights", response_model=dict)
    async def get_cultural_preservation_insights():
        """Get insights about Afro-Caribbean cultural preservation efforts"""
        try:
            insights = await heritage_service.get_preservation_insights()
            
            return {
                "success": True,
                "preservation_insights": insights,
                "mission_statement": "Preserving Afro-Caribbean culinary heritage for future generations",
                "community_impact": "Every recipe and ingredient documented helps keep traditions alive",
                "how_to_help": [
                    "Submit family recipes with cultural context",
                    "Document hard-to-find ingredients and where to buy them",
                    "Recommend ethnic grocery stores in your area",
                    "Share the stories behind traditional dishes",
                    "Verify authenticity of community-submitted recipes"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # CULTURAL SIGNIFICANCE & EDUCATION
    
    @router.get("/cultural/significance", response_model=List[dict])
    async def get_cultural_significance_types():
        """Get types of cultural significance for recipes"""
        return [
            {
                "code": "everyday",
                "name": "Everyday Family Meals",
                "description": "Regular dishes prepared for daily family meals",
                "examples": ["Rice and peas", "Plantain and saltfish"]
            },
            {
                "code": "celebration",
                "name": "Celebration & Holiday Dishes",
                "description": "Special foods for holidays, birthdays, and celebrations",
                "examples": ["Christmas black cake", "Carnival foods", "Wedding traditions"]
            },
            {
                "code": "ceremonial",
                "name": "Religious & Ceremonial Foods",
                "description": "Foods with spiritual or ceremonial importance",
                "examples": ["Ancestral offerings", "Religious festival foods"]
            },
            {
                "code": "heritage",
                "name": "Heritage & Traditional Recipes",
                "description": "Recipes passed down through generations",
                "examples": ["Grandmother's secret recipes", "Ancient preparation methods"]
            },
            {
                "code": "seasonal",
                "name": "Seasonal Traditions",
                "description": "Foods tied to specific seasons or harvest times",
                "examples": ["Mango season treats", "Harvest celebration dishes"]
            },
            {
                "code": "diaspora",
                "name": "Diaspora Comfort Foods",
                "description": "Adapted recipes that bring comfort to diaspora communities",
                "examples": ["Modified recipes using available ingredients", "Fusion adaptations"]
            }
        ]
    
    @router.get("/recipes/{recipe_id}", response_model=dict)
    async def get_heritage_recipe_details(recipe_id: str):
        """Get detailed information about a specific heritage recipe"""
        try:
            recipe = await heritage_service.db.heritage_recipes.find_one({"id": recipe_id}, {"_id": 0})
            
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            
            # Get ingredient sourcing info
            ingredient_sourcing = {}
            for ingredient_name in recipe.get("specialty_ingredients", []):
                sourcing_info = await heritage_service.find_ingredient_sources(
                    ingredient_name, {"lat": 0, "lng": 0}, 1000
                )
                if not sourcing_info.get("error"):
                    ingredient_sourcing[ingredient_name] = {
                        "rarity": sourcing_info.get("rarity_level"),
                        "substitutes": sourcing_info.get("substitutes", []),
                        "cultural_uses": sourcing_info.get("cultural_uses", [])
                    }
            
            return {
                "success": True,
                "recipe": recipe,
                "ingredient_sourcing": ingredient_sourcing,
                "authenticity_note": "This recipe has been shared by community members and may be verified by cultural experts",
                "preservation_importance": f"Priority level {recipe.get('preservation_priority', 3)}/5 for cultural preservation"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # SPECIALTY STORE CHAIN INTEGRATION
    
    @router.get("/stores/chains", response_model=dict)
    async def get_supported_store_chains():
        """Get list of supported ethnic grocery store chains"""
        chains = [
            {
                "chain_id": "h_mart",
                "name": "H Mart",
                "description": "Korean-American supermarket chain specializing in Asian foods",
                "specialties": ["Korean", "Japanese", "Chinese", "Vietnamese", "Thai"],
                "countries_served": ["korea", "japan", "china", "vietnam", "thailand"],
                "typical_products": ["Korean chili paste", "Miso", "Rice cakes", "Asian vegetables"],
                "locations_usa": "80+",
                "website": "hmart.com",
                "integration_status": "supported"
            },
            {
                "chain_id": "patel_brothers",
                "name": "Patel Brothers",
                "description": "Indian grocery store chain with authentic Indian ingredients",
                "specialties": ["Indian", "Pakistani", "Bangladeshi", "Sri Lankan"],
                "countries_served": ["india", "pakistan", "bangladesh", "sri_lanka"],
                "typical_products": ["Basmati rice", "Lentils", "Spices", "Curry leaves", "Ghee"],
                "locations_usa": "50+",
                "website": "patelbros.com",
                "integration_status": "supported"
            },
            {
                "chain_id": "ranch_99",
                "name": "99 Ranch Market",
                "description": "Asian-American supermarket chain",
                "specialties": ["Chinese", "Taiwanese", "Vietnamese", "Korean", "Filipino"],
                "countries_served": ["china", "taiwan", "vietnam", "korea", "philippines"],
                "typical_products": ["Chinese vegetables", "Fresh noodles", "Soy sauces", "Asian fruits"],
                "locations_usa": "50+",
                "website": "99ranch.com",
                "integration_status": "supported"
            },
            {
                "chain_id": "fresh_thyme",
                "name": "Fresh Thyme International",
                "description": "Latin American grocery stores",
                "specialties": ["Mexican", "Guatemalan", "Honduran", "Salvadoran"],
                "countries_served": ["mexico", "guatemala", "honduras", "el_salvador"],
                "typical_products": ["Mexican chiles", "Masa harina", "Mexican cheeses", "Plantains"],
                "locations_usa": "30+",
                "website": "varies by location",
                "integration_status": "basic"
            },
            {
                "chain_id": "african_market",
                "name": "African Food Markets",
                "description": "Various African grocery stores",
                "specialties": ["Nigerian", "Ghanaian", "Ethiopian", "Cameroonian"],
                "countries_served": ["nigeria", "ghana", "ethiopia", "cameroon", "senegal"],
                "typical_products": ["Cassava flour", "Palm oil", "African spices", "Dried fish"],
                "locations_usa": "varies",
                "website": "varies by location",
                "integration_status": "basic"
            }
        ]
        
        return {
            "success": True,
            "supported_chains": chains,
            "total_chains": len(chains),
            "integration_note": "We're continuously adding more ethnic grocery chains to help you find authentic ingredients"
        }
    
    @router.get("/ingredients/chain-availability", response_model=dict)
    async def check_ingredient_chain_availability(
        ingredient: str = Query(..., min_length=2),
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: float = 50
    ):
        """Check ingredient availability at major ethnic grocery chains"""
        try:
            user_location = {"lat": lat or 40.7128, "lng": lng or -74.0060}  # Default NYC
            
            chain_availability = await heritage_service.get_chain_store_availability(
                ingredient, user_location, radius_km
            )
            
            return {
                "success": True,
                "ingredient_searched": ingredient,
                "search_location": user_location if lat and lng else "default_location",
                "chain_results": chain_availability,
                "shopping_tips": [
                    "Call stores ahead to confirm current stock",
                    "Ask about special order options if not in stock",
                    "Check store websites for online shopping availability",
                    "Visit during restock days (usually mid-week) for best selection"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/stores/register-chain", response_model=dict)
    async def register_store_chain(
        chain_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Register a major ethnic grocery store chain with locations"""
        try:
            if not current_user_id:
                current_user_id = f"chain_registrant_{str(uuid.uuid4())[:8]}"
            
            chain_name = chain_data.get("chain_name", "").lower()
            result = await heritage_service.register_specialty_store_chain(chain_name, chain_data)
            
            if result.get("error"):
                raise HTTPException(status_code=400, detail=result["error"])
            
            return {
                "success": True,
                "chain_registration": result,
                "community_impact": "This helps diaspora communities find ingredients from their heritage",
                "next_steps": [
                    "Chain locations will be verified",
                    "Integration with chain inventory systems (if available)",
                    "Community members can report ingredient availability"
                ]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/stores/sync-inventory/{chain_name}", response_model=dict)
    async def sync_chain_inventory(
        chain_name: str,
        current_user_id: str = Depends(get_current_user)
    ):
        """Sync inventory data from store chain websites (admin only)"""
        try:
            result = await heritage_service.sync_store_chain_inventory(chain_name)
            
            return {
                "success": True,
                "sync_result": result,
                "note": "Web scraping integration is coming soon to automatically track ingredient availability"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router