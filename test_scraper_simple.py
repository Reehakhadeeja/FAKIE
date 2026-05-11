#!/usr/bin/env python3
"""
Simple test script to verify the job scraper functionality without streamlit dependencies
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def test_basic_scraping():
    """Test basic web scraping capabilities"""
    print("=== Testing Basic Web Scraping ===")
    
    # Test with the Amazon job URL from the user's example
    test_url = "https://www.amazon.jobs/en/jobs/3177897/data-engineer-ii-gtmo-data"
    
    print(f"Testing URL: {test_url}")
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    
    try:
        print("Making HTTP request...")
        resp = requests.get(test_url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        content_length = len(resp.text)
        print(f"✓ Successfully fetched {content_length} characters")
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove scripts/styles
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        
        # Try to find title
        title = ""
        
        # Try og:title meta tag
        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content", "").strip()
            print(f"✓ Title from og:title: {title}")
        
        # Try h1 tags
        if not title:
            h1_tags = soup.find_all("h1")
            for h1 in h1_tags:
                text = h1.get_text(strip=True)
                if text and len(text) > 10:
                    title = text
                    print(f"✓ Title from h1: {title}")
                    break
        
        # Try to find company
        company = ""
        
        # Try og:site_name
        og_site = soup.find("meta", property="og:site_name")
        if og_site:
            val = og_site.get("content", "").strip()
            if val and val.lower() not in ["linkedin", "indeed", "naukri", "glassdoor"]:
                company = val
                print(f"✓ Company from og:site_name: {company}")
        
        # Extract job description text
        job_desc_selectors = [
            "[class*='job-description']",
            "[class*='description']",
            "[data-testid='job-description']",
            ".jobsearch-jobDescriptionText",
            ".jobs-description__content",
            "[id*='job-description']"
        ]
        
        job_text = ""
        for sel in job_desc_selectors:
            el = soup.select_one(sel)
            if el:
                job_text = el.get_text(separator=" ", strip=True)
                print(f"✓ Job description from selector '{sel}': {len(job_text)} chars")
                break
        
        # If no specific description found, use full page text
        if not job_text or len(job_text) < 200:
            full_text = soup.get_text(separator=" ", strip=True)
            job_text = full_text[:5000]
            print(f"✓ Using full page text: {len(job_text)} chars")
        
        print(f"\n=== Results ===")
        print(f"Title: {title or 'Not found'}")
        print(f"Company: {company or 'Not found'}")
        print(f"Job Description Length: {len(job_text)} characters")
        print(f"Job Description Preview: {job_text[:200]}...")
        
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Request timeout after 15 seconds")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection error: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_url_validation():
    """Test URL validation"""
    print("\n=== Testing URL Validation ===")
    
    def is_valid_job_url(url: str):
        if not url or not url.strip():
            return False, "URL cannot be empty"
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False, "Invalid URL format"
            return True, ""
        except Exception as e:
            return False, f"URL parsing error: {str(e)}"
    
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

if __name__ == "__main__":
    test_url_validation()
    success = test_basic_scraping()
    
    if success:
        print("\n🎉 Scraper test completed successfully!")
    else:
        print("\n❌ Scraper test failed!")
