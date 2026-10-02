# file_ops

> 26 nodes · cohesion 0.11

## Key Concepts

- **file_ops.py** (21 connections) — `app/services/file_ops.py`
- **_resolve_path()** (14 connections) — `app/services/file_ops.py`
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
- **Path** (1 connections)
- **file_ops.py — Jarvis Full File System Operations (Step 4)…** (1 connections) — `app/services/file_ops.py`
- **Create a new file or overwrite an existing one with the given content.…** (1 connections) — `app/services/file_ops.py`
- **Append content to an existing file. Creates the file if it doesn't exist. A…** (1 connections) — `app/services/file_ops.py`
- **List all files and folders inside a directory. Returns name, type…** (1 connections) — `app/services/file_ops.py`
- **Move a file to a new location, or rename it. Both src and dst support path…** (1 connections) — `app/services/file_ops.py`
- **Move a file or folder to the Recycle Bin (NOT permanent delete). Blocks…** (1 connections) — `app/services/file_ops.py`
- **Recursively search for files matching a name or pattern within a directory.…** (1 connections) — `app/services/file_ops.py`
- **Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).…** (1 connections) — `app/services/file_ops.py`
- **Rename all files in a folder whose names contain 'find', replacing it with…** (1 connections) — `app/services/file_ops.py`
- **Compare two text files and return a summary of what changed. Shows added and…** (1 connections) — `app/services/file_ops.py`
- **Convert a user-friendly path to an absolute Path object. Handles: -…** (1 connections) — `app/services/file_ops.py`
- **Human-readable file size.** (1 connections) — `app/services/file_ops.py`
- *... and 1 more nodes in this community*

## Relationships

- [tools](tools.md) (9 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (4 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (3 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (2 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)

## Source Files

- `app/services/file_ops.py`

## Audit Trail

- EXTRACTED: 45 (75%)
- INFERRED: 15 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*