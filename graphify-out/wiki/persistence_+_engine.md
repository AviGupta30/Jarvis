# persistence + engine

> 73 nodes · cohesion 0.05

## Key Concepts

- **CacheEngine** (20 connections) — `neural_cache/engine.py`
- **server.py** (20 connections) — `neural_cache/server.py`
- **test_protocol.py** (20 connections) — `neural_cache/tests/test_protocol.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **ok_response()** (14 connections) — `neural_cache/protocol.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **err_response()** (13 connections) — `neural_cache/protocol.py`
- **._dispatch()** (11 connections) — `neural_cache/engine.py`
- **io** (10 connections)
- **Any** (7 connections)
- **queue** (6 connections)
- **._handle_del()** (5 connections) — `neural_cache/engine.py`
- **._handle_get()** (5 connections) — `neural_cache/engine.py`
- **._handle_set()** (5 connections) — `neural_cache/engine.py`
- **._handle_snapshot()** (5 connections) — `neural_cache/engine.py`
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **TestHelpers** (5 connections) — `neural_cache/tests/test_protocol.py`
- **._handle_ping()** (4 connections) — `neural_cache/engine.py`
- **._handle_stats()** (4 connections) — `neural_cache/engine.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **._worker()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- *... and 48 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (17 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (17 shared connections)
- [test_protocol](test_protocol.md) (13 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (5 shared connections)
- [lru](lru.md) (3 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (1 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/protocol.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 185 (96%)
- INFERRED: 8 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*