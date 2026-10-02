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
    # Groq model for image inputs — gpt-oss models are text-only and reject image_url content
    GROQ_VISION_MODEL:    str = os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b")
    # Backend base URL used by standalone clients (voice agent, prompt overlay)
    JARVIS_API_URL:       str = os.getenv("JARVIS_API_URL", "http://127.0.0.1:8000")
    # Voice (scripts/voice_agent.py + app/services/voice.py). See docs/features/voice.md
    JARVIS_VOICE_EN:      str = os.getenv("JARVIS_VOICE_EN", "en-GB-RyanNeural")     # British, movie-Jarvis-like
    JARVIS_VOICE_HI:      str = os.getenv("JARVIS_VOICE_HI", "hi-IN-MadhurNeural")   # native Hindi male
    JARVIS_VOICE_RATE_EN: str = os.getenv("JARVIS_VOICE_RATE_EN", "+4%")
    JARVIS_VOICE_RATE_HI: str = os.getenv("JARVIS_VOICE_RATE_HI", "+8%")
    JARVIS_STT_MODEL:     str = os.getenv("JARVIS_STT_MODEL", "whisper-large-v3-turbo")  # Groq
    JARVIS_STT_LOCAL:     str = os.getenv("JARVIS_STT_LOCAL", "base")   # faster-whisper fallback
    JARVIS_STT_MODE:      str = os.getenv("JARVIS_STT_MODE", "auto")    # auto | groq | local
    # Long-term RAG Memory — MySQL backend (local, never pauses unlike Supabase)
    MYSQL_URL:            str = os.getenv("MYSQL_URL", "mysql+aiomysql://root:@localhost/jarvis_memory")

settings = Settings()
