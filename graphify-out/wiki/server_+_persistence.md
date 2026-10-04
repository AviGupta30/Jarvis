# server + persistence

> 42 nodes · cohesion 0.08

## Key Concepts

- **threading** (22 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **logging** (14 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **queue** (7 connections)
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **socket** (3 connections)
- **neural_cache** (2 connections)
- **Queue** (2 connections)
- **client.py — Python Client Library for Neural Cache (Milestone 5)…** (1 connections) — `neural_cache/client.py`
- **engine.py — Single-Writer Command Queue (Milestone 3)…** (1 connections) — `neural_cache/engine.py`
- **persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…** (1 connections) — `neural_cache/persistence.py`
- *... and 17 more nodes in this community*

## Relationships

- [persistence](persistence.md) (10 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (8 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (8 shared connections)
- [test_protocol](test_protocol.md) (6 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (5 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (5 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (4 shared connections)
- [test_lru](test_lru.md) (4 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)

## Source Files

- `neural_cache/client.py`
- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/protocol.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 142 (95%)
- INFERRED: 8 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*