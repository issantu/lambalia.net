# Reference recipes database for Lambalia
import uuid
from datetime import datetime
from models_extension import ReferenceRecipe

# Major traditional recipes by country/region
REFERENCE_RECIPES = [
    # Italian Recipes
    ReferenceRecipe(
        name_english="Pasta Carbonara",
        name_local="Pasta alla Carbonara",
        local_language="Italian",
        country_id="italy",
        description="Classic Roman pasta dish with eggs, cheese, and guanciale",
        category="main",
        difficulty_level=3,
        estimated_time=25,
        serving_size="4 portions",
        key_ingredients=["spaghetti", "guanciale", "eggs", "pecorino romano", "black pepper"],
        cultural_significance="Traditional Roman dish, simple but requires technique to avoid scrambling eggs",
        is_featured=True,
        popularity_score=95
    ),
    ReferenceRecipe(
        name_english="Risotto Milanese",
        name_local="Risotto alla Milanese",
        local_language="Italian",
        country_id="italy",
        description="Creamy rice dish with saffron from Milan",
        category="main",
        difficulty_level=4,
        estimated_time=45,
        serving_size="4-6 portions",
        key_ingredients=["arborio rice", "saffron", "beef broth", "white wine", "parmigiano"],
        cultural_significance="Symbol of Lombard cuisine, traditionally served with osso buco",
        is_featured=True,
        popularity_score=88
    ),
    
    # French Recipes
    ReferenceRecipe(
        name_english="Beef Bourguignon",
        name_local="Bœuf Bourguignon",
        local_language="French",
        country_id="france",
        description="Slow-braised beef in red wine from Burgundy region",
        category="main",
        difficulty_level=4,
        estimated_time=180,
        serving_size="6-8 portions",
        key_ingredients=["beef chuck", "red wine", "bacon", "mushrooms", "pearl onions"],
        cultural_significance="Classic Burgundian dish, symbol of French countryside cooking",
        is_featured=True,
        popularity_score=92
    ),
    ReferenceRecipe(
        name_english="French Onion Soup",
        name_local="Soupe à l'Oignon Gratinée",
        local_language="French",
        country_id="france",
        description="Rich onion soup topped with cheese and bread",
        category="appetizer",
        difficulty_level=2,
        estimated_time=60,
        serving_size="4 portions",
        key_ingredients=["yellow onions", "beef broth", "gruyere cheese", "baguette", "white wine"],
        cultural_significance="Parisian bistro classic, traditionally eaten late at night",
        is_featured=True,
        popularity_score=85
    ),
    
    # Mexican Recipes
    ReferenceRecipe(
        name_english="Mole Poblano",
        name_local="Mole Poblano",
        local_language="Spanish",
        country_id="mexico",
        description="Complex sauce with chocolate and chiles from Puebla",
        category="main",
        difficulty_level=5,
        estimated_time=240,
        serving_size="8-10 portions",
        key_ingredients=["dried chiles", "chocolate", "turkey", "sesame seeds", "spices"],
        cultural_significance="National dish of Mexico, represents fusion of indigenous and Spanish cultures",
        is_featured=True,
        popularity_score=94
    ),
    ReferenceRecipe(
        name_english="Street Tacos",
        name_local="Tacos de la Calle",
        local_language="Spanish",
        country_id="mexico",
        description="Authentic street-style tacos with various fillings",
        category="main",
        difficulty_level=2,
        estimated_time=30,
        serving_size="4-6 portions",
        key_ingredients=["corn tortillas", "meat (al pastor, carnitas, carne asada)", "onion", "cilantro", "lime"],
        cultural_significance="Heart of Mexican street food culture, varies by region",
        is_featured=True,
        popularity_score=96
    ),
    
    # Indian Recipes
    ReferenceRecipe(
        name_english="Butter Chicken",
        name_local="Murgh Makhani",
        local_language="Hindi",
        country_id="india",
        description="Creamy tomato-based chicken curry from Delhi",
        category="main",
        difficulty_level=3,
        estimated_time=60,
        serving_size="4-6 portions",
        key_ingredients=["chicken", "tomatoes", "cream", "garam masala", "fenugreek"],
        cultural_significance="Modern Indian classic, invented in Delhi in the 1950s",
        is_featured=True,
        popularity_score=91
    ),
    ReferenceRecipe(
        name_english="Biryani",
        name_local="बिरयानी",
        local_language="Hindi",
        country_id="india",
        description="Fragrant rice dish with meat and spices",
        category="main",
        difficulty_level=5,
        estimated_time=120,
        serving_size="6-8 portions",
        key_ingredients=["basmati rice", "meat", "saffron", "yogurt", "fried onions"],
        cultural_significance="Royal Mughal dish, varies significantly by region",
        is_featured=True,
        popularity_score=93
    ),
    
    # Japanese Recipes
    ReferenceRecipe(
        name_english="Ramen",
        name_local="ラーメン",
        local_language="Japanese",
        country_id="japan",
        description="Japanese noodle soup with various regional styles",
        category="main",
        difficulty_level=4,
        estimated_time=180,
        serving_size="2-4 portions",
        key_ingredients=["ramen noodles", "pork bones", "miso or soy sauce", "green onions", "egg"],
        cultural_significance="Adapted from Chinese noodles, now essential Japanese comfort food",
        is_featured=True,
        popularity_score=89
    ),
    ReferenceRecipe(
        name_english="Sushi",
        name_local="寿司",
        local_language="Japanese",
        country_id="japan",
        description="Vinegared rice with fish and other ingredients",
        category="main",
        difficulty_level=5,
        estimated_time=90,
        serving_size="2-4 portions",
        key_ingredients=["sushi rice", "raw fish", "nori", "wasabi", "soy sauce"],
        cultural_significance="Ancient preservation method evolved into haute cuisine",
        is_featured=True,
        popularity_score=97
    ),
    
    # Thai Recipes
    ReferenceRecipe(
        name_english="Pad Thai",
        name_local="ผัดไทย",
        local_language="Thai",
        country_id="thailand",
        description="Stir-fried noodles with tamarind and fish sauce",
        category="main",
        difficulty_level=3,
        estimated_time=30,
        serving_size="2-3 portions",
        key_ingredients=["rice noodles", "tamarind paste", "fish sauce", "eggs", "bean sprouts"],
        cultural_significance="National dish of Thailand, balance of sweet, sour, and salty",
        is_featured=True,
        popularity_score=90
    ),
    ReferenceRecipe(
        name_english="Green Curry",
        name_local="แกงเขียวหวาน",
        local_language="Thai",
        country_id="thailand",
        description="Spicy coconut curry with green chilies",
        category="main",
        difficulty_level=3,
        estimated_time=45,
        serving_size="4 portions",
        key_ingredients=["green curry paste", "coconut milk", "thai basil", "fish sauce", "palm sugar"],
        cultural_significance="Central Thai curry, represents balance of flavors in Thai cuisine",
        is_featured=True,
        popularity_score=87
    ),
    
    # Chinese Recipes
    ReferenceRecipe(
        name_english="Kung Pao Chicken",
        name_local="宫保鸡丁",
        local_language="Chinese",
        country_id="china",
        description="Spicy stir-fried chicken with peanuts from Sichuan",
        category="main",
        difficulty_level=3,
        estimated_time=25,
        serving_size="3-4 portions",
        key_ingredients=["chicken", "peanuts", "dried chilies", "sichuan peppercorns", "black vinegar"],
        cultural_significance="Classic Sichuan dish with sweet, sour, and spicy flavors",
        is_featured=True,
        popularity_score=88
    ),
    
    # Lebanese Recipes
    ReferenceRecipe(
        name_english="Hummus",
        name_local="حُمُّص",
        local_language="Arabic",
        country_id="lebanon",
        description="Creamy chickpea dip with tahini",
        category="appetizer",
        difficulty_level=2,
        estimated_time=15,
        serving_size="4-6 portions",
        key_ingredients=["chickpeas", "tahini", "lemon juice", "garlic", "olive oil"],
        cultural_significance="Ancient Levantine dish, symbol of Middle Eastern cuisine",
        is_featured=True,
        popularity_score=86
    ),
    
    # Greek Recipes
    ReferenceRecipe(
        name_english="Moussaka",
        name_local="Μουσακάς",
        local_language="Greek",
        country_id="greece",
        description="Layered casserole with eggplant and meat sauce",
        category="main",
        difficulty_level=4,
        estimated_time=120,
        serving_size="6-8 portions",
        key_ingredients=["eggplant", "ground lamb", "bechamel sauce", "tomatoes", "cheese"],
        cultural_significance="National dish of Greece, comfort food for celebrations",
        is_featured=True,
        popularity_score=84
    ),
    
    # Spanish Recipes
    ReferenceRecipe(
        name_english="Paella",
        name_local="Paella",
        local_language="Spanish",
        country_id="spain",
        description="Saffron rice dish with seafood or meat from Valencia",
        category="main",
        difficulty_level=4,
        estimated_time=75,
        serving_size="6-8 portions",
        key_ingredients=["bomba rice", "saffron", "seafood/chicken", "green beans", "garrofón beans"],
        cultural_significance="Symbol of Valencian cuisine, traditionally cooked outdoors",
        is_featured=True,
        popularity_score=92
    )
]

def get_recipes_by_country(country_id: str):
    """Get reference recipes for a specific country"""
    return [recipe for recipe in REFERENCE_RECIPES if recipe.country_id == country_id]

def get_featured_recipes():
    """Get featured reference recipes"""
    return [recipe for recipe in REFERENCE_RECIPES if recipe.is_featured]

def get_recipe_by_id(recipe_id: str):
    """Get a specific reference recipe by ID"""
    return next((recipe for recipe in REFERENCE_RECIPES if recipe.id == recipe_id), None)