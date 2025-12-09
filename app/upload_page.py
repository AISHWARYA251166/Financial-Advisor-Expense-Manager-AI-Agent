# app/upload_page.py
import streamlit as st
from PIL import Image
from core.expense_manager import ExpenseManager
from services.toolbox import Tools

expense_manager = ExpenseManager()

def render_upload_page():
    st.header("📤 Upload Expense (Image / CSV / Manual)")

    api_key = st.session_state.get('gemini_api_key', '')

    col1, col2 = st.columns([2,1])

    with col1:
        uploaded = st.file_uploader("Image (png/jpg) or CSV", type=['png','jpg','jpeg','csv'], key='upload_main')

        if uploaded:
            if uploaded.name.lower().endswith('.csv'):
                # CSV import
                try:
                    # Tools.parse_expenses_csv works without needing gemini_model usages (but requires api_key in constructor)
                    parser = Tools(api_key=api_key or "dummy_key")
                    rows = parser.parse_expenses_csv(uploaded)
                    count = expense_manager.bulk_add_from_list(rows, source="csv")
                    st.success(f"Imported {count} expenses from CSV.")
                except Exception as e:
                    st.error(f"CSV import failed: {e}")
            else:
                # Image upload
                try:
                    image = Image.open(uploaded).convert("RGB")
                    st.image(image, caption="Uploaded Receipt", use_column_width=True)
                except Exception as e:
                    st.error(f"Could not open image: {e}")
                    image = None

                if image:
                    if not api_key:
                        st.info("Enter Gemini API key in the sidebar to enable image extraction.")
                    if st.button("🚀 Extract Using Gemini", key="extract_btn"):
                        if not api_key:
                            st.error("Gemini API key required")
                        else:
                            try:
                                tools = Tools(api_key=api_key)
                                parsed = tools.extract_expense_from_image(image)
                                expense_manager.add_expense(parsed, source='vision')
                                st.success("Expense extracted and saved to database.")
                                st.json(parsed)
                            except Exception as e:
                                st.error(f"Extraction failed: {e}")

        st.markdown("---")
        st.subheader("✍ Manual Entry")
        with st.form("manual_entry", clear_on_submit=True):
            amt = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
            merchant = st.text_input("Merchant")
            category = st.selectbox("Category", options=['food','transport','entertainment','shopping','utilities','other'])
            payment = st.text_input("Payment Method", value="Manual")
            date = st.date_input("Date")
            submitted = st.form_submit_button("➕ Add Expense")
            if submitted:
                if amt > 0 and merchant:
                    expense = {
                        'amount': float(amt),
                        'merchant': merchant,
                        'category': category,
                        'date': date.strftime('%Y-%m-%d'),
                        'paymentMethod': payment
                    }
                    expense_manager.add_expense(expense, source='manual')
                    st.success("Expense added.")
                else:
                    st.error("Enter a valid amount and merchant.")

    with col2:
        st.subheader("Recent Expenses")
        ex = expense_manager.list_expenses()
        if not ex:
            st.info("No expenses yet. Add using any source.")
        else:
            import pandas as pd
            df = pd.DataFrame(ex)
            st.dataframe(df.sort_values(by='date', ascending=False).head(12))
            if st.button("Clear All"):
                expense_manager.clear_all()
                st.success("All expenses cleared.")
