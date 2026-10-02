# Tool registry

From `app/services/tools.py` → `TOOL_REGISTRY` (bottom of file, ~L1107), updated 2026-09-28 after the known-issues fixes. **132 tools.**
- *Implementation*: `tools.py:fn (Lnn)` = defined inside tools.py. `module.fn` = lazily imported from `app/services/<module>.py`.
- *Keyword trigger*: the phrase that `keyword_detect_tool()` in `app/api/chat.py` maps to this tool (it runs before the LLM router).
- *Router prompt*: ✓ means the tool is described in `TOOL_ROUTER_PROMPT` (`app/services/personality.py:71`), so the Groq router can choose it. — means it's internal: reachable via keyword trigger, planner/DAG prompts, or `POST /execute` only.
- A tool returning a **generator** gets streamed chunk by chunk from `/chat` and skips the LLM rephrase: `ppt_create`, `ppt_edit`, `research_and_create_ppt`, `agentic_web_action`, `do_assignment` and other progress-style tools. From planner/DAG/`/execute`, `tool_runner.run_tool` joins the chunks.
- Multi-step media sentences ("close this song and play X") are split by `chat._media_compound` and run in order. Media tools skip the LLM rephrase too: `play_music`, `spotify_control`, `youtube_*` (incl. `youtube_channel`, `youtube_list_results`), `play_video_in_browser` run in a worker thread (`chat._run_direct_tool`) and their result string is the reply.
- Pseudo-tools the router may emit but that aren't in the registry: `ask_for_clarification` (handled in chat.py), `null` (plain chat).

To add a tool, follow the checklist in `CLAUDE.md` → "Adding / changing a tool".

