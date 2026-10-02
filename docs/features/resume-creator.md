# Resume creator

## Purpose
"Make my resume like this" + a picture of any resume → Jarvis copies its **design** (layout, colours, header shape, photo, heading style, skill graphic, section order and titles) and fills it with the user's own details. Output: A4 **PDF**, PNG previews and an editable **HTML** file in `data/uploads/resumes/` (served at `/media/resumes/...`). Without an image it uses a fixed format: `elegant` (gold diagonal banner + photo, Venn skills), `modern`, `minimal`, `creative`, `executive`, `tech`.

## Flow
1. `chat_endpoint` runs an early intercept (after the note/WhatsApp flows, **before** media/DAG/complex-task checks, because pasted details are long multi-clause text): `resume_builder.detect_resume_request(prompt)` → kwargs, or `{"_list": True}` for "list resume templates". The result streams via `iterate_in_threadpool` and is added to `conversation_history`.
2. `create_resume(...)` (generator, progress lines then markdown):
   - **Design** `_resolve_design`: image → `_analyse_design` runs **two Groq vision calls in parallel** (`settings.GROQ_VISION_MODEL`): a style prompt (header/photo/font/skills style, plus a k-means palette from `_palette` so it picks exact hexes) and a focused layout prompt (section → column, heading/banner/Venn colours). `_apply_layout_answer` maps headings to section keys (`_TITLE_KEYS`). The result is merged over the closest preset (`_merge_design`) → `template`/`color` overrides → `_sanitize_design` (contrast fixes, every section gets a column).
   - **Content**: `_build_content` (gpt-oss-120b → 20b, JSON mode) → `_normalise_content` → `_drop_invented` (removes any sentence/bullet with a number the user never wrote, and contact values not in the source). Edits go through `_edit_content(old JSON, instruction)`. A colour/template-only change skips the LLM.
   - No details yet → saves the design with `awaiting_details` (30 min) and asks for them. The next message counts as details if `_has_details()` (email/phone/experience words/length), even without the word "resume".
   - **Photo**: an attached photo (labelled, or a close-up face with >12% face area) → used. "use the same photo" → `_crop_photo` cuts it from the reference (Haar face → `_grow_photo_box` to the flat border → VLM bbox → face-expanded). No photo → initials block.
   - **Render** `_render_files`: `_render_html` (fixed CSS formats, inline SVG icons/Venn/rings) → Playwright Chromium `page.pdf` (falls back to the msedge channel). The fit loop counts **real PDF pages** with PyMuPDF: it first moves sidebar-friendly sections from main to a shorter sidebar, then shrinks `--s` (down to 0.8). PNG previews come from PyMuPDF.
3. State is saved in `app/memory/resume_state.json` (design, content, photo, ref image, last PDF), so follow-ups work: "change the resume colour to navy", "use the modern template for my resume", "add AWS certification to my resume".

## Visual editor (/resume/editor)
- Open it from the **✏️ Edit text, sections & layout** button in every "resume ready" reply, the paperclip menu → **✏️ Edit Last Resume**, or say "edit my resume" / "open resume editor" (`detect_resume_request` → `{"_editor": True}` → `open_resume_editor()`, which also opens the browser). A concrete change ("add Docker to my resume") still goes through the AI `instruction` path.
- `editor_page()` renders the saved resume with `_render_html(..., edit=True)`. The `_EDIT` contextvar makes `_f(path, value)` emit `<span data-f="experience.0.bullets.2" contenteditable>` and `_it(path)` mark list items. Normal PDF renders are unchanged (no editor attributes). Name/title upper-casing is CSS (`.up`), so edits keep the real case.
- Page JS (`_EDITOR_JS`) collects every `[data-f]` `textContent` into the content JSON and POSTs `/resume/save` (`app/api/resume_router.py` → `editor_save`). Hover controls ＋ ↑ ✕ send `op` (`_apply_op`: add a template item after / move up / delete). The toolbar sends `template`, `color`, `photo` (via `/upload`), `remove_photo`, `add_section` (`_ITEM_TEMPLATES`) or `instruction` (AI edit). These save and reload the page. **Save & export PDF** (or Ctrl+S) sends `export: true` → `_render_files` → returns the PDF link.
- Enter is blocked (single-line fields) and paste is plain text. The red line marks each A4 page break. Clearing a field's text deletes that item on save (`_normalise_content` drops empties).

## UI
Paperclip menu → **📄 Resume Design Image** / **🧑 Resume Photo** (amber chips above the input, like the PPT theme image). On send, `App.jsx` adds `[ATTACHED_FILE: … | DESCRIPTION: resume design reference]` / `… | DESCRIPTION: my photo for the resume`, prefixes "Create my resume exactly like this design using these details:" if the text has no resume word, and always posts to `/chat` (never `/ppt/create`). Labelled attachments alone count as a resume request in `detect_resume_request`.

