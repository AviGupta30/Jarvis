# persistence

> 27 nodes · cohesion 0.09

## Key Concepts

- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **.__init__()** (3 connections) — `neural_cache/persistence.py`
- **.read()** (3 connections) — `neural_cache/persistence.py`
- **.write()** (3 connections) — `neural_cache/persistence.py`
- **.append()** (3 connections) — `neural_cache/persistence.py`
- **.read_all()** (3 connections) — `neural_cache/persistence.py`
- **Path** (2 connections)
- **Queue** (2 connections)
- **.close()** (2 connections) — `neural_cache/persistence.py`
- **.__init__()** (2 connections) — `neural_cache/persistence.py`
- **.truncate()** (2 connections) — `neural_cache/persistence.py`
- **Flush and close the file handle cleanly on server shutdown.** (1 connections) — `neural_cache/persistence.py`
- **Manages periodic full-state snapshots. The snapshot itself is triggered through…** (1 connections) — `neural_cache/persistence.py`
- **Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…** (1 connections) — `neural_cache/persistence.py`
- **Load the snapshot from disk. Returns None if no snapshot exists yet. Called…** (1 connections) — `neural_cache/persistence.py`
- **Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.…** (1 connections) — `neural_cache/persistence.py`
- **Append-only write-ahead log. Each SET/DEL command is written as a JSON line…** (1 connections) — `neural_cache/persistence.py`
- **Append one command to the WAL and flush immediately. Flushing on every write is…** (1 connections) — `neural_cache/persistence.py`
- **Read and parse all commands from the WAL file. Called once at startup for…** (1 connections) — `neural_cache/persistence.py`
- **Empty the WAL file after a successful snapshot. We truncate (overwrite with…** (1 connections) — `neural_cache/persistence.py`
- *... and 2 more nodes in this community*

## Relationships

- [server + protocol](server_+_protocol.md) (6 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (5 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (4 shared connections)
- [lru](lru.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`

## Audit Trail

- EXTRACTED: 43 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*