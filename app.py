import streamlit as st
import requests
import random
from datetime import datetime
import time
from database import Database

# Initialize database
db = Database()

# Dark theme CSS
def load_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-bg: #0f172a;
        --secondary-bg: #1e293b;
        --accent-blue: #3b82f6;
        --accent-hover: #2563eb;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border-color: #334155;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    /* Global styles */
    .stApp {
        background-color: var(--primary-bg);
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background-color: var(--primary-bg) !important;
        border-right: 1px solid var(--border-color);
    }
    
    .css-1d391kg .css-17eq0hr {
        background-color: var(--primary-bg);
    }
    
    /* Sidebar navigation items */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        margin: 4px 8px;
        border-radius: 8px;
        color: var(--text-secondary);
        text-decoration: none;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background-color: var(--secondary-bg);
        color: var(--text-primary);
    }
    
    .nav-item.active {
        background-color: var(--accent-blue);
        color: white;
    }
    
    .nav-item i {
        margin-right: 12px;
        font-size: 18px;
    }
    
    /* Subscription card */
    .subscription-card {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-hover));
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin: 16px 8px;
        text-align: center;
    }
    
    /* Info box */
    .info-box {
        background-color: var(--secondary-bg);
        border-left: 4px solid var(--accent-blue);
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        color: var(--text-primary);
    }
    
    /* Result cards */
    .result-card {
        background-color: var(--secondary-bg);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border: 1px solid var(--border-color);
    }
    
    .result-legit {
        border-left: 4px solid var(--success);
    }
    
    .result-fraud {
        border-left: 4px solid var(--danger);
    }
    
    .result-suspicious {
        border-left: 4px solid var(--warning);
    }
    
    /* Header styles */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background-color: var(--secondary-bg);
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    .header-item {
        display: flex;
        align-items: center;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .header-item i {
        margin-right: 8px;
        font-size: 20px;
    }
    
    /* Button styles */
    .stButton > button {
        background-color: var(--accent-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--accent-hover);
    }
    
    .logout-btn {
        background-color: var(--danger) !important;
        color: white !important;
        width: 100%;
        margin-top: 20px;
    }
    
    /* Input styles */
    .stTextInput > div > div > input {
        background-color: var(--secondary-bg);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 8px;
    }
    
    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--secondary-bg);
        border-radius: 8px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        border-radius: 6px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-blue);
        color: white;
    }
    
    /* Chatbot button */
    .chatbot-btn {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background-color: var(--accent-blue);
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        transition: all 0.2s ease;
    }
    
    .chatbot-btn:hover {
        background-color: var(--accent-hover);
        transform: scale(1.1);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--primary-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        # App logo and name
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #3b82f6; margin: 0; font-size: 28px;">🐕 Sniff Job</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Subscription card
        user_data = st.session_state.get('user', {})
        plan = user_data.get('plan', 'Free')
        st.markdown(f"""
        <div class="subscription-card">
            <div style="font-size: 24px; margin-bottom: 8px;">💎</div>
            <div style="font-weight: 600;">{plan} Plan</div>
            <div style="font-size: 14px; opacity: 0.9;">Active subscription</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        nav_items = [
            ("📊", "Dashboard", "dashboard"),
            ("📄", "Upload CV", "upload_cv"),
            ("📁", "My Resume", "my_resume"),
            ("✨", "AI Assistant", "ai_assistant"),
            ("📋", "EasyApply Kit", "easyapply_kit"),
            ("👁️", "Sniff History", "sniff_history"),
            ("🔍", "Job Search", "job_search"),
            ("📂", "Files", "files"),
            ("💳", "Plans", "plans"),
            ("👤", "Profile", "profile")
        ]
        
        current_page = st.session_state.get('current_page', 'dashboard')
        
        for icon, label, page_key in nav_items:
            is_active = current_page == page_key
            nav_class = "nav-item active" if is_active else "nav-item"
            
            st.markdown(f"""
            <div class="{nav_class}" onclick="setPage('{page_key}')">
                <span>{icon}</span>
                <span>{label}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(label, key=f"nav_{page_key}", help=f"Navigate to {label}"):
                st.session_state.current_page = page_key
                st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", key="logout", help="Logout from your account"):
            st.session_state.clear()
            st.rerun()

def render_header():
    """Render top header with user info"""
    user_data = st.session_state.get('user', {})
    username = user_data.get('username', 'Guest')
    tokens = user_data.get('tokens', 20)
    
    # Get notification count
    notification_count = 0
    if 'user_id' in st.session_state:
        notification_count = db.get_unread_notifications_count(st.session_state.user_id)
    
    st.markdown(f"""
    <div class="header-container">
        <div class="header-item">
            <span>🪙</span>
            <span>{tokens}</span>
        </div>
        <div class="header-item">
            <span>🔔</span>
            <span>{notification_count}</span>
        </div>
        <div class="header-item">
            <span>👤</span>
            <span>{username}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def analyze_job_url(url: str) -> dict:
    """Simulate job URL analysis"""
    # Simulate API call delay
    time.sleep(2)
    
    # Random results for demonstration
    results = [
        {
            "status": "Legit",
            "confidence": random.uniform(0.85, 0.95),
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "details": "This job posting appears to be legitimate. The company has a verified presence and the job description is detailed and professional."
        },
        {
            "status": "Suspicious",
            "confidence": random.uniform(0.60, 0.80),
            "title": "Work From Home Data Entry",
            "company": "Quick Money Inc",
            "details": "This job posting shows some warning signs: vague job description, unusually high pay for minimal work, and requests for personal information upfront."
        },
        {
            "status": "Fraud",
            "confidence": random.uniform(0.90, 0.98),
            "title": "Urgent: Payment Processor Needed",
            "company": "Global Finance LLC",
            "details": "This is likely a fraudulent posting. Multiple red flags detected: requests for bank account information, promises of easy money, and poor grammar."
        }
    ]
    
    return random.choice(results)

def render_dashboard():
    """Render main dashboard page"""
    st.markdown("# 🔍 Job Post Analyzer")
    
    # Tabs
    tab1, tab2 = st.tabs(["Job URL", "Manual Entry"])
    
    with tab1:
        # Info box
        st.markdown("""
        <div class="info-box">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 20px; margin-right: 12px;">ℹ️</span>
                <span>Paste a job listing URL from any job board or company website.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # URL input
        col1, col2 = st.columns([4, 1])
        
        with col1:
            job_url = st.text_input(
                "Enter job URL to analyze (e.g., LinkedIn, Indeed, etc.)",
                placeholder="https://www.linkedin.com/jobs/view/...",
                key="job_url_input"
            )
        
        with col2:
            analyze_button = st.button("🔍 Sniff It", type="primary", use_container_width=True)
        
        # Analysis section
        if analyze_button and job_url:
            with st.spinner("Analyzing job posting..."):
                result = analyze_job_url(job_url)
                
                # Store in database if user is logged in
                if 'user_id' in st.session_state:
                    db.add_job_analysis(
                        st.session_state.user_id,
                        job_url,
                        result['title'],
                        result['company'],
                        result['status'],
                        result['confidence'],
                        result['details']
                    )
                
                # Display result
                result_class = f"result-card result-{result['status'].lower()}"
                status_emoji = {"Legit": "✅", "Suspicious": "⚠️", "Fraud": "🚨"}
                
                st.markdown(f"""
                <div class="{result_class}">
                    <h3 style="margin: 0 0 16px 0; color: #f1f5f9;">
                        {status_emoji.get(result['status'], '📋')} {result['status']}
                    </h3>
                    <div style="margin-bottom: 12px;">
                        <strong>Job Title:</strong> {result['title']}<br>
                        <strong>Company:</strong> {result['company']}<br>
                        <strong>Confidence:</strong> {result['confidence']:.1%}
                    </div>
                    <div style="color: #94a3b8; line-height: 1.6;">
                        {result['details']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        elif not job_url and analyze_button:
            st.error("Please enter a job URL to analyze.")
        
        # Empty state
        if not job_url:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 120px; margin-bottom: 24px;">🐕‍🦺</div>
                <h3 style="color: #f1f5f9; margin-bottom: 12px;">Enter a job URL to start analyzing</h3>
                <p style="color: #94a3b8;">
                    SniffJob AI will analyze the job post and determine if it's legitimate or potentially fraudulent.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Manual Job Entry")
        st.info("Manual entry feature coming soon!")

def render_sniff_history():
    """Render sniff history page"""
    st.markdown("# 👁️ Sniff History")
    
    if 'user_id' not in st.session_state:
        st.warning("Please login to view your sniff history.")
        return
    
    history = db.get_job_history(st.session_state.user_id)
    
    if not history:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 80px; margin-bottom: 24px;">📋</div>
            <h3 style="color: #f1f5f9; margin-bottom: 12px;">No job analysis history yet</h3>
            <p style="color: #94a3b8;">
                Start analyzing job postings to see your history here.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for job in history:
            status_emoji = {"Legit": "✅", "Suspicious": "⚠️", "Fraud": "🚨"}
            result_class = f"result-card result-{job['result'].lower()}"
            
            st.markdown(f"""
            <div class="{result_class}">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                    <div>
                        <h4 style="margin: 0; color: #f1f5f9;">
                            {status_emoji.get(job['result'], '📋')} {job['result']}
                        </h4>
                        <div style="color: #94a3b8; font-size: 14px;">
                            {job['job_title']} at {job['company']}
                        </div>
                    </div>
                    <div style="color: #64748b; font-size: 12px;">
                        {job['timestamp']}
                    </div>
                </div>
                <div style="color: #94a3b8; font-size: 14px; margin-bottom: 8px;">
                    <strong>URL:</strong> <a href="{job['job_url']}" target="_blank" style="color: #3b82f6;">{job['job_url'][:50]}...</a>
                </div>
                <div style="color: #94a3b8; font-size: 14px;">
                    <strong>Confidence:</strong> {job['confidence_score']:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_upload_cv():
    """Render CV upload page"""
    st.markdown("# 📄 Upload CV")
    
    if 'user_id' not in st.session_state:
        st.warning("Please login to upload your CV.")
        return
    
    uploaded_file = st.file_uploader(
        "Choose your CV file",
        type=['pdf', 'doc', 'docx'],
        help="Upload your resume in PDF or Word format"
    )
    
    if uploaded_file is not None:
        # Save file
        file_path = f"uploads/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store in database
        db.upload_resume(st.session_state.user_id, uploaded_file.name, file_path)
        
        st.success(f"Successfully uploaded: {uploaded_file.name}")
    
    # Show existing resumes
    resumes = db.get_user_resumes(st.session_state.user_id)
    
    if resumes:
        st.markdown("### Your Uploaded Resumes")
        for resume in resumes:
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{resume['file_name']}</strong>
                        <div style="color: #94a3b8; font-size: 14px;">
                            Uploaded: {resume['upload_date']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    # Load CSS
    load_css()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Check if user is logged in
    if 'user_id' not in st.session_state:
        # Authentication page with split layout
        st.markdown("""
        <style>
        .auth-container {
            display: flex;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .auth-left {
            flex: 1;
            padding: 60px 40px;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .auth-right {
            flex: 1;
            background: white;
            padding: 60px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .auth-logo {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .auth-title {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 20px;
            line-height: 1.2;
        }
        .auth-subtitle {
            font-size: 18px;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        .testimonial {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .testimonial-text {
            font-style: italic;
            margin-bottom: 10px;
        }
        .testimonial-author {
            font-size: 14px;
            opacity: 0.8;
        }
        .auth-form-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1a202c;
        }
        .auth-form-subtitle {
            color: #718096;
            margin-bottom: 30px;
        }
        .social-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 30px;
        }
        .social-btn {
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            font-size: 14px;
        }
        .social-btn:hover {
            background: #f7fafc;
            border-color: #cbd5e0;
        }
        .divider {
            text-align: center;
            margin: 20px 0;
            color: #718096;
            position: relative;
        }
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e2e8f0;
        }
        .divider span {
            background: white;
            padding: 0 15px;
            position: relative;
        }
        .auth-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 16px;
        }
        .auth-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .auth-checkbox {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .auth-link {
            color: #667eea;
            text-decoration: none;
        }
        .auth-link:hover {
            text-decoration: underline;
        }
        .signup-prompt {
            text-align: center;
            margin-top: 20px;
            color: #718096;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Tab selection for Sign In/Sign Up
        auth_tab = st.radio("", ["Sign In", "Create account"], horizontal=True)
        
        if auth_tab == "Sign In":
            st.markdown("""
            <div class="auth-container">
                <div class="auth-left">
                    <div class="auth-logo">🐕 SniffJob</div>
                    <div class="auth-title">Welcome back to SniffJob</div>
                    <div class="auth-subtitle">Your trusted companion for detecting fraudulent job postings</div>
                    
                    <div class="testimonial">
                        <div class="testimonial-text">"SniffJob saved me from a sophisticated job scam. The AI analysis was spot-on!"</div>
                        <div class="testimonial-author">- Sarah K., Software Developer</div>
                    </div>
                    
                    <div class="testimonial">
                        <div class="testimonial-text">"I feel more confident applying for jobs knowing SniffJob has my back."</div>
                        <div class="testimonial-author">- Michael R., Marketing Professional</div>
                    </div>
                </div>
                
                <div class="auth-right">
                    <div class="auth-form-title">Sign in</div>
                    <div class="auth-form-subtitle">Welcome back! Please enter your details.</div>
                    
                    <div class="social-buttons">
                        <button class="social-btn" onclick="handleSocialLogin('email')">📧 Sign in with Email</button>
                        <button class="social-btn" onclick="handleSocialLogin('google')">🔍 Continue with Google</button>
                        <button class="social-btn" onclick="handleSocialLogin('apple')">🍎 Continue with Apple</button>
                        <button class="social-btn" onclick="handleSocialLogin('linkedin')">💼 Continue with LinkedIn</button>
                    </div>
                    
                    <div class="divider"><span>or</span></div>
                </div>
            </div>
            
            <script>
            function handleSocialLogin(provider) {
                if (provider === 'email') {
                    // Focus on email input
                    const emailInput = document.querySelector('input[key="signin_username"]');
                    if (emailInput) emailInput.focus();
                } else {
                    // Show placeholder message for other providers
                    alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} login coming soon! For now, please use email login or the demo account.`);
                }
            }
            </script>
            """, unsafe_allow_html=True)
            
            # Email/Username and password inputs
            username = st.text_input("Email or Username", key="signin_username")
            password = st.text_input("Password", type="password", key="signin_password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.checkbox("Remember me", key="remember_me")
            with col2:
                st.markdown('<a href="#" class="auth-link">Forgot password?</a>', unsafe_allow_html=True)
            
            if st.button("Sign in", type="primary", use_container_width=True):
                if username and password:
                    user = db.authenticate_user(username, password)
                    if user:
                        st.session_state.user_id = user['id']
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
            
            st.markdown("""
            <div class="signup-prompt">
                Don't have an account? <a href="#" class="auth-link">Sign up</a>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Demo Account:**")
            st.markdown("Username: `demo`")
            st.markdown("Password: `demo123`")
            
            if st.button("Use Demo Account", use_container_width=True):
                # Create demo user if not exists
                db.create_user("demo", "demo123")
                user = db.authenticate_user("demo", "demo123")
                if user:
                    st.session_state.user_id = user['id']
                    st.session_state.user = user
                    st.rerun()
        
        else:  # Create account
            st.markdown("""
            <div class="auth-container">
                <div class="auth-left">
                    <div class="auth-logo">🐕 SniffJob</div>
                    <div class="auth-title">Join SniffJob Today</div>
                    <div class="auth-subtitle">Start protecting yourself from job scams with AI-powered analysis</div>
                    
                    <div class="testimonial">
                        <div class="testimonial-text">"The free plan helped me avoid 3 fake job offers in just one week!"</div>
                        <div class="testimonial-author">- Alex T., Recent Graduate</div>
                    </div>
                    
                    <div class="testimonial">
                        <div class="testimonial-text">"SniffJob's AI gives me peace of mind when job hunting."</div>
                        <div class="testimonial-author">- Jennifer L., Career Changer</div>
                    </div>
                </div>
                
                <div class="auth-right">
                    <div class="auth-form-title">Create account</div>
                    <div class="auth-form-subtitle">Start your journey to safer job hunting.</div>
                    
                    <div class="social-buttons">
                        <button class="social-btn" onclick="handleSocialSignup('email')">📧 Sign up with Email</button>
                        <button class="social-btn" onclick="handleSocialSignup('google')">🔍 Continue with Google</button>
                        <button class="social-btn" onclick="handleSocialSignup('apple')">🍎 Continue with Apple</button>
                        <button class="social-btn" onclick="handleSocialSignup('linkedin')">💼 Continue with LinkedIn</button>
                    </div>
                    
                    <div class="divider"><span>or</span></div>
                </div>
            </div>
            
            <script>
            function handleSocialSignup(provider) {
                if (provider === 'email') {
                    // Focus on username input
                    const usernameInput = document.querySelector('input[key="signup_username"]');
                    if (usernameInput) usernameInput.focus();
                } else {
                    // Show placeholder message for other providers
                    alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} signup coming soon! For now, please use email signup.`);
                }
            }
            </script>
            """, unsafe_allow_html=True)
            
            # Registration form
            new_username = st.text_input("Username", key="signup_username")
            email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            st.markdown("""
            <div class="auth-checkbox">
                <input type="checkbox" id="terms">
                <label for="terms">I agree to the Terms & Conditions and Privacy Policy</label>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Create account", type="primary", use_container_width=True):
                if new_username and email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        # Create new user
                        success = db.create_user(new_username, new_password, email)
                        if success:
                            st.success("Account created successfully! Please sign in.")
                            # Auto-switch to sign in tab
                            st.session_state.auth_tab = "Sign In"
                            st.rerun()
                        else:
                            st.error("Username already exists. Please choose another.")
                else:
                    st.error("Please fill in all fields")
            
            st.markdown("""
            <div class="signup-prompt">
                Already have an account? <a href="#" class="auth-link">Sign in</a>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # User is logged in - show main app
        render_sidebar()
        render_header()
        
        # Render current page
        current_page = st.session_state.current_page
        
        if current_page == 'dashboard':
            render_dashboard()
        elif current_page == 'sniff_history':
            render_sniff_history()
        elif current_page == 'upload_cv':
            render_upload_cv()
        elif current_page == 'my_resume':
            st.markdown("# 📁 My Resume")
            st.info("Resume management feature coming soon!")
        elif current_page == 'ai_assistant':
            st.markdown("# ✨ AI Assistant")
            st.info("AI Assistant feature coming soon!")
        elif current_page == 'easyapply_kit':
            st.markdown("# 📋 EasyApply Kit")
            st.info("EasyApply Kit feature coming soon!")
        elif current_page == 'job_search':
            st.markdown("# 🔍 Job Search")
            st.info("Job Search feature coming soon!")
        elif current_page == 'files':
            st.markdown("# 📂 Files")
            st.info("File management feature coming soon!")
        elif current_page == 'plans':
            st.markdown("# 💳 Plans")
            st.info("Subscription plans coming soon!")
        elif current_page == 'profile':
            st.markdown("# 👤 Profile")
            user_data = st.session_state.get('user', {})
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color: #f1f5f9;">User Profile</h3>
                <div style="color: #94a3b8;">
                    <strong>Username:</strong> {user_data.get('username', 'N/A')}<br>
                    <strong>Plan:</strong> {user_data.get('plan', 'Free')}<br>
                    <strong>Tokens:</strong> {user_data.get('tokens', 0)}<br>
                    <strong>Member Since:</strong> {user_data.get('created_at', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Chatbot button
        st.markdown("""
        <div class="chatbot-btn" onclick="alert('Chatbot coming soon!')">
            <span style="font-size: 24px;">💬</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
