# screen_reader + screen_vision

> 6 nodes · cohesion 0.33

## Key Concepts

- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **_classify_intent()** (5 connections) — `app/services/screen_vision.py`
- **read_my_screen()** (4 connections) — `app/services/tools.py`
- **Tool-callable version — called when user asks 'what's on my screen?' Routes…** (1 connections) — `app/services/screen_reader.py`
- **Parse the user's phrasing to determine the response mode. describe → "What am I…** (1 connections) — `app/services/screen_vision.py`
- **Read and describe the current screen using the VLM pipeline. Routes to the…** (1 connections) — `app/services/tools.py`

## Relationships

- [screen_reader](screen_reader.md) (3 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [screen_vision](screen_vision.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 13 (87%)
- INFERRED: 2 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*