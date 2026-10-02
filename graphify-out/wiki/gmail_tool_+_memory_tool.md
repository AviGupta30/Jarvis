# gmail_tool + memory_tool

> 52 nodes · cohesion 0.06

## Key Concepts

- **gmail_tool.py** (17 connections) — `app/services/gmail_tool.py`
- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **check_today_schedule()** (8 connections) — `app/services/calendar_tool.py`
- **Email, calendar & morning brief** (8 connections) — `docs/features/email-calendar.md`
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
- *... and 27 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (10 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (7 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)

## Source Files

- `app/services/calendar_tool.py`
- `app/services/gmail_tool.py`
- `app/services/memory_tool.py`
- `docs/features/email-calendar.md`
- `docs/features/memory.md`
- `test_gmail.py`

## Audit Trail

- EXTRACTED: 96 (86%)
- INFERRED: 16 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*