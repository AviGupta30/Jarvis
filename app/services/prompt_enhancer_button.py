"""
prompt_enhancer_button.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Floating "✦ Enhance" button that pops up next to whatever prompt box you are
typing in (Windows only).

  - Follows keyboard focus through UI Automation: when the focused element is an
    editable prompt box inside an AI site/app, the pill appears just above the
    box's top-right corner and follows it; it hides as soon as focus leaves.
    Works in browsers (ChatGPT, Gemini, Claude, Copilot, Perplexity, ... matched
    by the address-bar URL), IDE chat panels (VS Code Claude Code / Copilot Chat,
    Antigravity, Cursor, Windsurf, ...) and AI desktop apps (ChatGPT, Claude,
    Copilot, ...). JARVIS_ENHANCER_SCOPE=all shows it on every text box.
  - Click-only: nothing is sent until the pill is clicked. Click → Ctrl+A, Ctrl+C
    in the box → skill_prompt_enhancer.enhance_prompt_text() → Ctrl+A, Ctrl+V →
    the user's clipboard is restored.
  - Started automatically by the backend (app/main.py) and, optionally, at
    Windows login (--install-autostart). A named mutex keeps one instance.
    Disable the backend spawn with JARVIS_ENHANCER_BUTTON=0.
        python -m app.services.prompt_enhancer_button                 # run
        python -m app.services.prompt_enhancer_button --install-autostart
        python -m app.services.prompt_enhancer_button --uninstall-autostart
  - Left-drag moves it (offset per site/app in app/memory/enhancer_button.json).
    Right-click: undo, copy last result, hide for this site/app, reset position.
  - Log: app/memory/enhancer_button.log
"""

import ctypes
import ctypes.wintypes as wt
import json
import os
import queue
import re
import sys
import threading
import time
import tkinter as tk
from collections import namedtuple
from pathlib import Path
from tkinter import font as tkfont
from urllib.parse import urlparse

import psutil
import win32clipboard
import win32con
import win32gui
import win32process

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
except Exception:
    pass

user32 = ctypes.windll.user32
# explicit signatures: HWND_TOPMOST (-1) must be passed as a pointer-sized handle on x64
user32.SetWindowPos.argtypes = [wt.HWND, wt.HWND, ctypes.c_int, ctypes.c_int,
                                ctypes.c_int, ctypes.c_int, ctypes.c_uint]
user32.ShowWindow.argtypes = [wt.HWND, ctypes.c_int]
user32.GetParent.argtypes = [wt.HWND]
user32.GetParent.restype = wt.HWND

# ── Config ───────────────────────────────────────────────────────────────────
SCOPE = os.getenv("JARVIS_ENHANCER_SCOPE", "ai").strip().lower()   # ai | all

