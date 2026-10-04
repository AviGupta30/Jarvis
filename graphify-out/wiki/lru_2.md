# lru

> 7 nodes · cohesion 0.29

## Key Concepts

- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **.snapshot()** (4 connections) — `neural_cache/lru.py`
- **Any** (2 connections)
- **Serialise the entire live cache to a plain dict. Expired entries are excluded —…** (1 connections) — `neural_cache/lru.py`
- **Restore cache state from a snapshot dict (produced by snapshot()). Called once…** (1 connections) — `neural_cache/lru.py`
- **Place node at the LRU (least-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (6 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 12 (92%)
- INFERRED: 1 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*