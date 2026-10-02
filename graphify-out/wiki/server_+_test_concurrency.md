# server + test_concurrency

> 31 nodes · cohesion 0.09

## Key Concepts

- **server.py** (20 connections) — `neural_cache/server.py`
- **threading** (19 connections)
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **live_server()** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **random** (4 connections)
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **socket** (3 connections)
- **neural_cache** (2 connections)
- **acoustic_tripwire.py — Jarvis Acoustic Wake Engine…** (1 connections) — `app/services/acoustic_tripwire.py`
- **argparse** (1 connections)
- **client.py — Python Client Library for Neural Cache (Milestone 5)…** (1 connections) — `neural_cache/client.py`
- **_sigint()** (1 connections) — `neural_cache/server.py`
- **server.py — TCP Accept Loop for Neural Cache (Milestone 4)…** (1 connections) — `neural_cache/server.py`
- **Full startup: recover state, start engine, begin accepting connections.** (1 connections) — `neural_cache/server.py`
- **Restore cache state from disk before the engine thread starts. Called on the…** (1 connections) — `neural_cache/server.py`
- **Main thread: bind socket and accept connections indefinitely.** (1 connections) — `neural_cache/server.py`
- **One thread per connected client. Reads commands, enqueues them to the engine,…** (1 connections) — `neural_cache/server.py`
- *... and 6 more nodes in this community*

## Relationships

- [persistence](persistence.md) (9 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (5 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (4 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (3 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (3 shared connections)
- [benchmark](benchmark.md) (3 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [reply_generator](reply_generator.md) (2 shared connections)
- [test_protocol](test_protocol.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `neural_cache/client.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 94 (94%)
- INFERRED: 6 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*