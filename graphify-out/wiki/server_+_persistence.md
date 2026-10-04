# server + persistence

> 66 nodes · cohesion 0.05

## Key Concepts

- **time** (52 connections)
- **typing** (30 connections)
- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **pathlib** (28 connections)
- **threading** (22 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **logging** (14 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **io** (11 connections)
- **collections** (8 connections)
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **queue** (7 connections)
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- *... and 41 more nodes in this community*

## Relationships

- [test_protocol + engine](test_protocol_+_engine.md) (15 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (13 shared connections)
- [screen_vision](screen_vision.md) (9 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (5 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (5 shared connections)
- [voice](voice.md) (5 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (5 shared connections)
- [dump_wa_ui + find_call_btn](dump_wa_ui_+_find_call_btn.md) (5 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (4 shared connections)
- [screen_reader](screen_reader.md) (4 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (4 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `app/services/screen_vision.py`
- `neural_cache/benchmark.py`
- `neural_cache/client.py`
- `neural_cache/engine.py`
- `neural_cache/lru.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 312 (97%)
- INFERRED: 9 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*