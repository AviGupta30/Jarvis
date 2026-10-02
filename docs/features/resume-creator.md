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

- `app/services/resume_builder.py` (1688 lines): resume_builder.py — Resume Creator
  L29 MEDIA_URL · L30 _TEXT_MODEL · L31 _TEXT_MODEL_FALLBACK · L35 SECTION_KEYS · L37 DEFAULT_TITLES · L110 PRESET_BLURBS · L119 _FONTS · L128 _NAMED_COLORS · L138 _ICONS · L174 _icon() · L181 _e() · L185 _hex() · L198 _rgb() · L203 _mix() · L209 _lum() · L217 _contrast() · L222 _readable_on() · L228 _load_state() · L236 _save_state() · L249 _parse_json() · L273 _groq() · L281 _gemini() · L306 _llm_json() · L333 _palette() · L358 _faces() · L372 _face_ratio() · L385 _grow_photo_box() · L408 _crop_photo() · L449 _VISION_PROMPT · L484 _LAYOUT_PROMPT · L491 _TITLE_KEYS · L501 _title_key() · L509 _vision() · L525 _image_b64() · L544 _file_hash() · L553 _apply_layout_answer() · L589 _analyse_design() · L619 _closest_preset() · L629 _merge_design() · L674 _apply_color() · L692 _sanitize_design() · L721 _resolve_design() · L750 _CONTENT_SYSTEM · L777 _content_brief() · L791 _str_list() · L806 _normalise_content() · L877 _nums() · L881 _drop_invented() · L919 _guess_name() · L934 _guess_title() · L946 _build_content() · L963 _edit_content() · L972 _title() · L976 _sec() · L980 _venn() · L1000 _ring() · L1009 _skills_html() · L1048 _ICON_GUESS · L1059 _guess_icon() · L1067 _competencies_html() · L1080 _experience_html() · L1094 _education_html() · L1102 _contact_html() · L1111 _list_html() · L1122 _section_html() · L1158 _initials() · L1163 _photo_html() · L1171 _name_block() · L1182 _name_size() · L1187 _header_html() · L1209 _css() · L1328 _placement() · L1340 _render_html() · L1358 _data_uri() · L1368 _launch() · L1375 _render_files() · L1463 _NOUN · L1483 _attachments() · L1496 _split_images() · L1514 _strip_tags() · L1519 _has_details() · L1532 resume_awaiting_details() · L1537 detect_resume_request() · L1583 list_resume_templates() · L1590 create_resume() · L1680 resume_tool()
- `app/api/chat.py` (1929 lines)  *(filtered to this feature)*
  L1398 chat_endpoint()
<!-- AUTO:END -->
