# file_ops

> 30 nodes · cohesion 0.10

## Key Concepts

- **file_ops.py** (21 connections) — `app/services/file_ops.py`
- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **_resolve_path()** (14 connections) — `app/services/file_ops.py`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **list_directory()** (6 connections) — `app/services/file_ops.py`
- **create_folder()** (5 connections) — `app/services/file_ops.py`
- **delete_file()** (5 connections) — `app/services/file_ops.py`
- **move_file()** (5 connections) — `app/services/file_ops.py`
- **search_files()** (5 connections) — `app/services/file_ops.py`
- **write_file()** (5 connections) — `app/services/file_ops.py`
- **append_file()** (4 connections) — `app/services/file_ops.py`
- **bulk_rename()** (4 connections) — `app/services/file_ops.py`
- **diff_files()** (4 connections) — `app/services/file_ops.py`
- **_fmt_size()** (4 connections) — `app/services/file_ops.py`
- **_maybe_summarize()** (3 connections) — `app/services/file_ops.py`
- **Path** (1 connections)
- **file_ops.py — Jarvis Full File System Operations (Step 4)…** (1 connections) — `app/services/file_ops.py`
- **Read and return the contents of a text file or PDF. Long files are…** (1 connections) — `app/services/file_ops.py`
- **For files longer than 1000 chars, generate an LLM summary AND return the raw…** (1 connections) — `app/services/file_ops.py`
- **Create a new file or overwrite an existing one with the given content.…** (1 connections) — `app/services/file_ops.py`
- **Append content to an existing file. Creates the file if it doesn't exist. A…** (1 connections) — `app/services/file_ops.py`
- **List all files and folders inside a directory. Returns name, type…** (1 connections) — `app/services/file_ops.py`
- **Move a file to a new location, or rename it. Both src and dst support path…** (1 connections) — `app/services/file_ops.py`
- **Move a file or folder to the Recycle Bin (NOT permanent delete). Blocks…** (1 connections) — `app/services/file_ops.py`
- **Recursively search for files matching a name or pattern within a directory.…** (1 connections) — `app/services/file_ops.py`
- *... and 5 more nodes in this community*

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (10 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (5 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [screen_vision](screen_vision.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [chat](chat.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (1 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (1 shared connections)

## Source Files

- `app/services/file_ops.py`
- `docs/KNOWN_ISSUES.md`

## Audit Trail

- EXTRACTED: 52 (61%)
- INFERRED: 33 (39%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*