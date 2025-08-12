# Expanded Reference Recipes Database for Lambalia
import uuid
from datetime import datetime
from models_extension import ReferenceRecipe

# Native recipes organized by country
NATIVE_RECIPES_BY_COUNTRY = {
    "Italy": [
        "Margherita Pizza", "Lasagna", "Risotto alla Milanese", "Tiramisu", "Osso Buco",
        "Pasta Carbonara", "Pesto Genovese", "Focaccia", "Panettone", "Other"
    ],
    "Japan": [
        "Sushi", "Ramen", "Tempura", "Okonomiyaki", "Sashimi",
        "Udon", "Kaiseki", "Tonkatsu", "Miso Soup", "Other"
    ],
    "Mexico": [
        "Tacos", "Chiles en Nogada", "Pozole", "Mole Poblano", "Tamales",
        "Quesadillas", "Guacamole", "Enchiladas", "Carnitas", "Other"
    ],
    "India": [
        "Butter Chicken", "Biryani", "Masala Dosa", "Paneer Tikka", "Chole Bhature",
        "Rogan Josh", "Tandoori Chicken", "Samosa", "Dal Makhani", "Other"
    ],
    "France": [
        "Coq au Vin", "Bouillabaisse", "Ratatouille", "Crêpes", "Quiche Lorraine",
        "Boeuf Bourguignon", "Soufflé", "Croissant", "Tarte Tatin", "Other"
    ],
    "China": [
        "Peking Duck", "Kung Pao Chicken", "Dim Sum", "Sweet and Sour Pork", "Ma Po Tofu",
        "Chow Mein", "Spring Rolls", "Hot Pot", "Fried Rice", "Other"
    ],
    "Thailand": [
        "Pad Thai", "Tom Yum Soup", "Green Curry", "Massaman Curry", "Som Tum",
        "Mango Sticky Rice", "Panang Curry", "Larb", "Khao Pad", "Other"
    ],
    "Spain": [
        "Paella", "Gazpacho", "Tortilla Española", "Churros", "Jamón Ibérico",
        "Patatas Bravas", "Pulpo a la Gallega", "Fabada Asturiana", "Croquetas", "Other"
    ],
    "Greece": [
        "Moussaka", "Souvlaki", "Tzatziki", "Spanakopita", "Dolmades",
        "Baklava", "Greek Salad", "Kleftiko", "Pastitsio", "Other"
    ],
    "Lebanon": [
        "Tabbouleh", "Kibbeh", "Hummus", "Falafel", "Manakish",
        "Fattoush", "Shawarma", "Baba Ghanoush", "Kafta", "Other"
    ],
    "Morocco": [
        "Tagine", "Couscous", "Harira", "Bastilla", "Mechoui",
        "Rfissa", "Zaalouk", "Pastilla", "Msemen", "Other"
    ],
    "Brazil": [
        "Feijoada", "Pão de Queijo", "Moqueca", "Brigadeiro", "Coxinha",
        "Churrasco", "Vatapá", "Acarajé", "Tapioca", "Other"
    ],
    "Turkey": [
        "Kebabs", "Baklava", "Meze", "Lahmacun", "Pide",
        "Manti", "Dolma", "Köfte", "Imam Bayildi", "Other"
    ],
    "Russia": [
        "Borscht", "Pelmeni", "Blini", "Beef Stroganoff", "Pirozhki",
        "Shchi", "Olivier Salad", "Kholodets", "Kulebyaka", "Other"
    ],
    "South Korea": [
        "Kimchi", "Bibimbap", "Bulgogi", "Tteokbokki", "Japchae",
        "Samgyeopsal", "Sundubu Jjigae", "Galbi", "Naengmyeon", "Other"
    ],
    "Vietnam": [
        "Pho", "Banh Mi", "Goi Cuon", "Bun Cha", "Ca Kho To",
        "Com Tam", "Banh Xeo", "Hu Tieu", "Cha Gio", "Other"
    ],
    "Ethiopia": [
        "Injera", "Doro Wat", "Kitfo", "Tibs", "Shiro",
        "Berbere Chicken", "Atakilt Wat", "Gomen", "Teff Bread", "Other"
    ],
    "Germany": [
        "Bratwurst", "Sauerkraut", "Sauerbraten", "Pretzel", "Kartoffelsalat",
        "Spätzle", "Schweinshaxe", "Rouladen", "Apfelstrudel", "Other"
    ],
    "USA": [
        "Hamburger", "Barbecue Ribs", "Clam Chowder", "Mac and Cheese", "Fried Chicken",
        "Apple Pie", "Gumbo", "Jambalaya", "Pancakes", "Other"
    ],
    "UK": [
        "Fish and Chips", "Shepherd's Pie", "Full English Breakfast", "Sunday Roast", "Cornish Pasty",
        "Bangers and Mash", "Yorkshire Pudding", "Eton Mess", "Sticky Toffee Pudding", "Other"
    ],
    "Australia": [
        "Meat Pie", "Vegemite on Toast", "Lamingtons", "Pavlova", "Damper",
        "Anzac Biscuits", "Fairy Bread", "Barramundi", "Chicken Parmigiana", "Other"
    ],
    "Canada": [
        "Poutine", "Butter Tarts", "Nanaimo Bars", "Tourtière", "Caesar Cocktail",
        "Peameal Bacon", "BeaverTails", "Montreal Smoked Meat", "Maple Syrup Pie", "Other"
    ]
}

