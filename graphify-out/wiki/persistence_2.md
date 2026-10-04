# persistence

> 4 nodes · cohesion 0.50

## Key Concepts

- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **Queue** (2 connections)
- **Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.…** (1 connections) — `neural_cache/persistence.py`
- **_loop()** (1 connections) — `neural_cache/persistence.py`

## Relationships

- [benchmark + server](benchmark_+_server.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

## Source Files

- `neural_cache/persistence.py`

## Audit Trail

- EXTRACTED: 4 (80%)
- INFERRED: 1 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*