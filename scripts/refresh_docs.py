"""
refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with the code.

    python scripts/refresh_docs.py            # docs + graph (graph needs `graphify` on PATH)
    python scripts/refresh_docs.py --docs     # only regenerate the AUTO sections of feature docs

For every feature in FEATURES below, docs/features/<slug>.md gets an auto-generated
"Files & symbols" block (file sizes + top-level symbols with line numbers) between
the AUTO markers. Everything outside the markers is hand-written and preserved.
To add a feature: add an entry to FEATURES, run this script, then fill in the
hand-written sections of the new file.
"""
import ast
import fnmatch
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "features"
BEGIN, END = "<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->", "<!-- AUTO:END -->"

# slug: (title, {file: [symbol glob patterns] or None for all top-level symbols})
FEATURES = {
    "chat-routing": ("Chat pipeline & routing (/chat)", {
        "app/api/chat.py": None,
        "app/services/llm.py": ["check_for_tool_intent"],
        "app/services/personality.py": None,
        "app/main.py": None,
    }),
    "tool-registry": ("Tool registry & adding tools", {
        "app/services/tools.py": ["TOOL_REGISTRY", "_mail_tool", "_recall_memory_placeholder", "_ppt_*", "_research_and_create_ppt"],
        "app/services/tool_runner.py": None,
        "app/api/tools.py": None,
    }),
    "agents": ("Agents: DAG executor, linear planner, dynamic skills", {
        "app/services/dag_executor.py": None,
        "app/services/planner.py": None,
        "app/services/dynamic_skill.py": None,
        "app/services/safe_executor.py": None,
        "app/services/tool_runner.py": None,
    }),
    "llm-personality": ("LLM layer & Jarvis personality", {
        "app/services/llm.py": None,
        "app/services/personality.py": None,
        "app/services/context_classifier.py": None,
        "app/core/config.py": None,
    }),
    "memory": ("Memory: RAG, facts, task ledger, resume, skills", {
        "app/services/rag_memory.py": None,
        "app/core/mysql_db.py": None,
        "app/api/memory.py": None,
        "app/services/memory_tool.py": None,
        "app/services/task_ledger.py": None,
        "app/services/resume_detector.py": None,
        "app/memory/memory.py": None,
        "app/services/embeddings.py": None,
        "app/services/vector_store.py": None,
        "app/core/database.py": None,
    }),
    "ppt": ("PowerPoint generator", {
        "app/services/ppt_studio.py": None,
        "app/services/ppt_content.py": None,
        "app/services/ppt_designer.py": None,
        "app/services/ppt_composer.py": None,
        "app/services/ppt_research.py": None,
        "app/services/ppt_template.py": None,
        "app/services/ppt_tool.py": None,
        "app/services/ppt_chart_engine.py": ["ChartEngine", "_render_*", "_metrics_to_bar"],
        "app/services/ppt_image_engine.py": None,
        "app/api/ppt_router.py": None,
        "app/services/research_pipeline.py": None,
        "app/services/research_scraper.py": None,
        "app/services/nlp_extractor.py": None,
        "app/services/tools.py": ["_ppt_*", "_research_and_create_ppt"],
    }),
    "assignment": ("Assignment solver (5 phases)", {
        "app/services/assignment_tool.py": None,
        "app/services/assignment_answers.py": None,
        "app/services/assignment_humanizer.py": None,
        "app/services/assignment_assembler.py": None,
        "app/services/assignment_pipeline.py": None,
    }),
    "whatsapp": ("WhatsApp: send, call, read, reply-style cloning", {
        "app/services/whatsapp_smart.py": None,
        "app/services/whatsapp_call.py": None,
        "app/services/whatsapp.py": None,
        "app/services/whatsapp_intelligence/message_reader.py": None,
        "app/services/whatsapp_intelligence/thread_extractor.py": None,
        "app/services/whatsapp_intelligence/style_profiler.py": None,
        "app/services/whatsapp_intelligence/reply_generator.py": None,
        "app/api/chat.py": ["detect_whatsapp_*", "chat_endpoint"],
        "app/services/tools.py": ["read_whatsapp_thread", "build_style_profile", "generate_reply_draft", "send_style_reply"],
    }),
    "screen-vision": ("Screen understanding & UI automation", {
        "app/services/screen_vision.py": None,
        "app/services/screen_reader.py": None,
        "app/services/ui_inspector.py": None,
        "app/services/tools.py": ["read_my_screen", "click_ui_element_uia", "type_into_ui_element", "read_ui_element_text", "dump_app_ui_tree", "read_active_window_text"],
    }),
    "os-control": ("Windows/OS control: windows, media, apps, files", {
        "app/services/window_layout.py": None,
        "app/services/file_ops.py": None,
        "app/services/spotify_service.py": None,
        "app/services/youtube_control.py": None,
        "app/services/youtube_player.py": None,
        "app/services/media_state.py": None,
        "app/services/uia_local.py": None,
        "app/services/media_sessions.py": None,
        "app/services/tools.py": ["close_*", "minimize_*", "maximize_*", "lock_screen", "volume_*", "mute_volume", "media_*",
                                  "play_music", "open_app", "snap_windows", "take_screenshot", "*clipboard", "type_text",
                                  "*sticky*", "set_reminder", "calculate", "create_file", "append_to_file", "find_file",
                                  "open_file", "focus_window", "wait_for_window", "type_and_submit", "copy_selected_text",
                                  "create_word_doc", "read_pdf_text", "open_windows_copilot", "send_to_copilot",
                                  "get_system_*", "open_safe_website"],
    }),
    "web": ("Web search, research & browser automation", {
        "app/services/web_search.py": None,
        "app/services/agentic_web.py": None,
        "app/services/browser_tool.py": None,
        "app/services/smart_navigator.py": None,
        "app/services/tools.py": ["get_info", "get_weather", "_extract_location", "search_site_tool", "scrape_url_tool", "open_google_search_in_browser"],
    }),
    "email-calendar": ("Email, calendar & morning brief", {
        "app/services/gmail_tool.py": None,
        "app/services/browser_mail.py": None,
        "app/services/calendar_tool.py": None,
        "app/services/memory_tool.py": ["get_morning_brief"],
        "app/services/tools.py": ["_mail_tool"],
    }),
    "voice": ("Voice: STT, TTS, wake word, clap tripwire, overlay", {
        "app/services/voice.py": None,
        "scripts/voice_agent.py": None,
        "app/services/acoustic_tripwire.py": None,
        "app/services/hinglish_normalizer.py": None,
        "app/services/ssml_processor.py": None,
        "scripts/jarvis_overlay.py": None,
    }),
    "prompt-enhancer": ("Prompt enhancer (chat + floating Enhance button + Ctrl+Space overlay)", {
        "app/services/skill_prompt_enhancer.py": None,
        "app/services/prompt_enhancement_library.py": None,
        "app/services/prompt_enhancer_button.py": None,
        "app/services/prompt_overlay.py": None,
    }),
    "syllabus-auditor": ("Syllabus auditor (YouTube playlist vs syllabus)", {
        "app/services/syllabus_auditor.py": None,
    }),
    "content-tools": ("Content humanizer & social content", {
        "app/services/content_humanizer.py": None,
        "app/services/social_content_manager.py": None,
    }),
    "media-enhancement": ("Dark image/video enhancement", {
        "app/services/media_enhancement.py": None,
        "app/services/dark_enhancement.py": None,
        "app/services/dark_video_enhancement.py": None,
    }),
    "resume-creator": ("Resume creator (copy a resume design from an image / fixed formats)", {
        "app/services/resume_builder.py": None,
        "app/api/resume_router.py": None,
        "app/services/resume_replica/integrate.py": None,
        "app/services/resume_replica/pipeline.py": None,
        "app/services/resume_replica/ingest.py": None,
        "app/services/resume_replica/measure.py": None,
        "app/services/resume_replica/plate.py": None,
        "app/services/resume_replica/fonts.py": None,
        "app/services/resume_replica/fontmatch.py": None,
        "app/services/resume_replica/exact_render.py": None,
        "scripts/replica_eval.py": None,
        "app/api/chat.py": ["chat_endpoint"],
    }),
    "dsa-mode": ("DSA / LeetCode enforcer mode", {
        "app/services/dsa_enforcer.py": None,
        "app/services/tools.py": ["get_dsa_cache_status", "cache_set", "cache_get"],
    }),
    "neural-cache": ("Neural cache (Redis-like LRU server)", {
        "neural_cache/lru.py": None,
        "neural_cache/protocol.py": None,
        "neural_cache/engine.py": None,
        "neural_cache/server.py": None,
        "neural_cache/client.py": None,
        "neural_cache/persistence.py": None,
    }),
    "frontend": ("Web UI (React/Vite)", {
        "frontend/src/App.jsx": None,
        "frontend/src/DagPlanPanel.jsx": None,
        "frontend/src/MemorySidebar.jsx": None,
        "frontend/src/ChatMessage.jsx": None,
        "frontend/src/config.js": None,
    }),
    "air-drawing": ("Air drawing (webcam hand drawing)", {
        "app/services/air_drawing_tool.py": None,
        "frontend/src/AirDrawing/AirDrawingApp.jsx": None,
        "frontend/src/AirDrawing/components/*.jsx": None,
        "frontend/src/AirDrawing/modules/*.js": None,
    }),
}


