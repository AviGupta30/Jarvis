# gmail_tool + memory_tool

> 42 nodes · cohesion 0.08

## Key Concepts

- **gmail_tool.py** (17 connections) — `app/services/gmail_tool.py`
- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **check_emails()** (7 connections) — `app/services/gmail_tool.py`
- **summarize_inbox()** (7 connections) — `app/services/gmail_tool.py`
- **forget_fact()** (7 connections) — `app/services/memory_tool.py`
- **_load_memory()** (7 connections) — `app/services/memory_tool.py`
- **Purpose** (7 connections) — `docs/features/memory.md`
- **_format_date()** (6 connections) — `app/services/gmail_tool.py`
- **get_email_body()** (6 connections) — `app/services/gmail_tool.py`
- **_get_gmail_service()** (6 connections) — `app/services/gmail_tool.py`
- **_get_header()** (6 connections) — `app/services/gmail_tool.py`
- **list_unread()** (6 connections) — `app/services/gmail_tool.py`
- **get_morning_brief()** (6 connections) — `app/services/memory_tool.py`
- **recall_facts()** (6 connections) — `app/services/memory_tool.py`
- **save_fact()** (6 connections) — `app/services/memory_tool.py`
- **update_fact()** (6 connections) — `app/services/memory_tool.py`
- **_decode_body()** (5 connections) — `app/services/gmail_tool.py`
- **get_all_facts_as_context()** (5 connections) — `app/services/memory_tool.py`
- **_save_memory()** (5 connections) — `app/services/memory_tool.py`
- **test_gmail.py** (5 connections) — `test_gmail.py`
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_truncate()** (3 connections) — `app/services/gmail_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **Morning brief** (2 connections) — `docs/features/email-calendar.md`
- **gmail_tool.py — Jarvis Gmail Integration (Step 5)…** (1 connections) — `app/services/gmail_tool.py`
- *... and 17 more nodes in this community*

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (8 shared connections)
- [tools](tools.md) (6 shared connections)
- [calendar_tool](calendar_tool.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)
- [download_kokoro](download_kokoro.md) (1 shared connections)

## Source Files

- `app/services/gmail_tool.py`
- `app/services/memory_tool.py`
- `docs/features/email-calendar.md`
- `docs/features/memory.md`
- `test_gmail.py`

## Audit Trail

- EXTRACTED: 86 (88%)
- INFERRED: 12 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*