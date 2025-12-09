# core/analysis.py
from collections import defaultdict
import pandas as pd
from datetime import datetime
from typing import List, Dict

def df_from_expenses(expenses: List[Dict]):
    df = pd.DataFrame(expenses)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    else:
        df['date'] = pd.to_datetime('today').date()
    return df

def category_totals(expenses: List[Dict]) -> Dict[str,float]:
    df = df_from_expenses(expenses)
    return df.groupby('category')['amount'].sum().to_dict()

def monthly_trend(expenses: List[Dict]):
    df = df_from_expenses(expenses)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    agg = df.groupby('month')['amount'].sum().reset_index()
    agg['month'] = agg['month'].astype(str)
    return agg

def top_merchants(expenses: List[Dict], top_n=5):
    df = df_from_expenses(expenses)
    t = df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(top_n)
    return t.reset_index().to_dict(orient='records')

def budgeting_recommendations(expenses: List[Dict], budget_map: Dict[str,float]):
    """
    Simple recommendations:
     - Identify overbudget categories
     - Suggest reduction % and one recommendation per category
    """
    totals = category_totals(expenses)
    recs = []
    for cat, spent in totals.items():
        budget = budget_map.get(cat, None)
        if budget is None:
            continue
        if spent > budget:
            over = spent - budget
            pct = over / budget * 100
            recs.append({
                'category': cat,
                'status': 'over',
                'spent': spent,
                'budget': budget,
                'over_by': over,
                'recommendation': f"Reduce {cat} by {min(30, int(pct))}%: cut non-essential purchases, set weekly allowance and track receipts."
            })
        else:
            recs.append({
                'category': cat,
                'status': 'ok',
                'spent': spent,
                'budget': budget,
                'recommendation': f"Good job — you are within budget. Consider allocating surplus to SIP/PPF."
            })
    return recs
