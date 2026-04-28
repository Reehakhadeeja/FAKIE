import streamlit as st

from components.style import load_css
from components.sidebar import render_sidebar
from components.header import render_header
from utils import bi

from views.auth import render_auth
from views.dashboard import render_dashboard
from views.analyzer import render_analyzer
from views.history import render_history
from views.job_search import render_job_search
from views.saved_jobs import render_saved_jobs
from views.applications import render_applications
from views.upload_cv import render_upload_cv
from views.resume_builder import render_resume_builder
from views.cover_letters import render_cover_letters
from views.ai_assistant import render_ai_assistant
from views.easyapply import render_easyapply
from views.notes import render_notes
from views.files import render_files
from views.notifications import render_notifications
from views.settings import render_settings
from views.profile import render_profile

def main():
    st.set_page_config(
        page_title="SniffJob AI — Job Intelligence Platform",
        page_icon="\U0001F50D",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_css()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    # Gate — auth required
    if "user_id" not in st.session_state:
        render_auth()
        return

    render_sidebar()
    render_header()

    page = st.session_state.current_page
    routes = {
        "dashboard":     render_dashboard,
        "analyzer":      render_analyzer,
        "job_search":    render_job_search,
        "history":       render_history,
        "saved_jobs":    render_saved_jobs,
        "applications":  render_applications,
        "upload_cv":     render_upload_cv,
        "resume_builder":render_resume_builder,
        "cover_letters": render_cover_letters,
        "ai_assistant":  render_ai_assistant,
        "easyapply":     render_easyapply,
        "notes":         render_notes,
        "files":         render_files,
        "notifications": render_notifications,
        "settings":      render_settings,
        "profile":       render_profile,
    }
    fn = routes.get(page)
    if fn:
        fn()
    else:
        st.error(f"Page '{page}' not found.")




if __name__ == "__main__":
    main()