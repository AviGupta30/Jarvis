# voice_agent + acoustic_tripwire

> 22 nodes · cohesion 0.11

## Key Concepts

- **voice_agent.py** (35 connections) — `scripts/voice_agent.py`
- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **threading** (19 connections)
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **collections** (8 connections)
- **numpy** (8 connections)
- **extract_wake_word_command()** (5 connections) — `scripts/voice_agent.py`
- **difflib** (3 connections)
- **_clean_agentic_line()** (3 connections) — `scripts/voice_agent.py`
- **_speakable()** (3 connections) — `scripts/voice_agent.py`
- **app_services** (2 connections)
- **httpx** (2 connections)
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- **acoustic_tripwire.py — Jarvis Acoustic Wake Engine…** (1 connections) — `app/services/acoustic_tripwire.py`
- **screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…** (1 connections) — `app/services/screen_vision.py`
- **mss** (1 connections)
- **pyaudio** (1 connections)
- **_launch_overlay()** (1 connections) — `scripts/voice_agent.py`
- **voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)…** (1 connections) — `scripts/voice_agent.py`
- **None if no wake word; otherwise the command with the wake word (and a leading…** (1 connections) — `scripts/voice_agent.py`
- **Convert a linear-planner tag line into natural spoken text.** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (14 shared connections)
- [screen_vision](screen_vision.md) (11 shared connections)
- [voice_agent](voice_agent.md) (10 shared connections)
- [persistence + server](persistence_+_server.md) (5 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (4 shared connections)
- [voice](voice.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (2 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (2 shared connections)
- [uia_local](uia_local.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `app/services/screen_vision.py`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 112 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*