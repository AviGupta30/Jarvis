"""
screen_reader.py — Jarvis Screen Vision (Step 1)
-------------------------------------------------
Gives Jarvis eyes. Reads what's actually ON the screen using a layered approach:

  Layer 1 (Best):  Screenshot → pytesseract OCR  — works on ANY app (Chrome, VS Code, etc.)
  Layer 2 (Good):  pywinauto accessibility tree   — good for native Win32 apps
  Layer 3 (Basic): Window title only              — always works as last resort

Usage:
    from app.services.screen_reader import read_screen, describe_screen_for_llm
    text = read_screen()                 # raw text from screen
    summary = describe_screen_for_llm() # LLM-ready structured summary
"""

import os
import re
import base64
import tempfile
import time

import pyautogui
from PIL import Image


# ── Tesseract path resolution ─────────────────────────────────────────────────
# Try common Windows install paths for Tesseract OCR
_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.environ.get("USERNAME", "")),
]

_tesseract_ready = False

def _init_tesseract() -> bool:
    """Find and configure pytesseract. Returns True if ready."""
    global _tesseract_ready
    if _tesseract_ready:
        return True
    try:
        import pytesseract
        # Try to auto-locate tesseract binary on Windows
        for path in _TESSERACT_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        # Quick validation — try a 1px image
        img = Image.new("RGB", (10, 10), color="white")
        pytesseract.image_to_string(img)
        _tesseract_ready = True
        return True
    except Exception:
        return False


# ── Layer 1: OCR via pytesseract ──────────────────────────────────────────────

def _ocr_screen() -> str:
    """
    Takes a screenshot and runs OCR on it.
    Returns extracted text, or empty string on failure.
    """
    if not _init_tesseract():
        return ""
    try:
        import pytesseract
        # Take screenshot as PIL image (no disk write needed)
        screenshot = pyautogui.screenshot()
        # Resize to improve OCR speed on large displays (scale to max 1920px wide)
        w, h = screenshot.size
        if w > 1920:
            scale = 1920 / w
            screenshot = screenshot.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        # OCR — psm 6 = "assume uniform block of text", gives best results for mixed UIs
        config = "--psm 6 --oem 3"
        raw_text = pytesseract.image_to_string(screenshot, config=config)
        # Clean up: remove lines that are pure noise (< 3 chars)
        lines = [ln.strip() for ln in raw_text.splitlines() if len(ln.strip()) >= 3]
        text = "\n".join(lines)
        return text[:6000]  # cap to avoid flooding the LLM
    except Exception as e:
        return ""


# ── Layer 2: pywinauto accessibility tree ─────────────────────────────────────

def _accessibility_tree() -> str:
    """
    Reads the active window's accessibility tree.
    Works best for native Win32 apps (Notepad, File Explorer, Office, etc.)
    Returns empty string for apps that don't expose a tree (Chrome, VS Code, etc.)
    """
    try:
        from app.services.ui_inspector import get_active_window_info
        result = get_active_window_info()
        if "(no readable controls)" in result or not result:
            return ""
        return result
    except Exception:
        return ""


# ── Layer 3: Window title fallback ────────────────────────────────────────────

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


# ── Layer 4: Groq Vision AI (Step 9) ──────────────────────────────────────────

def _vision_screen() -> str:
    """
    Takes a screenshot, sends it to Groq's free Vision model,
    and returns a smart, contextual description of the screen.
    Falls back to OCR if the API fails or rate limits.
    """
    b64_image = get_screen_screenshot_b64()
    if not b64_image:
        return ""

    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        prompt = (
            "You are Jarvis, an AI assistant. Look closely at this screenshot of the user's screen. "
            "Describe exactly what they are looking at. What app is open? What is the main content? "
            "Are there any errors, popups, or unread notifications? "
            "Be concise but highly observant. Output plain text only."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.2,
            max_tokens=300
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Vision error: {e}")
        return ""

# ── Public API ────────────────────────────────────────────────────────────────

def read_screen() -> str:
    """
    Main function — returns a text description of what's currently on screen.
    Tries Vision first, then OCR, then accessibility tree, then title-only.
    """
    # 1. Try Vision AI first (Smartest)
    vision_text = _vision_screen()
    if vision_text and len(vision_text) > 20:
        # Also grab OCR in background so the LLM can read exact text if needed
        ocr_text = _ocr_screen()
        return f"[Vision Summary]\n{vision_text}\n\n[Raw OCR Text (for reference)]\n{ocr_text[:1000]}"

    # 2. Try OCR (works on any app)
    ocr_text = _ocr_screen()

    # 3. Try accessibility tree for native apps
    tree_text = _accessibility_tree()

    # Combine both if we have both
    parts = []
    if tree_text:
        parts.append(f"[Window Info]\n{tree_text}")
    if ocr_text:
        parts.append(f"[Screen Text (OCR)]\n{ocr_text}")

    if parts:
        return "\n\n".join(parts)

    # Last resort: just the title
    return _window_title_only()


def describe_screen_for_llm() -> str:
    """
    Returns a clean, LLM-optimized description of the current screen.
    Used as context injection in chat.py before every LLM call.
    """
    raw = read_screen()
    if not raw or len(raw.strip()) < 10:
        return ""

    # Trim to a reasonable length for context injection
    return raw[:3000]


def read_screen_as_tool() -> str:
    """
    Tool-callable version — returns a well-formatted, LLM-summarized response.
    Called when user says 'what's on my screen?' or 'what am I looking at?'
    """
    raw = read_screen()

    if not raw or len(raw.strip()) < 10:
        return "I couldn't read your screen. Make sure a window is open and focused."

    # ── Detect errors in OCR text proactively ────────────────────────────────
    error_keywords = [
        "error", "exception", "traceback", "warning", "failed", "crash",
        "403", "404", "500", "502", "504", "not found", "access denied"
    ]
    lower_raw = raw.lower()
    detected_issues = [kw for kw in error_keywords if kw in lower_raw]

    # ── Get active window title for app identification ────────────────────────
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(256)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        window_title = buf.value or ""
    except Exception:
        window_title = ""

    # ── Pass through LLM for natural spoken summary ───────────────────────────
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)

        app_hint = f"Active window: '{window_title}'. " if window_title else ""
        error_hint = f"Note: possible issues detected ({', '.join(detected_issues[:3])}). " if detected_issues else ""

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
            temperature=0.3
        )
        summary = resp.choices[0].message.content.strip()

        # Append error proactive warning
        if detected_issues:
            summary += f" I also noticed some potential issues on the screen ({', '.join(detected_issues[:2])})."
        return summary
    except Exception:
        # Fallback: clean raw OCR and truncate
        clean = re.sub(r'\n{3,}', '\n\n', raw)
        return f"Here's what I can see:\n\n{clean[:1500]}"


def get_screen_screenshot_b64() -> str:
    """
    Takes a screenshot and returns it as a base64-encoded JPEG string.
    Used by Step 9 (Vision AI) to send to vision model.
    Returns empty string on failure.
    """
    try:
        screenshot = pyautogui.screenshot()
        # Downscale for API efficiency: max 1280px wide
        w, h = screenshot.size
        if w > 1280:
            scale = 1280 / w
            screenshot = screenshot.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        # Convert to JPEG bytes in memory
        import io
        buf = io.BytesIO()
        screenshot.convert("RGB").save(buf, format="JPEG", quality=75)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception:
        return ""
