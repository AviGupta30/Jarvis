# server + test_concurrency

> 34 nodes · cohesion 0.07

## Key Concepts

- **sys** (29 connections)
- **threading** (19 connections)
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **prompt_overlay.py** (12 connections) — `app/services/prompt_overlay.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **jarvis_overlay.py** (11 connections) — `scripts/jarvis_overlay.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **pil** (4 connections)
- **test_agentic_web.py** (4 connections) — `test_agentic_web.py`
- **tkinter** (4 connections)
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **socket** (3 connections)
- **neural_cache** (2 connections)
- **prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…** (1 connections) — `app/services/prompt_overlay.py`
- **keyboard** (1 connections)
- **client.py — Python Client Library for Neural Cache (Milestone 5)…** (1 connections) — `neural_cache/client.py`
- **_sigint()** (1 connections) — `neural_cache/server.py`
- **Full startup: recover state, start engine, begin accepting connections.** (1 connections) — `neural_cache/server.py`
- **Restore cache state from disk before the engine thread starts. Called on the…** (1 connections) — `neural_cache/server.py`
- *... and 9 more nodes in this community*

## Relationships

- [persistence + engine](persistence_+_engine.md) (17 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (14 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (5 shared connections)
- [tools](tools.md) (4 shared connections)
- [whatsapp_call + dump_wa_ui](whatsapp_call_+_dump_wa_ui.md) (3 shared connections)
- [client](client.md) (3 shared connections)
- [voice_agent](voice_agent.md) (3 shared connections)
- [jarvis_overlay](jarvis_overlay.md) (3 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (3 shared connections)
- [prompt_overlay](prompt_overlay.md) (2 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (2 shared connections)
- [test_concurrency](test_concurrency.md) (2 shared connections)

## Source Files

- `app/services/prompt_overlay.py`
- `neural_cache/client.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`
- `patch_window.py`
- `scripts/jarvis_overlay.py`
- `test_agentic_web.py`

## Audit Trail

- EXTRACTED: 123 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*