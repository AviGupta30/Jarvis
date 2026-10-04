# lru

> 13 nodes · cohesion 0.18

## Key Concepts

- **Node** (15 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **.__init__()** (2 connections) — `neural_cache/lru.py`
- **.is_expired()** (2 connections) — `neural_cache/lru.py`
- **.__init__()** (1 connections) — `neural_cache/lru.py`
- **.__repr__()** (1 connections) — `neural_cache/lru.py`
- **Restore cache state from a snapshot dict (produced by snapshot()). Called once…** (1 connections) — `neural_cache/lru.py`
- **Place node at the LRU (least-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…** (1 connections) — `neural_cache/lru.py`
- **Evict the LRU entry (the node just before the tail sentinel). Returns the…** (1 connections) — `neural_cache/lru.py`
- **Return True if this entry has a TTL and it has elapsed.** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (11 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [README](README.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 27 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*