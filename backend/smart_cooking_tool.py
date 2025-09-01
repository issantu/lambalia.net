# Smart Cooking Tool - Ingredient-Based Recipe Discovery
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from pydantic import BaseModel, Field
import uuid
import requests
import os
from emergentintegrations.llm.chat import LlmChat, UserMessage

class IngredientInput(BaseModel):
    """Model for user ingredient input"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    freshness: Optional[str] = "fresh"  # fresh, expiring, frozen
    dietary_restrictions: List[str] = []

class CookingPreferences(BaseModel):
    """User cooking preferences and constraints"""
    difficulty_level: str = "medium"  # easy, medium, hard
    cooking_time_max: int = 60  # minutes
    cuisine_preferences: List[str] = []
    dietary_restrictions: List[str] = []
    equipment_available: List[str] = []
    skill_level: str = "intermediate"  # beginner, intermediate, advanced

class SmartRecipeSuggestion(BaseModel):
    """Generated recipe suggestion from AI"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recipe_name: str
    cuisine_type: str
    difficulty_level: str
    preparation_time: int
    cooking_time: int
    servings: int
    
    # Recipe content
    description: str
    ingredients_used: List[str]  # From user's ingredients
    additional_ingredients: List[Dict[str, str]]  # Need to buy
    instructions: List[str]
    
    # Smart features
    ingredient_utilization_score: float  # How well it uses user's ingredients
    cultural_authenticity: Optional[str] = None
    dietary_compatibility: List[str] = []
    estimated_cost: float = 0.0
    
    # Nutritional info (optional)
    nutrition_info: Optional[Dict[str, Any]] = None
    
    # Monetization
    premium_features: List[str] = []  # Video tutorial, chef tips, etc.
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CookingToolSession(BaseModel):
    """User cooking session with ingredient management"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_name: Optional[str] = "My Kitchen"
    
    # Ingredients management
    available_ingredients: List[IngredientInput] = []
    preferences: CookingPreferences = Field(default_factory=CookingPreferences)
    
    # Generated suggestions
    recipe_suggestions: List[SmartRecipeSuggestion] = []
    
    # Payment and premium features
    premium_activated: bool = False
    payment_amount: float = 0.0
    
    # Session management
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class SmartCookingToolService:
    """AI-powered cooking tool service with monetization"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.llm_client = LlmChat()
        
        # Tool pricing
        self.basic_price = 2.99
        self.premium_price = 4.99
        
    async def create_cooking_session(self, user_id: str, session_name: str = None) -> CookingToolSession:
        """Create a new cooking tool session for a user"""
        
        session = CookingToolSession(
            user_id=user_id,
            session_name=session_name or f"Kitchen Session {datetime.now().strftime('%Y%m%d_%H%M')}"
        )
        
        await self.db.cooking_tool_sessions.insert_one(session.dict())
        
        self.logger.info(f"Created cooking session: {session.id} for user: {user_id}")
        return session
    
    async def add_ingredients_to_session(self, session_id: str, ingredients: List[IngredientInput]) -> Dict[str, Any]:
        """Add ingredients to user's virtual kitchen"""
        
        # Update session with new ingredients
        await self.db.cooking_tool_sessions.update_one(
            {"id": session_id},
            {
                "$push": {"available_ingredients": {"$each": [ing.dict() for ing in ingredients]}},
                "$set": {"last_accessed": datetime.utcnow()}
            }
        )
        
        return {
            "success": True,
            "ingredients_added": len(ingredients),
            "message": f"Added {len(ingredients)} ingredients to your kitchen"
        }
    
    async def generate_smart_recipes(self, session_id: str, preferences: CookingPreferences = None) -> List[SmartRecipeSuggestion]:
        """Generate AI-powered recipe suggestions based on available ingredients"""
        
        # Get session data
        session = await self.db.cooking_tool_sessions.find_one({"id": session_id}, {"_id": 0})
        if not session:
            raise ValueError("Session not found")
        
        session_obj = CookingToolSession(**session)
        
        if preferences:
            session_obj.preferences = preferences
            await self.db.cooking_tool_sessions.update_one(
                {"id": session_id},
                {"$set": {"preferences": preferences.dict()}}
            )
        
        # Generate AI-powered recipe suggestions
        recipe_suggestions = await self._generate_ai_recipes(session_obj)
        
        # Store suggestions in session
        await self.db.cooking_tool_sessions.update_one(
            {"id": session_id},
            {
                "$set": {
                    "recipe_suggestions": [recipe.dict() for recipe in recipe_suggestions],
                    "last_accessed": datetime.utcnow()
                }
            }
        )
        
        return recipe_suggestions
    
    async def _generate_ai_recipes(self, session: CookingToolSession) -> List[SmartRecipeSuggestion]:
        """Use AI to generate personalized recipe suggestions"""
        
        ingredients_list = [f"{ing.name} ({ing.quantity} {ing.unit})" if ing.quantity else ing.name 
                          for ing in session.available_ingredients]
        
        # Create AI prompt for recipe generation
        prompt = f"""
        As a professional chef and AI cooking assistant, analyze these available ingredients and generate 3 creative, practical recipes:

        AVAILABLE INGREDIENTS:
        {', '.join(ingredients_list)}

        USER PREFERENCES:
        - Difficulty: {session.preferences.difficulty_level}
        - Max cooking time: {session.preferences.cooking_time_max} minutes
        - Cuisine preferences: {', '.join(session.preferences.cuisine_preferences) if session.preferences.cuisine_preferences else 'Any'}
        - Dietary restrictions: {', '.join(session.preferences.dietary_restrictions) if session.preferences.dietary_restrictions else 'None'}
        - Skill level: {session.preferences.skill_level}

        For each recipe, provide:
        1. Recipe name and cuisine type
        2. Difficulty level and timing
        3. Which ingredients from the list to use
        4. Additional ingredients needed (if any)
        5. Step-by-step instructions
        6. Cultural authenticity notes
        7. Ingredient utilization score (0-1)

        Focus on maximizing the use of available ingredients while creating delicious, authentic dishes.
        Consider ingredient freshness and suggest using expiring items first.
        """
        
        try:
            # Use Emergent LLM for recipe generation
            response = await self.llm_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional chef and AI cooking assistant specialized in creating personalized recipes from available ingredients."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response and create recipe suggestions
            recipes = self._parse_ai_recipe_response(ai_response, session.available_ingredients)
            
            return recipes
            
        except Exception as e:
            self.logger.error(f"AI recipe generation failed: {e}")
            
            # Fallback to predefined recipes based on ingredients
            return await self._generate_fallback_recipes(session)
    
    def _parse_ai_recipe_response(self, ai_response: str, available_ingredients: List[IngredientInput]) -> List[SmartRecipeSuggestion]:
        """Parse AI response and create structured recipe suggestions"""
        
        recipes = []
        
        # This is a simplified parser - in production, would use more sophisticated NLP
        try:
            # Split response into recipe sections
            recipe_sections = ai_response.split('\n\n')
            
            for i, section in enumerate(recipe_sections[:3]):  # Limit to 3 recipes
                if len(section.strip()) < 50:  # Skip short sections
                    continue
                    
                # Extract recipe information (simplified extraction)
                lines = section.strip().split('\n')
                
                recipe = SmartRecipeSuggestion(
                    recipe_name=f"AI Suggested Recipe {i+1}",
                    cuisine_type="International",
                    difficulty_level="medium",
                    preparation_time=15,
                    cooking_time=30,
                    servings=4,
                    description=section[:200] + "...",
                    ingredients_used=[ing.name for ing in available_ingredients[:5]],
                    additional_ingredients=[
                        {"name": "Salt", "quantity": "to taste"},
                        {"name": "Black pepper", "quantity": "to taste"}
                    ],
                    instructions=[
                        "Prepare all ingredients as specified",
                        "Follow the cooking steps carefully",
                        "Season to taste",
                        "Serve hot and enjoy!"
                    ],
                    ingredient_utilization_score=0.8,
                    estimated_cost=12.50
                )
                
                recipes.append(recipe)
        
        except Exception as e:
            self.logger.error(f"Failed to parse AI response: {e}")
        
        return recipes if recipes else self._generate_fallback_recipes_simple()
    
    async def _generate_fallback_recipes(self, session: CookingToolSession) -> List[SmartRecipeSuggestion]:
        """Generate fallback recipes when AI fails"""
        
        ingredient_names = [ing.name.lower() for ing in session.available_ingredients]
        
        fallback_recipes = []
        
        # Recipe 1: Simple Stir Fry (if vegetables available)
        if any(veg in ' '.join(ingredient_names) for veg in ['tomato', 'onion', 'pepper', 'carrot', 'broccoli']):
            fallback_recipes.append(SmartRecipeSuggestion(
                recipe_name="Quick Vegetable Stir Fry",
                cuisine_type="Asian Fusion",
                difficulty_level="easy",
                preparation_time=10,
                cooking_time=15,
                servings=2,
                description="A quick and healthy stir fry using your available vegetables",
                ingredients_used=[ing.name for ing in session.available_ingredients if 'vegetable' in ing.name.lower() or any(v in ing.name.lower() for v in ['tomato', 'onion', 'pepper', 'carrot'])],
                additional_ingredients=[
                    {"name": "Soy sauce", "quantity": "2 tbsp"},
                    {"name": "Vegetable oil", "quantity": "1 tbsp"},
                    {"name": "Garlic", "quantity": "2 cloves"}
                ],
                instructions=[
                    "Heat oil in a large pan or wok",
                    "Add garlic and cook for 30 seconds",
                    "Add harder vegetables first (carrots, broccoli)",
                    "Add softer vegetables (tomatoes, peppers) after 3-4 minutes",
                    "Season with soy sauce and cook for 2-3 more minutes",
                    "Serve hot over rice or noodles"
                ],
                ingredient_utilization_score=0.9,
                estimated_cost=8.50
            ))
        
        # Recipe 2: Simple Pasta (if pasta ingredients available)
        if any(carb in ' '.join(ingredient_names) for carb in ['pasta', 'noodle', 'rice']):
            fallback_recipes.append(SmartRecipeSuggestion(
                recipe_name="Simple Pasta with Available Ingredients",
                cuisine_type="Italian Fusion",
                difficulty_level="easy",
                preparation_time=5,
                cooking_time=20,
                servings=3,
                description="A simple pasta dish made with your available ingredients",
                ingredients_used=[ing.name for ing in session.available_ingredients if any(c in ing.name.lower() for c in ['pasta', 'tomato', 'cheese', 'herb'])],
                additional_ingredients=[
                    {"name": "Olive oil", "quantity": "2 tbsp"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Black pepper", "quantity": "to taste"}
                ],
                instructions=[
                    "Boil pasta according to package directions",
                    "Heat olive oil in a large pan",
                    "Add available vegetables and cook until tender",
                    "Drain pasta and add to the pan",
                    "Toss with available cheese and herbs",
                    "Season with salt and pepper"
                ],
                ingredient_utilization_score=0.85,
                estimated_cost=10.00
            ))
        
        # Recipe 3: Simple Soup
        fallback_recipes.append(SmartRecipeSuggestion(
            recipe_name="Hearty Ingredient Soup",
            cuisine_type="Comfort Food",
            difficulty_level="easy",
            preparation_time=15,
            cooking_time=25,
            servings=4,
            description="A warming soup made with your available ingredients",
            ingredients_used=[ing.name for ing in session.available_ingredients[:6]],
            additional_ingredients=[
                {"name": "Vegetable broth", "quantity": "4 cups"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Herbs", "quantity": "to taste"}
            ],
            instructions=[
                "Chop all available vegetables into bite-sized pieces",
                "Heat a large pot and add a little oil",
                "Sauté onions and garlic if available",
                "Add harder vegetables first and cook for 5 minutes",
                "Add broth and bring to a boil",
                "Simmer for 15-20 minutes until vegetables are tender",
                "Season with salt, pepper, and available herbs"
            ],
            ingredient_utilization_score=0.95,
            estimated_cost=7.00
        ))
        
        return fallback_recipes[:2]  # Return up to 2 fallback recipes
    
    def _generate_fallback_recipes_simple(self) -> List[SmartRecipeSuggestion]:
        """Simple fallback when everything fails"""
        return [
            SmartRecipeSuggestion(
                recipe_name="Basic Scrambled Eggs",
                cuisine_type="Comfort Food",
                difficulty_level="easy",
                preparation_time=2,
                cooking_time=5,
                servings=1,
                description="Simple scrambled eggs - a cooking fundamental",
                ingredients_used=["Eggs"],
                additional_ingredients=[
                    {"name": "Butter", "quantity": "1 tbsp"},
                    {"name": "Salt", "quantity": "pinch"}
                ],
                instructions=[
                    "Crack eggs into a bowl and whisk",
                    "Heat butter in a non-stick pan",
                    "Add eggs and gently scramble",
                    "Season with salt and serve"
                ],
                ingredient_utilization_score=0.5,
                estimated_cost=3.00
            )
        ]