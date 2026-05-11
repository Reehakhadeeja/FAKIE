#!/usr/bin/env python3
"""
Test the complete job analyzer functionality
"""
import sys
import os
import logging
import re
import pickle
from datetime import datetime
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import required libraries
try:
    import requests
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
    logging.info("BeautifulSoup4 and requests imported successfully")
except ImportError as e:
    BS4_AVAILABLE = False
    logging.error(f"Failed to import scraping libraries: {e}")

# Constants for analysis
FRAUD_KEYWORDS = [
    "bank account", "advance fee", "wire transfer", "western union",
    "money mule", "earn from home", "no experience needed", "guaranteed income",
    "pay registration", "whatsapp only", "urgent hiring", "₹50,000/day",
    "instant payment", "no interview", "work from mobile",
]
SUSPICIOUS_KEYWORDS = [
    "gmail.com", "yahoo.com", "work from home", "no degree required",
    "earn extra income", "part time unlimited", "immediate joining",
    "salary negotiable", "contact on whatsapp",
]
LEGIT_KEYWORDS = [
    "interview process", "ats", "background check", "equity",
    "health insurance", "401k", "pf", "esic", "annual leave",
    "probation period", "glassdoor", "linkedin", "careers page",
]

def _extract_title_from_url(url: str) -> str:
    """Extract job title from URL slug if present"""
    try:
        clean = url.split("?")[0].rstrip("/")
        path = clean.split("/")[-1]
        if len(path) > 5 and "-" in path and not path.isdigit():
            parts = path.split("-")
            parts = [p for p in parts if not p.isdigit()]
            if parts:
                return " ".join(parts).title()
        return ""
    except Exception:
        return ""

def _extract_domain(url: str) -> str:
    """Extract a readable company-like name from the URL domain"""
    try:
        domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
        name = domain.rsplit(".", 1)[0]
        return name.title()
    except Exception:
        return "Unknown Company"

def is_valid_job_url(url: str) -> tuple[bool, str]:
    """Validate URL and return (is_valid, error_message)"""
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

