# lru + README

> 38 nodes · cohesion 0.07

## Key Concepts

- **Node** (15 connections) — `neural_cache/lru.py`
- **Neural Cache** (10 connections) — `neural_cache/README.md`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.snapshot()** (3 connections) — `neural_cache/lru.py`
- **.__init__()** (2 connections) — `neural_cache/lru.py`
- **.is_expired()** (2 connections) — `neural_cache/lru.py`
- **Any** (2 connections)
- **Files** (2 connections) — `neural_cache/README.md`
- **.__init__()** (1 connections) — `neural_cache/lru.py`
- **.__repr__()** (1 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Serialise the entire live cache to a plain dict. Expired entries are excluded —…** (1 connections) — `neural_cache/lru.py`
- **Restore cache state from a snapshot dict (produced by snapshot()). Called once…** (1 connections) — `neural_cache/lru.py`
- **Place node at the MRU (most-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Place node at the LRU (least-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Remove node from its current position in the list (O(1) because doubly-linked).** (1 connections) — `neural_cache/lru.py`
- *... and 13 more nodes in this community*

## Relationships

- [test_lru + lru](test_lru_+_lru.md) (12 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `neural_cache/README.md`
- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 59 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*