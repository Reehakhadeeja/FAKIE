"""
Rule-based analysis engine for job posting legitimacy detection
"""

import logging
from datetime import datetime
from typing import Dict, List, Tuple

class RuleBasedAnalyzer:
    """Rule-based analyzer for job posting legitimacy"""
    
    def __init__(self):
        self.fraud_keywords = [
            "bank account", "advance fee", "wire transfer", "western union",
            "money mule", "earn from home", "no experience needed", "guaranteed income",
            "pay registration", "whatsapp only", "urgent hiring", "₹50,000/day",
            "instant payment", "no interview", "work from mobile",
        ]
        
        self.suspicious_keywords = [
            "gmail.com", "yahoo.com", "work from home", "no degree required",
            "earn extra income", "part time unlimited", "immediate joining",
            "salary negotiable", "contact on whatsapp",
        ]
        
        self.legit_keywords = [
            "interview process", "ats", "background check", "equity",
            "health insurance", "401k", "pf", "esic", "annual leave",
            "probation period", "glassdoor", "linkedin", "careers page",
        ]
        
        self.trusted_domains = [
            "linkedin.com", "indeed.com", "naukri.com", "glassdoor.com",
            "amazon.jobs", "google.com", "microsoft.com", "infosys.com",
            "flipkart.com", "swiggy.in", "zomato.com", "tcs.com",
            "internshala.com", "foundit.in", "shine.com", "monster.com",
            "angel.co", "wellfound.com", "builtin.com", "jobs.eu"
        ]
    
    def analyze(self, text: str, url: str = "") -> Dict:
        """
        Analyze job posting text using rule-based approach
        
        Args:
            text: Job description text
            url: Job posting URL (optional)
            
        Returns:
            Dictionary containing analysis results
        """
        logging.info(f"Starting rule-based analysis for {len(text)} characters")
        
        text_lower = text.lower()
        
        # Find keyword matches
        fraud_hits = [kw for kw in self.fraud_keywords if kw in text_lower]
        suspicious_hits = [kw for kw in self.suspicious_keywords if kw in text_lower]
        legit_hits = [kw for kw in self.legit_keywords if kw in text_lower]
        
        # Calculate fraud score
        fraud_score = len(fraud_hits) * 15 + len(suspicious_hits) * 5 - len(legit_hits) * 8
        
        # Check URL trust signals
        url_trusted = any(domain in url.lower() for domain in self.trusted_domains)
        if url_trusted:
            fraud_score -= 20
        
        # Classify based on score
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
        
        # Detail messages
        detail_map = {
            "Legit": "Analysis complete. The job posting shows strong authenticity signals. The description is detailed, the platform is reputable, and no deceptive patterns were detected.",
            "Suspicious": "Moderate risk detected. Some patterns in this posting match common job scam characteristics. Verify the company independently before sharing personal information.",
            "Fraud": "HIGH RISK — Multiple fraud indicators found in this posting. Do NOT share personal or financial information. Report this listing to the job platform.",
        }
        
        result = {
            "status": status,
            "confidence": confidence,
            "risk_score": risk_score,
            "details": detail_map[status],
            "red_flags": red_flags[:5],
            "pos_signals": pos_signals[:6],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "fraud_hits": fraud_hits,
            "suspicious_hits": suspicious_hits,
            "legit_hits": legit_hits,
            "url_trusted": url_trusted,
            "fraud_score": fraud_score
        }
        
        logging.info(f"Rule-based analysis completed: {status} with {confidence:.1%} confidence")
        return result

# Global analyzer instance
rule_analyzer = RuleBasedAnalyzer()

# Backward compatibility function
def _rule_based_analysis(text: str, url: str) -> Dict:
    """Backward compatibility wrapper for rule-based analysis"""
    return rule_analyzer.analyze(text, url)
