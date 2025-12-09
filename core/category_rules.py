# core/category_rules.py

import re

INDIAN_KEYWORDS = {
    "food": ["swiggy", "zomato", "restaurant", "hotel", "food", "eatery"],
    "transport": ["ola", "uber", "rapido", "fuel", "petrol", "diesel", "metro", "bus"],
    "entertainment": ["netflix", "hotstar", "spotify", "bookmyshow", "movies", "gaming"],
    "shopping": ["amazon", "flipkart", "myntra", "ajio", "shopping", "big bazaar"],
    "utilities": ["electricity", "water bill", "gas bill", "broadband", "wifi", "mobile recharge"],
    "investment": ["mutual fund", "sip", "lumpsum", "stocks", "ppf", "nps", "elss", "epf"],
    "other": []
}

def categorize_text(text: str) -> str:
    text = text.lower() if text else ""

    for category, keywords in INDIAN_KEYWORDS.items():
        if any(k in text for k in keywords):
            return category

    return "other"
