# ppt_research

> 37 nodes · cohesion 0.11

## Key Concepts

- **ppt_research.py** (29 connections) — `app/services/ppt_research.py`
- **ground_slides()** (16 connections) — `app/services/ppt_content.py`
- **numbers_in()** (10 connections) — `app/services/ppt_research.py`
- **Anti-hallucination for AI-written decks (`ppt_research.py` + `ppt_content.ground_slides`)** (9 connections) — `docs/features/ppt.md`
- **gather_sources()** (8 connections) — `app/services/ppt_research.py`
- **scrub_slide()** (8 connections) — `app/services/ppt_research.py`
- **_toks()** (8 connections) — `app/services/ppt_research.py`
- **audit_slide()** (7 connections) — `app/services/ppt_research.py`
- **extract_facts()** (7 connections) — `app/services/ppt_research.py`
- **relevant_facts()** (7 connections) — `app/services/ppt_research.py`
- **research_facts()** (6 connections) — `app/services/ppt_content.py`
- **_anchors()** (5 connections) — `app/services/ppt_research.py`
- **sources_note()** (5 connections) — `app/services/ppt_research.py`
- **strip_fact_ids()** (5 connections) — `app/services/ppt_research.py`
- **_walk_texts()** (5 connections) — `app/services/ppt_research.py`
- **plan_queries()** (4 connections) — `app/services/ppt_content.py`
- **wiki_pages()** (4 connections) — `app/services/ppt_research.py`
- **allowed_numbers()** (3 connections) — `app/services/ppt_research.py`
- **_drop_clauses()** (3 connections) — `app/services/ppt_research.py`
- **fetch_page()** (3 connections) — `app/services/ppt_research.py`
- **web_search()** (3 connections) — `app/services/ppt_research.py`
- **_clean_html()** (2 connections) — `app/services/ppt_research.py`
- **_norm_num()** (2 connections) — `app/services/ppt_research.py`
- **_sentences()** (2 connections) — `app/services/ppt_research.py`
- **4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…** (1 connections) — `app/services/ppt_content.py`
- *... and 12 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (20 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [web_search + tools](web_search_+_tools.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (1 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_research.py`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 88 (87%)
- INFERRED: 13 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*