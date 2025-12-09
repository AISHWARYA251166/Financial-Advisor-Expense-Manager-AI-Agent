import google.generativeai as genai
from PIL import Image

class GeminiService:
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        if not api_key:
            raise ValueError('Gemini API key required')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_expense(self, pil_image: Image.Image):
        if not isinstance(pil_image, Image.Image):
            raise TypeError('extract_expense expects a PIL.Image.Image')

        prompt = '''Extract ONLY a JSON object with fields:
        {"amount": number, "merchant": string, "category": "food|transport|entertainment|shopping|utilities|other", "date": "YYYY-MM-DD", "paymentMethod": string}
        If any field cannot be found, provide a reasonable default (date -> today, paymentMethod -> "UPI", category -> "other").
        Return ONLY the JSON object.'''

        response = self.model.generate_content([prompt, pil_image])
        return response.text
    
    
