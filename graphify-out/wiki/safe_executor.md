# safe_executor

> 17 nodes · cohesion 0.15

## Key Concepts

- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
- **test_exec.py** (2 connections) — `test_exec.py`
- **Exception** (1 connections)
- **Restricted open(): blocks writes to system paths.** (1 connections) — `app/services/safe_executor.py`
- **Restricted __import__: blocks dangerous modules.** (1 connections) — `app/services/safe_executor.py`
- **Raised when generated code violates safety constraints.** (1 connections) — `app/services/safe_executor.py`
- **AST visitor that inspects generated code before execution.** (1 connections) — `app/services/safe_executor.py`
- **Parse and walk the AST, raising SecurityError on violations.** (1 connections) — `app/services/safe_executor.py`
- **Validates and runs 'code' in a restricted namespace. Returns: (success: bool,…** (1 connections) — `app/services/safe_executor.py`

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (7 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 26 (81%)
- INFERRED: 6 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*