import os
import re
import asyncio
import tempfile
import pygame
import edge_tts
from groq import AsyncGroq
from app.core.config import settings

# No timeout in constructor — we handle timeouts in the caller (safe_transcribe)
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# Single consistent male voice
VOICE = "en-US-ChristopherNeural"

# Initialize pygame mixer ONCE at module level
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()


async def transcribe_audio(file_path: str) -> str:
    """
    Uses Groq Whisper to transcribe audio with auto language detection.
    Returns empty string on failure (too-short audio, no speech detected, etc.)
    This function itself has NO timeout — the caller (safe_transcribe) handles that.
    """
    try:
        with open(file_path, "rb") as file:
            audio_data = file.read()

        # Don't bother sending tiny files (< 4KB = less than ~0.25 seconds)
        if len(audio_data) < 4096:
            return ""

        transcription = await client.audio.transcriptions.create(
            file=(os.path.basename(file_path), audio_data),
            model="whisper-large-v3",
            language="en",
            temperature=0.0,
            prompt="The user may speak English or Hinglish. The wake word is Jarvis. Transcribe in English.",
        )
        text = transcription.text.strip()

        # Filter out Whisper hallucinations (common false positives on silence/noise)
        hallucinations = {
            "i understand", "okay", "thank you", "you", "thanks",
            "i'm sorry", "bye", "transcribe in english", "tanscribe in english",
            "the user may speak english or hinglish", "the wake word is jarvis",
            "do not transcribe silence", "silence", "...", ". . .",
            "thank you for watching", "please subscribe", "subtitles by",
            "like and subscribe", "see you next time", "увидимся!", "amém",
        }
        if text.lower().strip('.!?,') in hallucinations:
            return ""

        return text

    except Exception as e:
        err = str(e).lower()
        # Silently discard audio-quality errors (too short, no speech, etc.)
        if any(k in err for k in ["no audio", "audio", "empty", "short", "silent"]):
            return ""
        # Re-raise so safe_transcribe can handle it
        raise


async def _tts_play(text: str):
    """Generates and plays a single TTS chunk via edge-tts + pygame."""
    text = text.strip()
    if not text or len(text) < 2:
        return

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name

    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.03)
        pygame.mixer.music.unload()
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


async def speak_text(text: str):
    """Speaks a full text response — splits into sentences for faster first word."""
    if not text or not text.strip():
        return
    sentences = re.split(r'(?<=[.!?।])\s+', text.strip())
    for sentence in sentences:
        if sentence.strip():
            await _tts_play(sentence)


async def speak_stream(text_generator):
    """
    Accepts an async generator of text chunks (sentences or words).
    Buffers until a sentence is complete, then speaks it immediately.
    Gives the fastest perceived response — first sentence plays while
    the LLM is still generating the rest.
    """
    buffer = ""
    MIN_CHARS = 25  # Minimum chars before we attempt TTS

    async for chunk in text_generator:
        if not chunk:
            continue
        buffer += chunk

        # Only try to split when we have enough content
        if len(buffer) >= MIN_CHARS:
            match = re.search(r'^(.*[.!?।])\s+(.*)', buffer, re.DOTALL)
            if match:
                to_speak = match.group(1).strip()
                buffer = match.group(2).strip()
                if to_speak and len(to_speak) > 3:
                    await _tts_play(to_speak)

    # Speak any remaining text
    if buffer.strip() and len(buffer.strip()) > 2:
        await _tts_play(buffer.strip())
