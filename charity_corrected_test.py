#!/usr/bin/env python3
"""
Corrected Charity Program Testing
Tests the charity program endpoints with correct request formats
"""

import requests
import sys
import json
from datetime import datetime

class CharityCorrectedTester:
    def __init__(self, base_url="https://lambalia-web.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.test_user_data = {
            "username": f"charityuser_{datetime.now().strftime('%H%M%S')}",
            "email": f"charity_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "testpass123",
            "full_name": "Charity Test User",
            "postal_code": "10001",
            "preferred_language": "en"
        }
        self.charity_program_id = None
        self.activity_id = None

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        if success:
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
                response_data = {"raw_response": response.text, "status_code": response.status_code}

            if not success:
                print(f"   Status: {response.status_code} (expected {expected_status})")
                print(f"   Response: {response_data}")

            return success, response_data

        except requests.exceptions.RequestException as e:
            print(f"   Request failed: {str(e)}")
            return False, {"error": str(e)}

    def setup_user(self):
        """Register and login user"""
        print("🔧 Setting up test user...")
        
        # Register user
        success, data = self.make_request('POST', 'auth/register', self.test_user_data, 200)
        if not success:
            print("❌ Failed to register user")
            return False
            
        self.token = data.get('access_token')
        user_data = data.get('user', {})
        self.user_id = user_data.get('id')
        
        print(f"✅ User registered: {self.user_id}")
        return True

    def test_charity_program_registration(self):
        """Test charity program registration"""
        registration_data = {
            "commitment_hours_per_month": 10,
            "preferred_charity_types": ["food_bank", "community_kitchen"],
            "preferred_locations": ["10001", "10002"],
            "has_transportation": True,
            "available_days": ["saturday", "sunday"],
            "skills_offered": ["cooking", "food_preparation", "serving"],
            "previous_volunteer_experience": "Volunteered at local soup kitchen for 2 years",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "+1-555-0199"
        }

        success, data = self.make_request('POST', 'charity/register', registration_data, 200)
        
        if success:
            self.charity_program_id = data.get('program_id')
            status = data.get('status', 'unknown')
            impact_score = data.get('impact_score', 0)
            premium_tier = data.get('premium_tier', 'unknown')
            details = f"- Program ID: {self.charity_program_id}, Status: {status}, Impact: {impact_score}, Tier: {premium_tier}"
        else:
            details = ""
            
        return self.log_test("Charity Program Registration", success, details)

    def test_charity_activity_submission_corrected(self):
        """Test charity activity submission with correct format"""
        activity_data = {
            "activity_type": "food_bank",
            "charity_organization_name": "Downtown Food Bank",
            "activity_description": "Helped sort and distribute food packages to families in need",
            "activity_date": "2024-08-23",
            "food_donated_lbs": 25.0,
            "meals_provided": 50,
            "people_helped": 50,
            "volunteer_hours": 4.0,
            "location_address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "photo_urls": ["https://example.com/volunteer1.jpg"],
            "video_urls": [],
            "witness_contacts": [
                {
                    "name": "Sarah Johnson",
                    "phone": "+1-555-0123",
                    "email": "sarah@downtownfoodbank.org",
                    "role": "Volunteer Coordinator"
                }
            ]
        }

        success, data = self.make_request('POST', 'charity/submit-activity', activity_data, 200)
        
        if success:
            self.activity_id = data.get('activity_id')
            estimated_points = data.get('estimated_points', 0)
            verification_status = data.get('verification_status', 'unknown')
            total_activities = data.get('total_activities', 0)
            details = f"- Activity ID: {self.activity_id}, Points: {estimated_points}, Status: {verification_status}, Total: {total_activities}"
        else:
            details = ""
            
        return self.log_test("Charity Activity Submission (Corrected)", success, details)

    def test_community_impact_metrics(self):
        """Test community impact metrics endpoint"""
        success, data = self.make_request('GET', 'charity/community-impact', None, 200)
        
        if success:
            total_meals = data.get('total_meals_provided', 0)
            total_volunteers = data.get('total_volunteers', 0)
            total_hours = data.get('total_volunteer_hours', 0)
            total_orgs = data.get('total_organizations', 0)
            impact_score = data.get('community_impact_score', 0)
            growth_rate = data.get('monthly_growth_rate', 0)
            details = f"- Meals: {total_meals}, Volunteers: {total_volunteers}, Hours: {total_hours}, Orgs: {total_orgs}, Score: {impact_score}, Growth: {growth_rate}%"
        else:
            details = ""
            
        return self.log_test("Community Impact Metrics", success, details)

    def test_premium_membership_via_charity_corrected(self):
        """Test premium membership upgrade via charity with correct format"""
        upgrade_data = {
            "tier": "garden_supporter",  # Use string value, not object
            "payment_method": "charity_work",
            "monthly_payment_amount": 0.0,
            "charity_commitment": True
        }

        success, data = self.make_request('POST', 'charity/premium-upgrade', upgrade_data, 200)
        
        if success:
            new_tier = data.get('tier', 'unknown')
            commission_rate = data.get('new_commission_rate', 0)
            benefits = data.get('benefits', [])
            details = f"- New tier: {new_tier}, Commission: {commission_rate}%, Benefits: {len(benefits)}"
        else:
            # This might fail due to insufficient activity, which is expected
            error_detail = data.get('detail', 'Unknown error')
            details = f"- Error: {error_detail}"
            
        return self.log_test("Premium Membership via Charity (Corrected)", success, details)

    def test_impact_calculator_corrected(self):
        """Test impact calculator endpoint with GET method and query params"""
        params = {
            "activity_type": "food_bank",
            "food_donated_lbs": 25.0,
            "meals_provided": 50,
            "people_helped": 50,
            "volunteer_hours": 4.0
        }

        success, data = self.make_request('GET', 'charity/impact-calculator', params, 200)
        
        if success:
            estimated_score = data.get('estimated_impact_score', 0)
            breakdown = data.get('activity_breakdown', {})
            tier_progress = data.get('tier_progress', [])
            details = f"- Est. score: {estimated_score}, Base: {breakdown.get('base_score', 0)}, Tiers: {len(tier_progress)}"
        else:
            details = ""
            
        return self.log_test("Impact Calculator (Corrected)", success, details)

    def test_premium_benefits(self):
        """Test premium benefits endpoint"""
        success, data = self.make_request('GET', 'charity/premium-benefits', None, 200)
        
        if success:
            current_tier = data.get('current_tier', 'unknown')
            commission_rate = data.get('commission_rate', 0)
            benefits_count = data.get('benefits_count', 0)
            charity_points = data.get('charity_points_available', 0)
            details = f"- Tier: {current_tier}, Commission: {commission_rate}%, Benefits: {benefits_count}, Points: {charity_points}"
        else:
            details = ""
            
        return self.log_test("Premium Benefits", success, details)

    def run_corrected_tests(self):
        """Run corrected charity program tests"""
        print("🤝 CORRECTED CHARITY PROGRAM TESTING")
        print("=" * 60)
        
        if not self.setup_user():
            print("❌ Failed to setup user, aborting tests")
            return
        
        print("\n🔍 Testing Charity Program Endpoints with Correct Formats...")
        
        # Test charity program registration first
        self.test_charity_program_registration()
        
        # Submit some charity activity with correct format
        self.test_charity_activity_submission_corrected()
        
        # Test the previously stuck endpoints with corrections
        print("\n⚠️  Testing Previously Stuck Endpoints (Corrected):")
        self.test_community_impact_metrics()
        self.test_premium_membership_via_charity_corrected()
        self.test_impact_calculator_corrected()
        
        # Test working endpoints for comparison
        print("\n✅ Testing Working Endpoints:")
        self.test_premium_benefits()
        
        print("\n" + "=" * 60)
        print("🏁 CORRECTED CHARITY TESTING COMPLETE")

if __name__ == "__main__":
    tester = CharityCorrectedTester()
    tester.run_corrected_tests()