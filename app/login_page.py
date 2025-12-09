import streamlit as st
from core.auth_service import AuthService

auth = AuthService()

def render_login_page():

    # -------------------------------
    # Custom CSS for modern UI
    # -------------------------------
    st.markdown("""
    <style>
        .login-container {
            max-width: 420px;
            margin: 60px auto;
            padding: 30px 30px;
            background: #ffffff10;
            backdrop-filter: blur(12px);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }

        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #4F46E5;
            margin-bottom: 8px;
        }

        .login-subtext {
            text-align: center;
            color: #8b8b8b;
            margin-bottom: 25px;
        }

        .full-width-btn button {
            width: 100% !important;
            border-radius: 8px !important;
            height: 45px;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Login Box
    # -------------------------------
  

    st.markdown('<div class="login-title">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtext">Log in to access your financial dashboard</div>', unsafe_allow_html=True)

    email = st.text_input("📧 Email Address", key="login_email", placeholder="you@example.com")
    password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")

    st.markdown("")  # spacing

    # Login Button
    login_btn = st.container()
    with login_btn:
        col = st.columns([1])[0]
        if col.button("🔐 Login", use_container_width=True):
            ok, result = auth.login(email, password)
            if ok:
                st.session_state["logged_in"] = True
                st.session_state["user"] = result
                st.success(f"Welcome back, {result['name']}!")
                st.rerun()
            else:
                st.error(result)

    st.markdown("<br>", unsafe_allow_html=True)

    # Divider
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # Create Account Button
    signup_container = st.container()
    with signup_container:
        col = st.columns([1])[0]
        if col.button("📝 Create an Account", use_container_width=True):
            st.session_state["show_signup"] = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
