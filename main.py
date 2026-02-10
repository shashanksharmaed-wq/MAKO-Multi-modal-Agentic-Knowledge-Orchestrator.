import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import plotly.express as px

# --- 1. CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="MAKO | Secure Vault", page_icon="🦅", layout="wide")

# --- 2. THE TRIAL DATABASE ---
credentials = {
    'usernames': {
        'director_ujjain': {'name': 'The Director', 'password': 'mako_password_2026', 'email': 'dir@mako.ai', 'role': 'admin'},
        'trial_01': {'name': 'Trial 01', 'password': 'pass_01', 'email': 't1@mako.ai', 'role': 'unlocked'},
        'trial_02': {'name': 'Trial 02', 'password': 'pass_02', 'email': 't2@mako.ai', 'role': 'unlocked'},
        'trial_03': {'name': 'Trial 03', 'password': 'pass_03', 'email': 't3@mako.ai', 'role': 'unlocked'},
        'trial_04': {'name': 'Trial 04', 'password': 'pass_04', 'email': 't4@mako.ai', 'role': 'unlocked'},
        'trial_05': {'name': 'Trial 05', 'password': 'pass_05', 'email': 't5@mako.ai', 'role': 'unlocked'},
        'trial_06': {'name': 'Trial 06', 'password': 'pass_06', 'email': 't6@mako.ai', 'role': 'limited'},
        'trial_07': {'name': 'Trial 07', 'password': 'pass_07', 'email': 't7@mako.ai', 'role': 'limited'},
        'trial_08': {'name': 'Trial 08', 'password': 'pass_08', 'email': 't8@mako.ai', 'role': 'limited'},
        'trial_09': {'name': 'Trial 09', 'password': 'pass_09', 'email': 't9@mako.ai', 'role': 'limited'},
        'trial_10': {'name': 'Trial 10', 'password': 'pass_10', 'email': 't10@mako.ai', 'role': 'limited'}
    }
}

# --- 3. INITIALIZE AUTHENTICATOR ---
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='mako_vault_cookie_2026',
    cookie_key='mako_secure_key_2026',
    cookie_expiry_days=30,
    single_session=True 
)

# --- 4. THE LOGIN STRIKE ---
authenticator.login()

# --- 5. ACCESS CONTROL LOGIC ---
if st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect.')
    st.stop()
elif st.session_state.get("authentication_status") is None:
    st.warning('Welcome to the MAKO Trial Hub. Enter your ID to unlock.')
    st.stop()

# --- 6. THE VAULT (AUTHORIZED AREA) ---
if st.session_state.get("authentication_status"):
    username = st.session_state["username"]
    user_name = st.session_state["name"]
    # Retrieve the role safely from the credentials dictionary
    user_role = credentials['usernames'][username]['role']

    with st.sidebar:
        st.header(f"Verified: {user_name}")
        authenticator.logout('Lock & Logout', 'sidebar')
        st.divider()
        # FIX: Explicitly checking if user is admin OR unlocked
        if user_role == 'admin' or user_role == 'unlocked':
            st.success("VAULT STATUS: UNLOCKED ✅")
        else:
            st.error("VAULT STATUS: LIMITED TRIAL 🔒")

    # --- THE DIFFERENTIATED VIEWS ---
    # This is the "Gate" that was sticking. It's now wide open for the Director.
    if user_role == 'admin' or user_role == 'unlocked':
        st.title("🦅 MAKO | Agentic Knowledge Orchestrator")
        st.info(f"Welcome, {user_role.upper()}. Full Institutional Access Active.")
        
        uploaded_file = st.file_uploader("Upload Source (1GB Max)", type=['png', 'jpg', 'pdf'])
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                # Use container width for better UI
                if uploaded_file.type.startswith('image'):
                    st.image(Image.open(uploaded_file), use_container_width=True)
                else:
                    st.write("📄 Multi-page Document Active")
            with col2:
                if st.button("EXECUTE AGENTIC STRIKE"):
                    with st.spinner("Processing..."):
                        st.success("Intelligence Secured.")
                        st.plotly_chart(px.bar({"Metrics": [100]}, title="Strike Power"))
    
    else:
        # THE LIMITED VIEW (Trial 06-10)
        st.title("🔒 MAKO | Restricted Trial View")
        st.warning(f"Trial User {username[-2:]}, your current account tier does not allow 1GB uploads.")
        
        st.markdown("""
        ### Upgrade Required
        You are currently on a **Limited Trial**. To unlock the full extraction engine, 
        contact the Director for an **Institutional Key**.
        
        **Email:** admin@mako.ai
        """)
        # Teaser for the locked feature
        st.button("EXECUTE STRIKE (Locked)", disabled=True)

    st.divider()
    st.caption(f"MAKO v2.2 | Session ID: {username} | Mode: {user_role}")
