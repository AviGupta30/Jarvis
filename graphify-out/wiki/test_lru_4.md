# test_lru

> 16 nodes · cohesion 0.12

## Key Concepts

- **pathlib** (28 connections)
- **test_lru.py** (16 connections) — `neural_cache/tests/test_lru.py`
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **TestTTL** (6 connections) — `neural_cache/tests/test_lru.py`
- **TestSentinels** (5 connections) — `neural_cache/tests/test_lru.py`
- **lru.py — Hand-rolled LRU Cache (Milestone 1)…** (1 connections) — `neural_cache/lru.py`
- **test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_delete_all_returns_to_empty()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_empty_cache_head_tail_linked()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_sentinels_not_in_map()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_single_element_list_integrity()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_expired_key_counts_as_eviction()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_expired_key_evicted_from_map()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_set_without_ttl_never_expires()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_ttl_expiry_on_get()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_zero_ttl_immediately_expired()** (1 connections) — `neural_cache/tests/test_lru.py`

## Relationships

- [test_lru](test_lru.md) (6 shared connections)
- [server + persistence](server_+_persistence.md) (4 shared connections)
- [lru](lru.md) (4 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [test_protocol](test_protocol.md) (2 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`
- `neural_cache/tests/test_lru.py`

## Audit Trail

- EXTRACTED: 58 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*