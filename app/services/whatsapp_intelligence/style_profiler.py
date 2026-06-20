"""
style_profiler.py — Jarvis WhatsApp Intelligence: Style Profiler
=================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

PURPOSE:
    Builds a living JSON profile of how YOU communicate on WhatsApp.
    Two learning mechanisms:
      1. One-time training: parse a WhatsApp .txt chat export
      2. Ongoing learning:  every reply you send through Jarvis
                            is appended to your example history

PROFILE SCHEMA:
    {
        "avg_reply_length":    12,          ← words per reply
        "hinglish_ratio":      0.4,         ← 0.0 = full English, 1.0 = full Hindi
        "common_fillers":      ["okay so", "bhai", "haan"],
        "emoji_frequency":     0.15,        ← fraction of messages with emoji
        "punctuation_style":   "no_period", ← "normal" | "no_period" | "minimal"
        "formal_contacts":     ["boss_name"],
        "deflection_phrases":  ["dekh lete hai", "abhi busy hun"],
        "reply_examples":      [            ← raw examples for few-shot LLM
            {"their_msg": "...", "your_reply": "..."},
            ...
        ],
        "last_updated":        "2025-01-01T12:00:00"
    }

STORAGE:
    style_profiles/default.json             ← your global style
    style_profiles/per_contact/<name>.json  ← contact-specific override
"""

import os
import re
import json
import datetime
from typing import List, Dict, Optional
from collections import Counter

# ─────────────────────────────────────────────────────────────────────────────
# PATHS  (relative to this file, not the Jarvis root — keeps it isolated)
# ─────────────────────────────────────────────────────────────────────────────

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROFILES_DIR = os.path.join(_THIS_DIR, "style_profiles")
_PER_CONTACT_DIR = os.path.join(_PROFILES_DIR, "per_contact")
_DEFAULT_PROFILE_PATH = os.path.join(_PROFILES_DIR, "default.json")

