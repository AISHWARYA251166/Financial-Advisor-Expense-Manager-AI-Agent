import streamlit as st
import pandas as pd
import plotly.express as px
from core.expense_manager import ExpenseManager

expense_manager = ExpenseManager()

def render_dashboard_page():
    st.header("📊 Dashboard")

    # Fetch stored expenses
    expenses = expense_manager.list_expenses()
    if not expenses:
        st.info("No expenses yet. Upload receipts or CSV to get started.")
        return

    df = pd.DataFrame(expenses)

    # Ensure required columns exist
    if "category" not in df.columns:
        df["category"] = "other"
    if "amount" not in df.columns:
        df["amount"] = 0
    if "date" not in df.columns:
        df["date"] = ""

    # --------------- Total Spent ---------------
    total = df["amount"].sum()
    st.metric("Total Spent", f"₹{total:,.0f}")
    

    st.markdown("---")

    # --------------- Friendly Indian Category Labels ---------------
    friendly_names = {
        "food": "🍔 Food & Dining",
        "transport": "🚕 Transport",
        "entertainment": "🎭 Entertainment",
        "shopping": "🛍️ Shopping",
        "utilities": "💡 Utilities",
        "investment": "📈 Investments",
        "other": "🔖 Other"
    }

    st.subheader("Category Breakdown")

    # Group by category
    df["category"] = df["category"].fillna("other")
    cat_df = df.groupby("category")["amount"].sum().reset_index()

    # Map friendly names
    cat_df["friendly"] = cat_df["category"].apply(lambda c: friendly_names.get(c, c))

    # PIE CHART
    fig = px.pie(
        cat_df,
        names="friendly",
        values="amount",
        hole=0.4,
        title="Expenses by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --------------- All Expenses Table ---------------
    st.subheader("🧾 All Expenses")
    df_sorted = df.sort_values(by="date", ascending=False)
    st.dataframe(df_sorted, use_container_width=True)

    # Download CSV
    csv = df_sorted.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv"
    )
