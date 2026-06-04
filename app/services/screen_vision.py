"""
screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)
---------------------------------------------------------------------
Replaces Tesseract OCR with a Vision-Language Model (Gemini 2.0 Flash).
Sends the full screenshot as a base64 image to the VLM, which understands
layout, icons, colors, structure, and context — exactly like a human.

Architecture:
  Layer 0  — Screen capture via mss (~10ms, no disk I/O)
  Layer 1  — VLM analysis via Gemini 2.0 Flash (free tier, 15 req/min)
  Layer 2  — Context engine (active window title, per-app prompts, screen history)
  Layer 3  — Intent router (describe / suggest / execute modes)
  BG Loop  — Passive watch thread (pixel diff → VLM only on change)

Public API:
    understand_screen(user_query, intent_mode)   → LLM-ready string
    describe_screen_vlm()                        → passive description
    start_background_watcher(callback)           → starts BG thread
    stop_background_watcher()                    → stops BG thread
"""

import io
import base64
import threading
import time
import ctypes
import logging
from collections import deque
from typing import Callable, Optional

import mss
import numpy as np
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Model config ────────────────────────────────────────────────────────────────────────
# gemini-2.0-flash-lite → vision model (FREE: 30 req/min, 1500 req/day — most generous tier)
# gemma-3-27b-it        → deep text reasoning for suggest + execute modes (free, very capable)
VISION_MODEL  = "gemini-1.5-flash"  # multimodal — 15 req/min free tier
REASON_MODEL  = "gemini-1.5-flash"  # text-only  — deep reasoning

# ── Per-app system prompt injections ─────────────────────────────────────────
APP_PROMPTS: dict[str, str] = {
    "Code":         "User is coding. Watch for syntax errors, exceptions, open file names, and language. Suggest refactors if obvious issues are visible.",
    "Visual Studio": "User is coding in Visual Studio. Note errors in the Error List, currently open file, and any build output.",
    "Chrome":       "User is browsing the web. Note the URL, page title, visible content, and what they appear to be researching or doing.",
    "Firefox":      "User is browsing. Note the URL, page content, and any forms or errors visible.",
    "Edge":         "User is in Microsoft Edge. Note the URL, page content, and any alerts or popups.",
    "WhatsApp":     "User is messaging on WhatsApp. Note the open chat name and the last few visible messages.",
    "Excel":        "User is in a spreadsheet. Note visible data, any formulas, chart types, and whether there are errors (#REF!, #DIV/0!).",
    "Word":         "User is writing a document in Word. Note the document title and the visible paragraph content.",
    "PowerPoint":   "User is in PowerPoint. Note the current slide content, theme, and any layout issues.",
    "Outlook":      "User is in Outlook. Note whether they are composing, reading, or browsing inbox. Mention visible sender/subject.",
    "Terminal":     "User is in a terminal. Note the last commands run, any error output, and the current directory.",
    "cmd":          "User has a command prompt open. Note the last command and any visible output or errors.",
    "PowerShell":   "User is in PowerShell. Note the last command run, any error output or stack traces.",
    "Notepad":      "User is editing a plain text file in Notepad. Describe the content and any obvious formatting issues.",
    "default":      "Analyze what the user is currently working on. Describe the app, the content visible, any errors or alerts, and what would genuinely help them next.",
}

# ── Screen history (last 5 frames for diff reasoning) ────────────────────────
_screen_history: deque = deque(maxlen=5)  # each entry: {"b64": str, "timestamp": float, "array": np.ndarray}

# ── Background watcher state ──────────────────────────────────────────────────
_watcher_thread: Optional[threading.Thread] = None
_watcher_stop_event = threading.Event()
_last_watcher_array: Optional[np.ndarray] = None

# ── Watcher tuning ────────────────────────────────────────────────────────────
# Free tier: gemini-2.0-flash-lite = 30 req/min = 1 req every 2s max.
# Watcher fires every 15s at most, only when screen changes — very safe.
DIFF_THRESHOLD_PERCENT   = 5.0
WATCHER_INTERVAL_SECONDS = 15   # check every 15s (4 req/min max)
WATCHER_STARTUP_DELAY    = 30   # wait 30s after server boot before first analysis


# ── Layer 0: Screen capture ───────────────────────────────────────────────────

