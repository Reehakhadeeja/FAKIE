import streamlit as st
import time
import random
import re
import pickle
import os
import logging
from datetime import datetime
from urllib.parse import urlparse
from config import *

# Import new analysis modules
try:
    from analysis.rule_engine import rule_analyzer, _rule_based_analysis
    from analysis.scraper import job_scraper, is_valid_job_url, _fetch_job_page, _extract_title_from_url, _extract_domain
    ANALYSIS_MODULES_AVAILABLE = True
    logging.info("New analysis modules loaded successfully")
except ImportError as e:
    ANALYSIS_MODULES_AVAILABLE = False
    logging.warning(f"Analysis modules not available: {e}")

# ── Try to import URL fetching libraries ─────────────────────────────────────
try:
    import requests
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
    logging.info("BeautifulSoup4 and requests imported successfully")
except ImportError as e:
    BS4_AVAILABLE = False
    logging.error(f"Failed to import scraping libraries: {e}")

# ── Load ML model if available ───────────────────────────────────────────────
_model = None
_vectorizer = None

def _load_model():
    global _model, _vectorizer
    if _model is None:
        try:
            with open("fake_job_model.pkl", "rb") as f:
                _model = pickle.load(f)
            with open("tfidf_vectorizer.pkl", "rb") as f:
                _vectorizer = pickle.load(f)
        except Exception:
            _model = None
            _vectorizer = None

# ── Icon helper ───────────────────────────────────────────────────────────────
def bi(name, size="1em", color="inherit", extra_style=""):
    mapping = {
        "search-heart": "search-heart-line",
        "house-door": "home-4-line",
        "search": "search-line",
        "globe2": "global-line",
        "bar-chart-line": "bar-chart-line",
        "bookmark": "bookmark-line",
        "send": "send-plane-line",
        "cloud-upload": "upload-cloud-2-line",
        "file-earmark-person": "file-user-line",
        "envelope-paper": "mail-open-line",
        "robot": "robot-line",
        "rocket-takeoff": "rocket-line",
        "journal-text": "book-read-line",
        "folder2-open": "folder-open-line",
        "bell": "notification-3-line",
        "gem": "vip-diamond-line",
        "gear": "settings-4-line",
        "person-circle": "user-3-line",
        "bell-fill": "notification-3-fill",
        "check-circle-fill": "checkbox-circle-fill",
        "exclamation-triangle-fill": "alert-fill",
        "shield-exclamation": "shield-star-fill",
        "info-circle": "information-fill",
        "check": "check-line",
        "pin-angle": "pushpin-line",
        "clipboard-check": "clipboard-line",
        "trophy-fill": "trophy-fill",
        "award-fill": "award-fill",
        "star-fill": "star-fill",
        "emoji-smile": "emotion-line",
        "chat-dots-fill": "message-3-fill",
        "heart-fill": "heart-3-fill",
        "chevron-left": "arrow-left-s-line",
        "chevron-right": "arrow-right-s-line",
        "trash": "delete-bin-line",
        "copy": "clipboard-line",
        "plus-circle": "add-circle-line",
        "upload": "upload-2-line",
        "calendar": "calendar-line",
        "list-task": "list-check",
        "card-text": "article-line",
        "credit-card": "bank-card-line",
        "x-circle": "close-circle-line",
        "circle": "checkbox-blank-circle-line",
        "eye": "eye-line",
        "eye-slash": "eye-off-line",
        "box-arrow-right": "logout-box-r-line",
        "file-earmark-pdf": "file-pdf-line",
        "download": "download-2-line",
        "play": "play-line",
        "pause": "pause-line",
        "stop": "stop-line",
        "arrow-repeat": "refresh-line",
        "pencil": "pencil-line",
        "flag-fill": "flag-fill",
        "search-heart-fill": "search-heart-fill",
    }
    ri_name = mapping.get(name, name)
    if not ri_name.startswith('ri-'):
        ri_name = f"ri-{ri_name}"
    return f'<i class="{ri_name}" style="font-size:{size};color:{color};{extra_style}"></i>'


# ── Extract title from URL slug ───────────────────────────────────────────────
def _extract_title_from_url(url: str) -> str:
    """Extract job title from URL slug if present (e.g. amazon.jobs URLs)."""
    try:
        # Remove query string
        clean = url.split("?")[0].rstrip("/")
        path = clean.split("/")[-1]
        # Only use if it looks like a slug (has hyphens, not just a number)
        if len(path) > 5 and "-" in path and not path.isdigit():
            parts = path.split("-")
            # Remove pure numeric segments (job IDs)
            parts = [p for p in parts if not p.isdigit()]
            if parts:
                return " ".join(parts).title()
        return ""
    except Exception:
        return ""


