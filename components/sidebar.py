import streamlit as st
from database import db
from utils import bi

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="logo-wrap">
          <span>{bi('briefcase-fill','1.3rem','#fff')} SniffJob</span>
        </div>
        """, unsafe_allow_html=True)

        user = st.session_state.get("user", {})
        avatar = user.get("avatar", "🧑‍💼")
        uname  = user.get("username", "Admin User")
        st.markdown(f"""
        <div class="profile_info">
          <div style="font-size:35px;line-height:1;width:45px;text-align:center">{avatar}</div>
          <div class="profile_info_text">
            <span>Welcome,</span>
            <h2>{uname}</h2>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Navigation icons mapping ──
        nav_icons = {
      
        }

        nav = [
            ("Dashboard",      "dashboard"),
            ("Job Analyzer",   "analyzer"),
            ("Job Search",     "job_search"),
            ("Sniff History",  "history"),
            ("Saved Jobs",     "saved_jobs"),
            ("Applications",   "applications"),
        ]
        nav2 = [
            ("Upload CV",      "upload_cv"),
            ("Resume Builder", "resume_builder"),
            ("Cover Letters",  "cover_letters"),
        ]
        nav3 = [
            ("AI Assistant",   "ai_assistant"),
            ("EasyApply Kit",  "easyapply"),
            ("Notes",          "notes"),
            ("Files",          "files"),
        ]
        nav4 = [
            ("Notifications",  "notifications"),
            ("Settings",       "settings"),
            ("Profile",        "profile"),
        ]

        cur = st.session_state.get("current_page","dashboard")
        for group in [nav, nav2, nav3, nav4]:
            for label, key in group:
                icon = nav_icons.get(key, "")
                is_active = (cur == key)
                # Apply active style via CSS (handled in style.py via button attributes)
                
                notif_dot = ""
                if key == "notifications":
                    n = db.get_unread_notifications_count(st.session_state.get("user_id",0))
                    if n: notif_dot = f" ({n})"
                
                if st.button(f"{icon} {label}{notif_dot}", key=f"nav_{key}", use_container_width=True):
                    st.session_state.current_page = key
                    st.rerun()

        st.markdown("---")
        if st.button("Logout", key="nav_logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────