def capture_screen_b64(max_width: int = 1280, quality: int = 70) -> tuple[str, np.ndarray]:
    """
    Capture the primary monitor using mss (~10ms).
    Returns (base64_jpeg_string, numpy_array_for_diff).
    JPEG quality=70 is the sweet spot: small payload, Gemini reads it fine.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        raw = sct.grab(monitor)
        pil = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

    # Downscale for API efficiency
    w, h = pil.size
    if w > max_width:
        scale = max_width / w
        pil = pil.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # NumPy array for pixel diff (keep at reduced size)
    arr = np.array(pil)

    # Encode to JPEG in memory
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=quality)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return b64, arr


# ── Layer 2: Context engine ───────────────────────────────────────────────────

def _get_active_window_title() -> str:
    """Returns the foreground window title using WinAPI."""
    try:
        buf = ctypes.create_unicode_buffer(256)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        return buf.value or "(unknown window)"
    except Exception:
        return "(unknown window)"


def _get_active_process_name() -> str:
    """Returns the executable name of the foreground window's process."""
    try:
        import psutil
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        proc = psutil.Process(pid.value)
        return proc.name()  # e.g. "Code.exe"
    except Exception:
        return ""


def _resolve_app_prompt(window_title: str, process_name: str) -> str:
    """Match window title / process name to a per-app prompt."""
    combined = (window_title + " " + process_name).lower()
    for key, prompt in APP_PROMPTS.items():
        if key.lower() in combined:
            return prompt
    return APP_PROMPTS["default"]


def _build_history_context() -> str:
    """
    Summarise the last N screen states so the VLM can reason about what changed.
    Kept lightweight — just timestamps and count.
    """
    if len(_screen_history) < 2:
        return ""
    count = len(_screen_history)
    oldest = time.strftime("%H:%M:%S", time.localtime(_screen_history[0]["timestamp"]))
    newest = time.strftime("%H:%M:%S", time.localtime(_screen_history[-1]["timestamp"]))
    return (
        f"Note: This is frame {count} of a recent sequence captured between "
        f"{oldest} and {newest}. Reason about what has changed if relevant."
    )


# ── Layer 1: VLM call (Gemini 2.0 Flash) ─────────────────────────────────────

def _call_gemini_vision(b64_image: str, system_prompt: str, user_query: str) -> str:
    """
    Send screenshot + context to Gemini 2.0 Flash (vision model).
    Returns the model’s response text, or empty string on failure.
    Best for: screen capture analysis, image understanding, "describe" mode.
    """
    try:
        import google.generativeai as genai
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key == "YOUR_FREE_GEMINI_KEY_HERE":
            logger.warning("GEMINI_API_KEY not set — VLM vision unavailable.")
            return ""

        genai.configure(api_key=api_key, transport="rest")
        model = genai.GenerativeModel(VISION_MODEL)

        response = model.generate_content([
            system_prompt,
            {"mime_type": "image/jpeg", "data": b64_image},
            f"User asked: {user_query}" if user_query else "Describe what you see.",
        ])
        return response.text.strip()
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "quota" in err_str:
            logger.warning(f"[screen_vision] Gemini quota exceeded (429). EXACT ERROR: {e}")
        else:
            logger.error(f"[screen_vision] Gemini vision call failed: {e}")
        return ""


def _call_gemma_reasoning(scene_description: str, task_prompt: str) -> str:
    """
    Send a scene description (already extracted by Gemini vision) to Gemma 4
    for deep text reasoning. Used for suggest + execute intent modes.

    Why two-stage?
      • Gemini Flash sees the image → extracts what’s on screen as text
      • Gemma 4 reasons over that text → gives smart suggestions / action plans
      This gives you the best of both: fast vision + powerful reasoning, all free.

    Returns the model’s response text, or falls back to the scene description on failure.
    """
    try:
        import google.generativeai as genai
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key == "YOUR_FREE_GEMINI_KEY_HERE":
            return scene_description  # graceful fallback

        genai.configure(api_key=api_key, transport="rest")
        model = genai.GenerativeModel(REASON_MODEL)

        full_prompt = (
            f"You are JARVIS, a highly intelligent AI assistant.\n\n"
            f"Here is what is currently on the user’s screen (analysed by a vision model):\n"
            f"────────────────────────────────────────────────────────────\n"
            f"{scene_description}\n"
            f"────────────────────────────────────────────────────────────\n\n"
            f"{task_prompt}"
        )

        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "quota" in err_str:
            logger.warning("[screen_vision] Gemma quota exceeded (429). Falling back to scene desc.")
        else:
            logger.error(f"[screen_vision] Gemma reasoning call failed: {e}")
        return scene_description  # graceful fallback



# ── Layer 3: Intent router ────────────────────────────────────────────────────

INTENT_DESCRIBE = "describe"
INTENT_SUGGEST  = "suggest"
INTENT_EXECUTE  = "execute"

