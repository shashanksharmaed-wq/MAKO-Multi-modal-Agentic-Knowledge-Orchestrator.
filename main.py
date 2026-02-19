import streamlit as st
import streamlit_authenticator as stauth
from lesson_planner import LessonPlanner
# Import other agents if they are ready, e.g.:
# from agents.researcher import ResearcherAgent

# --- INITIAL CONFIG ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# --- AUTHENTICATION SETUP ---
# Password: password123
hashed_pw = stauth.Hasher(['password123']).generate()[0]

usernames = [f"user{i}" for i in range(1, 11)]
credentials = {
    "usernames": {
        u: {
            "name": f"Trial User {u[4:]}",
            "password": hashed_pw,
            "email": f"{u}@mako.ai"
        } for u in usernames
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "mako_session_cookie",
    "mako_secret_key",
    30
)

# Render Login
try:
    authenticator.login(location='main')
except Exception as e:
    st.error(f"Login Component Error: {e}")

# --- MAIN APP LOGIC ---
if st.session_state.get("authentication_status"):
    username = st.session_state["username"]
    st.sidebar.title(f"🦅 Welcome, {st.session_state['name']}")
    authenticator.logout('Logout', 'sidebar')

    # ALL CORE FUNCTIONS IN TABS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "📚 Lesson Planner", 
        "📝 Create Assessment", 
        "✅ Answer Checker",
        "📓 My Notes",
        "🔒 The Vault"
    ])

    with tab1:
        st.title("🦅 MAKO Dashboard")
        st.info("Agentic Hub is Online. All systems nominal.")
        col1, col2 = st.columns(2)
        col1.metric("Active Agents", "4")
        col2.metric("Storage Used", "12%")

    with tab2:
        st.header("📚 Lesson Planner")
        try:
            planner = LessonPlanner()
            planner.render_ui()
        except Exception as e:
            st.error(f"Error loading Lesson Planner: {e}")

    with tab3:
        st.header("📝 Assessment Generator")
        topic = st.text_input("Enter Subject/Topic for Assessment:")
        difficulty = st.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"])
        if st.button("Generate Questions"):
            st.write("---")
            st.success(f"Agent is generating a {difficulty} assessment for: {topic}")
            # Insert call to your assessment agent here

    with tab4:
        st.header("✅ Answer Checker")
        st.write("Upload an answer sheet or paste text to verify accuracy.")
        uploaded_file = st.file_uploader("Upload Student Answers (PDF/Image)", type=['pdf', 'png', 'jpg'])
        if st.button("Check Answers"):
            st.warning("Feature initializing... Ensure your document_processor.py is configured.")

    with tab5:
        st.header("📓 Digital Notebook")
        if 'user_notes' not in st.session_state:
            st.session_state['user_notes'] = ""
        
        user_input = st.text_area("Write or edit your notes here:", value=st.session_state['user_notes'], height=300)
        if st.button("Save Notes"):
            st.session_state['user_notes'] = user_input
            st.success("Notes saved to current session!")

    with tab6:
        st.subheader("🔒 Secure Vault")
        # Access Control
        if username in ["user1", "user2", "user3", "user4", "user5"]:
            st.success("✨ Director Access Granted.")
            st.info("Confidential Commercial Data: Tier 1 Clearance.")
        else:
            st.error("Vault Locked. Upgrade your trial to unlock Director Clearance.")

elif st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect')
elif st.session_state.get("authentication_status") is None:
    st.info('🦅 Please enter credentials to access the Orchestrator.')

# --- FOOTER ---
st.markdown("---")
st.caption("MAKO Agentic Knowledge Orchestrator v1.0 | Built with Streamlit")
