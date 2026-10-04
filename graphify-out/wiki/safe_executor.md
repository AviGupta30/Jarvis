# safe_executor

> 18 nodes · cohesion 0.15

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
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

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (7 shared connections)
- [server + persistence](server_+_persistence.md) (3 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [gmail_tool](gmail_tool.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`

## Audit Trail

- EXTRACTED: 39 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*