BROWSER_EXES = {
    "chrome.exe", "msedge.exe", "brave.exe", "firefox.exe", "opera.exe",
    "opera_gx.exe", "vivaldi.exe", "arc.exe", "comet.exe", "zen.exe", "floorp.exe",
}
# Sites matched against host (and path prefix when given).
AI_SITES = [
    "chatgpt.com", "chat.openai.com", "sora.com", "gemini.google.com",
    "aistudio.google.com", "notebooklm.google.com", "labs.google", "jules.google.com",
    "claude.ai", "copilot.microsoft.com", "m365.cloud.microsoft",
    "copilot.cloud.microsoft", "perplexity.ai", "chat.deepseek.com", "grok.com",
    "x.com/i/grok", "chat.mistral.ai", "poe.com", "huggingface.co/chat", "meta.ai",
    "chat.qwen.ai", "kimi.com", "you.com", "character.ai", "chat.z.ai",
    "github.com/copilot", "v0.dev", "v0.app", "bolt.new", "lovable.dev",
    "replit.com", "midjourney.com", "leonardo.ai", "ideogram.ai", "suno.com",
]
# Fallback when the browser URL can't be read: whole-word match in the title.
AI_TITLE_WORDS = [
    "chatgpt", "gemini", "claude", "copilot", "perplexity", "deepseek", "grok",
    "mistral", "le chat", "poe", "meta ai", "qwen", "ai studio",
]
# AI desktop apps (exe name, lower-case).
AI_APP_EXES = {
    "chatgpt.exe", "claude.exe", "copilot.exe", "mscopilot_proxy.exe",
    "m365copilot.exe", "perplexity.exe", "deepseek.exe", "grok.exe",
}
# IDEs: only their chat / agent inputs get the button, never the code editor.
IDE_EXES = {
    "code.exe", "code - insiders.exe", "antigravity.exe", "antigravity ide.exe",
    "cursor.exe", "windsurf.exe", "trae.exe", "kiro.exe", "void.exe", "zed.exe",
}
# Never show here, even with SCOPE=all (terminals: Ctrl+C would kill the process).
EXCLUDED_EXES = {
    "windowsterminal.exe", "cmd.exe", "powershell.exe", "pwsh.exe", "conhost.exe",
    "openconsole.exe", "wezterm-gui.exe", "alacritty.exe", "mintty.exe",
    "explorer.exe", "searchhost.exe", "startmenuexperiencehost.exe",
    "textinputhost.exe", "lockapp.exe", "keepass.exe", "1password.exe", "bitwarden.exe",
}
# Hints that a focused element (or an ancestor) is a chat / prompt input.
CHAT_HINTS = (
    "chat", "prompt", "message", "agent", "cascade", "composer", "conversation",
    "interactive", "copilot", "claude", "gemini", "assistant", "ask ", "aichat",
)

EXTRA_URL_PARTS = []
for _extra in filter(None, (s.strip().lower() for s in os.getenv("JARVIS_ENHANCER_APPS", "").split(","))):
    if _extra.endswith(".exe"):
        AI_APP_EXES.add(_extra)
    else:
        EXTRA_URL_PARTS.append(_extra)

MEMORY_DIR = REPO_ROOT / "app" / "memory"
STATE_FILE = MEMORY_DIR / "enhancer_button.json"
LOG_FILE = MEMORY_DIR / "enhancer_button.log"
GAP = 6                                   # px between pill and prompt box
MAX_BROWSER_CHARS = 15000
MAX_IDE_CHARS, MAX_IDE_LINES = 6000, 120

# Colours (match prompt_overlay.py)
KEY_COLOR = "#010203"          # transparent colour key
PILL_BG = "#1a1a2e"
PILL_HOVER = "#262648"
ACCENT = "#7c6af7"
TEXT = "#e2e0ff"
OK_GREEN = "#4ade80"
ERR_RED = "#f87171"

# A prompt box the button is attached to.
Target = namedtuple("Target", "hwnd key exe kind box")   # kind: browser | ide | app | any

# ── Win32 helpers ────────────────────────────────────────────────────────────
GWL_EXSTYLE = -20
WS_EX_TOPMOST, WS_EX_TOOLWINDOW, WS_EX_NOACTIVATE = 0x8, 0x80, 0x08000000
HWND_TOPMOST = -1
SWP_NOACTIVATE, SWP_SHOWWINDOW = 0x10, 0x40
VK_CONTROL, KEYEVENTF_KEYUP = 0x11, 0x2


def _set_dpi_aware():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass


def _window_rect(hwnd):
    """Visible frame bounds (excludes the invisible resize border)."""
    rect = wt.RECT()
    try:
        if ctypes.windll.dwmapi.DwmGetWindowAttribute(
                wt.HWND(hwnd), 9, ctypes.byref(rect), ctypes.sizeof(rect)) == 0:
            return rect.left, rect.top, rect.right, rect.bottom
    except Exception:
        pass
    return win32gui.GetWindowRect(hwnd)


def _ctrl(vk):
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)


def _clip_get():
    for _ in range(15):
        try:
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                return None
            finally:
                win32clipboard.CloseClipboard()
        except Exception:
            time.sleep(0.03)
    return None


def _clip_set(text):
    for _ in range(15):
        try:
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                if text is not None:
                    win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
                return True
            finally:
                win32clipboard.CloseClipboard()
        except Exception:
            time.sleep(0.03)
    return False


def _focus(hwnd):
    if user32.GetForegroundWindow() == hwnd:
        return True
    try:
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.12)
    except Exception:
        pass
    return user32.GetForegroundWindow() == hwnd


