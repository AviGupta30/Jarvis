"""
screen_reader.py — Jarvis Screen Vision (VLM-first architecture)
-----------------------------------------------------------------
Layered screen understanding strategy:

  Layer 1 (Best):   VLM via screen_vision.py (Gemini 2.0 Flash)
                    → Understands layout, icons, colors, errors, context
  Layer 2 (Good):   Groq LLaVA vision fallback
                    → Used if Gemini key missing/rate-limited
  Layer 3 (Basic):  pytesseract OCR
                    → Raw text extraction, no context understanding
  Layer 4 (Min):    pywinauto accessibility tree
                    → Native Win32 apps only
  Layer 5 (Last):   Window title only
                    → Always works as last resort

Usage:
    from app.services.screen_reader import read_screen, describe_screen_for_llm
    text = read_screen()                 # rich VLM description of screen
    summary = describe_screen_for_llm() # LLM-ready structured summary
"""

import os
import re
import base64
import io
import time
import logging

import pyautogui
from PIL import Image

logger = logging.getLogger(__name__)


# ── Tesseract path resolution (legacy OCR fallback) ──────────────────────────
_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(
        os.environ.get("USERNAME", "")
    ),
]
_tesseract_ready = False


def _init_tesseract() -> bool:
    """Find and configure pytesseract. Returns True if ready."""
    global _tesseract_ready
    if _tesseract_ready:
        return True
    try:
        import pytesseract
        for path in _TESSERACT_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        img = Image.new("RGB", (10, 10), color="white")
        pytesseract.image_to_string(img)
        _tesseract_ready = True
        return True
    except Exception:
        return False


# ── Layer 1: VLM via Gemini 2.0 Flash ────────────────────────────────────────

def _vlm_screen(user_query: str = "", intent_mode: str = None) -> str:
    """
    Primary layer: sends screenshot to Gemini 2.0 Flash VLM.
    Returns rich contextual description, or empty string on failure.
    """
    try:
        from app.services.screen_vision import understand_screen
        result = understand_screen(user_query=user_query, intent_mode=intent_mode)
        return result or ""
    except Exception as e:
        logger.warning(f"[screen_reader] VLM layer failed: {e}")
        return ""


# ── Layer 2: Groq LLaVA vision fallback ──────────────────────────────────────

def _groq_vision_screen() -> str:
    """
    Fallback vision layer using Groq LLaVA.
    Faster (~200ms) but weaker at complex UI understanding than Gemini.
    """
    b64_image = get_screen_screenshot_b64()
    if not b64_image:
        return ""
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)

        prompt = (
            "You are JARVIS, an AI assistant. Look closely at this screenshot of the user's screen. "
            "Describe exactly what they are looking at. What app is open? What is the main content? "
            "Are there any errors, popups, or unread notifications? "
            "Be concise but highly observant. Output plain text only."
        )
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{b64_image}"
                    }},
                ],
            }],
            model="llama-3.2-90b-vision-preview",
            temperature=0.2,
            max_tokens=300,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.warning(f"[screen_reader] Groq vision fallback failed: {e}")
        return ""


# ── Layer 3: OCR via pytesseract ──────────────────────────────────────────────

def _ocr_screen() -> str:
    """
    Legacy OCR layer. Works on any app but extracts raw text only —
    no layout, color, or context understanding.
    Returns extracted text, or empty string on failure.
    """
    if not _init_tesseract():
        return ""
    try:
        import pytesseract
        screenshot = pyautogui.screenshot()
        w, h = screenshot.size
        if w > 1920:
            scale = 1920 / w
            screenshot = screenshot.resize(
                (int(w * scale), int(h * scale)), Image.LANCZOS
            )
        config = "--psm 6 --oem 3"
        raw_text = pytesseract.image_to_string(screenshot, config=config)
        lines = [ln.strip() for ln in raw_text.splitlines() if len(ln.strip()) >= 3]
        return "\n".join(lines)[:6000]
    except Exception:
        return ""


# ── Layer 4: pywinauto accessibility tree ────────────────────────────────────

def _accessibility_tree() -> str:
    """
    Reads the active window's accessibility tree.
    Works best for native Win32 apps. Empty for Chrome, VS Code, etc.
    """
    try:
        from app.services.ui_inspector import get_active_window_info
        result = get_active_window_info()
        if "(no readable controls)" in result or not result:
            return ""
        return result
    except Exception:
        return ""


# ── Layer 5: Window title fallback ───────────────────────────────────────────

def _window_title_only() -> str:
    """Always works — returns at minimum the active window title."""
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(256)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        title = buf.value or "(unknown window)"
        return f"Active window: {title}"
    except Exception:
        return "Active window: (could not read)"


