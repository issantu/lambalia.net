# Enhanced Smart Cooking API - SuperCook + HackTheMenu Integration
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enhanced_smart_cooking_service import get_enhanced_cooking_service, EnhancedSmartCookingService

# Request Models
class AddIngredientsRequest(BaseModel):
    ingredients: List[str]

class RemoveIngredientsRequest(BaseModel):
    ingredients: List[str]

class CreatePantryRequest(BaseModel):
    pantry_name: str = "My Kitchen"

class RecipeSearchRequest(BaseModel):
    max_missing_ingredients: int = 0
    cuisine_preference: Optional[str] = None
    complexity_level: Optional[str] = None

# Response Models
class PantryResponse(BaseModel):
    success: bool
    pantry: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class RecipeSearchResponse(BaseModel):
    success: bool
    recipes: List[Dict[str, Any]] = []
    total_found: int = 0
    ingredients_used: List[str] = []
    error: Optional[str] = None

class IngredientSuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]

def create_enhanced_smart_cooking_router(db, get_current_user):
    """Create Enhanced Smart Cooking API router"""
    
    router = APIRouter(prefix="/enhanced-cooking", tags=["Enhanced Smart Cooking"])
    
    @router.post("/pantry/create")
    async def create_user_pantry(
        request: CreatePantryRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Create user's virtual pantry (SuperCook style)"""
        try:
            service = await get_enhanced_cooking_service(db)
            result = await service.create_user_pantry(current_user_id, request.pantry_name)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/pantry")
    async def get_user_pantry(
        current_user_id: str = Depends(get_current_user)
    ):
        """Get user's current pantry contents"""
        try:
            service = await get_enhanced_cooking_service(db)
            result = await service.get_user_pantry(current_user_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/pantry/add-ingredients")
    async def add_ingredients_to_pantry(
        request: AddIngredientsRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Add ingredients to user's virtual pantry"""
        try:
            service = await get_enhanced_cooking_service(db)
            result = await service.add_ingredients_to_pantry(current_user_id, request.ingredients)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/pantry/remove-ingredients")
    async def remove_ingredients_from_pantry(
        request: RemoveIngredientsRequest,
        current_user_id: str = Depends(get_current_user)
    ):
        """Remove ingredients from user's pantry"""
        try:
            service = await get_enhanced_cooking_service(db)
            result = await service.remove_ingredients_from_pantry(current_user_id, request.ingredients)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/recipes/find")
    async def find_recipes_by_available_ingredients(
        max_missing: int = Query(0, description="Maximum missing ingredients allowed"),
        current_user_id: str = Depends(get_current_user)
    ):
        """Find recipes based on available ingredients (SuperCook style)"""
        try:
            service = await get_enhanced_cooking_service(db)
            result = await service.find_recipes_by_ingredients(current_user_id, max_missing)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/ingredients/suggestions")
    async def get_ingredient_suggestions(
        query: str = Query(..., description="Search query for ingredient suggestions")
    ):
        """Get ingredient suggestions for autocomplete"""
        try:
            service = await get_enhanced_cooking_service(db)
            suggestions = await service.get_ingredient_suggestions(query)
            return {"suggestions": suggestions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/fastfood/restaurants")  
    async def get_supported_fastfood_restaurants():
        """Get list of supported fast food restaurants from HackTheMenu"""
        try:
            restaurants = [
                {
                    "name": "McDonald's",
                    "category": "Burgers",
                    "items_available": 15,
                    "secret_menu_items": 8
                },
                {
                    "name": "KFC", 
                    "category": "Chicken",
                    "items_available": 10,
                    "secret_menu_items": 5
                },
                {
                    "name": "Taco Bell",
                    "category": "Mexican",
                    "items_available": 12,
                    "secret_menu_items": 7
                },
                {
                    "name": "Burger King",
                    "category": "Burgers", 
                    "items_available": 8,
                    "secret_menu_items": 4
                },
                {
                    "name": "Subway",
                    "category": "Sandwiches",
                    "items_available": 6,
                    "secret_menu_items": 3
                }
            ]
            
            return {
                "success": True,
                "restaurants": restaurants,
                "total_items": sum(r["items_available"] for r in restaurants),
                "total_secret_items": sum(r["secret_menu_items"] for r in restaurants)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/recipes/fastfood/{restaurant}")
    async def get_fastfood_recipes_by_restaurant(
        restaurant: str,
        include_secret_menu: bool = Query(True, description="Include secret menu items")
    ):
        """Get fast food clone recipes for specific restaurant"""
        try:
            service = await get_enhanced_cooking_service(db)
            
            # Filter fast food database by restaurant
            restaurant_items = []
            for item in service.fastfood_database:
                if item.restaurant.lower() == restaurant.lower():
                    if include_secret_menu or not item.is_secret_menu:
                        restaurant_items.append({
                        "id": item.id,
                        "name": item.item_name,
                        "category": item.category,
                        "ingredients": item.ingredients,
                        "instructions": item.instructions,
                        "is_secret_menu": item.is_secret_menu,
                        "popularity_score": item.popularity_score
                    })
            
            return {
                "success": True,
                "restaurant": restaurant,
                "items": restaurant_items,
                "total_items": len(restaurant_items)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/recipes/secret-menu")
    async def get_all_secret_menu_items():
        """Get all secret menu items from various restaurants"""
        try:
            service = await get_enhanced_cooking_service(db)
            
            secret_items = []
            for item in service.fastfood_database:
                if item.is_secret_menu:
                    secret_items.append({
                        "id": item.id,
                        "restaurant": item.restaurant,
                        "name": item.item_name,
                        "category": item.category,
                        "ingredients": item.ingredients,
                        "instructions": item.instructions,
                        "popularity_score": item.popularity_score
                    })
            
            # Sort by popularity
            secret_items.sort(key=lambda x: x["popularity_score"], reverse=True)
            
            return {
                "success": True,
                "secret_menu_items": secret_items,
                "total_items": len(secret_items),
                "restaurants": list(set(item["restaurant"] for item in secret_items))
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/recipes/generate-ai")
    async def generate_ai_recipe_with_ingredients(
        current_user_id: str = Depends(get_current_user)
    ):
        """Generate AI-powered recipe using available ingredients"""
        try:
            service = await get_enhanced_cooking_service(db)
            
            # Get user's pantry
            pantry_result = await service.get_user_pantry(current_user_id)
            if not pantry_result["success"]:
                raise HTTPException(status_code=400, detail="No pantry found. Please add ingredients first.")
            
            ingredients = pantry_result["pantry"]["ingredients"]
            if len(ingredients) < 3:
                raise HTTPException(status_code=400, detail="Please add at least 3 ingredients for AI recipe generation.")
            
            # Generate AI recipe
            ai_recipes = await service._generate_ai_recipes(ingredients)
            
            return {
                "success": True,
                "ai_recipes": [recipe.dict() for recipe in ai_recipes],
                "ingredients_used": ingredients
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/stats")
    async def get_cooking_service_stats():
        """Get enhanced cooking service statistics"""
        try:
            service = await get_enhanced_cooking_service(db)
            
            stats = {
                "available_ingredients": len(service.basic_ingredients),
                "fastfood_items": len(service.fastfood_database),
                "secret_menu_items": len([item for item in service.fastfood_database if item.is_secret_menu]),
                "supported_restaurants": len(set(item.restaurant for item in service.fastfood_database)),
                "ingredient_categories": len(set(ing.category for ing in service.basic_ingredients)),
                "features": [
                    "SuperCook-style ingredient matching",
                    "HackTheMenu fast food clones",
                    "AI-powered recipe generation",
                    "Virtual pantry management",
                    "Secret menu items",
                    "Ingredient autocomplete"
                ]
            }
            
            return {
                "success": True,
                "stats": stats,
                "service_status": "Enhanced Smart Cooking Service Active"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router