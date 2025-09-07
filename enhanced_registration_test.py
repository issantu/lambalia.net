#!/usr/bin/env python3
"""
Enhanced User Registration System Test Suite
Tests the new registration system with phone number requirement and 2FA integration
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class EnhancedRegistrationTester:
    def __init__(self, base_url="https://local-food-market.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        
        # Test data for different scenarios
        self.timestamp = datetime.now().strftime('%H%M%S')
        
        # Valid registration data with phone number
        self.valid_user_data = {
            "username": f"testuser_{self.timestamp}",
            "email": f"test_{self.timestamp}@example.com",
            "password": "SecurePass123!",
            "phone_number": f"+1555012{self.timestamp[-4:]}",
            "full_name": "Test User Enhanced",
            "postal_code": "10001",
            "preferred_language": "en",
            "native_dishes": "Jollof Rice, Egusi Soup",
            "consultation_specialties": "Nigerian cuisine, West African dishes",
            "cultural_background": "Nigerian",
            "enable_2fa": False
        }
        
        # Test data for 2FA enabled registration
        self.user_with_2fa_data = {
            "username": f"testuser2fa_{self.timestamp}",
            "email": f"test2fa_{self.timestamp}@example.com", 
            "password": "SecurePass123!",
            "phone_number": f"+1555013{self.timestamp[-4:]}",
            "full_name": "Test User 2FA",
            "postal_code": "10001",
            "preferred_language": "en",
            "enable_2fa": True
        }

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
                response_data = {"raw_response": response.text, "status_code": response.status_code}

            if not success:
                print(f"   Status: {response.status_code} (expected {expected_status})")
                print(f"   Response: {response_data}")

            return success, response_data

        except requests.exceptions.RequestException as e:
            print(f"   Request failed: {str(e)}")
            return False, {"error": str(e)}

    def test_registration_with_phone_number_required(self):
        """Test that phone number is required for registration"""
        # Test registration without phone number (should fail)
        invalid_data = self.valid_user_data.copy()
        del invalid_data['phone_number']
        
        success, data = self.make_request('POST', 'auth/register', invalid_data, 422)
        
        if success:
            details = "- Correctly rejected registration without phone number"
        else:
            details = "- Failed to enforce phone number requirement"
            
        return self.log_test("Registration Phone Number Required", success, details)

    def test_registration_with_valid_phone_number(self):
        """Test successful registration with valid phone number"""
        success, data = self.make_request('POST', 'auth/register', self.valid_user_data, 200)
        
        if success:
            self.token = data.get('access_token')
            user_data = data.get('user', {})
            self.user_id = user_data.get('id')
            phone_number = user_data.get('phone_number')
            
            # Verify phone number is included in response
            phone_included = phone_number == self.valid_user_data['phone_number']
            details = f"- User ID: {self.user_id}, Phone: {phone_number}, Token: {'✓' if self.token else '✗'}"
            
            if not phone_included:
                success = False
                details += " - Phone number not properly returned"
        else:
            details = ""
            
        return self.log_test("Registration with Valid Phone Number", success, details)

    def test_phone_number_uniqueness_validation(self):
        """Test that duplicate phone numbers are rejected"""
        # Try to register another user with the same phone number
        duplicate_phone_data = {
            "username": f"duplicate_{self.timestamp}",
            "email": f"duplicate_{self.timestamp}@example.com",
            "password": "AnotherPass123!",
            "phone_number": self.valid_user_data['phone_number'],  # Same phone number
            "full_name": "Duplicate Phone User"
        }
        
        success, data = self.make_request('POST', 'auth/register', duplicate_phone_data, 400)
        
        if success:
            error_message = data.get('detail', '')
            phone_error = 'phone number' in error_message.lower() or 'already registered' in error_message.lower()
            details = f"- Correctly rejected duplicate phone: {error_message}"
            if not phone_error:
                success = False
                details = f"- Wrong error message: {error_message}"
        else:
            details = "- Failed to reject duplicate phone number"
            
        return self.log_test("Phone Number Uniqueness Validation", success, details)

    def test_registration_with_2fa_enabled(self):
        """Test registration with 2FA enabled creates security profile"""
        success, data = self.make_request('POST', 'auth/register', self.user_with_2fa_data, 200)
        
        if success:
            token = data.get('access_token')
            user_data = data.get('user', {})
            user_id = user_data.get('id')
            
            # Store for later tests
            self.token_2fa = token
            self.user_id_2fa = user_id
            
            details = f"- 2FA User ID: {user_id}, Token: {'✓' if token else '✗'}"
        else:
            details = ""
            
        return self.log_test("Registration with 2FA Enabled", success, details)

    def test_2fa_security_profile_creation(self):
        """Test that 2FA registration creates security profile"""
        if not hasattr(self, 'token_2fa'):
            return self.log_test("2FA Security Profile Creation", False, "- No 2FA user token available")
        
        # Check 2FA status for the user registered with 2FA enabled
        headers = {'Authorization': f'Bearer {self.token_2fa}'}
        
        success, data = self.make_request('GET', 'auth/2fa-status')
        
        if success:
            # For new registration with enable_2fa=True, security profile should exist but 2FA not yet enabled
            # (user needs to complete setup process)
            setup_required = data.get('setup_required', True)
            available_methods = data.get('available_methods', [])
            
            profile_exists = not setup_required or len(available_methods) > 0
            details = f"- Setup required: {setup_required}, Available methods: {available_methods}"
        else:
            details = ""
            profile_exists = False
            
        # Restore original token
        return self.log_test("2FA Security Profile Creation", profile_exists, details)

    def test_registration_without_2fa(self):
        """Test registration with 2FA disabled (default behavior)"""
        # The first user was registered with enable_2fa=False
        if not self.token:
            return self.log_test("Registration without 2FA", False, "- No user token available")
        
        success, data = self.make_request('GET', 'auth/2fa-status')
        
        if success:
            twofa_enabled = data.get('twofa_enabled', False)
            setup_required = data.get('setup_required', True)
            
            # For user with enable_2fa=False, 2FA should not be enabled and setup should be required
            no_2fa_setup = not twofa_enabled and setup_required
            details = f"- 2FA enabled: {twofa_enabled}, Setup required: {setup_required}"
        else:
            details = ""
            no_2fa_setup = False
            
        return self.log_test("Registration without 2FA", no_2fa_setup, details)

    def test_user_profile_includes_phone_number(self):
        """Test that user profile response includes phone number"""
        if not self.token:
            return self.log_test("User Profile Includes Phone Number", False, "- No user token available")
        
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            phone_number = data.get('phone_number')
            expected_phone = self.valid_user_data['phone_number']
            
            phone_matches = phone_number == expected_phone
            details = f"- Profile phone: {phone_number}, Expected: {expected_phone}"
            
            if not phone_matches:
                success = False
                details += " - Phone number mismatch"
        else:
            details = ""
            
        return self.log_test("User Profile Includes Phone Number", success, details)

    def test_jwt_token_contains_correct_user_data(self):
        """Test that JWT token is valid and contains correct user data"""
        if not self.token:
            return self.log_test("JWT Token Contains Correct User Data", False, "- No token available")
        
        # Test token by making authenticated request
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            username = data.get('username')
            email = data.get('email')
            user_id = data.get('id')
            
            # Verify data matches registration
            data_matches = (
                username == self.valid_user_data['username'] and
                email == self.valid_user_data['email'] and
                user_id == self.user_id
            )
            
            details = f"- Username: {username}, Email: {email}, ID: {user_id}"
            
            if not data_matches:
                success = False
                details += " - User data mismatch"
        else:
            details = ""
            
        return self.log_test("JWT Token Contains Correct User Data", success, details)

    def test_database_user_creation_with_phone(self):
        """Test that user is properly created in database with phone number"""
        if not self.token:
            return self.log_test("Database User Creation with Phone", False, "- No user token available")
        
        # Get user profile to verify database storage
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            # Check all expected fields are present
            required_fields = ['id', 'username', 'email', 'phone_number', 'full_name']
            fields_present = all(field in data for field in required_fields)
            
            # Check heritage fields if provided
            heritage_fields = ['native_dishes', 'consultation_specialties', 'cultural_background']
            heritage_present = any(field in data and data[field] for field in heritage_fields)
            
            details = f"- Required fields: {'✓' if fields_present else '✗'}, Heritage fields: {'✓' if heritage_present else '✗'}"
            
            if not fields_present:
                success = False
        else:
            details = ""
            
        return self.log_test("Database User Creation with Phone", success, details)

    def test_duplicate_email_validation(self):
        """Test that duplicate emails are still rejected (existing functionality)"""
        duplicate_email_data = {
            "username": f"duplicate_email_{self.timestamp}",
            "email": self.valid_user_data['email'],  # Same email
            "password": "AnotherPass123!",
            "phone_number": f"+1555099{self.timestamp[-4:]}",  # Different phone
            "full_name": "Duplicate Email User"
        }
        
        success, data = self.make_request('POST', 'auth/register', duplicate_email_data, 400)
        
        if success:
            error_message = data.get('detail', '')
            details = f"- Correctly rejected duplicate email: {error_message}"
        else:
            details = "- Failed to reject duplicate email"
            
        return self.log_test("Duplicate Email Validation", success, details)

    def test_duplicate_username_validation(self):
        """Test that duplicate usernames are still rejected (existing functionality)"""
        duplicate_username_data = {
            "username": self.valid_user_data['username'],  # Same username
            "email": f"different_{self.timestamp}@example.com",
            "password": "AnotherPass123!",
            "phone_number": f"+1555088{self.timestamp[-4:]}",  # Different phone
            "full_name": "Duplicate Username User"
        }
        
        success, data = self.make_request('POST', 'auth/register', duplicate_username_data, 400)
        
        if success:
            error_message = data.get('detail', '')
            details = f"- Correctly rejected duplicate username: {error_message}"
        else:
            details = "- Failed to reject duplicate username"
            
        return self.log_test("Duplicate Username Validation", success, details)

    def test_registration_validation_edge_cases(self):
        """Test various validation edge cases"""
        test_cases = [
            {
                "name": "Empty phone number",
                "data": {**self.valid_user_data, "phone_number": "", "username": f"empty_phone_{self.timestamp}", "email": f"empty_phone_{self.timestamp}@example.com"},
                "expected_status": 422
            },
            {
                "name": "Invalid phone format",
                "data": {**self.valid_user_data, "phone_number": "invalid-phone", "username": f"invalid_phone_{self.timestamp}", "email": f"invalid_phone_{self.timestamp}@example.com"},
                "expected_status": 422
            },
            {
                "name": "Missing required fields",
                "data": {"username": f"minimal_{self.timestamp}", "email": f"minimal_{self.timestamp}@example.com"},
                "expected_status": 422
            }
        ]
        
        passed_cases = 0
        
        for case in test_cases:
            success, data = self.make_request('POST', 'auth/register', case["data"], case["expected_status"])
            if success:
                passed_cases += 1
        
        details = f"- {passed_cases}/{len(test_cases)} validation cases passed"
        return self.log_test("Registration Validation Edge Cases", passed_cases == len(test_cases), details)

    def test_enhanced_login_with_phone_user(self):
        """Test enhanced login works with phone-registered user"""
        if not self.user_id:
            return self.log_test("Enhanced Login with Phone User", False, "- No registered user available")
        
        login_data = {
            "email": self.valid_user_data["email"],
            "password": self.valid_user_data["password"]
        }
        
        success, data = self.make_request('POST', 'auth/login', login_data, 200)
        
        if success:
            login_success = data.get('success', False)
            requires_2fa = data.get('requires_2fa', False)
            access_token = data.get('access_token')
            user_data = data.get('user', {})
            
            # For user without 2FA, login should succeed immediately
            login_works = login_success and not requires_2fa and access_token
            details = f"- Success: {login_success}, Requires 2FA: {requires_2fa}, Token: {'✓' if access_token else '✗'}"
            
            # Verify user data includes phone number
            if login_works and user_data:
                phone_in_response = user_data.get('phone_number') == self.valid_user_data['phone_number']
                if not phone_in_response:
                    login_works = False
                    details += " - Phone number missing from login response"
        else:
            details = ""
            login_works = False
            
        return self.log_test("Enhanced Login with Phone User", login_works, details)

    def test_user_response_model_includes_phone(self):
        """Test that UserResponse model includes phone_number field"""
        if not self.token:
            return self.log_test("UserResponse Model Includes Phone", False, "- No user token available")
        
        success, data = self.make_request('GET', 'users/me')
        
        if success:
            # Check that phone_number is in the response and not None/empty
            phone_number = data.get('phone_number')
            phone_field_exists = phone_number is not None and phone_number != ""
            
            # Also check other expected fields are still present
            expected_fields = ['id', 'username', 'email', 'phone_number', 'full_name', 'created_at']
            all_fields_present = all(field in data for field in expected_fields)
            
            details = f"- Phone field: {'✓' if phone_field_exists else '✗'}, All fields: {'✓' if all_fields_present else '✗'}"
            
            success = phone_field_exists and all_fields_present
        else:
            details = ""
            
        return self.log_test("UserResponse Model Includes Phone", success, details)

    def run_all_tests(self):
        """Run all enhanced registration tests"""
        print("🧪 ENHANCED USER REGISTRATION SYSTEM TESTS")
        print("=" * 60)
        
        # Core registration tests
        self.test_registration_with_phone_number_required()
        self.test_registration_with_valid_phone_number()
        self.test_phone_number_uniqueness_validation()
        
        # 2FA integration tests
        self.test_registration_with_2fa_enabled()
        self.test_2fa_security_profile_creation()
        self.test_registration_without_2fa()
        
        # User profile and response tests
        self.test_user_profile_includes_phone_number()
        self.test_jwt_token_contains_correct_user_data()
        self.test_database_user_creation_with_phone()
        self.test_user_response_model_includes_phone()
        
        # Validation tests
        self.test_duplicate_email_validation()
        self.test_duplicate_username_validation()
        self.test_registration_validation_edge_cases()
        
        # Login integration tests
        self.test_enhanced_login_with_phone_user()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 ENHANCED REGISTRATION TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL ENHANCED REGISTRATION TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME ENHANCED REGISTRATION TESTS FAILED")
            return False

def main():
    """Main test execution"""
    print("Starting Enhanced User Registration System Tests...")
    
    tester = EnhancedRegistrationTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()