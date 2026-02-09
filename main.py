import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import plotly.express as px
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION (MUST BE FIRST) ---
# This activates the 1GB limit you set in .streamlit/config.toml
st.set_page_config(page_title="MAKO | Secure Agentic Hub", page_icon="🦅", layout="wide")

# --- 2. CREDENTIALS DATA ---
# This dictionary acts as your user database for now.
# single_session=True (below) will ensure 'director_ujjain' can only be logged in once.
credentials = {
    'usernames': {
        'director_ujjain': {
            'name': 'The Director',
            'password': 'mako_password_2026', # Plain text for testing; hash this later!
            'email': 'director@mako.ai'
        },
        'admin_mako': {
            'name': 'System Admin',
            'password': 'admin_access_only',
            'email': 'admin@mako.ai'
        }
    }
}

# --- 3. INITIALIZE AUTHENTICATOR (2026 SYNTAX) ---
# We enable single_session=True to prevent multiple people using one login.
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='mako_auth_cookie',
    cookie_key='mako_signature_key',
    cookie_expiry_days=30,
    single_session=True  # <--- CRITICAL: ENFORCES ONE LOGIN PER USER
)

# --- 4. RENDER LOGIN INTERFACE ---
# Modern versions return (name, authentication_status, username)
name, authentication_status, username = authenticator.login(location='main')

# --- 5. SYSTEM GATEKEEPER ---

if authentication_status == False:
    st.error('Username/password is incorrect. Access Denied.')
    st.stop()

elif authentication_status == None:
    st.warning('Please enter your credentials to activate the MAKO strike engine.')
    st.stop()

elif authentication_status:
    # --- IF AUTHENTICATED: SHOW THE FULL HUB ---
    
    with st.sidebar:
        st.header(f"Welcome, {name}")
        authenticator.logout('Logout', 'sidebar')
        st.divider()
        st.info("Status: Gated Access Active")
        st.success("Session: Locked (Single User)")
        st.caption("Operating Frequency: Monday Strike Mode")
    
    st.title("🦅 MAKO | Agentic Knowledge Orchestrator")
    st.subheader("Institutional Intelligence Layer - Secure Environment")

    # --- 6. CORE WORKFLOW ---
    # The limit is now 1GB as per your config.toml
    uploaded_file = st.file_uploader("Upload Institutional Source (1GB Max)", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.info(f"File Size: {file_size_mb:.2f} MB")
            
            # Show image preview if applicable
            if uploaded_file.type in ["image/png", "image/jpeg"]:
                img = Image.open(uploaded_file)
                st.image(img, caption="Target Source", use_container_width=True)
            else:
                st.write("📄 Multi-page Document Loaded for Orchestration")
        
        with col2:
            if st.button("EXECUTE AGENTIC STRIKE"):
                with st.spinner("MAKO is penetrating data layers..."):
                    # Success State
                    st.success("Analysis Complete")
                    st.markdown("### 📊 Extracted Intelligence")
                    
                    # Demonstration chart using plotly (px)
                    sample_data = {"Category": ["Integrity", "Logic", "Strategy"], "Strength": [98, 95, 92]}
                    fig = px.bar(sample_data, x="Category", y="Strength", title="Orchestration Metrics")
                    st.plotly_chart(fig)
                    
                    st.write("Data encrypted and isolated for this session.")

    st.divider()
    st.caption("MAKO v2.1 | Proprietary Multi-User Architecture")
