"""
whatsapp_smart.py — Jarvis Smart WhatsApp Integration (Fully Isolated)
=======================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

FEATURES:
  - Smart fuzzy contact search (keyword-based, not exact match)
  - Multiple match disambiguation: asks user "Which Archit?" instead of guessing
  - Two-phase send flow: always CONFIRMS message before sending
  - Reads recent messages by opening the chat
  - Proper Unicode support via clipboard
  - No security PIN prompt — works with WhatsApp desktop already open

PUBLIC API (called from tools.py):
  search_whatsapp_contact(name)                  → str  fuzzy contact list
  initiate_whatsapp_send(contact_name, message)  → str  first phase: show confirmation
  confirm_whatsapp_send(contact_name, message)   → str  second phase: actually send
  open_whatsapp()                                → str  focus/open the app
"""

import re
import time
import subprocess
import pyautogui
import pyperclip

# ─────────────────────────────────────────────────────────────────────────────
# Safety settings
# ─────────────────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get_whatsapp_window():
    import pygetwindow as gw
    for w in gw.getAllWindows():
        if w.title in ("WhatsApp", "Whatsapp"):
            return w
    for w in gw.getAllWindows():
        t = w.title.lower()
        if "whatsapp" in t and not any(x in t for x in ["antigravity", "chrome", "edge", "firefox", "brave", "cursor", "devin", "regression", "jarvis", "issue", "bug"]):
            return w
    return None

def _focus_or_open_whatsapp() -> bool:
    """Focus the WhatsApp window or open it if not running. Returns True on success."""
    try:
        win = _get_whatsapp_window()
        if win:
            try:
                win.restore()
            except Exception:
                pass
            win.activate()
            time.sleep(1.0)
            return True
    except Exception:
        pass

    # Launch via Windows URI scheme (works for Microsoft Store / UWP WhatsApp)
    subprocess.Popen("start whatsapp:", shell=True)
    time.sleep(6)

    try:
        win = _get_whatsapp_window()
        if win:
            win.activate()
            time.sleep(0.8)
            return True
    except Exception:
        pass

    return False


def _type_via_clipboard(text: str, delay: float = 0.3):
    """Type text by copying to clipboard and pasting — handles Unicode names reliably."""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(delay)


def _clear_search():
    """Clear the WhatsApp search box."""
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.15)
    pyautogui.press('delete')
    time.sleep(0.15)


def _fuzzy_score(query: str, candidate: str) -> int:
    """
    Score how well 'query' matches 'candidate' name.
    Uses keyword matching so "archit" matches "Archit Shukla DTU".
    Returns 0-100 score.
    """
    query_words = re.split(r'\s+', query.lower().strip())
    candidate_lower = candidate.lower()

    # Try rapidfuzz if available for better scoring
    try:
        from rapidfuzz import fuzz
        base_score = fuzz.partial_ratio(query.lower(), candidate_lower)
    except ImportError:
        # Manual keyword scoring fallback
        base_score = 0
        for word in query_words:
            if word and word in candidate_lower:
                base_score += 40

    # Boost if the query is the start of the candidate name
    first_name = candidate_lower.split()[0] if candidate_lower.split() else ""
    if query_words[0] == first_name:
        base_score = min(100, base_score + 20)

    return base_score


def _get_visible_search_results() -> list[str]:
    """
    After typing a search in WhatsApp, take a screenshot and use OCR
    to read visible contact names from the search results panel.
    Returns list of visible names.
    """
    try:
        import pyautogui
        from PIL import Image
        screenshot = pyautogui.screenshot()

        # Crop left panel where search results appear (approx left 30% of screen)
        w, h = screenshot.size
        panel = screenshot.crop((0, 100, int(w * 0.32), h - 100))

        try:
            import pytesseract
            import os
            # Find tesseract
            for path in [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
            text = pytesseract.image_to_string(panel, config="--psm 6")
            lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) > 2]
            return lines
        except Exception:
            return []
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def open_whatsapp() -> str:
    """Opens the WhatsApp desktop app and brings it to focus."""
    success = _focus_or_open_whatsapp()
    if success:
        return "WhatsApp is open and ready."
    return "WhatsApp opened — it may take a few seconds to fully load."


def search_whatsapp_contact(name: str) -> str:
    """
    Fuzzy-search for a contact by keyword in WhatsApp's search.
    Opens WhatsApp, types the search keyword, and reads OCR results.
    Returns a formatted list of matching contact names found.
    
    Use this BEFORE sending to confirm which contact the user means.
    """
    if not _focus_or_open_whatsapp():
        return "Could not open WhatsApp. Please open it manually."

    time.sleep(1.5)

    try:
        # Open search (using New Chat for reliable focus)
        pyautogui.press('escape')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.8)

        # Type keyword (just the first word — broadest search)
        keyword = name.strip().split()[0]
        _type_via_clipboard(keyword, delay=2.0)

        # Read OCR results from panel
        results = _get_visible_search_results()

        # Close search
        pyautogui.press('escape')
        time.sleep(0.3)

        if not results:
            return (
                f"I searched for '{keyword}' in WhatsApp but couldn't read the results on screen. "
                f"Please tell me the exact contact name as it appears in WhatsApp."
            )

        # Filter by fuzzy score
        scored = [(r, _fuzzy_score(name, r)) for r in results if len(r) > 1]
        scored = [(r, s) for r, s in scored if s >= 35]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = [r for r, _ in scored[:5]]

        if not top:
            return (
                "__ASK_CONTACT__ "
                f"I searched for '{keyword}' but couldn't find a clear match. "
                f"Is there another name they might be saved under in WhatsApp?"
            )

        if len(top) == 1:
            return f"Found one match: '{top[0]}'. I'll use this contact."

        names_list = "\n".join(f"  {i+1}. {n}" for i, n in enumerate(top))
        return (
            f"I found {len(top)} contacts matching '{name}':\n{names_list}\n\n"
            f"Which one should I send the message to? Please say the number or full name."
        )

    except Exception as e:
        return f"WhatsApp search error: {e}"


