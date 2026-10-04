# benchmark + server

> 51 nodes · cohesion 0.06

## Key Concepts

- **os** (62 connections)
- **time** (52 connections)
- **pathlib** (28 connections)
- **threading** (22 connections)
- **server.py** (20 connections) — `neural_cache/server.py`
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **test_concurrency.py** (16 connections) — `neural_cache/tests/test_concurrency.py`
- **logging** (14 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **fonts.py** (13 connections) — `app/services/resume_replica/fonts.py`
- **prompt_overlay.py** (12 connections) — `app/services/prompt_overlay.py`
- **client.py** (12 connections) — `neural_cache/client.py`
- **replica_eval.py** (12 connections) — `scripts/replica_eval.py`
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **media_state.py** (9 connections) — `app/services/media_state.py`
- **JSONFileBaseline** (7 connections) — `neural_cache/benchmark.py`
- **main()** (7 connections) — `neural_cache/benchmark.py`
- **queue** (7 connections)
- **measure_throughput()** (4 connections) — `neural_cache/benchmark.py`
- **html** (3 connections)
- **measure_latency()** (3 connections) — `neural_cache/benchmark.py`
- **._handle_client()** (3 connections) — `neural_cache/server.py`
- **socket** (3 connections)
- **main()** (2 connections) — `app/services/prompt_overlay.py`
- **argparse** (2 connections)
- *... and 26 more nodes in this community*

## Relationships

- [server + persistence](server_+_persistence.md) (16 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (10 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (7 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (6 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (6 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (6 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (5 shared connections)
- [chat + llm](chat_+_llm.md) (5 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (5 shared connections)
- [resume_builder](resume_builder.md) (5 shared connections)
- [voice](voice.md) (5 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `app/services/media_state.py`
- `app/services/prompt_overlay.py`
- `app/services/resume_replica/fonts.py`
- `neural_cache/benchmark.py`
- `neural_cache/client.py`
- `neural_cache/persistence.py`
- `neural_cache/server.py`
- `neural_cache/tests/test_concurrency.py`
- `scripts/replica_eval.py`

## Audit Trail

- EXTRACTED: 303 (99%)
- INFERRED: 3 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*