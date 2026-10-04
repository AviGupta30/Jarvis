# server

> 24 nodes · cohesion 0.11

## Key Concepts

- **threading** (22 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **CacheServer** (14 connections) — `neural_cache/server.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **._accept_loop()** (4 connections) — `neural_cache/server.py`
- **.start()** (4 connections) — `neural_cache/server.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **._recover_state()** (3 connections) — `neural_cache/server.py`
- **._shutdown()** (3 connections) — `neural_cache/server.py`
- **main()** (3 connections) — `neural_cache/server.py`
- **socket** (3 connections)
- **neural_cache** (2 connections)
- **acoustic_tripwire.py — Jarvis Acoustic Wake Engine…** (1 connections) — `app/services/acoustic_tripwire.py`
- **client.py — Python Client Library for Neural Cache (Milestone 5)…** (1 connections) — `neural_cache/client.py`
- **_sigint()** (1 connections) — `neural_cache/server.py`
- **server.py — TCP Accept Loop for Neural Cache (Milestone 4)…** (1 connections) — `neural_cache/server.py`
- **Full startup: recover state, start engine, begin accepting connections.** (1 connections) — `neural_cache/server.py`
- **Restore cache state from disk before the engine thread starts. Called on the…** (1 connections) — `neural_cache/server.py`
- **Main thread: bind socket and accept connections indefinitely.** (1 connections) — `neural_cache/server.py`
- **One thread per connected client. Reads commands, enqueues them to the engine,…** (1 connections) — `neural_cache/server.py`
- **Graceful shutdown: take a final snapshot, stop engine, close socket.** (1 connections) — `neural_cache/server.py`
- **TCP server that wires incoming connections to the CacheEngine. Each accepted…** (1 connections) — `neural_cache/server.py`
- **signal** (1 connections)

## Relationships

- [persistence](persistence.md) (7 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (6 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [benchmark](benchmark.md) (3 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (2 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (2 shared connections)
- [test_protocol](test_protocol.md) (2 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (2 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `neural_cache/client.py`
- `neural_cache/server.py`

## Audit Trail

- EXTRACTED: 80 (94%)
- INFERRED: 5 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*