os.makedirs(_PER_CONTACT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# EMPTY PROFILE TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────

def _empty_profile() -> Dict:
    return {
        "avg_reply_length": 10,
        "hinglish_ratio": 0.3,
        "common_fillers": [],
        "emoji_frequency": 0.1,
        "punctuation_style": "no_period",
        "formal_contacts": [],
        "deflection_phrases": [],
        "reply_examples": [],
        "last_updated": _now(),
    }


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


# ─────────────────────────────────────────────────────────────────────────────
# LOAD / SAVE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _load_profile(contact_name: Optional[str] = None) -> Dict:
    """
    Loads the style profile for a contact (falls back to default).
    If neither exists, returns a blank template.
    """
    if contact_name:
        safe_name = _safe_filename(contact_name)
        contact_path = os.path.join(_PER_CONTACT_DIR, f"{safe_name}.json")
        if os.path.exists(contact_path):
            try:
                with open(contact_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    if os.path.exists(_DEFAULT_PROFILE_PATH):
        try:
            with open(_DEFAULT_PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return _empty_profile()


def _save_profile(profile: Dict, contact_name: Optional[str] = None) -> bool:
    """
    Saves the profile to the correct path.
    Returns True on success.
    """
    profile["last_updated"] = _now()

    if contact_name:
        safe_name = _safe_filename(contact_name)
        path = os.path.join(_PER_CONTACT_DIR, f"{safe_name}.json")
    else:
        path = _DEFAULT_PROFILE_PATH

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _safe_filename(name: str) -> str:
    """Converts a contact name to a safe filename."""
    return re.sub(r"[^\w\-]", "_", name.strip().lower())


# ─────────────────────────────────────────────────────────────────────────────
# CHAT EXPORT PARSER (.txt format from WhatsApp)
# ─────────────────────────────────────────────────────────────────────────────

def _parse_whatsapp_export(file_path: str, your_name: str) -> List[Dict]:
    """
    Parses a WhatsApp .txt chat export and extracts YOUR messages
    paired with the preceding message from the other person.

    WhatsApp export format:
      "12/25/24, 3:45 PM - ContactName: Message text here"
      "12/25/24, 3:46 PM - Aryan: My reply here"

    Returns list of {"their_msg": str, "your_reply": str} pairs.
    """
    if not os.path.exists(file_path):
        return []

    # Pattern: date/time - sender: message
    # Handles both 12h (3:45 PM) and 24h (15:45) formats and DD/MM/YY or MM/DD/YY
    line_pattern = re.compile(
        r"^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s?(?:AM|PM)?\s+[-–]\s+(.+?):\s+(.+)$",
        re.IGNORECASE
    )

    raw_messages = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                m = line_pattern.match(line)
                if m:
                    sender = m.group(1).strip()
                    text = m.group(2).strip()
                    # Skip system messages
                    if text in ["<Media omitted>", "This message was deleted",
                                "null", "image omitted", "video omitted",
                                "audio omitted", "sticker omitted", "GIF omitted"]:
                        continue
                    raw_messages.append({"sender": sender, "text": text})
    except Exception:
        return []

    # Extract pairs: (their_msg → your_reply)
    pairs = []
    for i, msg in enumerate(raw_messages):
        if msg["sender"].lower() == your_name.lower() and i > 0:
            prev = raw_messages[i - 1]
            if prev["sender"].lower() != your_name.lower():
                pairs.append({
                    "their_msg": prev["text"],
                    "your_reply": msg["text"]
                })

    return pairs


def _compute_profile_stats(pairs: List[Dict]) -> Dict:
    """
    Computes statistical features from your reply examples.
    """
    if not pairs:
        return _empty_profile()

    your_replies = [p["your_reply"] for p in pairs]

    # Average reply length in words
    lengths = [len(r.split()) for r in your_replies]
    avg_length = round(sum(lengths) / len(lengths), 1)

    # Hinglish ratio: presence of common Hindi/Hinglish words
    hindi_markers = [
        "hai", "hain", "kya", "nahi", "bhai", "yaar", "haan",
        "nope", "theek", "kal", "abhi", "bilkul", "dekh", "sab",
        "toh", "aur", "mera", "tera", "uska", "ye", "wo", "kuch",
        "matlab", "accha", "bas", "thoda", "bahut", "bohot", "yar",
        "chal", "ruk", "agar", "lekin", "phir", "aaja", "bata",
    ]
    hinglish_count = sum(
        1 for r in your_replies
        if any(w in r.lower().split() for w in hindi_markers)
    )
    hinglish_ratio = round(hinglish_count / len(your_replies), 2)

    # Emoji frequency
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        "\u2600-\u26FF\u2700-\u27BF]+",
        flags=re.UNICODE
    )
    emoji_count = sum(1 for r in your_replies if emoji_pattern.search(r))
    emoji_frequency = round(emoji_count / len(your_replies), 2)

    # Punctuation style
    period_count = sum(1 for r in your_replies if r.strip().endswith("."))
    if period_count / len(your_replies) < 0.2:
        punctuation_style = "no_period"
    elif period_count / len(your_replies) > 0.6:
        punctuation_style = "normal"
    else:
        punctuation_style = "minimal"

    # Common filler bigrams (appearing 3+ times)
    all_words = " ".join(your_replies).lower().split()
    bigrams = [f"{all_words[i]} {all_words[i+1]}" for i in range(len(all_words) - 1)]
    bigram_counts = Counter(bigrams)
    fillers = [phrase for phrase, count in bigram_counts.most_common(10) if count >= 3]

    # Keep only last 50 examples (enough for few-shot, not too large)
    examples = pairs[-50:] if len(pairs) > 50 else pairs

    return {
        "avg_reply_length": avg_length,
        "hinglish_ratio": hinglish_ratio,
        "common_fillers": fillers[:5],
        "emoji_frequency": emoji_frequency,
        "punctuation_style": punctuation_style,
        "formal_contacts": [],
        "deflection_phrases": [],
        "reply_examples": examples,
        "last_updated": _now(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# ONGOING LEARNING
# ─────────────────────────────────────────────────────────────────────────────

def record_sent_reply(
    their_message: str,
    your_reply: str,
    contact_name: Optional[str] = None
) -> bool:
    """
    Called every time you send a reply through Jarvis.
    Appends the example to your style history so the profile improves over time.

    Args:
        their_message: The message you were replying to.
        your_reply:    The reply you sent (or approved).
        contact_name:  If provided, also updates the contact-specific profile.
    """
    try:
        new_example = {"their_msg": their_message, "your_reply": your_reply}

        # Update default profile
        default_profile = _load_profile()
        default_profile["reply_examples"].append(new_example)
        # Cap at 100 examples to keep the file lean
        if len(default_profile["reply_examples"]) > 100:
            default_profile["reply_examples"] = default_profile["reply_examples"][-100:]
        _save_profile(default_profile, contact_name=None)

        # Update contact-specific profile if name given
        if contact_name:
            contact_profile = _load_profile(contact_name)
            contact_profile["reply_examples"].append(new_example)
            if len(contact_profile["reply_examples"]) > 50:
                contact_profile["reply_examples"] = contact_profile["reply_examples"][-50:]
            _save_profile(contact_profile, contact_name=contact_name)

        return True
    except Exception:
        return False


def mark_contact_formal(contact_name: str) -> str:
    """Marks a contact as formal so replies use a more professional tone."""
    try:
        profile = _load_profile()
        if contact_name not in profile["formal_contacts"]:
            profile["formal_contacts"].append(contact_name)
            _save_profile(profile)
            return f"{contact_name} marked as formal contact. Replies will be more professional."
        return f"{contact_name} is already marked as formal."
    except Exception as e:
        return f"Could not update formal contacts: {str(e)}"


def add_deflection_phrase(phrase: str) -> str:
    """
    Adds a personal deflection phrase to your style profile.
    e.g. "dekh lete hai", "abhi busy hun"
    """
    try:
        profile = _load_profile()
        if phrase not in profile["deflection_phrases"]:
            profile["deflection_phrases"].append(phrase)
            _save_profile(profile)
            return f"Added deflection phrase: '{phrase}'"
        return f"'{phrase}' is already in your deflection phrases."
    except Exception as e:
        return f"Could not add deflection phrase: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def build_style_profile(chat_export_path: str, your_name: str = "You") -> str:
    """
    Tool-registry entry point.
    One-time training: parses a WhatsApp .txt export and saves the profile.

    Args:
        chat_export_path: Full path to the exported .txt file.
        your_name:        Your name as it appears in the chat export.

    Returns:
        Human-readable result string.
    """
    try:
        if not os.path.exists(chat_export_path):
            return f"File not found: {chat_export_path}"

        pairs = _parse_whatsapp_export(chat_export_path, your_name)
        if not pairs:
            return (
                f"Could not extract your messages from the export. "
                f"Make sure your name in the file matches '{your_name}'."
            )

        profile = _compute_profile_stats(pairs)
        success = _save_profile(profile)

        if success:
            return (
                f"Style profile built from {len(pairs)} message pairs.\n"
                f"  Avg reply length: {profile['avg_reply_length']} words\n"
                f"  Hinglish ratio: {int(profile['hinglish_ratio'] * 100)}%\n"
                f"  Emoji frequency: {int(profile['emoji_frequency'] * 100)}%\n"
                f"  Punctuation style: {profile['punctuation_style']}\n"
                f"  Common fillers: {', '.join(profile['common_fillers']) or 'none detected'}\n"
                f"Profile saved to: {_DEFAULT_PROFILE_PATH}\n"
                f"Jarvis will now reply like you."
            )
        else:
            return "Profile computed but could not be saved. Check file permissions."

    except Exception as e:
        return f"Style profiler error: {str(e)}"


def get_profile(contact_name: Optional[str] = None) -> Dict:
    """
    Returns the loaded style profile dict.
    Used internally by reply_generator.py.
    """
    return _load_profile(contact_name)


def get_profile_summary(contact_name: Optional[str] = None) -> str:
    """Returns a human-readable summary of the current style profile."""
    try:
        profile = _load_profile(contact_name)
        label = f"for {contact_name}" if contact_name else "(default)"
        return (
            f"Style profile {label}:\n"
            f"  Avg reply length: {profile['avg_reply_length']} words\n"
            f"  Hinglish ratio: {int(profile['hinglish_ratio'] * 100)}%\n"
            f"  Emoji frequency: {int(profile['emoji_frequency'] * 100)}%\n"
            f"  Punctuation: {profile['punctuation_style']}\n"
            f"  Formal contacts: {', '.join(profile['formal_contacts']) or 'none'}\n"
            f"  Deflection phrases: {', '.join(profile['deflection_phrases']) or 'none'}\n"
            f"  Examples in memory: {len(profile['reply_examples'])}\n"
            f"  Last updated: {profile['last_updated']}"
        )
    except Exception as e:
        return f"Could not load profile: {str(e)}"
