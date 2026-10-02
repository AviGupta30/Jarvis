# safe_executor + ui_inspector

> 32 nodes · cohesion 0.09

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **ui_inspector.py** (18 connections) — `app/services/ui_inspector.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **click_ui_element()** (6 connections) — `app/services/ui_inspector.py`
- **ctypes** (6 connections)
- **debug_ui_tree()** (5 connections) — `app/services/ui_inspector.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **dump_spotify.py** (4 connections) — `dump_spotify.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
- **test_exec.py** (2 connections) — `test_exec.py`
- **Dynamic Skill Engine for Jarvis 2.0 ------------------------------------- When…** (1 connections) — `app/services/dynamic_skill.py`
- **Exception** (1 connections)
- **Safe Code Executor for Jarvis ------------------------------- Runs LLM-…** (1 connections) — `app/services/safe_executor.py`
- **Restricted open(): blocks writes to system paths.** (1 connections) — `app/services/safe_executor.py`
- **Restricted __import__: blocks dangerous modules.** (1 connections) — `app/services/safe_executor.py`
- **Raised when generated code violates safety constraints.** (1 connections) — `app/services/safe_executor.py`
- **AST visitor that inspects generated code before execution.** (1 connections) — `app/services/safe_executor.py`
- *... and 7 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (14 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (11 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)
- [tools](tools.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/dynamic_skill.py`
- `app/services/safe_executor.py`
- `app/services/ui_inspector.py`
- `dump_spotify.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 95 (93%)
- INFERRED: 7 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*