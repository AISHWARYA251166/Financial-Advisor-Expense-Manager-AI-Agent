import google.generativeai as genai
import json
import re

class GeminiAdvice:
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        if not api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    # ---------------------------------------------------------
    # INR CURRENCY NORMALISER
    # ---------------------------------------------------------
    def normalize_currency(self, text: str):
        """
        Detects plain numbers like 10000 → converts to ₹10,000
        """

        def repl(match):
            try:
                num = float(match.group(0))
                return f"₹{num:,.0f}"
            except:
                return match.group(0)

        return re.sub(r"\b\d{3,}\b", repl, text)

    # ---------------------------------------------------------
    # MAIN ADVICE GENERATOR
    # ---------------------------------------------------------
    def generate_advice(self, expenses, budget, philosophy):
        total = sum(e.get("amount", 0) for e in expenses)

        breakdown = {}
        for e in expenses:
            cat = e.get("category", "other")
            breakdown[cat] = breakdown.get(cat, 0) + e.get("amount", 0)

        # -----------------------------
        # India-specific financial prompt
        # -----------------------------
        prompt = f"""
You are an experienced **Indian financial advisor**.

Analyze the user's spending and provide:

### 1️⃣ Spending Summary  
Short 2–3 sentence overview.

### 2️⃣ Budget Compliance  
Identify where the user is over-spending or under-spending.

### 3️⃣ Indian-Specific Actionable Recommendations  
Include references to  
- **PPF**  
- **SIP (Mutual Funds)**  
- **ELSS (Tax Saving)**  
- **NPS**  
- **Emergency Fund**  
when relevant.

### 4️⃣ One Investment Idea  
Suggest a simple SIP or tax-saving instrument based on their risk profile.

---

### User Data:
- **Total Spent:** ₹{total}
- **Budget:** ₹{budget}
- **Financial Philosophy:** {philosophy}

### Category Breakdown:
{json.dumps(breakdown, indent=2)}

Write a clear, structured response in **beautiful markdown**.
"""

        response = self.model.generate_content(prompt)
        output = response.text or ""

        # Normalize currency like: 25000 → ₹25,000
        output = self.normalize_currency(output)

        return output
