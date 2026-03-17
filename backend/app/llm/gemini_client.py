import google.generativeai as genai

from app.config import settings
from app.llm.model_router import model_router


genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiClient:

    def generate(self, prompt, task=""):

        model_name = model_router.select_model(task)

        model = genai.GenerativeModel(model_name)

        response = model.generate_content(prompt)

        return response.text

    def generate_json(self, prompt, task=""):
        """Use Gemini's instruction following to get clean JSON."""
        model_name = model_router.select_model(task)
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(prompt)
        return response.text


gemini_client = GeminiClient()