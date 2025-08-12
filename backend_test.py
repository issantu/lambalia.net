#!/usr/bin/env python3
"""
Enhanced Lambalia Backend API Test Suite
Tests all backend endpoints for the enhanced traditional recipe sharing platform
with snippets, grocery integration, and reference recipes
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class LambaliaEnhancedAPITester:
    def __init__(self, base_url="https://446b805d-9b3a-4c1a-9d2c-c093357a79b2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.test_user_data = {
            "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "postal_code": "12345",
            "preferred_language": "en"
        }
        self.tests_run = 0
        self.tests_passed = 0
        self.snippet_id = None

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    expected_status: int = 200) -> tuple[bool, Dict]:
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
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

    def test_health_check(self):
        """Test health endpoint"""
        success, data = self.make_request('GET', 'health')
        details = f"- Status: {data.get('status', 'unknown')}" if success else ""
        return self.log_test("Health Check", success, details)

    def test_get_countries(self):
        """Test countries endpoint"""
        success, data = self.make_request('GET', 'countries')
        if success:
            countries_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {countries_count} countries"
        else:
            details = ""
        return self.log_test("Get Countries", success, details)

    def test_user_registration(self):
        """Test user registration"""
        success, data = self.make_request('POST', 'auth/register', self.test_user_data, 200)
        
        if success:
            self.token = data.get('access_token')
            user_data = data.get('user', {})
            self.user_id = user_data.get('id')
            details = f"- User ID: {self.user_id}, Token: {'✓' if self.token else '✗'}"
        else:
            details = ""
            
        return self.log_test("User Registration", success, details)

    def test_user_login(self):
        """Test user login with registered credentials"""
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        success, data = self.make_request('POST', 'auth/login', login_data, 200)
        
        if success:
            new_token = data.get('access_token')
            user_data = data.get('user', {})
            details = f"- Token received: {'✓' if new_token else '✗'}"
            # Update token for subsequent tests
            if new_token:
                self.token = new_token
        else:
            details = ""
            
        return self.log_test("User Login", success, details)

    def test_get_current_user(self):
        """Test getting current user profile"""
        if not self.token:
            return self.log_test("Get Current User", False, "- No auth token available")
            
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            username = data.get('username', 'unknown')
            email = data.get('email', 'unknown')
            details = f"- User: {username} ({email})"
        else:
            details = ""
            
        return self.log_test("Get Current User", success, details)

    # NEW ENHANCED FEATURES TESTS

    def test_get_reference_recipes(self):
        """Test getting reference recipes"""
        success, data = self.make_request('GET', 'reference-recipes')
        
        if success:
            recipes_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {recipes_count} reference recipes"
            if recipes_count > 0:
                first_recipe = data[0]
                details += f", First: {first_recipe.get('name_english', 'unknown')}"
        else:
            details = ""
            
        return self.log_test("Get Reference Recipes", success, details)

    def test_get_featured_reference_recipes(self):
        """Test getting featured reference recipes"""
        success, data = self.make_request('GET', 'reference-recipes?featured_only=true')
        
        if success:
            recipes_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {recipes_count} featured recipes"
        else:
            details = ""
            
        return self.log_test("Get Featured Reference Recipes", success, details)

    def test_get_country_reference_recipes(self):
        """Test getting reference recipes by country"""
        success, data = self.make_request('GET', 'countries/italy/reference-recipes')
        
        if success:
            recipes_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {recipes_count} Italian recipes"
        else:
            details = ""
            
        return self.log_test("Get Italian Reference Recipes", success, details)

    def test_create_snippet(self):
        """Test creating a recipe snippet"""
        if not self.token:
            return self.log_test("Create Snippet", False, "- No auth token available")

        snippet_data = {
            "title": "Quick Pasta Carbonara",
            "title_local": "Carbonara Veloce",
            "local_language": "Italian",
            "description": "A quick version of the classic Roman pasta dish",
            "snippet_type": "quick_recipe",
            "ingredients": [
                {"name": "spaghetti", "amount": "200", "unit": "g"},
                {"name": "eggs", "amount": "2", "unit": "pcs"},
                {"name": "pecorino romano", "amount": "50", "unit": "g"}
            ],
            "preparation_steps": [
                {"step_number": "1", "description": "Boil pasta in salted water"},
                {"step_number": "2", "description": "Mix eggs and cheese"},
                {"step_number": "3", "description": "Combine hot pasta with egg mixture"}
            ],
            "cooking_time_minutes": 15,
            "difficulty_level": 2,
            "servings": 2,
            "tags": ["quick", "italian", "pasta"],
            "video_duration": 45
        }

        success, data = self.make_request('POST', 'snippets', snippet_data, 200)
        
        if success:
            self.snippet_id = data.get('id')
            title = data.get('title', 'unknown')
            details = f"- Snippet ID: {self.snippet_id}, Title: {title}"
        else:
            details = ""
            
        return self.log_test("Create Snippet", success, details)

    def test_get_snippets(self):
        """Test getting all snippets"""
        success, data = self.make_request('GET', 'snippets')
        
        if success:
            snippets_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {snippets_count} snippets"
        else:
            details = ""
            
        return self.log_test("Get All Snippets", success, details)

    def test_get_user_snippets_playlist(self):
        """Test getting user's snippets playlist"""
        if not self.user_id:
            return self.log_test("Get User Snippets Playlist", False, "- No user ID available")
            
        success, data = self.make_request('GET', f'users/{self.user_id}/snippets/playlist')
        
        if success:
            snippets_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {snippets_count} snippets in playlist"
        else:
            details = ""
            
        return self.log_test("Get User Snippets Playlist", success, details)

    def test_like_snippet(self):
        """Test liking a snippet"""
        if not self.snippet_id or not self.token:
            return self.log_test("Like Snippet", False, "- Missing snippet ID or auth token")

        success, data = self.make_request('POST', f'snippets/{self.snippet_id}/like')
        
        if success:
            liked = data.get('liked', False)
            details = f"- Liked: {liked}"
        else:
            details = ""
            
        return self.log_test("Like Snippet", success, details)

    def test_grocery_search(self):
        """Test grocery store search functionality"""
        if not self.token:
            return self.log_test("Grocery Search", False, "- No auth token available")

        search_data = {
            "ingredients": ["tomatoes", "pasta", "cheese"],
            "user_postal_code": "12345",
            "max_distance_km": 10.0,
            "budget_preference": "medium",
            "delivery_preference": "either"
        }

        success, data = self.make_request('POST', 'grocery/search', search_data, 200)
        
        if success:
            stores_count = len(data.get('stores', [])) if data else 0
            total_cost = data.get('total_estimated_cost', 0) if data else 0
            details = f"- Found {stores_count} stores, Est. cost: ${total_cost}"
        else:
            details = ""
            
        return self.log_test("Grocery Search", success, details)

    def test_nearby_stores(self):
        """Test getting nearby grocery stores"""
        if not self.token:
            return self.log_test("Get Nearby Stores", False, "- No auth token available")

        success, data = self.make_request('GET', 'grocery/stores/nearby?postal_code=12345&radius_km=10')
        
        if success:
            stores_count = len(data.get('stores', [])) if data else 0
            details = f"- Found {stores_count} nearby stores"
        else:
            details = ""
            
        return self.log_test("Get Nearby Stores", success, details)

    def test_grocery_preferences(self):
        """Test updating and getting grocery preferences"""
        if not self.token:
            return self.log_test("Grocery Preferences", False, "- No auth token available")

        # Test updating preferences - include user_id as required by the model
        preferences_data = {
            "user_id": self.user_id,  # Required by UserGroceryPreference model
            "preferred_stores": ["store_1", "store_2"],
            "max_distance_km": 15.0,
            "budget_preference": "medium",
            "dietary_restrictions": ["vegetarian"],
            "delivery_preference": "pickup"
        }

        success, data = self.make_request('POST', 'users/grocery-preferences', preferences_data, 200)
        
        if not success:
            return self.log_test("Update Grocery Preferences", success, "")

        # Test getting preferences
        success, data = self.make_request('GET', 'users/me/grocery-preferences')
        
        if success:
            budget_pref = data.get('budget_preference', 'unknown')
            delivery_pref = data.get('delivery_preference', 'unknown')
            details = f"- Budget: {budget_pref}, Delivery: {delivery_pref}"
        else:
            details = ""
            
        return self.log_test("Grocery Preferences", success, details)

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting Enhanced Lambalia Backend API Tests")
        print("=" * 70)
        
        # Basic endpoint tests
        self.test_health_check()
        self.test_get_countries()
        
        # Authentication tests
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        
        # Reference recipes tests
        print("\n📚 Testing Reference Recipes...")
        self.test_get_reference_recipes()
        self.test_get_featured_reference_recipes()
        self.test_get_country_reference_recipes()
        
        # Snippets tests
        print("\n🎬 Testing Recipe Snippets...")
        self.test_create_snippet()
        self.test_get_snippets()
        self.test_get_user_snippets_playlist()
        self.test_like_snippet()
        
        # Grocery integration tests
        print("\n🛒 Testing Grocery Integration...")
        self.test_grocery_search()
        self.test_nearby_stores()
        self.test_grocery_preferences()
        
        # Print summary
        print("\n" + "=" * 70)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Enhanced Lambalia Backend API is working correctly.")
            return 0
        else:
            failed_count = self.tests_run - self.tests_passed
            print(f"⚠️  {failed_count} tests failed. Check the issues above.")
            return 1

def main():
    """Main test runner"""
    print("Enhanced Lambalia Backend API Test Suite")
    print(f"Testing against: https://446b805d-9b3a-4c1a-9d2c-c093357a79b2.preview.emergentagent.com")
    print()
    
    tester = LambaliaEnhancedAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())