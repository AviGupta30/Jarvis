# engine + test_protocol

> 27 nodes · cohesion 0.15

## Key Concepts

- **CacheEngine** (20 connections) — `neural_cache/engine.py`
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
- **Route a command dict to the appropriate handler. All handlers return a response…** (1 connections) — `neural_cache/engine.py`
- **Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…** (1 connections) — `neural_cache/engine.py`
- **Spawn the single writer thread. Call once at server boot.** (1 connections) — `neural_cache/engine.py`
- **Gracefully stop the engine writer thread.** (1 connections) — `neural_cache/engine.py`
- **The single consumer loop. Runs on CacheEngineThread. Processes one command at a…** (1 connections) — `neural_cache/engine.py`
- *... and 2 more nodes in this community*

## Relationships

- [server + persistence](server_+_persistence.md) (8 shared connections)
- [test_protocol + protocol](test_protocol_+_protocol.md) (5 shared connections)
- [test_protocol](test_protocol.md) (3 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [lru](lru.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/protocol.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 68 (93%)
- INFERRED: 5 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*