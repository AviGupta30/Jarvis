"""
voice.py — Jarvis Voice Engine
------------------------------
STT:  faster-whisper (local, CPU, int8 — zero network latency, zero API cost)
      Falls back to Groq Whisper API automatically if local model fails.
TTS:  ElevenLabs Multilingual v2 (PRIMARY — best Hinglish quality)
      Falls back to edge-tts + pygame if ElevenLabs is unavailable.

Why faster-whisper instead of whisper.cpp binary:
  - Pure Python + pip install — no C++ compilation needed
  - Same CTranslate2 engine as whisper.cpp — identical speed on CPU
  - int8 compute_type = 4x less RAM, 2x faster than float32
  - On your i9 (20 threads): ~tiny=0.1s, ~small=0.3s, ~base=0.2s per clip
  - 100% offline — no API key, no network, no rate limit

Model selection:
  WHISPER_MODEL = "base"   → best balance of speed + accuracy for short commands
  WHISPER_MODEL = "small"  → slightly better accuracy, ~0.3s on i9
  WHISPER_MODEL = "tiny"   → fastest (~0.1s), slightly lower accuracy

The model is loaded ONCE at module import and kept in RAM.
First transcription may take ~0.5s to warm up; subsequent ones are instant.
"""

import os
import re
import asyncio
import tempfile
import threading
import logging
import pygame
import edge_tts
from groq import AsyncGroq
from app.core.config import settings
from app.services.hinglish_normalizer import normalize_for_tts
from app.services.ssml_processor import strip_ssml

# Suppress HuggingFace symlink warning on Windows (cosmetic only — no effect on function)
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
# Use HF token for faster model downloads (authenticated = higher rate limits)
if settings.HF_API_KEY:
    os.environ.setdefault("HF_TOKEN", settings.HF_API_KEY)

logger = logging.getLogger(__name__)


# ── Groq fallback client (only used if local STT fails) ──────────────────────
_groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── TTS config ────────────────────────────────────────────────────────────────
# Kokoro ONNX  — English TTS  (local, free, unlimited, ~85MB model)
# edge-tts EN  — English fallback (Microsoft Christopher Neural)
# edge-tts HI  — Hindi TTS    (Microsoft Madhur Neural — native Hindi speaker)
EDGE_TTS_VOICE_EN = "en-US-ChristopherNeural"   # English fallback
EDGE_TTS_VOICE_HI = "hi-IN-MadhurNeural"         # Native Hindi — perfect pronunciation
KOKORO_VOICE      = "am_adam"                     # American Male Adam — close to movie Jarvis
KOKORO_SPEED      = 1.0

# Kokoro model paths (downloaded once by scripts/download_kokoro.py)
_KOKORO_DIR    = os.path.join(os.path.dirname(__file__), "..", "..", "models", "kokoro")
KOKORO_MODEL   = os.path.join(_KOKORO_DIR, "kokoro-v1.0.int8.onnx")
KOKORO_VOICES  = os.path.join(_KOKORO_DIR, "voices-v1.0.bin")

# Lazy-loaded Kokoro singleton — loaded once, kept in RAM
_kokoro_engine  = None
_kokoro_lock    = threading.Lock()
_kokoro_ready   = False

# ── Local Whisper config ──────────────────────────────────────────────────────
# "base" is the sweet spot: ~0.2s on i9, accurate enough for commands
# Change to "small" for better accuracy on longer sentences
WHISPER_MODEL    = "base"
WHISPER_DEVICE   = "cpu"
WHISPER_COMPUTE  = "int8"    # 4x less RAM than float32, 2x faster on CPU

# Lazy-loaded model singleton — loaded once, stays in RAM
_whisper_model   = None
_whisper_lock    = threading.Lock()
_whisper_ready   = False


def _load_whisper_model():
    """
    Load the faster-whisper model into RAM.
    Called once at startup in a background thread so server boots instantly.
    Thread-safe via _whisper_lock.
    """
    global _whisper_model, _whisper_ready
    with _whisper_lock:
        if _whisper_ready:
            return
        try:
            from faster_whisper import WhisperModel
            logger.info(f"[STT] Loading local Whisper '{WHISPER_MODEL}' model...")
            _whisper_model = WhisperModel(
                WHISPER_MODEL,
                device=WHISPER_DEVICE,
                compute_type=WHISPER_COMPUTE,
                cpu_threads=8,          # Use 8 of your i9's 20 threads for STT
                num_workers=2,          # 2 parallel decode workers
                download_root=os.path.join(os.path.dirname(__file__), "..", "..", "models"),
            )
            _whisper_ready = True
            logger.info(f"[STT] ✅ Local Whisper '{WHISPER_MODEL}' loaded. Zero-latency STT active.")
        except Exception as e:
            logger.warning(f"[STT] Local Whisper load failed: {e}. Will fall back to Groq API.")
            _whisper_ready = False


