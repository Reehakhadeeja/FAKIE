import streamlit as st
from datetime import datetime

class Database:
    """In-memory mock database. Swap with SQLite / Postgres in production."""

    def _init_db(self):
        if "db_store" not in st.session_state:
            st.session_state.db_store = {
                "users": {
                    "demo": {
                        "id": 1, "username": "demo", "password": "demo123",
                        "email": "demo@sniffjob.ai", "avatar": "",
                        "created_at": "2024-01-15",
                    }
                },
                "job_analyses": [],
                "resumes": [],
                "notifications": [
                    {"id": 1, "msg": "Welcome to SniffJob! ", "read": False, "ts": "2025-04-14 10:00"},
                    {"id": 2, "msg": "New fraud pattern detected in IT sector", "read": False, "ts": "2025-04-14 12:00"},
                ],
                "saved_jobs": [],
                "applied_jobs": [],
                "cover_letters": [],
                "notes": [],
            }

    @property
    def store(self):
        self._init_db()
        return st.session_state.db_store

    # Auth
    def authenticate(self, username, password):
        u = self.store["users"].get(username)
        if u and u["password"] == password:
            return u
        return None

    def register(self, username, password, email):
        if username in self.store["users"]:
            return False, "Username already exists"
        uid = len(self.store["users"]) + 1
        self.store["users"][username] = {
            "id": uid, "username": username, "password": password,
            "email": email, "avatar": "",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        }
        return True, "Registered successfully"

    # Job analysis
    def add_job_analysis(self, uid, url, title, company, status, confidence, details, notes=""):
        self.store["job_analyses"].append({
            "user_id": uid, "job_url": url, "job_title": title,
            "company": company, "result": status,
            "confidence_score": confidence, "details": details,
            "notes": notes,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": len(self.store["job_analyses"]) + 1,
        })

    def get_job_history(self, uid):
        return [j for j in self.store["job_analyses"] if j["user_id"] == uid][::-1]

    def delete_job_analysis(self, uid, jid):
        self.store["job_analyses"] = [
            j for j in self.store["job_analyses"]
            if not (j["user_id"] == uid and j["id"] == jid)
        ]

    # Resumes
    def upload_resume(self, uid, fname, fpath, size=0):
        self.store["resumes"].append({
            "user_id": uid, "file_name": fname, "file_path": fpath,
            "size": size, "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": len(self.store["resumes"]) + 1,
        })

    def get_user_resumes(self, uid):
        return [r for r in self.store["resumes"] if r["user_id"] == uid][::-1]

    def delete_resume(self, uid, rid):
        self.store["resumes"] = [
            r for r in self.store["resumes"]
            if not (r["user_id"] == uid and r["id"] == rid)
        ]

    # Notifications
    def get_unread_notifications_count(self, uid):
        return sum(1 for n in self.store["notifications"] if not n["read"])

    def get_all_notifications(self):
        return self.store["notifications"][::-1]

    def mark_all_read(self):
        for n in self.store["notifications"]:
            n["read"] = True

    def add_notification(self, msg):
        self.store["notifications"].append({
            "id": len(self.store["notifications"]) + 1,
            "msg": msg, "read": False,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    # Saved / Applied jobs
    def save_job(self, uid, title, company, url, status="Legit"):
        self.store["saved_jobs"].append({
            "user_id": uid, "title": title, "company": company,
            "url": url, "status": status,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": len(self.store["saved_jobs"]) + 1,
        })

    def get_saved_jobs(self, uid):
        return [j for j in self.store["saved_jobs"] if j["user_id"] == uid][::-1]

    def mark_applied(self, uid, jid, note=""):
        self.store["applied_jobs"].append({
            "user_id": uid, "saved_job_id": jid,
            "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": note,
            "id": len(self.store["applied_jobs"]) + 1,
        })

    def get_applied_jobs(self, uid):
        applied_ids = {a["saved_job_id"] for a in self.store["applied_jobs"] if a["user_id"] == uid}
        return [j for j in self.store["saved_jobs"] if j["id"] in applied_ids]

    # Cover letters
    def save_cover_letter(self, uid, title, company, content):
        self.store["cover_letters"].append({
            "user_id": uid, "title": title, "company": company,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": len(self.store["cover_letters"]) + 1,
        })

    def get_cover_letters(self, uid):
        return [c for c in self.store["cover_letters"] if c["user_id"] == uid][::-1]

    # Notes
    def add_note(self, uid, title, content):
        self.store["notes"].append({
            "user_id": uid, "title": title, "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": len(self.store["notes"]) + 1,
        })

    def get_notes(self, uid):
        return [n for n in self.store["notes"] if n["user_id"] == uid][::-1]

    def delete_note(self, uid, nid):
        self.store["notes"] = [
            n for n in self.store["notes"]
            if not (n["user_id"] == uid and n["id"] == nid)
        ]

    # Stats
    def get_stats(self, uid):
        hist = self.get_job_history(uid)
        return {
            "total": len(hist),
            "legit": sum(1 for j in hist if j["result"] == "Legit"),
            "suspicious": sum(1 for j in hist if j["result"] == "Suspicious"),
            "fraud": sum(1 for j in hist if j["result"] == "Fraud"),
            "saved": len(self.get_saved_jobs(uid)),
            "applied": len(self.get_applied_jobs(uid)),
        }

    # User update
    def update_user(self, username, **kwargs):
        if username in self.store["users"]:
            self.store["users"][username].update(kwargs)


# ── Global DB instance ───────────────────────────────────────────────────────
db = Database()
