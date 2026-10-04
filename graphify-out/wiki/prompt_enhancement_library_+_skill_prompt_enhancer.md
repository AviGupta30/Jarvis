# prompt_enhancement_library + skill_prompt_enhancer

> 30 nodes · cohesion 0.12

## Key Concepts

- **skill_prompt_enhancer.py** (15 connections) — `app/services/skill_prompt_enhancer.py`
- **enhance_prompt_text()** (14 connections) — `app/services/skill_prompt_enhancer.py`
- **prompt_enhancement_library.py** (9 connections) — `app/services/prompt_enhancement_library.py`
- **enhance_prompt()** (9 connections) — `app/services/skill_prompt_enhancer.py`
- **Pipeline (`skill_prompt_enhancer.enhance_prompt_text`)** (8 connections) — `docs/features/prompt-enhancer.md`
- **Prompt enhancer (chat + floating Enhance button + Ctrl+Space overlay)** (7 connections) — `docs/features/prompt-enhancer.md`
- **protect_blocks()** (6 connections) — `app/services/prompt_enhancement_library.py`
- **check_for_hallucination()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **clean_output()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **is_bloated()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **restore_blocks()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **detect_domain()** (3 connections) — `app/services/prompt_enhancement_library.py`
- **_build_messages()** (3 connections) — `app/services/skill_prompt_enhancer.py`
- **_call_groq()** (2 connections) — `app/services/skill_prompt_enhancer.py`
- **_is_how_to()** (2 connections) — `app/services/skill_prompt_enhancer.py`
- **Gotchas** (2 connections) — `docs/features/prompt-enhancer.md`
- **_sub()** (1 connections) — `app/services/prompt_enhancement_library.py`
- **prompt_enhancement_library.py…** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Replace ``` fenced blocks with [[BLOCK_n]] placeholders.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Put protected blocks back; append any the model dropped.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Strip labels, wrapping quotes and code fences the model sometimes adds.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **True if the output looks like a chatbot reply rather than a rewritten prompt.…** (1 connections) — `app/services/prompt_enhancement_library.py`
- **True if the rewrite is far longer than the input warrants.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **skill_prompt_enhancer.py…** (1 connections) — `app/services/skill_prompt_enhancer.py`
- **Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header.** (1 connections) — `app/services/skill_prompt_enhancer.py`
- *... and 5 more nodes in this community*

## Relationships

- [prompt_enhancer_button](prompt_enhancer_button.md) (6 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/prompt_enhancement_library.py`
- `app/services/skill_prompt_enhancer.py`
- `docs/features/prompt-enhancer.md`

## Audit Trail

- EXTRACTED: 51 (81%)
- INFERRED: 12 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*