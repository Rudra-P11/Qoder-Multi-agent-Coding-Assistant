import google.generativeai as genai

from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiClient:

    def __init__(self):

        self.model = genai.GenerativeModel(
            settings.MODEL_FLASH
        )

    def generate(self, prompt: str):

        response = self.model.generate_content(prompt)

        return response.text


gemini_client = GeminiClient()