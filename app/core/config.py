import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY:         str = os.getenv("GROQ_API_KEY", "")
    HF_API_KEY:           str = os.getenv("HF_API_KEY", "")
    DATABASE_URL:         str = os.getenv("DATABASE_URL", "")
    GEMINI_API_KEY:       str = os.getenv("GEMINI_API_KEY", "")
    ELEVENLABS_API_KEY:   str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID:  str = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Default: Adam
    GPTZERO_API_KEY:      str = os.getenv("GPTZERO_API_KEY", "")

settings = Settings()
