# lru

> 16 nodes · cohesion 0.18

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Place node at the MRU (most-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Remove node from its current position in the list (O(1) because doubly-linked).** (1 connections) — `neural_cache/lru.py`
- **Evict a specific node (unlink + remove from map).** (1 connections) — `neural_cache/lru.py`
- **O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…** (1 connections) — `neural_cache/lru.py`
- **Return the value for key, or None on miss / expiry. On hit: moves node to the…** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (11 shared connections)
- [test_lru](test_lru.md) (8 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 38 (84%)
- INFERRED: 7 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*