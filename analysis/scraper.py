"""
Web scraper for job posting content extraction
"""

import logging
import re
from urllib.parse import urlparse
from typing import Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError as e:
    SCRAPER_AVAILABLE = False
    logging.error(f"Scraper libraries not available: {e}")

class JobScraper:
    """Job posting content scraper"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.title_selectors = [
            "h1.job-title", "h1.topcard__title", "h1",
            "[class*='job-title']", "[class*='jobtitle']",
            "[data-testid='job-title']", ".jobsearch-JobInfoHeader-title",
            ".job-title", ".top-card-layout__title", ".jobs-unified-top-card__job-title",
            "[class*='JobTitle']", "[class*='jobTitle']"
        ]
        
        self.company_selectors = [
            ".topcard__org-name-link",
            ".jobsearch-InlineCompanyRating",
            "[class*='company-name']",
            "[class*='employer-name']",
            "[data-testid='company-name']",
            ".jobs-unified-top-card__company-name",
            "[class*='company']",
            "[class*='employer']",
            ".company-name", ".employer-name"
        ]
        
        self.description_selectors = [
            "[class*='job-description']",
            "[class*='description']",
            "[data-testid='job-description']",
            ".jobsearch-jobDescriptionText",
            ".jobs-description__content",
            "[id*='job-description']"
        ]
    
    def validate_url(self, url: str) -> tuple[bool, str]:
        """Validate job posting URL"""
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
    
    def extract_title_from_url(self, url: str) -> str:
        """Extract job title from URL slug"""
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
    
    def extract_domain(self, url: str) -> str:
        """Extract company name from domain"""
        try:
            domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
            name = domain.rsplit(".", 1)[0]
            return name.title()
        except Exception:
            return "Unknown Company"
    
    def fetch_page(self, url: str) -> Dict:
        """Fetch and parse job posting page"""
        if not SCRAPER_AVAILABLE:
            return {
                "success": False,
                "error": "Web scraping libraries not available",
                "title": "",
                "company": "",
                "text": ""
            }
        
        logging.info(f"Fetching URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            content_length = len(response.text)
            logging.info(f"Successfully fetched {content_length} characters")
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove unnecessary elements
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            
            # Extract title
            title = self._extract_title(soup, url)
            
            # Extract company
            company = self._extract_company(soup, url)
            
            # Extract description
            text = self._extract_description(soup)
            
            result = {
                "success": True,
                "title": title,
                "company": company,
                "text": text,
                "content_length": len(text),
                "url": url
            }
            
            logging.info(f"Successfully extracted: title='{title}', company='{company}', text_length={len(text)}")
            return result
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout after 15 seconds"
            logging.error(f"Timeout fetching {url}: {error_msg}")
            return {"success": False, "error": error_msg, "title": self.extract_title_from_url(url), "company": self.extract_domain(url), "text": ""}
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            logging.error(f"Connection error fetching {url}: {error_msg}")
            return {"success": False, "error": error_msg, "title": self.extract_title_from_url(url), "company": self.extract_domain(url), "text": ""}
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {e.response.status_code}"
            logging.error(f"HTTP error fetching {url}: {error_msg}")
            return {"success": False, "error": error_msg, "title": self.extract_title_from_url(url), "company": self.extract_domain(url), "text": ""}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(f"Error fetching {url}: {error_msg}")
            return {"success": False, "error": error_msg, "title": self.extract_title_from_url(url), "company": self.extract_domain(url), "text": ""}
    
    def _extract_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract job title from page"""
        # Try URL slug first
        title = self.extract_title_from_url(url)
        logging.info(f"Title from URL: {title}")
        
        # Try og:title meta tag
        if not title:
            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = og_title.get("content", "").strip()
                logging.info(f"Title from og:title: {title}")
        
        # Try common selectors
        if not title:
            for selector in self.title_selectors:
                element = soup.select_one(selector)
                if element and element.get_text(strip=True):
                    title = element.get_text(strip=True)
                    logging.info(f"Title from selector '{selector}': {title}")
                    break
        
        return title or "Unknown Position"
    
    def _extract_company(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name from page"""
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
            for selector in self.company_selectors:
                element = soup.select_one(selector)
                if element and element.get_text(strip=True):
                    company = element.get_text(strip=True)
                    logging.info(f"Company from selector '{selector}': {company}")
                    break
        
        # Fallback to domain
        if not company:
            company = self.extract_domain(url)
            logging.info(f"Company from domain: {company}")
        
        return company
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract job description text"""
        # Try specific description selectors
        for selector in self.description_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=" ", strip=True)
                if len(text) > 200:
                    logging.info(f"Job description from selector '{selector}': {len(text)} chars")
                    return text
        
        # Fallback to full page text
        full_text = soup.get_text(separator=" ", strip=True)
        text = full_text[:5000]
        logging.info(f"Using full page text: {len(text)} chars")
        return text

# Global scraper instance
job_scraper = JobScraper()

# Backward compatibility functions
def is_valid_job_url(url: str) -> tuple[bool, str]:
    """Backward compatibility wrapper for URL validation"""
    return job_scraper.validate_url(url)

def _fetch_job_page(url: str) -> Dict:
    """Backward compatibility wrapper for page fetching"""
    return job_scraper.fetch_page(url)

def _extract_title_from_url(url: str) -> str:
    """Backward compatibility wrapper for title extraction"""
    return job_scraper.extract_title_from_url(url)

def _extract_domain(url: str) -> str:
    """Backward compatibility wrapper for domain extraction"""
    return job_scraper.extract_domain(url)
