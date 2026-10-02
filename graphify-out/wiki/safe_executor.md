# safe_executor

> 21 nodes · cohesion 0.14

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
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
- **contextlib** (1 connections)

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (5 shared connections)
- [ui_inspector + tools](ui_inspector_+_tools.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [screen_reader](screen_reader.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 42 (88%)
- INFERRED: 6 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*