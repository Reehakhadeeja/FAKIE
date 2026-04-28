import streamlit as st
from database import Database

# Initialize database
db = Database()

def load_auth_css():
    """Load authentication page specific CSS"""
    st.markdown("""
    <style>
    /* Authentication page styles */
    .auth-container {
        display: flex;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -20px;
        padding: 20px;
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
        border-radius: 12px;
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
    
    /* Hide streamlit elements for auth page */
    .stApp > header {display: none;}
    .stApp > footer {display: none;}
    .stApp > .main .block-container {padding-top: 0;}
    </style>
    """, unsafe_allow_html=True)

def render_sign_in():
    """Render sign in page"""
    st.markdown("## ?? Sign In")
    st.markdown("Welcome back to SniffJob! Your trusted companion for detecting fraudulent job postings.")
    
    # Testimonials
    st.markdown("---")
    st.markdown("### What Our Users Say")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **"SniffJob saved me from a sophisticated job scam. The AI analysis was spot-on!"**
        
        *- Sarah K., Software Developer*
        """)
    
    with col2:
        st.info("""
        **"I feel more confident applying for jobs knowing SniffJob has my back."**
        
        *- Michael R., Marketing Professional*
        """)
    
    st.markdown("---")
    st.markdown("### Social Login")
    
    # Social login buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("?? Sign in with Email", use_container_width=True):
            st.info("Please use the form below to sign in with email")
    with col2:
        if st.button("?? Continue with Google", use_container_width=True):
            st.info("Google login coming soon!")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("?? Continue with Apple", use_container_width=True):
            st.info("Apple login coming soon!")
    with col4:
        if st.button("?? Continue with LinkedIn", use_container_width=True):
            st.info("LinkedIn login coming soon!")
    
    st.markdown("---")
    st.markdown("### Sign In with Email")
    
    # Email/Username and password inputs
    username = st.text_input("Email or Username", key="signin_username")
    password = st.text_input("Password", type="password", key="signin_password")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.checkbox("Remember me", key="remember_me")
    with col2:
        st.markdown('[Forgot password?](#)', unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    st.markdown("### Demo Account")
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

def render_sign_up():
    """Render sign up page"""
    st.markdown("## ?? Create Account")
    st.markdown("Start your journey to safer job hunting with AI-powered analysis.")
    
    # Testimonials
    st.markdown("---")
    st.markdown("### Why Join SniffJob?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **"The free plan helped me avoid 3 fake job offers in just one week!"**
        
        *- Alex T., Recent Graduate*
        """)
    
    with col2:
        st.info("""
        **"SniffJob's AI gives me peace of mind when job hunting."**
        
        *- Jennifer L., Career Changer*
        """)
    
    st.markdown("---")
    st.markdown("### Social Signup")
    
    # Social signup buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("?? Sign up with Email", use_container_width=True):
            st.info("Please use the form below to create an account")
    with col2:
        if st.button("?? Continue with Google", use_container_width=True):
            st.info("Google signup coming soon!")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("?? Continue with Apple", use_container_width=True):
            st.info("Apple signup coming soon!")
    with col4:
        if st.button("?? Continue with LinkedIn", use_container_width=True):
            st.info("LinkedIn signup coming soon!")
    
    st.markdown("---")
    st.markdown("### Create Account with Email")
    
    # Registration form
    new_username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email", key="signup_email")
    new_password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    st.checkbox("I agree to the Terms & Conditions and Privacy Policy", key="terms")
    
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
    
    st.markdown("---")
    st.markdown("Already have an account? [Sign in](#)")

def render_auth_page():
    """Main authentication page renderer"""
    # Tab selection for Sign In/Sign Up
    auth_tab = st.radio("Choose an option", ["Sign In", "Create account"], horizontal=True, label_visibility="collapsed")
    
    if auth_tab == "Sign In":
        render_sign_in()
    else:
        render_sign_up()

if __name__ == "__main__":
    render_auth_page()
