# app/analysis_page.py
import streamlit as st
from core.expense_manager import ExpenseManager
from core.analysis import category_totals, monthly_trend, top_merchants, budgeting_recommendations
import plotly.express as px
from services.splitwise_service import SplitwiseService

expense_manager = ExpenseManager()
split_service = SplitwiseService()

def render_analysis_page():
    st.header("🔎 Spending Analysis & Recommendations")
    expenses = expense_manager.list_expenses()
    if not expenses:
        st.info("No expenses available. Add via Upload or CSV first.")
        return

    # Category totals
    cat_tot = category_totals(expenses)
    st.subheader("Category totals")
    st.table([{ 'Category':k, 'Amount':v} for k,v in cat_tot.items()])

    # Monthly trend
    st.subheader("Monthly spending trend")
    trend = monthly_trend(expenses)
    fig = px.line(trend, x='month', y='amount', markers=True, title="Monthly Spend")
    st.plotly_chart(fig, use_container_width=True)

    # Top merchants
    st.subheader("Top merchants")
    tm = top_merchants(expenses)
    st.table(tm)

    # Budget recommendation
    st.subheader("Budgeting recommendations")
    # budget_map from session or defaults
    budget_map = st.session_state.get('budget_map', {
        'food':5000,'transport':3000,'entertainment':2000,'shopping':4000,'utilities':3000,'other':3000
    })
    recs = budgeting_recommendations(expenses, budget_map)
    for r in recs:
        if r['status']=='over':
            st.error(f"{r['category'].capitalize()}: Over by ₹{r['over_by']:.0f}. {r['recommendation']}")
        else:
            st.success(f"{r['category'].capitalize()}: ₹{r['spent']:.0f} / ₹{r['budget']:.0f}. {r['recommendation']}")

    st.markdown("---")
    # Splitwise CSV import
    st.subheader("Splitwise Group Import (CSV)")
    file = st.file_uploader("Upload Splitwise CSV (group expenses export)", type=['csv'], key='splitwise_csv')
    if file:
        group = split_service.parse_splitwise_csv(file)
        st.write("Imported", len(group), "group expenses")
        # basic per-member summary (if data present)
        # show raw for now
        st.dataframe(group)
