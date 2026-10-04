# persistence

> 9 nodes · cohesion 0.22

## Key Concepts

- **Any** (4 connections)
- **.read()** (3 connections) — `neural_cache/persistence.py`
- **.write()** (3 connections) — `neural_cache/persistence.py`
- **.append()** (3 connections) — `neural_cache/persistence.py`
- **.read_all()** (3 connections) — `neural_cache/persistence.py`
- **Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…** (1 connections) — `neural_cache/persistence.py`
- **Load the snapshot from disk. Returns None if no snapshot exists yet. Called…** (1 connections) — `neural_cache/persistence.py`
- **Append one command to the WAL and flush immediately. Flushing on every write is…** (1 connections) — `neural_cache/persistence.py`
- **Read and parse all commands from the WAL file. Called once at startup for…** (1 connections) — `neural_cache/persistence.py`

## Relationships

- [server + persistence](server_+_persistence.md) (4 shared connections)

## Source Files

- `neural_cache/persistence.py`

## Audit Trail

- EXTRACTED: 12 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*