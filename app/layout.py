import streamlit as st

def apply_layout():
    st.markdown("""
    <style>

        /* ---------- MAIN HEADER STYLING ---------- */
        .main-header { 
            font-size: 2.4rem; 
            font-weight: 700; 
            color: #4F46E5; 
            text-align: center; 
            margin-bottom: 4px; 
        }

        .sub-header { 
            color: #6B7280; 
            text-align: center; 
            font-size: 1.05rem;
            margin-top: 0px; 
            margin-bottom: 22px; 
        }


        /* -------------------------------------------------------
           PROFESSIONAL SIDEBAR NAVIGATION BUTTONS (Equal Size)
        ------------------------------------------------------- */

        div[data-testid="stSidebar"] button {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;

            height: 48px !important;        /* EXACT SAME HEIGHT */
            padding: 0 14px !important;

            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            border-radius: 8px !important;
            margin-bottom: 10px !important;

            font-size: 15px !important;
            font-weight: 500 !important;

            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;

            transition: 0.18s ease-in-out !important;
        }

        div[data-testid="stSidebar"] button:hover {
            background: rgba(255,255,255,0.14) !important;
            border-color: rgba(255,255,255,0.25) !important;
        }

        div[data-testid="stSidebar"] button:focus:not(:active) {
            background: linear-gradient(90deg, #4F46E5, #6D28D9) !important;
            border-color: transparent !important;
            color: white !important;
        }


        /* Sidebar headers */
        .sidebar .sidebar-content h2, 
        div[data-testid="stSidebar"] h2 {
            font-size: 1.2rem !important;
            font-weight: 700 !important;
        }

    </style>
    """, unsafe_allow_html=True)

    # Render Title
    st.markdown('<div class="main-header">💰 AI Financial Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Gemini Vision + Gemini LLM — Expense extraction & personalized advice</div>', unsafe_allow_html=True)


def format_inr(amount):
    """Format number into Indian Rupee with commas."""
    try:
        return f"₹{amount:,.2f}"
    except:
        return "₹0.00"

