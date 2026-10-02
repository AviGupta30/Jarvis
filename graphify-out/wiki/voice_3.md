# voice

> 25 nodes · cohesion 0.11

## Key Concepts

- **Speaker** (17 connections) — `app/services/voice.py`
- **Channel** (8 connections) — `app/services/voice.py`
- **hinglish_to_devanagari()** (6 connections) — `app/services/hinglish_normalizer.py`
- **TTS (`voice.Speaker`, `start_clip`, `_Player`)** (6 connections) — `docs/features/voice.md`
- **.is_echo()** (5 connections) — `app/services/voice.py`
- **._take()** (5 connections) — `app/services/voice.py`
- **_norm_words()** (4 connections) — `app/services/voice.py`
- **.run()** (4 connections) — `app/services/voice.py`
- **.stop_all()** (4 connections) — `app/services/voice.py`
- **Fixed on 2026-09-30 (voice)** (4 connections) — `docs/KNOWN_ISSUES.md`
- **._wake()** (3 connections) — `app/services/voice.py`
- **.channel()** (2 connections) — `app/services/voice.py`
- **._gc()** (2 connections) — `app/services/voice.py`
- **.say_now()** (2 connections) — `app/services/voice.py`
- **Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…** (1 connections) — `app/services/hinglish_normalizer.py`
- **.close()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.mute()** (1 connections) — `app/services/voice.py`
- **The speech stream of one command's reply.** (1 connections) — `app/services/voice.py`
- **Plays sentences from many Channels without overlap: - urgent phrases (acks,…** (1 connections) — `app/services/voice.py`
- **Barge-in "stop": silence now and drop everything queued.** (1 connections) — `app/services/voice.py`
- **Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back…** (1 connections) — `app/services/voice.py`
- **Next (channel, text, lang) or None. Non-blocking.** (1 connections) — `app/services/voice.py`
- **.busy()** (1 connections) — `app/services/voice.py`
- **.wait_idle()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (10 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (3 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (2 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 40 (78%)
- INFERRED: 11 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*