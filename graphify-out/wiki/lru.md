# lru

> 25 nodes · cohesion 0.13

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **Node** (15 connections) — `neural_cache/lru.py`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.__init__()** (2 connections) — `neural_cache/lru.py`
- **.is_expired()** (2 connections) — `neural_cache/lru.py`
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **.__init__()** (1 connections) — `neural_cache/lru.py`
- **.__repr__()** (1 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Place node at the MRU (most-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Remove node from its current position in the list (O(1) because doubly-linked).** (1 connections) — `neural_cache/lru.py`
- **Evict a specific node (unlink + remove from map).** (1 connections) — `neural_cache/lru.py`
- **A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…** (1 connections) — `neural_cache/lru.py`
- **Evict the LRU entry (the node just before the tail sentinel). Returns the…** (1 connections) — `neural_cache/lru.py`
- **Return True if this entry has a TTL and it has elapsed.** (1 connections) — `neural_cache/lru.py`
- **O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…** (1 connections) — `neural_cache/lru.py`
- **Return the value for key, or None on miss / expiry. On hit: moves node to the…** (1 connections) — `neural_cache/lru.py`

## Relationships

- [test_lru](test_lru.md) (8 shared connections)
- [lru](lru.md) (6 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [persistence](persistence.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [README](README.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 51 (86%)
- INFERRED: 8 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*