| Tool | Implementation | Args (lambda) | Keyword trigger in chat.py | Router prompt |
|---|---|---|---|---|
| `get_info` | tools.py:get_info (L144) |  | weather/temp/mausam, news, sports/IPL/score, stock/crypto | ✓ |
| `get_system_time` | tools.py:get_system_time (L266) |  | short prompt with time/date/day | ✓ |
| `get_system_info` | tools.py:get_system_info (L272) |  |  | ✓ |
| `open_website` | tools.py:open_safe_website (L213) |  | "open <known site / x.com>" | ✓ |
| `open_google_search_in_browser` | tools.py:open_google_search_in_browser (L239) |  |  | ✓ |
| `youtube_search` | youtube_control.youtube_search | query, autoplay | "play X on youtube" / "open youtube and play X" (autoplay), "search X on youtube", "youtube search X" | ✓ |
| `youtube_open` | youtube_control.youtube_open | query? | "open youtube", "youtube" → enters YouTube mode | ✓ |
| `youtube_channel` | youtube_control.youtube_channel | name, play_latest | "search for channel mr beast", "open MrBeast's channel", "open his channel" (playing video), "play mrbeast's latest video" (play_latest) | ✓ |
| `youtube_list_results` | youtube_control.youtube_list_results |  | YouTube mode: "read the results", "what are the options" (search replies no longer read titles) | ✓ |
| `youtube_play_result` | youtube_control.youtube_play_result | choice | "play the first result", "open the second one", "play the latest video", "the one by X", "the 10 minute one": **reads the videos on screen** in the YouTube tab | ✓ |
| `youtube_control` | youtube_control.youtube_control → youtube_player.player_action | action, amount, value | YouTube mode, or a YouTube tab in front: "speed 2x", "forward 10 minutes", "go to 5:30", "skip this part", "next chapter", "how much time is left", "volume 40", "captions off", "loop", "1080p", "skip ad", "like this video", full screen/theater/mini player, pause/resume, next/previous video, close | ✓ |
| `take_screenshot` | tools.py:take_screenshot (L290) |  | "screenshot", "take ss" | ✓ |
| `snap_windows` | tools.py:snap_windows (L298) |  |  | ✓ |
| `create_file` | tools.py:create_file (L304) |  |  | — |
| `append_to_file` | tools.py:append_to_file (L313) |  |  | — |
| `close_tab` | tools.py:close_tab (L322) |  | "close tab" | ✓ |
| `close_window` | tools.py:close_window (L327) |  | "close this window" | ✓ |
| `close_specific_window` | tools.py:close_specific_window (L337) |  | "close X" | ✓ |
| `minimize_window` | tools.py:minimize_window (L342) |  | "minimize X" | ✓ |
| `maximize_window` | tools.py:maximize_window (L347) |  | "maximize X" | ✓ |
| `minimize_all_windows` | tools.py:minimize_all_windows (L352) |  | "minimize all" | ✓ |
| `lock_screen` | tools.py:lock_screen (L357) |  |  | ✓ |
| `volume_up` | tools.py:volume_up (L364) |  | "volume up", "louder" | ✓ |
| `volume_down` | tools.py:volume_down (L370) |  | "volume down", "quieter" | ✓ |
| `mute_volume` | tools.py:mute_volume (L376) |  | "mute" | ✓ |
| `play_music` | tools.py:play_music → spotify_service.play_song_dynamic |  | "play X" (default) / "play X on spotify" / "open spotify and play X" | ✓ |
| `media_control` | media_sessions.media_command | action, app | "stop the song", "pause it", "stop the music", "close this song", "resume", "next/previous song", "what's playing": whatever is ACTUALLY playing (Windows media sessions: Spotify, any browser tab, other apps). app = spotify / youtube to narrow | — |
| `spotify_control` | spotify_service.spotify_control | action | "pause that song", "stop the music", "resume the music", "next song" (when Spotify is the last/open player, see `chat._media_target`), "what song is this", "like this song", "shuffle", "repeat", "open spotify", "close/quit spotify" | ✓ |
| `media_play_pause` | tools.py:media_play_pause |  | pause/resume only when neither Spotify nor a YouTube tab is open (OS media key) | ✓ |
| `media_next` | tools.py:media_next |  | (router only; "next song" now → spotify_control) | ✓ |
| `media_previous` | tools.py:media_previous |  | (router only; "previous song" now → spotify_control) | ✓ |
| `read_clipboard` | tools.py:read_clipboard (L412) |  |  | ✓ |
| `write_clipboard` | tools.py:write_clipboard (L417) |  |  | ✓ |
| `type_text` | tools.py:type_text (L422) |  |  | ✓ |
| `open_app` | tools.py:open_app (L432) |  | "open <known app>" / fallback "open X" | ✓ |
| `create_sticky_note` | tools.py:create_sticky_note (L472) |  |  | ✓ |
| `close_sticky_notes` | tools.py:close_sticky_notes (L477) |  |  | ✓ |
| `set_reminder` | tools.py:set_reminder (L506) |  |  | ✓ |
| `calculate` | tools.py:calculate (L494) |  |  | ✓ |
| `open_whatsapp` | whatsapp_smart.open_whatsapp |  | "open whatsapp" | ✓ |
| `search_whatsapp_contact` | whatsapp_smart.search_whatsapp_contact | name | "find X on whatsapp" | ✓ |
| `initiate_whatsapp_send` | whatsapp_smart.initiate_whatsapp_send | contact_name, message | "send/message X saying …" | ✓ |
| `confirm_whatsapp_send` | whatsapp_smart.confirm_whatsapp_send | contact_name, message | "yes" after confirm prompt | — |
| `read_whatsapp_messages` | whatsapp_smart.read_whatsapp_messages | contact_name, count | "read messages from X" | ✓ |
| `send_whatsapp_message` | whatsapp_smart.initiate_whatsapp_send | contact_name, message |  | — |
| `initiate_whatsapp_call` | whatsapp_call.initiate_whatsapp_call | contact_name | "call X on whatsapp" | ✓ |
| `confirm_whatsapp_call` | whatsapp_call.confirm_whatsapp_call | contact_name |  | — |
| `read_whatsapp_thread` | tools.py:read_whatsapp_thread (L954) |  |  | ✓ |
| `build_style_profile` | tools.py:build_style_profile (L967) |  |  | ✓ |
| `generate_reply_draft` | tools.py:generate_reply_draft (L981) |  |  | ✓ |
| `send_style_reply` | tools.py:send_style_reply (L995) |  |  | ✓ |
| `remember_preference` | tools.py:remember_preference (L522) |  |  | ✓ |
| `list_learned_skills` | tools.py:list_learned_skills (L531) |  |  | ✓ |
| `read_pdf_text` | tools.py:read_pdf_text (L545) |  |  | ✓ |
| `find_file` | tools.py:find_file (L609) |  |  | ✓ |
| `open_file` | tools.py:open_file (L635) |  |  | ✓ |
| `focus_window` | tools.py:focus_window (L647) |  |  | ✓ |
| `wait_for_window` | tools.py:wait_for_window (L659) |  |  | — |
| `adjust_active_window` | window_layout.adjust_active_window | position, width_percent, height_percent, app_name | layout verb + position/percent ("snap chrome to left", "60% width") | ✓ |
| `type_and_submit` | tools.py:type_and_submit (L671) |  |  | — |
| `copy_selected_text` | tools.py:copy_selected_text (L681) |  |  | ✓ |
| `create_word_doc` | tools.py:create_word_doc (L691) |  |  | ✓ |
| `read_active_window_text` | tools.py:read_active_window_text (L730) |  |  | ✓ |
| `open_windows_copilot` | tools.py:open_windows_copilot (L816) |  |  | ✓ |
| `send_to_copilot` | tools.py:send_to_copilot (L823) |  |  | ✓ |
| `read_my_screen` | tools.py:read_my_screen (L31) |  | "what's on my screen" / "what should I do" / "fix this" | ✓ |
| `play_video_in_browser` | alias → youtube_control.youtube_play_result("that") |  | (legacy name; keyword route now emits youtube_play_result) | ✓ |
| `search_site` | tools.py:search_site_tool (L869) |  | "search X on <site>" | ✓ |
| `scrape_url` | tools.py:scrape_url_tool (L877) |  | URL + "read this page" | ✓ |
| `read_file` | file_ops.read_file | path | "read notes.txt" | ✓ |
| `write_file` | file_ops.write_file | path, content |  | ✓ |
| `append_file` | file_ops.append_file | path, content |  | ✓ |
| `list_directory` | file_ops.list_directory | path | "list files on desktop" | ✓ |
| `move_file` | file_ops.move_file | src, dst |  | ✓ |
| `delete_file` | file_ops.delete_file | path | "delete x.txt" | ✓ |
| `search_files` | file_ops.search_files | name, root_dir | "find resume.pdf" | ✓ |
| `create_folder` | file_ops.create_folder (bare names → Desktop) | path |  | ✓ |
| `bulk_rename` | file_ops.bulk_rename | directory, find, replace |  | ✓ |
| `diff_files` | file_ops.diff_files | path1, path2 |  | ✓ |
| `check_emails` | tools.py:_mail_tool → gmail_tool, fallback browser_mail | query, max_results | "check my email", "emails about/from X" | ✓ |
| `list_unread` | tools.py:_mail_tool → gmail_tool, fallback browser_mail | max_results | "unread emails", "new emails" | ✓ |
| `get_email_body` | tools.py:_mail_tool → gmail_tool, fallback browser_mail | email_id |  | ✓ |
| `summarize_inbox` | tools.py:_mail_tool → gmail_tool, fallback browser_mail | max_results | "summarize my inbox" | ✓ |
| `smart_mail_action` | browser_mail.smart_mail_action | task |  | ✓ |
| `browse_and_read` | browser_tool.browse_and_read | url |  | ✓ |
| `search_on_site` | browser_tool.search_on_site | site_url, query |  | — |
| `click_element` | browser_tool.click_element | page_url, text |  | — |
| `scroll_and_read` | browser_tool.scroll_and_read | url, px |  | — |
| `get_upcoming_events` | calendar_tool.get_upcoming_events | days | "upcoming events" | ✓ |
| `check_today_schedule` | calendar_tool.check_today_schedule |  | "today's schedule" | ✓ |
| `add_event` | calendar_tool.add_event | title, date, time, notes |  | ✓ |
| `save_fact` | memory_tool.save_fact | topic, fact |  | ✓ |
| `recall_facts` | memory_tool.recall_facts | topic |  | ✓ |
| `get_morning_brief` | memory_tool.get_morning_brief |  | "good morning", "morning brief" | ✓ |
| `update_fact` | memory_tool.update_fact | topic, old_fact, new_fact |  | ✓ |
| `forget_fact` | memory_tool.forget_fact | topic |  | ✓ |
| `fill_form` | browser_tool.fill_form | url, fields |  | — |
| `browse_and_paginate` | browser_tool.browse_and_paginate | url, pages |  | — |
| `smart_web_action` | agentic_web.agentic_web_action | site_name, task |  | — |
| `agentic_web_action` | agentic_web.agentic_web_action | site_or_task, specific_task | "go to <site> and find …", "find X on <site>", "find me/latest/hackathons…" | ✓ |
| `click_ui_element_uia` | tools.py:click_ui_element_uia (L740) |  |  | ✓ |
| `type_into_ui_element` | tools.py:type_into_ui_element (L761) |  |  | ✓ |
| `read_ui_element_text` | tools.py:read_ui_element_text (L781) |  |  | ✓ |
| `dump_app_ui_tree` | tools.py:dump_app_ui_tree (L799) |  |  | ✓ |
| `extract_questions` | assignment_tool.extract_questions | pdf_path | "extract questions from x.pdf" | ✓ |
| `list_assignments` | assignment_tool.list_assignments |  | "list my assignments" | ✓ |
| `generate_answers` | assignment_answers.generate_answers | questions_json, pdf_path | "generate answers" | — |
| `generate_answer` | assignment_answers.generate_answer | question, question_type, has_figure | "answer this question: …" | ✓ |
| `humanize_all_answers` | assignment_humanizer.humanize_all_answers | qa_json | "humanize answers" | — |
| `humanize_text` | assignment_humanizer.humanize_text | text, force_site |  | — |
| `assemble_assignment` | assignment_assembler.assemble_assignment | qa_json, filename, format_type | "assemble assignment" | — |
| `do_assignment` | assignment_pipeline.do_assignment | pdf_path, output_format, humanize | "do/complete my assignment" | ✓ |
| `audit_playlist_syllabus` | syllabus_auditor.audit_playlist_syllabus | playlist_url, image_path | "audit my playlist" + playlist URL + syllabus image | ✓ |
| `humanize_ai_content` | content_humanizer.humanize_text_sync | text | "humanize this text: …" | ✓ |
| `ppt_create` | tools.py:_ppt_create (L889) → ppt_studio.create | user_prompt, style, purpose, image_paths, image_descriptions, template_path | "make a ppt/presentation on …" (+"N slides", "dark", theme name, images, pasted "Slide 1: …" content used verbatim, attached .pptx/.potx = exact format) | ✓ |
| `ppt_edit` | tools.py:_ppt_edit (L928) → ppt_studio.edit | edit_prompt, image_paths | follow-ups on the last deck: "on slide 3 …", "delete slide 5", "make slide 4 a timeline", "add a slide after 2 about …", "use a dark theme", "undo" (needs an active deck) | ✓ |
| `ppt_styles` | tools.py:_ppt_styles (L939) |  | "list ppt styles" | ✓ |
| `research_and_create_ppt` | tools.py:_research_and_create_ppt (L902) |  |  | ✓ |
| `enhance_prompt` | skill_prompt_enhancer.enhance_prompt | raw_prompt | "enhance …"/"refine …" (streamed directly) | ✓ |
| `activate_dsa_mode` | dsa_enforcer.get_dsa_enforcer().start_mode | num_questions |  | ✓ |
| `deactivate_dsa_mode` | dsa_enforcer.get_dsa_enforcer().stop_mode |  |  | ✓ |
| `dsa_status` | tools.py:get_dsa_cache_status (L1061) |  |  | ✓ |
| `enhance_media` | media_enhancement.enhance_media | file_path | "enhance/fix … image/video/dark" + attachment | ✓ |
| `create_resume` | resume_builder.resume_tool → create_resume (generator) | details, image_path, photo_path, template, color, instruction, reuse_photo | "make my resume like this" + resume image, "create a CV in modern template", "change the resume colour to navy", "add X to my resume", "list resume templates", "edit my resume" (opens the visual editor at `/resume/editor`); early intercept in chat_endpoint via `detect_resume_request` | ✓ |
| `generate_social_content` | social_content_manager.generate_social_content | idea, platform, tone, creativity, formality, smart_emojis, auto_hashtag, contextual_suggestions, target_audience | "linkedin post", "caption for …" (asks tone first) | ✓ |
| `refine_social_content` | social_content_manager.refine_social_content | original_content, refinement_instruction, platform |  | ✓ |
| `recall_memory` | async: chat.py / tool_runner.run_tool → rag_memory.recall (registry entry is a placeholder) | query | "do you remember", "what did I say" | ✓ |
| `cache_set` | tools.py:cache_set (L1012) |  |  | — |
| `cache_get` | tools.py:cache_get (L1038) |  |  | — |
| `open_air_drawing` | air_drawing_tool.open_air_drawing |  |  | ✓ |
| `get_recent_tasks` | task_ledger.get_recent_tasks | n |  | ✓ |
| `find_resumable_task` | task_ledger.find_resumable_task | query |  | ✓ |
| `get_task_history` | task_ledger.get_task_ledger_for_prompt |  |  | — |
