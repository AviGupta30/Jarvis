# message_reader + thread_extractor

> 72 nodes · cohesion 0.05

## Key Concepts

- **time** (52 connections)
- **typing** (30 connections)
- **pathlib** (28 connections)
- **threading** (22 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **test_lru.py** (16 connections) — `neural_cache/tests/test_lru.py`
- **pyautogui** (15 connections)
- **logging** (14 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **pyperclip** (8 connections)
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **pygetwindow** (7 connections)
- **queue** (7 connections)
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- *... and 47 more nodes in this community*

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (29 shared connections)
- [persistence + server](persistence_+_server.md) (13 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (10 shared connections)
- [refresh_docs + whatsapp](refresh_docs_+_whatsapp.md) (9 shared connections)
- [tools](tools.md) (8 shared connections)
- [test_lru](test_lru.md) (8 shared connections)
- [whatsapp_smart + whatsapp_call](whatsapp_smart_+_whatsapp_call.md) (6 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (5 shared connections)
- [lru](lru.md) (5 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (5 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (4 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `neural_cache/benchmark.py`
- `neural_cache/client.py`
- `neural_cache/engine.py`
- `neural_cache/lru.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`
- `neural_cache/tests/test_lru.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 331 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*