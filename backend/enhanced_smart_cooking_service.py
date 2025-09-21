# Enhanced Smart Cooking Service - SuperCook Style + HackTheMenu Integration
import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from enum import Enum

# Import the translation service for AI-powered recipe generation
from translation_service import get_translation_service

class IngredientCategory(str, Enum):
    PROTEINS = "proteins"
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    GRAINS = "grains"
    DAIRY = "dairy"
    SPICES = "spices"
    OILS = "oils"
    PANTRY = "pantry"
    BEVERAGES = "beverages"

class CuisineType(str, Enum):
    AMERICAN = "american"
    ITALIAN = "italian"
    MEXICAN = "mexican"
    ASIAN = "asian"
    INDIAN = "indian"
    MIDDLE_EASTERN = "middle_eastern"
    FAST_FOOD = "fast_food"
    COMFORT_FOOD = "comfort_food"

class RecipeComplexity(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class IngredientItem(BaseModel):
    name: str
    category: IngredientCategory
    common_names: List[str] = []
    storage_tips: Optional[str] = None

class RecipeMatch(BaseModel):
    id: str
    name: str
    cuisine_type: CuisineType
    complexity: RecipeComplexity
    prep_time: int  # minutes
    cook_time: int  # minutes
    servings: int
    ingredients_used: List[str]
    missing_ingredients: List[str] = []
    instructions: List[str]
    nutrition_info: Optional[Dict[str, Any]] = None
    source: str  # "supercook_clone", "hackthemenu", "lambalia_original"
    fast_food_restaurant: Optional[str] = None
    is_secret_menu: bool = False

class FastFoodItem(BaseModel):
    id: str
    restaurant: str
    item_name: str
    category: str
    ingredients: List[str]
    instructions: str
    price_range: Optional[str] = None
    is_secret_menu: bool = False
    popularity_score: int = 0

class EnhancedSmartCookingService:
    """
    Enhanced Smart Cooking Service with SuperCook-style ingredient matching
    and HackTheMenu fast food integration
    """
    
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        # Collections
        self.ingredients_collection = self.db.cooking_ingredients
        self.recipes_collection = self.db.enhanced_recipes
        self.fastfood_collection = self.db.fastfood_items
        self.user_pantries_collection = self.db.user_pantries
        self.cooking_sessions_collection = self.db.cooking_sessions
        
        # Initialize with basic ingredient database
        self.basic_ingredients = self._load_basic_ingredients()
        self.fastfood_database = self._load_fastfood_database()
        
    def _load_basic_ingredients(self) -> List[IngredientItem]:
        """Load comprehensive ingredient database similar to SuperCook"""
        return [
            # Proteins
            IngredientItem(name="chicken breast", category=IngredientCategory.PROTEINS, 
                         common_names=["chicken", "chicken fillet"], 
                         storage_tips="Refrigerate and use within 2-3 days"),
            IngredientItem(name="ground beef", category=IngredientCategory.PROTEINS,
                         common_names=["beef mince", "hamburger meat"]),
            IngredientItem(name="salmon", category=IngredientCategory.PROTEINS,
                         common_names=["salmon fillet", "fresh salmon"]),
            IngredientItem(name="eggs", category=IngredientCategory.PROTEINS,
                         common_names=["chicken eggs", "fresh eggs"]),
            IngredientItem(name="tofu", category=IngredientCategory.PROTEINS,
                         common_names=["bean curd", "soy tofu"]),
            
            # Vegetables
            IngredientItem(name="onion", category=IngredientCategory.VEGETABLES,
                         common_names=["yellow onion", "white onion"]),
            IngredientItem(name="garlic", category=IngredientCategory.VEGETABLES,
                         common_names=["garlic cloves", "fresh garlic"]),
            IngredientItem(name="tomato", category=IngredientCategory.VEGETABLES,
                         common_names=["fresh tomato", "tomatoes"]),
            IngredientItem(name="bell pepper", category=IngredientCategory.VEGETABLES,
                         common_names=["sweet pepper", "capsicum"]),
            IngredientItem(name="carrots", category=IngredientCategory.VEGETABLES,
                         common_names=["fresh carrots", "baby carrots"]),
            
            # Grains & Pantry
            IngredientItem(name="rice", category=IngredientCategory.GRAINS,
                         common_names=["white rice", "jasmine rice"]),
            IngredientItem(name="pasta", category=IngredientCategory.GRAINS,
                         common_names=["spaghetti", "penne", "macaroni"]),
            IngredientItem(name="bread", category=IngredientCategory.GRAINS,
                         common_names=["white bread", "whole wheat bread"]),
            IngredientItem(name="flour", category=IngredientCategory.PANTRY,
                         common_names=["all-purpose flour", "white flour"]),
            
            # Dairy
            IngredientItem(name="milk", category=IngredientCategory.DAIRY,
                         common_names=["whole milk", "2% milk"]),
            IngredientItem(name="cheese", category=IngredientCategory.DAIRY,
                         common_names=["cheddar cheese", "mozzarella"]),
            IngredientItem(name="butter", category=IngredientCategory.DAIRY,
                         common_names=["unsalted butter", "salted butter"]),
            
            # Spices (assumed basics like SuperCook)
            IngredientItem(name="salt", category=IngredientCategory.SPICES,
                         common_names=["table salt", "sea salt"]),
            IngredientItem(name="black pepper", category=IngredientCategory.SPICES,
                         common_names=["pepper", "ground pepper"]),
            IngredientItem(name="olive oil", category=IngredientCategory.OILS,
                         common_names=["extra virgin olive oil", "cooking oil"]),
        ]
    
    def _load_fastfood_database(self) -> List[FastFoodItem]:
        """Load HackTheMenu-style fast food database"""
        return [
            # McDonald's Items
            FastFoodItem(
                id="mcdonalds_big_mac_clone",
                restaurant="McDonald's",
                item_name="Homemade Big Mac",
                category="Burgers",
                ingredients=["ground beef", "lettuce", "onion", "pickle", "cheese", "bread", "mayonnaise", "ketchup"],
                instructions="Form beef patties, cook until done. Toast buns. Layer: sauce, lettuce, onion, patty, cheese, pickle. Assemble burger.",
                is_secret_menu=False
            ),
            FastFoodItem(
                id="mcdonalds_mcgriddle_clone",
                restaurant="McDonald's", 
                item_name="Homemade McGriddle",
                category="Breakfast",
                ingredients=["pancake mix", "maple syrup", "eggs", "cheese", "bacon"],
                instructions="Make pancake 'buns' with syrup mixed in. Cook eggs and bacon. Assemble sandwich.",
                is_secret_menu=False
            ),
            
            # KFC Items
            FastFoodItem(
                id="kfc_chicken_clone",
                restaurant="KFC",
                item_name="Copycat KFC Fried Chicken",
                category="Chicken", 
                ingredients=["chicken", "flour", "salt", "black pepper", "paprika", "garlic powder", "oil"],
                instructions="Season flour with spices. Coat chicken, fry until golden and cooked through.",
                is_secret_menu=False
            ),
            
            # Secret Menu Items
            FastFoodItem(
                id="mcdonalds_land_sea_air",
                restaurant="McDonald's",
                item_name="Land, Sea & Air Burger (Secret)",
                category="Secret Menu",
                ingredients=["ground beef", "chicken breast", "fish fillet", "cheese", "lettuce", "bread"],
                instructions="Order a Big Mac, add chicken patty and fish fillet. Stack all proteins together.",
                is_secret_menu=True,
                popularity_score=85
            ),
            
            # Taco Bell
            FastFoodItem(
                id="tacobell_quesadilla_hack",
                restaurant="Taco Bell", 
                item_name="Copycat Crunchwrap",
                category="Mexican",
                ingredients=["large tortilla", "ground beef", "cheese", "lettuce", "tomato", "sour cream", "taco shell"],
                instructions="Layer beef, cheese, and crushed taco shell in center of tortilla. Add toppings, fold edges, cook until crispy.",
                is_secret_menu=False
            )
        ]
    
    async def create_user_pantry(self, user_id: str, pantry_name: str = "My Pantry") -> Dict[str, Any]:
        """Create a user's virtual pantry similar to SuperCook"""
        try:
            pantry = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "name": pantry_name,
                "ingredients": [],
                "excluded_ingredients": [],
                "dietary_preferences": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            await self.user_pantries_collection.insert_one(pantry)
            
            return {
                "success": True,
                "pantry_id": pantry["id"],
                "message": "Virtual pantry created successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create pantry: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def add_ingredients_to_pantry(self, user_id: str, ingredients: List[str]) -> Dict[str, Any]:
        """Add ingredients to user's pantry"""
        try:
            # Find user's pantry
            pantry = await self.user_pantries_collection.find_one({"user_id": user_id})
            
            if not pantry:
                # Create default pantry
                result = await self.create_user_pantry(user_id)
                if not result["success"]:
                    return result
                pantry = await self.user_pantries_collection.find_one({"user_id": user_id})
            
            # Add ingredients (avoid duplicates)
            current_ingredients = set(pantry.get("ingredients", []))
            new_ingredients = [ing.lower().strip() for ing in ingredients]
            updated_ingredients = list(current_ingredients.union(set(new_ingredients)))
            
            await self.user_pantries_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "ingredients": updated_ingredients,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return {
                "success": True,
                "ingredients_added": len(new_ingredients),
                "total_ingredients": len(updated_ingredients)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add ingredients: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def find_recipes_by_ingredients(self, user_id: str, max_missing: int = 0) -> Dict[str, Any]:
        """
        Find recipes based on available ingredients - SuperCook style
        max_missing: 0 = only recipes with all ingredients, 1+ = allow missing ingredients
        """
        try:
            # Get user's pantry
            pantry = await self.user_pantries_collection.find_one({"user_id": user_id})
            if not pantry:
                return {"success": False, "error": "No pantry found. Please add ingredients first."}
            
            available_ingredients = set([ing.lower() for ing in pantry.get("ingredients", [])])
            excluded_ingredients = set([ing.lower() for ing in pantry.get("excluded_ingredients", [])])
            
            # Basic recipes from ingredients
            ingredient_based_recipes = await self._generate_ingredient_based_recipes(available_ingredients)
            
            # Fast food clones
            fastfood_matches = self._match_fastfood_recipes(available_ingredients, max_missing)
            
            # AI-generated recipes using available ingredients
            ai_recipes = await self._generate_ai_recipes(list(available_ingredients))
            
            all_recipes = ingredient_based_recipes + fastfood_matches + ai_recipes
            
            # Filter by missing ingredients
            filtered_recipes = []
            for recipe in all_recipes:
                recipe_ingredients = set([ing.lower() for ing in recipe.ingredients_used])
                missing = recipe_ingredients - available_ingredients
                
                # Remove excluded ingredients
                if any(exc in recipe_ingredients for exc in excluded_ingredients):
                    continue
                
                if len(missing) <= max_missing:
                    recipe.missing_ingredients = list(missing)
                    filtered_recipes.append(recipe)
            
            # Sort by completeness (fewer missing ingredients first)
            filtered_recipes.sort(key=lambda x: len(x.missing_ingredients))
            
            return {
                "success": True,
                "recipes": [recipe.dict() for recipe in filtered_recipes[:20]],  # Limit to 20
                "total_found": len(filtered_recipes),
                "ingredients_used": list(available_ingredients),
                "max_missing_allowed": max_missing
            }
            
        except Exception as e:
            self.logger.error(f"Recipe search failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _generate_ingredient_based_recipes(self, ingredients: set) -> List[RecipeMatch]:
        """Generate basic recipes based on ingredient combinations"""
        recipes = []
        
        # Simple pattern matching for common recipes
        if {"eggs", "milk", "flour"}.issubset(ingredients):
            recipes.append(RecipeMatch(
                id="basic_pancakes",
                name="Basic Pancakes",
                cuisine_type=CuisineType.AMERICAN,
                complexity=RecipeComplexity.BEGINNER,
                prep_time=10,
                cook_time=15,
                servings=4,
                ingredients_used=["eggs", "milk", "flour", "salt"],
                instructions=[
                    "Mix dry ingredients in bowl",
                    "Whisk eggs and milk separately", 
                    "Combine wet and dry ingredients",
                    "Cook on hot griddle until bubbles form",
                    "Flip and cook until golden"
                ],
                source="supercook_clone"
            ))
        
        if {"chicken", "rice", "onion"}.issubset(ingredients):
            recipes.append(RecipeMatch(
                id="chicken_rice_bowl",
                name="Simple Chicken Rice Bowl",
                cuisine_type=CuisineType.ASIAN,
                complexity=RecipeComplexity.BEGINNER,
                prep_time=15,
                cook_time=25,
                servings=2,
                ingredients_used=["chicken", "rice", "onion", "garlic", "oil"],
                instructions=[
                    "Cook rice according to package directions",
                    "Season and cook chicken until done",
                    "Sauté onions and garlic",
                    "Serve chicken over rice with vegetables"
                ], 
                source="supercook_clone"
            ))
        
        if {"pasta", "tomato", "cheese"}.issubset(ingredients):
            recipes.append(RecipeMatch(
                id="simple_pasta",
                name="Basic Pasta with Tomato and Cheese",
                cuisine_type=CuisineType.ITALIAN,
                complexity=RecipeComplexity.BEGINNER,
                prep_time=5,
                cook_time=15,
                servings=2,
                ingredients_used=["pasta", "tomato", "cheese", "garlic", "olive oil"],
                instructions=[
                    "Cook pasta according to package directions",
                    "Sauté garlic in olive oil",
                    "Add diced tomatoes and cook until soft",
                    "Toss pasta with tomato sauce",
                    "Top with cheese and serve"
                ],
                source="supercook_clone"
            ))
        
        return recipes
    
    def _match_fastfood_recipes(self, ingredients: set, max_missing: int) -> List[RecipeMatch]:
        """Match ingredients to fast food clone recipes"""
        matches = []
        
        for item in self.fastfood_database:
            item_ingredients = set([ing.lower() for ing in item.ingredients])
            missing = item_ingredients - ingredients
            
            if len(missing) <= max_missing:
                recipe = RecipeMatch(
                    id=item.id,
                    name=item.item_name,
                    cuisine_type=CuisineType.FAST_FOOD,
                    complexity=RecipeComplexity.INTERMEDIATE,
                    prep_time=15,
                    cook_time=20,
                    servings=1,
                    ingredients_used=item.ingredients,
                    missing_ingredients=list(missing),
                    instructions=item.instructions.split(". "),
                    source="hackthemenu",
                    fast_food_restaurant=item.restaurant,
                    is_secret_menu=item.is_secret_menu
                )
                matches.append(recipe)
        
        return matches
    
    async def _generate_ai_recipes(self, ingredients: List[str]) -> List[RecipeMatch]:
        """Use AI to generate creative recipes with available ingredients"""
        try:
            translation_service = await get_translation_service()
            
            # Create prompt for AI recipe generation
            ingredients_text = ", ".join(ingredients)
            prompt = f"""
            Create a unique, delicious recipe using these available ingredients: {ingredients_text}
            
            Please provide:
            1. Recipe name
            2. Cuisine type
            3. Prep time and cook time
            4. Step-by-step instructions
            5. Number of servings
            
            Focus on creating something practical and tasty that uses most of the available ingredients.
            """
            
            # Use translation service's AI capabilities
            ai_response = await translation_service.translate_text(
                text=prompt,
                target_language="en",  # Keep in English but use AI processing
                preserve_cultural_context=False
            )
            
            # Parse AI response into recipe format (simplified for MVP)
            if ai_response.get("success"):
                recipe_text = ai_response.get("translated_text", "")
                
                # Basic parsing (in production, would use more sophisticated parsing)
                recipe = RecipeMatch(
                    id=f"ai_recipe_{uuid.uuid4().hex[:8]}",
                    name="AI-Generated Recipe",
                    cuisine_type=CuisineType.COMFORT_FOOD,
                    complexity=RecipeComplexity.INTERMEDIATE,
                    prep_time=20,
                    cook_time=30,
                    servings=4,
                    ingredients_used=ingredients,
                    instructions=recipe_text.split("\n")[:10],  # Basic instruction extraction
                    source="lambalia_ai"
                )
                return [recipe]
            
        except Exception as e:
            self.logger.error(f"AI recipe generation failed: {str(e)}")
        
        return []
    
    async def get_ingredient_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """Get ingredient suggestions for autocomplete - SuperCook style"""
        try:
            query = query.lower().strip()
            suggestions = []
            
            for ingredient in self.basic_ingredients:
                # Match name or common names
                if (query in ingredient.name.lower() or 
                    any(query in name.lower() for name in ingredient.common_names)):
                    suggestions.append({
                        "name": ingredient.name,
                        "category": ingredient.category,
                        "common_names": ingredient.common_names,
                        "storage_tips": ingredient.storage_tips
                    })
            
            return suggestions[:10]  # Limit to 10 suggestions
            
        except Exception as e:
            self.logger.error(f"Ingredient suggestions failed: {str(e)}")
            return []
    
    async def get_user_pantry(self, user_id: str) -> Dict[str, Any]:
        """Get user's current pantry contents"""
        try:
            pantry = await self.user_pantries_collection.find_one({"user_id": user_id})
            
            if not pantry:
                return {
                    "success": False,
                    "error": "No pantry found",
                    "suggestion": "Add some ingredients to get started!"
                }
            
            return {
                "success": True,
                "pantry": {
                    "id": pantry["id"],
                    "name": pantry["name"],
                    "ingredients": pantry.get("ingredients", []),
                    "excluded_ingredients": pantry.get("excluded_ingredients", []),
                    "ingredient_count": len(pantry.get("ingredients", [])),
                    "last_updated": pantry.get("updated_at")
                }
            }
            
        except Exception as e:
            self.logger.error(f"Get pantry failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def remove_ingredients_from_pantry(self, user_id: str, ingredients: List[str]) -> Dict[str, Any]:
        """Remove ingredients from user's pantry"""
        try:
            ingredients_to_remove = set([ing.lower().strip() for ing in ingredients])
            
            result = await self.user_pantries_collection.update_one(
                {"user_id": user_id},
                {
                    "$pull": {"ingredients": {"$in": list(ingredients_to_remove)}},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                return {
                    "success": True,
                    "message": f"Removed {len(ingredients_to_remove)} ingredients"
                }
            else:
                return {
                    "success": False,
                    "error": "No ingredients were removed"
                }
                
        except Exception as e:
            self.logger.error(f"Remove ingredients failed: {str(e)}")
            return {"success": False, "error": str(e)}

# Global service instance
enhanced_cooking_service = None

async def get_enhanced_cooking_service(db) -> EnhancedSmartCookingService:
    """Get or create enhanced cooking service instance"""
    global enhanced_cooking_service
    if enhanced_cooking_service is None:
        enhanced_cooking_service = EnhancedSmartCookingService(db)
    return enhanced_cooking_service