# core/expense_manager.py
from typing import List, Dict
from sqlalchemy.orm import Session
from database.db import SessionLocal, init_db
from database.models import Expense, Budget
from .category_rules import categorize_text

# Ensure DB initialized on import (idempotent)
init_db()

class ExpenseManager:
    def __init__(self):
        # lightweight: we open sessions per operation
        pass

    def _get_session(self) -> Session:
        return SessionLocal()

    def add_expense(self, expense: Dict, source: str = "manual") -> Dict:
        """
        Add an expense and return the inserted row as dict.
        """
        s = self._get_session()
        try:
            e = Expense(
                amount=float(expense.get('amount', 0) or 0),
                merchant=expense.get('merchant') or "Unknown",
                category=(expense.get('category') or categorize_text(expense.get('merchant',''))).lower(),
                date=expense.get('date') or "",
                paymentMethod=expense.get('paymentMethod') or "Unknown",
                source=source
            )
            s.add(e)
            s.commit()
            s.refresh(e)
            return {
                'id': e.id,
                'amount': e.amount,
                'merchant': e.merchant,
                'category': e.category,
                'date': e.date,
                'paymentMethod': e.paymentMethod,
                'source': e.source,
                'timestamp': e.timestamp.isoformat() if e.timestamp else None
            }
        finally:
            s.close()

    def list_expenses(self) -> List[Dict]:
        s = self._get_session()
        try:
            rows = s.query(Expense).order_by(Expense.date.desc(), Expense.id.desc()).all()
            out = []
            for e in rows:
                out.append({
                    'id': e.id,
                    'amount': e.amount,
                    'merchant': e.merchant,
                    'category': e.category,
                    'date': e.date,
                    'paymentMethod': e.paymentMethod,
                    'source': e.source,
                    'timestamp': e.timestamp.isoformat() if e.timestamp else None
                })
            return out
        finally:
            s.close()

    def bulk_add_from_list(self, rows: List[Dict], source: str = "csv") -> int:
        s = self._get_session()
        added = 0
        try:
            for r in rows:
                e = Expense(
                    amount=float(r.get('amount', 0) or 0),
                    merchant=r.get('merchant') or "Unknown",
                    category=(r.get('category') or "other").lower(),
                    date=r.get('date') or "",
                    paymentMethod=r.get('paymentMethod') or "CSV",
                    source=source
                )
                s.add(e)
                added += 1
            s.commit()
            return added
        finally:
            s.close()

    def clear_all(self):
        s = self._get_session()
        try:
            s.query(Expense).delete()
            s.commit()
        finally:
            s.close()

    # Optional budget helpers
    def set_budget(self, category: str, amount: float):
        s = self._get_session()
        try:
            b = s.query(Budget).filter(Budget.category == category).first()
            if b:
                b.amount = float(amount)
            else:
                b = Budget(category=category, amount=float(amount))
                s.add(b)
            s.commit()
        finally:
            s.close()

    def get_budgets(self) -> Dict[str, float]:
        s = self._get_session()
        try:
            rows = s.query(Budget).all()
            return {r.category: r.amount for r in rows}
        finally:
            s.close()
