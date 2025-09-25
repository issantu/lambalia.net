#!/usr/bin/env python3
"""
Enhanced Smart Cooking Tool Test Suite
Focused testing for the specific issues mentioned in the review request
"""

import requests
import sys
import json
from datetime import datetime

class EnhancedCookingTester:
    def __init__(self, base_url="https://cuisine-translator.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.test_user_data = {
            "username": f"cooktest_{datetime.now().strftime('%H%M%S')}",
            "email": f"cooktest_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "testpass123",
            "full_name": "Cooking Test User",
            "postal_code": "12345",
            "preferred_language": "en"
        }
        self.tests_run = 0
        self.tests_passed = 0

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def make_request(self, method: str, endpoint: str, data=None, expected_status: int = 200):
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=data, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            if not success:
                print(f"   Status: {response.status_code} (expected {expected_status})")
                print(f"   Response: {response_data}")

            return success, response_data

        except requests.exceptions.RequestException as e:
            print(f"   Request failed: {str(e)}")
            return False, {"error": str(e)}

    def setup_user(self):
        """Register and login a test user"""
        print("🔧 Setting up test user...")
        
        # Register
        success, data = self.make_request('POST', 'auth/register', self.test_user_data, 200)
        if not success:
            print("❌ Failed to register test user")
            return False
            
        self.token = data.get('access_token')
        user_data = data.get('user', {})
        self.user_id = user_data.get('id')
        
        print(f"✅ Test user registered: {self.user_id}")
        return True

    def test_hackthemenu_content_expansion(self):
        """Test HackTheMenu Content Expansion - Should have 51+ items across all restaurants"""
        print("\n🍔 Testing HackTheMenu Content Expansion...")
        
        success, data = self.make_request('GET', 'enhanced-cooking/fastfood/restaurants')
        
        if success:
            restaurants = data.get('restaurants', [])
            total_items = data.get('total_items', 0)
            total_secret_items = data.get('total_secret_items', 0)
            
            # Check for expected restaurants
            restaurant_names = [r.get('name', '') for r in restaurants]
            expected_restaurants = ["McDonald's", "KFC", "Taco Bell", "Burger King", "Subway"]
            found_restaurants = sum(1 for name in expected_restaurants if name in restaurant_names)
            
            # Verify expansion from 5 items to 51+ items
            expansion_success = total_items >= 51
            secret_menu_success = total_secret_items >= 19  # Should have 19+ secret menu items
            
            details = f"- Total items: {total_items} (target: 51+), Secret items: {total_secret_items} (target: 19+), Restaurants: {found_restaurants}/5"
            details += f", Expansion: {'✓' if expansion_success else '✗'}, Secret menu: {'✓' if secret_menu_success else '✗'}"
            
            overall_success = expansion_success and secret_menu_success and found_restaurants == 5
        else:
            details = "- Failed to get restaurant data"
            overall_success = False
            
        return self.log_test("HackTheMenu Content Expansion (5→51+ items)", overall_success, details)

    def test_restaurant_name_case_sensitivity(self):
        """Test Restaurant Name Case Sensitivity - Both 'McDonalds' and 'McDonald's' should work"""
        print("\n🔤 Testing Restaurant Name Case Sensitivity...")
        
        test_cases = [
            ("McDonald's", "with apostrophe"),
            ("McDonalds", "without apostrophe"),
            ("mcdonalds", "lowercase"),
            ("MCDONALDS", "uppercase")
        ]
        
        successful_cases = 0
        
        for restaurant_name, description in test_cases:
            success, data = self.make_request('GET', f'enhanced-cooking/recipes/fastfood/{restaurant_name}')
            
            if success:
                items = data.get('items', [])
                if len(items) > 0:
                    successful_cases += 1
                    print(f"   ✅ {restaurant_name} ({description}): {len(items)} items found")
                else:
                    print(f"   ❌ {restaurant_name} ({description}): No items found")
            else:
                print(f"   ❌ {restaurant_name} ({description}): Request failed")
        
        details = f"- {successful_cases}/{len(test_cases)} case variations working"
        return self.log_test("Restaurant Name Case Sensitivity", successful_cases >= 2, details)

    def test_secret_menu_items_expansion(self):
        """Test Secret Menu Items - Should have 19+ secret menu items with popularity scores"""
        print("\n🤫 Testing Secret Menu Items Expansion...")
        
        success, data = self.make_request('GET', 'enhanced-cooking/recipes/secret-menu')
        
        if success:
            secret_items = data.get('secret_menu_items', [])
            total_items = data.get('total_items', 0)
            restaurants = data.get('restaurants', [])
            
            # Check if items have popularity scores
            items_with_scores = sum(1 for item in secret_items if item.get('popularity_score', 0) > 0)
            
            # Check if sorted by popularity
            is_sorted = all(
                secret_items[i].get('popularity_score', 0) >= secret_items[i+1].get('popularity_score', 0)
                for i in range(len(secret_items)-1)
            ) if len(secret_items) > 1 else True
            
            expansion_success = total_items >= 19  # Should have 19+ secret menu items
            
            details = f"- Secret items: {total_items} (target: 19+), With scores: {items_with_scores}, Restaurants: {len(restaurants)}"
            details += f", Sorted by popularity: {'✓' if is_sorted else '✗'}, Expansion: {'✓' if expansion_success else '✗'}"
            
            overall_success = expansion_success and items_with_scores > 0 and is_sorted
        else:
            details = "- Failed to get secret menu data"
            overall_success = False
            
        return self.log_test("Secret Menu Items Expansion (19+ items)", overall_success, details)

    def test_ai_recipe_generation_fix(self):
        """Test AI Recipe Generation - Should work without server errors"""
        print("\n🤖 Testing AI Recipe Generation Fix...")
        
        if not self.token:
            return self.log_test("AI Recipe Generation", False, "- No auth token available")
        
        # First, add some ingredients to pantry
        ingredients_data = {
            "ingredients": ["chicken", "rice", "onion", "garlic", "tomato", "cheese"]
        }
        
        success, data = self.make_request('POST', 'enhanced-cooking/pantry/add-ingredients', ingredients_data)
        if not success:
            return self.log_test("AI Recipe Generation", False, "- Failed to add ingredients to pantry")
        
        # Now test AI recipe generation
        success, data = self.make_request('POST', 'enhanced-cooking/recipes/generate-ai')
        
        if success:
            ai_recipes = data.get('ai_recipes', [])
            ingredients_used = data.get('ingredients_used', [])
            
            # Check if recipes were generated
            recipes_generated = len(ai_recipes) > 0
            
            # Check if recipes have proper structure
            valid_structure = True
            if ai_recipes:
                first_recipe = ai_recipes[0]
                required_fields = ['id', 'name', 'ingredients_used', 'instructions', 'source']
                valid_structure = all(field in first_recipe for field in required_fields)
                
                # Check if it's marked as AI-generated
                is_ai_source = first_recipe.get('source') == 'lambalia_ai'
            else:
                is_ai_source = False
            
            details = f"- Recipes generated: {len(ai_recipes)}, Ingredients used: {len(ingredients_used)}"
            details += f", Valid structure: {'✓' if valid_structure else '✗'}, AI source: {'✓' if is_ai_source else '✗'}"
            
            overall_success = recipes_generated and valid_structure and is_ai_source
        else:
            details = f"- Server error occurred: {data.get('detail', 'Unknown error')}"
            overall_success = False
            
        return self.log_test("AI Recipe Generation Fix", overall_success, details)

    def test_ingredient_based_recipe_matching(self):
        """Test Recipe Finding with Ingredients - SuperCook-style ingredient matching"""
        print("\n🥘 Testing Ingredient-Based Recipe Matching...")
        
        if not self.token:
            return self.log_test("Ingredient-Based Recipe Matching", False, "- No auth token available")
        
        # Test recipe finding with different max_missing values
        test_cases = [
            (0, "exact matches only"),
            (1, "allow 1 missing ingredient"),
            (2, "allow 2 missing ingredients")
        ]
        
        successful_cases = 0
        total_recipes_found = 0
        
        for max_missing, description in test_cases:
            success, data = self.make_request('GET', f'enhanced-cooking/recipes/find?max_missing={max_missing}')
            
            if success:
                recipes = data.get('recipes', [])
                ingredients_used = data.get('ingredients_used', [])
                total_found = data.get('total_found', 0)
                
                if len(recipes) > 0:
                    successful_cases += 1
                    total_recipes_found += len(recipes)
                    print(f"   ✅ {description}: {len(recipes)} recipes found")
                    
                    # Check recipe structure
                    first_recipe = recipes[0]
                    has_missing_info = 'missing_ingredients' in first_recipe
                    print(f"      - Missing ingredients info: {'✓' if has_missing_info else '✗'}")
                else:
                    print(f"   ⚠️  {description}: No recipes found")
            else:
                print(f"   ❌ {description}: Request failed")
        
        details = f"- {successful_cases}/{len(test_cases)} search types working, Total recipes: {total_recipes_found}"
        return self.log_test("Ingredient-Based Recipe Matching", successful_cases > 0, details)

    def test_comprehensive_functionality(self):
        """Test comprehensive functionality to ensure all features work together"""
        print("\n🔧 Testing Comprehensive Enhanced Smart Cooking Functionality...")
        
        # Test service stats
        success, data = self.make_request('GET', 'enhanced-cooking/stats')
        
        if success:
            stats = data.get('stats', {})
            available_ingredients = stats.get('available_ingredients', 0)
            fastfood_items = stats.get('fastfood_items', 0)
            secret_menu_items = stats.get('secret_menu_items', 0)
            supported_restaurants = stats.get('supported_restaurants', 0)
            features = stats.get('features', [])
            
            # Check if all expected features are present
            expected_features = [
                "SuperCook-style ingredient matching",
                "HackTheMenu fast food clones", 
                "AI-powered recipe generation",
                "Virtual pantry management",
                "Secret menu items",
                "Ingredient autocomplete"
            ]
            
            features_present = sum(1 for feature in expected_features if feature in features)
            
            # Verify minimum requirements
            meets_requirements = (
                available_ingredients >= 20 and  # 20+ base ingredients
                fastfood_items >= 51 and        # 51+ fast food items
                secret_menu_items >= 19 and     # 19+ secret menu items
                supported_restaurants >= 5 and   # 5+ restaurants
                features_present >= 6            # All 6 core features
            )
            
            details = f"- Ingredients: {available_ingredients}/20+, FastFood: {fastfood_items}/51+, Secret: {secret_menu_items}/19+"
            details += f", Restaurants: {supported_restaurants}/5+, Features: {features_present}/6"
            details += f", Requirements met: {'✓' if meets_requirements else '✗'}"
            
            overall_success = meets_requirements
        else:
            details = "- Failed to get service stats"
            overall_success = False
            
        return self.log_test("Comprehensive Enhanced Smart Cooking", overall_success, details)

    def run_all_tests(self):
        """Run all Enhanced Smart Cooking Tool tests"""
        print("🍳 Enhanced Smart Cooking Tool - Focused Test Suite")
        print("=" * 70)
        print("Testing specific fixes mentioned in review request:")
        print("1. HackTheMenu Content Expansion (5→51+ items)")
        print("2. AI Recipe Generation Fix")
        print("3. Restaurant Name Case Sensitivity")
        print("4. Secret Menu Items Expansion (19+ items)")
        print("5. Ingredient-Based Recipe Matching")
        print("=" * 70)
        
        # Setup
        if not self.setup_user():
            print("❌ Failed to setup test user. Aborting tests.")
            return
        
        # Run focused tests
        self.test_hackthemenu_content_expansion()
        self.test_restaurant_name_case_sensitivity()
        self.test_secret_menu_items_expansion()
        self.test_ai_recipe_generation_fix()
        self.test_ingredient_based_recipe_matching()
        self.test_comprehensive_functionality()
        
        # Summary
        print("\n" + "=" * 70)
        print(f"📊 Enhanced Smart Cooking Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Enhanced Smart Cooking Tool fixes are working correctly.")
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"⚠️  {failed_tests} test(s) failed. Some issues may still exist.")
        
        print("=" * 70)

if __name__ == "__main__":
    tester = EnhancedCookingTester()
    tester.run_all_tests()