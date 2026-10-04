# chat_endpoint()

> God node · 50 connections · `app/api/chat.py`

**Community:** [chat + youtube_control](chat_+_youtube_control.md)

## Connections by Relation

### calls
- [create_resume()](create_resume.md) `EXTRACTED`
- keyword_detect_tool() `EXTRACTED`
- store_turn() `EXTRACTED`
- run_dynamic_skill() `EXTRACTED`
- detect_resume_request() `EXTRACTED`
- parse_youtube_followup() `EXTRACTED`
- recall() `EXTRACTED`
- detect_resume_intent() `EXTRACTED`
- check_for_tool_intent() `EXTRACTED`
- read_file() `EXTRACTED`
- _media_compound() `EXTRACTED`
- _save_session() `EXTRACTED`
- is_complex_task() `EXTRACTED`
- format_recall_for_prompt() `EXTRACTED`
- is_dag_task() `EXTRACTED`
- get_embedding() `EXTRACTED`
- youtube_tab_open() `EXTRACTED`
- get_task_ledger_for_prompt() `EXTRACTED`
- _run_direct_tools() `EXTRACTED`
- youtube_session_active() `EXTRACTED`
- *…and 12 more `calls` connection(s) not listed (lowest-degree first to go)*

### contains
- chat.py `EXTRACTED`
- _dag_stream_with_history() `EXTRACTED`
- planner_stream() `EXTRACTED`
- response_stream_with_history() `EXTRACTED`
- flow_stream() `EXTRACTED`
- resume_stream() `EXTRACTED`
- tool_stream() `EXTRACTED`
- clarification_stream() `EXTRACTED`

### indirect_call
- get_screen_text_summary() `INFERRED`
- describe_screen_for_llm() `INFERRED`

### references
- [Key pieces](Key_pieces.md) `INFERRED`
- Flow `INFERRED`
- Fixed on 2026-09-28 `INFERRED`
- Jump table for the big files `INFERRED`
- Flow (`chat_endpoint`, order matters, first hit wins) `INFERRED`
- ChatRequest `EXTRACTED`
- Calling tools from code `INFERRED`
- post `EXTRACTED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*