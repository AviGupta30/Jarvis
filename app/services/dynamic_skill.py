"""
Dynamic Skill Engine for Jarvis 2.0
-------------------------------------
When Jarvis doesn't have a built-in tool for a task, this engine:
  1. Checks long-term memory for a previously learned skill.
  2. If found AND similarity > threshold → execute it directly.
  3. If not found → asks Groq LLM to write a Python script.
  4. Validates via safe_executor (AST security scan).
  5. Runs it and captures output.
  6. If successful → saves to memory for future use.
  7. If error → sends error back to LLM to self-fix (up to 3 retries).
"""

import os
import sys
import asyncio
from groq import AsyncGroq
from app.core.config import settings
from app.services.safe_executor import execute_safe
from app.memory import find_skill, save_skill

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# Similarity threshold: if closest skill distance < this, reuse it directly
SKILL_REUSE_THRESHOLD = 0.35

SKILL_WRITER_PROMPT = """\
You are Jarvis's dynamic execution brain. Write a self-contained Python script to accomplish the user's task on a Windows 11 laptop.

AVAILABLE LIBRARIES AND APIs — use these directly, they are already importable:
  os, sys, re, json, time, pathlib, subprocess, shutil, datetime
  pyautogui      — mouse clicks, keyboard input, screenshots (pyautogui.click, hotkey, press, typewrite, screenshot)
  pygetwindow    — find and focus windows (gw.getAllWindows(), win.activate(), win.restore(), win.maximize())
  pyperclip      — clipboard read/write (pyperclip.paste(), pyperclip.copy(text))
  requests       — HTTP requests
  webbrowser     — open URLs (webbrowser.open(url))
  psutil         — system info (psutil.cpu_percent(), psutil.virtual_memory())
  pdfplumber     — read PDF text (with pdfplumber.open(path) as pdf: for p in pdf.pages: p.extract_text())
  python-docx    — create Word docs (from docx import Document; doc = Document(); doc.add_heading(...); doc.save(path))
  win32com.client — Office COM automation (word, excel, outlook via win32com.client.Dispatch)

JARVIS BUILT-IN FUNCTIONS (already injected, call directly):
  get_screen_text_summary()   → returns string of active window UI text (use to verify state)
  get_active_window_info()    → detailed accessibility tree of focused window
  click_ui_element("text")    → finds a UI control containing "text" and clicks its center, returns bool

WINDOWS COPILOT (sidebar):
  - Open with: pyautogui.hotkey('win', 'c'); time.sleep(2.5)
  - Then click input area, type question, press Enter
  - Wait for response (time.sleep(8)), then try clicking "Copy" button or ctrl+c

STRICT RULES:
1. The script MUST be self-contained. Handle all imports at the top.
2. For missing third-party libraries: wrap import in try/except and use subprocess.run([sys.executable, "-m", "pip", "install", "<pkg>", "-q"]) then re-import.
3. NEVER use: os.remove, os.unlink, os.rmdir, shutil.rmtree — these are permanently blocked.
4. Add time.sleep() between UI actions to let windows animate (min 0.5s after clicks, 2s after opening apps).
5. Print a clear, human-readable success message at the very end (e.g. "Done! Created Assignment_Answers.docx on your Desktop.").
6. Return ONLY raw Python code. No markdown, no ```python fences, no explanations.

SCREEN CONTEXT (what's currently visible):
{context}

TASK:
{task}

PYTHON CODE:
"""

SKILL_FIXER_PROMPT = """\
The following Python script produced an error. Fix it to accomplish the task.

TASK:
{task}

PREVIOUS CODE:
{code}

ERROR:
{error}

STRICT RULES:
- If a module is missing (ModuleNotFoundError), add: subprocess.run([sys.executable, "-m", "pip", "install", "<module>", "-q"])
- Do not use os.remove, shutil.rmtree or any destructive file ops.
- Add time.sleep() between UI actions.
- Return ONLY the corrected raw Python code. No markdown, no ``` fences.

FIXED CODE:
"""


async def _llm_write_code(task: str, context: str = "") -> str:
    """Ask the LLM to write Python code for a given task."""
    prompt = SKILL_WRITER_PROMPT.format(task=task, context=context or "None")
    resp = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


async def _llm_fix_code(task: str, code: str, error: str) -> str:
    """Ask the LLM to fix a broken script."""
    prompt = SKILL_FIXER_PROMPT.format(task=task, code=code, error=error)
    resp = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.1,
    )
    return resp.choices[0].message.content.strip()


def _strip_fences(code: str) -> str:
    """Remove accidental markdown code fences if LLM adds them."""
    import re
    code = re.sub(r"^```(?:python)?\s*", "", code, flags=re.MULTILINE)
    code = re.sub(r"```\s*$", "", code, flags=re.MULTILINE)
    return code.strip()


async def run_dynamic_skill(task: str, ui_context: str = "") -> str:
    """
    Main entry point. Tries memory first, then LLM-generation.

    Returns:
        A human-readable result string for Jarvis to speak.
    """
    # 1. Check memory for a matching past skill
    skills = find_skill(task, n=1)
    if skills and skills[0]["distance"] < SKILL_REUSE_THRESHOLD:
        saved = skills[0]
        print(f"[DynamicSkill] Reusing learned skill: '{saved['description'][:60]}'")
        success, output = await asyncio.get_event_loop().run_in_executor(
            None, execute_safe, saved["code"]
        )
        if success:
            return f"Done (learned skill)! {output}"
        # Skill failed — fall through to regeneration
        print(f"[DynamicSkill] Saved skill failed, regenerating...")

    # 2. Generate new code
    code = await _llm_write_code(task, context=ui_context)
    code = _strip_fences(code)
    print(f"[DynamicSkill] Generated code:\n{code}\n")

    # 3. Execute with up to 3 self-fix retries
    max_retries = 3
    for attempt in range(max_retries):
        loop = asyncio.get_event_loop()
        success, output = await loop.run_in_executor(None, execute_safe, code)

        if success:
            # 4. Save to memory for future reuse
            save_skill(task, code)
            print(f"[DynamicSkill] Skill saved to memory.")
            return output or "Done!"

        print(f"[DynamicSkill] Attempt {attempt+1} failed: {output[:200]}")
        if attempt < max_retries - 1:
            code = await _llm_fix_code(task, code, output)
            code = _strip_fences(code)
            print(f"[DynamicSkill] Fixed code:\n{code}\n")

    return f"I tried {max_retries} times but couldn't complete that task. The last error was: {output[:150]}"
