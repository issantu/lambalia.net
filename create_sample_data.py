#!/usr/bin/env python3
"""
Create sample data for Lambalia platform
Creates sample users and traditional recipes from different countries
"""

import requests
import sys
from datetime import datetime

class LambaliaSampleDataCreator:
    def __init__(self, base_url="https://cuisine-finder-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.users = []
        
    def create_user(self, username, email, password, full_name, country_id=None):
        """Create a user and return token"""
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name,
            "preferred_language": "en"
        }
        if country_id:
            user_data["country_id"] = country_id
            
        try:
            response = requests.post(f"{self.api_url}/auth/register", json=user_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                user_info = data.get('user', {})
                print(f"✅ Created user: {username} ({full_name})")
                return token, user_info
            else:
                print(f"❌ Failed to create user {username}: {response.text}")
                return None, None
        except Exception as e:
            print(f"❌ Error creating user {username}: {str(e)}")
            return None, None
    
    def create_recipe(self, token, recipe_data):
        """Create a recipe with authentication"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        try:
            response = requests.post(f"{self.api_url}/recipes", json=recipe_data, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Created recipe: {data.get('title', 'Unknown')}")
                return data
            else:
                print(f"❌ Failed to create recipe: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error creating recipe: {str(e)}")
            return None
    
    def create_sample_data(self):
        """Create all sample users and recipes"""
        print("🚀 Creating Sample Data for Lambalia Platform")
        print("=" * 60)
        
        # Create sample users from different cultures
        users_data = [
            {
                "username": "maria_italiana",
                "email": "maria@lambalia.net",
                "password": "lambalia123",
                "full_name": "Maria Rossi",
                "recipes": [
                    {
                        "title": "Nonna's Traditional Risotto Milanese",
                        "description": "A cherished family recipe from Milan, passed down through four generations. This creamy risotto gets its golden color from precious saffron and represents the heart of Lombard cuisine.",
                        "ingredients": [
                            {"name": "Arborio rice", "amount": "320", "unit": "g"},
                            {"name": "Beef bone broth", "amount": "1.5", "unit": "L"},
                            {"name": "Saffron threads", "amount": "1", "unit": "pinch"},
                            {"name": "White wine", "amount": "150", "unit": "ml"},
                            {"name": "Onion", "amount": "1", "unit": "medium"},
                            {"name": "Parmigiano-Reggiano", "amount": "100", "unit": "g"},
                            {"name": "Butter", "amount": "80", "unit": "g"},
                            {"name": "Bone marrow", "amount": "50", "unit": "g"}
                        ],
                        "steps": [
                            {"step_number": "1", "description": "Heat the beef broth in a separate pot and keep it simmering. Dissolve saffron in a small amount of warm broth."},
                            {"step_number": "2", "description": "In a heavy-bottomed pan, melt half the butter and sauté finely chopped onion until translucent."},
                            {"step_number": "3", "description": "Add rice and toast for 2 minutes until edges become translucent. Add wine and stir until absorbed."},
                            {"step_number": "4", "description": "Add warm broth one ladle at a time, stirring constantly. Continue for 18-20 minutes until rice is creamy but al dente."},
                            {"step_number": "5", "description": "Stir in saffron mixture, remaining butter, bone marrow, and grated Parmigiano. Rest for 2 minutes before serving."}
                        ],
                        "cooking_time_minutes": 45,
                        "difficulty_level": 4,
                        "servings": 4,
                        "cuisine_type": "Italian",
                        "dietary_preferences": [],
                        "tags": ["traditional", "risotto", "saffron", "milan", "family-recipe"]
                    }
                ]
            },
            {
                "username": "carlos_mexicano",
                "email": "carlos@lambalia.net", 
                "password": "lambalia123",
                "full_name": "Carlos Hernández",
                "recipes": [
                    {
                        "title": "Abuela's Mole Poblano",
                        "description": "An authentic mole poblano recipe from Puebla, Mexico. This complex sauce contains over 20 ingredients and represents centuries of culinary tradition, blending indigenous and Spanish influences.",
                        "ingredients": [
                            {"name": "Dried chiles (ancho, mulato, pasilla)", "amount": "8", "unit": "pieces"},
                            {"name": "Tomatoes", "amount": "3", "unit": "large"},
                            {"name": "Tomatillos", "amount": "4", "unit": "medium"},
                            {"name": "White onion", "amount": "1", "unit": "large"},
                            {"name": "Garlic cloves", "amount": "6", "unit": "pieces"},
                            {"name": "Mexican chocolate", "amount": "90", "unit": "g"},
                            {"name": "Sesame seeds", "amount": "3", "unit": "tbsp"},
                            {"name": "Pumpkin seeds", "amount": "2", "unit": "tbsp"},
                            {"name": "Raisins", "amount": "2", "unit": "tbsp"},
                            {"name": "Cinnamon stick", "amount": "1", "unit": "piece"},
                            {"name": "Chicken", "amount": "1", "unit": "whole"}
                        ],
                        "steps": [
                            {"step_number": "1", "description": "Toast dried chiles in a dry pan until fragrant. Soak in hot water for 30 minutes."},
                            {"step_number": "2", "description": "Char tomatoes, tomatillos, onion, and garlic on a comal or griddle until blackened in spots."},
                            {"step_number": "3", "description": "Toast sesame seeds, pumpkin seeds, and spices separately until fragrant."},
                            {"step_number": "4", "description": "Blend all ingredients in batches with chile soaking liquid until completely smooth."},
                            {"step_number": "5", "description": "Fry the mole paste in lard for 45 minutes, stirring constantly. Add chocolate and simmer with cooked chicken for 30 minutes."}
                        ],
                        "cooking_time_minutes": 180,
                        "difficulty_level": 5,
                        "servings": 8,
                        "cuisine_type": "Mexican",
                        "dietary_preferences": [],
                        "tags": ["traditional", "mole", "puebla", "complex", "celebration"]
                    }
                ]
            },
            {
                "username": "priya_indian",
                "email": "priya@lambalia.net",
                "password": "lambalia123", 
                "full_name": "Priya Sharma",
                "recipes": [
                    {
                        "title": "Hyderabadi Dum Biryani",
                        "description": "An authentic Hyderabadi biryani recipe from my grandmother's kitchen. This royal dish uses the dum cooking method where rice and meat are layered and slow-cooked in a sealed pot, creating aromatic perfection.",
                        "ingredients": [
                            {"name": "Basmati rice", "amount": "500", "unit": "g"},
                            {"name": "Mutton/Goat meat", "amount": "1", "unit": "kg"},
                            {"name": "Yogurt", "amount": "200", "unit": "ml"},
                            {"name": "Fried onions (birista)", "amount": "150", "unit": "g"},
                            {"name": "Saffron", "amount": "1", "unit": "pinch"},
                            {"name": "Mint leaves", "amount": "1", "unit": "cup"},
                            {"name": "Coriander leaves", "amount": "1", "unit": "cup"},
                            {"name": "Ghee", "amount": "100", "unit": "ml"},
                            {"name": "Ginger-garlic paste", "amount": "2", "unit": "tbsp"},
                            {"name": "Red chili powder", "amount": "1", "unit": "tsp"},
                            {"name": "Garam masala", "amount": "1", "unit": "tsp"}
                        ],
                        "steps": [
                            {"step_number": "1", "description": "Marinate mutton with yogurt, ginger-garlic paste, red chili powder, and salt for 2 hours."},
                            {"step_number": "2", "description": "Soak basmati rice for 30 minutes. Boil with whole spices until 70% cooked."},
                            {"step_number": "3", "description": "Cook marinated mutton until tender. Soak saffron in warm milk."},
                            {"step_number": "4", "description": "Layer cooked rice over mutton. Sprinkle fried onions, mint, coriander, saffron milk, and ghee."},
                            {"step_number": "5", "description": "Cover with aluminum foil, then lid. Cook on high heat for 3 minutes, then dum on low heat for 45 minutes."}
                        ],
                        "cooking_time_minutes": 120,
                        "difficulty_level": 4,
                        "servings": 6,
                        "cuisine_type": "Indian",
                        "dietary_preferences": [],
                        "tags": ["traditional", "biryani", "hyderabadi", "dum", "royal"]
                    }
                ]
            },
            {
                "username": "takeshi_japanese",
                "email": "takeshi@lambalia.net",
                "password": "lambalia123",
                "full_name": "Takeshi Yamamoto", 
                "recipes": [
                    {
                        "title": "Traditional Tonkotsu Ramen",
                        "description": "An authentic tonkotsu ramen recipe from Fukuoka, perfected over generations. The rich, creamy broth is made by boiling pork bones for hours, creating the soul-warming comfort food of Japan.",
                        "ingredients": [
                            {"name": "Pork bones (trotters, femur)", "amount": "2", "unit": "kg"},
                            {"name": "Pork belly", "amount": "500", "unit": "g"},
                            {"name": "Fresh ramen noodles", "amount": "400", "unit": "g"},
                            {"name": "Soft-boiled eggs", "amount": "4", "unit": "pieces"},
                            {"name": "Green onions", "amount": "4", "unit": "stalks"},
                            {"name": "Nori seaweed", "amount": "4", "unit": "sheets"},
                            {"name": "Bamboo shoots", "amount": "200", "unit": "g"},
                            {"name": "Garlic", "amount": "1", "unit": "head"},
                            {"name": "Ginger", "amount": "50", "unit": "g"},
                            {"name": "White miso paste", "amount": "2", "unit": "tbsp"},
                            {"name": "Soy sauce", "amount": "3", "unit": "tbsp"}
                        ],
                        "steps": [
                            {"step_number": "1", "description": "Blanch pork bones in boiling water for 10 minutes. Rinse thoroughly under cold water."},
                            {"step_number": "2", "description": "Place bones in a large pot, cover with water, and boil vigorously for 12-18 hours. Add water as needed."},
                            {"step_number": "3", "description": "Char pork belly and slice. Prepare soft-boiled eggs and marinate in soy sauce mixture."},
                            {"step_number": "4", "description": "Strain the milky white broth. Season with miso, soy sauce, and garlic oil."},
                            {"step_number": "5", "description": "Cook fresh noodles for 2 minutes. Assemble bowls with noodles, broth, chashu, eggs, and toppings."}
                        ],
                        "cooking_time_minutes": 1080,
                        "difficulty_level": 5,
                        "servings": 4,
                        "cuisine_type": "Japanese",
                        "dietary_preferences": [],
                        "tags": ["traditional", "ramen", "tonkotsu", "fukuoka", "comfort-food"]
                    }
                ]
            }
        ]
        
        # Create users and their recipes
        for user_data in users_data:
            token, user_info = self.create_user(
                user_data["username"],
                user_data["email"], 
                user_data["password"],
                user_data["full_name"]
            )
            
            if token:
                self.users.append({
                    "token": token,
                    "info": user_info,
                    "username": user_data["username"]
                })
                
                # Create recipes for this user
                for recipe_data in user_data["recipes"]:
                    self.create_recipe(token, recipe_data)
        
        print("\n" + "=" * 60)
        print(f"✅ Sample data creation completed!")
        print(f"Created {len(self.users)} users with traditional recipes")
        print("Users can login with password: lambalia123")
        print("\nSample users:")
        for user in self.users:
            print(f"  - {user['username']} ({user['info'].get('full_name', 'Unknown')})")

def main():
    creator = LambaliaSampleDataCreator()
    creator.create_sample_data()

if __name__ == "__main__":
    main()