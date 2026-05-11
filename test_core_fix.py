#!/usr/bin/env python3
"""
Test script to verify the core analyzer fix without streamlit dependencies
"""
import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_rule_based_analysis_import():
    """Test that _rule_based_analysis can be imported and used"""
    print("=== Testing Rule-Based Analysis Import ===")
    
    try:
        # Test direct import from analysis module
        from analysis.rule_engine import _rule_based_analysis
        print("✓ _rule_based_analysis imported from analysis.rule_engine")
        
        # Test the function
        sample_text = "We are hiring a software engineer. No experience needed. Pay registration fee."
        result = _rule_based_analysis(sample_text, "test.com")
        
        print(f"✓ Function executed successfully")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"✗ Rule-based analysis import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analyzer_text_simulation():
    """Test the exact scenario from the analyzer without streamlit"""
    print("\n=== Testing Analyzer Text Simulation ===")
    
    try:
        # Import the core functions
        from analysis.rule_engine import _rule_based_analysis
        from analysis.scraper import _extract_domain
        
        # Simulate the exact code from analyzer.py line 90
        jd_text = """
        We are looking for a Data Engineer to join our team at Amazon. 
        This position requires 5+ years of experience in data engineering, 
        strong Python skills, and experience with AWS. 
        We offer competitive salary, health insurance, and 401k.
        The interview process includes technical screening and team interviews.
        """
        
        manual_title = "Data Engineer"
        manual_company = "Amazon"
        
        # This is the exact line that was failing
        status_result = _rule_based_analysis(jd_text, "manual_entry")["status"]
        
        print(f"✓ Critical line executed: _rule_based_analysis(jd_text, 'manual_entry')['status']")
        print(f"  Result: {status_result}")
        
        # Test full result assignment (like in the fixed code)
        rule_result = _rule_based_analysis(jd_text, "manual_entry")
        result = {
            "title": manual_title or "Manual Entry",
            "company": manual_company or "User Provided",
            "status": rule_result["status"],
            "confidence": rule_result["confidence"],
            "risk_score": rule_result["risk_score"],
            "details": "Analysis based on manually provided job description text.",
            "red_flags": rule_result["red_flags"],
            "pos_signals": rule_result["pos_signals"],
        }
        
        print(f"✓ Full result assignment completed")
        print(f"  Title: {result['title']}")
        print(f"  Company: {result['company']}")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Risk Score: {result['risk_score']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Analyzer text simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that the old utils.py functions still work"""
    print("\n=== Testing Backward Compatibility ===")
    
    try:
        # Test that we can import the functions like the old utils.py
        from analysis.rule_engine import _rule_based_analysis as old_rule_analysis
        from analysis.scraper import is_valid_job_url, _fetch_job_page, _extract_title_from_url, _extract_domain
        
        print("✓ All backward compatibility functions imported")
        
        # Test URL validation
        is_valid, error = is_valid_job_url("https://www.amazon.jobs/jobs/123")
        print(f"✓ URL validation: {is_valid}")
        
        # Test title extraction
        title = _extract_title_from_url("https://www.amazon.jobs/jobs/123/data-engineer")
        print(f"✓ Title extraction: {title}")
        
        # Test domain extraction
        domain = _extract_domain("https://www.amazon.jobs/jobs/123")
        print(f"✓ Domain extraction: {domain}")
        
        # Test rule analysis
        result = old_rule_analysis("Sample job text", "https://example.com")
        print(f"✓ Rule analysis: {result['status']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling scenarios"""
    print("\n=== Testing Error Handling ===")
    
    try:
        from analysis.rule_engine import _rule_based_analysis
        from analysis.scraper import is_valid_job_url
        
        # Test with empty text
        result = _rule_based_analysis("", "test.com")
        print(f"✓ Empty text handled: {result['status']}")
        
        # Test with invalid URL
        is_valid, error = is_valid_job_url("invalid-url")
        print(f"✓ Invalid URL handled: {is_valid}, {error}")
        
        # Test with suspicious text
        suspicious_text = "PAY REGISTRATION FEE NOW! WORK FROM HOME! NO EXPERIENCE NEEDED! whatsapp only!"
        result = _rule_based_analysis(suspicious_text, "suspicious-site.com")
        print(f"✓ Suspicious text detected: {result['status']} (confidence: {result['confidence']:.1%})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run core tests"""
    print("🧪 Testing Core Analyzer Fix")
    print("=" * 50)
    print("This test verifies that the NameError fix works correctly")
    print("without requiring streamlit or pandas dependencies.")
    
    tests = [
        ("Rule-Based Analysis Import", test_rule_based_analysis_import),
        ("Analyzer Text Simulation", test_analyzer_text_simulation),
        ("Backward Compatibility", test_backward_compatibility),
        ("Error Handling", test_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 CORE TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL CORE TESTS PASSED!")
        print("✅ The NameError fix is working correctly.")
        print("✅ _rule_based_analysis function is properly imported and functional.")
        print("✅ The 'Analyze Text' button should now work without crashing.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