# ── App / site detection ─────────────────────────────────────────────────────
def _site_match(url: str):
    if not url:
        return None
    u = url.strip().lower()
    full = u if "://" in u else "https://" + u
    try:
        p = urlparse(full)
        host = (p.hostname or "").removeprefix("www.")
    except Exception:
        return None
    path = p.path or "/"
    for site in AI_SITES:
        if "/" in site:
            s_host, s_path = site.split("/", 1)
            if host == s_host and path.startswith("/" + s_path):
                return site
        elif host == site or host.endswith("." + site):
            return site
    return next((part for part in EXTRA_URL_PARTS if part in u), None)


def _title_match(title: str):
    lower = title.lower()
    for w in AI_TITLE_WORDS:
        if re.search(rf"(^|[^a-z]){re.escape(w)}([^a-z]|$)", lower):
            return w
    return None


def _app_title_match(title: str):
    """Desktop AI apps whose exe we don't know: title is exactly the product name."""
    t = title.strip().lower()
    for name in ("chatgpt", "claude", "copilot", "microsoft copilot", "gemini",
                 "perplexity", "deepseek", "grok", "meta ai"):
        if t == name or t.startswith(name + " -") or t.endswith("- " + name):
            return name
    return None


def _browser_url(hwnd):
    """Read the address bar through UI Automation (~0.2 s). None if unreadable."""
    import uiautomation as auto
    try:
        win = auto.ControlFromHandle(hwnd)
        bar = win.ToolBarControl(searchDepth=12)
        if not bar.Exists(0, 0):
            return None
        edit = bar.EditControl(searchDepth=6)
        if not edit.Exists(0, 0):
            return None
        return edit.GetValuePattern().Value
    except Exception:
        return None


def _exe_name(pid, cache={}):
    if pid not in cache:
        try:
            cache[pid] = psutil.Process(pid).name().lower()
        except Exception:
            cache[pid] = ""
    return cache[pid]


def classify_app(hwnd, pid, title):
    """(key, exe, kind) if prompt boxes in this window should get the button, else None."""
    exe = _exe_name(pid)
    if not exe or exe in EXCLUDED_EXES:
        return None
    if exe in BROWSER_EXES:
        url = _browser_url(hwnd)
        site = _site_match(url) if url else _title_match(title)
        if site:
            return (site, exe, "browser")
        return (exe, exe, "any") if SCOPE == "all" else None
    if exe in IDE_EXES:
        return (exe, exe, "ide")
    if exe in AI_APP_EXES:
        return (exe, exe, "app")
    name = _app_title_match(title)
    if name:
        return (name, exe, "app")
    return (exe, exe, "any") if SCOPE == "all" else None


# ── Prompt-box detection (focused UIA element) ───────────────────────────────
def _has_pattern(ctrl, pattern_id):
    try:
        return bool(ctrl.GetPattern(pattern_id))
    except Exception:
        return False


def _is_editable(ctrl):
    """Writable text input: <textarea>/<input>/native edit, or a contenteditable
    (Chromium exposes those as a focusable Group/Document with a TextPattern)."""
    import uiautomation as auto
    try:
        if ctrl.IsPassword:
            return False
    except Exception:
        pass
    ctype = ctrl.ControlTypeName
    has_value = _has_pattern(ctrl, auto.PatternId.ValuePattern)
    read_only = False
    if has_value:
        try:
            read_only = ctrl.GetValuePattern().IsReadOnly
        except Exception:
            pass
    if ctype in ("EditControl", "ComboBoxControl"):
        return not read_only
    if ctype in ("GroupControl", "CustomControl", "DocumentControl", "PaneControl", "TextControl"):
        # page root documents expose a read-only ValuePattern (the URL)
        return _has_pattern(ctrl, auto.PatternId.TextPattern) and not (has_value and read_only)
    return False


def _hint_text(ctrl):
    return " ".join(filter(None, (
        ctrl.Name, ctrl.ClassName, ctrl.AutomationId))).lower()