def _classify_intent(user_query: str) -> str:
    """
    Parse the user's phrasing to determine the response mode.
      describe → "What am I looking at?", "What's on my screen?", "Describe this"
      suggest  → "What should I do?", "Help me", "What's next?"
      execute  → "Fix this", "Do that", "Run it", "Close it"
    """
    q = user_query.lower().strip()

    describe_kw = [
        "what am i looking at", "what's on my screen", "whats on my screen",
        "what is on my screen", "describe my screen", "what do you see",
        "describe this", "what's open", "read my screen", "what is this",
        "what app", "what page", "what is happening",
    ]
    suggest_kw = [
        "what should i do", "help me", "what's next", "whats next",
        "what do i do", "any suggestions", "suggest", "recommend",
        "what would you do", "how do i", "how should i",
        "what can i do", "what are my options",
    ]
    execute_kw = [
        "fix this", "fix it", "fix the error", "do that", "do it",
        "run it", "close it", "click it", "execute", "apply",
        "automate", "handle this", "take care of", "resolve",
    ]

    if any(kw in q for kw in execute_kw):
        return INTENT_EXECUTE
    if any(kw in q for kw in suggest_kw):
        return INTENT_SUGGEST
    if any(kw in q for kw in describe_kw):
        return INTENT_DESCRIBE
    return INTENT_DESCRIBE  # default


def _build_system_prompt(intent: str, app_prompt: str, history_ctx: str) -> str:
    """Assemble the full system prompt based on intent mode and context."""

    base = f"""You are JARVIS, a highly intelligent AI assistant with vision.
{app_prompt}
{history_ctx}
The user's screen is attached as an image. Understand it deeply — not just the text,
but the layout, colors, icons, UI state, open files, errors, notifications, and context."""

    if intent == INTENT_DESCRIBE:
        return base + """

TASK: Give a clear, concise structured description of what is currently on the screen.
Format:
  App: <name>
  Doing: <what user is working on>
  Content: <main visible content>
  Alerts/Errors: <any visible errors, warnings, popups — or "none">
Be specific. 3-6 sentences max."""

    elif intent == INTENT_SUGGEST:
        return base + """

TASK: Suggest the 3 best next actions the user should take RIGHT NOW, given what you see.
Format each suggestion as a numbered list.
Be concrete and actionable. Reference what is actually on the screen.
End with one short sentence on what you would prioritize."""

    elif intent == INTENT_EXECUTE:
        return base + """

TASK: The user wants you to take action on what you see.
Describe exactly what action needs to be taken, in precise step-by-step instructions.
If it is code-related, provide the corrected code snippet.
If it is a UI action, describe the exact clicks/keystrokes needed.
Be direct — the user wants you to DO it, not explain it endlessly."""

    return base


# ── Public API ────────────────────────────────────────────────────────────────

def understand_screen(
    user_query: str = "",
    intent_mode: Optional[str] = None,
) -> str:
    """
    Main entry point. Captures screen, resolves context, calls VLM, routes response.

    Args:
        user_query:   What the user asked (used for intent classification).
        intent_mode:  Force a specific mode ('describe'/'suggest'/'execute').
                      If None, auto-classified from user_query.

    Returns:
        VLM response string, or empty string if VLM unavailable.
    """
    # Capture
    try:
        b64, arr = capture_screen_b64()
    except Exception as e:
        logger.error(f"[screen_vision] Capture failed: {e}")
        return ""

    # Store in history
    _screen_history.append({
        "b64": b64,
        "timestamp": time.time(),
        "array": arr,
    })

    # Context
    window_title  = _get_active_window_title()
    process_name  = _get_active_process_name()
    app_prompt    = _resolve_app_prompt(window_title, process_name)
    history_ctx   = _build_history_context()

    # Intent
    intent = intent_mode or _classify_intent(user_query)

    # Augment query with window context
    context_preamble = f"[Active window: '{window_title}' | Process: '{process_name}']"
    full_query = f"{context_preamble}\n{user_query}" if user_query else context_preamble

    # System prompt (always describe for the vision stage)
    vision_system = _build_system_prompt(INTENT_DESCRIBE, app_prompt, history_ctx)

    # ── Stage 1: Gemini 2.0 Flash sees the image ──────────────────────────────
    scene_description = _call_gemini_vision(b64, vision_system, full_query)

    if not scene_description:
        return ""

    # ── Stage 2: Gemma 4 reasons over the scene (suggest + execute only) ───────
    if intent == INTENT_DESCRIBE:
        # Describe mode — Gemini’s output is already the answer
        return scene_description

    elif intent == INTENT_SUGGEST:
        task_prompt = (
            "The user wants suggestions. Based on what is on their screen, give the "
            "3 best next actions they should take RIGHT NOW. Format as a numbered list. "
            "Be concrete — reference what is actually visible. End with one sentence on "
            "what you would prioritize."
        )
        return _call_gemma_reasoning(scene_description, task_prompt)

    elif intent == INTENT_EXECUTE:
        task_prompt = (
            "The user wants you to take action. Based on what is on their screen, "
            "describe exactly what needs to be done in precise step-by-step instructions. "
            "If it is code-related, provide the corrected code snippet. "
            "If it is a UI action, describe the exact clicks/keystrokes. "
            "Be direct and actionable — the user wants it done."
        )
        return _call_gemma_reasoning(scene_description, task_prompt)

    return scene_description



