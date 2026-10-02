# file_ops

> 30 nodes · cohesion 0.10

## Key Concepts

- **file_ops.py** (21 connections) — `app/services/file_ops.py`
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
- **Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).…** (1 connections) — `app/services/file_ops.py`
- *... and 5 more nodes in this community*

## Relationships

- [tools](tools.md) (10 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (5 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [main](main.md) (1 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)

## Source Files

- `app/services/file_ops.py`

## Audit Trail

- EXTRACTED: 51 (73%)
- INFERRED: 19 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*