def _ide_allows(ctrl, window_title):
    """In IDEs only chat / agent inputs qualify, never the code editor, the
    terminal, or the IDE's own search/quick-open boxes."""
    own = _hint_text(ctrl)
    if "xterm" in own or "terminal" in own:
        return False
    # Monaco (class "inputarea") is used for code editors AND some chat inputs, and
    # its name can be a file name like "chat.py", so only ancestors decide for it.
    monaco = "inputarea" in own or "monaco" in own
    if not monaco and any(h in own for h in CHAT_HINTS):
        return True                           # e.g. Claude Code "Message input"
    title = window_title.strip().lower()
    c = ctrl
    for _ in range(25):
        try:
            c = c.GetParentControl()
        except Exception:
            c = None
        if not c:
            return False
        hint = " ".join(filter(None, (c.ClassName, c.AutomationId))).lower()
        if "xterm" in hint or "terminal" in hint or "editor-instance" in hint:
            return False                       # code editor / terminal
        if any(h in hint for h in CHAT_HINTS):
            return True
        if c.ControlTypeName == "DocumentControl":
            name = (c.Name or "").strip().lower()
            # the workbench's own document is named like the window; any other
            # (nested) document is a webview panel such as Claude Code
            return not monaco and (not name or not title.startswith(name))
    return False


def is_prompt_box(ctrl, kind, window_title):
    if not _is_editable(ctrl):
        return False
    own = _hint_text(ctrl)
    if "omniboxviewviews" in own or "urlbar" in own or "address and search bar" in own:
        return False                           # browser address bar
    if kind == "ide":
        return _ide_allows(ctrl, window_title)
    if "xterm" in own or "terminal" in own:
        return False
    return True


def _norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def _focused_text():
    """Text of the focused box via UIA, or None if unreadable. Note: empty boxes
    often report their placeholder, so only use this for 'contains X' checks."""
    import uiautomation as auto
    with auto.UIAutomationInitializerInThread():
        ctrl = auto.GetFocusedControl()
        if not ctrl:
            return None
        try:
            return ctrl.GetValuePattern().Value
        except Exception:
            pass
        try:
            return ctrl.GetTextPattern().DocumentRange.GetText(-1)
        except Exception:
            return None


def _box_contains(text):
    """True/False whether the focused box now holds `text`; None if unreadable."""
    try:
        current = _focused_text()
    except Exception:
        return None
    if current is None:
        return None
    probe = _norm(text)[:40]
    return bool(probe) and probe in _norm(current)


def _box_set_value(text):
    """Fallback write through UIA ValuePattern (fires input events in Chromium)."""
    import uiautomation as auto
    try:
        with auto.UIAutomationInitializerInThread():
            ctrl = auto.GetFocusedControl()
            vp = ctrl.GetValuePattern()
            if vp.IsReadOnly:
                return False
            vp.SetValue(text)
        time.sleep(0.2)
        return _box_contains(text) is not False
    except Exception:
        return False


# ── State persistence (per-app button offsets) ───────────────────────────────
def _load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"offsets": {}}


def _save_state(state):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[EnhanceButton] could not save state: {e}")


