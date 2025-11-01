#!/usr/bin/env python3
"""
Focused test for Resend Verification Code Feature
"""

import requests
import sys
import json
from datetime import datetime
import time

class ResendVerificationTester:
    def __init__(self, base_url="https://food-platform-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def make_request(self, method: str, endpoint: str, data=None, expected_status: int = 200):
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

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

    def test_resend_verification_complete_flow(self):
        """Test complete resend verification flow"""
        print("🔄 Testing Resend Verification Code Feature - Complete Flow")
        print("=" * 70)
        
        # Step 1: Create a user registration
        timestamp = datetime.now().strftime('%H%M%S%f')
        test_user_data = {
            "username": f"resend_test_{timestamp}",
            "email": f"resend_test_{timestamp}@example.com",
            "password": "testpass123",
            "full_name": "Resend Test User",
            "postal_code": "12345",
            "preferred_language": "en"
        }
        
        print(f"1. Registering user: {test_user_data['email']}")
        reg_success, reg_data = self.make_request('POST', 'auth/register', test_user_data, 200)
        
        if not reg_success:
            print("❌ User registration failed")
            return False
            
        if not reg_data.get('verification_required'):
            print("❌ Registration should require verification")
            return False
            
        print("✅ User registration successful - verification required")
        
        # Step 2: Test resend verification code
        print(f"2. Testing resend verification for: {test_user_data['email']}")
        resend_endpoint = f'auth/resend-verification?email={test_user_data["email"]}&code_type=registration'
        
        resend_success, resend_data = self.make_request('POST', resend_endpoint, None, 200)
        
        if not resend_success:
            print("❌ Resend verification failed")
            return False
            
        print("✅ Resend verification successful")
        print(f"   Message: {resend_data.get('message', 'N/A')}")
        print(f"   Email: {resend_data.get('email', 'N/A')}")
        print(f"   Code Type: {resend_data.get('code_type', 'N/A')}")
        
        # Step 3: Test rate limiting
        print("3. Testing rate limiting (immediate second request)")
        rate_limit_success, rate_limit_data = self.make_request('POST', resend_endpoint, None, 429)
        
        if rate_limit_success:
            print("✅ Rate limiting working correctly")
            print(f"   Error: {rate_limit_data.get('detail', 'N/A')}")
        else:
            print("❌ Rate limiting not working as expected")
            
        # Step 4: Test with suspicious_login code type
        print("4. Testing suspicious_login code type")
        suspicious_endpoint = f'auth/resend-verification?email={test_user_data["email"]}&code_type=suspicious_login'
        
        # Wait a bit to avoid rate limiting
        time.sleep(2)
        
        suspicious_success, suspicious_data = self.make_request('POST', suspicious_endpoint, None, 200)
        
        if suspicious_success:
            print("✅ Suspicious login code type working")
            print(f"   Message: {suspicious_data.get('message', 'N/A')}")
            print(f"   Code Type: {suspicious_data.get('code_type', 'N/A')}")
        else:
            print("❌ Suspicious login code type failed")
            
        # Step 5: Test non-existent email
        print("5. Testing non-existent email")
        nonexistent_email = f"nonexistent_{timestamp}@example.com"
        nonexistent_endpoint = f'auth/resend-verification?email={nonexistent_email}&code_type=registration'
        
        nonexistent_success, nonexistent_data = self.make_request('POST', nonexistent_endpoint, None, 404)
        
        if nonexistent_success:
            print("✅ Non-existent email properly rejected")
            print(f"   Error: {nonexistent_data.get('detail', 'N/A')}")
        else:
            print("❌ Non-existent email handling failed")
            
        print("\n" + "=" * 70)
        print("🏁 Resend Verification Code Feature Test Complete")
        
        return True

if __name__ == "__main__":
    tester = ResendVerificationTester()
    tester.test_resend_verification_complete_flow()