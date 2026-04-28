import os
import re

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

def get_block(start_line, end_line):
    return "".join(lines[start_line:end_line])

# We'll parse by looking for specific function definitions.
# Let's find all function defs and class defs line indices
defs = []
for i, line in enumerate(lines):
    if line.startswith("def ") or line.startswith("class ") or line.startswith("# ──"):
        defs.append((i, line.strip()))

def find_line(prefix):
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            return i
    return -1

# Let's write specific extractors:
database_start = find_line("class Database:")
db_instance = find_line("db = Database()")
load_css_start = find_line("def load_css():")
bi_start = find_line("def bi(")
status_icon_start = find_line("STATUS_ICON   =")
simulate_start = find_line("def simulate_analysis(")
build_pdf_start = find_line("def build_pdf(")
render_sidebar_start = find_line("def render_sidebar():")
render_header_start = find_line("def render_header():")
render_auth_start = find_line("def render_auth():")
render_dashboard_start = find_line("def render_dashboard():")
render_analyzer_start = find_line("def render_analyzer():")
show_result_start = find_line("def _show_result(")
render_history_start = find_line("def render_history():")
render_job_search_start = find_line("def render_job_search():")
render_saved_jobs_start = find_line("def render_saved_jobs():")
render_applications_start = find_line("def render_applications():")
render_upload_cv_start = find_line("def render_upload_cv():")
init_resume_start = find_line("def _init_resume_state():")
render_resume_builder_start = find_line("def render_resume_builder():")
render_cover_letters_start = find_line("def render_cover_letters():")
render_ai_assistant_start = find_line("def render_ai_assistant():")
render_easyapply_start = find_line("def render_easyapply():")
render_notes_start = find_line("def render_notes():")
render_files_start = find_line("def render_files():")
render_notifications_start = find_line("def render_notifications():")
render_settings_start = find_line("def render_settings():")
render_profile_start = find_line("def render_profile():")
main_start = find_line("def main():")

# 1. database.py
with open("database.py", "w", encoding="utf-8") as f:
    f.write("import streamlit as st\nfrom datetime import datetime\n\n")
    f.write(get_block(database_start, db_instance + 1))

# 2. config.py
with open("config.py", "w", encoding="utf-8") as f:
    f.write(get_block(status_icon_start, simulate_start))

# 3. utils.py
with open("utils.py", "w", encoding="utf-8") as f:
    f.write("import streamlit as st\nimport time\nimport random\nfrom datetime import datetime\nimport re\n")
    f.write("from config import *\n\n")
    f.write(get_block(bi_start, status_icon_start))
    f.write(get_block(simulate_start, build_pdf_start))
    f.write(get_block(show_result_start, render_history_start))

# 4. pdf_builder.py
with open("pdf_builder.py", "w", encoding="utf-8") as f:
    f.write("import io\nimport streamlit as st\n")
    f.write(get_block(find_line("try:\n    from reportlab"), find_line("# ── Lightweight mock DB")))
    f.write(get_block(build_pdf_start, render_sidebar_start))

# 5. components/style.py
with open("components/style.py", "w", encoding="utf-8") as f:
    f.write("import streamlit as st\n\n")
    f.write(get_block(load_css_start, bi_start))

# 6. components/sidebar.py
with open("components/sidebar.py", "w", encoding="utf-8") as f:
    f.write("import streamlit as st\nfrom database import db\nfrom utils import bi\n\n")
    f.write(get_block(render_sidebar_start, render_header_start))

# 7. components/header.py
with open("components/header.py", "w", encoding="utf-8") as f:
    f.write("import streamlit as st\nfrom database import db\nfrom utils import bi\n\n")
    f.write(get_block(render_header_start, render_auth_start))

# Function to write a view file
def write_view(name, start, end):
    with open(f"views/{name}.py", "w", encoding="utf-8") as f:
        f.write("import streamlit as st\nimport time\nimport json\nfrom database import db\nfrom utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result\nfrom config import *\n")
        if name == "resume_builder":
            f.write("from pdf_builder import build_pdf\n")
            f.write("import io\n")
        f.write("\n")
        f.write(get_block(start, end))

# 8. Views
write_view("auth", render_auth_start, render_dashboard_start)
write_view("dashboard", render_dashboard_start, render_analyzer_start)
write_view("analyzer", render_analyzer_start, show_result_start)
write_view("history", render_history_start, render_job_search_start)
write_view("job_search", render_job_search_start, render_saved_jobs_start)
write_view("saved_jobs", render_saved_jobs_start, render_applications_start)
write_view("applications", render_applications_start, render_upload_cv_start)
write_view("upload_cv", render_upload_cv_start, init_resume_start)
write_view("resume_builder", init_resume_start, render_cover_letters_start)
write_view("cover_letters", render_cover_letters_start, render_ai_assistant_start)
write_view("ai_assistant", render_ai_assistant_start, render_easyapply_start)
write_view("easyapply", render_easyapply_start, render_notes_start)
write_view("notes", render_notes_start, render_files_start)
write_view("files", render_files_start, render_notifications_start)
write_view("notifications", render_notifications_start, render_settings_start)
write_view("settings", render_settings_start, render_profile_start)
write_view("profile", render_profile_start, main_start)

# 9. Main app.py replacement
with open("app_new.py", "w", encoding="utf-8") as f:
    f.write("""import streamlit as st

from components.style import load_css
from components.sidebar import render_sidebar
from components.header import render_header

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

""")
    f.write(get_block(main_start, len(lines)))

print("Split completed successfully.")
