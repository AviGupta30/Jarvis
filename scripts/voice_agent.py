import os
import sys
import struct
import wave
import pyaudio
import asyncio
import httpx
import re
import time
import math
import json
import subprocess
import random

# ── Shared UI state file (read by jarvis_overlay.py) ────────────────────────
_UI_STATE_FILE = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'jarvis_ui_state.json')

def set_ui_state(state: str):
    """Write Jarvis UI state so the overlay can animate accordingly."""
    try:
        with open(_UI_STATE_FILE, 'w') as f:
            json.dump({'state': state, 'ts': time.time()}, f)
    except Exception:
        pass

# Timing constants
SILENCE_LIMIT = 1.5      # Stop recording 1.5s after speech ends
MAX_RECORD_TIME = 8.0    # Max recording time
CHUNK = 512
RATE = 16000
SILENCE_THRESHOLD = 500  # Dynamically calibrated at startup

def get_rms(data):
    count = len(data) // 2
    if count == 0:
        return 0
    shorts = struct.unpack(f"{count}h", data)
    sum_squares = sum(s * s for s in shorts)
    return math.sqrt(sum_squares / count)


def calibrate_noise(audio_stream, sample_seconds: float = 1.5) -> float:
    print("🎤 Calibrating ambient noise level...")
    samples = []
    num_chunks = int(RATE / CHUNK * sample_seconds)
    for _ in range(num_chunks):
        data = audio_stream.read(CHUNK, exception_on_overflow=False)
        samples.append(get_rms(data))
    avg_noise = sum(samples) / len(samples) if samples else 300
    threshold = max(avg_noise * 2.5, 300)
    print(f"✅ Noise floor: {avg_noise:.0f} → Trigger threshold set to {threshold:.0f}")
    return threshold


# Known wake word forms (English + Devanagari + common Whisper mishearings)
WAKE_WORDS = [
    "jarvis", "जारविस", "जार्विस",
    "jarwis", "jaarvis", "jarbus", "jarvas", "jarves",
    "jarbis", "jarbi", "harvey", "j.a.r.v.i.s",
    "hey jarvis", "javis", "jarvice",
]

WAKE_PREFIXES = ["hey", "ok", "okay", "hi", "yo", "aye"]


def _fuzzy_contains_wake_word(text: str) -> tuple[bool, str]:
    import difflib
    words = text.split()
    for i, word in enumerate(words):
        cleaned = re.sub(r'[^a-z]', '', word.lower())
        if not cleaned:
            continue
        for ww in WAKE_WORDS:
            ww_clean = re.sub(r'[^a-z]', '', ww.lower())
            if not ww_clean:
                continue
            ratio = difflib.SequenceMatcher(None, cleaned, ww_clean).ratio()
            if ratio >= 0.72 or cleaned == ww_clean:
                remaining = ' '.join(words[i+1:]).strip()
                remaining = re.sub(r'^[,!?.।\s]+', '', remaining).strip()
                return True, remaining
    for ww in ["जारविस", "जार्विस"]:
        if ww in text:
            idx = text.index(ww)
            remaining = text[idx + len(ww):].strip().lstrip(',!?. ')
            return True, remaining
    return False, ""


def extract_wake_word_command(text: str) -> str | None:
    found, command = _fuzzy_contains_wake_word(text)
    if found:
        return command
    return None


# ── Ensure we can import the app module ─────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.voice import transcribe_audio, speak_text, speak_stream
from app.services.whatsapp import open_whatsapp, send_whatsapp_message
from app.services.hinglish_normalizer import normalize_for_tts

# ── Acoustic Tripwire (double-clap wake) ─────────────────────────────────────
try:
    from app.services.acoustic_tripwire import get_engine as _get_tripwire_engine
    _TRIPWIRE_AVAILABLE = True
except Exception as _tw_err:
    print(f"[Tripwire] Could not load acoustic engine (non-fatal): {_tw_err}")
    _TRIPWIRE_AVAILABLE = False

# Import planner classifier at module level (not inside the hot loop)
try:
    from app.services.planner import is_complex_task as _is_complex_task
except Exception:
    def _is_complex_task(cmd): return False

# (PIN removed — WhatsApp now uses two-phase confirmation instead)




def clean_markdown(text: str) -> str:
    """Strip markdown and Devanagari before text reaches TTS."""
    # Use the hinglish normalizer — it handles Devanagari + markdown in one pass
    return normalize_for_tts(text)


