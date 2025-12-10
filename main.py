import streamlit as st
from app.layout import apply_layout
from app.upload_page import render_upload_page
from app.dashboard_page import render_dashboard_page
from app.advice_page import render_advice_page
from app.analytics_page import render_analytics_page
from app.analysis_page import render_analysis_page
from core.database import init_db
from app.login_page import render_login_page
from app.signup_page import render_signup_page
import os




# -----------------------------------------------------------
# Streamlit App Settings
# -----------------------------------------------------------
st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="wide")
init_db()
apply_layout()

# -----------------------------------------------------------
# LOGIN / SIGNUP HANDLING
# -----------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

if not st.session_state["logged_in"]:
    if st.session_state["show_signup"]:
        render_signup_page()
    else:
        render_login_page()

    st.stop()



# -----------------------------------------------------------
# Sidebar Header
# -----------------------------------------------------------
st.sidebar.markdown("""
<style>

    .sidebar-title-block {
        text-align: center;
        margin-top: -8px;
        margin-bottom: 22px;
    }

    .sidebar-title-icon {
        font-size: 38px;
        display: block;
        margin-bottom: -4px;
    }

    .sidebar-title-text {
        font-size: 1.55rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        color: transparent;
    }

    .sidebar-subtitle {
        color: #9CA3AF;
        font-size: 0.82rem;
        margin-top: -6px;
    }

</style>

<div class="sidebar-title-block">
    <span class="sidebar-title-icon">💰</span>
    <div class="sidebar-title-text">AI Financial Advisor</div>
    <div class="sidebar-subtitle">Gemini Vision + Gemini LLM</div>
</div>
""", unsafe_allow_html=True)



# -----------------------------------------------------------
# GEMINI API KEY (SECURE VERSION)
# -----------------------------------------------------------

# Initialize session variable
if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""

# 1. Try loading from Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    st.session_state["gemini_api_key"] = st.secrets["GEMINI_API_KEY"]

# 2. Fallback to environment variables (for local .env)
elif os.getenv("GEMINI_API_KEY"):
    st.session_state["gemini_api_key"] = os.getenv("GEMINI_API_KEY")

# 3. If not found, show warning
if not st.session_state["gemini_api_key"]:
    st.sidebar.warning("⚠ Gemini API Key not found. Add it in .streamlit/secrets.toml")



# -----------------------------------------------------------
# Navigation Section
# -----------------------------------------------------------
st.sidebar.markdown("### 🧭 Navigation")

def nav_button(label, page_key):
    clicked = st.sidebar.button(label, key=f"nav_{page_key}")
    if clicked:
        st.session_state["active_page"] = page_key

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "upload"

nav_button("📤 Upload Expense", "upload")
nav_button("📊 Dashboard", "dashboard")
nav_button("💡 Get Advice", "advice")
nav_button("📈 Analytics", "analytics")
nav_button("📊 Analysis", "analysis")

page = st.session_state["active_page"]



# -----------------------------------------------------------
# Page Routing
# -----------------------------------------------------------
if page == "upload":
    render_upload_page()
elif page == "dashboard":
    render_dashboard_page()
elif page == "advice":
    render_advice_page()
elif page == "analytics":
    render_analytics_page()
elif page == "analysis":
    render_analysis_page()



# -----------------------------------------------------------
# Sidebar Button Styling
# -----------------------------------------------------------
st.markdown("""
<style>

div[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;
    height: 48px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    padding-left: 14px !important;
    padding-right: 14px !important;

    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 500 !important;

    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;

    margin-bottom: 10px !important;
}

div[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.30) !important;
}

div[data-testid="stSidebar"] div.stButton > button:focus {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)



# -----------------------------------------------------------
# Logout Button (Stays at Bottom)
# -----------------------------------------------------------
logout_container = st.sidebar.empty()

if logout_container.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.markdown("""
<style>
[data-testid="stSidebar"] > div {
    display: flex;
    flex-direction: column;
    height: 100%;
}
[data-testid="stSidebar"] > div > div:last-child {
    margin-top: auto;
}
</style>
""", unsafe_allow_html=True)