## Data/config
Vision: Groq `GROQ_VISION_MODEL` (qwen, **200k tokens/day cap**) → Gemini fallback (`GEMINI_API_KEY`, `_GEMINI_MODELS`: flash-lite-latest first). Text: gpt-oss-120b → 20b → Gemini. Images are downscaled to 1400px JPEG before sending (`_image_b64`). Designs are cached per image SHA-1 in `resume_state.json["design_cache"]` (last 10), so re-using a picture costs no vision tokens. Google Fonts load when online (system fallbacks otherwise). `RESUME_DEBUG=1` prints the fit loop.

## Gotchas
- Routing is **order-based** on both sides: whichever artifact is named first wins (`isResumeRequest` in App.jsx, `_OTHER_ARTIFACT_RX` vs `_NOUN` in the backend). Resume details contain "email", "presentation skills", "slides" etc. The old "any PPT word → PPT" check sent resume requests to `/ppt/create`.
- Fallback models sometimes drop the name/headline → `_guess_name` / `_guess_title` recover them from the user's text. The content prompt forbids pronouns (the model guessed "he" from a name).
- Fit loop (`_render_files`): `_placement` materializes every section into a column first, then moves sections from the longer column to the shorter (never back: `moved` set), then shrinks `--s` to 0.8. 2 pages are accepted when page 2 is ≥45% full.
- The word "resume" collides with media ("resume the music") and task-resume. `_MEDIA_RX` bails out, and creation needs a verb+noun / "resume like this" / template-or-colour+noun. PPT/cover-letter/email prompts are excluded (`_OTHER_ARTIFACT_RX`).
- The small VLM alone often answers "single_column". The second, focused layout prompt is what makes sidebar detection reliable. Don't drop it.
- Chromium print: the sidebar background is a `position:fixed` div (repeats on every page). Column padding uses `box-decoration-break: clone` so page 2 has top padding.
- Testing burns Groq TPM quickly (429s). `_llm_json` retries and falls back to 20b.

## Graphify
`graphify explain "create_resume"` · `graphify explain "detect_resume_request"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/resume_builder.py` (2043 lines): resume_builder.py — Resume Creator
  L30 MEDIA_URL · L31 _TEXT_MODEL · L32 _TEXT_MODEL_FALLBACK · L36 SECTION_KEYS · L38 DEFAULT_TITLES · L111 PRESET_BLURBS · L120 _FONTS · L129 _NAMED_COLORS · L139 _ICONS · L175 _icon() · L182 _e() · L186 _hex() · L199 _rgb() · L204 _mix() · L210 _lum() · L218 _contrast() · L223 _readable_on() · L229 _load_state() · L237 _save_state() · L250 _parse_json() · L274 _groq() · L282 _gemini() · L307 _llm_json() · L334 _palette() · L359 _faces() · L373 _face_ratio() · L386 _grow_photo_box() · L409 _crop_photo() · L450 _VISION_PROMPT · L485 _LAYOUT_PROMPT · L492 _TITLE_KEYS · L502 _title_key() · L510 _vision() · L526 _image_b64() · L545 _file_hash() · L554 _apply_layout_answer() · L590 _analyse_design() · L620 _closest_preset() · L630 _merge_design() · L675 _apply_color() · L693 _sanitize_design() · L722 _resolve_design() · L751 _CONTENT_SYSTEM · L778 _content_brief() · L792 _str_list() · L807 _normalise_content() · L878 _nums() · L882 _drop_invented() · L920 _guess_name() · L935 _guess_title() · L947 _build_content() · L964 _edit_content() · L973 _title() · L977 _sec() · L981 _venn() · L1001 _ring() · L1014 _f() · L1022 _it() · L1027 _skill_name() · L1031 _skills_html() · L1077 _ICON_GUESS · L1088 _guess_icon() · L1096 _competencies_html() · L1114 _experience_html() · L1136 _education_html() · L1152 _contact_html() · L1162 _list_html() · L1173 _section_html() · L1214 _initials() · L1219 _photo_html() · L1227 _name_block() · L1239 _name_size() · L1244 _header_html() · L1266 _css() · L1385 _placement() · L1397 _render_html() · L1405 _render_html_inner() · L1423 _data_uri() · L1433 _launch() · L1440 _render_files() · L1531 EDITOR_URL · L1533 _ITEM_TEMPLATES · L1546 _ADDABLE · L1549 _EDITOR_CSS · L1585 _EDITOR_JS · L1671 _editor_toolbar() · L1693 editor_page() · L1716 _apply_op() · L1738 editor_save() · L1795 open_resume_editor() · L1810 _NOUN · L1830 _attachments() · L1843 _split_images() · L1861 _strip_tags() · L1866 _has_details() · L1879 resume_awaiting_details() · L1884 detect_resume_request() · L1937 list_resume_templates() · L1944 create_resume() · L2035 resume_tool()
- `app/api/resume_router.py` (30 lines): resume_router.py — FastAPI router for the visual resume editor
  L21 resume_editor() · L27 resume_save()
- `app/api/chat.py` (1934 lines)  *(filtered to this feature)*
  L1398 chat_endpoint()
<!-- AUTO:END -->
