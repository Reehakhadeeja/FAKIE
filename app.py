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
        # Import and render authentication page
        from pages.auth import render_auth_page
        render_auth_page()
        return
    
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