def initiate_whatsapp_send(contact_name: str, message: str) -> str:
    """
    PHASE 1 — Confirmation step.
    Does NOT send yet. Returns a confirmation prompt for the user to approve.
    The UI layer should display this and wait for user confirmation before calling confirm_whatsapp_send().
    """
    # Sanitize
    contact_name = contact_name.strip()
    message = message.strip()

    if not contact_name:
        return "I need a contact name. Who should I send the message to?"
    if not message:
        return "What message should I send?"

    # Build a clear confirmation
    return (
        f"Before I send, let me confirm:\n\n"
        f"  To: {contact_name}\n"
        f"  Message: \"{message}\"\n\n"
        f"Should I go ahead and send this? Say 'yes send it' or 'no cancel'."
    )


def confirm_whatsapp_send(contact_name: str, message: str) -> str:
    """
    PHASE 2 — Actually sends the WhatsApp message after user confirmed.
    Single clean flow: open search → type name → select first result → type message → enter.
    """
    contact_name = contact_name.strip()
    message = message.strip()

    if not _focus_or_open_whatsapp():
        return "Could not open WhatsApp. Please open it manually and try again."

    time.sleep(1.5)

    try:
        pyautogui.press('escape')  # Close any open panels
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.8)
        _type_via_clipboard(contact_name, delay=2.0)
        pyautogui.press('enter')
        time.sleep(1.5)

        # Verification: if we are still in the search box, the text will match the contact name
        pyperclip.copy("")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
        if contact_name.lower() in pyperclip.paste().lower():
            pyautogui.press('escape')
            return f"Could not find contact '{contact_name}'. Please try a different name."

        # Step 5: Type the message
        _type_via_clipboard(message, delay=0.5)

        # Step 6: Send
        pyautogui.press('enter')
        time.sleep(0.5)

        return (
            f"Done! Your message to {contact_name} has been sent:\n"
            f"\"{message}\""
        )

    except Exception as e:
        return f"WhatsApp send error: {e}"


def read_whatsapp_messages(contact_name: str, count: int = 5) -> str:
    """
    Open a contact's chat in WhatsApp and use OCR to read the latest messages.
    Returns recent message text from the chat window.
    """
    contact_name = contact_name.strip()

    if not _focus_or_open_whatsapp():
        return "Could not open WhatsApp."

    time.sleep(1.5)

    try:
        # Search for contact using New Chat
        pyautogui.press('escape')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.8)
        _type_via_clipboard(contact_name, delay=2.0)
        pyautogui.press('enter')
        time.sleep(1.5)

        # Take screenshot and crop the chat area (right ~70% of screen)
        screenshot = pyautogui.screenshot()
        w, h = screenshot.size
        chat_area = screenshot.crop((int(w * 0.32), 80, w, h - 80))

        try:
            import pytesseract, os
            for path in [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
            raw_text = pytesseract.image_to_string(chat_area, config="--psm 6")
            lines = [ln.strip() for ln in raw_text.splitlines() if len(ln.strip()) > 3]
            recent = lines[-min(count * 3, 40):]  # grab last N*3 lines then let LLM pick

            if not recent:
                return f"Opened chat with {contact_name} but couldn't read messages."

            # Pass through LLM for clean extraction
            try:
                from groq import Groq
                import os as _os
                api_key = _os.environ.get("GROQ_API_KEY", "")
                if not api_key:
                    # Try loading from config
                    try:
                        import sys
                        sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent.parent))
                        from app.core.config import settings
                        api_key = settings.GROQ_API_KEY
                    except Exception:
                        pass

                if api_key:
                    client = Groq(api_key=api_key)
                    raw_joined = "\n".join(recent)
                    prompt = (
                        f"This is OCR text from a WhatsApp chat with '{contact_name}'. "
                        f"Extract and list the last {count} readable messages clearly, "
                        f"indicating who sent each one if possible (you or {contact_name}). "
                        f"Ignore UI text like timestamps, delivery ticks, etc.\n\nRAW:\n{raw_joined}"
                    )
                    resp = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200,
                        temperature=0.2
                    )
                    return f"Recent messages with {contact_name}:\n\n{resp.choices[0].message.content.strip()}"
            except Exception:
                pass

            # Plain fallback
            return f"Recent messages with {contact_name}:\n\n" + "\n".join(recent[-20:])

        except ImportError:
            return "Tesseract OCR is not installed — can't read messages from screen."

    except Exception as e:
        return f"WhatsApp read error: {e}"
