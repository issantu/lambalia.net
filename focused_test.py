#!/usr/bin/env python3
"""
Focused test for Enhanced African Cuisine Database and Payment Processing Features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend_test import LambaliaEnhancedAPITester

def main():
    """Run focused tests for the review request"""
    print("🎯 Enhanced African Cuisine Database and Payment Processing Test Suite")
    print("=" * 80)
    
    tester = LambaliaEnhancedAPITester()
    print(f"Testing against: {tester.base_url}")
    print()
    
    # Basic setup
    print("🔧 Setting up test environment...")
    tester.test_health_check()
    tester.test_user_registration()
    tester.test_user_login()
    
    # Enhanced African Cuisine Database Tests
    print("\n🌍 Testing Enhanced African Cuisine Database...")
    tester.test_enhanced_african_cuisine_native_recipes()
    tester.test_enhanced_african_cuisine_reference_recipes()
    tester.test_enhanced_african_cuisine_countries_endpoint()
    tester.test_enhanced_african_cuisine_authentic_dishes()
    
    # Enhanced Grocery Payment Processing Tests
    print("\n💳 Testing Enhanced Grocery Payment Processing...")
    tester.test_enhanced_grocery_payment_processing_search()
    tester.test_enhanced_grocery_payment_delivery_options()
    tester.test_enhanced_grocery_commission_calculations()
    
    # Integration Verification Tests
    print("\n🔗 Testing Integration Verification...")
    tester.test_grocery_ingredient_suggestions_integration()
    tester.test_african_cuisine_data_serving_integration()
    tester.test_grocery_payment_data_structure_integration()
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All enhanced features tests passed!")
        return 0
    else:
        failed_count = tester.tests_run - tester.tests_passed
        print(f"⚠️  {failed_count} tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())