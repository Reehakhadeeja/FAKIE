import streamlit as st
from database import db
from utils import bi

def render_header():
    user   = st.session_state.get("user", {})
    uname  = user.get("username", "Guest")
    notif  = db.get_unread_notifications_count(st.session_state.get("user_id",0))
    page = st.session_state.get("current_page", "Dashboard").replace('_', ' ').title()
    st.markdown(f"""
    <div class="topbar">
      <div class="topbar-title">{bi('list','1.2rem')}  {page}</div>
      <div style="display:flex;gap:20px;align-items:center">
        <div class="topbar-item" style="cursor:pointer;">{bi('envelope','1.1em')}</div>
        <div class="topbar-item" style="cursor:pointer;position:relative;">
          {bi('bell-fill','1.1em','var(--text2)')} 
          {f'<span class="badge badge-red" style="position:absolute;top:-8px;right:-12px;padding:2px 5px;font-size:9px;">{notif}</span>' if notif else ''}
        </div>
        <div class="topbar-item" style="cursor:pointer;margin-left:10px;">
          <img src="https://ui-avatars.com/api/?name={uname}&background=random" style="width:28px;border-radius:50%;margin-right:5px;"/> {uname} {bi('chevron-down','0.8em')}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH PAGE
# ══════════════════════════════════════════════════════════════════════════════