# Start loading the model in a background thread immediately at module import
# This means by the time the user first speaks, the model is already warm
threading.Thread(target=_load_whisper_model, daemon=True, name="whisper-loader").start()


# ── Hallucination filter (shared by both local and cloud STT) ────────────────
_HALLUCINATIONS = {
    "i understand", "okay", "thank you", "you", "thanks",
    "i'm sorry", "bye", "transcribe in english", "tanscribe in english",
    "the user may speak english or hinglish", "the wake word is jarvis",
    "do not transcribe silence", "silence", "...", ". . .",
    "thank you for watching", "please subscribe", "subtitles by",
    "like and subscribe", "see you next time", "увидимся!", "amém",
    "you can find me on twitter", "follow me on instagram",
    "thank you for listening",
}

def _filter_hallucinations(text: str) -> str:
    """Return empty string if text is a known Whisper hallucination."""
    cleaned = text.lower().strip('.!?,')
    if cleaned in _HALLUCINATIONS:
        return ""
    # Also filter very short noise artifacts
    if len(cleaned) < 2:
        return ""
    return text


# ── Local STT (faster-whisper) ────────────────────────────────────────────────

def _transcribe_local(file_path: str) -> str:
    """
    Transcribe audio using the local faster-whisper model.
    Runs synchronously (called from thread pool via asyncio.run_in_executor).

    Returns transcribed text, or empty string on failure / no speech.
    """
    if not _whisper_ready or _whisper_model is None:
        raise RuntimeError("Local Whisper model not ready")

    # Skip tiny files (< 4KB ≈ less than 0.25 seconds of audio)
    try:
        if os.path.getsize(file_path) < 4096:
            return ""
    except Exception:
        return ""

    segments, info = _whisper_model.transcribe(
        file_path,
        language="en",
        beam_size=3,                # Faster than default beam_size=5
        best_of=3,
        temperature=0.0,
        vad_filter=True,            # Voice Activity Detection — skip silence automatically
        vad_parameters={
            "min_silence_duration_ms": 300,
            "threshold": 0.5,
        },
        initial_prompt=(
            "The user is speaking to Jarvis, an AI assistant. "
            "They may speak English or Hinglish. Transcribe accurately."
        ),
        condition_on_previous_text=False,   # Prevents hallucination loops
        no_speech_threshold=0.6,            # Discard segments with high no-speech probability
        log_prob_threshold=-1.0,            # Discard low-confidence segments
    )

    # Collect all segments
    text_parts = []
    for segment in segments:
        if segment.no_speech_prob < 0.6:    # Only keep high-confidence speech
            text_parts.append(segment.text.strip())

    full_text = " ".join(text_parts).strip()
    return _filter_hallucinations(full_text)


# ── Cloud STT fallback (Groq Whisper API) ────────────────────────────────────

async def _transcribe_groq(file_path: str) -> str:
    """
    Fallback: Groq Whisper large-v3 API.
    Only called when local model is unavailable or fails.
    """
    try:
        with open(file_path, "rb") as f:
            audio_data = f.read()
        if len(audio_data) < 4096:
            return ""

        transcription = await _groq_client.audio.transcriptions.create(
            file=(os.path.basename(file_path), audio_data),
            model="whisper-large-v3",
            language="en",
            temperature=0.0,
            prompt="The user may speak English or Hinglish. The wake word is Jarvis. Transcribe in English.",
        )
        return _filter_hallucinations(transcription.text.strip())
    except Exception as e:
        err = str(e).lower()
        if any(k in err for k in ["no audio", "audio", "empty", "short", "silent"]):
            return ""
        raise


# ── Public API: transcribe_audio ──────────────────────────────────────────────

async def transcribe_audio(file_path: str) -> str:
    """
    PRIMARY entry point for all STT in Jarvis.
    
    Routing:
      1. Local faster-whisper (0.1–0.3s, offline, zero cost)  ← PRIMARY
      2. Groq Whisper API (cloud fallback if local fails)

    The Jarvis brain (LLM routing, tools, planner) is UNCHANGED.
    Only the STT layer is upgraded — everything above this function
    sees the same transcribed string it always did.

    Returns empty string on failure (too-short audio, no speech, etc.)
    The caller (safe_transcribe in chat.py) handles timeouts.
    """
    # Try local first
    if _whisper_ready and _whisper_model is not None:
        try:
            loop = asyncio.get_event_loop()
            # Run in thread pool — faster-whisper is CPU-bound, not async
            text = await loop.run_in_executor(None, _transcribe_local, file_path)
            if text:
                logger.debug(f"[STT] Local: '{text[:60]}'")
            return text
        except Exception as e:
            logger.warning(f"[STT] Local transcription failed, falling back to Groq: {e}")

    # Fallback: Groq API
    try:
        text = await _transcribe_groq(file_path)
        if text:
            logger.debug(f"[STT] Groq fallback: '{text[:60]}'")
        return text
    except Exception as e:
        err = str(e).lower()
        if any(k in err for k in ["no audio", "audio", "empty", "short", "silent"]):
            return ""
        raise


