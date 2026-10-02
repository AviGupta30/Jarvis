# voice_agent

> 18 nodes · cohesion 0.12

## Key Concepts

- **voice_agent.py** (35 connections) — `scripts/voice_agent.py`
- **extract_wake_word_command()** (5 connections) — `scripts/voice_agent.py`
- **random** (4 connections)
- **difflib** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **app_services** (2 connections)
- **httpx** (2 connections)
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- **pyaudio** (1 connections)
- **_launch_overlay()** (1 connections) — `scripts/voice_agent.py`
- **voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)…** (1 connections) — `scripts/voice_agent.py`
- **None if no wake word; otherwise the command with the wake word (and a leading…** (1 connections) — `scripts/voice_agent.py`
- **Convert a linear-planner tag line into natural spoken text.** (1 connections) — `scripts/voice_agent.py`
- **Write Jarvis UI state so the overlay can animate accordingly.** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent](voice_agent.md) (12 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (5 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (5 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (3 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [whatsapp_call + dump_wa_ui](whatsapp_call_+_dump_wa_ui.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 52 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*