def _fetch_job_page(url: str) -> dict:
    """Fetch a job posting URL and extract content"""
    logging.info(f"Starting to fetch URL: {url}")
    
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
        logging.info(f"Making HTTP request to {url}")
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        content_length = len(resp.text)
        logging.info(f"Successfully fetched {content_length} characters from {url}")
        
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extract job title
        title = _extract_title_from_url(url)
        logging.info(f"Title from URL: {title}")

        # Try og:title meta tag
        if not title:
            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = og_title.get("content", "").strip()
                logging.info(f"Title from og:title: {title}")

        # Try common HTML selectors
        if not title:
            selectors = [
                "h1.job-title", "h1.topcard__title", "h1",
                "[class*='job-title']", "[class*='jobtitle']",
                "[data-testid='job-title']", ".jobsearch-JobInfoHeader-title",
            ]
            for sel in selectors:
                el = soup.select_one(sel)
                if el and el.get_text(strip=True):
                    title = el.get_text(strip=True)
                    logging.info(f"Title from selector '{sel}': {title}")
                    break

        # Extract company name
        company = ""

        # Try og:site_name
        og_site = soup.find("meta", property="og:site_name")
        if og_site:
            val = og_site.get("content", "").strip()
            if val and val.lower() not in ["linkedin", "indeed", "naukri", "glassdoor"]:
                company = val
                logging.info(f"Company from og:site_name: {company}")

        # Try common selectors
        if not company:
            selectors = [
                ".topcard__org-name-link",
                ".jobsearch-InlineCompanyRating",
                "[class*='company-name']",
                "[class*='employer-name']",
                "[data-testid='company-name']",
            ]
            for sel in selectors:
                el = soup.select_one(sel)
                if el and el.get_text(strip=True):
                    company = el.get_text(strip=True)
                    logging.info(f"Company from selector '{sel}': {company}")
                    break

        # Fallback: use domain name as company
        if not company:
            company = _extract_domain(url)
            logging.info(f"Company from domain: {company}")

        # Extract job description text
        job_desc_selectors = [
            "[class*='job-description']",
            "[class*='description']",
            "[data-testid='job-description']",
            ".jobsearch-jobDescriptionText",
        ]
        
        job_text = ""
        for sel in job_desc_selectors:
            el = soup.select_one(sel)
            if el:
                job_text = el.get_text(separator=" ", strip=True)
                logging.info(f"Job description from selector '{sel}': {len(job_text)} chars")
                break
        
        # If no specific description found, use full page text
        if not job_text or len(job_text) < 200:
            full_text = soup.get_text(separator=" ", strip=True)
            job_text = full_text[:5000]
            logging.info(f"Using full page text: {len(job_text)} chars")

        result = {
            "title": title or _extract_title_from_url(url) or "Unknown Position",
            "company": company,
            "text": job_text,
            "success": True,
            "error": None,
            "content_length": len(job_text)
        }
        
        logging.info(f"Successfully extracted: title='{result['title']}', company='{result['company']}', text_length={result['content_length']}")
        return result

    except requests.exceptions.Timeout:
        error_msg = "Request timeout after 15 seconds"
        logging.error(f"Timeout fetching {url}: {error_msg}")
        return {"title": _extract_title_from_url(url), "company": _extract_domain(url), "text": "", "success": False, "error": error_msg}
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error: {str(e)}"
        logging.error(f"Connection error fetching {url}: {error_msg}")
        return {"title": _extract_title_from_url(url), "company": _extract_domain(url), "text": "", "success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(f"Error fetching {url}: {error_msg}")
        return {"title": _extract_title_from_url(url), "company": _extract_domain(url), "text": "", "success": False, "error": error_msg}

def _rule_based_analysis(text: str, url: str) -> dict:
    """Analyze text using keyword rules and URL signals"""
    text_lower = text.lower()

    fraud_hits = [kw for kw in FRAUD_KEYWORDS if kw in text_lower]
    susp_hits  = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]
    legit_hits = [kw for kw in LEGIT_KEYWORDS if kw in text_lower]

    fraud_score = len(fraud_hits) * 15 + len(susp_hits) * 5 - len(legit_hits) * 8

    # URL trust signals
    trusted_domains = [
        "linkedin.com", "indeed.com", "naukri.com", "glassdoor.com",
        "amazon.jobs", "google.com", "microsoft.com", "infosys.com",
    ]
    url_trusted = any(d in url.lower() for d in trusted_domains)
    if url_trusted:
        fraud_score -= 20

    # Classify
    if fraud_score >= 20:
        status = "Fraud"
        confidence = min(0.98, 0.75 + fraud_score / 200)
        risk_score = min(98, 70 + fraud_score)
    elif fraud_score >= 5:
        status = "Suspicious"
        confidence = 0.70  # Fixed instead of random
        risk_score = 50     # Fixed instead of random
    else:
        status = "Legit"
        confidence = min(0.97, 0.80 + len(legit_hits) * 0.03 + (0.10 if url_trusted else 0))
        risk_score = max(5, 25 - len(legit_hits) * 3)

    # Build red flags
    red_flags = []
    if fraud_hits:
        red_flags += [f'Contains phrase: "{kw}"' for kw in fraud_hits[:3]]
    if "gmail" in text_lower or "yahoo" in text_lower:
        red_flags.append("Free email provider used as contact")
    if len(text) < 300:
        red_flags.append("Very short / vague job description")
    if not url_trusted and "http" in url:
        red_flags.append("Job posted on unknown/unverified domain")

    # Build positive signals
    pos_signals = []
    if url_trusted:
        pos_signals.append("Trusted job platform detected")
    if legit_hits:
        pos_signals += [f'Mentions: "{kw}"' for kw in legit_hits[:3]]
    if len(text) > 800:
        pos_signals.append("Detailed job description provided")

    detail_map = {
        "Legit":      "Analysis complete. The job posting shows strong authenticity signals. The description is detailed, the platform is reputable, and no deceptive patterns were detected.",
        "Suspicious": "Moderate risk detected. Some patterns in this posting match common job scam characteristics. Verify the company independently before sharing personal information.",
        "Fraud":      "HIGH RISK — Multiple fraud indicators found in this posting. Do NOT share personal or financial information. Report this listing to the job platform.",
    }

    return {
        "status":      status,
        "confidence":  confidence,
        "risk_score":  risk_score,
        "details":     detail_map[status],
        "red_flags":   red_flags[:5],
        "pos_signals": pos_signals[:6],
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

def analyze_job_url(url: str) -> dict:
    """Main analysis function"""
    logging.info(f"Starting analysis for URL: {url}")
    
    # Step 0: Validate URL
    is_valid, error_msg = is_valid_job_url(url)
    if not is_valid:
        logging.error(f"URL validation failed: {error_msg}")
        return {
            "status": "Error",
            "confidence": 0.0,
            "risk_score": 100,
            "title": "Invalid URL",
            "company": "Unknown",
            "details": f"Unable to analyze this job posting: {error_msg}",
            "red_flags": [f"URL validation failed: {error_msg}"],
            "pos_signals": [],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "error": error_msg
        }

    if not BS4_AVAILABLE:
        logging.error("BeautifulSoup4 not available")
        return {
            "status": "Error",
            "confidence": 0.0,
            "risk_score": 100,
            "title": "Scraping Unavailable",
            "company": "Unknown",
            "details": "Web scraping libraries are not available. Please install beautifulsoup4.",
            "red_flags": ["Scraping libraries not installed"],
            "pos_signals": [],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "error": "BeautifulSoup4 not available"
        }

    # Step 1: Fetch the page
    page = _fetch_job_page(url)
    
    if not page["success"]:
        logging.error(f"Failed to fetch page: {page['error']}")
        return {
            "status": "Error",
            "confidence": 0.0,
            "risk_score": 100,
            "title": page["title"] or "Unable to Fetch",
            "company": page["company"] or "Unknown",
            "details": f"Unable to fetch or analyze this job posting: {page['error']}",
            "red_flags": [f"Failed to fetch job content: {page['error']}"],
            "pos_signals": [],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "error": page["error"]
        }

    title   = page["title"] or _extract_title_from_url(url) or (_extract_domain(url) + " Position")
    company = page["company"] or _extract_domain(url)
    text    = page.get("text", "")
    
    # Check if we got meaningful content
    if len(text) < 50:
        logging.warning(f"Very little content extracted: {len(text)} characters")
        return {
            "status": "Error",
            "confidence": 0.0,
            "risk_score": 100,
            "title": title,
            "company": company,
            "details": "Unable to extract meaningful job description content from the URL. The page may be protected, require login, or use JavaScript rendering.",
            "red_flags": ["No job description content could be extracted"],
            "pos_signals": [],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "error": "Insufficient content extracted"
        }

    logging.info(f"Extracted {len(text)} characters of job content")

    # Step 2: Rule-based analysis
    rule_result = _rule_based_analysis(text, url)
    logging.info(f"Rule-based analysis result: {rule_result['status']} with confidence {rule_result['confidence']:.2f}")

    result = {
        "status":      rule_result["status"],
        "confidence":  rule_result["confidence"],
        "risk_score":  rule_result["risk_score"],
        "title":       title,
        "company":     company,
        "details":     rule_result["details"],
        "red_flags":   rule_result["red_flags"],
        "pos_signals": rule_result["pos_signals"],
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "content_length": len(text),
        "url_received": url,
        "scraping_success": page["success"]
    }
    
    logging.info(f"Final analysis result: {result['status']} with {result['confidence']:.1%} confidence")
    return result

def test_job_analyzer():
    """Test the job analyzer with the Amazon URL"""
    print("=== Job Analyzer Test ===")
    
    # Test with the Amazon job URL from the user's example
    test_url = "https://www.amazon.jobs/en/jobs/3177897/data-engineer-ii-gtmo-data"
    
    print(f"Testing URL: {test_url}")
    print()
    
    result = analyze_job_url(test_url)
    
    print("=== ANALYSIS RESULTS ===")
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Title: {result['title']}")
    print(f"Company: {result['company']}")
    print(f"Content Length: {result.get('content_length', 0)} characters")
    print(f"Scraping Success: {result.get('scraping_success', False)}")
    print()
    print("Details:")
    print(result['details'])
    print()
    
    if result.get('red_flags'):
        print("Red Flags:")
        for flag in result['red_flags']:
            print(f"  - {flag}")
        print()
    
    if result.get('pos_signals'):
        print("Positive Signals:")
        for signal in result['pos_signals']:
            print(f"  + {signal}")
        print()
    
    if result.get('error'):
        print(f"Error: {result['error']}")
    
    return result['status'] != "Error"

if __name__ == "__main__":
    success = test_job_analyzer()
    
    if success:
        print("\n🎉 Job Analyzer test completed successfully!")
        print("✅ The analyzer is now working with real scraped content!")
    else:
        print("\n❌ Job Analyzer test failed!")
