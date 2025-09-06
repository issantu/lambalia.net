# Smart Cooking Tool API Routes
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from smart_cooking_tool import (
    SmartCookingToolService, IngredientInput, CookingPreferences, 
    SmartRecipeSuggestion, CookingToolSession
)

def create_smart_cooking_router(cooking_service: SmartCookingToolService, get_current_user, get_current_user_optional):
    """Create Smart Cooking Tool API router with dependency injection"""
    
    router = APIRouter(prefix="/smart-cooking", tags=["Smart Cooking Tool"])
    
    # COOKING SESSION MANAGEMENT
    
    @router.post("/session/create", response_model=dict)
    async def create_cooking_session(
        session_name: Optional[str] = None,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Create a new smart cooking session"""
        try:
            if not current_user_id:
                current_user_id = f"guest_{str(uuid.uuid4())[:8]}"
            
            session = await cooking_service.create_cooking_session(current_user_id, session_name)
            
            return {
                "success": True,
                "session_id": session.id,
                "session_name": session.session_name,
                "message": "Cooking session created! Start adding your ingredients.",
                "pricing": {
                    "basic_features": f"${cooking_service.basic_price}",
                    "premium_features": f"${cooking_service.premium_price}",
                    "trial_recipes": 1  # Free trial
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/sessions", response_model=dict)
    async def get_user_cooking_sessions(current_user_id: str = Depends(get_current_user)):
        """Get all cooking sessions for the current user"""
        try:
            sessions = await cooking_service.get_user_sessions(current_user_id)
            
            return {
                "success": True,
                "sessions": sessions,
                "total_sessions": len(sessions)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # INGREDIENT MANAGEMENT
    
    @router.post("/session/{session_id}/ingredients", response_model=dict)
    async def add_ingredients_to_session(
        session_id: str,
        ingredients_data: List[dict]
    ):
        """Add ingredients to a cooking session"""
        try:
            # Convert dict to IngredientInput objects
            ingredients = []
            for ing_data in ingredients_data:
                ingredient = IngredientInput(
                    name=ing_data["name"],
                    quantity=ing_data.get("quantity"),
                    unit=ing_data.get("unit"),
                    freshness=ing_data.get("freshness", "fresh"),
                    dietary_restrictions=ing_data.get("dietary_restrictions", [])
                )
                ingredients.append(ingredient)
            
            result = await cooking_service.add_ingredients_to_session(session_id, ingredients)
            
            return {
                **result,
                "next_step": "Set your cooking preferences and generate AI recipes!",
                "tip": "The more ingredients you add, the better recipe suggestions you'll get."
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # AI RECIPE GENERATION
    
    @router.post("/session/{session_id}/generate-recipes", response_model=dict)
    async def generate_smart_recipes(
        session_id: str,
        preferences: Optional[dict] = None
    ):
        """Generate AI-powered recipe suggestions based on available ingredients"""
        try:
            # Convert preferences if provided
            cooking_prefs = None
            if preferences:
                cooking_prefs = CookingPreferences(
                    difficulty_level=preferences.get("difficulty_level", "medium"),
                    cooking_time_max=preferences.get("cooking_time_max", 60),
                    cuisine_preferences=preferences.get("cuisine_preferences", []),
                    dietary_restrictions=preferences.get("dietary_restrictions", []),
                    equipment_available=preferences.get("equipment_available", []),
                    skill_level=preferences.get("skill_level", "intermediate")
                )
            
            recipes = await cooking_service.generate_smart_recipes(session_id, cooking_prefs)
            
            return {
                "success": True,
                "recipes": [recipe.dict() for recipe in recipes],
                "total_recipes": len(recipes),
                "ai_powered": True,
                "message": f"Generated {len(recipes)} personalized recipes using AI!",
                "premium_upgrade": {
                    "available": True,
                    "features": [
                        "Video cooking tutorials",
                        "Professional chef tips", 
                        "Nutritional analysis",
                        "Wine pairing suggestions"
                    ],
                    "pricing": {
                        "basic": f"${cooking_service.basic_price}",
                        "premium": f"${cooking_service.premium_price}"
                    }
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # PREMIUM FEATURES & MONETIZATION
    
    @router.post("/session/{session_id}/activate-premium", response_model=dict)
    async def activate_premium_features(
        session_id: str,
        payment_data: dict
    ):
        """Activate premium cooking features"""
        try:
            payment_amount = payment_data.get("amount", 0.0)
            payment_method = payment_data.get("method", "stripe")
            
            # In production, integrate with actual payment processor
            if payment_amount < cooking_service.basic_price:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Minimum payment required: ${cooking_service.basic_price}"
                )
            
            result = await cooking_service.activate_premium_features(session_id, payment_amount)
            
            return {
                **result,
                "payment_processed": True,
                "access_level": result.get("feature_level"),
                "thank_you": "Thank you for supporting Lambalia's AI cooking assistant!"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # COMPETITOR ANALYSIS & FEATURES
    
    @router.get("/competitor-analysis", response_model=dict)
    async def get_competitor_analysis():
        """Get analysis of competitor cooking apps and our advantages"""
        try:
            analysis = await cooking_service.get_competitor_analysis()
            
            return {
                "success": True,
                "analysis": analysis,
                "lambalia_advantages": [
                    "AI-powered personalized recipe generation",
                    "Cultural authenticity from 80+ global communities", 
                    "Smart ingredient utilization scoring",
                    "Integration with ethnic grocery store network",
                    "Fair pricing with significant value",
                    "Community-driven authentic recipes"
                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # UTILITY ENDPOINTS
    
    @router.get("/pricing", response_model=dict)
    async def get_pricing_info():
        """Get current pricing for smart cooking features"""
        return {
            "success": True,
            "pricing_tiers": {
                "trial": {
                    "price": "$0.00",
                    "features": ["1 AI recipe generation", "Basic ingredients management"],
                    "limitations": "Limited to 1 recipe per session"
                },
                "basic": {
                    "price": f"${cooking_service.basic_price}",
                    "features": [
                        "Unlimited AI recipe generation",
                        "Advanced ingredient management",
                        "Step-by-step cooking instructions",
                        "Basic nutritional info",
                        "Cooking timer integration"
                    ],
                    "best_for": "Home cooks who want AI assistance"
                },
                "premium": {
                    "price": f"${cooking_service.premium_price}",
                    "features": [
                        "Everything in Basic",
                        "Video cooking tutorials",
                        "Professional chef tips",
                        "Advanced nutritional analysis",
                        "Wine pairing suggestions",
                        "Cultural authenticity verification",
                        "Advanced cooking techniques"
                    ],
                    "best_for": "Serious cooking enthusiasts",
                    "popular": True
                }
            },
            "competitive_comparison": {
                "paprika": "$4.99 one-time (no AI)",
                "yummly": "$2.99/month (limited AI)",
                "supercook": "Free (basic features only)",
                "mealime": "$5.99/month (meal planning focus)",
                "lambalia": f"${cooking_service.basic_price}-${cooking_service.premium_price} (advanced AI + cultural authenticity)"
            }
        }
    
    @router.delete("/session/{session_id}", response_model=dict)
    async def delete_cooking_session(
        session_id: str,
        current_user_id: str = Depends(get_current_user)
    ):
        """Delete a cooking session"""
        try:
            result = await cooking_service.delete_session(session_id, current_user_id)
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # RECIPE SHARING & INTEGRATION
    
    @router.post("/session/{session_id}/recipe/{recipe_id}/share", response_model=dict)
    async def share_ai_recipe(
        session_id: str,
        recipe_id: str,
        share_data: dict,
        current_user_id: str = Depends(get_current_user_optional)
    ):
        """Share an AI-generated recipe with the Lambalia community"""
        try:
            # Integration with main Lambalia recipe sharing system
            recipe_title = share_data.get("title", "AI Generated Recipe")
            recipe_description = share_data.get("description", "")
            make_public = share_data.get("public", False)
            
            # In production, integrate with main recipe database
            shared_recipe_id = str(uuid.uuid4())
            
            return {
                "success": True,
                "shared_recipe_id": shared_recipe_id,
                "message": "Recipe shared with Lambalia community!",
                "url": f"/recipes/{shared_recipe_id}",
                "earnings_potential": "Others can pay for detailed instructions and tips",
                "community_impact": "Your AI-enhanced recipe can help other home cooks"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/session/{session_id}/grocery-list", response_model=dict)
    async def generate_grocery_list(session_id: str):
        """Generate grocery shopping list based on recipe suggestions"""
        try:
            # Get session data
            session_data = await cooking_service.db.cooking_tool_sessions.find_one(
                {"id": session_id}, {"_id": 0}
            )
            
            if not session_data:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Extract additional ingredients needed
            grocery_items = []
            estimated_cost = 0.0
            
            for recipe in session_data.get("recipe_suggestions", []):
                for ingredient in recipe.get("additional_ingredients", []):
                    grocery_items.append({
                        "name": ingredient["name"],
                        "quantity": ingredient.get("quantity", "as needed"),
                        "estimated_price": 2.50,  # Mock pricing
                        "recipe": recipe["recipe_name"]
                    })
                    estimated_cost += 2.50
            
            return {
                "success": True,
                "grocery_list": grocery_items,
                "total_items": len(grocery_items),
                "estimated_cost": estimated_cost,
                "store_integration": {
                    "available": True,
                    "supported_stores": ["H-Mart", "Whole Foods", "Walmart", "Local stores"],
                    "feature": "Integration with Lambalia's ethnic grocery network"
                },
                "savings_tip": "Use Lambalia's grocery partnerships for 5-15% discounts on specialty ingredients"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router