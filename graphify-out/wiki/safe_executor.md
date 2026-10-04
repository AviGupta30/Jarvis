# safe_executor

> 19 nodes · cohesion 0.14

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **io** (11 connections)
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
- **ast** (2 connections)
- **Exception** (1 connections)
- **Safe Code Executor for Jarvis ------------------------------- Runs LLM-…** (1 connections) — `app/services/safe_executor.py`
- **Restricted open(): blocks writes to system paths.** (1 connections) — `app/services/safe_executor.py`
- **Restricted __import__: blocks dangerous modules.** (1 connections) — `app/services/safe_executor.py`
- **Raised when generated code violates safety constraints.** (1 connections) — `app/services/safe_executor.py`
- **AST visitor that inspects generated code before execution.** (1 connections) — `app/services/safe_executor.py`
- **Parse and walk the AST, raising SecurityError on violations.** (1 connections) — `app/services/safe_executor.py`
- **contextlib** (1 connections)

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (7 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (3 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [ui_inspector + tools](ui_inspector_+_tools.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [test_lru](test_lru.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (1 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`

## Audit Trail

- EXTRACTED: 49 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*