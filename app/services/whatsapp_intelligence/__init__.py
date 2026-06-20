"""
whatsapp_intelligence/ — Jarvis WhatsApp Intelligence Layer
============================================================
Isolated package. Zero imports from any other Jarvis service.

Modules:
    message_reader.py   — UIA tree + OCR fallback, extracts structured messages
    thread_extractor.py — pulls last N messages with sender/timestamp context
    style_profiler.py   — builds + updates your personal reply style JSON
    reply_generator.py  — LLM call with style injection, returns ranked drafts

Entry points registered in tools.py:
    read_whatsapp_thread(contact, n_messages)
    build_style_profile(chat_export_path)
    generate_reply_draft(contact, thread)
    send_style_reply(contact, draft_index)
"""
