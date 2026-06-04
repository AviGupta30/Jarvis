"""
hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer
-----------------------------------------------------------------------
The TTS engine (edge-tts or ElevenLabs) CANNOT handle Devanagari script.
This module:
  1. Converts common Devanagari words/phrases to their Romanized equivalents
  2. Strips any remaining Devanagari characters (Unicode block U+0900–U+097F)
  3. Cleans up markdown artifacts (bold, italic, code blocks) before TTS
"""

import re

# ── Devanagari → Romanized Hinglish lookup table ────────────────────────────
DEVANAGARI_TO_ROMAN: dict[str, str] = {
    # Greetings / Acknowledgements
    "नमस्ते":          "Namaste",
    "नमस्कार":         "Namaskar",
    "ठीक है":          "Theek hai",
    "ठीक हैं":         "Theek hain",
    "बिल्कुल":         "Bilkul",
    "हाँ":             "Haan",
    "हां":             "Haan",
    "नहीं":            "Nahi",
    "क्या":            "Kya",
    "कैसे":            "Kaise",
    "अच्छा":           "Achha",
    "जल्दी":           "Jaldi",
    "समझ गया":         "Samajh gaya",
    "काम हो गया":      "Kaam ho gaya",
    "हो गया":          "Ho gaya",
    "कोई बात नहीं":    "Koi baat nahi",
    "थोड़ा रुको":       "Thoda ruko",
    "शुक्रिया":         "Shukriya",
    "धन्यवाद":          "Dhanyavaad",
    "माफ़ कीजिए":       "Maaf kijiye",
    "सॉरी":            "Sorry",
    "चलो":             "Chalo",
    "चलिए":            "Chaliye",
    "देखो":             "Dekho",
    "सुनो":             "Suno",
    "यार":             "Yaar",
    "दोस्त":           "Dost",
    "भाई":             "Bhai",
    "सर":              "Sir",
    "अभी":             "Abhi",
    "बाद में":          "Baad mein",
    "पहले":            "Pehle",
    "अब":              "Ab",
    "फिर":             "Phir",
    "लेकिन":           "Lekin",
    "लेकिन नहीं":      "Lekin nahi",
    "मतलब":            "Matlab",
    "शायद":            "Shayad",
    "सच में":          "Sach mein",
    "बस":              "Bas",
    "और":              "Aur",
    "कर दो":           "Kar do",
    "कर दिया":         "Kar diya",
    "कर रहा हूँ":      "Kar raha hoon",
    "देख रहा हूँ":     "Dekh raha hoon",
    "पता नहीं":        "Pata nahi",
    "लग रहा है":       "Lag raha hai",
    "हो रहा है":       "Ho raha hai",
    "मिल गया":         "Mil gaya",
    "नहीं मिला":       "Nahi mila",
    "सब ठीक है":       "Sab theek hai",
    "क्या हुआ":        "Kya hua",
    "कोई समस्या नहीं": "Koi samasya nahi",
    "रुकिए":           "Rukiye",
    "एक सेकंड":        "Ek second",
    "एक मिनट":         "Ek minute",
}


def normalize_for_tts(text: str) -> str:
    """
    Transform text so it's safe and natural-sounding for TTS:
      1. Replace known Devanagari phrases with Romanized equivalents
      2. Strip any remaining Devanagari characters
      3. Clean markdown (bold, italic, code fences, headers)
      4. Normalize whitespace

    This must run BEFORE text is sent to any TTS engine.
    """
    # Step 1: Replace known Devanagari phrases (longest-first to avoid partial hits)
    for devanagari, roman in sorted(DEVANAGARI_TO_ROMAN.items(), key=lambda x: -len(x[0])):
        text = text.replace(devanagari, roman)

    # Step 2: Strip remaining Devanagari characters (U+0900–U+097F)
    text = re.sub(r'[\u0900-\u097F]+', '', text)

    # Step 3: Clean markdown artifacts
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)   # code blocks
    text = re.sub(r'`[^`]*`', '', text)                        # inline code
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)            # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)                 # italic
    text = re.sub(r'__([^_]+)__', r'\1', text)                 # underline
    text = re.sub(r'_([^_]+)_', r'\1', text)                   # italic
    text = re.sub(r'~~([^~]+)~~', r'\1', text)                 # strikethrough
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE) # headers
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)      # links [text](url)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # bullet points
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # numbered lists

    # Step 4: Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
