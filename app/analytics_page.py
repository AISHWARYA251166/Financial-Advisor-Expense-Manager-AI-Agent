import streamlit as st
import pandas as pd
import plotly.express as px
from core.expense_manager import ExpenseManager

expense_manager = ExpenseManager()

def render_analytics_page():
    st.header('📈 Analytics')
    expenses = expense_manager.list_expenses()
    if not expenses:
        st.info('No data yet.')
        return
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby('date')['amount'].sum().reset_index()
    fig = px.line(daily, x='date', y='amount', title='Daily Spending')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Top Merchants')
    merchants = df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(5)
    st.bar_chart(merchants)
