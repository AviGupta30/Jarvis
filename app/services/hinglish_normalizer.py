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
    return strip_markdown(text)


def strip_markdown(text: str) -> str:
    """Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji."""
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
    text = re.sub(r'https?://\S+|www\.\S+', '', text)          # URLs are unspeakable
    text = _EMOJI_RE.sub('', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE0F\U0000200D\U00002B00-\U00002BFF]+"
)


# ═════════════════════════════════════════════════════════════════════════════
# Voice-mode script conversion
#   STT side : Devanagari transcript → romanized Hinglish (what the router/LLM expect)
#   TTS side : romanized Hinglish reply → Devanagari Hindi words (+ English kept in
#              Latin) so hi-IN neural voices pronounce Hindi natively instead of
#              reading "kya hai" with English phonetics.
# ═════════════════════════════════════════════════════════════════════════════

# English loanwords as Whisper writes them in Devanagari → proper English spelling.
# Keeps the keyword router working ("यूट्यूब पे गाना चलाओ" → "YouTube pe gaana chalao").
_LOANWORDS_DEV: dict[str, str] = {
    "जार्विस": "Jarvis", "जारविस": "Jarvis", "जार्वीस": "Jarvis", "जर्विस": "Jarvis",
    "जारवीस": "Jarvis", "जार्विज़": "Jarvis", "जार्वेस": "Jarvis", "जरविस": "Jarvis",
    "यूट्यूब": "YouTube", "यूटूब": "YouTube", "यूट्यूब़": "YouTube", "क्रोम": "Chrome",
    "गूगल": "Google", "व्हाट्सएप": "WhatsApp", "व्हाट्सऐप": "WhatsApp", "वॉट्सऐप": "WhatsApp",
    "वॉट्सएप": "WhatsApp", "व्हाट्सप्प": "WhatsApp", "स्पॉटिफाई": "Spotify", "स्पोटिफाई": "Spotify",
    "इंस्टाग्राम": "Instagram", "लिंक्डइन": "LinkedIn", "नोटपैड": "Notepad", "जीमेल": "Gmail",
    "वॉल्यूम": "volume", "वोल्यूम": "volume", "म्यूजिक": "music", "म्यूज़िक": "music",
    "वीडियो": "video", "ओपन": "open", "क्लोज़": "close", "क्लोज": "close", "प्ले": "play",
    "पॉज़": "pause", "पॉज": "pause", "स्टॉप": "stop", "नेक्स्ट": "next", "सॉन्ग": "song",
    "मैसेज": "message", "मेसेज": "message", "कॉल": "call", "ईमेल": "email", "मेल": "mail",
    "वेदर": "weather", "टाइम": "time", "अलार्म": "alarm", "रिमाइंडर": "reminder",
    "स्क्रीन": "screen", "विंडो": "window", "फाइल": "file", "फ़ाइल": "file", "फोल्डर": "folder",
    "ब्राउज़र": "browser", "ब्राउजर": "browser", "सर्च": "search", "कैलेंडर": "calendar",
    "मीटिंग": "meeting", "न्यूज़": "news", "न्यूज": "news", "पीपीटी": "PPT",
    "प्रेजेंटेशन": "presentation", "प्रेज़ेंटेशन": "presentation", "असाइनमेंट": "assignment",
    "लैपटॉप": "laptop", "ब्राइटनेस": "brightness", "बैटरी": "battery", "वाईफाई": "WiFi",
    "ब्लूटूथ": "Bluetooth", "टैब": "tab", "सिस्टम": "system", "शटडाउन": "shutdown",
    "रीस्टार्ट": "restart", "लॉक": "lock", "सेंड": "send", "टाइप": "type", "नोट": "note",
    "नोट्स": "notes", "सर": "sir", "ओके": "okay", "प्लीज़": "please", "प्लीज": "please",
    "थैंक्स": "thanks", "थैंक": "thank", "यू": "you", "हेलो": "hello", "हैलो": "hello",
    "सॉरी": "sorry", "डेस्कटॉप": "desktop", "डाउनलोड": "download", "डाउनलोड्स": "downloads",
    "अप": "up", "डाउन": "down", "ऐप": "app", "एप": "app", "चैट": "chat", "कंप्यूटर": "computer",
    "मोबाइल": "mobile", "फोन": "phone", "फ़ोन": "phone", "प्लेलिस्ट": "playlist",
    "सेटिंग्स": "settings", "मैक्सिमाइज़": "maximize", "मिनिमाइज़": "minimize",
    "स्क्रीनशॉट": "screenshot", "कैमरा": "camera", "ईमेल्स": "emails", "मेल्स": "mails",
    "द": "the", "एंड": "and", "टर्न": "turn", "ऑन": "on", "ऑफ": "off", "ऑफ़": "off", "व्हाट": "what",
    "इज़": "is", "इज": "is", "इट": "it", "प्लेय": "play", "सम": "some", "मी": "me", "माय": "my",
    "टू": "to", "फॉर": "for", "विथ": "with", "कैन": "can", "हाउ": "how", "आर": "are",
}

