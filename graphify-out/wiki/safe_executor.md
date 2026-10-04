# safe_executor

> 20 nodes · cohesion 0.13

## Key Concepts

- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **io** (10 connections)
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
- **contextlib** (1 connections)

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (7 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [tools](tools.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (1 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 49 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*