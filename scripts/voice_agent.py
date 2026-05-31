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

# Import planner classifier at module level (not inside the hot loop)
try:
    from app.services.planner import is_complex_task as _is_complex_task
except Exception:
    def _is_complex_task(cmd): return False

# (PIN removed — WhatsApp now uses two-phase confirmation instead)

_NON_CONTACTS = {
    'me', 'a', 'the', 'my', 'him', 'her', 'them', 'someone', 'anybody',
    'anyone', 'you', 'it', 'that', 'this', 'message', 'msg', 'text'
}

def detect_whatsapp_send(text: str):
    normalized = text.strip().rstrip('.,!?।')
    patterns = [
        r'send\s+(?:a\s+)?(?:message|msg|text|whatsapp\s+message)\s+to\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
        r'message\s+([\w\s\.]+?)\s+on\s+(?:whatsapp|wp)',
        r'whatsapp\s+(?:message\s+(?:to\s+)?|text\s+(?:to\s+)?)?([\w\s\.]+?)(?:\s+saying.*)?$',
        r'send\s+([\w\s\.]+?)\s+a\s+(?:message|msg|text|whatsapp)',
        r'send\s+(?:a\s+)?(?:message|msg|text)(?:\s+to)?\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
    ]
    for pattern in patterns:
        m = re.search(pattern, normalized, re.IGNORECASE)
        if m:
            contact = m.group(1).strip().strip('.,!?')
            words = contact.lower().split()
            if len(contact) > 1 and not all(w in _NON_CONTACTS for w in words):
                return contact
    return None


def detect_note_intent(text: str) -> bool:
    normalized = text.strip().rstrip('.,!?\u0964').lower()
    patterns = [
        r'^(?:add|create|write|make|put|save)\s+(?:a\s+)?(?:short\s+)?(?:note|sticky|reminder)(?:\s+(?:on|to|for)\s+\S+)?',
        r'^take\s+(?:a\s+)?note(?:\s+(?:for|on)\s+\S+)?',
        r'^(?:note|sticky|reminder)\s+(?:it|this|down)?',
        r'^remind\s+me\s+to',
    ]
    for p in patterns:
        if re.search(p, normalized):
            return True
    return False


