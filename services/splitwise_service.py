# services/splitwise_service.py
import pandas as pd
from typing import List, Dict

class SplitwiseService:
    """
    Two ways:
     - parse CSV exported from Splitwise
     - (Optional) API client (skeleton)
    """

    def parse_splitwise_csv(self, file_like) -> List[Dict]:
        # Expect columns: description, cost, paid_by, owed_by (or participant_1...participant_n)
        df = pd.read_csv(file_like)
        results = []
        # Try to detect common Splitwise export columns:
        for _, r in df.iterrows():
            results.append({
                "description": r.get("description") or r.get("Description") or "",
                "amount": float(r.get("cost") or r.get("amount") or 0),
                "date": str(r.get("date","")),
                "paid_by": r.get("paid_by") or r.get("Paid By") or "",
                "split_details": { }  # you can extend to parse per-person
            })
        return results

    # Optional: API integration (requires keys & oauth) — skeleton only
    def api_get_balances(self, consumer_key, consumer_secret, token=None):
        raise NotImplementedError("Splitwise API integration requires oauth flow (out of scope for auto code). Use CSV export for now.")
