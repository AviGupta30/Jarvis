# server + persistence

> 31 nodes · cohesion 0.08

## Key Concepts

- **engine.py** (16 connections) — `neural_cache/engine.py`
- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **.__init__()** (3 connections) — `neural_cache/persistence.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **Path** (2 connections)
- **.close()** (2 connections) — `neural_cache/persistence.py`
- **.__init__()** (2 connections) — `neural_cache/persistence.py`
- **.truncate()** (2 connections) — `neural_cache/persistence.py`
- **engine.py — Single-Writer Command Queue (Milestone 3)…** (1 connections) — `neural_cache/engine.py`
- **Flush and close the file handle cleanly on server shutdown.** (1 connections) — `neural_cache/persistence.py`
- **Manages periodic full-state snapshots. The snapshot itself is triggered through…** (1 connections) — `neural_cache/persistence.py`
- **Append-only write-ahead log. Each SET/DEL command is written as a JSON line…** (1 connections) — `neural_cache/persistence.py`
- **Empty the WAL file after a successful snapshot. We truncate (overwrite with…** (1 connections) — `neural_cache/persistence.py`
- **_sigint()** (1 connections) — `neural_cache/server.py`
- **Path** (1 connections)
- **Full startup: recover state, start engine, begin accepting connections.** (1 connections) — `neural_cache/server.py`
- *... and 6 more nodes in this community*

## Relationships

- [benchmark + server](benchmark_+_server.md) (16 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (8 shared connections)
- [persistence](persistence.md) (5 shared connections)
- [lru](lru.md) (2 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (1 shared connections)
- [test_lru](test_lru.md) (1 shared connections)
- [test_protocol + protocol](test_protocol_+_protocol.md) (1 shared connections)
- [client](client.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 66 (89%)
- INFERRED: 8 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*