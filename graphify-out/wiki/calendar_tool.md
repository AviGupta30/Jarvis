# calendar_tool

> 14 nodes · cohesion 0.18

## Key Concepts

- **datetime** (10 connections)
- **calendar_tool.py** (8 connections) — `app/services/calendar_tool.py`
- **check_today_schedule()** (8 connections) — `app/services/calendar_tool.py`
- **_get_calendar_service()** (6 connections) — `app/services/calendar_tool.py`
- **get_morning_brief()** (6 connections) — `app/services/memory_tool.py`
- **add_event()** (5 connections) — `app/services/calendar_tool.py`
- **get_upcoming_events()** (5 connections) — `app/services/calendar_tool.py`
- **Morning brief** (2 connections) — `docs/features/email-calendar.md`
- **calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…** (1 connections) — `app/services/calendar_tool.py`
- **Create a new event in Google Calendar. - title: "Project Meeting" - date:…** (1 connections) — `app/services/calendar_tool.py`
- **Authenticate and return a Google Calendar API service object.** (1 connections) — `app/services/calendar_tool.py`
- **List events in the next N days.** (1 connections) — `app/services/calendar_tool.py`
- **What's on today's agenda, with time remaining until each event.** (1 connections) — `app/services/calendar_tool.py`
- **Generates a smart, narrative morning briefing via LLM. Pulls calendar and email…** (1 connections) — `app/services/memory_tool.py`

## Relationships

- [tools](tools.md) (5 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (4 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [memory_tool](memory_tool.md) (3 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (2 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [gmail_tool + download_kokoro](gmail_tool_+_download_kokoro.md) (1 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)

## Source Files

- `app/services/calendar_tool.py`
- `app/services/memory_tool.py`
- `docs/features/email-calendar.md`

## Audit Trail

- EXTRACTED: 30 (75%)
- INFERRED: 10 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*