# Assignment solver (5 phases)

## Purpose
Solve an assignment PDF/DOCX end-to-end, or run any phase alone.

## Phases
1. `assignment_tool.extract_questions(pdf_path)`: 3 tracks (numbered-question regex with sub-questions, page images → vision model, LLM text) → `_merge_and_deduplicate`. `_resolve_pdf_path` accepts a partial name (searches Desktop/Documents/Downloads). `list_assignments()` lists candidate PDFs.
2. `assignment_answers.generate_answers(questions_json, pdf_path)`: Playwright persistent-profile visible browser on AI sites (Gemini → ChatGPT → DeepSeek; uploads the PDF, asks each question, copy-button/DOM/screenshot-vision extraction) → Groq fallback. `generate_answer(question)` = Groq only.
3. `assignment_humanizer.humanize_all_answers(qa_json)` / `humanize_text`: paraphraser sites via browser in chunks, protecting code/math placeholders → Groq fallback.
4. `assignment_assembler.assemble_assignment(qa_json, filename, format_type)`: Word or PPTX.
5. `assignment_pipeline.do_assignment(pdf_path, output_format, humanize)`: master orchestrator; Playwright runs in a background thread (Edge/Chrome profile → Jarvis profile); streams progress.

## Triggers
"do/complete my assignment [file] [ppt]", "extract questions from x.pdf", "list my assignments", "answer this question: …", "humanize answers", "assemble assignment". The router has `do_assignment`, `extract_questions`, `list_assignments`, `generate_answer`.

## Gotchas
- Browsers are visible and rely on logged-in sessions; site selectors break when the sites change their UI.
- Each module is intentionally standalone (duplicate helpers like `_groq_answer` exist in both answers and pipeline).
- Vision calls use `settings.GROQ_VISION_MODEL`.

## Graphify
`graphify explain "do_assignment"` · `graphify explain "extract_questions"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/assignment_tool.py` (781 lines): Jarvis Assignment Tool — Phase 1: Smart Question Extractor
  L48 _TYPE_HINTS · L70 _resolve_pdf_path() · L102 _pdf_pages_to_text() · L133 _pdf_pages_to_images() · L160 _classify_question_type() · L170 _clean_text() · L183 _regex_extract_questions() · L266 _split_with_subquestions() · L337 _extract_marks() · L345 _has_figure_reference() · L355 _VISION_PROMPT · L378 _extract_via_vision() · L427 _LLM_TEXT_PROMPT · L448 _extract_via_llm_text() · L486 _parse_llm_json_response() · L557 _merge_and_deduplicate() · L605 extract_questions() · L734 list_assignments()
- `app/services/assignment_answers.py` (597 lines): Jarvis Assignment Tool — Phase 2: Answer Generation
  L35 _REALISTIC_UA · L42 _AI_SITES · L100 _get_persistent_page() · L129 _find_input() · L141 _send_message() · L173 _upload_pdf() · L202 _wait_for_generation() · L232 _try_copy_button() · L257 _screenshot_extract() · L290 _ask_question_on_page() · L313 _run_browser_session() · L410 _groq_answer() · L473 generate_answers() · L579 generate_answer()
- `app/services/assignment_humanizer.py` (643 lines): Jarvis Assignment Tool — Phase 3: Answer Humanizer
  L40 _REALISTIC_UA · L47 _HUMANIZER_SITES · L129 _PRESERVE_PATTERNS · L145 _protect_technical() · L165 _restore_technical() · L174 _split_into_chunks() · L215 _get_browser_page() · L240 _find_element() · L252 _fill_input() · L285 _extract_output_text() · L325 _humanize_chunk_via_browser() · L375 _humanize_via_browser() · L426 _LLM_HUMANIZE_SYSTEM · L447 _LLM_HUMANIZE_USER · L450 _humanize_via_llm() · L509 humanize_text() · L557 humanize_all_answers()
- `app/services/assignment_assembler.py` (195 lines): Jarvis Assignment Tool — Phase 4: Document Assembly
  L18 _parse_qa_json() · L38 _create_word_doc() · L103 _create_powerpoint() · L158 assemble_assignment()
- `app/services/assignment_pipeline.py` (623 lines): Jarvis Assignment Tool — Phase 5: End-to-End Pipeline
  L20 _CHROME_EXE · L23 _EDGE_PATHS · L33 _SENTINEL · L34 _ERROR_PREFIX · L41 _get_browser_ctx() · L88 _find_el() · L99 _type_into() · L123 _upload_file() · L186 _wait_done() · L204 _get_answer() · L261 _humanize_browser() · L329 _groq_answer() · L356 _groq_humanize() · L385 _browser_thread() · L527 do_assignment()
<!-- AUTO:END -->