# ── TTS Engine ────────────────────────────────────────────────────────────────

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()


def _load_kokoro() -> bool:
    """
    Load the Kokoro ONNX model into RAM.
    Thread-safe. Called once at startup.
    Returns True on success, False if model files not yet downloaded.
    """
    global _kokoro_engine, _kokoro_ready
    with _kokoro_lock:
        if _kokoro_ready:
            return True
        model_path  = os.path.abspath(KOKORO_MODEL)
        voices_path = os.path.abspath(KOKORO_VOICES)
        if not os.path.exists(model_path) or not os.path.exists(voices_path):
            logger.warning(
                "[TTS] Kokoro model files not found. "
                "Run: python scripts/download_kokoro.py"
            )
            return False
        try:
            from kokoro_onnx import Kokoro
            logger.info("[TTS] Loading Kokoro ONNX model...")
            _kokoro_engine = Kokoro(model_path, voices_path)
            _kokoro_ready  = True
            logger.info("[TTS] Kokoro TTS ready. Primary voice: " + KOKORO_VOICE)
            return True
        except Exception as e:
            logger.warning(f"[TTS] Kokoro load failed: {e}")
            return False


# Pre-load Kokoro in background so first speak is instant
threading.Thread(target=_load_kokoro, daemon=True, name="kokoro-loader").start()


def _kokoro_speak_sync(text: str) -> bool:
    """
    Synchronous Kokoro TTS playback — runs in thread pool.
    Returns True on success.
    """
    if not _kokoro_ready or _kokoro_engine is None:
        return False
    try:
        import sounddevice as _sd
        samples, sample_rate = _kokoro_engine.create(
            text,
            voice=KOKORO_VOICE,
            speed=KOKORO_SPEED,
            lang="en-us",
        )
        _sd.play(samples, sample_rate)
        _sd.wait()
        return True
    except Exception as e:
        logger.warning(f"[TTS] Kokoro playback failed: {e}. Falling back to edge-tts.")
        return False


async def _tts_kokoro(text: str) -> bool:
    """
    Speak via Kokoro ONNX (PRIMARY — local, free, unlimited).
    Returns True on success, False to trigger fallback.
    """
    if not _kokoro_ready:
        return False
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _kokoro_speak_sync, text)


async def _tts_edge(text: str, voice: str | None = None):
    """Speak via edge-tts + pygame. Uses the specified voice, defaults to English."""
    text = text.strip()
    if not text or len(text) < 2:
        return

    selected_voice = voice or EDGE_TTS_VOICE_EN

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name

    try:
        communicate = edge_tts.Communicate(text, selected_voice)
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


async def _tts_play(text: str):
    """
    Language-adaptive TTS pipeline:
      - English text  → Kokoro am_adam (local, clear English accent)
      - Hindi/Hinglish → edge-tts hi-IN-MadhurNeural (native Hindi voice, perfect pronunciation)
      - English fallback (if Kokoro fails) → edge-tts en-US-ChristopherNeural
    """
    text = text.strip()
    if not text or len(text) < 2:
        return

    # Step 1: Normalize (Devanagari → Roman, strip markdown)
    plain_text = normalize_for_tts(text)
    plain_text = strip_ssml(plain_text)
    if not plain_text.strip():
        return

    # Step 2: Detect language of this specific text chunk
    from app.services.context_classifier import detect_language
    lang = detect_language(plain_text)

    # Step 3: Route to the right TTS engine
    if lang in ('hindi', 'hinglish'):
        # Native Hindi Microsoft voice — perfect pronunciation
        await _tts_edge(plain_text, voice=EDGE_TTS_VOICE_HI)
    else:
        # English — try Kokoro first (local), fall back to edge-tts English
        success = await _tts_kokoro(plain_text)
        if not success:
            await _tts_edge(plain_text, voice=EDGE_TTS_VOICE_EN)


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
    Accepts an async generator of text chunks.
    Buffers until a sentence is complete, then speaks it immediately.
    First sentence plays while the LLM is still generating the rest.
    """
    buffer    = ""
    MIN_CHARS = 25

    async for chunk in text_generator:
        if not chunk:
            continue
        buffer += chunk

        if len(buffer) >= MIN_CHARS:
            match = re.search(r'^(.*[.!?।])\s+(.*)', buffer, re.DOTALL)
            if match:
                to_speak = match.group(1).strip()
                buffer   = match.group(2).strip()
                if to_speak and len(to_speak) > 3:
                    await _tts_play(to_speak)

    if buffer.strip() and len(buffer.strip()) > 2:
        await _tts_play(buffer.strip())
