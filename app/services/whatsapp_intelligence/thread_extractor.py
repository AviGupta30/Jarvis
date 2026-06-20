"""
thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor
=====================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

PURPOSE:
    Sits on top of message_reader.py.
    Adds contact-name awareness, groups messages into turns,
    identifies the LATEST incoming message that needs a reply,
    and returns a clean thread summary ready for the LLM.

OUTPUT FORMAT (dict):
    {
        "contact":          "Mom",
        "latest_incoming":  "kab aa raha hai?",
        "thread": [
            {"sender": "them", "text": "...", "timestamp": "3:44 PM"},
            {"sender": "you",  "text": "...", "timestamp": "3:45 PM"},
            ...
        ],
        "needs_reply": True,
        "message_count": 8
    }
"""

import time
import re
from typing import List, Dict, Optional

try:
    import pyperclip
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pygetwindow as gw
    GW_AVAILABLE = True
except ImportError:
    GW_AVAILABLE = False

# Internal import — only from within this package
from whatsapp_intelligence.message_reader import read_messages, _bring_whatsapp_to_front


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

def _open_contact_chat(contact_name: str) -> bool:
    """
    Opens a specific contact's chat using Ctrl+N → paste → Enter.
    Mirrors the exact flow from whatsapp_smart.py for consistency.
    Returns True if navigation succeeded.
    """
    if not PYAUTOGUI_AVAILABLE:
        return False

    if not _bring_whatsapp_to_front():
        return False

    try:
        time.sleep(0.3)

        # Press Escape first to clear any stray state
        pyautogui.press("escape")
        time.sleep(0.2)

        # Open new chat search (same hotkey used in whatsapp_smart.py)
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.8)

        # Paste contact name via clipboard (handles unicode, emojis, Hindi names)
        pyperclip.copy(contact_name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1.5)  # Wait for search results to populate

        # Select first result and open
        pyautogui.press("down")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(1.0)

        return True

    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# THREAD EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def _get_current_chat_title() -> str:
    """
    Tries to read the active chat's contact name from the WhatsApp window title.
    WhatsApp Desktop usually sets the title to: "ContactName - WhatsApp"
    Returns empty string if it can't determine.
    """
    if not GW_AVAILABLE:
        return ""

    try:
        for w in gw.getAllWindows():
            if " - WhatsApp" in w.title:
                return w.title.replace(" - WhatsApp", "").strip()
    except Exception:
        pass

    return ""


def _group_into_turns(messages: List[Dict]) -> List[Dict]:
    """
    Merges consecutive messages from the same sender into a single turn.
    This makes the thread cleaner for LLM context.

    Input:  [{"sender":"them","text":"Hey"},{"sender":"them","text":"Kya haal?"}]
    Output: [{"sender":"them","text":"Hey Kya haal?","timestamp":"..."}]
    """
    if not messages:
        return []

    grouped = []
    current = dict(messages[0])

    for msg in messages[1:]:
        if msg["sender"] == current["sender"]:
            current["text"] += " " + msg["text"]
            if msg["timestamp"]:
                current["timestamp"] = msg["timestamp"]   # keep latest timestamp
        else:
            grouped.append(current)
            current = dict(msg)

    grouped.append(current)
    return grouped


def _find_latest_incoming(thread: List[Dict]) -> Optional[str]:
    """
    Scans the thread from the end to find the most recent message
    from 'them' — this is what we need to reply to.
    Returns None if the last message is from 'you' (no pending reply needed).
    """
    for msg in reversed(thread):
        if msg["sender"] == "them":
            return msg["text"]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def extract_thread(contact_name: str, n_messages: int = 20) -> Dict:
    """
    Main entry point. Opens the contact's chat and extracts a structured thread.

    Args:
        contact_name: Name as saved in WhatsApp (e.g. "Mom", "Rahul Bhai").
        n_messages:   How many recent messages to read (default 20).

    Returns:
        Thread dict (see module docstring). On failure returns error dict.
    """
    try:
        # Navigate to the contact
        success = _open_contact_chat(contact_name)
        if not success:
            return {
                "error": f"Could not open chat with {contact_name}.",
                "contact": contact_name,
                "thread": [],
                "needs_reply": False,
                "message_count": 0,
            }

        # Small wait for messages to render after navigation
        time.sleep(0.5)

        # Read raw messages
        raw_messages = read_messages(max_messages=n_messages)
        if not raw_messages:
            return {
                "error": "Chat opened but no messages could be read.",
                "contact": contact_name,
                "thread": [],
                "needs_reply": False,
                "message_count": 0,
            }

        # Group consecutive messages from same sender
        thread = _group_into_turns(raw_messages)

        # Find if there's a pending incoming message to reply to
        latest_incoming = _find_latest_incoming(thread)
        needs_reply = latest_incoming is not None

        return {
            "contact": contact_name,
            "latest_incoming": latest_incoming or "",
            "thread": thread,
            "needs_reply": needs_reply,
            "message_count": len(thread),
        }

    except Exception as e:
        return {
            "error": f"Thread extraction failed: {str(e)}",
            "contact": contact_name,
            "thread": [],
            "needs_reply": False,
            "message_count": 0,
        }


def extract_thread_as_string(contact_name: str, n_messages: int = 20) -> str:
    """
    Tool-registry-friendly wrapper. Returns human-readable string.
    Called by tools.py entry point: read_whatsapp_thread()
    """
    try:
        result = extract_thread(contact_name, n_messages)

        if "error" in result and result["error"]:
            return result["error"]

        if not result["thread"]:
            return f"No messages found in chat with {contact_name}."

        lines = [f"Chat with {contact_name} (last {result['message_count']} turns):\n"]

        for msg in result["thread"]:
            ts = f" [{msg['timestamp']}]" if msg.get("timestamp") else ""
            who = "You" if msg["sender"] == "you" else contact_name
            lines.append(f"  {who}{ts}: {msg['text']}")

        if result["needs_reply"]:
            lines.append(f"\n⟶ Latest message from {contact_name}: \"{result['latest_incoming']}\"")
            lines.append("  (Reply needed)")
        else:
            lines.append("\n  (Your last message — no reply pending)")

        return "\n".join(lines)

    except Exception as e:
        return f"Thread extractor error: {str(e)}"
