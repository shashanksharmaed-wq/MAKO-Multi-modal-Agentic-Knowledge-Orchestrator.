import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import plotly.express as px
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="MAKO | Secure Agentic Hub", page_icon="🦅", layout="wide")

# --- 2. DIRECTOR CREDENTIALS ---
# Use these to login: 
# Username: director_ujjain
# Password: mako_password_2026
credentials = {
    'usernames': {
        'director_ujjain': {
            'name': 'The Director',
            'password': 'mako_password_2026', # Change this in production
            'email': 'director@mako.ai'
        },
        'admin_mako': {
            'name': 'System Admin',
            'password': 'admin_access_only',
            'email': 'admin@mako.ai'
        }
    }
}

# --- 3. INITIALIZE AUTHENTICATOR ---
authenticator = stauth.Authenticate(
    credentials,
    'mako_auth_cookie',
    'mako_signature_key',
    30,
    single_session=True  # Enforces one login at a time
)

# --- 4. RENDER LOGIN ---
# FIX: The latest version often uses positional arguments or no arguments for default
# We use the method that ensures the 3-value return works
auth_result = authenticator.login()

# Handle modern return logic
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    authentication_status = st.session_state["authentication_status"]
    username = st.session_state["username"]
else:
    authentication_status = st.session_state.get("authentication_status")

# --- 5. ACCESS CONTROL ---

if authentication_status == False:
    st.error('Username/password is incorrect.')
    st.stop()

elif authentication_status == None:
    st.warning('Please enter your credentials.')
    st.stop()

elif authentication_status:
    # --- IF AUTHENTICATED: REVEAL MAKO ---
    with st.sidebar:
        st.header(f"Welcome, {name}")
        authenticator.logout('Logout', 'sidebar')
        st.divider()
        st.success("Vault Locked: Single Session Active")

    st.title("🦅 MAKO | Agentic Knowledge Orchestrator")
    
    # 6. CORE WORKFLOW
    uploaded_file = st.file_uploader("Upload Institutional Source (1GB Max)", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"File: {uploaded_file.name} | Size: {uploaded_file.size / (1024*1024):.2f} MB")
            if uploaded_file.type in ["image/png", "image/jpeg"]:
                st.image(Image.open(uploaded_file), use_container_width=True)
        
        with col2:
            if st.button("EXECUTE STRIKE"):
                with st.spinner("Processing..."):
                    st.success("Target Analyzed.")
                    sample_data = {"Security": [100], "Logic": [95], "Speed": [90]}
                    st.plotly_chart(px.bar(sample_data, title="Agentic Metrics"))

    st.divider()
    st.caption("MAKO v2.1 | Director's Private Infrastructure")
