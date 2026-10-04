# voice_agent

> 14 nodes · cohesion 0.16

## Key Concepts

- **voice_agent.py** (35 connections) — `scripts/voice_agent.py`
- **extract_wake_word_command()** (5 connections) — `scripts/voice_agent.py`
- **difflib** (4 connections)
- **random** (4 connections)
- **app_services** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **httpx** (2 connections)
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **pyaudio** (1 connections)
- **_launch_overlay()** (1 connections) — `scripts/voice_agent.py`
- **voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)…** (1 connections) — `scripts/voice_agent.py`
- **None if no wake word; otherwise the command with the wake word (and a leading…** (1 connections) — `scripts/voice_agent.py`
- **Convert a linear-planner tag line into natural spoken text.** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent](voice_agent.md) (12 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (4 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [exact_render](exact_render.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 50 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*