# ═════════════════════════════════════════════════════════════════════════════
class EnhanceButton:
    def __init__(self, parent_pid=None):
        self.parent_pid = parent_pid
        self.state = _load_state()
        self.state.setdefault("offsets", {})
        self.hidden_keys = set()
        self.target = None             # Target or None (written by the watcher thread)
        self.cur = None                # target the pill is currently attached to
        self._lock = threading.Lock()
        self.ui_q = queue.Queue()
        self.busy = False
        self.visible = False
        self.pos = (-3000, -3000)
        self.size = (0, 0)
        self.label = "✦ Enhance"
        self.label_color = TEXT
        self.hover = False
        self.drag = None
        self.last_undo = None          # (hwnd, original_text)
        self.last_result = None
        self._label_reset_id = None

    # ── Tk window ────────────────────────────────────────────────────────────
    def build(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.config(bg=KEY_COLOR)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", KEY_COLOR)
        self.scale = self.root.winfo_fpixels("1i") / 96.0
        self.font = tkfont.Font(family="Segoe UI Semibold", size=9)
        self.canvas = tk.Canvas(self.root, bg=KEY_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.root.geometry("10x10+-3000+-3000")
        self.root.deiconify()
        self.root.update_idletasks()
        self.hwnd = user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()
        ex = user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(self.hwnd, GWL_EXSTYLE,
                              ex | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW | WS_EX_TOPMOST)
        self._hide()
        self._render()

        c = self.canvas
        c.bind("<Enter>", lambda e: self._set_hover(True))
        c.bind("<Leave>", lambda e: self._set_hover(False))
        c.bind("<ButtonPress-1>", self._on_press)
        c.bind("<B1-Motion>", self._on_motion)
        c.bind("<ButtonRelease-1>", self._on_release)
        c.bind("<ButtonRelease-3>", self._on_menu)

        self.menu = tk.Menu(self.root, tearoff=0, bg=PILL_BG, fg=TEXT,
                            activebackground=ACCENT, activeforeground="white", bd=0)
        self.menu.add_command(label="Undo last enhance", command=self._undo)
        self.menu.add_command(label="Copy last enhanced prompt", command=self._copy_last)
        self.menu.add_separator()
        self.menu.add_command(label="Hide on this site/app (until restart)", command=self._hide_here)
        self.menu.add_command(label="Reset button position", command=self._reset_pos)

    def _render(self):
        s = self.scale
        text = self.label
        h = int(26 * s)
        w = max(int(88 * s), self.font.measure(text) + int(26 * s))
        c = self.canvas
        c.delete("all")
        c.config(width=w, height=h)
        r = h // 2
        fill = PILL_HOVER if (self.hover and not self.busy) else PILL_BG
        # border pill, then inner pill
        for inset, colour in ((0, ACCENT), (max(1, int(1.5 * s)), fill)):
            x0, y0, x1, y1 = inset, inset, w - 1 - inset, h - 1 - inset
            rr = r - inset
            c.create_oval(x0, y0, x0 + 2 * rr, y1, fill=colour, outline=colour)
            c.create_oval(x1 - 2 * rr, y0, x1, y1, fill=colour, outline=colour)
            c.create_rectangle(x0 + rr, y0, x1 - rr, y1, fill=colour, outline=colour)
        c.create_text(w // 2, h // 2, text=text, fill=self.label_color, font=self.font)
        if (w, h) != self.size:
            # keep the right edge anchored when the label width changes
            x, y = self.pos
            if self.size != (0, 0):
                x += self.size[0] - w
            self.size = (w, h)
            self._move(x, y)

    def _set_hover(self, on):
        self.hover = on
        self._render()

    def _set_label(self, text, color=TEXT, reset_after=None):
        self.label, self.label_color = text, color
        self._render()
        if self._label_reset_id:
            self.root.after_cancel(self._label_reset_id)
            self._label_reset_id = None
        if reset_after:
            self._label_reset_id = self.root.after(reset_after, lambda: self._set_label("✦ Enhance"))

    def _move(self, x, y, show=False):
        """Move (and optionally show) without ever activating the window;
        Tk's deiconify() would steal focus from the prompt box."""
        self.pos = (int(x), int(y))
        flags = SWP_NOACTIVATE | (SWP_SHOWWINDOW if show else 0)
        w, h = self.size
        user32.SetWindowPos(self.hwnd, HWND_TOPMOST, int(x), int(y), int(w), int(h), flags)

    def _hide(self):
        if getattr(self, "hwnd", None):
            user32.ShowWindow(self.hwnd, 0)
        self.visible = False

    # ── Focus watcher (background thread) ────────────────────────────────────
    def _watch_loop(self):
        import uiautomation as auto
        my_pid = os.getpid()
        app_cache = {}                 # hwnd -> (title, classify_app result, checked_at)
        box_cache = {}                 # element runtime id -> is_prompt_box
        with auto.UIAutomationInitializerInThread():
            while True:
                try:
                    if self.parent_pid and not psutil.pid_exists(self.parent_pid):
                        self.ui_q.put(lambda: os._exit(0))
                        return
                    self._set_target(self._detect(auto, my_pid, app_cache, box_cache))
                except Exception as e:
                    print(f"[EnhanceButton] watcher error: {e}")
                time.sleep(0.2)

    def _set_target(self, t):
        if t is Ellipsis:              # our own window/menu has focus: keep as is
            return
        with self._lock:
            self.target = t

    def _detect(self, auto, my_pid, app_cache, box_cache):
        fg = user32.GetForegroundWindow()
        if not fg:
            return None
        _, pid = win32process.GetWindowThreadProcessId(fg)
        if pid == my_pid:
            return Ellipsis
        title = win32gui.GetWindowText(fg)
        # re-classify on title change (tab switch / navigation), but at most once a
        # second per window: some pages rewrite their title constantly
        cached = app_cache.get(fg)
        now = time.time()
        if not cached or (cached[0] != title and now - cached[2] > 1.0):
            if len(app_cache) > 200:
                app_cache.clear()
            cached = app_cache[fg] = (title, classify_app(fg, pid, title), now)
        app = cached[1]
        if not app:
            return None
        ctrl = auto.GetFocusedControl()
        if not ctrl:
            return None
        try:
            if ctrl.ProcessId == my_pid:
                return Ellipsis
        except Exception:
            pass
        try:
            rid = tuple(ctrl.GetRuntimeId() or ()) or None
        except Exception:
            rid = None
        cache_key = (fg, rid) if rid else None
        if cache_key and cache_key in box_cache:
            ok = box_cache[cache_key]
        else:
            ok = is_prompt_box(ctrl, app[2], title)
            if cache_key:
                if len(box_cache) > 500:
                    box_cache.clear()
                box_cache[cache_key] = ok
        if not ok:
            return None
        r = ctrl.BoundingRectangle
        if r.width() <= 4 or r.height() <= 4:
            return None
        return Target(fg, app[0], app[1], app[2], (r.left, r.top, r.right, r.bottom))

    # ── UI tick (Tk thread) ──────────────────────────────────────────────────
    def _tick(self):
        try:
            while True:
                self.ui_q.get_nowait()()
        except queue.Empty:
            pass
        try:
            self._update_position()
        except Exception as e:
            print(f"[EnhanceButton] ui error: {e}")
        self.root.after(120, self._tick)

    def _anchor(self, t):
        """Default spot: just above the prompt box's top-right corner; below it or
        inside its top-right corner when there is no room above."""
        bl, bt, br, bb = t.box
        wl, wt_, wr, wb = _window_rect(t.hwnd)
        w, h = self.size
        if bt - h - GAP >= wt_ + 2:
            x, y = br - w, bt - h - GAP          # above
        elif bb + GAP + h <= wb:
            x, y = br - w, bb + GAP              # below
        else:
            x, y = br - w - GAP, bt + GAP        # inside, top-right
        off = self.state["offsets"].get(t.key, {"dx": 0, "dy": 0})
        x, y = x + off.get("dx", 0), y + off.get("dy", 0)
        x = min(max(x, wl), wr - w)
        y = min(max(y, wt_), wb - h)
        return int(x), int(y)

    def _update_position(self):
        if self.drag:
            return
        with self._lock:
            t = self.target
        if self.busy:                          # keep the progress label where it is
            return
        if not t or t.key in self.hidden_keys or win32gui.IsIconic(t.hwnd):
            if self.visible:
                self._hide()
            return
        x, y = self._anchor(t)
        if not self.visible or (x, y) != self.pos:
            self._move(x, y, show=True)
            self.visible = True
        self.cur = t

    # ── Mouse ────────────────────────────────────────────────────────────────
    def _on_press(self, e):
        self.drag = None
        self._press = (e.x_root, e.y_root, self.pos)

    def _on_motion(self, e):
        x0, y0, (px, py) = self._press
        dx, dy = e.x_root - x0, e.y_root - y0
        if self.drag or abs(dx) + abs(dy) > 5:
            self.drag = True
            self._move(px + dx, py + dy)

    def _on_release(self, e):
        if self.drag:
            self.drag = None
            t = self.cur
            if t:
                self.state["offsets"].pop(t.key, None)
                ax, ay = self._anchor(t)             # default spot, without offset
                self.state["offsets"][t.key] = {"dx": self.pos[0] - ax, "dy": self.pos[1] - ay}
                _save_state(self.state)
            return
        self._click()

    def _on_menu(self, e):
        try:
            self.menu.tk_popup(e.x_root, e.y_root)
        finally:
            self.menu.grab_release()

    # ── Menu actions ─────────────────────────────────────────────────────────
    def _undo(self):
        if not self.last_undo:
            self._set_label("Nothing to undo", reset_after=1800)
            return
        hwnd, original = self.last_undo
        self.busy = True
        threading.Thread(target=self._paste_into, args=(hwnd, original, "↶ Restored"), daemon=True).start()

    def _copy_last(self):
        if self.last_result:
            _clip_set(self.last_result.replace("\n", "\r\n"))
            self._set_label("✓ Copied", OK_GREEN, 1500)
        else:
            self._set_label("Nothing yet", reset_after=1500)

    def _hide_here(self):
        if self.cur:
            self.hidden_keys.add(self.cur.key)
            self._hide()

    def _reset_pos(self):
        if self.cur and self.cur.key in self.state["offsets"]:
            del self.state["offsets"][self.cur.key]
            _save_state(self.state)

    # ── Enhance flow ─────────────────────────────────────────────────────────
    def _click(self):
        if self.busy or not self.cur:
            return
        self.busy = True
        self._animate(0)
        threading.Thread(target=self._enhance_worker, args=(self.cur,), daemon=True).start()

    def _animate(self, i):
        if not self.busy:
            return
        self.label, self.label_color = "Enhancing" + "." * (i % 4), TEXT
        self._render()
        self.root.after(350, self._animate, i + 1)

    def _done(self, text, color, ms=2600):
        self.busy = False
        self._set_label(text, color, ms)

    def _enhance_worker(self, t):
        post = self.ui_q.put
        original_clip = _clip_get()
        try:
            if not _focus(t.hwnd):
                post(lambda: self._done("Click the prompt box first", ERR_RED))
                return

            # 1. grab the prompt
            seq = user32.GetClipboardSequenceNumber()
            _ctrl(ord("A"))
            time.sleep(0.06)
            _ctrl(ord("C"))
            raw = None
            for _ in range(30):
                time.sleep(0.03)
                if user32.GetClipboardSequenceNumber() != seq:
                    time.sleep(0.03)
                    raw = _clip_get()
                    break
            raw = (raw or "").replace("\r\n", "\n").strip()
            if not raw:
                _clip_set(original_clip)
                post(lambda: self._done("Type a prompt first", ERR_RED))
                return
            too_long = (len(raw) > MAX_IDE_CHARS or raw.count("\n") > MAX_IDE_LINES) \
                if t.kind == "ide" else len(raw) > MAX_BROWSER_CHARS
            if too_long:
                _clip_set(original_clip)
                post(lambda: self._done("Too long / not a prompt box", ERR_RED))
                return

            # 2. enhance
            print(f"[EnhanceButton] enhancing {len(raw)} chars in {t.key}")
            from app.services.skill_prompt_enhancer import enhance_prompt_text
            enhanced = enhance_prompt_text(raw)
            if not enhanced:
                raise RuntimeError("empty result")
            self.last_result = enhanced
            self.last_undo = (t.hwnd, raw)

            # 3. paste back (only if the same window is still in front)
            if user32.GetForegroundWindow() != t.hwnd:
                _clip_set(enhanced.replace("\n", "\r\n"))
                post(lambda: self._done("✓ Copied – press Ctrl+V", OK_GREEN, 4000))
                return
            self._paste_into(t.hwnd, enhanced, "✓ Enhanced", original_clip)
        except Exception as e:
            print(f"[EnhanceButton] enhance failed: {e}")
            _clip_set(original_clip)
            post(lambda: self._done("✗ Enhance failed", ERR_RED, 3500))

    def _paste_into(self, hwnd, text, ok_label, restore_clip=Ellipsis):
        post = self.ui_q.put
        try:
            if restore_clip is Ellipsis:
                restore_clip = _clip_get()
            if not _focus(hwnd):
                _clip_set(text.replace("\n", "\r\n"))
                post(lambda: self._done("✓ Copied – press Ctrl+V", OK_GREEN, 4000))
                return
            _clip_set(text.replace("\n", "\r\n"))
            _ctrl(ord("A"))
            time.sleep(0.06)
            _ctrl(ord("V"))
            time.sleep(0.4)                     # let the app read the clipboard
            landed = _box_contains(text)
            if landed is False:
                # paste swallowed (app-specific paste handler): set the value directly
                print("[EnhanceButton] paste not visible in the box - trying SetValue")
                landed = _box_set_value(text)
            if landed is False:
                _clip_set(text.replace("\n", "\r\n"))
                post(lambda: self._done("✓ Copied – press Ctrl+V", OK_GREEN, 4000))
                return
            _clip_set(restore_clip)
            post(lambda: self._done(ok_label, OK_GREEN))
        except Exception as e:
            print(f"[EnhanceButton] paste failed: {e}")
            post(lambda: self._done("✗ Paste failed", ERR_RED, 3500))

    # ── Run ──────────────────────────────────────────────────────────────────
    def run(self):
        self.build()
        threading.Thread(target=self._watch_loop, daemon=True).start()
        # warm the Groq/enhancer import so the first click is quick
        threading.Thread(target=lambda: __import__("app.services.skill_prompt_enhancer"),
                         daemon=True).start()
        self.root.after(150, self._tick)
        print(f"[EnhanceButton] running (scope={SCOPE}, parent={self.parent_pid}).")
        self.root.mainloop()


# ── Single instance ──────────────────────────────────────────────────────────
def _acquire_single_instance(wait_s=8.0):
    """Named mutex so backend restarts / --reload / login autostart never stack
    two buttons. Waits a little in case the previous instance is shutting down."""
    deadline = time.time() + wait_s
    while True:
        handle = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\JarvisPromptEnhancerButton")
        if ctypes.windll.kernel32.GetLastError() != 183:   # ERROR_ALREADY_EXISTS
            return handle
        ctypes.windll.kernel32.CloseHandle(handle)
        if time.time() > deadline:
            return None
        time.sleep(0.5)


# ── Windows-login autostart (Startup-folder shortcut, no console window) ─────
def _startup_shortcut() -> Path:
    return Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Startup/Jarvis Prompt Enhancer.lnk"


def install_autostart() -> str:
    import win32com.client
    exe = Path(sys.executable)
    pythonw = exe.with_name("pythonw.exe")
    sc = win32com.client.Dispatch("WScript.Shell").CreateShortCut(str(_startup_shortcut()))
    sc.TargetPath = str(pythonw if pythonw.exists() else exe)
    sc.Arguments = "-m app.services.prompt_enhancer_button"
    sc.WorkingDirectory = str(REPO_ROOT)
    sc.Description = "Jarvis floating prompt-enhance button"
    sc.save()
    return str(_startup_shortcut())


def uninstall_autostart() -> bool:
    p = _startup_shortcut()
    if p.exists():
        p.unlink()
        return True
    return False


def _setup_logging():
    """Send prints to app/memory/enhancer_button.log (pythonw / DEVNULL have no console)."""
    try:
        if LOG_FILE.exists() and LOG_FILE.stat().st_size > 512_000:
            LOG_FILE.unlink()
        f = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stderr = f
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} pid={os.getpid()} ---")
    except Exception:
        pass


def main():
    if "--install-autostart" in sys.argv:
        print("Autostart installed:", install_autostart())
        return
    if "--uninstall-autostart" in sys.argv:
        print("Autostart removed." if uninstall_autostart() else "Autostart was not installed.")
        return
    parent_pid = None
    if "--parent-pid" in sys.argv:
        try:
            parent_pid = int(sys.argv[sys.argv.index("--parent-pid") + 1])
        except Exception:
            parent_pid = None
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    mutex = _acquire_single_instance()
    if not mutex:
        print("[EnhanceButton] already running - exiting.")
        return
    _setup_logging()
    _set_dpi_aware()
    try:
        EnhanceButton(parent_pid).run()
    except Exception as e:
        print(f"[EnhanceButton] crashed: {e!r}")
        raise


if __name__ == "__main__":
    main()
