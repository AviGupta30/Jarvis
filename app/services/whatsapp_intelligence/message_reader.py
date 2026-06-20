"""
message_reader.py — Jarvis WhatsApp Intelligence: Message Reader
=================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

STRATEGY:
  Primary  → Windows UI Automation (UIA) accessibility tree
             Fast, structured, zero image processing needed.
  Fallback → Screenshot + Tesseract OCR
             Used when UIA tree returns empty or app is unresponsive.

RETURNS:
  Always a list of dicts:
  [
    {
      "sender":    "them" | "you",
      "text":      "message content",
      "timestamp": "3:45 PM"  (empty string if not found)
    },
    ...
  ]
  On hard failure → returns [] and logs reason.
"""

import time
import re
from typing import List, Dict

# ── UIA ──────────────────────────────────────────────────────────────────────
try:
    import uiautomation as auto
    UIA_AVAILABLE = True
except ImportError:
    UIA_AVAILABLE = False

# ── OCR fallback ──────────────────────────────────────────────────────────────
try:
    import pyautogui
    import pytesseract
    from PIL import Image, ImageGrab
    OCR_AVAILABLE = True
    # Locate tesseract binary
    import os as _os
    for _tpath in [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]:
        if _os.path.exists(_tpath):
            pytesseract.pytesseract.tesseract_cmd = _tpath
            break
except ImportError:
    OCR_AVAILABLE = False

# ── Window acquisition (mirrors whatsapp_smart.py pattern exactly) ─────────────
try:
    import pygetwindow as gw
    GW_AVAILABLE = True
except ImportError:
    GW_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# WINDOW HELPERS
# ─────────────────────────────────────────────────────────────────────────────

_EXCLUDED_TITLES = [
    "chrome", "firefox", "edge", "cursor", "antigravity",
    "jarvis", "vs code", "visual studio", "notepad", "explorer",
    "brave", "devin", "regression", "issue", "bug"
]


def _get_whatsapp_window():
    """
    Finds the WhatsApp Desktop window safely.
    Mirrors the exact exclusion logic from whatsapp_smart.py.
    Returns the window object or None.
    """
    if not GW_AVAILABLE:
        return None

    try:
        # Exact title match first — safest
        for w in gw.getAllWindows():
            if w.title in ("WhatsApp", "Whatsapp"):
                return w

        # Fuzzy match — but exclude browsers, editors, Jarvis itself
        for w in gw.getAllWindows():
            t = w.title.lower()
            if "whatsapp" in t and not any(ex in t for ex in _EXCLUDED_TITLES):
                return w
    except Exception:
        pass

    return None


def _bring_whatsapp_to_front() -> bool:
    """Restores and focuses WhatsApp window. Returns True on success."""
    win = _get_whatsapp_window()
    if not win:
        return False
    try:
        if win.isMinimized:
            win.restore()
            time.sleep(0.4)
        win.activate()
        time.sleep(0.6)
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# PRIMARY: UIA TREE READER
# ─────────────────────────────────────────────────────────────────────────────

def _read_via_uia(max_messages: int = 30) -> List[Dict]:
    """
    Walks the WhatsApp UIA accessibility tree to extract messages.

    WhatsApp Desktop (Windows Store version) exposes each message bubble
    as a ListItem inside a List control. Each ListItem has a Name property
    that contains the full message text + sender + timestamp.

    Pattern for received messages: "ContactName, MessageText, TimeStamp"
    Pattern for sent messages:     "You, MessageText, TimeStamp"
    """
    if not UIA_AVAILABLE:
        return []

    messages = []

    try:
        # Find WhatsApp main window via UIA
        wa_window = auto.WindowControl(searchDepth=1, Name="WhatsApp")
        if not wa_window.Exists(maxSearchSeconds=3):
            return []

        # Walk down to the message list — WhatsApp uses a List control
        # for the chat scroll area
        message_list = wa_window.ListControl(searchDepth=10)
        if not message_list.Exists(maxSearchSeconds=2):
            return []

        items = message_list.GetChildren()
        if not items:
            return []

        # Take the last N items (most recent messages)
        recent_items = items[-max_messages:] if len(items) > max_messages else items

        for item in recent_items:
            raw = item.Name.strip()
            if not raw:
                continue

            parsed = _parse_uia_message_string(raw)
            if parsed:
                messages.append(parsed)

    except Exception:
        pass

    return messages


