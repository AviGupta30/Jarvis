# persistence + server

> 72 nodes · cohesion 0.05

## Key Concepts

- **time** (46 connections)
- **typing** (29 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **threading** (19 connections)
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **logging** (14 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **queue** (6 connections)
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **.__init__()** (3 connections) — `neural_cache/persistence.py`
- *... and 47 more nodes in this community*

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (15 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (13 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (13 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (11 shared connections)
- [test_lru + lru](test_lru_+_lru.md) (9 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [client](client.md) (4 shared connections)
- [benchmark](benchmark.md) (4 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (4 shared connections)
- [syllabus_auditor](syllabus_auditor.md) (3 shared connections)
- [voice](voice.md) (3 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `neural_cache/benchmark.py`
- `neural_cache/client.py`
- `neural_cache/engine.py`
- `neural_cache/lru.py`
- `neural_cache/persistence.py`
- `neural_cache/protocol.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 253 (97%)
- INFERRED: 9 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*