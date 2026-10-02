# test_lru + lru

> 34 nodes · cohesion 0.07

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **test_protocol.py** (20 connections) — `neural_cache/tests/test_protocol.py`
- **test_lru.py** (16 connections) — `neural_cache/tests/test_lru.py`
- **TestSnapshot** (7 connections) — `neural_cache/tests/test_lru.py`
- **TestSentinels** (5 connections) — `neural_cache/tests/test_lru.py`
- **_recv_exact()** (4 connections) — `neural_cache/protocol.py`
- **small_cache()** (4 connections) — `neural_cache/tests/test_lru.py`
- **TestO1Timing** (4 connections) — `neural_cache/tests/test_lru.py`
- **._time_ops()** (4 connections) — `neural_cache/tests/test_lru.py`
- **large_cache()** (3 connections) — `neural_cache/tests/test_lru.py`
- **.test_o1_set_get_scaling()** (3 connections) — `neural_cache/tests/test_lru.py`
- **pytest** (3 connections)
- **fixture** (2 connections)
- **.test_snapshot_load_respects_capacity()** (2 connections) — `neural_cache/tests/test_lru.py`
- **struct** (2 connections)
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…** (1 connections) — `neural_cache/lru.py`
- **Loop until exactly n bytes have been read from sock. This is necessary because…** (1 connections) — `neural_cache/protocol.py`
- **test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…** (1 connections) — `neural_cache/tests/test_lru.py`
- **Return average time per (set + get) operation in microseconds.** (1 connections) — `neural_cache/tests/test_lru.py`
- **Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…** (1 connections) — `neural_cache/tests/test_lru.py`
- **Snapshot with more keys than capacity should trigger LRU eviction on load.** (1 connections) — `neural_cache/tests/test_lru.py`
- **LRU cache with capacity 3 — easy to reason about eviction.** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_delete_all_returns_to_empty()** (1 connections) — `neural_cache/tests/test_lru.py`
- *... and 9 more nodes in this community*

## Relationships

- [lru + README](lru_+_README.md) (12 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (12 shared connections)
- [persistence + server](persistence_+_server.md) (9 shared connections)
- [test_lru](test_lru.md) (4 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (4 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`
- `neural_cache/protocol.py`
- `neural_cache/tests/test_lru.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 77 (92%)
- INFERRED: 7 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*