"""
ssml_processor.py — Human Prosody Pre-processor
-------------------------------------------------
Transforms plain text into natural-sounding speech by adding:
  - Breathing pauses at commas and sentence ends
  - Pauses before Hinglish connector words (lekin, toh, matlab…)
  - Slight emphasis on action confirmation words (done, ready, error…)
  - Speed-up for filler transitions (Theek hai, Bilkul, Haan…)

ElevenLabs supports a subset of SSML tags. This processor uses only
the supported ones: <break>, <emphasis>, <prosody>.

For edge-tts fallback: SSML tags are stripped cleanly so it still works.
"""

import re


# ── Words that get a pause before them (Hinglish rhythm) ────────────────────
_HINGLISH_PAUSE_WORDS = [
    "lekin", "par", "toh", "matlab", "actually", "basically", "anyway",
    "aur", "phir", "waise", "dekho", "suno", "yaar", "haan", "nahi",
    "shayad", "abhi", "bas", "acha", "theek hai",
]

# ── Words that get emphasis (action confirmations / alerts) ──────────────────
_EMPHASIS_WORDS = [
    "done", "complete", "completed", "ready", "warning", "alert",
    "error", "found", "saved", "sent", "opened", "closed", "deleted",
    "failed", "success", "ho gaya", "mil gaya", "kar diya",
]

# ── Filler transitions that should be spoken slightly faster ─────────────────
_FAST_PHRASES = [
    "Theek hai", "Bilkul", "Haan", "Sure", "Of course",
    "Got it", "On it", "Right", "Okay", "Alright", "Chalo",
]


def add_human_prosody(text: str, use_ssml: bool = True) -> str:
    """
    Add natural speech prosody to plain text.

    Args:
        text:     Plain text (already normalized, no Devanagari).
        use_ssml: If True, wraps output in SSML <speak> tags for ElevenLabs.
                  If False, returns clean text (for edge-tts).

    Returns:
        SSML string ready for ElevenLabs, or plain text for edge-tts.
    """
    if not text or not text.strip():
        return text

    # ── 1. Comma pauses ──────────────────────────────────────────────────────
    text = re.sub(r',(\s)', r", <break time='120ms'/>\1", text)

    # ── 2. Sentence-end pauses ───────────────────────────────────────────────
    text = re.sub(r'\.(\s+)', r'. <break time="280ms"/>\1', text)
    text = re.sub(r'!(\s+)', r'! <break time="250ms"/>\1', text)
    text = re.sub(r'\?(\s+)', r'? <break time="300ms"/>\1', text)

    # ── 3. Hinglish connector word pauses ───────────────────────────────────
    for word in _HINGLISH_PAUSE_WORDS:
        text = re.sub(
            rf'\b({re.escape(word)})\b',
            r"<break time='160ms'/>\1",
            text,
            flags=re.IGNORECASE,
            count=2,   # Only first two occurrences per response to avoid over-pausing
        )

    # ── 4. Emphasize action confirmation words ───────────────────────────────
    for word in _EMPHASIS_WORDS:
        text = re.sub(
            rf'\b({re.escape(word)})\b',
            r'<emphasis level="moderate">\1</emphasis>',
            text,
            flags=re.IGNORECASE,
            count=1,   # One emphasis per word keeps it natural
        )

    # ── 5. Speed up filler/transition phrases ────────────────────────────────
    for phrase in _FAST_PHRASES:
        text = text.replace(
            phrase,
            f'<prosody rate="105%">{phrase}</prosody>',
        )

    if use_ssml:
        return f"<speak>{text}</speak>"
    return text


def strip_ssml(text: str) -> str:
    """
    Remove all SSML tags from text — used when falling back to edge-tts
    which does not support SSML.
    """
    return re.sub(r'<[^>]+>', '', text).strip()
