# engine + test_protocol

> 29 nodes · cohesion 0.14

## Key Concepts

- **CacheEngine** (20 connections) — `neural_cache/engine.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **ok_response()** (14 connections) — `neural_cache/protocol.py`
- **err_response()** (13 connections) — `neural_cache/protocol.py`
- **._dispatch()** (11 connections) — `neural_cache/engine.py`
- **Any** (7 connections)
- **._handle_del()** (5 connections) — `neural_cache/engine.py`
- **._handle_get()** (5 connections) — `neural_cache/engine.py`
- **._handle_set()** (5 connections) — `neural_cache/engine.py`
- **._handle_snapshot()** (5 connections) — `neural_cache/engine.py`
- **TestHelpers** (5 connections) — `neural_cache/tests/test_protocol.py`
- **._handle_ping()** (4 connections) — `neural_cache/engine.py`
- **._handle_stats()** (4 connections) — `neural_cache/engine.py`
- **._worker()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- **.test_helpers_are_json_serialisable()** (4 connections) — `neural_cache/tests/test_protocol.py`
- **.start()** (2 connections) — `neural_cache/engine.py`
- **.stop()** (2 connections) — `neural_cache/engine.py`
- **.test_err_response()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_ok_response_no_value()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_ok_response_with_value()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **engine.py — Single-Writer Command Queue (Milestone 3)…** (1 connections) — `neural_cache/engine.py`
- **Route a command dict to the appropriate handler. All handlers return a response…** (1 connections) — `neural_cache/engine.py`
- **Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…** (1 connections) — `neural_cache/engine.py`
- **Spawn the single writer thread. Call once at server boot.** (1 connections) — `neural_cache/engine.py`
- *... and 4 more nodes in this community*

## Relationships

- [test_protocol](test_protocol.md) (9 shared connections)
- [persistence](persistence.md) (7 shared connections)
- [server](server.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [lru](lru.md) (2 shared connections)
- [benchmark](benchmark.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/protocol.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 81 (94%)
- INFERRED: 5 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*