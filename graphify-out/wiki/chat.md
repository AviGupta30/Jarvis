# chat

> 10 nodes · cohesion 0.31

## Key Concepts

- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **resume_stream()** (2 connections) — `app/api/chat.py`
- **tool_stream()** (2 connections) — `app/api/chat.py`
- **clarification_stream()** (1 connections) — `app/api/chat.py`
- **post** (1 connections)
- **Call this whenever conversation_history is updated.** (1 connections) — `app/services/llm.py`

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (15 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (4 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (4 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (4 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (3 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (3 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (1 shared connections)
- [CLAUDE + agents](CLAUDE_+_agents.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/llm.py`

## Audit Trail

- EXTRACTED: 58 (88%)
- INFERRED: 8 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*