def _parse_uia_message_string(raw: str) -> Dict:
    """
    Parses a raw UIA ListItem Name string into a structured message dict.

    WhatsApp's UIA Name format (observed patterns):
      "You: Hello there  3:45 PM"
      "Rahul: Kya haal hai  3:44 PM"
      "You  Hey  3:43 PM"               ← older format without colon
      "Unread messages. Scroll up."      ← system message, skip
      "Today"                            ← date separator, skip

    Returns {} for system/date strings we want to skip.
    """
    # Skip known non-message strings
    skip_patterns = [
        r"^(today|yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)$",
        r"^unread message",
        r"^messages are end-to-end encrypted",
        r"^\d+ unread",
        r"^you blocked this contact",
        r"^tap to learn more",
        r"^this message was deleted",
    ]
    for pat in skip_patterns:
        if re.search(pat, raw.lower()):
            return {}

    # Try to extract timestamp (e.g. "3:45 PM" or "15:45")
    ts_match = re.search(r"\b(\d{1,2}:\d{2}\s?(?:AM|PM)?)\s*$", raw, re.IGNORECASE)
    timestamp = ts_match.group(1).strip() if ts_match else ""
    text_body = raw[: ts_match.start()].strip() if ts_match else raw

    # Determine sender
    if text_body.lower().startswith("you"):
        # Strip leading "You" or "You:" prefix
        text_body = re.sub(r"^you\s*:?\s*", "", text_body, flags=re.IGNORECASE).strip()
        sender = "you"
    else:
        # Everything before first colon is sender name
        colon_idx = text_body.find(":")
        if colon_idx != -1:
            sender = "them"
            text_body = text_body[colon_idx + 1:].strip()
        else:
            sender = "them"

    if not text_body:
        return {}

    return {
        "sender": sender,
        "text": text_body,
        "timestamp": timestamp,
    }


# ─────────────────────────────────────────────────────────────────────────────
# FALLBACK: OCR READER
# ─────────────────────────────────────────────────────────────────────────────

def _read_via_ocr(max_messages: int = 20) -> List[Dict]:
    """
    Screenshot-based OCR fallback.
    Crops the right 65% of the WhatsApp window (chat panel only),
    runs Tesseract, and heuristically splits into messages.

    Less accurate than UIA but works even when accessibility tree
    is partially broken or the UIA version mismatches.
    """
    if not OCR_AVAILABLE:
        return []

    try:
        win = _get_whatsapp_window()
        if not win:
            return []

        # Crop to chat panel only (right 65% of window)
        left = win.left + int(win.width * 0.35)
        top = win.top
        right = win.left + win.width
        bottom = win.top + win.height

        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        # Upscale for better OCR accuracy
        w, h = screenshot.size
        screenshot = screenshot.resize((w * 2, h * 2), Image.LANCZOS)

        raw_text = pytesseract.image_to_string(screenshot, config="--psm 6")

        lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
        messages = _heuristic_parse_ocr_lines(lines, max_messages)

        return messages

    except Exception:
        return []


def _heuristic_parse_ocr_lines(lines: List[str], max_messages: int) -> List[Dict]:
    """
    Turns raw OCR lines into message dicts.
    Heuristic: a line ending with a time pattern (e.g. 3:45 PM) is a
    message boundary. Lines above it are that message's text.
    """
    messages = []
    buffer = []

    ts_pattern = re.compile(r"\b\d{1,2}:\d{2}\s?(?:AM|PM)?\s*$", re.IGNORECASE)

    for line in lines:
        buffer.append(line)
        if ts_pattern.search(line):
            full_text = " ".join(buffer).strip()
            ts_match = ts_pattern.search(full_text)
            timestamp = ts_match.group(0).strip() if ts_match else ""
            text_body = full_text[: ts_match.start()].strip() if ts_match else full_text

            # Very rough sender detection: short left-aligned lines after a gap
            # are usually received; we default to "them" for OCR path
            messages.append({
                "sender": "them",
                "text": text_body,
                "timestamp": timestamp,
            })
            buffer = []

    # Leftover buffer with no timestamp
    if buffer:
        text_body = " ".join(buffer).strip()
        if text_body:
            messages.append({"sender": "them", "text": text_body, "timestamp": ""})

    return messages[-max_messages:]


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def read_messages(max_messages: int = 30) -> List[Dict]:
    """
    Main entry point. Tries UIA first, falls back to OCR.

    Args:
        max_messages: How many recent messages to return (default 30).

    Returns:
        List of message dicts: [{"sender": ..., "text": ..., "timestamp": ...}]
        Empty list on total failure.
    """
    if not _bring_whatsapp_to_front():
        return []

    # Try UIA first
    if UIA_AVAILABLE:
        messages = _read_via_uia(max_messages)
        if messages:
            return messages

    # OCR fallback
    if OCR_AVAILABLE:
        messages = _read_via_ocr(max_messages)
        if messages:
            return messages

    return []


def read_messages_as_string(max_messages: int = 30) -> str:
    """
    Tool-registry-friendly wrapper. Returns a human-readable string.
    Called by tools.py entry point.
    """
    try:
        messages = read_messages(max_messages)
        if not messages:
            return "Could not read messages. Make sure WhatsApp is open and a chat is active."

        lines = []
        for i, msg in enumerate(messages, 1):
            ts = f" [{msg['timestamp']}]" if msg["timestamp"] else ""
            prefix = "You" if msg["sender"] == "you" else "Them"
            lines.append(f"{i}. {prefix}{ts}: {msg['text']}")

        return "\n".join(lines)

    except Exception as e:
        return f"Message reader error: {str(e)}"
