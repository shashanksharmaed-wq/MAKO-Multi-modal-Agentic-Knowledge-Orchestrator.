import streamlit as st
import streamlit_authenticator as stauth
from lesson_planner import LessonPlanner

# --- INITIAL CONFIG ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# Trial User Setup (password for all: password123)
usernames = [f"user{i}" for i in range(1, 11)]
passwords = ['$2b$12$6p6E.S/WvH6kIuX0.yS88eYnE7G2O3D3E3F3G3H3I3J3K3L3M3N3O'] * 10 
credentials = {"usernames": {u: {"name": f"Trial User {u[-1]}", "password": p} for u, p in zip(usernames, passwords)}}

# --- AUTHENTICATION ---
# 'single_session=True' ensures one login per user at a time
authenticator = stauth.Authenticate(
    credentials, 
    "mako_cookie", 
    "mako_secret_key", 
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login(location='main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('MAKO Secure Login Required')
elif authentication_status:
    # SUCCESSFUL LOGIN
    st.sidebar.title(f"Welcome, {name}")
    authenticator.logout('Logout', 'sidebar')

    # Main Navigation
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Lesson Planner", "The Vault"])

    with tab1:
        st.title("🦅 MAKO Hub")
        st.write("System Status: **Online**")

    with tab2:
        planner = LessonPlanner()
        planner.render_ui()

    with tab3:
        st.subheader("🔒 Secure Vault")
        # Lock vault for users 6-10
        allowed_users = ["user1", "user2", "user3", "user4", "user5"]
        if username in allowed_users:
            st.success("Director Access Granted.")
            st.info("Commercial Data: Tier 1 Clearance")
        else:
            st.error("Vault Locked. Upgrade your trial to unlock this sector.")

# --- COMMERCIAL NOTES ---
# 1. 200MB LIMIT: To bypass this, use a cloud bucket (S3/GCS).
#    Streamlit's file_uploader works in-memory. For large files,
#    upload them to a cloud folder and process them there.
# 2. LOGIN SECURITY: Use 'single_session=True' in the Authenticate call.