# ── Public API ────────────────────────────────────────────────────────────────

def read_screen(user_query: str = "", intent_mode: str = None) -> str:
    """
    Main function — returns the richest available description of the screen.

    Priority: VLM (Gemini) → Groq Vision → OCR → Accessibility Tree → Title only.

    Args:
        user_query:   Optional user question to guide VLM response style.
        intent_mode:  'describe' | 'suggest' | 'execute' — passed to VLM.
    """
    # Layer 1: VLM (best — understands layout, context, colors)
    vlm_result = _vlm_screen(user_query=user_query, intent_mode=intent_mode)
    if vlm_result and len(vlm_result) > 30:
        return f"[VLM Analysis]\n{vlm_result}"

    # Layer 2: Groq LLaVA vision fallback
    groq_result = _groq_vision_screen()
    if groq_result and len(groq_result) > 20:
        return f"[Vision Summary]\n{groq_result}"

    # Layer 3: OCR (text extraction only)
    ocr_text = _ocr_screen()

    # Layer 4: Accessibility tree
    tree_text = _accessibility_tree()

    parts = []
    if tree_text:
        parts.append(f"[Window Info]\n{tree_text}")
    if ocr_text:
        parts.append(f"[Screen Text (OCR)]\n{ocr_text}")
    if parts:
        return "\n\n".join(parts)

    # Layer 5: Last resort
    return _window_title_only()


def describe_screen_for_llm() -> str:
    """
    Returns a clean, LLM-optimized description of the current screen.
    Used as context injection in chat.py before every LLM call.
    Uses VLM describe mode for richest passive context.
    """
    try:
        from app.services.screen_vision import describe_screen_vlm
        vlm_result = describe_screen_vlm()
        if vlm_result and len(vlm_result.strip()) > 20:
            return vlm_result[:3000]
    except Exception as e:
        logger.warning(f"[screen_reader] VLM describe failed: {e}")

    # Fallback to legacy read_screen
    raw = read_screen()
    if not raw or len(raw.strip()) < 10:
        return ""
    return raw[:3000]


def read_screen_as_tool(user_query: str = "What am I looking at?") -> str:
    """
    Tool-callable version — called when user asks 'what's on my screen?'
    Routes through the full VLM pipeline with intent classification.
    """
    from app.services.screen_vision import understand_screen, _classify_intent

    intent = _classify_intent(user_query)
    result = understand_screen(user_query=user_query, intent_mode=intent)

    if result and len(result.strip()) > 20:
        return result

    # Fallback: legacy read + OCR summary
    raw = read_screen(user_query=user_query)
    if not raw or len(raw.strip()) < 10:
        return "I couldn't read your screen. Make sure a window is open and focused."

    # Proactive error detection
    error_keywords = [
        "error", "exception", "traceback", "warning", "failed", "crash",
        "403", "404", "500", "502", "504", "not found", "access denied",
    ]
    lower_raw = raw.lower()
    detected_issues = [kw for kw in error_keywords if kw in lower_raw]

    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(256)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        window_title = buf.value or ""
    except Exception:
        window_title = ""

    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)

        app_hint   = f"Active window: '{window_title}'. " if window_title else ""
        error_hint = (
            f"Note: possible issues detected ({', '.join(detected_issues[:3])}). "
            if detected_issues else ""
        )
        prompt = (
            f"{app_hint}{error_hint}"
            f"Below is raw OCR text from the user's screen. "
            f"Describe in 2-3 natural spoken sentences what the user is looking at. "
            f"Name the app, the main content, and any visible errors or alerts.\n\n"
            f"RAW TEXT:\n{raw[:3000]}"
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3,
        )
        summary = resp.choices[0].message.content.strip()
        if detected_issues:
            summary += f" I also noticed some potential issues on the screen ({', '.join(detected_issues[:2])})."
        return summary
    except Exception:
        clean = re.sub(r'\n{3,}', '\n\n', raw)
        return f"Here's what I can see:\n\n{clean[:1500]}"


def get_screen_screenshot_b64() -> str:
    """
    Takes a screenshot and returns it as a base64-encoded JPEG string.
    Used as fallback for Groq vision layer.
    Returns empty string on failure.
    """
    try:
        screenshot = pyautogui.screenshot()
        w, h = screenshot.size
        if w > 1280:
            scale = 1280 / w
            screenshot = screenshot.resize(
                (int(w * scale), int(h * scale)), Image.LANCZOS
            )
        buf = io.BytesIO()
        screenshot.convert("RGB").save(buf, format="JPEG", quality=75)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception:
        return ""
