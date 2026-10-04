# calendar_tool + email-calendar

> 21 nodes · cohesion 0.11

## Key Concepts

- **datetime** (11 connections)
- **calendar_tool.py** (8 connections) — `app/services/calendar_tool.py`
- **check_today_schedule()** (8 connections) — `app/services/calendar_tool.py`
- **Email, calendar & morning brief** (8 connections) — `docs/features/email-calendar.md`
- **_get_calendar_service()** (6 connections) — `app/services/calendar_tool.py`
- **get_morning_brief()** (6 connections) — `app/services/memory_tool.py`
- **add_event()** (5 connections) — `app/services/calendar_tool.py`
- **get_upcoming_events()** (5 connections) — `app/services/calendar_tool.py`
- **Calendar** (2 connections) — `docs/features/email-calendar.md`
- **Morning brief** (2 connections) — `docs/features/email-calendar.md`
- **calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…** (1 connections) — `app/services/calendar_tool.py`
- **Create a new event in Google Calendar. - title: "Project Meeting" - date:…** (1 connections) — `app/services/calendar_tool.py`
- **Authenticate and return a Google Calendar API service object.** (1 connections) — `app/services/calendar_tool.py`
- **List events in the next N days.** (1 connections) — `app/services/calendar_tool.py`
- **What's on today's agenda, with time remaining until each event.** (1 connections) — `app/services/calendar_tool.py`
- **Generates a smart, narrative morning briefing via LLM. Pulls calendar and email…** (1 connections) — `app/services/memory_tool.py`
- **email-calendar.md** (1 connections) — `docs/features/email-calendar.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/email-calendar.md`
- **Gotchas** (1 connections) — `docs/features/email-calendar.md`
- **Graphify** (1 connections) — `docs/features/email-calendar.md`
- **Purpose** (1 connections) — `docs/features/email-calendar.md`

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (5 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [memory_tool + memory](memory_tool_+_memory.md) (3 shared connections)
- [gmail_tool](gmail_tool.md) (2 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [analyzer](analyzer.md) (1 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (1 shared connections)
- [style_profiler](style_profiler.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)

## Source Files

- `app/services/calendar_tool.py`
- `app/services/memory_tool.py`
- `docs/features/email-calendar.md`

## Audit Trail

- EXTRACTED: 38 (79%)
- INFERRED: 10 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*