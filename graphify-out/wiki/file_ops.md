# file_ops

> 29 nodes · cohesion 0.10

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
- **shutil** (3 connections)
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
- *... and 4 more nodes in this community*

## Relationships

- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (13 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)

## Source Files

- `app/services/file_ops.py`

## Audit Trail

- EXTRACTED: 49 (77%)
- INFERRED: 15 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*