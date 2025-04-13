from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Configuration class to hold environment variables."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")