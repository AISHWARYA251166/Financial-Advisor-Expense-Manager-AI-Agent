# app/advice_page.py
import streamlit as st
from core.expense_manager import ExpenseManager
from services.guru_service import GuruService
from services.gemini_advice import GeminiAdvice
import json

expense_manager = ExpenseManager()
guru = GuruService()

def render_advice_page():
    st.header("💡 Get Personalized Financial Advice")

    api_key = st.session_state.get('gemini_api_key', '')
    if not api_key:
        st.info("Enter your Gemini API key in the sidebar to generate advice.")
        return

    # ------------------------------
    # Guru Documents Upload Section
    # ------------------------------
    st.subheader("📚 Upload Guru Documents (PDF / TXT / MD)")
    uploaded_doc = st.file_uploader(
        "Upload a financial book or article to enrich advice",
        type=['pdf', 'txt', 'md'],
        key='guru_upload'
    )

    if uploaded_doc:
        ent = guru.ingest_file(uploaded_doc, uploaded_doc.name)
        st.success(f"Ingested {ent['filename']}")

    # List stored docs
    docs = guru.list_docs()
    if docs:
        st.info(f"{len(docs)} guru document(s) available for context.")
        for d in docs:
            st.markdown(f"- **{d['filename']}**")
    else:
        st.warning("Upload at least one Guru document to improve advice quality.")

    # ------------------------------
    # Expenses Check
    # ------------------------------
    expenses = expense_manager.list_expenses()
    if not expenses:
        st.info("No expenses yet. Upload receipts or CSV to continue.")
        return

    total_spent = sum(e.get('amount', 0) for e in expenses)
    st.metric("Total Spent", f"₹{total_spent:,.0f}")

    # ------------------------------
    # Advice Settings
    # ------------------------------
    budget = st.number_input(
        "Monthly Budget (₹)",
        min_value=0,
        value=30000,
        step=500,
        key='advice_budget'
    )

    philosophy = st.selectbox(
        "Financial Philosophy",
        options=['balanced', 'aggressive', 'conservative'],
        index=0
    )

    # ------------------------------
    # Generate Advice
    # ------------------------------
    if st.button("🎯 Generate Advice"):
        with st.spinner("Generating advice..."):
            try:
                # Build category breakdown
                breakdown = {}
                for e in expenses:
                    c = e.get('category', 'other')
                    breakdown[c] = breakdown.get(c, 0) + e.get('amount', 0)

                # Retrieve top guru context
                relevant = guru.retrieve_relevant(
                    "personal finance spending budgeting investment India",
                    top_k=3
                )

                context_text = "\n\n".join(
                    [r['snippet'] for r in relevant]
                ) if relevant else "No guru documents available."

                # Create prompt
                advice_engine = GeminiAdvice(api_key)

                prompt = f"""
You are an Indian financial advisor. Use clear, practical, India-specific guidance.

Use these guru documents:
{context_text}

NOW ANALYZE USER’S FINANCES:

Total Monthly Spending: ₹{total_spent}
User's Declared Monthly Budget: ₹{budget}
Financial Philosophy: {philosophy}

Spending Category Breakdown:
{json.dumps(breakdown, indent=2)}

Provide a comprehensive Indian-personalized financial advisory report:

1️⃣ **SPENDING BEHAVIOR ANALYSIS**  
- Identify overspending / underspending  
- Compare with typical Indian household patterns  

2️⃣ **TAX-SAVING RECOMMENDATIONS (INDIA)**  
Explain applicable Indian tax-saving instruments under:
- Section 80C (PPF, ELSS, Life Insurance, EPF, Tax Saver FD)  
- Section 80CCD (NPS)  
- Section 80D (Mediclaim)  
- Home loan tax benefits (Sec 24 & Sec 80C)

3️⃣ **INVESTMENT STRATEGY (BASED ON PROFILE)**  
Balanced profile → mix of ELSS + Blue-chip SIP  
Aggressive → Higher equity SIP, small-cap exposure  
Conservative → PPF + FD + Debt mutual funds  

4️⃣ **MONTHLY SAVINGS PLAN (INDIA-SPECIFIC)**  
- Recommend SIP amounts  
- PPF annual deposit suggestion  
- Emergency fund ideal value in INR  

5️⃣ **ACTIONABLE NEXT STEPS**  
Provide 5 crystal-clear steps like:
- “Start a ₹2,000 SIP in Nifty 50 Index Fund”  
- “Open PPF account at SBI/Post Office, invest ₹12,000 yearly”  
- “Move recurring expenses to UPI AutoPay for control”

Format the entire response in BEAUTIFUL MARKDOWN.
"""


                # Generate advice using Gemini
                resp = advice_engine.model.generate_content(prompt)

                # Display advice
                st.markdown("### 🧠 Your Personalized Financial Advice")
                st.markdown(resp.text)

            except Exception as e:
                st.error(f"Advice generation failed: {e}")
