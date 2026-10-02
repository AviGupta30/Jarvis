# Feature index

One file per feature in `docs/features/`. Each has purpose, flow, data/config, gotchas, graphify commands, and an auto-generated **Files & symbols** table with current line numbers. Open only the one you need.

| Feature slug | Covers | Typical user phrases |
|---|---|---|
| `chat-routing` | `/chat` pipeline, keyword router, LLM router, flows | "Jarvis picked the wrong tool", new trigger phrase |
| `tool-registry` | TOOL_REGISTRY, adding tools, tool_runner, `/execute` | "add a new tool/skill" |
| `agents` | DAG executor, linear planner, dynamic skills, sandbox | multi-step tasks, "X and Y and Z" |
| `llm-personality` | Groq models, reply generation, persona, context classifier | tone, language, model choice |
| `memory` | MySQL+FAISS RAG, facts, task ledger/resume, ChromaDB, pgvector, `/memory/*` | "remember", "continue that" |
| `ppt` | PowerPoint engine, charts, images, research, `/ppt/*` | "make a ppt on …" |
| `assignment` | 5-phase assignment solver | "do my assignment" |
| `whatsapp` | send/call/read, reply-style cloning | "message X on WhatsApp" |
| `screen-vision` | screen reading, VLM, watcher alerts, UIA automation | "what's on my screen" |
| `os-control` | windows, media, volume, apps, files, Spotify, Copilot | "snap chrome left", "play X" |
| `web` | web search, agentic research, Playwright browser tools | "find hackathons", weather/news |
| `email-calendar` | Gmail API/browser fallback, Calendar, morning brief | "check my email", "good morning" |
| `voice` | voice agent, STT/TTS, wake word, clap tripwire, overlay | voice issues |
| `prompt-enhancer` | enhancer pipeline, floating Enhance button on AI sites/apps, Ctrl+Space overlay | "enhance this prompt" |
| `syllabus-auditor` | YouTube playlist vs syllabus coverage | "audit my playlist" |
| `content-tools` | AI-text humanizer, social posts | "humanize this", "linkedin post" |
| `media-enhancement` | dark image/video enhancement | "enhance this dark image" |
| `resume-creator` | copy a resume design from an uploaded image, or fixed formats, then PDF/PNG/HTML | "make my resume like this", "create a CV" |
| `dsa-mode` | LeetCode enforcer | "start DSA mode" |
| `neural-cache` | LRU TCP cache server | cache internals |
| `frontend` | React UI, streaming, uploads | UI changes |
| `air-drawing` | webcam hand drawing (MediaPipe) | "draw in the air" |

Keep in sync: `python scripts/refresh_docs.py` regenerates the tables and rebuilds the graph. New feature → add it to `FEATURES` in that script, run it, then fill in the hand-written sections.
