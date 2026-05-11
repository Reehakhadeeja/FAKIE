#!/usr/bin/env python3
"""
Test script to verify the job scraper functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import simulate_analysis, is_valid_job_url, _fetch_job_page

def test_url_validation():
    """Test URL validation function"""
    print("=== Testing URL Validation ===")
    
    test_urls = [
        ("https://www.amazon.jobs/en/jobs/3177897/data-engineer-ii-gtmo-data", True),
        ("invalid-url", False),
        ("", False),
        ("https://linkedin.com/jobs/view/12345", True),
        ("ftp://example.com/job", False)
    ]
    
    for url, expected in test_urls:
        is_valid, error = is_valid_job_url(url)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {url[:50]}... -> Valid: {is_valid}, Error: {error}")

def test_scraper():
    """Test the actual scraper with a real URL"""
    print("\n=== Testing Job Scraper ===")
    
    # Test with the Amazon job URL from the user's example
    test_url = "https://www.amazon.jobs/en/jobs/3177897/data-engineer-ii-gtmo-data"
    
    print(f"Testing URL: {test_url}")
    
    # Test the fetch function directly
    print("\n--- Testing _fetch_job_page ---")
    page_data = _fetch_job_page(test_url)
    
    print(f"Success: {page_data['success']}")
    print(f"Title: {page_data['title']}")
    print(f"Company: {page_data['company']}")
    print(f"Content Length: {len(page_data.get('text', ''))}")
    print(f"Error: {page_data.get('error', 'None')}")
    
    if page_data['text']:
        print(f"Text preview: {page_data['text'][:200]}...")
    
    # Test the full analysis
    print("\n--- Testing simulate_analysis ---")
    result = simulate_analysis(test_url)
    
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Title: {result['title']}")
    print(f"Company: {result['company']}")
    print(f"Details: {result['details'][:100]}...")
    
    if result.get('error'):
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_url_validation()
    test_scraper()