async def record_audio(audio_stream, pa) -> str | None:
    """Records audio from the stream until silence, saves to temp file, returns path."""
    frames = []
    start_time = time.time()
    silence_start = None

    # Flush stale buffer
    audio_stream.read(audio_stream.get_read_available(), exception_on_overflow=False)

    while True:
        data = audio_stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

        current_time = time.time()
        elapsed = current_time - start_time
        current_rms = get_rms(data)

        if current_rms < SILENCE_THRESHOLD:
            if silence_start is None:
                silence_start = current_time
            elif current_time - silence_start > SILENCE_LIMIT:
                break
        else:
            silence_start = None

        if elapsed > MAX_RECORD_TIME:
            break

    # Minimum recording: 0.8 seconds of audio — anything shorter is TTS echo or noise
    MIN_FRAMES = int(RATE / CHUNK * 0.8)
    if len(frames) < MIN_FRAMES:
        return None

    temp_audio = "temp_command.wav"
    with wave.open(temp_audio, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return temp_audio


# ── Agentic tag detection ─────────────────────────────────────────────────────
_AGENTIC_TAGS = ("[STEP", "[PLAN]", "[DONE]", "[REPLAN]", "[SUMMARY]", "[RESULT]")

def _is_agentic_line(text: str) -> bool:
    return any(text.startswith(tag) for tag in _AGENTIC_TAGS)

def _clean_agentic_line(text: str) -> str:
    """Convert an agentic tag line into natural spoken text."""
    # [STEP 1] Description → "Step 1: Description"
    text = re.sub(r'^\[STEP (\d+)[^\]]*\]\s*', r'Step \1. ', text)
    # [STEP 1 ✓] result → "Step 1 done. result"
    text = re.sub(r'^\[STEP (\d+) ✓\]\s*', r'Step \1 done. ', text)
    # [STEP 1 ✗] error → "Step \1 failed. error"
    text = re.sub(r'^\[STEP (\d+) ✗\]\s*', r'Step \1 encountered an issue. ', text)
    text = text.replace("[PLAN] ", "")
    text = text.replace("[DONE] ", "All done. ")
    text = text.replace("[REPLAN] ", "Adjusting the plan. ")
    text = text.replace("[SUMMARY] ", "")
    text = text.replace("[RESULT] ", "")
    return text.strip()


async def send_command_streaming(http_client: httpx.AsyncClient, command: str) -> str:
    """
    Streams the backend response and speaks it sentence-by-sentence.

    Handles two response modes:
    - Regular streaming (simple commands): tokens arrive continuously, buffer into sentences
    - Agentic plan updates: lines starting with [STEP N], [PLAN], etc. — speak each immediately
    """
    full_response = ""
    sentence_buffer = ""

    async def smart_text_generator():
        nonlocal full_response, sentence_buffer

        try:
            async with http_client.stream(
                "POST",
                "http://127.0.0.1:8000/chat",
                json={"prompt": command},
                timeout=180.0,   # 3 minutes for complex agentic tasks
            ) as response:
                async for chunk in response.aiter_text():
                    if not chunk:
                        continue

                    # Strip SSE prefix if present
                    chunk = chunk.replace("data: ", "")
                    full_response += chunk

                    # Check if this chunk contains an agentic update tag
                    # Agentic lines come in complete: "[STEP 1] Opening the PDF\n"
                    if "\n" in chunk:
                        # Split on newlines, process each line
                        parts = chunk.split("\n")
                        for part in parts:
                            part = part.strip()
                            if not part:
                                continue
                            if _is_agentic_line(part):
                                # Flush any pending sentence buffer first
                                if sentence_buffer.strip():
                                    yield sentence_buffer.strip()
                                    sentence_buffer = ""
                                spoken = _clean_agentic_line(part)
                                if spoken:
                                    yield spoken
                            else:
                                sentence_buffer += part + " "
                                # Try to extract a complete sentence
                                while True:
                                    found = -1
                                    for sep in ('.', '!', '?', '।'):
                                        idx = sentence_buffer.find(sep)
                                        if idx != -1 and (found == -1 or idx < found):
                                            found = idx
                                    if found != -1:
                                        sentence = sentence_buffer[:found+1].strip()
                                        sentence_buffer = sentence_buffer[found+1:].strip()
                                        if sentence and len(sentence) > 5:
                                            yield sentence
                                    else:
                                        break
                    else:
                        # Regular token chunk — accumulate and sentence-split
                        sentence_buffer += chunk
                        while True:
                            found = -1
                            for sep in ('.', '!', '?', '।'):
                                idx = sentence_buffer.find(sep)
                                if idx != -1 and (found == -1 or idx < found):
                                    found = idx
                            if found != -1 and len(sentence_buffer[:found+1].strip()) > 5:
                                sentence = sentence_buffer[:found+1].strip()
                                sentence_buffer = sentence_buffer[found+1:].strip()
                                yield sentence
                            else:
                                break

        except httpx.ConnectError:
            msg = "I can't reach my backend server. Please make sure the Jarvis server is running."
            print(f"[Backend Error] ConnectError")
            yield msg
        except Exception as e:
            msg = f"Backend error: {str(e)[:80]}"
            print(f"[Backend Error] {e}")
            yield msg

        # Yield any remaining buffer
        if sentence_buffer.strip() and len(sentence_buffer.strip()) > 2:
            yield sentence_buffer.strip()

    print("🔊 Speaking...")
    set_ui_state("speaking")
    await speak_stream(smart_text_generator())
    set_ui_state("idle")
    print()
    return full_response


async def safe_transcribe(audio_path: str) -> str:
    """
    Transcribes audio with a 20-second timeout. Returns empty string on failure.
    """
    try:
        result = await asyncio.wait_for(
            transcribe_audio(audio_path),
            timeout=20.0
        )
        return result
    except asyncio.TimeoutError:
        print("⏳ Transcription timed out (>20s) — skipping.")
        return ""
    except Exception as e:
        err_str = str(e)
        if any(k in err_str.lower() for k in ["audio", "no speech", "empty", "short"]):
            return ""
        print(f"❌ Transcription error: {type(e).__name__}: {err_str[:80]}")
        return ""


async def run_voice_agent():
    pa = None
    audio_stream = None

    # Follow-up state
    awaiting_followup = False

    # ── Acoustic Tripwire (inline mode — shares voice_agent's mic stream) ────
    # IMPORTANT: We do NOT call engine.start() here. That would open a second
    # PyAudio stream at 44100 Hz while voice_agent already owns the mic at
    # 16000 Hz. On Windows, dual exclusive streams at different sample rates
    # corrupt each other — causing garbled transcriptions and failed detection.
    # Instead, process_chunk() is called inline on every audio frame we read.
    _tripwire = None
    if _TRIPWIRE_AVAILABLE:
        try:
            _tripwire = _get_tripwire_engine()
            _tripwire.enable()   # arm it (no background thread started)
        except Exception as _e:
            print(f"[Tripwire] Engine init failed (non-fatal): {_e}")
            _tripwire = None

    try:
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=CHUNK
        )

        # ── Calibrate ambient noise at startup ──────────────────────────────
        global SILENCE_THRESHOLD
        SILENCE_THRESHOLD = calibrate_noise(audio_stream)

        # ── Wire tripwire threshold to calibrated noise floor ──────────────
        # Claps are ~3× louder than speech, so set a much stricter gate to
        # avoid speech or ambient noise triggering a false wake.
        if _tripwire is not None:
            _tw_thresh = max(SILENCE_THRESHOLD * 3.0, 2000.0)
            _tripwire.set_volume_threshold(_tw_thresh)
            print(f"👏 Acoustic tripwire armed. Clap threshold: {_tw_thresh:.0f} RMS")

        print("🤖 Jarvis is ready. Say 'Jarvis' or clap twice to wake me up. (Ctrl+C to exit)")
        set_ui_state("idle")

        # Single persistent HTTP client — no per-request overhead
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=10.0)) as http_client:
            while True:

                # Read one audio frame (this is the ONLY stream read — shared
                # by both the wake-word detector and the tripwire)
                data = audio_stream.read(CHUNK, exception_on_overflow=False)
                rms  = get_rms(data)

                # ── Acoustic tripwire (inline, no competing stream) ──────────
                if _tripwire is not None and _tripwire.process_chunk(data, RATE):
                    print("\n👏 Double-clap — Jarvis awakened by acoustic tripwire!")
                    set_ui_state("listening")
                    await speak_text("Yes sir?")
                    # Longer flush: TTS takes ~0.8–1s to play; we must let it
                    # fully finish before re-enabling the mic or the TTS echo
                    # gets transcribed as a command.
                    await asyncio.sleep(1.2)
                    _flush_mic(audio_stream)
                    await asyncio.sleep(0.4)
                    _flush_mic(audio_stream)
                    awaiting_followup = True
                    continue

                # State 1: Idle — wait for sound above threshold
                if rms <= SILENCE_THRESHOLD:
                    continue

                # State 2: Recording
                print("\n🎙️  Listening...")
                set_ui_state("listening")
                audio_path = await record_audio(audio_stream, pa)

                if not audio_path:
                    continue

                # State 3: Transcribing
                print("⚙️  Processing...")
                set_ui_state("processing")
                transcribed_text = await safe_transcribe(audio_path)
                text_lower = transcribed_text.lower().strip()

                if not text_lower:
                    set_ui_state("idle")
                    if awaiting_followup:
                        print("\n⏳ No response heard. Going back to sleep. Say 'Jarvis' to wake me up.")
                        awaiting_followup = False
                    continue

                print(f"📝 Heard: '{transcribed_text}'")


                # ── Normal command / Wake-word routing ─────────────────────────
                if awaiting_followup:
                    awaiting_followup = False
                    command = transcribed_text.strip()
                    print(f"📝 Follow-up: {command}")
                else:
                    # Multilingual wake word detection
                    command = extract_wake_word_command(transcribed_text)
                    if command is None:
                        print(f"[Ignored — no wake word: '{transcribed_text}']")
                        continue
                    print(f"🗣️  Command: '{command}'")

                    if not command:
                        # User only said "Jarvis" — greet locally in the same language
                        print("👋 Just a greeting — responding locally.")
                        from app.services.context_classifier import detect_language
                        lang = detect_language(transcribed_text)

                        if lang == "english":
                            greetings = [
                                "Yes Sir?",
                                "How can I help?",
                                "I'm listening.",
                                "What can I do for you?",
                                "Go ahead, Sir.",
                            ]
                        else:
                            # Hindi/Hinglish wake — Hinglish greeting
                            greetings = [
                                "Haan Sir, boliye?",
                                "Ji Sir, kya kaam hai?",
                                "Bol Sir, sun raha hoon.",
                                "Batao Sir, kya karna hai?",
                            ]
                        await speak_text(random.choice(greetings))
                        _flush_mic(audio_stream)
                        await asyncio.sleep(0.5)
                        _flush_mic(audio_stream)
                        awaiting_followup = True
                        continue



                # ── Send to backend ───────────────────────────────────────────
                print("🧠 Sending to Jarvis brain...")

                if _is_complex_task(command):
                    print("🤖 Complex task detected — engaging agentic planner...")
                    await speak_text("On it, sir. Let me work through this step by step.")
                    set_ui_state("working")
                elif any(w in command.lower() for w in
                         ['list', 'organize', 'rename', 'convert', 'batch', 'compress',
                          'resize', 'automate', 'scroll', 'drag', 'empty', 'find all',
                          'sort all', 'clean', 'download all', 'move all']):
                    set_ui_state("working")
                else:
                    set_ui_state("processing")

                try:
                    full_response = await send_command_streaming(http_client, command)
                except Exception as e:
                    err_msg = f"Sorry sir, I ran into a problem: {str(e)[:80]}"
                    print(f"\n[Error: {e}]")
                    await speak_text(err_msg)
                    set_ui_state("idle")
                    _flush_mic(audio_stream)
                    continue

                # Detect if Jarvis asked a follow-up question
                response_stripped = full_response.strip()



                if response_stripped.endswith("?"):
                    print("\n💬 Jarvis is waiting for your answer (no wake word needed)...")
                    awaiting_followup = True
                else:
                    followups = [
                        "Aur kuch chahiye, Sir?",
                        "Koi aur kaam?",
                        "Kuch aur kar sakta hoon?",
                        "Batao Sir, aur kya karna hai?",
                        "Ho gaya. Kuch aur?",
                    ]
                    followup = random.choice(followups)
                    print(f"\n💬 {followup} (Listening...)")
                    await speak_text(followup)
                    awaiting_followup = True

                # Post-speech cooldown — flush mic to prevent TTS echo re-triggering
                await asyncio.sleep(1.0)
                _flush_mic(audio_stream)

    except KeyboardInterrupt:
        print("\nStopping Jarvis voice agent...")
    except Exception as e:
        print(f"\n[Fatal error in voice agent]: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if audio_stream is not None:
            try:
                audio_stream.close()
            except Exception:
                pass
        if pa is not None:
            try:
                pa.terminate()
            except Exception:
                pass


def _flush_mic(audio_stream):
    """Discard any audio in the mic buffer to prevent TTS echo from re-triggering."""
    try:
        available = audio_stream.get_read_available()
        if available > 0:
            audio_stream.read(available, exception_on_overflow=False)
    except Exception:
        pass


if __name__ == '__main__':
    # Kill any existing orphaned overlays first
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline and 'jarvis_overlay.py' in ' '.join(cmdline):
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            pass

    # Launch the arc reactor overlay as a background process
    _overlay_path = os.path.join(os.path.dirname(__file__), 'jarvis_overlay.py')
    _overlay_proc = None
    if os.path.exists(_overlay_path):
        try:
            _overlay_proc = subprocess.Popen(
                [sys.executable, _overlay_path],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            print("🎨 Jarvis overlay started.")
        except Exception as e:
            print(f"[Overlay] Could not start: {e}")

    set_ui_state('idle')
    try:
        asyncio.run(run_voice_agent())
    finally:
        set_ui_state('idle')
        if _overlay_proc:
            _overlay_proc.terminate()
