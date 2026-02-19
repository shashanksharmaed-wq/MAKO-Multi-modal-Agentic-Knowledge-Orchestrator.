import streamlit as st
import streamlit_authenticator as stauth
from lesson_planner import LessonPlanner

# --- INITIAL CONFIG ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# --- USER DATA SETUP ---
# Pre-hashing is the safest way to avoid the TypeError
# 'password123' hashed:
hashed_pw = stauth.Hasher(['password123']).generate()[0]

usernames = [f"user{i}" for i in range(1, 11)]
credentials = {
    "usernames": {
        u: {
            "name": f"Trial User {u[4:]}",
            "password": hashed_pw,
            "email": f"{u}@example.com"  # New versions require an email field
        } for u in usernames
    }
}

# --- AUTHENTICATION ---
# The new signature: credentials, cookie_name, key, cookie_expiry_days
authenticator = stauth.Authenticate(
    credentials,
    "mako_session_cookie",
    "mako_secret_key",
    30  # cookie_expiry_days must be an integer
)

# Render login - use st.session_state for status checks
try:
    authenticator.login(location='main')
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- APP LOGIC ---
if st.session_state.get("authentication_status"):
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

    with tab2:
        try:
            planner = LessonPlanner()
            planner.render_ui()
        except Exception as e:
            st.error(f"Error loading Lesson Planner: {e}")

    with tab3:
        st.subheader("🔒 Secure Vault")
        # user1 to user5 are Directors
        allowed_users = ["user1", "user2", "user3", "user4", "user5"]
        
        if username in allowed_users:
            st.success("✨ Director Access Granted.")
        else:
            st.error("Vault Locked. Upgrade your trial for Director Clearance.")

elif st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect')
elif st.session_state.get("authentication_status") is None:
    st.info('🦅 Please log in to the MAKO Hub.')

# --- FOOTER ---
st.markdown("---")
st.caption("MAKO Agentic Knowledge Orchestrator | © 2026")
