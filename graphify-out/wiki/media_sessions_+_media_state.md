# media_sessions + media_state

> 29 nodes · cohesion 0.11

## Key Concepts

- **media_sessions.py** (18 connections) — `app/services/media_sessions.py`
- **control()** (11 connections) — `app/services/media_sessions.py`
- **media_state.py** (9 connections) — `app/services/media_state.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **media_command()** (8 connections) — `app/services/media_sessions.py`
- **set_last()** (8 connections) — `app/services/media_state.py`
- **sessions()** (7 connections) — `app/services/media_sessions.py`
- **spotify_running()** (6 connections) — `app/services/media_state.py`
- **_label()** (4 connections) — `app/services/media_sessions.py`
- **_run()** (4 connections) — `app/services/media_sessions.py`
- **run()** (3 connections) — `app/services/media_sessions.py`
- **_filter()** (3 connections) — `app/services/media_sessions.py`
- **_sessions_async()** (3 connections) — `app/services/media_sessions.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
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
- **media_state.py — which media app the user used last (Spotify or YouTube)…** (1 connections) — `app/services/media_state.py`
- *... and 4 more nodes in this community*

## Relationships

- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (6 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [window_layout + tools](window_layout_+_tools.md) (2 shared connections)
- [spotify_service](spotify_service.md) (2 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`
- `app/services/media_state.py`
- `app/services/youtube_control.py`

## Audit Trail

- EXTRACTED: 68 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*