def _py_symbols(path: Path, patterns):
    src = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src)
    doc = (ast.get_docstring(tree) or "").strip().splitlines()
    out = []
    for n in tree.body:
        name = None
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name, label = n.name, n.name + "()"
        elif isinstance(n, ast.ClassDef):
            name, label = n.name, "class " + n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id.isupper() and isinstance(n.value, (ast.Dict, ast.List, ast.Constant, ast.JoinedStr)):
            name, label = n.targets[0].id, n.targets[0].id
        if name is None or (patterns and not any(fnmatch.fnmatch(name, p) for p in patterns)):
            continue
        out.append(f"L{n.lineno} {label}")
        if isinstance(n, ast.ClassDef) and not patterns:
            meths = [f"L{m.lineno} .{m.name}" for m in n.body
                     if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and not m.name.startswith("__")]
            if meths:
                out.append("(" + ", ".join(meths) + ")")
    summary = next((l.strip(" -=—") for l in doc if l.strip(" -=—━")), "")
    return src.count("\n") + 1, summary, out


def _js_symbols(path: Path):
    import re
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # top-level and one-level-nested (component handlers) functions/classes/arrow consts
    pat = re.compile(r"^\s{0,2}(?:export\s+(?:default\s+)?)?(?:async\s+)?(?:function\s+(\w+)|class\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(?[\w,\s{}]*\)?\s*=>)")
    out = []
    for i, l in enumerate(lines, 1):
        m = pat.match(l)
        if m:
            out.append(f"L{i} {next(g for g in m.groups() if g)}")
    return len(lines), "", out


