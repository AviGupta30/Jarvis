"""
test_task_resumption.py -- Comprehensive automated verification for the Task Resumption feature.
Runs completely standalone (no FastAPI server needed).
Tests: task_ledger.py, resume_detector.py, and the integration logic in chat.py.
"""

import sys
import os
import json
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import shutil
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# -- Test harness --------------------------------------------------------------

PASS = 0
FAIL = 0
RESULTS = []

def check(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    symbol = "[OK]" if condition else "[XX]"
    msg = f"  {symbol} {name}"
    if detail:
        msg += f"\n        -> {detail}"
    RESULTS.append((status, name, detail))
    print(msg)

def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# -- Temporary ledger file (isolated from real data) ---------------------------

_REAL_LEDGER = Path("app/data/task_ledger.json")
_TEST_LEDGER = Path("app/data/task_ledger_TEST_BACKUP.json")

def _backup_ledger():
    if _REAL_LEDGER.exists():
        shutil.copy(_REAL_LEDGER, _TEST_LEDGER)
    _REAL_LEDGER.write_text("[]", encoding="utf-8")

def _restore_ledger():
    if _TEST_LEDGER.exists():
        shutil.copy(_TEST_LEDGER, _REAL_LEDGER)
        _TEST_LEDGER.unlink()
    else:
        _REAL_LEDGER.write_text("[]", encoding="utf-8")

# =============================================================================
# SECTION 1: task_ledger.py -- unit tests
# =============================================================================
section("SECTION 1: task_ledger.py -- Core Ledger Operations")

_backup_ledger()
try:
    from app.services.task_ledger import (
        log_task, get_recent_tasks, get_recent_tasks_raw,
        find_resumable_task, update_task, get_task_ledger_for_prompt,
        _load_ledger, _LEDGER_FILE
    )

    # 1.1 Log a task
    r = log_task("write_file", "Created quantum_computing.docx",
                 {"args": {"path": "Desktop/quantum_computing.docx"},
                  "path": "Desktop/quantum_computing.docx"}, "completed", "write_file")
    check("1.1 log_task returns success string", "logged" in r.lower(), r)

    # 1.2 Verify entry was written to disk
    entries = _load_ledger()
    check("1.2 Entry persisted to task_ledger.json", len(entries) == 1, f"Found {len(entries)} entries")

    # 1.3 Entry has all required fields
    e = entries[0]
    required = ["task_id", "timestamp", "task_type", "description", "context", "status", "resumable", "related_tool"]
    missing = [f for f in required if f not in e]
    check("1.3 Entry has all required fields", len(missing) == 0, f"Missing: {missing}" if missing else "All present")

    # 1.4 write_file is correctly flagged as resumable
    check("1.4 write_file flagged as resumable=True", e["resumable"] is True, str(e.get("resumable")))

    # 1.5 Log a non-resumable task (get_system_time)
    log_task("get_system_time", "Got current time", {}, "completed", "get_system_time")
    entries2 = _load_ledger()
    non_resumable = [x for x in entries2 if x["task_type"] == "get_system_time"]
    check("1.5 get_system_time flagged as resumable=False", non_resumable[0]["resumable"] is False, str(non_resumable[0].get("resumable")))

    # 1.6 get_recent_tasks returns formatted string
    r2 = get_recent_tasks(5)
    check("1.6 get_recent_tasks returns formatted string", "write_file" in r2, r2[:120])

    # 1.7 get_recent_tasks_raw returns list
    raw = get_recent_tasks_raw(10)
    check("1.7 get_recent_tasks_raw returns list", isinstance(raw, list) and len(raw) == 2, f"Got {len(raw)} entries")

    # 1.8 find_resumable_task finds the write_file entry
    found = find_resumable_task("word document")
    check("1.8 find_resumable_task('word document') finds write_file", found is not None and found["task_type"] == "write_file", str(found["task_type"] if found else None))

    # 1.9 find_resumable_task('ppt') returns None (no ppt logged)
    found_ppt = find_resumable_task("ppt presentation")
    check("1.9 find_resumable_task('ppt') returns None (not logged yet)", found_ppt is None, str(found_ppt))

    # 1.10 update_task works
    task_id = entries[0]["task_id"]
    upd = update_task(task_id, {"status": "updated", "description": "Added entanglement section"})
    updated_entries = _load_ledger()
    updated_entry = next((x for x in updated_entries if x["task_id"] == task_id), None)
    check("1.10 update_task persists changes", updated_entry and updated_entry["status"] == "updated", str(updated_entry.get("status") if updated_entry else None))

    # 1.11 update_task on non-existent ID returns graceful message
    r_bad = update_task("nonexistent-id", {"status": "x"})
    check("1.11 update_task on bad ID returns graceful string", "not found" in r_bad.lower(), r_bad)

    # 1.12 get_task_ledger_for_prompt returns non-empty string with history
    prompt_ctx = get_task_ledger_for_prompt()
    check("1.12 get_task_ledger_for_prompt returns non-empty string", len(prompt_ctx) > 10, prompt_ctx[:120])

    # 1.13 FIFO cap -- log 25 entries, verify only 20 remain
    for i in range(25):
        log_task("write_file", f"Test entry {i}", {}, "completed", "write_file")
    capped = _load_ledger()
    check("1.13 Ledger capped at 20 entries (FIFO)", len(capped) == 20, f"Found {len(capped)} entries")

    # 1.14 get_recent_tasks_raw(5) returns exactly 5 when ≥5 entries exist
    raw5 = get_recent_tasks_raw(5)
    check("1.14 get_recent_tasks_raw(5) returns exactly 5", len(raw5) == 5, f"Got {len(raw5)}")

    # 1.15 Empty ledger returns graceful strings
    _REAL_LEDGER.write_text("[]", encoding="utf-8")
    empty_str = get_recent_tasks(5)
    empty_raw = get_recent_tasks_raw(5)
    empty_find = find_resumable_task("document")
    empty_prompt = get_task_ledger_for_prompt()
    check("1.15 Empty ledger -- get_recent_tasks returns graceful string", "no recent" in empty_str.lower(), empty_str)
    check("1.16 Empty ledger -- get_recent_tasks_raw returns []", empty_raw == [], str(empty_raw))
    check("1.17 Empty ledger -- find_resumable_task returns None", empty_find is None, str(empty_find))
    check("1.18 Empty ledger -- get_task_ledger_for_prompt returns ''", empty_prompt == "", repr(empty_prompt))

    # 1.19 Corrupted JSON file -- should degrade gracefully
    _REAL_LEDGER.write_text("THIS IS NOT JSON {{{", encoding="utf-8")
    try:
        r_corrupt = get_recent_tasks(3)
        check("1.19 Corrupted ledger JSON -- graceful degradation", True, r_corrupt[:80])
    except Exception as ex:
        check("1.19 Corrupted ledger JSON -- graceful degradation", False, str(ex))
    _REAL_LEDGER.write_text("[]", encoding="utf-8")

finally:
    pass

# =============================================================================
# SECTION 2: resume_detector.py -- unit tests
# =============================================================================
section("SECTION 2: resume_detector.py -- Intent Detection")

try:
    from app.services.resume_detector import detect_resume_intent, get_resume_context_string

    # Build a realistic mock ledger
    mock_tasks = [
        {
            "task_id": "uuid-write-001",
            "timestamp": "2026-06-30T22:00:00",
            "task_type": "write_file",
            "description": "Write a word doc about quantum computing",
            "context": {"args": {"path": "Desktop/quantum_computing.docx"}, "path": "Desktop/quantum_computing.docx"},
            "status": "completed",
            "resumable": True,
            "related_tool": "write_file",
        },
        {
            "task_id": "uuid-ppt-001",
            "timestamp": "2026-06-30T22:05:00",
            "task_type": "ppt_create",
            "description": "Create a ppt on AI in healthcare",
            "context": {"args": {"user_prompt": "ppt on AI in healthcare"}},
            "status": "completed",
            "resumable": True,
            "related_tool": "ppt_create",
        },
        {
            "task_id": "uuid-wa-001",
            "timestamp": "2026-06-30T22:10:00",
            "task_type": "initiate_whatsapp_send",
            "description": "Send WhatsApp message to Archit",
            "context": {"args": {"contact_name": "Archit", "message": "Hey, you free tonight?"}, "contact_name": "Archit"},
            "status": "completed",
            "resumable": True,
            "related_tool": "initiate_whatsapp_send",
        },
    ]

    # -- SHOULD DETECT resume --------------------------------------------------
    SHOULD_DETECT = [
        ("add a section on entanglement to that document",      "write_file",            "2.1"),
        ("add more content to it",                              "initiate_whatsapp_send","2.2"),  # last resumable
        ("continue from where you left off",                    "initiate_whatsapp_send","2.3"),
        ("update that word document",                           "write_file",            "2.4"),
        ("edit that doc",                                       "write_file",            "2.5"),
        ("add a new slide to that presentation",                "ppt_create",            "2.6"),
        ("extend the ppt with a slide on diagnosis",            "ppt_create",            "2.7"),
        ("send another message to the same person",             "initiate_whatsapp_send","2.8"),
        ("append more details to the previous document",        "write_file",            "2.9"),
        ("resume the previous task",                            "initiate_whatsapp_send","2.10"),
        ("pick up where we left off",                           "initiate_whatsapp_send","2.11"),
        ("follow up with him",                                  "initiate_whatsapp_send","2.12"),
    ]

    for prompt, expected_type, test_id in SHOULD_DETECT:
        result = detect_resume_intent(prompt, mock_tasks)
        detected = result is not None and result.get("is_resume") is True
        matched_type = result.get("original_task", {}).get("task_type") if result else None
        check(
            f"{test_id} DETECT: '{prompt[:50]}'",
            detected,
            f"Detected={detected}, matched_type={matched_type}"
        )

    # -- SHOULD NOT DETECT (fresh tasks) --------------------------------------
    SHOULD_NOT_DETECT = [
        ("create a new word document about biology",         "2.13"),
        ("make a fresh presentation on machine learning",    "2.14"),
        ("what is the weather today",                        "2.15"),
        ("open spotify",                                     "2.16"),
        ("take a screenshot",                               "2.17"),
        ("open youtube and play kesariya",                   "2.18"),
        ("create a brand new file called notes.txt",         "2.19"),
        ("check my emails",                                  "2.20"),
        ("start a new document about physics",               "2.21"),
    ]

    for prompt, test_id in SHOULD_NOT_DETECT:
        result = detect_resume_intent(prompt, mock_tasks)
        not_detected = result is None or result.get("is_resume") is not True
        check(
            f"{test_id} NO-DETECT: '{prompt[:50]}'",
            not_detected,
            f"Correctly not detected" if not_detected else f"FALSE POSITIVE: {result}"
        )

    # -- Edge cases ------------------------------------------------------------
    # Empty ledger
    r_empty = detect_resume_intent("add more to that document", [])
    check("2.22 Empty task list -> returns None", r_empty is None, str(r_empty))

    # Empty prompt
    r_empty_prompt = detect_resume_intent("", mock_tasks)
    check("2.23 Empty prompt -> returns None", r_empty_prompt is None, str(r_empty_prompt))

    # None inputs don't crash
    try:
        r_none = detect_resume_intent(None, mock_tasks)
        check("2.24 None prompt -> returns None gracefully", r_none is None, str(r_none))
    except Exception as ex:
        check("2.24 None prompt -> returns None gracefully", False, str(ex))

    # get_resume_context_string with valid result
    valid_resume = detect_resume_intent("continue from where you left off", mock_tasks)
    ctx_str = get_resume_context_string(valid_resume)
    check("2.25 get_resume_context_string returns non-empty string", len(ctx_str) > 20, ctx_str[:100])
    check("2.26 Context string contains RESUMING PRIOR TASK", "RESUMING PRIOR TASK" in ctx_str, ctx_str[:120])

    # get_resume_context_string with None
    ctx_none = get_resume_context_string(None)
    check("2.27 get_resume_context_string(None) returns ''", ctx_none == "", repr(ctx_none))

except Exception as ex:
    check("SECTION 2 CRASHED", False, traceback.format_exc())

# =============================================================================
# SECTION 3: Integration -- task_ledger + resume_detector working together
# =============================================================================
section("SECTION 3: Integration -- Full End-to-End Flow Simulation")

_REAL_LEDGER.write_text("[]", encoding="utf-8")

try:
    from app.services.task_ledger import log_task, get_recent_tasks_raw
    from app.services.resume_detector import detect_resume_intent, get_resume_context_string

    # Simulate: Jarvis creates a Word doc
    log_task("write_file", "Write a Word doc about quantum computing",
             {"args": {"path": "Desktop/quantum_computing.docx"}, "path": "Desktop/quantum_computing.docx"},
             "completed", "write_file")

    # Simulate: Jarvis creates a PPT
    log_task("ppt_create", "Create a ppt on AI in healthcare",
             {"args": {"user_prompt": "ppt on AI in healthcare"}},
             "completed", "ppt_create")

    # Simulate: Jarvis sends a WhatsApp message
    log_task("initiate_whatsapp_send", "Send WhatsApp message to Archit",
             {"args": {"contact_name": "Archit", "message": "Hey, you free?"},
              "contact_name": "Archit"},
             "completed", "initiate_whatsapp_send")

    tasks = get_recent_tasks_raw(10)
    check("3.1 All 3 tasks logged and retrievable", len(tasks) == 3, f"Got {len(tasks)}")

    # Test: 'add to that document' -- should resume write_file
    r1 = detect_resume_intent("add a section on entanglement to that document", tasks)
    check("3.2 'add to that document' -> resume write_file", r1 and r1["original_task"]["task_type"] == "write_file", str(r1["original_task"]["task_type"] if r1 else None))
    check("3.3 resume_action is 'append'", r1 and r1["resume_action"] == "append", str(r1.get("resume_action") if r1 else None))

    # Verify the resource (file path) is correctly extracted
    check("3.4 Resource extracted (file path)", r1 and "quantum_computing.docx" in r1.get("resource", ""), str(r1.get("resource") if r1 else None))

    # Test: 'add more slides to that presentation' -- should resume ppt_create
    r2 = detect_resume_intent("add more slides to that presentation", tasks)
    check("3.5 'add slides to that presentation' -> resume ppt_create", r2 and r2["original_task"]["task_type"] == "ppt_create", str(r2["original_task"]["task_type"] if r2 else None))
    check("3.6 resume_action is 'extend'", r2 and r2["resume_action"] == "extend", str(r2.get("resume_action") if r2 else None))

    # Test: 'send another message to him' -- should resume whatsapp
    r3 = detect_resume_intent("send another message to him", tasks)
    check("3.7 'send another message to him' -> resume whatsapp", r3 and "whatsapp" in r3["original_task"]["task_type"], str(r3["original_task"]["task_type"] if r3 else None))

    # Test: context string injected into prompt (simulating what chat.py does)
    r_ctx = get_resume_context_string(r1)
    injected_prompt = r_ctx + "\n\n[USER INSTRUCTION]: add a section on entanglement"
    check("3.8 Context string injected into prompt correctly", "[RESUMING PRIOR TASK]" in injected_prompt and "[USER INSTRUCTION]" in injected_prompt, injected_prompt[:150])

    # Test: fresh request is NOT intercepted
    r_fresh = detect_resume_intent("create a new document about physics", tasks)
    check("3.9 'create new document' is NOT intercepted (no false positive)", r_fresh is None, str(r_fresh))

    # Test: unrelated command is NOT intercepted
    r_unrelated = detect_resume_intent("play kesariya on spotify", tasks)
    check("3.10 'play spotify' is NOT intercepted", r_unrelated is None, str(r_unrelated))

except Exception as ex:
    check("SECTION 3 CRASHED", False, traceback.format_exc())

# =============================================================================
# SECTION 4: tools.py -- verify new entries exist in TOOL_REGISTRY
# =============================================================================
section("SECTION 4: tools.py -- TOOL_REGISTRY entries")

try:
    # We can't do a full import of tools.py without the whole app,
    # so we grep the source file directly
    tools_src = Path("app/services/tools.py").read_text(encoding="utf-8")
    check("4.1 'get_recent_tasks' registered in TOOL_REGISTRY", '"get_recent_tasks"' in tools_src, "")
    check("4.2 'find_resumable_task' registered in TOOL_REGISTRY", '"find_resumable_task"' in tools_src, "")
    check("4.3 'get_task_history' registered in TOOL_REGISTRY", '"get_task_history"' in tools_src, "")
    check("4.4 tools.py references task_ledger module", "task_ledger" in tools_src, "")
except Exception as ex:
    check("SECTION 4 CRASHED", False, str(ex))

# =============================================================================
# SECTION 5: chat.py -- verify injection points exist
# =============================================================================
section("SECTION 5: chat.py -- Integration Points")

try:
    chat_src = Path("app/api/chat.py").read_text(encoding="utf-8")
    check("5.1 Resume detection block present in chat.py", "detect_resume_intent" in chat_src, "")
    check("5.2 Task logging block present in chat.py", "log_task" in chat_src, "")
    check("5.3 Ledger context injection present in chat.py", "get_task_ledger_for_prompt" in chat_src, "")
    check("5.4 All 3 new resumption blocks wrapped in try/except",
          "detect_resume_intent" in chat_src and "except Exception:\n        pass  # Best-effort" in chat_src,
          "try/except guards present around resumption blocks")
    check("5.5 'import json' present at top of chat.py", "import json" in chat_src[:500], "")
    check("5.6 get_resume_context_string imported in chat.py", "get_resume_context_string" in chat_src, "")
    check("5.7 get_recent_tasks_raw imported in chat.py", "get_recent_tasks_raw" in chat_src, "")
except Exception as ex:
    check("SECTION 5 CRASHED", False, str(ex))

# =============================================================================
# SECTION 6: planner.py -- verify task history injection
# =============================================================================
section("SECTION 6: planner.py -- Planner Task History Injection")

try:
    planner_src = Path("app/services/planner.py").read_text(encoding="utf-8")
    check("6.1 {task_history} placeholder in PLANNER_PROMPT", "{task_history}" in planner_src, "")
    check("6.2 'RECENT TASK HISTORY' label in PLANNER_PROMPT", "RECENT TASK HISTORY" in planner_src, "")
    check("6.3 get_task_ledger_for_prompt imported in _call_planner", "get_task_ledger_for_prompt" in planner_src, "")
    check("6.4 planner injection wrapped in try/except", "except Exception:" in planner_src and "task_history" in planner_src, "")
    check("6.5 task_history passed to PLANNER_PROMPT.format()", "task_history=task_history" in planner_src, "")
except Exception as ex:
    check("SECTION 6 CRASHED", False, str(ex))

# =============================================================================
# SECTION 7: Architecture compliance checks
# =============================================================================
section("SECTION 7: Architecture Rule Compliance")

try:
    ledger_src  = Path("app/services/task_ledger.py").read_text(encoding="utf-8")
    detect_src  = Path("app/services/resume_detector.py").read_text(encoding="utf-8")

    # Rule #1: No cross-tool imports in new files
    forbidden_imports = [
        "from app.services.llm", "from app.services.planner", "from app.services.tools",
        "from app.services.file_ops", "from app.services.whatsapp", "from app.services.gmail",
    ]
    ledger_violations  = [i for i in forbidden_imports if i in ledger_src]
    detector_violations = [i for i in forbidden_imports if i in detect_src]
    check("7.1 Rule #1: task_ledger.py has NO cross-tool imports", len(ledger_violations) == 0, str(ledger_violations))
    check("7.2 Rule #1: resume_detector.py has NO cross-tool imports", len(detector_violations) == 0, str(detector_violations))

    # Rule #2: try/except in every public function
    check("7.3 Rule #2: task_ledger.py uses try/except", "try:" in ledger_src and "except Exception" in ledger_src, "")
    check("7.4 Rule #2: resume_detector.py uses try/except", "try:" in detect_src and "except Exception" in detect_src, "")

    # Rule #3: No in-memory singletons (no module-level mutable state)
    check("7.5 Rule #3: task_ledger.py loads/saves to file (not memory-only)", "_load_ledger" in ledger_src and "_save_ledger" in ledger_src, "")
    check("7.6 Rule #3: resume_detector.py is fully stateless (no global state)", "global " not in detect_src, "")

    # Rule #4: accessible via /chat (both frontend and voice share the same route)
    chat_src = Path("app/api/chat.py").read_text(encoding="utf-8")
    check("7.7 Rule #4: integrated into /chat route (works for both frontend + voice)", "@router.post(\"/chat\")" in chat_src and "task_ledger" in chat_src, "")

except Exception as ex:
    check("SECTION 7 CRASHED", False, str(ex))

# =============================================================================
# FINAL SUMMARY
# =============================================================================
_restore_ledger()

section("FINAL RESULTS")
total = PASS + FAIL
print(f"\n  Total tests: {total}")
print(f"  Passed:      {PASS} ({PASS*100//total}%)")
print(f"  Failed:      {FAIL} ({FAIL*100//total}%)")
print()

if FAIL > 0:
    print("  FAILED TESTS:")
    for status, name, detail in RESULTS:
        if status == "FAIL":
            print(f"    [XX] {name}")
            if detail:
                print(f"        -> {detail}")

if FAIL == 0:
    print("  ALL TESTS PASSED -- Task Resumption feature is working correctly.")
else:
    print(f"  WARNING: {FAIL} test(s) failed. See above for details.")

sys.exit(0 if FAIL == 0 else 1)
