STATUS_ICON   = {"Legit": "check-circle-fill", "Suspicious": "exclamation-triangle-fill", "Fraud": "shield-exclamation"}
STATUS_EMOJI  = {"Legit": "check-circle-fill", "Suspicious": "exclamation-triangle-fill", "Fraud": "shield-exclamation"}
STATUS_COLOR  = {"Legit": "green", "Suspicious": "yellow", "Fraud": "red"}
STATUS_CLASS  = {"Legit": "card-legit", "Suspicious": "card-suspicious", "Fraud": "card-fraud"}

FAKE_TITLES   = [
    "Senior Software Engineer", "Data Analyst", "UX Designer",
    "Work From Home Data Entry", "Urgent: Payment Processor Needed",
    "Remote Customer Support", "Digital Marketing Specialist",
    "Full Stack Developer", "Business Development Manager",
    "Easy Online Work – Earn ₹50,000/day",
]
FAKE_COMPANIES = [
    "TechCorp India", "Quick Money Inc", "Global Finance LLC",
    "InfoSys Partners", "FakeCo Ltd", "Amazon Hiring India",
    "StartupXYZ", "Fortune 500 Hiring", "Dream Job Agency",
]
FAKE_DETAILS = {
    "Legit": [
        "This posting appears legitimate. The company has a verified presence, the JD is detailed and professional, salary range is realistic, and contact information is verifiable.",
        "Analysis complete. Strong signals of authenticity: registered company domain, ATS-style application, reasonable experience requirements, and standard interview process mentioned.",
    ],
    "Suspicious": [
        "Several red flags detected: vague job description, unusually high pay for minimal work, requests personal information upfront, no mention of interview process.",
        "Moderate risk: company domain is newly registered (<6 months), email contact is a free provider (gmail/yahoo), salary claim is far above market average.",
    ],
    "Fraud": [
        "HIGH RISK — Multiple fraud indicators: requests bank account info, promises extremely easy money, poor grammar, no verifiable company address, domain flagged in fraud database.",
        "SCAM DETECTED — Classic advance-fee / money mule pattern. Never share personal or financial information with this listing.",
    ],
}

RED_FLAGS = [
    "Requests bank details upfront",
    "Salary too good to be true",
    "Free Gmail / Yahoo contact",
    "No interview process mentioned",
    "Poor grammar and spelling",
    "Newly registered domain",
    "Asks for money from applicant",
    "Vague job description",
    "No company address listed",
    "Pressure to decide immediately",
]

POSITIVE_SIGNALS = [
    "Verified company domain",
    "Detailed job description",
    "Realistic salary range",
    "Structured interview process",
    "LinkedIn company page exists",
    "GSTIN / CIN mentioned",
    "Clear contact information",
    "Professional email domain",
]

JOB_MOCK = [
    {"title":"Senior Python Developer","company":"Flipkart","location":"Bengaluru","type":"Full-time","salary":"₹25-40 LPA","exp":"4-7 years","tags":["Python","Django","AWS","PostgreSQL"],"url":"#","status":"Legit"},
    {"title":"Data Scientist","company":"Swiggy","location":"Remote","type":"Full-time","salary":"₹18-30 LPA","exp":"3-5 years","tags":["ML","Python","TensorFlow","SQL"],"url":"#","status":"Legit"},
    {"title":"UI/UX Designer","company":"Razorpay","location":"Bengaluru","type":"Full-time","salary":"₹12-20 LPA","exp":"2-4 years","tags":["Figma","Design Systems","Prototyping"],"url":"#","status":"Legit"},
    {"title":"EASY WORK FROM HOME","company":"Quick Earn Ltd","location":"Anywhere","type":"Part-time","salary":"₹50,000/day","exp":"0 years","tags":["NO SKILL NEEDED","URGENT"],"url":"#","status":"Fraud"},
    {"title":"DevOps Engineer","company":"Zepto","location":"Mumbai","type":"Full-time","salary":"₹20-35 LPA","exp":"3-6 years","tags":["Kubernetes","Docker","CI/CD","Terraform"],"url":"#","status":"Legit"},
    {"title":"Freelance Content Writer","company":"ContentHub","location":"Remote","type":"Freelance","salary":"₹500-1000/article","exp":"1-2 years","tags":["Writing","SEO","Research"],"url":"#","status":"Suspicious"},
    {"title":"Product Manager","company":"CRED","location":"Bengaluru","type":"Full-time","salary":"₹30-50 LPA","exp":"5-8 years","tags":["Product","Roadmap","Analytics","Agile"],"url":"#","status":"Legit"},
    {"title":"URGENT: Crypto Trader Needed","company":"CryptoFast LLC","location":"Remote","type":"Contract","salary":"₹2L/day","exp":"0 years","tags":["INSTANT PAYMENT","NO EXPERIENCE"],"url":"#","status":"Fraud"},
]

