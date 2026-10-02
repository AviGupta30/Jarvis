# safe_executor + ui_inspector

> 26 nodes · cohesion 0.11

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **traceback** (7 connections)
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **click_ui_element()** (6 connections) — `app/services/ui_inspector.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **test_api.py** (3 connections) — `test_api.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
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
- **Returns a text summary of the currently focused window: window title + list of…** (1 connections) — `app/services/ui_inspector.py`
- *... and 1 more nodes in this community*

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (7 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [tools](tools.md) (3 shared connections)
- [server + protocol](server_+_protocol.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [style_profiler + refresh_docs](style_profiler_+_refresh_docs.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (1 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (1 shared connections)
- [download_kokoro](download_kokoro.md) (1 shared connections)
- [dark_enhancement](dark_enhancement.md) (1 shared connections)
- [main](main.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `app/services/ui_inspector.py`
- `test_api.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 60 (90%)
- INFERRED: 7 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*