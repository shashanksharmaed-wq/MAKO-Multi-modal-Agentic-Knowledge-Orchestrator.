import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import plotly.express as px
import os

# --- 1. CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="MAKO | Secure Vault", page_icon="🦅", layout="wide")

# --- 2. THE TRIAL DATABASE ---
# Trial 01-05: Unlocked (Full Vault Access)
# Trial 06-10: Locked (Limited View)
# Note: For security, I have pre-defined the structure.
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
    single_session=True # Enforces one login per person
)

# --- 4. THE LOGIN STRIKE ---
# In the 2026 version, we don't catch the return value to avoid TypeErrors.
# We check st.session_state directly.
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
    user_role = credentials['usernames'][username]['role']

    with st.sidebar:
        st.header(f"Verified: {user_name}")
        authenticator.logout('Lock & Logout', 'sidebar')
        st.divider()
        if user_role in ['admin', 'unlocked']:
            st.success("VAULT STATUS: UNLOCKED")
        else:
            st.error("VAULT STATUS: LIMITED TRIAL")

    # --- THE DIFFERENTIATED VIEWS ---
    if user_role in ['admin', 'unlocked']:
        # THE OPEN VAULT (Full Features)
        st.title("🦅 MAKO | Agentic Knowledge Orchestrator")
        st.info("Full Institutional Access Enabled.")
        
        uploaded_file = st.file_uploader("Upload Source (1GB Max)", type=['png', 'jpg', 'pdf'])
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open(uploaded_file), use_container_width=True) if uploaded_file.type.startswith('image') else st.write("📄 Document Active")
            with col2:
                if st.button("EXECUTE AGENTIC STRIKE"):
                    with st.spinner("Processing..."):
                        st.success("Intelligence Secured.")
                        st.plotly_chart(px.bar({"Metrics": [100]}, title="Strike Power"))
    
    else:
        # THE LIMITED VAULT
        st.title("🔒 MAKO | Restricted Trial View")
        st.warning(f"Trial User {username[-2:]}, your current account tier does not allow 1GB uploads.")
        
        st.markdown("""
        ### Upgrade Required
        You are currently on a **Limited Trial**. To unlock the full extraction engine, 
        contact the Director for an **Institutional Key**.
        
        **Email:** admin@mako.ai
        """)
        st.button("EXECUTE STRIKE (Disabled)", disabled=True)

    st.divider()
    st.caption(f"MAKO v2.2 | Session Locked for {username}")