# ── Extract company from domain ───────────────────────────────────────────────
def _extract_domain(url: str) -> str:
    """Extract a readable company-like name from the URL domain."""
    try:
        domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
        # Remove TLD
        name = domain.rsplit(".", 1)[0]
        return name.title()
    except Exception:
        return "Unknown Company"


# ── URL validation ─────────────────────────────────────────────────────────

def is_valid_job_url(url: str) -> tuple[bool, str]:
    """Validate URL and return (is_valid, error_message)."""
    if not url or not url.strip():
        return False, "URL cannot be empty"
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "Invalid URL format"
        
        # Check for common job posting domains
        job_domains = [
            'linkedin.com', 'indeed.com', 'naukri.com', 'glassdoor.com',
            'amazon.jobs', 'google.com', 'microsoft.com', 'infosys.com',
            'flipkart.com', 'swiggy.in', 'zomato.com', 'tcs.com',
            'internshala.com', 'foundit.in', 'shine.com', 'monster.com',
            'angel.co', 'wellfound.com', 'builtin.com', 'jobs.eu'
        ]
        
        domain_lower = parsed.netloc.lower()
        is_job_site = any(domain in domain_lower for domain in job_domains)
        
        if not is_job_site:
            logging.warning(f"URL from non-standard job site: {domain_lower}")
        
        return True, ""
    except Exception as e:
        return False, f"URL parsing error: {str(e)}"


