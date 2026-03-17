import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    APP_NAME = "Qoder Agentic System"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    MODEL_FLASH = "gemini-1.5-flash"
    MODEL_PRO = "gemini-1.5-pro"

    MAX_RETRIES = 3

    LOG_LEVEL = "INFO"

settings = Settings()