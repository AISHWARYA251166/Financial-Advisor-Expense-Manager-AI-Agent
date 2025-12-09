# services/toolbox.py
from services.gemini_service import GeminiService
from PIL import Image
from typing import Dict, Any, List
import pandas as pd
from core.json_parser import extract_json_from_text
import re


# -----------------------------------------
# UPI Extraction Helper (GLOBAL FUNCTION)
# -----------------------------------------
def extract_upi_info(raw_text: str) -> Dict[str, str]:
    """
    Extract Indian UPI-specific info:
    - UPI ID (xyz@okicici)
    - UTR (12-digit number)
    """
    upi_id = None
    utr = None

    upi_match = re.search(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]+", raw_text)
    if upi_match:
        upi_id = upi_match.group(0)

    utr_match = re.search(r"\b\d{12}\b", raw_text)
    if utr_match:
        utr = utr_match.group(0)

    return {"upi_id": upi_id, "utr": utr}


# -----------------------------------------
# Tools Class
# -----------------------------------------
class Tools:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key required for Tools")
        self.gem = GeminiService(api_key)

    # -----------------------------------------------------
    # Image Expense Extraction (Gemini Vision)
    # -----------------------------------------------------
    def extract_expense_from_image(self, pil_image: Image.Image) -> Dict[str, Any]:
        raw_response = self.gem.extract_expense(pil_image)

        # Parse JSON from Gemini response
        parsed = extract_json_from_text(raw_response)

        # Extract UPI info
        upi_info = extract_upi_info(raw_response)

        # If parsing failed, use fallback
        if not parsed:
            prompt = (
                "Return ONLY a JSON object with fields: "
                "amount:number, merchant:string, category:string "
                "(one of food,transport,entertainment,shopping,utilities,investment,other), "
                "date:YYYY-MM-DD, paymentMethod:string"
            )
            resp = self.gem.model.generate_content([prompt, pil_image])
            parsed = extract_json_from_text(resp.text)

        if not parsed:
            raise ValueError("Could not parse expense from image")

        # Normalize values
        parsed['amount'] = float(parsed.get('amount', 0) or 0)
        parsed['category'] = (parsed.get('category') or 'other').lower()

        # Add UPI extracted values
        parsed["upi_id"] = upi_info.get("upi_id")
        parsed["utr"] = upi_info.get("utr")

        return parsed

    # -----------------------------------------------------
    # CSV Expense Extraction
    # -----------------------------------------------------
    def parse_expenses_csv(self, file_like) -> List[Dict[str, Any]]:
        df = pd.read_csv(file_like)
        rows = []

        for _, r in df.iterrows():
            amt = r.get('amount') if 'amount' in r else r.get('Amount', 0)

            try:
                amt = float(amt or 0)
            except Exception:
                amt = 0.0

            rows.append({
                'amount': amt,
                'merchant': r.get('merchant') or r.get('Merchant') or "Unknown",
                'category': (r.get('category') or r.get('Category') or "other").lower(),
                'date': str(r.get('date') or r.get('Date') or ""),
                'paymentMethod': r.get('paymentMethod') or r.get('PaymentMethod') or "CSV"
            })

        return rows
