# Financial Advisor AI - Gemini-only Professional Version
This project is a Streamlit app that uses Google Gemini Vision for receipt/screenshot extraction and Gemini LLM for financial advice.

Features:
- Gemini-only OCR & structured JSON extraction from screenshots
- Expense manager with CSV upload and manual entry
- Dashboard and Analytics (Plotly)
- Gemini-only advice generator (no OpenAI)
- Centralized Gemini API key management via Streamlit session_state

Quick start:
1. Install dependencies: pip install -r requirements.txt
2. Install Tesseract is NOT required (Gemini Vision used)
3. Run: streamlit run main.py
4. Enter your Gemini API key in the sidebar (get from https://aistudio.google.com/app/apikey)
