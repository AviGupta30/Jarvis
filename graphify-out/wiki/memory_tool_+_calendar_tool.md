# memory_tool + calendar_tool

> 34 nodes · cohesion 0.09

## Key Concepts

- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **datetime** (10 connections)
- **calendar_tool.py** (8 connections) — `app/services/calendar_tool.py`
- **check_today_schedule()** (8 connections) — `app/services/calendar_tool.py`
- **forget_fact()** (7 connections) — `app/services/memory_tool.py`
- **_load_memory()** (7 connections) — `app/services/memory_tool.py`
- **Purpose** (7 connections) — `docs/features/memory.md`
- **_get_calendar_service()** (6 connections) — `app/services/calendar_tool.py`
- **get_morning_brief()** (6 connections) — `app/services/memory_tool.py`
- **recall_facts()** (6 connections) — `app/services/memory_tool.py`
- **save_fact()** (6 connections) — `app/services/memory_tool.py`
- **update_fact()** (6 connections) — `app/services/memory_tool.py`
- **add_event()** (5 connections) — `app/services/calendar_tool.py`
- **get_upcoming_events()** (5 connections) — `app/services/calendar_tool.py`
- **get_all_facts_as_context()** (5 connections) — `app/services/memory_tool.py`
- **_save_memory()** (5 connections) — `app/services/memory_tool.py`
- **remember_preference()** (5 connections) — `app/services/tools.py`
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **Morning brief** (2 connections) — `docs/features/email-calendar.md`
- **calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…** (1 connections) — `app/services/calendar_tool.py`
- **Create a new event in Google Calendar. - title: "Project Meeting" - date:…** (1 connections) — `app/services/calendar_tool.py`
- **Authenticate and return a Google Calendar API service object.** (1 connections) — `app/services/calendar_tool.py`
- **List events in the next N days.** (1 connections) — `app/services/calendar_tool.py`
- **What's on today's agenda, with time remaining until each event.** (1 connections) — `app/services/calendar_tool.py`
- *... and 9 more nodes in this community*

## Relationships

- [tools](tools.md) (11 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (3 shared connections)
- [gmail_tool](gmail_tool.md) (3 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [server + protocol](server_+_protocol.md) (2 shared connections)
- [email-calendar + tools](email-calendar_+_tools.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (2 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)

## Source Files

- `app/services/calendar_tool.py`
- `app/services/memory_tool.py`
- `app/services/tools.py`
- `docs/features/email-calendar.md`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 66 (75%)
- INFERRED: 22 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*