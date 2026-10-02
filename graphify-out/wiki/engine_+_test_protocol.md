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

- [persistence + server](persistence_+_server.md) (11 shared connections)
- [test_protocol](test_protocol.md) (9 shared connections)
- [lru + test_lru](lru_+_test_lru.md) (3 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (2 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (1 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (1 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (1 shared connections)

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