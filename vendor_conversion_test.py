#!/usr/bin/env python3
"""
Vendor Conversion Hub Backend Test Suite
Tests backend functionality that supports the vendor conversion hub integration
Focus areas: Authentication, User Management, Vendor Application Endpoints
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class VendorConversionTester:
    def __init__(self, base_url="https://cuisine-finder-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.test_user_data = {
            "username": f"vendor_test_{datetime.now().strftime('%H%M%S')}",
            "email": f"vendor_test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "VendorTest123!",
            "full_name": "Vendor Test User",
            "postal_code": "10001",
            "preferred_language": "en",
            "native_dishes": "Pasta Carbonara, Risotto Milanese",
            "consultation_specialties": "Italian cuisine, Traditional cooking methods",
            "cultural_background": "Italian"
        }
        self.tests_run = 0
        self.tests_passed = 0
        self.vendor_application_id = None

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
                response = requests.get(url, headers=headers, params=data, timeout=10)
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

    def test_server_health(self):
        """Test basic server health check"""
        success, data = self.make_request('GET', 'health')
        if success:
            status = data.get('status', 'unknown')
            service = data.get('service', 'unknown')
            details = f"- Status: {status}, Service: {service}"
        else:
            details = ""
        return self.log_test("Server Health Check", success, details)

    def test_user_registration_with_heritage_fields(self):
        """Test user registration with heritage/cultural fields for vendor conversion"""
        success, data = self.make_request('POST', 'auth/register', self.test_user_data, 200)
        
        if success:
            self.token = data.get('access_token')
            user_data = data.get('user', {})
            self.user_id = user_data.get('id')
            username = user_data.get('username', 'unknown')
            details = f"- User ID: {self.user_id}, Username: {username}, Token: {'✓' if self.token else '✗'}"
        else:
            details = ""
            
        return self.log_test("User Registration with Heritage Fields", success, details)

    def test_enhanced_login_flow(self):
        """Test enhanced login flow that supports 2FA"""
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        success, data = self.make_request('POST', 'auth/login', login_data, 200)
        
        if success:
            login_success = data.get('success', False)
            requires_2fa = data.get('requires_2fa', False)
            new_token = data.get('access_token')
            user_data = data.get('user', {})
            details = f"- Login success: {login_success}, 2FA required: {requires_2fa}, Token: {'✓' if new_token else '✗'}"
            # Update token for subsequent tests
            if new_token:
                self.token = new_token
        else:
            details = ""
            
        return self.log_test("Enhanced Login Flow", success, details)

    def test_user_profile_access(self):
        """Test user profile access for profile page functionality"""
        if not self.token:
            return self.log_test("User Profile Access", False, "- No auth token available")
            
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            username = data.get('username', 'unknown')
            email = data.get('email', 'unknown')
            is_vendor = data.get('is_vendor', False)
            native_dishes = data.get('native_dishes', '')
            cultural_bg = data.get('cultural_background', '')
            details = f"- User: {username}, Vendor: {is_vendor}, Heritage data: {'✓' if native_dishes else '✗'}"
        else:
            details = ""
            
        return self.log_test("User Profile Access", success, details)

    def test_2fa_status_check(self):
        """Test 2FA status endpoint for security features"""
        if not self.token:
            return self.log_test("2FA Status Check", False, "- No auth token available")
            
        success, data = self.make_request('GET', 'auth/2fa-status')
        
        if success:
            twofa_enabled = data.get('twofa_enabled', False)
            available_methods = data.get('available_methods', [])
            setup_required = data.get('setup_required', True)
            details = f"- 2FA enabled: {twofa_enabled}, Methods: {len(available_methods)}, Setup required: {setup_required}"
        else:
            details = ""
            
        return self.log_test("2FA Status Check", success, details)

    def test_vendor_application_submission(self):
        """Test vendor application submission for home restaurant"""
        if not self.token:
            return self.log_test("Vendor Application Submission", False, "- No auth token available")

        application_data = {
            "vendor_type": "home_restaurant",
            "legal_name": "Maria Rossi",
            "phone_number": "+1-555-0123",
            "address": "123 Vendor Street",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
            "background_check_consent": True,
            "has_food_handling_experience": True,
            "years_cooking_experience": 10,
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
            next_steps = data.get('next_steps', 'unknown')
            details = f"- Application ID: {self.vendor_application_id}, Type: {vendor_type}, Status: {status}"
        else:
            details = ""
            
        return self.log_test("Vendor Application Submission", success, details)

    def test_vendor_application_status(self):
        """Test checking vendor application status"""
        if not self.vendor_application_id or not self.token:
            return self.log_test("Vendor Application Status", False, "- Missing application ID or auth token")

        success, data = self.make_request('GET', f'vendor/application/{self.vendor_application_id}')
        
        if success:
            status = data.get('status', 'unknown')
            vendor_type = data.get('vendor_type', 'unknown')
            application_date = data.get('application_date', 'unknown')
            documents = data.get('documents', [])
            details = f"- Status: {status}, Type: {vendor_type}, Documents: {len(documents)}"
        else:
            details = ""
            
        return self.log_test("Vendor Application Status", success, details)

    def test_heritage_data_collection(self):
        """Test heritage data collection endpoints for cultural background"""
        if not self.token:
            return self.log_test("Heritage Data Collection", False, "- No auth token available")

        success, data = self.make_request('GET', 'heritage/user-contributions')
        
        if success:
            total_contributors = data.get('total_contributors', 0)
            cultural_backgrounds = data.get('cultural_backgrounds', {})
            top_dishes = data.get('top_native_dishes', {})
            details = f"- Contributors: {total_contributors}, Backgrounds: {len(cultural_backgrounds)}, Top dishes: {len(top_dishes)}"
        else:
            details = ""
            
        return self.log_test("Heritage Data Collection", success, details)

    def test_dishes_by_culture(self):
        """Test getting dishes by cultural background"""
        cultural_background = "Italian"
        
        success, data = self.make_request('GET', f'heritage/dishes-by-culture/{cultural_background}')
        
        if success:
            total_contributors = data.get('total_contributors', 0)
            dishes = data.get('dishes', [])
            total_dishes = data.get('total_dishes', 0)
            details = f"- {cultural_background} contributors: {total_contributors}, Dishes: {total_dishes}"
        else:
            details = ""
            
        return self.log_test("Dishes by Culture (Italian)", success, details)

    def test_global_dishes_access(self):
        """Test access to global dishes database for vendor training"""
        success, data = self.make_request('GET', 'heritage/global-dishes')
        
        if success:
            dishes_count = len(data) if isinstance(data, list) else 0
            # Check for variety of cuisines
            cuisines_found = set()
            if data and isinstance(data, list):
                for dish in data[:20]:  # Check first 20 dishes
                    if isinstance(dish, dict) and 'cuisine_type' in dish:
                        cuisines_found.add(dish['cuisine_type'])
            
            details = f"- Total dishes: {dishes_count}, Cuisines found: {len(cuisines_found)}"
        else:
            details = ""
            
        return self.log_test("Global Dishes Access", success, details)

    def test_vendor_training_resources(self):
        """Test access to vendor training resources (heritage recipes)"""
        # Test African dishes for Home Restaurant training
        success1, data1 = self.make_request('GET', 'heritage/dishes-by-cuisine/african')
        african_dishes = len(data1) if success1 and isinstance(data1, list) else 0
        
        # Test Caribbean dishes for Quick Eats training  
        success2, data2 = self.make_request('GET', 'heritage/dishes-by-cuisine/caribbean')
        caribbean_dishes = len(data2) if success2 and isinstance(data2, list) else 0
        
        # Test Asian dishes for diversity training
        success3, data3 = self.make_request('GET', 'heritage/dishes-by-cuisine/asian')
        asian_dishes = len(data3) if success3 and isinstance(data3, list) else 0
        
        overall_success = success1 and success2 and success3
        details = f"- African: {african_dishes}, Caribbean: {caribbean_dishes}, Asian: {asian_dishes} dishes"
        
        return self.log_test("Vendor Training Resources", overall_success, details)

    def test_specialty_ingredients_access(self):
        """Test access to specialty ingredients for vendor education"""
        # Test ingredient search functionality
        success1, data1 = self.make_request('GET', 'heritage/ingredients/search?ingredient=saffron')
        saffron_results = len(data1) if success1 and isinstance(data1, list) else 0
        
        # Test rare ingredients list
        success2, data2 = self.make_request('GET', 'heritage/ingredients/rare')
        rare_ingredients = len(data2) if success2 and isinstance(data2, list) else 0
        
        overall_success = success1 and success2
        details = f"- Saffron search: {saffron_results} results, Rare ingredients: {rare_ingredients}"
        
        return self.log_test("Specialty Ingredients Access", overall_success, details)

    def test_ethnic_grocery_stores(self):
        """Test ethnic grocery store network for vendor sourcing"""
        success, data = self.make_request('GET', 'heritage/stores/nearby?postal_code=10001&radius_km=25')
        
        if success:
            stores_count = len(data) if isinstance(data, list) else 0
            # Check for store details
            store_types = set()
            if data and isinstance(data, list):
                for store in data[:10]:
                    if isinstance(store, dict) and 'specialties' in store:
                        specialties = store.get('specialties', [])
                        store_types.update(specialties)
            
            details = f"- Nearby stores: {stores_count}, Specialty types: {len(store_types)}"
        else:
            details = ""
            
        return self.log_test("Ethnic Grocery Stores", success, details)

    def test_delivery_partner_info(self):
        """Test delivery partner information access"""
        # Test farm ecosystem for delivery partnerships
        success, data = self.make_request('GET', 'heritage/stores/chains')
        
        if success:
            chains_count = len(data) if isinstance(data, list) else 0
            # Check for major chains
            chain_names = []
            if data and isinstance(data, list):
                for chain in data:
                    if isinstance(chain, dict) and 'name' in chain:
                        chain_names.append(chain['name'])
            
            has_major_chains = any(name in ['H-Mart', 'Patel Brothers', '99 Ranch Market'] for name in chain_names)
            details = f"- Store chains: {chains_count}, Major chains: {'✓' if has_major_chains else '✗'}"
        else:
            details = ""
            
        return self.log_test("Delivery Partner Info", success, details)

    def test_vendor_certification_tracking(self):
        """Test vendor certification and application tracking"""
        if not self.token:
            return self.log_test("Vendor Certification Tracking", False, "- No auth token available")

        # Check user vendor status
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            is_vendor = data.get('is_vendor', False)
            vendor_app_id = data.get('vendor_application_id')
            total_earnings = data.get('total_earnings', 0)
            details = f"- Vendor status: {is_vendor}, Application ID: {'✓' if vendor_app_id else '✗'}, Earnings: ${total_earnings}"
        else:
            details = ""
            
        return self.log_test("Vendor Certification Tracking", success, details)

    def test_authentication_security(self):
        """Test authentication security features"""
        # Test accessing protected endpoint without token
        old_token = self.token
        self.token = None
        
        success1, data1 = self.make_request('GET', 'users/me', expected_status=401)
        
        # Test with invalid token
        self.token = "invalid-token-12345"
        success2, data2 = self.make_request('GET', 'users/me', expected_status=401)
        
        # Restore valid token
        self.token = old_token
        success3, data3 = self.make_request('GET', 'users/me', expected_status=200)
        
        overall_success = success1 and success2 and success3
        details = f"- No token: {'✓' if success1 else '✗'}, Invalid token: {'✓' if success2 else '✗'}, Valid token: {'✓' if success3 else '✗'}"
        
        return self.log_test("Authentication Security", overall_success, details)

    def run_all_tests(self):
        """Run all vendor conversion hub tests"""
        print("🏪 Vendor Conversion Hub Backend Test Suite")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print()

        print("🔧 Basic Server & Authentication Tests...")
        self.test_server_health()
        self.test_user_registration_with_heritage_fields()
        self.test_enhanced_login_flow()
        self.test_user_profile_access()
        self.test_2fa_status_check()
        self.test_authentication_security()
        print()

        print("📋 Vendor Application Tests...")
        self.test_vendor_application_submission()
        self.test_vendor_application_status()
        self.test_vendor_certification_tracking()
        print()

        print("🌍 Heritage & Training Resources Tests...")
        self.test_heritage_data_collection()
        self.test_dishes_by_culture()
        self.test_global_dishes_access()
        self.test_vendor_training_resources()
        self.test_specialty_ingredients_access()
        self.test_ethnic_grocery_stores()
        self.test_delivery_partner_info()
        print()

        print("=" * 60)
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed ({success_rate:.1f}%)")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All vendor conversion hub backend tests PASSED!")
            return True
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"⚠️  {failed_tests} tests failed. Backend functionality needs attention.")
            return False

if __name__ == "__main__":
    tester = VendorConversionTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)