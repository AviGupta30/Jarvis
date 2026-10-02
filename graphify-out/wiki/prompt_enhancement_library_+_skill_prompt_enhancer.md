# prompt_enhancement_library + skill_prompt_enhancer

> 22 nodes · cohesion 0.17

## Key Concepts

- **skill_prompt_enhancer.py** (15 connections) — `app/services/skill_prompt_enhancer.py`
- **enhance_prompt_text()** (14 connections) — `app/services/skill_prompt_enhancer.py`
- **prompt_enhancement_library.py** (9 connections) — `app/services/prompt_enhancement_library.py`
- **Pipeline (`skill_prompt_enhancer.enhance_prompt_text`)** (8 connections) — `docs/features/prompt-enhancer.md`
- **protect_blocks()** (6 connections) — `app/services/prompt_enhancement_library.py`
- **check_for_hallucination()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **clean_output()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **is_bloated()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **restore_blocks()** (5 connections) — `app/services/prompt_enhancement_library.py`
- **detect_domain()** (3 connections) — `app/services/prompt_enhancement_library.py`
- **_build_messages()** (3 connections) — `app/services/skill_prompt_enhancer.py`
- **_call_groq()** (2 connections) — `app/services/skill_prompt_enhancer.py`
- **_is_how_to()** (2 connections) — `app/services/skill_prompt_enhancer.py`
- **_sub()** (1 connections) — `app/services/prompt_enhancement_library.py`
- **prompt_enhancement_library.py…** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Replace ``` fenced blocks with [[BLOCK_n]] placeholders.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Put protected blocks back; append any the model dropped.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **Strip labels, wrapping quotes and code fences the model sometimes adds.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **True if the output looks like a chatbot reply rather than a rewritten prompt.…** (1 connections) — `app/services/prompt_enhancement_library.py`
- **True if the rewrite is far longer than the input warrants.** (1 connections) — `app/services/prompt_enhancement_library.py`
- **skill_prompt_enhancer.py…** (1 connections) — `app/services/skill_prompt_enhancer.py`
- **Return the enhanced prompt as plain text (no header). Raises on Groq/API…** (1 connections) — `app/services/skill_prompt_enhancer.py`

## Relationships

- [tools](tools.md) (4 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (3 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)
- [prompt_enhancer_button + prompt-enhancer](prompt_enhancer_button_+_prompt-enhancer.md) (2 shared connections)

## Source Files

- `app/services/prompt_enhancement_library.py`
- `app/services/skill_prompt_enhancer.py`
- `docs/features/prompt-enhancer.md`

## Audit Trail

- EXTRACTED: 42 (82%)
- INFERRED: 9 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*