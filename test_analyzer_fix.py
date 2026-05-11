#!/usr/bin/env python3
"""
Test script to verify the analyzer fixes work correctly
"""
import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_imports():
    """Test that all required imports work"""
    print("=== Testing Imports ===")
    
    try:
        # Test basic imports
        import streamlit as st
        print("✓ Streamlit imported")
        
        import requests
        print("✓ Requests imported")
        
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup4 imported")
        
        # Test analysis modules
        from analysis.rule_engine import RuleBasedAnalyzer, rule_analyzer, _rule_based_analysis
        print("✓ Rule engine imported")
        
        from analysis.scraper import JobScraper, job_scraper, is_valid_job_url, _fetch_job_page
        print("✓ Job scraper imported")
        
        from analysis.validator import AnalysisValidator, validator
        print("✓ Validator imported")
        
        # Test utils imports
        from utils import bi, simulate_analysis, _rule_based_analysis as utils_rule_analysis
        print("✓ Utils functions imported")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_rule_based_analysis():
    """Test rule-based analysis function"""
    print("\n=== Testing Rule-Based Analysis ===")
    
    try:
        from analysis.rule_engine import _rule_based_analysis
        
        # Test with sample text
        sample_text = """
        We are looking for a Data Engineer to join our team at Amazon. 
        This position requires 5+ years of experience in data engineering, 
        strong Python skills, and experience with AWS. 
        We offer competitive salary, health insurance, and 401k.
        The interview process includes technical screening and team interviews.
        """
        
        result = _rule_based_analysis(sample_text, "https://amazon.jobs/example")
        
        print(f"✓ Analysis completed successfully")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Risk Score: {result['risk_score']}")
        print(f"  Red Flags: {len(result.get('red_flags', []))}")
        print(f"  Positive Signals: {len(result.get('pos_signals', []))}")
        
        return True
        
    except Exception as e:
        print(f"✗ Rule-based analysis failed: {e}")
        return False

def test_scraper():
    """Test job scraper functionality"""
    print("\n=== Testing Job Scraper ===")
    
    try:
        from analysis.scraper import is_valid_job_url, _extract_title_from_url, _extract_domain
        
        # Test URL validation
        test_url = "https://www.amazon.jobs/en/jobs/3177897/data-engineer-ii-gtmo-data"
        is_valid, error = is_valid_job_url(test_url)
        
        if is_valid:
            print(f"✓ URL validation passed for: {test_url[:50]}...")
        else:
            print(f"✗ URL validation failed: {error}")
            return False
        
        # Test title extraction
        title = _extract_title_from_url(test_url)
        print(f"✓ Title extracted: {title}")
        
        # Test domain extraction
        domain = _extract_domain(test_url)
        print(f"✓ Domain extracted: {domain}")
        
        return True
        
    except Exception as e:
        print(f"✗ Scraper test failed: {e}")
        return False

def test_validator():
    """Test startup validator"""
    print("\n=== Testing Validator ===")
    
    try:
        from analysis.validator import validator
        
        result = validator.run_full_validation()
        
        if result['valid']:
            print("✅ All validations passed")
            print(f"  Successes: {len(result['successes'])}")
            print(f"  Warnings: {len(result['warnings'])}")
            print(f"  Errors: {len(result['errors'])}")
        else:
            print("❌ Validation failed")
            for error in result['errors']:
                print(f"  Error: {error}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Validator test failed: {e}")
        return False

def test_manual_text_analysis():
    """Test manual text analysis like the Analyze Text button"""
    print("\n=== Testing Manual Text Analysis ===")
    
    try:
        # Simulate the Analyze Text functionality
        from utils import simulate_analysis, _rule_based_analysis
        
        # Sample job description
        jd_text = """
        We are hiring a Senior Software Engineer at Google!
        
        Requirements:
        - 5+ years of software development experience
        - Strong programming skills in Python, Java, or C++
        - Bachelor's degree in Computer Science or related field
        - Experience with cloud platforms (AWS, GCP, Azure)
        
        Benefits:
        - Competitive salary and equity
        - Health, dental, and vision insurance
        - 401(k) matching
        - Flexible work hours
        - Professional development opportunities
        
        Our interview process includes:
        1. Technical screening
        2. On-site interviews
        3. Team lunch
        4. Background check
        
        Apply at careers.google.com
        """
        
        manual_title = "Senior Software Engineer"
        manual_company = "Google"
        
        # Create mock URL for analysis
        mock_url = f"manual_text_entry_{len(jd_text)}"
        
        # Get base analysis result
        result = simulate_analysis(mock_url)
        
        # Override with manual entries and use rule-based analysis on actual text
        result["title"] = manual_title or "Manual Entry"
        result["company"] = manual_company or "User Provided"
        
        # Use rule-based analysis on the actual text
        rule_result = _rule_based_analysis(jd_text, "manual_entry")
        result["status"] = rule_result["status"]
        result["confidence"] = rule_result["confidence"]
        result["risk_score"] = rule_result["risk_score"]
        result["details"] = "Analysis based on manually provided job description text."
        result["red_flags"] = rule_result["red_flags"]
        result["pos_signals"] = rule_result["pos_signals"]
        
        print(f"✓ Manual text analysis completed")
        print(f"  Title: {result['title']}")
        print(f"  Company: {result['company']}")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Risk Score: {result['risk_score']}")
        print(f"  Red Flags: {len(result.get('red_flags', []))}")
        print(f"  Positive Signals: {len(result.get('pos_signals', []))}")
        
        return True
        
    except Exception as e:
        print(f"✗ Manual text analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing SniffJob Analyzer Fixes")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Rule-Based Analysis", test_rule_based_analysis),
        ("Job Scraper", test_scraper),
        ("Validator", test_validator),
        ("Manual Text Analysis", test_manual_text_analysis),
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
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The analyzer fixes are working correctly.")
        print("✅ The 'Analyze Text' button should now work without NameError.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