_DEV_VOWELS = {
    "अ": "a", "आ": "aa", "इ": "i", "ई": "ee", "उ": "u", "ऊ": "oo", "ऋ": "ri",
    "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au", "ऑ": "o", "ऍ": "e",
}
_DEV_MATRAS = {
    "ा": "aa", "ि": "i", "ी": "ee", "ु": "u", "ू": "oo", "ृ": "ri",
    "े": "e", "ै": "ai", "ो": "o", "ौ": "au", "ॉ": "o", "ॅ": "e",
}
_DEV_CONSONANTS = {
    "क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "n", "च": "ch", "छ": "chh", "ज": "j",
    "झ": "jh", "ञ": "n", "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "त": "t",
    "थ": "th", "द": "d", "ध": "dh", "न": "n", "प": "p", "फ": "ph", "ब": "b", "भ": "bh",
    "म": "m", "य": "y", "र": "r", "ल": "l", "व": "v", "श": "sh", "ष": "sh", "स": "s",
    "ह": "h", "क़": "q", "ख़": "kh", "ग़": "g", "ज़": "z", "ड़": "d", "ढ़": "dh", "फ़": "f",
}
_NUKTA_FORMS = {"क": "क़", "ख": "ख़", "ग": "ग़", "ज": "ज़", "ड": "ड़", "ढ": "ढ़", "फ": "फ़"}
_VIRAMA, _NUKTA = "्", "़"
_DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_DEV_WORD_RE = re.compile(r'[ऀ-ॿ]+')


def _translit_dev_word(word: str) -> str:
    """One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" → "karna")."""
    # Tokenise into units: [consonant, vowel_sound or None(=inherent a) or '' (virama)]
    units: list[list] = []
    i = 0
    while i < len(word):
        ch = word[i]
        if ch in _DEV_CONSONANTS or (ch in _NUKTA_FORMS and i + 1 < len(word) and word[i + 1] == _NUKTA):
            if i + 1 < len(word) and word[i + 1] == _NUKTA:
                ch = _NUKTA_FORMS.get(ch, ch)
                i += 1
            units.append([_DEV_CONSONANTS.get(ch, ""), None])
        elif ch in _DEV_MATRAS and units and units[-1][1] is None:
            units[-1][1] = _DEV_MATRAS[ch]
        elif ch == _VIRAMA and units:
            units[-1][1] = ""
        elif ch in _DEV_VOWELS:
            units.append(["", _DEV_VOWELS[ch]])
        elif ch in "ंँ":
            if units:
                v = units[-1][1]
                units[-1][1] = ("a" if v is None else v) + "n"
        elif ch == "ः":
            units.append(["h", ""])
        i += 1

    # Schwa deletion: word-final inherent 'a' is silent; medial one too in V C _ C V.
    if len(units) > 1 and units[-1][0] and units[-1][1] is None:
        units[-1][1] = ""
    for k in range(len(units) - 2, 0, -1):
        if (units[k][0] and units[k][1] is None
                and units[k - 1][1] not in ("",)
                and units[k + 1][0] and units[k + 1][1] not in ("",)):
            units[k][1] = ""
    out = "".join(c + ("a" if v is None else v) for c, v in units)
    # Casual spelling: long vowels at word end are written short ("ka", "ki", "gaya")
    out = re.sub(r'aa(?=[aeiou])', 'a', out)   # "chalaao" → "chalao"
    out = re.sub(r'aa$', 'a', out)
    out = re.sub(r'ee$', 'i', out)
    return out


def loanword_ratio(text: str) -> float:
    """Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0).
    High ratio = English speech that Whisper wrote in Devanagari."""
    words = _DEV_WORD_RE.findall(text)
    if not words:
        return 0.0
    return sum(1 for w in words if w in _LOANWORDS_DEV) / len(words)