# Recipe metadata and cultural information
RECIPE_METADATA = {
    # Italian Recipes
    "Margherita Pizza": {
        "local_name": "Pizza Margherita",
        "local_language": "Italian",
        "category": "main",
        "difficulty": 3,
        "time": 45,
        "servings": "2-4 portions",
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "fresh basil", "olive oil"],
        "significance": "Named after Queen Margherita, represents the Italian flag colors"
    },
    "Lasagna": {
        "local_name": "Lasagne",
        "local_language": "Italian", 
        "category": "main",
        "difficulty": 4,
        "time": 120,
        "servings": "6-8 portions",
        "ingredients": ["pasta sheets", "ground beef", "tomato sauce", "bechamel", "parmesan"],
        "significance": "Ancient Roman dish, evolved in Emilia-Romagna region"
    },
    "Risotto alla Milanese": {
        "local_name": "Risotto alla Milanese",
        "local_language": "Italian",
        "category": "main",
        "difficulty": 4,
        "time": 45,
        "servings": "4-6 portions",
        "ingredients": ["arborio rice", "saffron", "beef broth", "white wine", "parmigiano"],
        "significance": "Symbol of Lombard cuisine, traditionally served with osso buco"
    },
    
    # Japanese Recipes
    "Sushi": {
        "local_name": "寿司",
        "local_language": "Japanese",
        "category": "main",
        "difficulty": 5,
        "time": 90,
        "servings": "2-4 portions",
        "ingredients": ["sushi rice", "raw fish", "nori", "wasabi", "soy sauce"],
        "significance": "Ancient preservation method evolved into haute cuisine"
    },
    "Ramen": {
        "local_name": "ラーメン",
        "local_language": "Japanese",
        "category": "main",
        "difficulty": 4,
        "time": 180,
        "servings": "2-4 portions",
        "ingredients": ["ramen noodles", "pork bones", "miso", "green onions", "egg"],
        "significance": "Adapted from Chinese noodles, now essential Japanese comfort food"
    },
    "Tempura": {
        "local_name": "天ぷら",
        "local_language": "Japanese",
        "category": "appetizer",
        "difficulty": 3,
        "time": 30,
        "servings": "2-4 portions",
        "ingredients": ["shrimp", "vegetables", "tempura batter", "oil", "tentsuyu sauce"],
        "significance": "Introduced by Portuguese missionaries, became quintessentially Japanese"
    },
    
    # Mexican Recipes
    "Tacos": {
        "local_name": "Tacos",
        "local_language": "Spanish",
        "category": "main",
        "difficulty": 2,
        "time": 30,
        "servings": "4-6 portions",
        "ingredients": ["corn tortillas", "meat", "onion", "cilantro", "lime"],
        "significance": "Heart of Mexican street food culture, varies by region"
    },
    "Mole Poblano": {
        "local_name": "Mole Poblano",
        "local_language": "Spanish",
        "category": "main",
        "difficulty": 5,
        "time": 240,
        "servings": "8-10 portions",
        "ingredients": ["dried chiles", "chocolate", "turkey", "sesame seeds", "spices"],
        "significance": "National dish of Mexico, represents fusion of indigenous and Spanish cultures"
    },
    
    # Indian Recipes
    "Butter Chicken": {
        "local_name": "Murgh Makhani",
        "local_language": "Hindi",
        "category": "main",
        "difficulty": 3,
        "time": 60,
        "servings": "4-6 portions",
        "ingredients": ["chicken", "tomatoes", "cream", "garam masala", "fenugreek"],
        "significance": "Modern Indian classic, invented in Delhi in the 1950s"
    },
    "Biryani": {
        "local_name": "बिरयानी",
        "local_language": "Hindi",
        "category": "main",
        "difficulty": 5,
        "time": 120,
        "servings": "6-8 portions",
        "ingredients": ["basmati rice", "meat", "saffron", "yogurt", "fried onions"],
        "significance": "Royal Mughal dish, varies significantly by region"
    },
    
    # French Recipes
    "Boeuf Bourguignon": {
        "local_name": "Bœuf Bourguignon",
        "local_language": "French",
        "category": "main",
        "difficulty": 4,
        "time": 180,
        "servings": "6-8 portions",
        "ingredients": ["beef chuck", "red wine", "bacon", "mushrooms", "pearl onions"],
        "significance": "Classic Burgundian dish, symbol of French countryside cooking"
    },
    "Croissant": {
        "local_name": "Croissant",
        "local_language": "French",
        "category": "breakfast",
        "difficulty": 5,
        "time": 240,
        "servings": "8-12 portions",
        "ingredients": ["flour", "butter", "yeast", "milk", "sugar"],
        "significance": "Austrian origin, perfected in France, symbol of French bakery"
    },
    
    # Thai Recipes
    "Pad Thai": {
        "local_name": "ผัดไทย",
        "local_language": "Thai",
        "category": "main",
        "difficulty": 3,
        "time": 30,
        "servings": "2-3 portions",
        "ingredients": ["rice noodles", "tamarind paste", "fish sauce", "eggs", "bean sprouts"],
        "significance": "National dish of Thailand, balance of sweet, sour, and salty"
    },
    "Tom Yum Soup": {
        "local_name": "ต้มยำกุ้ง",
        "local_language": "Thai",
        "category": "soup",
        "difficulty": 2,
        "time": 20,
        "servings": "2-4 portions",
        "ingredients": ["shrimp", "lemongrass", "lime leaves", "galangal", "chili"],
        "significance": "Iconic Thai soup, represents the perfect balance of Thai flavors"
    },
    
    # Add more metadata for other popular dishes...
    "Paella": {
        "local_name": "Paella",
        "local_language": "Spanish",
        "category": "main",
        "difficulty": 4,
        "time": 75,
        "servings": "6-8 portions",
        "ingredients": ["bomba rice", "saffron", "seafood", "green beans", "garrofón beans"],
        "significance": "Symbol of Valencian cuisine, traditionally cooked outdoors"
    },
    "Moussaka": {
        "local_name": "Μουσακάς",
        "local_language": "Greek",
        "category": "main",
        "difficulty": 4,
        "time": 120,
        "servings": "6-8 portions",
        "ingredients": ["eggplant", "ground lamb", "bechamel sauce", "tomatoes", "cheese"],
        "significance": "National dish of Greece, comfort food for celebrations"
    },
    "Hummus": {
        "local_name": "حُمُّص",
        "local_language": "Arabic",
        "category": "appetizer",
        "difficulty": 2,
        "time": 15,
        "servings": "4-6 portions",
        "ingredients": ["chickpeas", "tahini", "lemon juice", "garlic", "olive oil"],
        "significance": "Ancient Levantine dish, symbol of Middle Eastern cuisine"
    }
}

