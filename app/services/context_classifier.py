"""
context_classifier.py — Jarvis Situational Awareness
-----------------------------------------------------
Reads the user's input and classifies:
  - Language    (english / hinglish / hindi)
  - Urgency level  (normal / high / urgent)
  - Topic category (os_task / memory / casual_chat / general)
  - Time of day    (morning / day / evening / night)
  - Mood signal    (neutral / stressed / playful / urgent)

The output is passed to personality.get_context_aware_prompt() so Jarvis
adjusts its tone and language to fit the situation automatically.
"""

import datetime
import re


# Common Hindi/Hinglish words that signal the user is speaking Hindi
_HINDI_SIGNAL_WORDS = {
    "kya", "hai", "haan", "nahi", "kar", "karo", "mera", "meri", "mujhe",
    "aap", "tum", "yeh", "woh", "isko", "usko", "bata", "batao", "dekho",
    "suno", "jaldi", "abhi", "thoda", "bilkul", "theek", "achha", "acha",
    "kuch", "sab", "bahut", "zyada", "bhi", "toh", "lekin", "aur", "ya",
    "matlab", "shayad", "pata", "lagta", "raha", "rahi", "gaya", "gayi",
    "dena", "lena", "khelna", "jana", "aana", "baat", "kaam", "cheez",
    "yaar", "bhai", "dost", "chal", "chalo", "bol", "bolna",
    "samajh", "pehle", "baad", "phir", "fir", "waise",
    # Prepositions / conjunctions
    "mein", "pe", "par", "se", "ko", "ka", "ki", "ke", "ne",
    # Common nouns
    "gaana", "gaane", "gana", "naam", "kaam", "baat", "cheez", "jagah",
    "din", "raat", "subah", "shaam", "waqt", "time",
    # Verbs
    "kholo", "kholna", "band", "bandh", "karo", "karna", "dena", "lena",
    "chalao", "chalana", "dekhna", "sunna", "padhna", "likhna",
    "delete",   # often used in Hinglish alongside Hindi words
}


def detect_language(text: str) -> str:
    """
    Detect whether the user spoke English, Hinglish, or Hindi.

    Returns:
        'english'  — mostly English, no Hindi signal words
        'hinglish' — mix of English + Hindi signal words
        'hindi'    — heavy Hindi (>50% of words are Hindi signal words)
    """
    # Devanagari present — pure Hindi
    if re.search(r'[\u0900-\u097F]', text):
        return 'hindi'

    words = re.findall(r'[a-zA-Z]+', text.lower())
    # Remove the wake word from consideration
    words = [w for w in words if w not in ('jarvis', 'hey', 'ok', 'okay', 'hi')]

    if not words:
        return 'english'

    hindi_count = sum(1 for w in words if w in _HINDI_SIGNAL_WORDS)
    ratio = hindi_count / len(words)

    if ratio >= 0.45:
        return 'hindi'
    elif ratio >= 0.12:   # even 1 Hindi word in a 8-word sentence = hinglish
        return 'hinglish'
    return 'english'


def classify_context(user_input: str) -> dict:
    """
    Classify the situation from user input.

    Returns a dict with keys:
        urgency    : "normal" | "high" | "urgent"
        topic      : "os_task" | "memory" | "casual_chat" | "general"
        time_of_day: "morning" | "day" | "evening" | "night"
        hour       : int (0-23)
        mood       : "neutral" | "stressed" | "playful" | "urgent"
    """
    text = user_input.lower().strip()
    now  = datetime.datetime.now()
    hour = now.hour

    # ── Time of day ──────────────────────────────────────────────────────────
    if 22 <= hour or hour < 6:
        time_of_day = "night"
    elif hour < 9:
        time_of_day = "morning"
    elif hour < 18:
        time_of_day = "day"
    else:
        time_of_day = "evening"

    # ── Urgency ──────────────────────────────────────────────────────────────
    urgency_high_kw = [
        "jaldi", "quick", "fast", "asap", "urgent", "abhi", "right now",
        "immediately", "hurry", "now", "quickly", "emergency", "fast karo",
    ]
    urgency_normal_kw = ["please", "can you", "could you", "would you"]

    urgency = "normal"
    if any(w in text for w in urgency_high_kw):
        urgency = "high"
    # If the sentence is a very short imperative (<5 words), treat as high urgency
    if urgency == "normal" and len(text.split()) <= 4 and not any(w in text for w in urgency_normal_kw):
        urgency = "high"

    # ── Topic ────────────────────────────────────────────────────────────────
    os_task_kw = [
        "open", "close", "snap", "click", "type", "search", "volume",
        "screenshot", "minimize", "maximize", "file", "folder", "download",
        "install", "run", "play", "pause", "next", "previous", "spotify",
        "chrome", "notepad", "word", "excel",
    ]
    memory_kw   = ["remind", "note", "remember", "save", "schedule", "calendar"]
    chat_kw     = [
        "kya hal", "kya chal", "how are", "how r u", "baat karo", "hello",
        "hi jarvis", "hey jarvis", "what's up", "sup", "kya haal", "theek ho",
        "sab theek", "kuch nahi", "bored", "mood", "feeling",
    ]

    topic = "general"
    if any(w in text for w in chat_kw):
        topic = "casual_chat"
    elif any(w in text for w in memory_kw):
        topic = "memory"
    elif any(w in text for w in os_task_kw):
        topic = "os_task"

    # ── Mood detection ───────────────────────────────────────────────────────
    stressed_kw = [
        "ugh", "argh", "not working", "broken", "crashed", "error", "failed",
        "doesn't work", "won't", "help", "stuck", "lost", "confused", "damn",
        "shit", "oh no", "oh god", "seriously", "why is", "why isn't",
        "ugh yaar", "kya hai yeh", "kuch nahi ho raha",
    ]
    playful_kw = [
        "haha", "lol", "lmao", "😂", "😄", "nice", "cool", "awesome",
        "amazing", "wow", "great", "fun", "happy", "yay", "love it",
        "fantastic", "kya baat", "maza aa gaya", "solid", "noice",
    ]

    mood = "neutral"
    if urgency in ("high", "urgent"):
        mood = "urgent"
    elif any(w in text for w in stressed_kw):
        mood = "stressed"
    elif any(w in text for w in playful_kw):
        mood = "playful"

    return {
        "urgency":     urgency,
        "topic":       topic,
        "time_of_day": time_of_day,
        "hour":        hour,
        "mood":        mood,
        "language":    detect_language(text),
    }
