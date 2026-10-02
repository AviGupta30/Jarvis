# lru

> 11 nodes · cohesion 0.22

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **.snapshot()** (3 connections) — `neural_cache/lru.py`
- **Any** (2 connections)
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **Serialise the entire live cache to a plain dict. Expired entries are excluded —…** (1 connections) — `neural_cache/lru.py`
- **Restore cache state from a snapshot dict (produced by snapshot()). Called once…** (1 connections) — `neural_cache/lru.py`
- **Place node at the LRU (least-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (11 shared connections)
- [test_lru](test_lru.md) (6 shared connections)
- [persistence + engine](persistence_+_engine.md) (3 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (2 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 28 (80%)
- INFERRED: 7 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*