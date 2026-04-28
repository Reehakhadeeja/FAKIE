import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_auth():
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:10vh;margin-bottom:2rem;">
      <div style="text-align:center;">
        <div style="background:var(--bg2); width:100px; height:100px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin: 0 auto 1.5rem; box-shadow: var(--shadow); border: 2px solid var(--border);">
            <div style="font-size:3rem; line-height:1;">{bi('briefcase-fill','3rem','var(--blue)')}</div>
        </div>
        <h1 style="color:var(--text); font-size:2.8rem; font-weight:700; margin:0; letter-spacing:-1px;">SniffJob <span style="color:var(--teal)">AI</span></h1>
        <p style="color:var(--text2); font-size:1rem; margin-top:0.5rem; font-weight:400;">Advanced Job Intelligence & Fraud Detection</p>
      </div>
    </div>""", unsafe_allow_html=True)

    col = st.columns([1,1.4,1])[1]
    with col:
        tab_l, tab_r = st.tabs(["Login", "Register"])
        with tab_l:
            uname = st.text_input("Username", key="auth_uname", placeholder="demo")
            pwd   = st.text_input("Password", type="password", key="auth_pwd", placeholder="demo123")
            if st.button("Login", use_container_width=True, key="btn_login"):
                user = db.authenticate(uname.strip(), pwd)
                if user:
                    st.session_state.user_id       = user["id"]
                    st.session_state.user          = user
                    st.session_state.current_page  = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try demo / demo123")
        with tab_r:
            new_u  = st.text_input("Username", key="reg_uname", placeholder="Choose username")
            new_e  = st.text_input("Email",    key="reg_email", placeholder="you@example.com")
            new_p  = st.text_input("Password", type="password", key="reg_pwd", placeholder="Min 6 chars")
            new_p2 = st.text_input("Confirm",  type="password", key="reg_pwd2", placeholder="Repeat password")
            if st.button("Create Account", use_container_width=True, key="btn_reg"):
                if not new_u or not new_e or not new_p:
                    st.error("All fields required")
                elif new_p != new_p2:
                    st.error("Passwords do not match")
                elif len(new_p) < 6:
                    st.error("Password too short")
                else:
                    ok, msg = db.register(new_u.strip(), new_p, new_e.strip())
                    if ok:
                        st.success("Account created! Please login.")
                    else:
                        st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
