# ui_inspector + tools

> 23 nodes · cohesion 0.09

## Key Concepts

- **ui_inspector.py** (18 connections) — `app/services/ui_inspector.py`
- **click_ui_element_uia()** (6 connections) — `app/services/tools.py`
- **dump_app_ui_tree()** (6 connections) — `app/services/tools.py`
- **read_ui_element_text()** (6 connections) — `app/services/tools.py`
- **send_to_copilot()** (6 connections) — `app/services/tools.py`
- **type_into_ui_element()** (6 connections) — `app/services/tools.py`
- **click_ui_element()** (6 connections) — `app/services/ui_inspector.py`
- **debug_ui_tree()** (5 connections) — `app/services/ui_inspector.py`
- **read_element_text()** (4 connections) — `app/services/ui_inspector.py`
- **smart_click()** (4 connections) — `app/services/ui_inspector.py`
- **type_into_element()** (4 connections) — `app/services/ui_inspector.py`
- **dump_spotify.py** (4 connections) — `dump_spotify.py`
- **Click a UI element inside an app by AutomationId, name, or control type. Does…** (1 connections) — `app/services/tools.py`
- **Inject text into a specific input field in an app via UIA Value pattern. No…** (1 connections) — `app/services/tools.py`
- **Read the current text content of a UI element — e.g. a terminal output pane, a…** (1 connections) — `app/services/tools.py`
- **Dump the full Windows UI Automation accessibility tree of an app window. Use…** (1 connections) — `app/services/tools.py`
- **Type a question into the Windows Copilot sidebar and retrieve the response.…** (1 connections) — `app/services/tools.py`
- **ui_inspector.py — Jarvis UIA Engine (Upgraded)…** (1 connections) — `app/services/ui_inspector.py`
- **Legacy-compatible API: find a control by text in the active window and click…** (1 connections) — `app/services/ui_inspector.py`
- **Click a UI element by AutomationId, name, or control type inside an app. Does…** (1 connections) — `app/services/ui_inspector.py`
- **Inject text into a specific input field in an app via UIA Value pattern. No…** (1 connections) — `app/services/ui_inspector.py`
- **Read the current text content of a UI element (e.g. terminal output pane,…** (1 connections) — `app/services/ui_inspector.py`
- **Dump the full accessibility tree of an app window as a readable string. Use…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [tools](tools.md) (15 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (5 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (5 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (3 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (2 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [uia_local](uia_local.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `dump_spotify.py`

## Audit Trail

- EXTRACTED: 42 (67%)
- INFERRED: 21 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*