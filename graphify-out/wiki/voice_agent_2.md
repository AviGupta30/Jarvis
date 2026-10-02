# voice_agent

> 38 nodes · cohesion 0.09

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
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **._ui_loop()** (4 connections) — `scripts/voice_agent.py`
- **difflib** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **._greet_after_pause()** (3 connections) — `scripts/voice_agent.py`
- **.on_clap()** (3 connections) — `scripts/voice_agent.py`
- **._overlaps_speech()** (3 connections) — `scripts/voice_agent.py`
- **._safe_utterance()** (3 connections) — `scripts/voice_agent.py`
- **app_services** (2 connections)
- **httpx** (2 connections)
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- **._open_followup()** (2 connections) — `scripts/voice_agent.py`
- *... and 13 more nodes in this community*

## Relationships

- [context_classifier + personality](context_classifier_+_personality.md) (8 shared connections)
- [voice_agent](voice_agent.md) (7 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (2 shared connections)
- [server + protocol](server_+_protocol.md) (2 shared connections)
- [memory + main](memory_+_main.md) (2 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [spotify_service](spotify_service.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 89 (94%)
- INFERRED: 6 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*