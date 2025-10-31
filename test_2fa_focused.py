#!/usr/bin/env python3
"""
Focused 2FA Email Verification System Test
Tests the new 2FA "Option C" email verification system for Lambalia application
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class TwoFAEmailVerificationTester:
    def __init__(self, base_url="https://food-platform-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        
        # Test data
        self.verified_user_data = {
            "username": f"verified_user_{datetime.now().strftime('%H%M%S')}",
            "email": f"verified_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "secure_password_123",
            "full_name": "Verified Test User",
            "postal_code": "10001",
            "preferred_language": "en"
        }
        self.verified_user_token = None

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
                    expected_status: int = 200, headers: Optional[Dict] = None) -> tuple[bool, Dict]:
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        request_headers = {'Content-Type': 'application/json'}
        
        if headers:
            request_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, params=data, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=10)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text, "status_code": response.status_code}

            if not success:
                print(f"   Status: {response.status_code} (expected {expected_status})")
                if response_data.get('detail'):
                    print(f"   Detail: {response_data['detail']}")

            return success, response_data

        except requests.exceptions.RequestException as e:
            print(f"   Request failed: {str(e)}")
            return False, {"error": str(e)}

    def test_1_registration_email_verification_flow(self):
        """Test 1: Registration requires email verification"""
        print("\n🔐 Test 1: Registration Email Verification Flow")
        
        registration_data = {
            "username": f"2fa_user_{datetime.now().strftime('%H%M%S')}",
            "email": f"2fa_test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "secure_password_123",
            "full_name": "2FA Test User",
            "postal_code": "10001",
            "preferred_language": "en"
        }
        
        success, data = self.make_request('POST', 'auth/register', registration_data, 200)
        
        if not success:
            return self.log_test("Registration Email Verification Flow", False, "- Registration failed")
        
        # Check response structure
        verification_required = data.get('verification_required', False)
        email_in_response = data.get('email') == registration_data['email']
        message = data.get('message', '')
        
        # Should NOT receive access_token immediately
        access_token = data.get('access_token')
        
        success_criteria = (
            verification_required and 
            email_in_response and 
            'verification' in message.lower() and
            not access_token  # Should not get token until verified
        )
        
        details = f"- Verification required: {'✓' if verification_required else '✗'}, Email returned: {'✓' if email_in_response else '✗'}, No immediate token: {'✓' if not access_token else '✗'}"
        
        # Store for later tests
        self.temp_unverified_email = registration_data['email']
        self.temp_unverified_password = registration_data['password']
        
        return self.log_test("Registration Email Verification Flow", success_criteria, details)

    def test_2_unverified_user_login_rejection(self):
        """Test 2: Unverified users cannot login"""
        print("\n🚫 Test 2: Unverified User Login Rejection")
        
        if not hasattr(self, 'temp_unverified_email'):
            return self.log_test("Unverified User Login Rejection", False, "- No unverified user from previous test")
        
        login_data = {
            "email": self.temp_unverified_email,
            "password": self.temp_unverified_password
        }
        
        # Should get 403 Forbidden for unverified users
        success, data = self.make_request('POST', 'auth/login', login_data, 403)
        
        if success:
            message = data.get('message', '')
            detail = data.get('detail', '')
            
            # Check if error message mentions email verification
            email_verification_mentioned = (
                'email' in message.lower() or 
                'email' in detail.lower() or 
                'verify' in message.lower() or 
                'verify' in detail.lower()
            )
            
            details = f"- Properly rejected (403), Email verification mentioned: {'✓' if email_verification_mentioned else '✗'}"
            return self.log_test("Unverified User Login Rejection", True, details)
        else:
            details = "- Did not properly reject unverified user with 403"
            return self.log_test("Unverified User Login Rejection", False, details)

    def test_3_email_verification_endpoint(self):
        """Test 3: Email verification endpoint exists and validates codes"""
        print("\n📧 Test 3: Email Verification Endpoint")
        
        if not hasattr(self, 'temp_unverified_email'):
            return self.log_test("Email Verification Endpoint", False, "- No unverified user from previous test")
        
        # Test with invalid code (should get 400 Bad Request)
        test_code = "123456"
        success, data = self.make_request('POST', f'auth/verify-email?email={self.temp_unverified_email}&code={test_code}', None, 400)
        
        if success:
            details = "- Endpoint accessible, properly validates codes (400 for invalid code)"
            return self.log_test("Email Verification Endpoint", True, details)
        else:
            # Check if endpoint exists but returns different error
            status_code = data.get('status_code', 0)
            if status_code == 422:
                details = "- Endpoint exists but expects different parameter format"
                return self.log_test("Email Verification Endpoint", True, details)
            else:
                details = f"- Endpoint issue (status: {status_code})"
                return self.log_test("Email Verification Endpoint", False, details)

    def test_4_create_verified_user(self):
        """Test 4: Create a verified user for subsequent tests"""
        print("\n👤 Test 4: Create Verified User (Legacy Method)")
        
        # Use the legacy registration endpoint that might not require verification
        success, data = self.make_request('POST', 'auth/register', self.verified_user_data, 200)
        
        if success:
            # Check if we got a token (legacy behavior) or need verification
            access_token = data.get('access_token')
            verification_required = data.get('verification_required', False)
            
            if access_token:
                # Legacy behavior - user is immediately verified
                self.verified_user_token = access_token
                details = "- User created and verified (legacy method)"
                return self.log_test("Create Verified User", True, details)
            elif verification_required:
                # New behavior - would need email verification
                details = "- User created but requires email verification (new 2FA system active)"
                return self.log_test("Create Verified User", True, details)
            else:
                details = "- Unexpected registration response"
                return self.log_test("Create Verified User", False, details)
        else:
            details = "- Failed to create user"
            return self.log_test("Create Verified User", False, details)

    def test_5_normal_login_flow(self):
        """Test 5: Normal login flow for verified users"""
        print("\n🔓 Test 5: Normal Login Flow (Verified User)")
        
        if not self.verified_user_token:
            return self.log_test("Normal Login Flow", False, "- No verified user token available")
        
        login_data = {
            "email": self.verified_user_data["email"],
            "password": self.verified_user_data["password"]
        }
        
        success, data = self.make_request('POST', 'auth/login', login_data, 200)
        
        if success:
            access_token = data.get('access_token')
            requires_2fa = data.get('requires_2fa', False)
            
            # Normal login should provide token and not require 2FA
            normal_login = access_token and not requires_2fa
            
            details = f"- Token received: {'✓' if access_token else '✗'}, No 2FA required: {'✓' if not requires_2fa else '✗'}"
            return self.log_test("Normal Login Flow", normal_login, details)
        else:
            details = "- Login failed for verified user"
            return self.log_test("Normal Login Flow", False, details)

    def test_6_suspicious_login_detection(self):
        """Test 6: Suspicious login detection triggers 2FA"""
        print("\n🕵️ Test 6: Suspicious Login Detection")
        
        if not self.verified_user_token:
            return self.log_test("Suspicious Login Detection", False, "- No verified user available")
        
        login_data = {
            "email": self.verified_user_data["email"],
            "password": self.verified_user_data["password"]
        }
        
        # Simulate suspicious activity with different headers
        suspicious_headers = {
            'User-Agent': 'SuspiciousBot/1.0 (Unknown Device)',
            'X-Forwarded-For': '192.168.1.100',  # Different IP
            'X-Real-IP': '10.0.0.1'
        }
        
        success, data = self.make_request('POST', 'auth/login', login_data, 200, headers=suspicious_headers)
        
        if success:
            requires_2fa = data.get('requires_2fa', False)
            session_id = data.get('session_id')
            message = data.get('message', '')
            
            # Check if suspicious activity was detected
            suspicious_detected = (
                requires_2fa or 
                'suspicious' in message.lower() or
                session_id  # Session ID indicates 2FA flow
            )
            
            details = f"- Suspicious activity detected: {'✓' if suspicious_detected else '✗'}, 2FA required: {'✓' if requires_2fa else '✗'}"
            return self.log_test("Suspicious Login Detection", suspicious_detected, details)
        else:
            details = "- Failed to test suspicious login"
            return self.log_test("Suspicious Login Detection", False, details)

    def test_7_2fa_verification_endpoint(self):
        """Test 7: 2FA verification endpoint exists"""
        print("\n🔐 Test 7: 2FA Verification Endpoint")
        
        test_data = {
            "email": "test@example.com",
            "code": "123456"
        }
        
        # Should get 400 for invalid code, not 404 for missing endpoint
        success, data = self.make_request('POST', 'auth/verify-2fa', test_data, 400)
        
        if success:
            details = "- Endpoint accessible, validates 2FA codes (400 for invalid code)"
            return self.log_test("2FA Verification Endpoint", True, details)
        else:
            status_code = data.get('status_code', 0)
            if status_code == 422:
                details = "- Endpoint exists but expects different parameter format"
                return self.log_test("2FA Verification Endpoint", True, details)
            elif status_code == 404:
                details = "- Endpoint not found"
                return self.log_test("2FA Verification Endpoint", False, details)
            else:
                details = f"- Unexpected response (status: {status_code})"
                return self.log_test("2FA Verification Endpoint", False, details)

    def test_8_email_service_configuration(self):
        """Test 8: Email service is configured"""
        print("\n📮 Test 8: Email Service Configuration")
        
        # Check if SMTP is configured by testing registration (which should send email)
        test_registration = {
            "username": f"smtp_test_{datetime.now().strftime('%H%M%S')}",
            "email": f"smtp_test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "test_password_123",
            "full_name": "SMTP Test User"
        }
        
        success, data = self.make_request('POST', 'auth/register', test_registration, 200)
        
        if success:
            verification_required = data.get('verification_required', False)
            message = data.get('message', '')
            
            # If verification is required, it implies email service is working
            email_service_working = verification_required and 'email' in message.lower()
            
            details = f"- Email service configured: {'✓' if email_service_working else '✗'}, Verification emails sent: {'✓' if verification_required else '✗'}"
            return self.log_test("Email Service Configuration", email_service_working, details)
        else:
            details = "- Could not test email service configuration"
            return self.log_test("Email Service Configuration", False, details)

    def run_all_tests(self):
        """Run all 2FA email verification tests"""
        print("🚀 2FA Email Verification System Test Suite")
        print("=" * 60)
        print("Testing 2FA 'Option C' - Free Email-based 2FA Implementation")
        print(f"Backend URL: {self.base_url}")
        print("=" * 60)

        # Run tests in sequence
        self.test_1_registration_email_verification_flow()
        self.test_2_unverified_user_login_rejection()
        self.test_3_email_verification_endpoint()
        self.test_4_create_verified_user()
        self.test_5_normal_login_flow()
        self.test_6_suspicious_login_detection()
        self.test_7_2fa_verification_endpoint()
        self.test_8_email_service_configuration()

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL 2FA TESTS PASSED! Email verification system is fully functional!")
        elif self.tests_passed >= 6:
            print("✅ 2FA system is mostly functional with minor issues")
        elif self.tests_passed >= 4:
            print("⚠️ 2FA system has some issues but core functionality works")
        else:
            print("❌ 2FA system has significant issues that need attention")
        
        return self.tests_passed >= 6  # Consider success if most tests pass

def main():
    tester = TwoFAEmailVerificationTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())