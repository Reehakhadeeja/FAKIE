import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_settings():
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('gear','1.2rem')} Settings</h2>", unsafe_allow_html=True)
    user = st.session_state.get("user",{})

    t1,t2,t3 = st.tabs(["Account","Preferences","Privacy"])
    with t1:
        st.markdown(f'<div class="x_title"><h2>{bi("person-vcard")} Account Details</h2></div>', unsafe_allow_html=True)
        new_email = st.text_input("Email",         value=user.get("email",""),    key="set_email")
        avatar_choices = ["🐶","🐕","🦮","🐩","🐈","🦊","🐺","🤖"]
        current_avatar = user.get("avatar")
        if not current_avatar or current_avatar not in avatar_choices:
            current_avatar = "🐶"
        
        try:
            idx = avatar_choices.index(current_avatar)
        except ValueError:
            idx = 0

        new_avatar= st.selectbox("Avatar Emoji", avatar_choices, index=idx, key="set_avatar")
        if st.button("Save Account", key="set_save_acc"):
            st.session_state.user["email"]  = new_email
            st.session_state.user["avatar"] = new_avatar
            db.update_user(user.get("username",""), email=new_email, avatar=new_avatar)
            st.success("Saved!")

        st.markdown("---")
        st.markdown(f'<div class="x_title"><h2>{bi("shield-lock")} Change Password</h2></div>', unsafe_allow_html=True)
        old_p = st.text_input("Current password", type="password", key="set_oldp")
        new_p = st.text_input("New password",     type="password", key="set_newp")
        if st.button("Change Password", key="set_chpwd"):
            if old_p == user.get("password",""):
                db.update_user(user.get("username",""), password=new_p)
                st.session_state.user["password"] = new_p
                st.success("Password changed!")
            else:
                st.error("Current password incorrect.")

    with t2:
        st.markdown(f'<div class="x_title"><h2>{bi("bell")} Notification Preferences</h2></div>', unsafe_allow_html=True)
        st.checkbox("Email alerts for fraud detections",        value=True,  key="pref_email")
        st.checkbox("Weekly job market digest",                 value=True,  key="pref_digest")
        st.checkbox("Application reminder notifications",       value=False, key="pref_app_rem")
        st.checkbox("Tips and tricks from SniffJob AI",         value=True,  key="pref_tips")
        st.markdown(f'<div class="x_title"><h2>{bi("display")} Display Settings</h2></div>', unsafe_allow_html=True)
        st.selectbox("Default job search location", ["Bengaluru","Mumbai","Delhi","Hyderabad","Chennai","Remote"], key="pref_loc")
        st.selectbox("Default results per page", [5,10,20,50], key="pref_rpp")
        if st.button("Save Preferences", key="set_save_prefs"):
            st.success("Preferences saved!")

    with t3:
        st.markdown(f'<div class="x_title"><h2>{bi("shield-shaded")} Privacy & Data Management</h2></div>', unsafe_allow_html=True)
        st.info("SniffJob stores your data locally in this session. No data is sent to external servers.")
        if st.button("Clear All My Data", key="clear_data_btn"):
            uid = st.session_state.get("user_id")
            if uid:
                st.session_state.db_store["job_analyses"] = [j for j in st.session_state.db_store["job_analyses"] if j["user_id"]!=uid]
                st.session_state.db_store["resumes"]       = [r for r in st.session_state.db_store["resumes"]       if r["user_id"]!=uid]
                st.session_state.db_store["notes"]         = [n for n in st.session_state.db_store["notes"]         if n["user_id"]!=uid]
                st.success("All data cleared.")
        if st.button("Delete Account", key="del_acc_btn"):
            username = st.session_state.user.get("username","")
            if username in st.session_state.db_store["users"]:
                del st.session_state.db_store["users"][username]
            st.session_state.clear()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PROFILE
# ══════════════════════════════════════════════════════════════════════════════
