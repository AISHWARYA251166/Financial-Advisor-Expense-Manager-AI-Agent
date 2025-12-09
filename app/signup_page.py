import streamlit as st
from core.auth_service import AuthService

auth = AuthService()

def render_signup_page():

    # -------------------------------
    # Custom CSS
    # -------------------------------
    st.markdown("""
    <style>
        .signup-container {
            max-width: 430px;
            margin: 60px auto;
            padding: 32px 30px;
            background: #ffffff15;
            backdrop-filter: blur(12px);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        }

        .signup-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #4F46E5;
            margin-bottom: 6px;
        }

        .signup-subtext {
            text-align: center;
            color: #8b8b8b;
            margin-bottom: 25px;
        }

        .full-width-btn button {
            width: 100% !important;
            border-radius: 8px !important;
            height: 45px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }

        .back-btn button {
            width: 100% !important;
            border-radius: 8px !important;
            height: 42px !important;
            background: #e5e7eb !important;
            color: black !important;
            font-weight: 500 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Signup UI Container
    # -------------------------------
    st.markdown('<div class="signup-container">', unsafe_allow_html=True)

    st.markdown('<div class="signup-title">Create Your Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="signup-subtext">Sign up to start managing your finances smarter</div>', unsafe_allow_html=True)

    name = st.text_input("👤 Full Name", key="signup_name", placeholder="Enter your full name")
    email = st.text_input("📧 Email Address", key="signup_email", placeholder="you@example.com")
    password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Choose a secure password")

    st.markdown("")  # spacing

    # -------------------------------
    # Sign Up Button
    # -------------------------------
    sign_btn = st.container()
    with sign_btn:
        if st.button("📝 Sign Up", use_container_width=True):
            ok, result = auth.signup(name, email, password)
            if ok:
                st.success("🎉 Account created successfully! You can now log in.")
                st.session_state["show_signup"] = False
                st.rerun()
            else:
                st.error(result)

    st.markdown("<br>", unsafe_allow_html=True)

    # Divider
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # -------------------------------
    # Back to Login
    # -------------------------------
    back_btn = st.container()
    with back_btn:
        if st.button("⬅ Back to Login", use_container_width=True):
            st.session_state["show_signup"] = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
