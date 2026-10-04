# voice_agent

> 39 nodes · cohesion 0.08

## Key Concepts

- **voice_agent.py** (35 connections) — `scripts/voice_agent.py`
- **VoiceAgent** (14 connections) — `scripts/voice_agent.py`
- **stream_chat()** (9 connections) — `scripts/voice_agent.py`
- **.handle_utterance()** (9 connections) — `scripts/voice_agent.py`
- **_pick()** (7 connections) — `scripts/voice_agent.py`
- **.dispatch()** (6 connections) — `scripts/voice_agent.py`
- **._run_command()** (6 connections) — `scripts/voice_agent.py`
- **extract_wake_word_command()** (5 connections) — `scripts/voice_agent.py`
- **.run()** (5 connections) — `scripts/voice_agent.py`
- **difflib** (4 connections)
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **._ui_loop()** (4 connections) — `scripts/voice_agent.py`
- **app_services** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **._greet_after_pause()** (3 connections) — `scripts/voice_agent.py`
- **.on_clap()** (3 connections) — `scripts/voice_agent.py`
- **._overlaps_speech()** (3 connections) — `scripts/voice_agent.py`
- **._safe_utterance()** (3 connections) — `scripts/voice_agent.py`
- **httpx** (2 connections)
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- *... and 14 more nodes in this community*

## Relationships

- [voice + context_classifier](voice_+_context_classifier.md) (7 shared connections)
- [voice_agent](voice_agent.md) (7 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (3 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [exact_render](exact_render.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 93 (94%)
- INFERRED: 6 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*