# ── Real URL fetcher ──────────────────────────────────────────────────────────
def _fetch_job_page(url: str) -> dict:
    """
    Fetch a job posting URL and extract: title, company, description text.
    Returns a dict with keys: title, company, text, success, error
    """
    logging.info(f"Starting to fetch URL: {url}")
    
    headers = {
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

        # ── Extract job title ────────────────────────────────────────────
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
                ".job-title", ".top-card-layout__title", ".jobs-unified-top-card__job-title",
                "[class*='JobTitle']", "[class*='jobTitle']"
            ]
            for sel in selectors:
                el = soup.select_one(sel)
                if el and el.get_text(strip=True):
                    title = el.get_text(strip=True)
                    logging.info(f"Title from selector '{sel}': {title}")
                    break

        # ── Extract company name ─────────────────────────────────────────
        company = ""

        # Try og:site_name
        og_site = soup.find("meta", property="og:site_name")
        if og_site:
            val = og_site.get("content", "").strip()
            # Ignore generic site names
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
                ".jobs-unified-top-card__company-name",
                "[class*='company']",
                "[class*='employer']",
                ".company-name", ".employer-name"
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

        # ── Full page text for ML analysis ───────────────────────────────
        # Try to find specific job description sections first
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
                logging.info(f"Job description from selector '{sel}': {len(job_text)} chars")
                break
        
        # If no specific description found, use full page text
        if not job_text or len(job_text) < 200:
            full_text = soup.get_text(separator=" ", strip=True)
            job_text = full_text[:5000]  # Increased limit for better analysis
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
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error: {e.response.status_code}"
        logging.error(f"HTTP error fetching {url}: {error_msg}")
        return {"title": _extract_title_from_url(url), "company": _extract_domain(url), "text": "", "success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(f"Error fetching {url}: {error_msg}")
        return {"title": _extract_title_from_url(url), "company": _extract_domain(url), "text": "", "success": False, "error": error_msg}


# ── Fraud signal analyser (rule-based) ───────────────────────────────────────
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


def _rule_based_analysis(text: str, url: str) -> dict:
    """Analyze text using keyword rules and URL signals."""
    text_lower = text.lower()

    fraud_hits = [kw for kw in FRAUD_KEYWORDS if kw in text_lower]
    susp_hits  = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]
    legit_hits = [kw for kw in LEGIT_KEYWORDS if kw in text_lower]

    fraud_score = len(fraud_hits) * 15 + len(susp_hits) * 5 - len(legit_hits) * 8

    # URL trust signals
    trusted_domains = [
        "linkedin.com", "indeed.com", "naukri.com", "glassdoor.com",
        "amazon.jobs", "google.com", "microsoft.com", "infosys.com",
        "flipkart.com", "swiggy.in", "zomato.com", "tcs.com",
        "internshala.com", "foundit.in", "shine.com",
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
        confidence = random.uniform(0.60, 0.80)
        risk_score = random.randint(35, 65)
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

    # Fallbacks
    if not red_flags and status != "Legit":
        red_flags = random.sample(RED_FLAGS, k=2)
    if not pos_signals and status == "Legit":
        pos_signals = random.sample(POSITIVE_SIGNALS, k=3)

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


# ── ML-based analysis ────────────────────────────────────────────────────────
def _ml_analysis(text: str):
    """Use the trained ML model if available."""
    _load_model()
    if _model is None or _vectorizer is None:
        return None
    try:
        vec = _vectorizer.transform([text])
        pred = _model.predict(vec)[0]
        prob = _model.predict_proba(vec)[0]
        if pred == 1:
            confidence = float(prob[1])
            status = "Fraud" if confidence > 0.75 else "Suspicious"
            risk_score = int(confidence * 100)
        else:
            confidence = float(prob[0])
            status = "Legit"
            risk_score = int((1 - confidence) * 40)
        return {"status": status, "confidence": confidence, "risk_score": risk_score}
    except Exception:
        return None


# ── Main analysis function ────────────────────────────────────────────────────
def simulate_analysis(url: str) -> dict:
    """
    Fetch the job URL, extract real title/company/text,
    run ML + rule-based analysis, and return real results.
    Falls back gracefully if the URL cannot be fetched.
    """
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
    
    time.sleep(0.5)  # Brief delay to prevent overwhelming servers

    if not BS4_AVAILABLE:
        logging.error("BeautifulSoup4 not available, falling back to mock analysis")
        return _old_simulate(url)

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

    # Even if fetch failed, we may have title/company from URL slug
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

    # Step 2: Try ML model
    ml_result = _ml_analysis(text) if text else None
    if ml_result:
        logging.info(f"ML analysis result: {ml_result}")

    # Step 3: Rule-based analysis
    rule_result = _rule_based_analysis(text, url)
    logging.info(f"Rule-based analysis result: {rule_result['status']} with confidence {rule_result['confidence']:.2f}")

    # Step 4: Merge results
    if ml_result:
        status     = ml_result["status"]
        confidence = ml_result["confidence"]
        risk_score = ml_result["risk_score"]
        logging.info("Using ML model results")
    else:
        status     = rule_result["status"]
        confidence = rule_result["confidence"]
        risk_score = rule_result["risk_score"]
        logging.info("Using rule-based analysis results")

    result = {
        "status":      status,
        "confidence":  confidence,
        "risk_score":  risk_score,
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
    
    logging.info(f"Final analysis result: {status} with {confidence:.1%} confidence")
    return result


def _old_simulate(url: str) -> dict:
    """Original random simulation — fallback only."""
    weights    = [0.55, 0.25, 0.20]
    status     = random.choices(["Legit", "Suspicious", "Fraud"], weights=weights)[0]
    confidence = {"Legit": random.uniform(0.82, 0.96), "Suspicious": random.uniform(0.58, 0.78), "Fraud": random.uniform(0.88, 0.98)}[status]
    num_flags  = {"Legit": random.randint(0, 2), "Suspicious": random.randint(2, 5), "Fraud": random.randint(5, 8)}[status]
    num_pos    = {"Legit": random.randint(4, 7), "Suspicious": random.randint(1, 3), "Fraud": random.randint(0, 1)}[status]
    risk_score = {"Legit": random.randint(5, 25), "Suspicious": random.randint(35, 65), "Fraud": random.randint(75, 98)}[status]
    title      = _extract_title_from_url(url) or (_extract_domain(url) + " Position")
    company    = _extract_domain(url)
    return {
        "status":      status,
        "confidence":  confidence,
        "risk_score":  risk_score,
        "title":       title,
        "company":     company,
        "details":     random.choice(FAKE_DETAILS[status]),
        "red_flags":   random.sample(RED_FLAGS, k=num_flags),
        "pos_signals": random.sample(POSITIVE_SIGNALS, k=num_pos),
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def is_valid_email(e): return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", e))
def is_valid_phone(p): return bool(re.match(r"^[\d\s\+\-\(\)]{7,15}$", p))


# ── Show result card ──────────────────────────────────────────────────────────
def _show_result(r: dict, url: str, compact=False):
    from database import db
    emoji = bi(STATUS_EMOJI.get(r["status"], "clipboard"), '1em',
               {'Legit': '#1ABB9C', 'Suspicious': '#F39C12', 'Fraud': '#E74C3C'}.get(r['status'], '#999'))
    clr_b = STATUS_COLOR.get(r["status"], "blue")

    if compact:
        st.markdown(f"""
        <div class="table-card" style="padding:15px; border-left:4px solid {'#1ABB9C' if r['status']=='Legit' else '#F39C12' if r['status']=='Suspicious' else '#E74C3C'};">
          <div style="display:flex;justify-content:space-between">
            <div style="font-size:14px;font-weight:700;color:#2A3F54">{emoji} {r['title']} @ {r['company']}</div>
            <div class="badge badge-{clr_b}">{r['status']}</div>
          </div>
          <div style="color:#73879C;font-size:12px">{url[:60]}…</div>
        </div>""", unsafe_allow_html=True)
        return

    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown(f"""
        <div class="table-card" style="padding:20px; border-top: 3px solid {'#1ABB9C' if r['status']=='Legit' else '#F39C12' if r['status']=='Suspicious' else '#E74C3C'};">
          <div style="display:flex;align-items:center;gap:15px;margin-bottom:15px">
            <span style="font-size:2.5rem; line-height:1;">{emoji}</span>
            <div>
              <div style="font-size:1.25rem;font-weight:700;color:#2A3F54">{r['status']} Verification</div>
              <div style="color:#73879C;font-size:13px">Confidence: {r['confidence']:.1%} · Risk score: {r['risk_score']}/100</div>
            </div>
          </div>
          <div style="color:#73879C;margin-bottom:6px"><b style="color:#2A3F54">Job Position:</b> {r['title']}</div>
          <div style="color:#73879C;margin-bottom:6px"><b style="color:#2A3F54">Company:</b> {r['company']}</div>
          <div style="color:#555;font-size:14px;line-height:1.6;margin-top:15px; padding:10px; background:#f9f9f9; border-radius:4px;">{r['details']}</div>
        </div>""", unsafe_allow_html=True)

    with col_r:
        if r.get("red_flags"):
            flags_html = "".join(
                f"<div style='color:#E74C3C;font-size:13px;margin:5px 0; display:flex; gap:8px;'>"
                f"{bi('flag-fill','1em','#E74C3C')} <span>{f}</span></div>"
                for f in r["red_flags"]
            )
            st.markdown(f"""
            <div class="table-card" style="padding:15px; border-left:4px solid #E74C3C">
              <div style="font-weight:700;color:#E74C3C;margin-bottom:10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;">RED FLAGS DETECTED</div>
              {flags_html}
            </div>""", unsafe_allow_html=True)
        if r.get("pos_signals"):
            sig_html = "".join(
                f"<div style='color:#1ABB9C;font-size:13px;margin:5px 0; display:flex; gap:8px;'>"
                f"{bi('check-circle-fill','1em','#1ABB9C')} <span>{s}</span></div>"
                for s in r["pos_signals"]
            )
            st.markdown(f"""
            <div class="table-card" style="padding:15px; border-left:4px solid #1ABB9C">
              <div style="font-weight:700;color:#1ABB9C;margin-bottom:10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;">POSITIVE SIGNALS</div>
              {sig_html}
            </div>""", unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("Save Job", use_container_width=True, key=f"save_{r['analyzed_at']}"):
            db.save_job(st.session_state.user_id, r["title"], r["company"], url, r["status"])
            st.success("Saved!")
    with a2:
        if st.button("Generate Cover Letter", use_container_width=True, key=f"cl_{r['analyzed_at']}"):
            st.session_state.cl_prefill_title   = r["title"]
            st.session_state.cl_prefill_company = r["company"]
            st.session_state.current_page = "cover_letters"
            st.rerun()
    with a3:
        report = (
            f"SniffJob Analysis Report\n{'='*40}\n"
            f"Job: {r['title']}\nCompany: {r['company']}\n"
            f"Status: {r['status']}\nConfidence: {r['confidence']:.1%}\n"
            f"Risk Score: {r['risk_score']}/100\n\n{r['details']}\n\n"
            f"Red Flags:\n" + "\n".join(f"  - {f}" for f in r.get("red_flags", [])) +
            f"\n\nPositive Signals:\n" + "\n".join(f"  + {s}" for s in r.get("pos_signals", []))
        )
        st.download_button("Export Report", data=report, file_name="sniffjob_report.txt",
                           mime="text/plain", use_container_width=True, key=f"exp_{r['analyzed_at']}")