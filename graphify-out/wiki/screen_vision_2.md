# screen_vision

> 12 nodes · cohesion 0.18

## Key Concepts

- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **_classify_intent()** (5 connections) — `app/services/screen_vision.py`
- **_build_history_context()** (3 connections) — `app/services/screen_vision.py`
- **_build_system_prompt()** (3 connections) — `app/services/screen_vision.py`
- **_call_gemma_reasoning()** (3 connections) — `app/services/screen_vision.py`
- **Tool-callable version — called when user asks 'what's on my screen?' Routes…** (1 connections) — `app/services/screen_reader.py`
- **Summarise the last N screen states so the VLM can reason about what changed.…** (1 connections) — `app/services/screen_vision.py`
- **Send a scene description to Groq (openai/gpt-oss-20b) for reasoning.** (1 connections) — `app/services/screen_vision.py`
- **Parse the user's phrasing to determine the response mode. describe → "What am I…** (1 connections) — `app/services/screen_vision.py`
- **Assemble the full system prompt based on intent mode and context.** (1 connections) — `app/services/screen_vision.py`
- **Main entry point. Captures screen, resolves context, calls VLM, routes…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [screen_reader](screen_reader.md) (6 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (5 shared connections)
- [screen_vision](screen_vision.md) (4 shared connections)
- [tools](tools.md) (2 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [screen_reader + screen_vision](screen_reader_+_screen_vision.md) (1 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 31 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*