def describe_screen_vlm() -> str:
    """
    Lightweight passive description — used as context injection in chat.py.
    Always runs in describe mode. Returns empty string if VLM not available.
    """
    return understand_screen(user_query="", intent_mode=INTENT_DESCRIBE)


# ── Background passive watch loop ─────────────────────────────────────────────

def _pixel_diff_percent(a: np.ndarray, b: np.ndarray) -> float:
    """
    Returns the percentage of pixels that changed significantly between two frames.
    Uses mean absolute difference per channel > 20 as "changed".
    """
    if a.shape != b.shape:
        # Resize b to match a
        pil_b = Image.fromarray(b)
        pil_b = pil_b.resize((a.shape[1], a.shape[0]), Image.LANCZOS)
        b = np.array(pil_b)
    diff = np.abs(a.astype(np.int16) - b.astype(np.int16))
    changed_pixels = np.mean(diff, axis=2) > 20  # threshold per pixel
    return float(np.sum(changed_pixels) / changed_pixels.size * 100)


def _watcher_loop(callback: Callable[[str], None]) -> None:
    """
    Background thread body.
    Every WATCHER_INTERVAL_SECONDS:
      - Capture screen
      - Compute pixel diff vs last frame
      - If diff > DIFF_THRESHOLD_PERCENT → call VLM
      - If VLM finds something notable → call callback(alert_text)
    Zero API cost during idle!
    """
    global _last_watcher_array

    proactive_system = """You are JARVIS monitoring the user's screen silently.
If you see something that clearly needs attention (build errors, test failures,
an unread alert, a crash dialog, a security warning, or a significant change),
respond with a short alert: "Sir, <observation>. Want me to <action>?"
If everything looks normal and nothing needs attention, respond with exactly: IDLE
Be very selective — only alert on genuinely important events."""

    # Wait before first analysis so the server settles and API key propagates
    logger.info(f"[watcher] Startup delay {WATCHER_STARTUP_DELAY}s — will begin passive monitoring shortly.")
    _watcher_stop_event.wait(timeout=WATCHER_STARTUP_DELAY)

    while not _watcher_stop_event.is_set():
        try:
            b64, arr = capture_screen_b64(max_width=960, quality=60)

            should_analyze = False
            if _last_watcher_array is None:
                should_analyze = True
            else:
                diff_pct = _pixel_diff_percent(_last_watcher_array, arr)
                if diff_pct >= DIFF_THRESHOLD_PERCENT:
                    should_analyze = True
                    logger.debug(f"[watcher] Screen changed {diff_pct:.1f}% — triggering VLM")

            if should_analyze:
                _last_watcher_array = arr
                window_title = _get_active_window_title()
                process_name = _get_active_process_name()
                app_prompt   = _resolve_app_prompt(window_title, process_name)

                ctx = f"[Window: '{window_title}' | Process: '{process_name}']\n{app_prompt}"
                full_system = proactive_system + "\n\n" + ctx

                response = _call_gemini_vision(b64, full_system, "")
                if response and response.strip().upper() != "IDLE" and len(response.strip()) > 10:
                    callback(response.strip())

        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "rate limit" in err_str:
                logger.warning("[watcher] Gemini quota exceeded. Pausing passive watcher for 60 seconds.")
                _watcher_stop_event.wait(timeout=60.0)
                continue
            else:
                logger.error(f"[watcher] Loop error: {e}")

        _watcher_stop_event.wait(timeout=WATCHER_INTERVAL_SECONDS)


def start_background_watcher(callback: Callable[[str], None]) -> None:
    """
    Start the passive background screen watcher.

    Args:
        callback: Function called with the VLM alert string whenever
                  a significant screen change is detected.
                  e.g. lambda msg: print(f"[JARVIS] {msg}")
    """
    global _watcher_thread
    if _watcher_thread and _watcher_thread.is_alive():
        logger.info("[watcher] Already running.")
        return

    _watcher_stop_event.clear()
    _watcher_thread = threading.Thread(
        target=_watcher_loop,
        args=(callback,),
        daemon=True,
        name="jarvis-screen-watcher",
    )
    _watcher_thread.start()
    logger.info("[watcher] Background screen watcher started.")


def stop_background_watcher() -> None:
    """Stop the background screen watcher thread cleanly."""
    _watcher_stop_event.set()
    if _watcher_thread:
        _watcher_thread.join(timeout=WATCHER_INTERVAL_SECONDS + 2)
    logger.info("[watcher] Background screen watcher stopped.")
