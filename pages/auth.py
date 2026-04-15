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
    st.markdown("""
    <div class="auth-container">
        <div class="auth-left">
            <div class="auth-logo">?? SniffJob</div>
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
                <button class="social-btn" onclick="showMessage('email')">?? Sign in with Email</button>
                <button class="social-btn" onclick="showMessage('google')">?? Continue with Google</button>
                <button class="social-btn" onclick="showMessage('apple')">?? Continue with Apple</button>
                <button class="social-btn" onclick="showMessage('linkedin')">?? Continue with LinkedIn</button>
            </div>
            
            <div class="divider"><span>or</span></div>
        </div>
    </div>
    
    <script>
    function showMessage(provider) {
        if (provider === 'email') {
            // Focus on email input
            const emailInput = document.querySelector('input[aria-label="Email or Username"]');
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

def render_sign_up():
    """Render sign up page"""
    st.markdown("""
    <div class="auth-container">
        <div class="auth-left">
            <div class="auth-logo">?? SniffJob</div>
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
                <button class="social-btn" onclick="showSignupMessage('email')">?? Sign up with Email</button>
                <button class="social-btn" onclick="showSignupMessage('google')">?? Continue with Google</button>
                <button class="social-btn" onclick="showSignupMessage('apple')">?? Continue with Apple</button>
                <button class="social-btn" onclick="showSignupMessage('linkedin')">?? Continue with LinkedIn</button>
            </div>
            
            <div class="divider"><span>or</span></div>
        </div>
    </div>
    
    <script>
    function showSignupMessage(provider) {
        if (provider === 'email') {
            // Focus on username input
            const usernameInput = document.querySelector('input[aria-label="Username"]');
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

def render_auth_page():
    """Main authentication page renderer"""
    # Load auth-specific CSS
    load_auth_css()
    
    # Tab selection for Sign In/Sign Up
    auth_tab = st.radio("Choose an option", ["Sign In", "Create account"], horizontal=True, label_visibility="collapsed")
    
    if auth_tab == "Sign In":
        render_sign_in()
    else:
        render_sign_up()

if __name__ == "__main__":
    render_auth_page()
