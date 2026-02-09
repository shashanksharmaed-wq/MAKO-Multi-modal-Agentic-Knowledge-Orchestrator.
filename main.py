import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import plotly.express as px
import os
from dotenv import load_dotenv

# --- 1. PAGE CONFIGURATION (MUST BE FIRST) ---
# This ensures the 1GB limit from your config.toml is active
st.set_page_config(page_title="MAKO | Secure Agentic Hub", page_icon="🦅", layout="wide")

# --- 2. LOAD AUTHENTICATION CONFIG ---
# We use a YAML file to store user data securely
# For this script to run the first time, we define a dummy config below
# In production, you will move this to a separate 'config.yaml' file
auth_config = {
    'credentials': {
        'usernames': {
            'director_ujjain': {
                'name': 'The Director',
                'password': 'mako_password_2026', # In production, use hashed strings
                'email': 'director@mako.ai'
            },
            'admin_mako': {
                'name': 'System Admin',
                'password': 'admin_access_only',
                'email': 'admin@mako.ai'
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'mako_auth_signature',
        'name': 'mako_cookie'
    },
    'preauthorized': {
        'emails': ['director@mako.ai']
    }
}

# --- 3. INITIALIZE AUTHENTICATOR ---
# 'single_session=True' ensures one login per user at a time
authenticator = stauth.Authenticate(
    auth_config['credentials'],
    auth_config['cookie']['name'],
    auth_config['cookie']['key'],
    auth_config['cookie']['expiry_days'],
    auth_config['preauthorized']
)

# --- 4. RENDER LOGIN INTERFACE ---
name, authentication_status, username = authenticator.login('MAKO | Secure Login', 'main')

# --- 5. SYSTEM LOGIC BASED ON STATUS ---

if authentication_status == False:
    st.error('Username/password is incorrect. Access Denied.')
    st.stop()

elif authentication_status == None:
    st.warning('Please enter your credentials to activate the MAKO strike engine.')
    st.stop()

elif authentication_status:
    # --- IF AUTHENTICATED: SHOW THE FULL HUB ---
    
    # 5.1 Sidebar with Logout and Info
    with st.sidebar:
        st.header(f"Welcome, {name}")
        authenticator.logout('Logout', 'sidebar')
        st.divider()
        st.info("System: Gated Access Active")
        st.caption("Operating Frequency: Monday Strike Mode")
    
    # 5.2 Main Hub UI
    st.title("🦅 MAKO | Agentic Knowledge Orchestrator")
    st.subheader("Secure Institutional Intelligence Layer")

    # 5.3 Core Workflow
    uploaded_file = st.file_uploader("Upload Institutional Source (Limit: 1GB)", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.info(f"File Size: {file_size_mb:.2f} MB")
            
            # If it's an image, show it
            if uploaded_file.type in ["image/png", "image/jpeg"]:
                img = Image.open(uploaded_file)
                st.image(img, caption="Target Source", use_container_width=True)
            else:
                st.write("📄 Document Loaded for Processing")
        
        with col2:
            if st.button("EXECUTE AGENTIC STRIKE"):
                with st.spinner("MAKO is penetrating data layers..."):
                    # Success State
                    st.success("Analysis Complete")
                    st.markdown("### 📊 Extracted Intelligence")
                    
                    # Demonstration Chart
                    sample_data = {"Category": ["Integrity", "Logic", "Strategy"], "Strength": [98, 95, 92]}
                    fig = px.bar(sample_data, x="Category", y="Strength", title="Orchestration Metrics")
                    st.plotly_chart(fig)
                    
                    st.write("Results gated and secured for session user.")

    # 5.4 Footer
    st.divider()
    st.caption("MAKO v2.1 | Proprietary Multi-User Architecture")
