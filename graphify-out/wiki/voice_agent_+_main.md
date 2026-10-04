# voice_agent + main

> 13 nodes · cohesion 0.17

## Key Concepts

- **stream_chat()** (9 connections) — `scripts/voice_agent.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **AsyncClient** (1 connections)
- **Convert a linear-planner tag line into natural spoken text.** (1 connections) — `scripts/voice_agent.py`
- **POST /chat with the spoken language, speak the reply into `ch` as it streams.…** (1 connections) — `scripts/voice_agent.py`
- **pusher()** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (4 shared connections)
- [voice_agent + voice](voice_agent_+_voice.md) (3 shared connections)
- [main](main.md) (2 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (1 shared connections)
- [voice + voice](voice_+_voice.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 24 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*