def auto_block(files: dict) -> str:
    rows = [BEGIN, "## Files & symbols (auto-generated, line numbers are current)", ""]
    for pattern, symbols in files.items():
        for path in sorted(ROOT.glob(pattern)) or [ROOT / pattern]:
            rel = path.relative_to(ROOT).as_posix()
            if not path.exists():
                rows.append(f"- `{rel}`: MISSING")
                continue
            if path.suffix == ".py":
                n, summary, syms = _py_symbols(path, symbols)
            else:
                n, summary, syms = _js_symbols(path)
            head = f"- `{rel}` ({n} lines)" + (f": {summary[:110]}" if summary else "")
            if symbols:
                head += "  *(filtered to this feature)*"
            rows.append(head)
            if syms:
                rows.append("  " + " · ".join(syms))
    rows.append(END)
    return "\n".join(rows)


def write_docs():
    DOCS.mkdir(parents=True, exist_ok=True)
    for slug, (title, files) in FEATURES.items():
        path = DOCS / f"{slug}.md"
        block = auto_block(files)
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if BEGIN in text and END in text:
                text = text[:text.index(BEGIN)] + block + text[text.index(END) + len(END):]
            else:
                text = text.rstrip() + "\n\n" + block + "\n"
        else:
            text = (f"# {title}\n\n## What it does\nTODO\n\n## Flow\nTODO\n\n"
                    f"## Data & config\nTODO\n\n## Gotchas\nTODO\n\n## Graphify\n"
                    f"`graphify explain \"<main symbol>\"`\n\n{block}\n")
        path.write_text(text, encoding="utf-8")
    print(f"[docs] refreshed {len(FEATURES)} feature docs in {DOCS.relative_to(ROOT)}")


def label_communities():
    """Name each graph community after its dominant source file(s) (no LLM)."""
    g = json.loads((ROOT / "graphify-out" / "graph.json").read_text(encoding="utf-8"))
    by = defaultdict(Counter)
    for n in g["nodes"]:
        if n.get("source_file"):
            by[n["community"]][n["source_file"]] += 1
    labels = {}
    for c, cnt in by.items():
        (top, k), total = cnt.most_common(1)[0], sum(cnt.values())
        names = [os.path.splitext(os.path.basename(f))[0] for f, _ in cnt.most_common(2)]
        labels[str(c)] = names[0] if len(names) == 1 or k / total > 0.75 else " + ".join(names)
    (ROOT / "graphify-out" / ".graphify_labels.json").write_text(json.dumps(labels, indent=1), encoding="utf-8")


def refresh_graph():
    run = lambda *a: subprocess.run(["graphify", *a], cwd=ROOT, check=True,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run("update", ".", "--force")
    label_communities()
    run("cluster-only", ".")
    run("export", "wiki")
    print("[graph] graphify-out/ rebuilt, communities labelled, wiki exported")


if __name__ == "__main__":
    write_docs()
    if "--docs" not in sys.argv:
        refresh_graph()
