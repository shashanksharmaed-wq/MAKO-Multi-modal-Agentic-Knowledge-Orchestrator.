import streamlit as st
import streamlit_authenticator as stauth
from lesson_planner import LessonPlanner

# --- INITIAL CONFIG ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# --- USER DATA SETUP ---
# We are using 'password123' for all accounts. 
# In this version, we set auto_hash=True so the library handles the math for us.
usernames = [f"user{i}" for i in range(1, 11)]
credentials = {
    "usernames": {
        u: {
            "name": f"Trial User {u[4:]}", 
            "password": "password123"  # Plain text here, handled by auto_hash below
        } for u in usernames
    }
}

# --- AUTHENTICATION ---
# cookie_name and key are for session persistence
authenticator = stauth.Authenticate(
    credentials, 
    "mako_session_cookie", 
    "mako_secret_key", 
    cookie_expiry_days=1,
    auto_hash=True  # THIS IS THE KEY FIX: It hashes 'password123' correctly for you
)

# Render the login widget
# Using st.session_state is more reliable in newer versions
try:
    authenticator.login(location='main')
except Exception as e:
    st.error(f"Authentication Error: {e}")

# --- APP LOGIC ---
if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.info('🦅 Welcome to MAKO. Please log in to continue.')
elif st.session_state["authentication_status"]:
    # SUCCESSFUL LOGIN
    username = st.session_state["username"]
    name = st.session_state["name"]
    
    st.sidebar.title(f"Welcome, {name}")
    authenticator.logout('Logout', 'sidebar')

    # Main Navigation
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📚 Lesson Planner", "🔒 The Vault"])

    with tab1:
        st.title("🦅 MAKO Hub")
        st.write(f"System Status: **Online** | User: **{username}**")
        st.info("Agentic Knowledge Orchestrator initialized.")

    with tab2:
        try:
            planner = LessonPlanner()
            planner.render_ui()
        except Exception as e:
            st.error(f"Error loading Lesson Planner: {e}")

    with tab3:
        st.subheader("🔒 Secure Vault")
        # Logic: user1 to user5 are "Directors"
        allowed_users = ["user1", "user2", "user3", "user4", "user5"]
        
        if username in allowed_users:
            st.success("✨ Director Access Granted.")
            st.write("Welcome, Director. Sensitive data is now visible.")
        else:
            st.error("Vault Locked. Upgrade your trial for Director Clearance.")

# --- FOOTER ---
st.markdown("---")
st.caption("MAKO Agentic Knowledge Orchestrator | © 2026")
