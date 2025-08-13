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
    def __init__(self, base_url="https://60782b34-2e04-483f-bfaa-6a39ebd6777d.preview.emergentagent.com"):
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
        
        # Traditional restaurant marketplace test data
        self.vendor_application_id = None
        self.traditional_restaurant_id = None
        self.special_order_id = None
        self.special_order_booking_id = None

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

    # TRADITIONAL RESTAURANT MARKETPLACE TESTS

    def test_traditional_restaurant_vendor_application(self):
        """Test traditional restaurant vendor application"""
        if not self.token:
            return self.log_test("Traditional Restaurant Vendor Application", False, "- No auth token available")

        application_data = {
            "vendor_type": "traditional_restaurant",
            "legal_name": "Maria Rossi",
            "phone_number": "+1-555-0123",
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
            "restaurant_name": "Nonna's Kitchen",
            "business_license_number": "NYC-REST-2024-001",
            "years_in_business": 5,
            "cuisine_specialties": ["Italian", "Mediterranean"],
            "dietary_accommodations": ["vegetarian", "gluten_free"],
            "background_check_consent": True,
            "has_food_handling_experience": True,
            "years_cooking_experience": 15,
            "has_liability_insurance": True,
            "emergency_contact_name": "Giuseppe Rossi",
            "emergency_contact_phone": "+1-555-0124",
            "terms_accepted": True,
            "privacy_policy_accepted": True
        }

        success, data = self.make_request('POST', 'vendor/apply', application_data, 200)
        
        if success:
            self.vendor_application_id = data.get('id')
            vendor_type = data.get('vendor_type', 'unknown')
            status = data.get('status', 'unknown')
            details = f"- Application ID: {self.vendor_application_id}, Type: {vendor_type}, Status: {status}"
        else:
            details = ""
            
        return self.log_test("Traditional Restaurant Vendor Application", success, details)

    def test_admin_approve_vendor_application(self):
        """Test admin approval of vendor application (simulated)"""
        if not self.vendor_application_id:
            return self.log_test("Admin Approve Vendor Application", False, "- No application ID available")

        approval_data = {
            "approval_notes": "Application approved after document review"
        }

        success, data = self.make_request('POST', f'admin/vendor/approve/{self.vendor_application_id}', approval_data, 200)
        
        if success:
            status = data.get('status', 'unknown')
            message = data.get('message', 'unknown')
            details = f"- Status: {status}, Message: {message}"
        else:
            details = ""
            
        return self.log_test("Admin Approve Vendor Application", success, details)

    def test_create_traditional_restaurant_profile(self):
        """Test creating traditional restaurant profile after approval"""
        if not self.token:
            return self.log_test("Create Traditional Restaurant Profile", False, "- No auth token available")

        restaurant_data = {
            "restaurant_name": "Nonna's Kitchen",
            "business_name": "Nonna's Kitchen LLC",
            "description": "Authentic Italian cuisine with family recipes passed down through generations",
            "cuisine_type": ["Italian", "Mediterranean"],
            "specialty_dishes": ["Homemade Pasta", "Wood-fired Pizza", "Tiramisu"],
            "phone_number": "+1-555-0123",
            "website": "https://nonnas-kitchen.com",
            "business_license_number": "NYC-REST-2024-001",
            "years_in_business": 5,
            "seating_capacity": 40,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "operating_days": ["tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
            "operating_hours": {
                "tuesday": {"start": "17:00", "end": "22:00"},
                "wednesday": {"start": "17:00", "end": "22:00"},
                "thursday": {"start": "17:00", "end": "22:00"},
                "friday": {"start": "17:00", "end": "23:00"},
                "saturday": {"start": "16:00", "end": "23:00"},
                "sunday": {"start": "16:00", "end": "21:00"}
            },
            "minimum_order_value": 75.0,
            "maximum_order_value": 400.0,
            "advance_order_days": 2,
            "offers_delivery": True,
            "offers_pickup": True,
            "delivery_radius_km": 15.0,
            "photos": [
                {"type": "exterior", "url": "https://example.com/exterior.jpg", "caption": "Restaurant exterior"},
                {"type": "interior", "url": "https://example.com/interior.jpg", "caption": "Dining room"}
            ]
        }

        success, data = self.make_request('POST', 'vendor/traditional-restaurant/create', restaurant_data, 200)
        
        if success:
            self.traditional_restaurant_id = data.get('id')
            restaurant_name = data.get('restaurant_name', 'unknown')
            cuisine_type = data.get('cuisine_type', [])
            details = f"- Restaurant ID: {self.traditional_restaurant_id}, Name: {restaurant_name}, Cuisine: {cuisine_type}"
        else:
            details = ""
            
        return self.log_test("Create Traditional Restaurant Profile", success, details)

    def test_get_traditional_restaurants(self):
        """Test getting traditional restaurants with filtering"""
        success, data = self.make_request('GET', 'traditional-restaurants')
        
        if success:
            restaurants_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {restaurants_count} traditional restaurants"
            if restaurants_count > 0:
                first_restaurant = data[0]
                details += f", First: {first_restaurant.get('restaurant_name', 'unknown')}"
        else:
            details = ""
            
        return self.log_test("Get Traditional Restaurants", success, details)

    def test_get_traditional_restaurants_with_filters(self):
        """Test getting traditional restaurants with various filters"""
        # Test with cuisine filter
        success, data = self.make_request('GET', 'traditional-restaurants?cuisine_type=Italian')
        
        if success:
            italian_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {italian_count} Italian restaurants"
        else:
            details = ""
            
        return self.log_test("Get Traditional Restaurants with Filters", success, details)

    def test_create_special_order(self):
        """Test creating a special order proposal"""
        if not self.token:
            return self.log_test("Create Special Order", False, "- No auth token available")

        from datetime import datetime, timedelta
        
        # Create available dates for the next week
        available_dates = []
        for i in range(1, 8):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            available_dates.append(date)

        special_order_data = {
            "title": "Romantic Italian Dinner for Two",
            "description": "A carefully curated 4-course Italian dinner featuring seasonal ingredients and wine pairings",
            "cuisine_style": "Italian",
            "occasion_type": "romantic",
            "proposed_menu_items": [
                {"name": "Antipasto Misto", "description": "Selection of Italian cured meats and cheeses", "course": "appetizer"},
                {"name": "Risotto ai Porcini", "description": "Creamy risotto with wild mushrooms", "course": "primo"},
                {"name": "Osso Buco", "description": "Braised veal shanks with saffron risotto", "course": "secondo"},
                {"name": "Tiramisu", "description": "Classic Italian dessert with espresso", "course": "dessert"}
            ],
            "includes_appetizers": True,
            "includes_main_course": True,
            "includes_dessert": True,
            "includes_beverages": False,
            "price_per_person": 85.0,
            "minimum_people": 2,
            "maximum_people": 8,
            "vegetarian_options": True,
            "vegan_options": False,
            "gluten_free_options": True,
            "allergen_info": ["dairy", "gluten", "eggs"],
            "special_accommodations": "Can accommodate dietary restrictions with 24-hour notice",
            "available_dates": available_dates,
            "preparation_time_hours": 3,
            "advance_notice_hours": 48,
            "delivery_available": True,
            "pickup_available": True,
            "dine_in_available": False,
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
        }

        success, data = self.make_request('POST', 'special-orders/create', special_order_data, 200)
        
        if success:
            self.special_order_id = data.get('id')
            title = data.get('title', 'unknown')
            price = data.get('price_per_person', 0)
            details = f"- Order ID: {self.special_order_id}, Title: {title}, Price: ${price}/person"
        else:
            details = ""
            
        return self.log_test("Create Special Order", success, details)

    def test_get_special_orders(self):
        """Test getting all special orders"""
        success, data = self.make_request('GET', 'special-orders')
        
        if success:
            orders_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {orders_count} special orders"
            if orders_count > 0:
                first_order = data[0]
                details += f", First: {first_order.get('title', 'unknown')}"
        else:
            details = ""
            
        return self.log_test("Get Special Orders", success, details)

    def test_get_special_orders_with_filters(self):
        """Test getting special orders with various filters"""
        # Test with cuisine filter
        success, data = self.make_request('GET', 'special-orders?cuisine_style=Italian&max_price=100')
        
        if success:
            filtered_count = len(data) if isinstance(data, list) else 0
            details = f"- Found {filtered_count} Italian orders under $100/person"
        else:
            details = ""
            
        return self.log_test("Get Special Orders with Filters", success, details)

    def test_get_special_order_details(self):
        """Test getting detailed information about a specific special order"""
        if not self.special_order_id:
            return self.log_test("Get Special Order Details", False, "- No special order ID available")

        success, data = self.make_request('GET', f'special-orders/{self.special_order_id}')
        
        if success:
            title = data.get('title', 'unknown')
            restaurant_name = data.get('restaurant_name', 'unknown')
            views_count = data.get('views_count', 0)
            details = f"- Title: {title}, Restaurant: {restaurant_name}, Views: {views_count}"
        else:
            details = ""
            
        return self.log_test("Get Special Order Details", success, details)

    def test_book_special_order(self):
        """Test booking a special order"""
        if not self.special_order_id or not self.token:
            return self.log_test("Book Special Order", False, "- Missing special order ID or auth token")

        from datetime import datetime, timedelta
        
        # Use tomorrow's date for booking
        booking_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT18:00:00Z')

        booking_data = {
            "booking_type": "special_order",
            "special_order_id": self.special_order_id,
            "booking_date": booking_date,
            "number_of_guests": 4,
            "service_type": "delivery",
            "delivery_address": "456 Oak Avenue, New York, NY 10002",
            "dietary_restrictions": ["vegetarian"],
            "special_requests": "Please include extra bread",
            "guest_message": "Looking forward to this special dinner!"
        }

        success, data = self.make_request('POST', f'special-orders/{self.special_order_id}/book', booking_data, 200)
        
        if success:
            self.special_order_booking_id = data.get('id')
            total_amount = data.get('total_amount', 0)
            confirmation_code = data.get('confirmation_code', 'unknown')
            details = f"- Booking ID: {self.special_order_booking_id}, Total: ${total_amount}, Code: {confirmation_code}"
        else:
            details = ""
            
        return self.log_test("Book Special Order", success, details)

    def test_special_order_validation_scenarios(self):
        """Test validation scenarios for special orders"""
        if not self.special_order_id or not self.token:
            return self.log_test("Special Order Validation", False, "- Missing special order ID or auth token")

        from datetime import datetime, timedelta
        
        # Test booking with invalid guest count (too few)
        booking_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT18:00:00Z')
        
        invalid_booking_data = {
            "booking_type": "special_order",
            "special_order_id": self.special_order_id,
            "booking_date": booking_date,
            "number_of_guests": 1,  # Below minimum of 2
            "service_type": "delivery",
            "delivery_address": "456 Oak Avenue, New York, NY 10002"
        }

        success, data = self.make_request('POST', f'special-orders/{self.special_order_id}/book', invalid_booking_data, 400)
        
        if success:  # Success means we got the expected 400 error
            details = "- Correctly rejected booking with invalid guest count"
        else:
            details = "- Failed to validate guest count properly"
            
        return self.log_test("Special Order Validation", success, details)

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
        
        # Traditional Restaurant Marketplace tests
        print("\n🏪 Testing Traditional Restaurant Marketplace...")
        self.test_traditional_restaurant_vendor_application()
        self.test_admin_approve_vendor_application()
        self.test_create_traditional_restaurant_profile()
        self.test_get_traditional_restaurants()
        self.test_get_traditional_restaurants_with_filters()
        
        print("\n📋 Testing Special Orders...")
        self.test_create_special_order()
        self.test_get_special_orders()
        self.test_get_special_orders_with_filters()
        self.test_get_special_order_details()
        self.test_book_special_order()
        self.test_special_order_validation_scenarios()
        
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
    print(f"Testing against: https://foodie-share.preview.emergentagent.com")
    print()
    
    tester = LambaliaEnhancedAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())