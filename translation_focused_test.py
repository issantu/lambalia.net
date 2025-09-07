#!/usr/bin/env python3
"""
Focused Translation System Test for Lambalia
Tests the critical translation features as specified in the review request
"""

import requests
import json
import time

class TranslationSystemTester:
    def __init__(self):
        self.base_url = "https://foodloc-platform.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        
    def test_cultural_preservation_critical(self):
        """Test critical cultural preservation scenarios from review request"""
        print("🍽️ Testing Cultural Preservation Logic...")
        
        test_cases = [
            {
                "text": "Tonight we're making Paella Valenciana with authentic saffron",
                "target": "fr",
                "expected_preserved": "Paella Valenciana"
            },
            {
                "text": "My grandmother's Chicken Biryani recipe is the best",
                "target": "de", 
                "expected_preserved": "Biryani"
            },
            {
                "text": "This Coq au Vin needs more wine and herbs",
                "target": "es",
                "expected_preserved": "Coq au Vin"
            },
            {
                "text": "The Ratatouille was perfectly seasoned with Provençal herbs",
                "target": "ja",
                "expected_preserved": "Ratatouille"
            }
        ]
        
        preserved_count = 0
        for i, case in enumerate(test_cases, 1):
            try:
                response = requests.post(f"{self.api_url}/translate", 
                    json={
                        "text": case["text"],
                        "target_language": case["target"],
                        "preserve_cultural": True
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    translated = data.get('translated_text', '')
                    method = data.get('method', 'unknown')
                    processing_time = data.get('processing_time_ms', 0)
                    
                    if case["expected_preserved"] in translated:
                        preserved_count += 1
                        print(f"  ✅ Test {i}: {case['expected_preserved']} preserved ({method}, {processing_time:.1f}ms)")
                    else:
                        print(f"  ❌ Test {i}: {case['expected_preserved']} NOT preserved")
                        print(f"     Original: {case['text']}")
                        print(f"     Translated: {translated}")
                else:
                    print(f"  ❌ Test {i}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Test {i}: Error - {str(e)}")
        
        print(f"  📊 Cultural Preservation: {preserved_count}/{len(test_cases)} terms preserved")
        return preserved_count == len(test_cases)
    
    def test_service_integration(self):
        """Test AI service connectivity and fallback behavior"""
        print("\n🔧 Testing Service Integration...")
        
        # Test AI service connectivity
        try:
            response = requests.post(f"{self.api_url}/translate",
                json={
                    "text": "Testing AI service connectivity",
                    "target_language": "es",
                    "preserve_cultural": True
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                method = data.get('method', 'unknown')
                print(f"  ✅ AI Service: Connected (method: {method})")
                ai_working = True
            else:
                print(f"  ❌ AI Service: HTTP {response.status_code}")
                ai_working = False
                
        except Exception as e:
            print(f"  ❌ AI Service: Error - {str(e)}")
            ai_working = False
        
        # Test service stats
        try:
            response = requests.get(f"{self.api_url}/translate/stats", timeout=10)
            if response.status_code == 200:
                stats = response.json().get('stats', {})
                total_requests = stats.get('total_requests', 0)
                ai_usage = stats.get('ai_usage_rate', 0)
                cache_rate = stats.get('cache_hit_rate', 0)
                print(f"  ✅ Service Stats: {total_requests} requests, {ai_usage}% AI usage, {cache_rate}% cache hit")
            else:
                print(f"  ❌ Service Stats: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ Service Stats: Error - {str(e)}")
        
        return ai_working
    
    def test_performance_and_caching(self):
        """Test response times and caching effectiveness"""
        print("\n⚡ Testing Performance and Caching...")
        
        test_text = "This is a performance test for the translation caching system"
        
        # First request (no cache)
        start_time = time.time()
        try:
            response1 = requests.post(f"{self.api_url}/translate",
                json={
                    "text": test_text,
                    "target_language": "fr",
                    "preserve_cultural": True
                },
                timeout=10
            )
            first_request_time = (time.time() - start_time) * 1000
            
            if response1.status_code == 200:
                data1 = response1.json()
                processing_time1 = data1.get('processing_time_ms', 0)
                cache_hit1 = data1.get('cache_hit', False)
                print(f"  ✅ First Request: {first_request_time:.1f}ms total, {processing_time1:.1f}ms processing, cache: {cache_hit1}")
            else:
                print(f"  ❌ First Request: HTTP {response1.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ First Request: Error - {str(e)}")
            return False
        
        # Second request (should be cached)
        start_time = time.time()
        try:
            response2 = requests.post(f"{self.api_url}/translate",
                json={
                    "text": test_text,
                    "target_language": "fr", 
                    "preserve_cultural": True
                },
                timeout=10
            )
            second_request_time = (time.time() - start_time) * 1000
            
            if response2.status_code == 200:
                data2 = response2.json()
                processing_time2 = data2.get('processing_time_ms', 0)
                cache_hit2 = data2.get('cache_hit', False)
                print(f"  ✅ Second Request: {second_request_time:.1f}ms total, {processing_time2:.1f}ms processing, cache: {cache_hit2}")
                
                # Verify caching worked
                if cache_hit2 and processing_time2 < processing_time1:
                    print(f"  ✅ Caching: Effective ({processing_time1:.1f}ms → {processing_time2:.1f}ms)")
                    return True
                else:
                    print(f"  ⚠️ Caching: May not be working optimally")
                    return False
            else:
                print(f"  ❌ Second Request: HTTP {response2.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Second Request: Error - {str(e)}")
            return False
    
    def test_language_support(self):
        """Test support for 70+ languages"""
        print("\n🌍 Testing Language Support...")
        
        try:
            response = requests.get(f"{self.api_url}/translate/supported-languages", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                languages = data.get('languages', [])
                total_languages = data.get('total_languages', 0)
                
                # Check for key languages mentioned in review
                language_codes = [lang.get('code') for lang in languages]
                key_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko', 'zh', 'ar', 'hi', 'ru']
                supported_key_languages = [code for code in key_languages if code in language_codes]
                
                print(f"  ✅ Total Languages: {total_languages}")
                print(f"  ✅ Key Languages Supported: {len(supported_key_languages)}/{len(key_languages)}")
                
                if total_languages >= 70:
                    print(f"  ✅ Language Requirement: Met (70+ languages)")
                    return True
                else:
                    print(f"  ⚠️ Language Requirement: {total_languages} < 70 languages")
                    return False
            else:
                print(f"  ❌ Language Support: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Language Support: Error - {str(e)}")
            return False
    
    def test_batch_processing_efficiency(self):
        """Test batch processing efficiency"""
        print("\n📦 Testing Batch Processing...")
        
        # Test with recipe snippets as mentioned in review
        recipe_snippets = [
            "Start by heating olive oil in a large paella pan",
            "Add the Bomba rice and stir for 2 minutes", 
            "Pour in the saffron-infused stock slowly",
            "Let the Paella rest for 5 minutes before serving",
            "Garnish with fresh lemon wedges and parsley"
        ]
        
        try:
            start_time = time.time()
            response = requests.post(f"{self.api_url}/translate/batch",
                json={
                    "texts": recipe_snippets,
                    "target_language": "es",
                    "preserve_cultural": True
                },
                timeout=15
            )
            batch_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                successful = data.get('successful_translations', 0)
                total_texts = data.get('total_texts', 0)
                total_chars = data.get('total_characters', 0)
                
                print(f"  ✅ Batch Processing: {successful}/{total_texts} texts, {total_chars} chars, {batch_time:.1f}ms")
                
                # Check if cultural terms are preserved in batch
                translations = data.get('translations', [])
                cultural_preserved = any('Paella' in t.get('translated_text', '') for t in translations)
                if cultural_preserved:
                    print(f"  ✅ Cultural Preservation in Batch: Working")
                
                return successful == total_texts
            else:
                print(f"  ❌ Batch Processing: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Batch Processing: Error - {str(e)}")
            return False
    
    def run_focused_tests(self):
        """Run all focused translation tests"""
        print("🌐 Lambalia AI-Powered Translation System - Focused Testing")
        print("=" * 70)
        
        results = []
        
        # Run critical tests from review request
        results.append(("Cultural Preservation", self.test_cultural_preservation_critical()))
        results.append(("Service Integration", self.test_service_integration()))
        results.append(("Performance & Caching", self.test_performance_and_caching()))
        results.append(("Language Support (70+)", self.test_language_support()))
        results.append(("Batch Processing", self.test_batch_processing_efficiency()))
        
        # Summary
        print("\n" + "=" * 70)
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"📊 Focused Test Results: {passed}/{total} critical areas passed")
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} {test_name}")
        
        if passed == total:
            print("\n🎉 All critical translation features are working correctly!")
            print("✅ Zero language barriers achieved with cultural authenticity preserved")
            return True
        else:
            print(f"\n⚠️ {total - passed} critical areas need attention")
            return False

if __name__ == "__main__":
    tester = TranslationSystemTester()
    success = tester.run_focused_tests()
    exit(0 if success else 1)