def generate_comprehensive_reference_recipes():
    """Generate comprehensive reference recipes from all countries"""
    recipes = []
    
    # Country codes mapping
    country_codes = {
        "Italy": "italy", "Japan": "japan", "Mexico": "mexico", "India": "india",
        "France": "france", "China": "china", "Thailand": "thailand", "Spain": "spain",
        "Greece": "greece", "Lebanon": "lebanon", "Morocco": "morocco", "Brazil": "brazil",
        "Turkey": "turkey", "Russia": "russia", "South Korea": "south_korea", 
        "Vietnam": "vietnam", "Ethiopia": "ethiopia", "Germany": "germany",
        "USA": "usa", "UK": "uk", "Australia": "australia", "Canada": "canada"
    }
    
    for country, recipe_names in NATIVE_RECIPES_BY_COUNTRY.items():
        country_code = country_codes.get(country, country.lower().replace(" ", "_"))
        
        for recipe_name in recipe_names:
            if recipe_name == "Other":
                continue  # Skip "Other" entries
                
            # Get metadata if available, otherwise use defaults
            metadata = RECIPE_METADATA.get(recipe_name, {
                "local_name": recipe_name,
                "local_language": "English",
                "category": "main",
                "difficulty": 3,
                "time": 60,
                "servings": "4 portions",
                "ingredients": ["traditional ingredients"],
                "significance": f"Traditional {country} dish"
            })
            
            recipe = ReferenceRecipe(
                id=str(uuid.uuid4()),
                name_english=recipe_name,
                name_local=metadata["local_name"],
                local_language=metadata["local_language"],
                country_id=country_code,
                description=f"Traditional {recipe_name} from {country}",
                category=metadata["category"],
                difficulty_level=metadata["difficulty"],
                estimated_time=metadata["time"],
                serving_size=metadata["servings"],
                key_ingredients=metadata["ingredients"],
                cultural_significance=metadata["significance"],
                is_featured=recipe_name in [
                    "Margherita Pizza", "Sushi", "Tacos", "Butter Chicken", "Boeuf Bourguignon",
                    "Pad Thai", "Paella", "Moussaka", "Hummus", "Peking Duck"
                ],
                popularity_score=95 if recipe_name in ["Sushi", "Tacos", "Pizza"] else 
                               90 if recipe_name in ["Ramen", "Biryani", "Pad Thai"] else 
                               85
            )
            recipes.append(recipe)
    
    return recipes

