# context_classifier + personality

> 20 nodes · cohesion 0.13

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **context_classifier.py** (8 connections) — `app/services/context_classifier.py`
- **classify_context()** (7 connections) — `app/services/context_classifier.py`
- **get_context_aware_prompt()** (6 connections) — `app/services/personality.py`
- **test_language.py** (6 connections) — `scripts/test_language.py`
- **_maybe_compress_history()** (5 connections) — `app/services/llm.py`
- **personality.py** (5 connections) — `app/services/personality.py`
- **Flow of `generate_chat_response`** (5 connections) — `docs/features/llm-personality.md`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **context_classifier.py — Jarvis Situational Awareness…** (1 connections) — `app/services/context_classifier.py`
- **Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…** (1 connections) — `app/services/context_classifier.py`
- **Classify the situation from user input. Returns a dict with keys: urgency :…** (1 connections) — `app/services/context_classifier.py`
- **When conversation history exceeds 15 messages, compress the oldest 10 into a…** (1 connections) — `app/services/llm.py`
- **personality.py — Jarvis Character & Personality Engine…** (1 connections) — `app/services/personality.py`
- **Returns a dynamically adjusted system prompt based on: - Time of day (hour:…** (1 connections) — `app/services/personality.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice_agent](voice_agent.md) (11 shared connections)
- [voice](voice.md) (11 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (1 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `app/services/voice.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 42 (65%)
- INFERRED: 23 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*