def clean_markdown(text: str) -> str:
    text = re.sub(r'```.*?```', ' code block ', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', '', text)
    text = re.sub(r'(\*\*|\*|__|_|~~)', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text.strip()


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

    # WhatsApp smart multi-step flow state machine
    # Steps: "ask_message" | "confirm" | None
    whatsapp_flow = {
        "active": False,
        "step": None,
        "contact": None,      # final resolved contact name
        "message": None,      # message to send
    }

    # Note creation state machine
    note_flow = {
        "active": False
    }

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

        print("🤖 Jarvis is ready. Say 'Jarvis' to wake me up. (Ctrl+C to exit)")
        set_ui_state("idle")

        # Single persistent HTTP client — no per-request overhead
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=10.0)) as http_client:
            while True:
                data = audio_stream.read(CHUNK, exception_on_overflow=False)
                rms = get_rms(data)

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

                # ── Note Flow State Machine ────────────────────────────────────
                if note_flow["active"]:
                    note_flow["active"] = False
                    note_content = transcribed_text.strip()
                    print(f"📝 Note content: {note_content}")
                    command = f"create a sticky note that says: {note_content}"
                    print("🧠 Sending to Jarvis brain...")
                    set_ui_state("processing")
                    try:
                        await send_command_streaming(http_client, command)
                    except Exception as e:
                        print(f"\n[Error: Could not reach backend — {e}]")
                    print("\n🤖 Ready. Say 'Jarvis' to wake me up.")
                    _flush_mic(audio_stream)
                    continue

                # ── WhatsApp Smart State Machine ───────────────────────────────
                if whatsapp_flow["active"]:
                    step = whatsapp_flow["step"]

                    # ---- User is saying the message text -----------------------
                    if step == "ask_message":
                        message_text = transcribed_text.strip()
                        contact = whatsapp_flow["contact"]
                        whatsapp_flow["message"] = message_text
                        whatsapp_flow["step"] = "confirm"
                        reply = (
                            f"Got it. Before I send, confirming: "
                            f"To {contact} — {message_text}. "
                            f"Should I go ahead and send this?"
                        )
                        print(f"\U0001f4cb {reply}")
                        await speak_text(reply)
                        awaiting_followup = True
                        _flush_mic(audio_stream)
                        continue

                    # ---- Waiting for yes / no confirmation ---------------------
                    elif step == "confirm":
                        # Words that mean YES
                        yes_kw = ['yes', 'yeah', 'yep', 'go ahead', 'do it',
                                  'ok', 'okay', 'confirm', 'haan', 'kar do', 'correct', 'sure']
                        # Words that mean NO
                        no_kw  = ['no', 'nope', 'cancel', 'stop', 'abort',
                                  'nahi', 'mat bhejo', 'nevermind', 'never mind',
                                  "don't", "dont", 'not', 'wait']

                        # Check NO first (higher priority — prevents false sends)
                        is_no  = any(w in text_lower for w in no_kw)
                        is_yes = (not is_no) and any(w in text_lower for w in yes_kw)

                        if is_yes:
                            contact = whatsapp_flow["contact"]
                            msg     = whatsapp_flow["message"]
                            whatsapp_flow = {"active": False, "step": None,
                                             "contact": None, "message": None}
                            print(f"\U0001f4e4 Sending WhatsApp to {contact}: {msg}")
                            await speak_text("Sending now, sir.")
                            try:
                                from app.services.whatsapp_smart import confirm_whatsapp_send
                                loop = asyncio.get_event_loop()
                                result = await loop.run_in_executor(
                                    None, confirm_whatsapp_send, contact, msg
                                )
                                print(f"\u2705 {result}")
                                await speak_text("Done! Your message has been sent.")
                            except Exception as send_err:
                                print(f"\u274c WhatsApp error: {send_err}")
                                await speak_text("Sorry, I ran into a problem while sending.")
                        elif any(w in text_lower for w in no_kw):
                            whatsapp_flow = {"active": False, "step": None,
                                             "contact": None, "message": None}
                            await speak_text("Okay, message cancelled.")
                        else:
                            await speak_text("Should I send it? Please say yes or no.")
                            awaiting_followup = True
                        _flush_mic(audio_stream)
                        continue

                    # ---- No contact found — waiting for alternate name ----------
                    elif step == "ask_contact":
                        new_contact = transcribed_text.strip()
                        stored_msg  = whatsapp_flow.get("message")
                        whatsapp_flow["contact"] = new_contact
                        if stored_msg:
                            whatsapp_flow["step"] = "confirm"
                            reply = f"Okay. To {new_contact}: {stored_msg}. Should I send?"
                        else:
                            whatsapp_flow["step"] = "ask_message"
                            reply = f"What message should I send to {new_contact}?"
                        await speak_text(reply)
                        awaiting_followup = True
                        _flush_mic(audio_stream)
                        continue

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
                        # User only said "Jarvis" — greet locally
                        print("👋 Just a greeting — responding locally.")
                        greetings = [
                            "How may I help you?",
                            "Yes, sir?",
                            "I'm listening.",
                            "How can I assist you today?",
                            "What can I do for you?"
                        ]
                        await speak_text(random.choice(greetings))
                        _flush_mic(audio_stream)
                        await asyncio.sleep(0.5)
                        _flush_mic(audio_stream)
                        awaiting_followup = True
                        continue

                # ── WhatsApp send intent (first trigger) ──────────────────────────
                wa_contact = detect_whatsapp_send(command)
                if wa_contact:
                    # Only match inline message if user said "saying X" / "say X" / "that says X"
                    # NOT "send a message to X" (which would wrongly capture "to X" as the message)
                    msg_inline = re.search(
                        r'(?:saying|say(?:ing)?|that\s+says)[:\s]+["\']?(.+?)["\']?\s*$',
                        command, re.I
                    )
                    if msg_inline:
                        inline_msg = msg_inline.group(1).strip()
                        whatsapp_flow = {"active": True, "step": "confirm",
                                         "contact": wa_contact, "message": inline_msg}
                        reply = (
                            f"Before I send, confirming: "
                            f"To {wa_contact} — {inline_msg}. Should I go ahead?"
                        )
                    else:
                        whatsapp_flow = {"active": True, "step": "ask_message",
                                         "contact": wa_contact, "message": None}
                        reply = f"Sure. What message should I send to {wa_contact}?"
                    awaiting_followup = True
                    print(f"\U0001f4ac {reply}")
                    await speak_text(reply)
                    _flush_mic(audio_stream)
                    continue

                # ── Note intent ───────────────────────────────────────────────
                if detect_note_intent(command):
                    note_flow["active"] = True
                    awaiting_followup = True
                    reply = "What should I write in the note?"
                    print(f"📝 {reply}")
                    await speak_text(reply)
                    _flush_mic(audio_stream)
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

                # ── WhatsApp no-contact fallback ──────────────────────────────────────
                if response_stripped.startswith("__ASK_CONTACT__"):
                    clean_resp = response_stripped.replace("__ASK_CONTACT__", "").strip()
                    # Store the pending message (if any) in the flow
                    if not whatsapp_flow["active"]:
                        whatsapp_flow = {"active": True, "step": "ask_contact",
                                         "contact": None, "message": None}
                    else:
                        whatsapp_flow["step"] = "ask_contact"
                    awaiting_followup = True
                    print(f"\U0001f50d {clean_resp}")
                    await speak_text(clean_resp)
                    _flush_mic(audio_stream)
                    continue

                if response_stripped.endswith("?"):
                    print("\n💬 Jarvis is waiting for your answer (no wake word needed)...")
                    awaiting_followup = True
                else:
                    followups = [
                        "Can I help you in any other way?",
                        "Is there anything else I can do for you?",
                        "Do you need help with anything else?",
                        "What else can I do for you?"
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
