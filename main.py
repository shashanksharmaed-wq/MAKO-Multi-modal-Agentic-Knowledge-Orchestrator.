import streamlit as st
import streamlit_authenticator as stauth
from lesson_planner import LessonPlanner

# --- INITIAL CONFIG ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# --- USER DATA SETUP ---
# Password for all users: password123
# Note: This is a pre-generated BCrypt hash for "password123"
hashed_password = ['$2b$12$h.p.n8.hB6O6T.8pP8pP8uxQz5f5Z5f5Z5f5Z5f5Z5f5Z5f5Z5f5Z']

usernames = [f"user{i}" for i in range(1, 11)]
credentials = {
    "usernames": {
        u: {
            "name": f"Trial User {u[4:]}", 
            "password": hashed_password[0]
        } for u in usernames
    }
}

# --- AUTHENTICATION ---
# cookie_name and key can be any string for session persistence
authenticator = stauth.Authenticate(
    credentials, 
    "mako_cookie", 
    "mako_secret_key", 
    cookie_expiry_days=1
)

# Login Widget
name, authentication_status, username = authenticator.login(location='main')

# --- APP LOGIC BASED ON LOGIN ---
if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.info('🦅 Please enter your credentials to access the MAKO Hub.')
elif authentication_status:
    # SUCCESSFUL LOGIN
    st.sidebar.title(f"Welcome, {name}")
    authenticator.logout('Logout', 'sidebar')

    # Main Navigation
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📚 Lesson Planner", "🔒 The Vault"])

    with tab1:
        st.title("🦅 MAKO Hub")
        st.write(f"Hello **{name}**. System Status: **Online**")
        st.metric(label="Agent Status", value="Active", delta="All Systems Nominal")

    with tab2:
        # Assuming LessonPlanner is defined in lesson_planner.py
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
            st.info("Commercial Data: Tier 1 Clearance Active.")
            st.write("---")
            st.write("Welcome to the inner sanctum. Your sensitive files and agent logs are stored here.")
        else:
            st.error("Vault Locked. Upgrade your trial to unlock Director-level sectors.")
            st.warning("Access Denied for non-Director accounts.")

# --- FOOTER ---
st.markdown("---")
st.caption("MAKO Agentic Knowledge Orchestrator v1.0 | Secure Session Active")
