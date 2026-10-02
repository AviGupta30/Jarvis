# WhatsApp: send, call, read, reply-style cloning

## Purpose
Control WhatsApp **Desktop** (not web): search contacts, send with confirmation, call, read chats, and draft replies in your own style.

## Flows
- **Send:** chat.py `detect_whatsapp_send` / keyword branch → `api_whatsapp_flow` state machine (ask_contact → ask_message → confirm yes/no incl. Hindi) → `whatsapp_smart.confirm_whatsapp_send`. `initiate_whatsapp_send` only builds the confirmation text.
- **Contact search:** clipboard-paste into the search box → OCR of results → `_fuzzy_score`. `__ASK_CONTACT__` marker → chat asks which contact.
- **Call:** `detect_whatsapp_call` → `api_whatsapp_call_flow` confirm → `whatsapp_call.confirm_whatsapp_call` (clicks the header voice-call button).
- **Read:** `read_whatsapp_messages` (OCR, quick) or `read_whatsapp_thread` → `thread_extractor` + `message_reader` (UIA first, OCR fallback).
- **Style cloning:** `build_style_profile(export.txt, your_name)` → profiles in `app/services/whatsapp_intelligence/style_profiles/` (default + per_contact) → `generate_reply_draft(contact)` (3 drafts, in-memory cache) → `send_style_reply(contact, n)` (records the reply to the profile).

## Gotchas
- Window focus/coordinates depend on the WhatsApp Desktop UI version. Debug helpers at the root: `debug_wa.py`, `dump_wa_ui.py`, `find_call_btn.py`, `get_btn_pos.py`.
- `whatsapp.py` is the legacy sender (still imported by tools.py/voice_agent).
- The voice agent has its own copy of the flow logic in `scripts/voice_agent.py`.

## Graphify
`graphify explain "confirm_whatsapp_send"` · `graphify explain "generate_reply_draft"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/whatsapp_smart.py` (390 lines): whatsapp_smart.py — Jarvis Smart WhatsApp Integration (Fully Isolated)
  L38 _get_whatsapp_window() · L49 _focus_or_open_whatsapp() · L80 _type_via_clipboard() · L87 _clear_search() · L95 _fuzzy_score() · L123 _get_visible_search_results() · L162 open_whatsapp() · L170 search_whatsapp_contact() · L233 initiate_whatsapp_send() · L257 confirm_whatsapp_send() · L305 read_whatsapp_messages()
- `app/services/whatsapp_call.py` (144 lines): whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)
  L28 _get_whatsapp_window() · L39 _focus_or_open_whatsapp() · L68 _type_via_clipboard() · L73 initiate_whatsapp_call() · L84 _click_voice_call_button() · L111 confirm_whatsapp_call()
- `app/services/whatsapp.py` (95 lines): WhatsApp Windows Desktop App Automation
  L15 _focus_or_open_whatsapp() · L49 open_whatsapp() · L55 send_whatsapp_message()
- `app/services/whatsapp_intelligence/message_reader.py` (360 lines): message_reader.py — Jarvis WhatsApp Intelligence: Message Reader
  L67 _EXCLUDED_TITLES · L74 _get_whatsapp_window() · L100 _bring_whatsapp_to_front() · L120 _read_via_uia() · L170 _parse_uia_message_string() · L230 _read_via_ocr() · L270 _heuristic_parse_ocr_lines() · L311 read_messages() · L340 read_messages_as_string()
- `app/services/whatsapp_intelligence/thread_extractor.py` (253 lines): thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor
  L54 _open_contact_chat() · L98 _get_current_chat_title() · L117 _group_into_turns() · L144 _find_latest_incoming() · L160 extract_thread() · L222 extract_thread_as_string()
- `app/services/whatsapp_intelligence/style_profiler.py` (401 lines): style_profiler.py — Jarvis WhatsApp Intelligence: Style Profiler
  L58 _empty_profile() · L72 _now() · L80 _load_profile() · L105 _save_profile() · L126 _safe_filename() · L135 _parse_whatsapp_export() · L188 _compute_profile_stats() · L260 record_sent_reply() · L298 mark_contact_formal() · L311 add_deflection_phrase() · L331 build_style_profile() · L375 get_profile() · L383 get_profile_summary()
- `app/services/whatsapp_intelligence/reply_generator.py` (404 lines): reply_generator.py — Jarvis WhatsApp Intelligence: Reply Generator
  L54 _get_groq_api_key() · L76 _call_groq() · L106 _build_system_prompt() · L178 _build_user_prompt() · L202 _parse_drafts_from_response() · L242 generate_reply_draft() · L334 get_cached_drafts() · L342 get_cached_contact() · L347 get_cached_incoming() · L352 send_style_reply()
- `app/api/chat.py` (1929 lines)  *(filtered to this feature)*
  L46 detect_whatsapp_call() · L74 detect_whatsapp_send() · L1398 chat_endpoint()
- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L872 read_whatsapp_thread() · L885 build_style_profile() · L899 generate_reply_draft() · L913 send_style_reply()
<!-- AUTO:END -->
