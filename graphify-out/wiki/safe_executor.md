# safe_executor

> 23 nodes · cohesion 0.13

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **click_ui_element()** (6 connections) — `app/services/ui_inspector.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
- **ast** (2 connections)
- **test_exec.py** (2 connections) — `test_exec.py`
- **Exception** (1 connections)
- **Safe Code Executor for Jarvis ------------------------------- Runs LLM-…** (1 connections) — `app/services/safe_executor.py`
- **Restricted open(): blocks writes to system paths.** (1 connections) — `app/services/safe_executor.py`
- **Restricted __import__: blocks dangerous modules.** (1 connections) — `app/services/safe_executor.py`
- **Raised when generated code violates safety constraints.** (1 connections) — `app/services/safe_executor.py`
- **AST visitor that inspects generated code before execution.** (1 connections) — `app/services/safe_executor.py`
- **Parse and walk the AST, raising SecurityError on violations.** (1 connections) — `app/services/safe_executor.py`
- **Validates and runs 'code' in a restricted namespace. Returns: (success: bool,…** (1 connections) — `app/services/safe_executor.py`
- **Legacy-compatible API: find a control by text in the active window and click…** (1 connections) — `app/services/ui_inspector.py`
- **contextlib** (1 connections)

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (7 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [screen_reader](screen_reader.md) (2 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [gmail_tool + download_kokoro](gmail_tool_+_download_kokoro.md) (1 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `app/services/ui_inspector.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 46 (88%)
- INFERRED: 6 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*