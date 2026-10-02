# persistence + server

> 59 nodes · cohesion 0.05

## Key Concepts

- **server.py** (20 connections) — `neural_cache/server.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **WALWriter** (14 connections) — `neural_cache/persistence.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **SnapshotManager** (13 connections) — `neural_cache/persistence.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **queue** (6 connections)
- **.__init__()** (5 connections) — `neural_cache/server.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.__init__()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- **.start_background_thread()** (4 connections) — `neural_cache/persistence.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **random** (4 connections)
- **.__init__()** (3 connections) — `neural_cache/persistence.py`
- **.read()** (3 connections) — `neural_cache/persistence.py`
- **.write()** (3 connections) — `neural_cache/persistence.py`
- **.append()** (3 connections) — `neural_cache/persistence.py`
- **.read_all()** (3 connections) — `neural_cache/persistence.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- *... and 34 more nodes in this community*

## Relationships

- [engine + test_protocol](engine_+_test_protocol.md) (11 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (10 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (5 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (3 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (3 shared connections)
- [client](client.md) (3 shared connections)
- [test_protocol](test_protocol.md) (2 shared connections)
- [lru + test_lru](lru_+_test_lru.md) (2 shared connections)
- [test_concurrency](test_concurrency.md) (2 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)

## Source Files

- `neural_cache/client.py`
- `neural_cache/engine.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 121 (93%)
- INFERRED: 9 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*