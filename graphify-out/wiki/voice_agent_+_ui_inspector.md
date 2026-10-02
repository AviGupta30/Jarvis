# voice_agent + ui_inspector

> 25 nodes · cohesion 0.09

## Key Concepts

- **voice_agent.py** (35 connections) — `scripts/voice_agent.py`
- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **ui_inspector.py** (18 connections) — `app/services/ui_inspector.py`
- **context_classifier.py** (8 connections) — `app/services/context_classifier.py`
- **collections** (8 connections)
- **numpy** (8 connections)
- **ctypes** (6 connections)
- **debug_ui_tree()** (5 connections) — `app/services/ui_inspector.py`
- **dump_spotify.py** (4 connections) — `dump_spotify.py`
- **random** (4 connections)
- **difflib** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **app_services** (2 connections)
- **httpx** (2 connections)
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- **context_classifier.py — Jarvis Situational Awareness…** (1 connections) — `app/services/context_classifier.py`
- **screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…** (1 connections) — `app/services/screen_vision.py`
- **ui_inspector.py — Jarvis UIA Engine (Upgraded)…** (1 connections) — `app/services/ui_inspector.py`
- **Dump the full accessibility tree of an app window as a readable string. Use…** (1 connections) — `app/services/ui_inspector.py`
- **mss** (1 connections)
- **pyaudio** (1 connections)
- **_launch_overlay()** (1 connections) — `scripts/voice_agent.py`
- **voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)…** (1 connections) — `scripts/voice_agent.py`
- **Convert a linear-planner tag line into natural spoken text.** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent](voice_agent.md) (15 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (12 shared connections)
- [persistence + server](persistence_+_server.md) (11 shared connections)
- [screen_vision](screen_vision.md) (11 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (5 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (4 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [voice](voice.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/screen_vision.py`
- `app/services/ui_inspector.py`
- `dump_spotify.py`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 121 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*