# Generate all reference recipes
COMPREHENSIVE_REFERENCE_RECIPES = generate_comprehensive_reference_recipes()

def get_recipes_by_country(country_id: str):
    """Get reference recipes for a specific country"""
    return [recipe for recipe in COMPREHENSIVE_REFERENCE_RECIPES if recipe.country_id == country_id]

def get_featured_recipes():
    """Get featured reference recipes"""
    return [recipe for recipe in COMPREHENSIVE_REFERENCE_RECIPES if recipe.is_featured]

def get_recipe_by_name(recipe_name: str):
    """Get a specific reference recipe by name"""
    return next((recipe for recipe in COMPREHENSIVE_REFERENCE_RECIPES if recipe.name_english == recipe_name), None)

def get_all_countries_with_recipes():
    """Get list of all countries that have recipes"""
    countries = set()
    for recipe in COMPREHENSIVE_REFERENCE_RECIPES:
        countries.add(recipe.country_id)
    return sorted(list(countries))

def get_recipes_by_category(category: str):
    """Get recipes by category"""
    return [recipe for recipe in COMPREHENSIVE_REFERENCE_RECIPES if recipe.category == category]

def search_recipes(query: str):
    """Search recipes by name or ingredients"""
    query = query.lower()
    results = []
    
    for recipe in COMPREHENSIVE_REFERENCE_RECIPES:
        if (query in recipe.name_english.lower() or 
            query in recipe.name_local.lower() or
            any(query in ingredient.lower() for ingredient in recipe.key_ingredients)):
            results.append(recipe)
    
    return results

# Export the native recipes data for frontend use
def get_native_recipes_json():
    """Get the native recipes by country as JSON structure"""
    return NATIVE_RECIPES_BY_COUNTRY