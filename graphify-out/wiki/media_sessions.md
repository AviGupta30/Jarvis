# media_sessions

> 20 nodes · cohesion 0.17

## Key Concepts

- **media_sessions.py** (18 connections) — `app/services/media_sessions.py`
- **control()** (11 connections) — `app/services/media_sessions.py`
- **media_command()** (8 connections) — `app/services/media_sessions.py`
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
- **onnxruntime** (1 connections)

## Relationships

- [media_state + youtube_control](media_state_+_youtube_control.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`

## Audit Trail

- EXTRACTED: 41 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*