# persistence + server

> 44 nodes · cohesion 0.06

## Key Concepts

- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **.__init__()** (3 connections) — `neural_cache/persistence.py`
- **.read()** (3 connections) — `neural_cache/persistence.py`
- **.write()** (3 connections) — `neural_cache/persistence.py`
- **.append()** (3 connections) — `neural_cache/persistence.py`
- **.read_all()** (3 connections) — `neural_cache/persistence.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **Path** (2 connections)
- **Queue** (2 connections)
- **.close()** (2 connections) — `neural_cache/persistence.py`
- **.__init__()** (2 connections) — `neural_cache/persistence.py`
- **.truncate()** (2 connections) — `neural_cache/persistence.py`
- **Flush and close the file handle cleanly on server shutdown.** (1 connections) — `neural_cache/persistence.py`
- *... and 19 more nodes in this community*

## Relationships

- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (13 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (5 shared connections)
- [lru](lru.md) (1 shared connections)
- [client](client.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 65 (88%)
- INFERRED: 9 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*