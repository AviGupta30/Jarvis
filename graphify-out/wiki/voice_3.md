# voice

> 17 nodes · cohesion 0.16

## Key Concepts

- **Speaker** (17 connections) — `app/services/voice.py`
- **hinglish_to_devanagari()** (6 connections) — `app/services/hinglish_normalizer.py`
- **TTS (`voice.Speaker`, `start_clip`, `_Player`)** (6 connections) — `docs/features/voice.md`
- **._take()** (5 connections) — `app/services/voice.py`
- **_norm_words()** (4 connections) — `app/services/voice.py`
- **.run()** (4 connections) — `app/services/voice.py`
- **.stop_all()** (4 connections) — `app/services/voice.py`
- **Fixed on 2026-09-30 (voice)** (4 connections) — `docs/KNOWN_ISSUES.md`
- **._wake()** (3 connections) — `app/services/voice.py`
- **._gc()** (2 connections) — `app/services/voice.py`
- **.say_now()** (2 connections) — `app/services/voice.py`
- **Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Plays sentences from many Channels without overlap: - urgent phrases (acks,…** (1 connections) — `app/services/voice.py`
- **Barge-in "stop": silence now and drop everything queued.** (1 connections) — `app/services/voice.py`
- **Next (channel, text, lang) or None. Non-blocking.** (1 connections) — `app/services/voice.py`
- **.busy()** (1 connections) — `app/services/voice.py`
- **.wait_idle()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (10 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [voice + hinglish_normalizer](voice_+_hinglish_normalizer.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [KNOWN_ISSUES](KNOWN_ISSUES.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 32 (78%)
- INFERRED: 9 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*