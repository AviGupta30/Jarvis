# prompt_enhancement_library + skill_prompt_enhancer

> 24 nodes · cohesion 0.16

## Key Concepts

- **skill_prompt_enhancer.py** (15 connections) — `app/services/skill_prompt_enhancer.py`
- **enhance_prompt_text()** (14 connections) — `app/services/skill_prompt_enhancer.py`
- **prompt_enhancement_library.py** (9 connections) — `app/services/prompt_enhancement_library.py`
- **enhance_prompt()** (9 connections) — `app/services/skill_prompt_enhancer.py`
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
- **Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header.** (1 connections) — `app/services/skill_prompt_enhancer.py`
- **Return the enhanced prompt as plain text (no header). Raises on Groq/API…** (1 connections) — `app/services/skill_prompt_enhancer.py`

## Relationships

- [prompt-enhancer + prompt_enhancer_button](prompt-enhancer_+_prompt_enhancer_button.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/prompt_enhancement_library.py`
- `app/services/skill_prompt_enhancer.py`
- `docs/features/prompt-enhancer.md`

## Audit Trail

- EXTRACTED: 45 (80%)
- INFERRED: 11 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*