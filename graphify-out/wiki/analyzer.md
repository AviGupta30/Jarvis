# analyzer

> 53 nodes · cohesion 0.10

## Key Concepts

- **analyzer.py** (47 connections) — `app/services/resume_replica/analyzer.py`
- **_hex()** (19 connections) — `app/services/resume_builder.py`
- **analyze_reference()** (14 connections) — `app/services/resume_replica/analyzer.py`
- **_build_scene_graph()** (13 connections) — `app/services/resume_replica/analyzer.py`
- **_build_section_heading_node()** (12 connections) — `app/services/resume_replica/analyzer.py`
- **_build_from_legacy()** (11 connections) — `app/services/resume_replica/analyzer.py`
- **_build_header_nodes()** (10 connections) — `app/services/resume_replica/analyzer.py`
- **_build_section_group()** (10 connections) — `app/services/resume_replica/analyzer.py`
- **_solid()** (10 connections) — `app/services/resume_replica/analyzer.py`
- **_build_experience_component()** (9 connections) — `app/services/resume_replica/analyzer.py`
- **_build_decor_nodes()** (8 connections) — `app/services/resume_replica/analyzer.py`
- **_llm_json()** (7 connections) — `app/services/resume_builder.py`
- **_build_style_registry()** (7 connections) — `app/services/resume_replica/analyzer.py`
- **_no_fill()** (7 connections) — `app/services/resume_replica/analyzer.py`
- **_path_commands()** (7 connections) — `app/services/resume_replica/analyzer.py`
- **_path_parametric()** (7 connections) — `app/services/resume_replica/analyzer.py`
- **_text_node()** (7 connections) — `app/services/resume_replica/analyzer.py`
- **_gemini()** (6 connections) — `app/services/resume_builder.py`
- **_make_section_nodes()** (6 connections) — `app/services/resume_replica/analyzer.py`
- **_vision_call()** (6 connections) — `app/services/resume_replica/analyzer.py`
- **_file_hash()** (5 connections) — `app/services/resume_builder.py`
- **_groq()** (5 connections) — `app/services/resume_builder.py`
- **_parse_json()** (5 connections) — `app/services/resume_builder.py`
- **_vision()** (5 connections) — `app/services/resume_builder.py`
- **_build_skills_node()** (5 connections) — `app/services/resume_replica/analyzer.py`
- *... and 28 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (26 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (8 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (2 shared connections)
- [resume_builder + exact_render](resume_builder_+_exact_render.md) (1 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (1 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/analyzer.py`

## Audit Trail

- EXTRACTED: 172 (99%)
- INFERRED: 2 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*