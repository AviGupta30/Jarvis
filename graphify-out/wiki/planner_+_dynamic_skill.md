# planner + dynamic_skill

> 45 nodes · cohesion 0.08

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **asyncio** (15 connections)
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **is_complex_task()** (12 connections) — `app/services/planner.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **concurrent_futures** (7 connections)
- **find_skill()** (6 connections) — `app/memory/memory.py`
- **save_skill()** (6 connections) — `app/memory/memory.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_llm_write_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_strip_fences()** (3 connections) — `app/services/dynamic_skill.py`
- **_call_replanner()** (3 connections) — `app/services/planner.py`
- **app_memory** (2 connections)
- **test_exec.py** (2 connections) — `test_exec.py`
- *... and 20 more nodes in this community*

## Relationships

- [dag_executor](dag_executor.md) (20 shared connections)
- [chat + llm](chat_+_llm.md) (18 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (8 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (8 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (7 shared connections)
- [safe_executor](safe_executor.md) (7 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (6 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (6 shared connections)
- [memory](memory.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (6 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (5 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/memory/memory.py`
- `app/services/dynamic_skill.py`
- `app/services/embeddings.py`
- `app/services/file_ops.py`
- `app/services/planner.py`
- `app/services/safe_executor.py`
- `app/services/task_ledger.py`
- `app/services/ui_inspector.py`
- `docs/features/chat-routing.md`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 195 (86%)
- INFERRED: 31 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*