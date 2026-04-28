import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_profile():
    uid  = st.session_state.user_id
    user = st.session_state.get("user",{})
    stats= db.get_stats(uid)
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('person-circle','1.2rem')} Profile</h2>", unsafe_allow_html=True)
import streamlit as st
import time
import json
from database import db
from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
from config import *

def render_profile():
    uid  = st.session_state.user_id
    user = st.session_state.get("user",{})
    stats= db.get_stats(uid)
    # st.markdown(f"<h2 style='font-family: sans-serif;color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0 0 12px'>{bi('person-circle','1.2rem')} Profile</h2>", unsafe_allow_html=True)

    c1,c2 = st.columns([1,2])
    with c1:
        st.markdown(f"""
        <div class="table-card" style="text-align:center; padding:30px 20px;">
          <div style="font-size:5rem; line-height:1; margin-bottom:15px;">{user.get('avatar','🧑‍💼')}</div>
          <div style="font-weight:700;font-size:1.4rem;color:var(--text)">{user.get('username','')}</div>
          <div style="color:var(--text2);font-size:14px; margin-top:5px;">{user.get('email','')}</div>
          <div style="color:var(--text3);font-size:12px;margin-top:10px">Member since {user.get('created_at','')}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f'<div class="x_title"><h2>{bi("activity")} Activity Summary</h2></div>', unsafe_allow_html=True)
        rows = [
            (f"{bi('search')} Jobs Analyzed", stats["total"]),
            (f"{bi('check-circle-fill','1em','#1ABB9C')} Legit Found",   stats["legit"]),
            (f"{bi('exclamation-triangle-fill','1em','#F39C12')} Suspicious",   stats["suspicious"]),
            (f"{bi('shield-fill-x','1em','#E74C3C')} Fraud Caught",  stats["fraud"]),
            (f"{bi('bookmark-fill')} Jobs Saved",    stats["saved"]),
            (f"{bi('send-fill')} Applied",       stats["applied"]),
        ]
        for lbl,val in rows:
            c,v = st.columns([3,1])
            with c: st.markdown(f"<div style='color:var(--text2);font-size:14px; padding:8px 0; border-bottom:1px solid var(--border);'>{lbl}</div>", unsafe_allow_html=True)
            with v: st.markdown(f"<div style='font-weight:700;color:var(--text);text-align:right; padding:8px 0; border-bottom:1px solid var(--border);'>{val}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="x_title"><h2>{bi("award")} Achievement Badges</h2></div>', unsafe_allow_html=True)
        fraud_caught = stats["fraud"]
        tier_map = [
            (10, bi('trophy-fill','2.5rem','#F39C12'), "Fraud Hunter"),
            (5, bi('award-fill','2.5rem','#337AB7'), "Vigilant Scout"),
            (1, bi('star-fill','2.5rem','#1ABB9C'), "Apprentice Hunter"),
            (0, bi('emoji-smile','2.5rem','#999'), "New Investigator"),
        ]
        tier_icon = ""
        tier_label = ""
        for threshold, tico, tlabel in tier_map:
            if fraud_caught >= threshold:
                tier_icon = tico
                tier_label = tlabel
                break
        st.markdown(f"""
        <div class="table-card" style="text-align:center;padding:20px; border-top: 3px solid #9B59B6;">
          <div style="font-size:2.5rem; margin-bottom:10px;">{tier_icon}</div>
          <div style="font-weight:700;color:#9B59B6; font-size:1.1rem; text-transform:uppercase; letter-spacing:1px;">{tier_label}</div>
          <div style="color:var(--text2);font-size:13px; margin-top:5px;">{fraud_caught} fraud job(s) caught</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
