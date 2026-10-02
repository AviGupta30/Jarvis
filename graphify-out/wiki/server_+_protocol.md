# server + protocol

> 46 nodes · cohesion 0.07

## Key Concepts

- **sys** (29 connections)
- **pathlib** (28 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **test_protocol.py** (20 connections) — `neural_cache/tests/test_protocol.py`
- **threading** (19 connections)
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **test_lru.py** (16 connections) — `neural_cache/tests/test_lru.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **queue** (6 connections)
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **_recv_exact()** (4 connections) — `neural_cache/protocol.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **pytest** (3 connections)
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **socket** (3 connections)
- **neural_cache** (2 connections)
- **struct** (2 connections)
- *... and 21 more nodes in this community*

## Relationships

- [message_reader + reply_generator](message_reader_+_reply_generator.md) (17 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (17 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (13 shared connections)
- [test_lru](test_lru.md) (8 shared connections)
- [persistence](persistence.md) (6 shared connections)
- [client](client.md) (4 shared connections)
- [benchmark](benchmark.md) (4 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [ppt_studio](ppt_studio.md) (3 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (3 shared connections)
- [agentic_web](agentic_web.md) (3 shared connections)

## Source Files

- `neural_cache/benchmark.py`
- `neural_cache/client.py`
- `neural_cache/protocol.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`
- `neural_cache/tests/test_lru.py`
- `neural_cache/tests/test_protocol.py`
- `patch_window.py`
- `scripts/test_routing.py`

## Audit Trail

- EXTRACTED: 196 (97%)
- INFERRED: 6 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*