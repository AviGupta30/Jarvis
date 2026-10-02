# media_sessions

> 22 nodes · cohesion 0.16

## Key Concepts

- **media_sessions.py** (18 connections) — `app/services/media_sessions.py`
- **control()** (11 connections) — `app/services/media_sessions.py`
- **media_command()** (8 connections) — `app/services/media_sessions.py`
- **set_last()** (8 connections) — `app/services/media_state.py`
- **sessions()** (7 connections) — `app/services/media_sessions.py`
- **_label()** (4 connections) — `app/services/media_sessions.py`
- **_run()** (4 connections) — `app/services/media_sessions.py`
- **run()** (3 connections) — `app/services/media_sessions.py`
- **_filter()** (3 connections) — `app/services/media_sessions.py`
- **_sessions_async()** (3 connections) — `app/services/media_sessions.py`
- **app_kind()** (2 connections) — `app/services/media_sessions.py`
- **_do()** (2 connections) — `app/services/media_sessions.py`
- **kind_playing()** (2 connections) — `app/services/media_sessions.py`
- **rank()** (1 connections) — `app/services/media_sessions.py`
- **media_sessions.py — control whatever is ACTUALLY playing (helper, not a tool)…** (1 connections) — `app/services/media_sessions.py`
- **action: pause | play | next | previous | toggle app: None (anything) |…** (1 connections) — `app/services/media_sessions.py`
- **# NOTE: the reported playback status lags (Edge: ~2 s after a pause it still…** (1 connections) — `app/services/media_sessions.py`
- **Tool entry (registered as `media_control` in TOOL_REGISTRY): pause / resume /…** (1 connections) — `app/services/media_sessions.py`
- **Run a coroutine from sync code (we're on the media worker thread, no running…** (1 connections) — `app/services/media_sessions.py`
- **[{app_id, kind: spotify|browser|other, status: playing|paused|…, title, artist,…** (1 connections) — `app/services/media_sessions.py`
- **app: 'spotify' | 'youtube'.** (1 connections) — `app/services/media_state.py`
- **onnxruntime** (1 connections)

## Relationships

- [chat + llm](chat_+_llm.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [spotify_service](spotify_service.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [window_layout](window_layout.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`
- `app/services/media_state.py`

## Audit Trail

- EXTRACTED: 47 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*