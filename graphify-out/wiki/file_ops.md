# file_ops

> 27 nodes · cohesion 0.11

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
- **_maybe_summarize()** (3 connections) — `app/services/file_ops.py`
- **Path** (1 connections)
- **file_ops.py — Jarvis Full File System Operations (Step 4)…** (1 connections) — `app/services/file_ops.py`
- **For files longer than 1000 chars, generate an LLM summary AND return the raw…** (1 connections) — `app/services/file_ops.py`
- **Create a new file or overwrite an existing one with the given content.…** (1 connections) — `app/services/file_ops.py`
- **Append content to an existing file. Creates the file if it doesn't exist. A…** (1 connections) — `app/services/file_ops.py`
- **List all files and folders inside a directory. Returns name, type…** (1 connections) — `app/services/file_ops.py`
- **Move a file to a new location, or rename it. Both src and dst support path…** (1 connections) — `app/services/file_ops.py`
- **Move a file or folder to the Recycle Bin (NOT permanent delete). Blocks…** (1 connections) — `app/services/file_ops.py`
- **Recursively search for files matching a name or pattern within a directory.…** (1 connections) — `app/services/file_ops.py`
- **Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).…** (1 connections) — `app/services/file_ops.py`
- **Rename all files in a folder whose names contain 'find', replacing it with…** (1 connections) — `app/services/file_ops.py`
- **Compare two text files and return a summary of what changed. Shows added and…** (1 connections) — `app/services/file_ops.py`
- *... and 2 more nodes in this community*

## Relationships

- [tools](tools.md) (9 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (4 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (1 shared connections)

## Source Files

- `app/services/file_ops.py`

## Audit Trail

- EXTRACTED: 47 (76%)
- INFERRED: 15 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*