def devanagari_to_hinglish(text: str) -> str:
    """
    Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin text.
    English loanwords are restored to their English spelling.
    """
    if not _DEV_WORD_RE.search(text):
        return text
    text = text.translate(_DEV_DIGITS).replace("।", ".").replace("॥", ".")

    def _sub(m: re.Match) -> str:
        w = m.group(0)
        if w in _LOANWORDS_DEV:
            return _LOANWORDS_DEV[w]
        if w in DEVANAGARI_TO_ROMAN:
            return DEVANAGARI_TO_ROMAN[w].lower()
        return _translit_dev_word(w)

    return _DEV_WORD_RE.sub(_sub, text)


# Romanized Hindi → Devanagari for TTS. Only unambiguous Hindi words: anything not
# listed stays in Latin script and hi-IN voices read it as (Indian-accented) English.
_HINGLISH_TO_DEV: dict[str, str] = {
    # pronouns / people
    "main": "मैं", "mai": "मैं", "mein": "में", "mujhe": "मुझे", "mujhse": "मुझसे", "mera": "मेरा",
    "meri": "मेरी", "mere": "मेरे", "hum": "हम", "hamara": "हमारा", "hamari": "हमारी",
    "aap": "आप", "aapka": "आपका", "aapki": "आपकी", "aapke": "आपके", "aapko": "आपको",
    "tum": "तुम", "tumhara": "तुम्हारा", "tumhari": "तुम्हारी", "tumhe": "तुम्हें", "tumhein": "तुम्हें",
    "tu": "तू", "tera": "तेरा", "teri": "तेरी", "yeh": "यह", "ye": "ये", "woh": "वो", "wo": "वो",
    "voh": "वो", "vo": "वो", "isko": "इसको", "usko": "उसको", "iska": "इसका", "uska": "उसका",
    "iski": "इसकी", "uski": "उसकी", "iske": "इसके", "uske": "उसके", "inhe": "इन्हें", "unhe": "उन्हें",
    "koi": "कोई", "kuch": "कुछ", "kuchh": "कुछ", "sab": "सब", "sabhi": "सभी", "sabko": "सबको",
    "apna": "अपना", "apni": "अपनी", "apne": "अपने", "khud": "खुद", "logon": "लोगों",
    "bhai": "भाई", "yaar": "यार", "dost": "दोस्त", "ji": "जी",
    # question words
    "kya": "क्या", "kyun": "क्यों", "kyon": "क्यों", "kaise": "कैसे", "kaisa": "कैसा", "kaisi": "कैसी",
    "kab": "कब", "kahan": "कहाँ", "kaha": "कहाँ", "kaun": "कौन", "kitna": "कितना", "kitni": "कितनी",
    "kitne": "कितने", "kidhar": "किधर", "konsa": "कौनसा", "kaunsa": "कौनसा",
    # be / auxiliaries
    "hai": "है", "hain": "हैं", "hoon": "हूँ", "hu": "हूँ", "hun": "हूँ", "ho": "हो", "tha": "था",
    "thi": "थी", "hoga": "होगा", "hogi": "होगी", "honge": "होंगे", "hota": "होता", "hoti": "होती",
    "hote": "होते", "hua": "हुआ", "hui": "हुई", "hue": "हुए", "raha": "रहा", "rahi": "रही",
    "rahe": "रहे", "rahega": "रहेगा", "gaya": "गया", "gayi": "गई", "gai": "गई", "gaye": "गए",
    "diya": "दिया", "di": "दी", "diye": "दिए", "liya": "लिया", "li": "ली", "liye": "लिए",
    "chuka": "चुका", "chuki": "चुकी", "chuke": "चुके", "sakta": "सकता", "sakti": "सकती",
    "sakte": "सकते", "sake": "सके", "chahiye": "चाहिए", "chahie": "चाहिए", "wala": "वाला",
    "wali": "वाली", "wale": "वाले", "waala": "वाला", "waali": "वाली", "waale": "वाले",
    # postpositions / connectors
    "ka": "का", "ki": "की", "ke": "के", "ko": "को", "se": "से", "pe": "पे", "par": "पर",
    "tak": "तक", "ne": "ने", "aur": "और", "ya": "या", "lekin": "लेकिन",
    "magar": "मगर", "kyunki": "क्योंकि", "isliye": "इसलिए", "toh": "तो", "bhi": "भी",
    "sirf": "सिर्फ", "bas": "बस", "phir": "फिर", "fir": "फिर", "agar": "अगर",
    "jab": "जब", "jaise": "जैसे", "waise": "वैसे", "saath": "साथ", "sath": "साथ",
    "baare": "बारे", "andar": "अंदर", "bahar": "बाहर", "upar": "ऊपर",
    "neeche": "नीचे", "niche": "नीचे", "pehle": "पहले", "baad": "बाद", "abhi": "अभी",
    "ab": "अब", "aaj": "आज", "kal": "कल", "parso": "परसों", "roz": "रोज़", "hamesha": "हमेशा",
    "kabhi": "कभी", "jaldi": "जल्दी", "dheere": "धीरे", "turant": "तुरंत", "fauran": "फौरन",
    "yahan": "यहाँ", "yaha": "यहाँ", "wahan": "वहाँ", "waha": "वहाँ", "idhar": "इधर", "udhar": "उधर",
    # yes / no / fillers
    "haan": "हाँ", "haa": "हाँ", "han": "हाँ", "nahi": "नहीं", "nahin": "नहीं", "na": "ना",
    "mat": "मत", "theek": "ठीक", "thik": "ठीक", "achha": "अच्छा", "acha": "अच्छा",
    "accha": "अच्छा", "achhi": "अच्छी", "achhe": "अच्छे", "bilkul": "बिल्कुल", "zaroor": "ज़रूर",
    "jaroor": "ज़रूर", "shayad": "शायद", "matlab": "मतलब", "arre": "अरे",
    "haanji": "हांजी", "shukriya": "शुक्रिया", "dhanyavaad": "धन्यवाद",
    "namaste": "नमस्ते", "maaf": "माफ़", "kripya": "कृपया", "chaliye": "चलिए", "chalo": "चलो",
    # quantity / adjectives
    "bahut": "बहुत", "bohot": "बहुत", "bohut": "बहुत", "zyada": "ज़्यादा", "jyada": "ज़्यादा",
    "kam": "कम", "thoda": "थोड़ा", "thodi": "थोड़ी", "thode": "थोड़े", "sara": "सारा", "sare": "सारे",
    "saari": "सारी", "poora": "पूरा", "pura": "पूरा", "puri": "पूरी", "naya": "नया", "nayi": "नई",
    "purana": "पुराना", "bada": "बड़ा", "badi": "बड़ी", "bade": "बड़े", "chhota": "छोटा",
    "chhoti": "छोटी", "sahi": "सही", "galat": "गलत", "mushkil": "मुश्किल", "aasaan": "आसान",
    "ek": "एक", "teen": "तीन", "char": "चार", "paanch": "पांच", "pehla": "पहला",
    "doosra": "दूसरा", "dusra": "दूसरा", "agla": "अगला", "agle": "अगले", "pichla": "पिछला",
    # nouns
    "kaam": "काम", "baat": "बात", "cheez": "चीज़", "cheezein": "चीज़ें", "naam": "नाम",
    "gaana": "गाना", "gaane": "गाने", "gana": "गाना", "din": "दिन", "raat": "रात", "subah": "सुबह",
    "shaam": "शाम", "waqt": "वक्त", "samay": "समय", "ghanta": "घंटा", "ghante": "घंटे",
    "jagah": "जगह", "ghar": "घर", "paani": "पानी", "khana": "खाना", "mausam": "मौसम",
    "tabiyat": "तबीयत", "dimaag": "दिमाग", "dil": "दिल", "duniya": "दुनिया", "sawaal": "सवाल",
    "sawal": "सवाल", "jawab": "जवाब", "madad": "मदद", "khabar": "खबर", "taiyaar": "तैयार",
    "tayyar": "तैयार", "koshish": "कोशिश", "zarurat": "ज़रूरत", "dikkat": "दिक्कत",
    "pareshani": "परेशानी", "samasya": "समस्या", "tarah": "तरह", "taraf": "तरफ", "hisaab": "हिसाब",
    # verbs (stems + common forms)
    "kar": "कर", "karo": "करो", "karna": "करना", "karta": "करता", "karti": "करती", "karte": "करते",
    "karunga": "करूँगा", "karungi": "करूँगी", "karenge": "करेंगे", "kiya": "किया", "kiye": "किए",
    "karke": "करके", "kijiye": "कीजिए", "karein": "करें", "karen": "करें", "karoon": "करूँ",
    "de": "दे", "dena": "देना", "deta": "देता", "deti": "देती", "dete": "देते", "dunga": "दूँगा",
    "doon": "दूँ", "dijiye": "दीजिए", "le": "ले", "lena": "लेना", "leta": "लेता", "lo": "लो",
    "lijiye": "लीजिए", "lunga": "लूँगा", "ja": "जा", "jao": "जाओ", "jana": "जाना", "jata": "जाता",
    "jati": "जाती", "jaate": "जाते", "jayega": "जाएगा", "jaega": "जाएगा", "jaayega": "जाएगा",
    "jaaye": "जाए", "jaye": "जाए", "aa": "आ", "aao": "आओ", "aana": "आना", "aata": "आता",
    "aati": "आती", "aaya": "आया", "aayi": "आई", "aaye": "आए", "aayega": "आएगा",
    "dekh": "देख", "dekho": "देखो", "dekhna": "देखना", "dekhiye": "देखिए", "dekha": "देखा",
    "suno": "सुनो", "suniye": "सुनिए", "sunna": "सुनना", "suna": "सुना",
    "bol": "बोल", "bolo": "बोलो", "bolna": "बोलना", "boliye": "बोलिए", "bola": "बोला",
    "bata": "बता", "batao": "बताओ", "batana": "बताना", "bataiye": "बताइए", "bataya": "बताया",
    "bataunga": "बताऊँगा", "samajh": "समझ", "samjha": "समझा", "samjho": "समझो", "samjhe": "समझे",
    "pata": "पता", "lag": "लग", "laga": "लगा", "lagta": "लगता", "lagti": "लगती", "lagega": "लगेगा",
    "mil": "मिल", "mila": "मिला", "mili": "मिली", "mile": "मिले", "milega": "मिलेगा",
    "chal": "चल", "chala": "चला", "chalao": "चलाओ", "chalana": "चलाना", "chalu": "चालू",
    "chalte": "चलते", "khol": "खोल", "kholo": "खोलो", "khola": "खोला", "kholna": "खोलना",
    "kholta": "खोलता", "band": "बंद", "bandh": "बंद", "ruk": "रुक", "ruko": "रुको",
    "rukiye": "रुकिए", "ruka": "रुका", "bhej": "भेज", "bhejo": "भेजो", "bheja": "भेजा",
    "bhejna": "भेजना", "bhejta": "भेजता", "bhejunga": "भेजूँगा", "likh": "लिख", "likho": "लिखो",
    "likha": "लिखा", "padh": "पढ़", "padho": "पढ़ो", "padha": "पढ़ा", "dhoondh": "ढूंढ",
    "dhundh": "ढूंढ", "dhoondho": "ढूंढो", "dhundho": "ढूंढो", "dhoondha": "ढूंढा", "dhundha": "ढूंढा",
    "rakh": "रख", "rakho": "रखो", "rakha": "रखा", "badha": "बढ़ा", "badhao": "बढ़ाओ",
    "ghata": "घटा", "ghatao": "घटाओ", "hata": "हटा", "hatao": "हटाओ", "hataya": "हटाया",
    "baja": "बजा", "bajao": "बजाओ", "baj": "बज", "sakun": "सकूँ", "chahta": "चाहता",
    "chahti": "चाहती", "chahte": "चाहते", "socha": "सोचा", "soch": "सोच", "jaan": "जान",
    "jaanta": "जानता", "jaante": "जानते", "yaad": "याद", "bana": "बना", "banao": "बनाओ",
    "banaya": "बनाया", "banana": "बनाना", "bhool": "भूल", "kho": "खो",
    "dikha": "दिखा", "dikhao": "दिखाओ", "dikhata": "दिखाता", "sunao": "सुनाओ", "sunata": "सुनाता",
    "rahiye": "रहिए", "baitho": "बैठो", "utho": "उठो",
    "hona": "होना", "hoke": "होके", "raho": "रहो", "rukna": "रुकना", "chalega": "चलेगा",
}
# Words that are also common English — only convert them right after another Hindi word
# ("kar do" → "कर दो", but "do you want" stays English).
_HINGLISH_CONTEXTUAL: dict[str, str] = {
    "do": "दो", "the": "थे", "to": "तो", "me": "में", "so": "सो", "par": "पर", "age": "आगे",
    "sun": "सुन", "hi": "ही", "log": "लोग", "le": "ले", "de": "दे", "pass": "पास", "bus": "बस",
}
_LATIN_WORD_RE = re.compile(r"[A-Za-z']+")


def hinglish_to_devanagari(text: str) -> str:
    """
    Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving
    English words in Latin. Output is meant ONLY for hi-IN TTS voices.
    """
    out: list[str] = []
    prev_hindi = False
    pos = 0
    for m in _LATIN_WORD_RE.finditer(text):
        out.append(text[pos:m.start()])
        word = m.group(0)
        low = word.lower()
        dev = _HINGLISH_TO_DEV.get(low)
        if dev is None and prev_hindi:
            dev = _HINGLISH_CONTEXTUAL.get(low)
        if dev is not None:
            out.append(dev)
            prev_hindi = True
        else:
            out.append(word)
            prev_hindi = False
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)
