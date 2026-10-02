"""
youtube_player.py — low-level bridge to the YouTube player in the user's browser
================================================================================
Helper module for youtube_control.py (not a tool itself, like window_layout.py).

Precise control ("speed 2x", "go to 5:30", "forward 10 minutes", "skip this part")
needs the page's own player API (#movie_player: seekTo, setPlaybackRate, getVideoData…).
We reach it without extensions or debug ports:

    focus the YouTube browser window → Ctrl+L → check (UIA) the address bar really has
    focus → type "javascript:" (browsers strip it when pasted) → paste a one-line script →
    Enter. The script runs in the page, writes its JSON result into document.title as
    __JV<nonce>__{...}__JE__, and restores the title 400 ms later. We read the result from
    the window title with GetWindowTextW.

Gotchas (verified on Edge 2026-09-28):
  - In HTML fullscreen the address bar is hidden and Ctrl+L leaves focus in the page, where
    typed letters are YouTube shortcuts (j/c/i/t…). So: detect fullscreen (window rect ==
    monitor rect), press Esc first, run, and let the script click the fullscreen button again.
  - The script is a URL: never put '%' or '#' in it (percent-decoding / fragment). Strings
    from the user go through _js_str(), which escapes both.
  - Firefox blocks javascript: in the URL bar → keyboard-shortcut fallback (fewer features).
  - After the script runs, keyboard focus is back in the page, so shortcut keys still work.
"""

import re
import json
import time
import random
import ctypes
from ctypes import wintypes

import pyautogui
import pyperclip

BROWSERS = {"msedge.exe", "chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe"}
NO_TAB = "I don't see a YouTube tab in front, Sir. Switch to it (or ask me to open YouTube) and try again."

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32


# ── windows / focus ────────────────────────────────────────────────────────

def com_init():
    try:
        import comtypes
        comtypes.CoInitialize()
    except Exception:
        pass


def youtube_windows() -> list[tuple[int, str]]:
    """Visible browser windows whose active tab is YouTube → [(hwnd, title)], foreground first."""
    try:
        from app.services.window_layout import _enumerate_app_windows, _get_process_name
        fg = _user32.GetForegroundWindow()
        out = []
        for hwnd, title in _enumerate_app_windows(require_visible=True):
            # "__JV" = our script's result marker, still in the title for a moment after a call
            t = (title or "").lower()
            if ("youtube" in t or "__jv" in t) and _get_process_name(hwnd) in BROWSERS:
                out.append((hwnd, title))
        out.sort(key=lambda w: w[0] != fg)
        return out
    except Exception:
        return []


def window_title(hwnd: int) -> str:
    buf = ctypes.create_unicode_buffer(8192)
    _user32.GetWindowTextW(hwnd, buf, 8192)
    return buf.value


def _process_name(hwnd: int) -> str:
    try:
        from app.services.window_layout import _get_process_name
        return _get_process_name(hwnd) or ""
    except Exception:
        return ""


def focus(hwnd: int) -> bool:
    """Force a window to the foreground. AttachThreadInput first; if Windows' foreground
    lock still refuses (it did on a freshly opened window: "couldn't bring the YouTube
    window to the front"), tap Alt (keybd_event), which lets the next SetForegroundWindow
    through, and toggle TOPMOST as a last resort."""
    try:
        if _user32.IsIconic(hwnd):
            _user32.ShowWindow(hwnd, 9)
        for attempt in range(3):
            fg = _user32.GetForegroundWindow()
            if fg == hwnd:
                return True
            cur_tid = _kernel32.GetCurrentThreadId()
            fg_tid = _user32.GetWindowThreadProcessId(fg, None)
            _user32.AttachThreadInput(cur_tid, fg_tid, True)
            try:
                if attempt >= 1:
                    _user32.keybd_event(0x12, 0, 0, 0)        # Alt down
                    _user32.keybd_event(0x12, 0, 2, 0)        # Alt up
                if attempt == 2:
                    _user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)   # TOPMOST
                    _user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)   # NOTOPMOST
                _user32.ShowWindow(hwnd, 5)                   # SW_SHOW
                _user32.BringWindowToTop(hwnd)
                _user32.SetForegroundWindow(hwnd)
            finally:
                _user32.AttachThreadInput(cur_tid, fg_tid, False)
            time.sleep(0.25)
            if _user32.GetForegroundWindow() == hwnd:
                if attempt >= 1:
                    # the Alt tap may have put focus on the browser menu: send it back
                    time.sleep(0.05)
                    if _focused_is_toolbar() and not is_fullscreen(hwnd):
                        _user32.keybd_event(0x1B, 0, 0, 0)
                        _user32.keybd_event(0x1B, 0, 2, 0)
                return True
        return False
    except Exception:
        return False


def _in_page(el) -> bool | None:
    """Is a UIA element inside the web page (has a Document ancestor)?"""
    try:
        from app.services.uia_local import uia
        walker = uia().ControlViewWalker
        cur, depth = el, 0
        while cur is not None and depth < 40:
            ct = cur.CurrentControlType
            if ct == 50030:                       # Document = the web page
                return True
            if ct == 50032:                       # Window = reached the browser frame
                return False
            cur = walker.GetParentElement(cur)
            depth += 1
        return False
    except Exception:
        return None


def _focused_is_toolbar() -> bool:
    try:
        com_init()
        from app.services.uia_local import uia
        el = uia().GetFocusedElement()
        return el.CurrentControlType != 50004 and _in_page(el) is False
    except Exception:
        return False


class _MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]


def is_fullscreen(hwnd: int) -> bool:
    """HTML fullscreen: the window exactly covers its monitor (maximised windows don't)."""
    try:
        r = wintypes.RECT()
        _user32.GetWindowRect(hwnd, ctypes.byref(r))
        mi = _MONITORINFO()
        mi.cbSize = ctypes.sizeof(_MONITORINFO)
        _user32.GetMonitorInfoW(_user32.MonitorFromWindow(hwnd, 2), ctypes.byref(mi))
        m = mi.rcMonitor
        return (r.left, r.top, r.right, r.bottom) == (m.left, m.top, m.right, m.bottom)
    except Exception:
        return False


def _address_bar_focused():
    """True/False via UI Automation (focused element is an Edit); None if we can't tell."""
    try:
        com_init()
        from app.services.uia_local import uia
        el = uia().GetFocusedElement()
        return el.CurrentControlType == 50004  # UIA_EditControlTypeId
    except Exception:
        return None


def _focused_desc() -> str:
    try:
        com_init()
        from app.services.uia_local import uia
        el = uia().GetFocusedElement()
        return f"{el.CurrentControlType}:{(el.CurrentName or '')[:30]}"
    except Exception as e:
        return f"error {type(e).__name__}: {e}"


def _squash(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


def _page_focused():
    """True if keyboard focus is inside the web page (so YouTube shortcuts reach the player).
    None if UIA can't tell."""
    try:
        com_init()
        from app.services.uia_local import uia
        el = uia().GetFocusedElement()
        ct = el.CurrentControlType
        # Edit = address bar / text box, TabItem = tab strip, both swallow shortcut keys.
        # Anything else must be INSIDE the page (browser toolbar buttons don't count).
        if ct in (50004, 50019):
            return False
        if ct in (50030, 50033):           # the document itself / fullscreen video pane
            return True
        inside = _in_page(el)
        return True if inside is None else inside
    except Exception:
        return None


def _focus_page(hwnd: int) -> bool:
    """Move keyboard focus from the address bar / tab strip into the page.
    Edge/Chrome: Esc reverts the address bar, F6 cycles address bar → page → tab strip."""
    if _page_focused() is not False:
        return True
    if _user32.GetForegroundWindow() != hwnd:
        focus(hwnd)
    fs = is_fullscreen(hwnd)
    # Esc would EXIT fullscreen, so in fullscreen only ever move focus via UI Automation
    if not fs and _address_bar_focused():
        pyautogui.press("escape")              # revert anything half-typed in the address bar
    if _uia_focus(hwnd, "document"):
        return True
    if fs:
        return False
    if _address_bar_focused():
        pyautogui.press("escape")
        pyautogui.press("escape")
    for _ in range(3):
        pyautogui.press("f6")
        time.sleep(0.2)
        if _page_focused() is not False:
            return True
    return False


def _uia_focus(hwnd: int, what: str) -> bool:
    """Put keyboard focus straight on the address bar ('address') or the web page
    ('document') through UI Automation. Ctrl+L / F6 don't work when Edge's focus is stuck
    on an internal container (seen on freshly opened windows: focus on a 'View' pane)."""
    try:
        com_init()
        from app.services.uia_local import uia, element_from_handle, UIA_ControlTypePropertyId, TreeScope_Descendants
        win = element_from_handle(hwnd)
        if what == "address":
            cands = [e for e in win.descendants("Edit")
                     if "address" in e.window_text().lower() or e.el.CurrentClassName == "OmniboxViewViews"]
            target = cands[0].el if cands else None
        else:
            docs = win.el.FindAll(TreeScope_Descendants, uia().CreatePropertyCondition(UIA_ControlTypePropertyId, 50030))
            target = None
            for i in range(docs.Length):
                d = docs.GetElement(i)
                try:
                    if not d.CurrentIsOffscreen:
                        target = d
                        break
                except Exception:
                    target = d
                    break
        if target is None:
            return False
        target.SetFocus()
        time.sleep(0.12)
        return _address_bar_focused() is True if what == "address" else _page_focused() is not False
    except Exception:
        return False


def _focus_address_bar(hwnd: int) -> bool:
    """Ctrl+L until the address bar has focus (Edge sometimes needs a second try)."""
    if _user32.GetForegroundWindow() != hwnd:
        focus(hwnd)
    if _uia_focus(hwnd, "address"):
        return True
    for wait in (0.2, 0.4, 0.7, 1.0):
        if _user32.GetForegroundWindow() != hwnd:
            focus(hwnd)
        pyautogui.hotkey("ctrl", "l")
        time.sleep(wait)
        if _address_bar_focused() is not False:
            return True
    return False


# ── navigation / keys ──────────────────────────────────────────────────────

# Is YouTube muted (player now, or the saved preference the next page will load with)?
_MUTED_JS = ("var M=false;try{var sv=JSON.parse(JSON.parse(localStorage.getItem('yt-player-volume')).data);"
             "M=!!sv.muted||sv.volume===0;}catch(e){}"
             "var mp=document.getElementById('movie_player');if(mp&&mp.isMuted&&mp.isMuted()){M=true;}")


def navigate(url: str) -> str:
    """
    Load url in the front YouTube tab (switching videos / search pages), else a new tab.
    Uses the script bridge (verified + retried) with a delayed location.assign so the result
    marker is read before the page unloads. If the tab can't be reused, the video playing
    there is paused first, so two videos never play at once.
    """
    import webbrowser
    wins = youtube_windows()
    if wins:
        hwnd = wins[0][0]
        if _process_name(hwnd) != "firefox.exe":
            before = window_title(hwnd)
            for _ in range(2):
                res, err = run_js(_MUTED_JS + "setTimeout(function(){location.assign(" + _js_str(url) + ");},700);"
                                  "return {ok:1,muted:M};", 3.0)
                if err is None:
                    return "same-tab-muted" if isinstance(res, dict) and res.get("muted") else "same-tab"
                if err in ("notab", "focus"):
                    break
                if err == "timeout":
                    # the script may have run and the page already be leaving: check the title
                    end = time.time() + 2.5
                    while time.time() < end:
                        t = window_title(hwnd)
                        if t and t != before and "__JV" not in t:
                            return "same-tab"
                        time.sleep(0.1)
                    break
                time.sleep(0.5)
        if focus(hwnd):
            if is_fullscreen(hwnd):
                pyautogui.press("escape")
                time.sleep(0.6)
            old = _clip_get()
            try:
                if _focus_address_bar(hwnd) and _clip_set(url):
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.hotkey("ctrl", "v")
                    val, end = None, time.time() + 1.0
                    while time.time() < end:
                        time.sleep(0.06)
                        val = _address_bar_value()
                        if val is None or _squash(val) == _squash(url):
                            break
                    if _user32.GetForegroundWindow() == hwnd and (val is None or _squash(val) == _squash(url)):
                        pyautogui.press("enter")
                        return "same-tab"
                    print(f"[youtube_player] navigate: URL not in address bar (value={str(val)[:50]!r})")
                    _focus_page(hwnd)
            finally:
                _clip_restore(old)
        pause_quietly()
    webbrowser.open(url)
    return "new-tab-muted"


def pause_quietly() -> bool:
    """Pause the front YouTube video if one is playing (no reply text)."""
    try:
        res, err = run_js(_PRE + "if(!v.paused){if(A){A.pauseVideo();}else{v.pause();}}return {ok:1};", 3.0)
        return err is None
    except Exception:
        return False


def send_keys(*keys) -> str | None:
    """Focus the YouTube tab and send shortcut keys. Returns an error string or None."""
    wins = youtube_windows()
    if not wins:
        return NO_TAB
    hwnd = wins[0][0]
    if not focus(hwnd):
        return "I couldn't bring the YouTube window to the front, Sir."
    time.sleep(0.1)
    # Single keys (k, f, m, <, >…) would be typed into the address bar if it has focus
    # (that's how "<<<<>>>>" once ended up there). Hotkeys like Ctrl+W work anywhere.
    if any(not isinstance(k, tuple) or k[0] == "shift" for k in keys) and not _focus_page(hwnd):
        return "I couldn't get keyboard focus onto the video, Sir. Click on it once and try again."
    for k in keys:
        if isinstance(k, tuple):
            pyautogui.hotkey(*k)
        else:
            pyautogui.press(k)
        time.sleep(0.03)
    return None


def _address_bar_value():
    """Text currently in the focused address bar (UIA ValuePattern); None if unreadable."""
    try:
        com_init()
        from app.services.uia_local import uia
        import comtypes.gen.UIAutomationClient as UIA
        el = uia().GetFocusedElement()
        if el.CurrentControlType != 50004:
            return ""
        pat = el.GetCurrentPattern(10002).QueryInterface(UIA.IUIAutomationValuePattern)
        return pat.CurrentValue or ""
    except Exception:
        return None


def _clip_set(text: str) -> bool:
    """Copy to clipboard and verify (another app can hold the clipboard open)."""
    for _ in range(4):
        try:
            pyperclip.copy(text)
            if pyperclip.paste() == text:
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


def _clip_get():
    try:
        return pyperclip.paste()
    except Exception:
        return None


def _clip_restore(old):
    if old is None:
        return
    time.sleep(0.15)
    try:
        pyperclip.copy(old)
    except Exception:
        pass


# ── javascript bridge ──────────────────────────────────────────────────────

def _js_str(s) -> str:
    """JSON-encode a value for embedding in the javascript: URL (no raw % or #)."""
    return json.dumps(s, ensure_ascii=True).replace("%", "\\u0025").replace("#", "\\u0023")


# Prelude shared by every player script. One line, every statement ends with ';'.
_PRE = (
    "if(location.pathname.indexOf('/watch')!==0&&location.pathname.indexOf('/shorts/')!==0)"
    "{return {err:'notwatch'};}"
    "var p=document.getElementById('movie_player');"
    "if(location.pathname.indexOf('/shorts/')===0){p=document.getElementById('shorts-player')||p;}"
    "var v=(p&&p.querySelector('video'))||document.querySelector('video');"
    "if(!v){return {err:'novideo'};}"
    "var A=(p&&p.getPlayerState)?p:null;"
    "var T=function(){return A?A.getCurrentTime():v.currentTime;};"
    "var D=function(){var d=A?A.getDuration():v.duration;return d||v.duration||0;};"
    "var SK=function(t){var d=D();t=Math.max(0,d?Math.min(t,d-1):t);"
    "if(A){A.seekTo(t,true);}else{v.currentTime=t;}return t;};"
    "var VD=function(){try{return A.getVideoData()||{};}catch(e){return {};}};"
    "var CH=function(){var s={},o=[];"
    "document.querySelectorAll('ytd-macro-markers-list-item-renderer').forEach(function(e){"
    "var tm=e.querySelector('[id=time]'),ti=e.querySelector('h3,h4');if(!tm){return;}"
    "var k=tm.textContent.trim();if(!k||s[k]){return;}s[k]=1;var x=0;"
    "k.split(':').forEach(function(n){x=x*60+Number(n);});"
    "o.push({t:x,n:ti?ti.textContent.trim():''});});"
    "o.sort(function(a,b){return a.t-b.t;});return o;};"
    "var BTN=function(sel){var b=document.querySelector(sel);return (b&&b.offsetParent!==null)?b:null;};"
    "var ST=function(){var d=VD();return {t:T(),d:D(),r:v.playbackRate,"
    "vol:A?A.getVolume():Math.round(v.volume*100),m:A?A.isMuted():v.muted,paused:v.paused,"
    "loop:v.loop,title:d.title||document.title,author:d.author||'',live:!!d.isLive,"
    "ad:!!document.querySelector('.ad-showing')};};"
)


def run_js(body: str, timeout: float = 3.0, restore_ms: int = 1500):
    """
    Run `body` (a JS function body that returns a JSON-able value) inside the YouTube page.
    Returns (result, None) or (None, error_code) where error_code is 'notab', 'focus',
    'noaddressbar', 'firefox' or 'timeout'.
    """
    wins = youtube_windows()
    if not wins:
        return None, "notab"
    hwnd = wins[0][0]
    if _process_name(hwnd) == "firefox.exe":
        return None, "firefox"
    if not focus(hwnd):
        return None, "focus"

    was_fs = is_fullscreen(hwnd)
    if was_fs:
        pyautogui.press("escape")
        time.sleep(0.8)
        if is_fullscreen(hwnd):
            # Still covering the monitor after Esc → browser fullscreen (F11), not the video's:
            # don't "restore" by clicking YouTube's fullscreen button afterwards.
            was_fs = False

    nonce = str(random.randint(100000, 999999))
    refs = ""   # fullscreen is restored from Python with the 'f' key (see restore_fs below)
    # Edge/Chrome update the window title lazily (measured: a 150 ms marker was missed 6/6,
    # 550 ms 1/8), so the marker stays up for restore_ms.
    # If a previous call's marker is still up, reuse its saved original title and cancel
    # its restore timer, so back-to-back commands never clobber each other.
    # The restore only runs if the page did NOT navigate meanwhile (YouTube sets the new
    # video's title itself; restoring the old one showed "Believer" while "Hanuman Ansh" played).
    code = ("(function(){var W=window;clearTimeout(W.__jvT);var H=location.href;"
            "var o=(document.title.indexOf('__JV')===0&&W.__jvO)?W.__jvO:document.title;W.__jvO=o;var R;"
            "try{R=(function(){" + body + "})();}catch(e){R={err:String(e)};}"
            "document.title='__JV" + nonce + "__'+JSON.stringify(R)+'__JE__';"
            "W.__jvT=setTimeout(function(){if(document.title.indexOf('__JV')===0){"
            "if(location.href===H){document.title=o;}else{document.title='YouTube';}}},"
            + str(int(restore_ms)) + ");" + refs + "})()")

    def _abort(reason: str):
        """Nothing ran: revert the address bar, give focus back to the page, restore fullscreen."""
        print(f"[youtube_player] {reason}")
        _focus_page(hwnd)
        if was_fs and _page_focused():
            pyautogui.press("f")
        return None, "noaddressbar"

    want = _squash("javascript:" + code)
    old = _clip_get()
    try:
        if not _focus_address_bar(hwnd):
            return _abort(f"address bar never got focus (focused={_focused_desc()})")
        # Never press Enter unless the address bar holds exactly our script: a failed or slow
        # paste (clipboard busy, user typing) would otherwise search "javascript:" and leave
        # the video. Edge fills the box asynchronously, so poll for the complete text.
        typed, val = False, None
        for attempt in range(2):
            if attempt:
                pyautogui.press("escape")
                if not _focus_address_bar(hwnd):
                    break
            if not _clip_set(code):
                continue
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite("javascript:", interval=0.004)
            pyautogui.hotkey("ctrl", "v")
            end = time.time() + 1.2
            while time.time() < end:
                time.sleep(0.06)
                val = _address_bar_value()
                if val is None or _squash(val) == want:
                    break
            if _user32.GetForegroundWindow() == hwnd and (val is None or _squash(val) == want):
                typed = True
                break
        if not typed:
            return _abort(f"script not in address bar (value={str(val)[:50]!r}, "
                          f"foreground_ok={_user32.GetForegroundWindow() == hwnd})")
        pyautogui.press("enter")

        if was_fs:
            # Put the video back in fullscreen with YouTube's own 'f' key (a real keypress is a
            # user gesture the browser always honours). One method only: a script click plus a
            # fallback key raced each other and toggled fullscreen back off.
            def _restore_fs():
                for _ in range(2):
                    if is_fullscreen(hwnd):
                        return
                    if not _focus_page(hwnd):
                        print("[youtube_player] fullscreen restore: page focus failed")
                        return
                    pyautogui.press("f")
                    end = time.time() + 2.5
                    while time.time() < end:
                        if is_fullscreen(hwnd):
                            return
                        time.sleep(0.15)
                print("[youtube_player] fullscreen restore failed")
            restore_fs = _restore_fs
        else:
            restore_fs = None
        marker = re.compile(r"__JV" + nonce + r"__(.*)__JE__", re.S)
        end = time.time() + timeout
        while time.time() < end:
            m = marker.search(window_title(hwnd))
            if m:
                if restore_fs:
                    restore_fs()
                try:
                    return json.loads(m.group(1)), None
                except Exception:
                    return None, "timeout"
            time.sleep(0.05)
        print(f"[youtube_player] no result marker within {timeout}s (title={window_title(hwnd)[:60]!r})")
        if restore_fs:
            restore_fs()
        return None, "timeout"
    finally:
        _clip_restore(old)


# ── formatting helpers ─────────────────────────────────────────────────────

def fmt_time(sec) -> str:
    try:
        sec = int(round(float(sec)))
    except Exception:
        return "?"
    h, rem = divmod(max(sec, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_span(sec) -> str:
    """10 → '10 seconds', 600 → '10 minutes', 90 → '1 minute 30 seconds'."""
    sec = int(round(abs(float(sec))))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if h:
        parts.append(f"{h} hour" + ("s" if h != 1 else ""))
    if m:
        parts.append(f"{m} minute" + ("s" if m != 1 else ""))
    if s or not parts:
        parts.append(f"{s} second" + ("s" if s != 1 else ""))
    return " ".join(parts)


def _rate(r) -> str:
    try:
        r = float(r)
        return (f"{r:.2f}".rstrip("0").rstrip(".")) + "x"
    except Exception:
        return "?"


def _pos(st: dict) -> str:
    if st.get("live"):
        return "live"
    return f"{fmt_time(st.get('t', 0))} of {fmt_time(st.get('d', 0))}"


# ── spoken number / time parsing ───────────────────────────────────────────

_WORDNUM = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "ninety": 90, "half": 0.5, "half a": 0.5, "couple": 2,
    "a couple of": 2, "few": 3, "a few": 3,
}
_NUM = r"(\d+(?:\.\d+)?|a couple of|a few|half a|couple|few|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|ninety|half)"
_UNIT = r"(hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)\b"


def _num(tok: str) -> float:
    tok = tok.strip().lower()
    try:
        return float(tok)
    except ValueError:
        return float(_WORDNUM.get(tok, 0))


def parse_duration(text: str):
    """'10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90. None if absent."""
    total, found = 0.0, False
    for m in re.finditer(_NUM + r"\s*" + _UNIT, text.lower()):
        n, unit = _num(m.group(1)), m.group(2)
        mult = 3600 if unit.startswith("h") else 60 if unit.startswith("m") else 1
        total += n * mult
        found = True
    return total if found else None


def parse_clock(text: str):
    """'5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent."""
    m = re.search(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\b", text)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), m.group(3)
        return a * 3600 + b * 60 + int(c) if c is not None else a * 60 + b
    m = re.search(r"\b(?:to|at|from)\s+(\d{1,2})\s+(\d{2})\b(?!\s*(?:seconds?|secs?|minutes?|mins?|percent))", text)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None


# ── player actions ─────────────────────────────────────────────────────────

_ERR = {
    "notab": NO_TAB,
    "focus": "I couldn't bring the YouTube window to the front, Sir.",
    "notwatch": "No video is open on that YouTube tab yet, Sir. Pick one first.",
    "novideo": "I can't find the video player on that page, Sir.",
}

# Keyboard fallbacks (YouTube shortcuts) for when the script bridge can't run.
_KEY_FALLBACK = {
    "pause": ["k"], "play": ["k"], "toggle": ["k"], "mute": ["m"], "unmute": ["m"],
    "captions": ["c"], "fullscreen": ["f"], "theater": ["t"], "miniplayer": ["i"],
    "faster": [("shift", ".")], "slower": [("shift", ",")], "next": [("shift", "n")],
    "previous": [("alt", "left")], "skip_part": [("ctrl", "right")],
    "chapter_next": [("ctrl", "right")], "chapter_prev": [("ctrl", "left")],
}


def _fallback(action: str, amount: float, value: str, reason: str) -> str:
    """Keyboard-only version of an action. Only used for Firefox (which blocks the script
    bridge); in Edge/Chrome a failed script means something interfered, so say so instead
    of blindly pressing keys."""
    if reason in ("notab", "focus", "notwatch", "novideo"):
        return _ERR[reason]
    if reason != "firefox":
        return "I couldn't reach the YouTube player just then, Sir. Please say that again."
    keys = None
    msg = "Done with the keyboard shortcut, Sir."
    if action in ("forward", "rewind"):
        n = max(1, min(360, round((amount or 10) / 10)))
        keys = ["l" if action == "forward" else "j"] * n
        msg = f"{'Forward' if action == 'forward' else 'Back'} {fmt_span(n * 10)}, Sir."
    elif action == "seek_pct":
        pct = max(0, min(90, int(float(value or 0)) // 10 * 10))
        keys = [str(pct // 10)]
        msg = f"Jumped to {pct} percent, Sir."
    elif action == "seek_to" and float(amount or 0) == 0:
        keys = ["0"]
        msg = "Back to the start, Sir."
    elif action == "speed":
        r = max(0.25, min(2.0, float(value or 1)))
        keys = [("shift", ",")] * 7 + [("shift", ".")] * int(round((r - 0.25) / 0.25))
        msg = f"Speed set to {_rate(r)} with keyboard shortcuts, Sir."
    elif action in _KEY_FALLBACK:
        keys = _KEY_FALLBACK[action]
    if keys is None:
        why = ("Firefox doesn't let me reach the player directly"
               if reason == "firefox" else "I couldn't reach the player directly")
        return f"{why}, Sir, so I can't do that one. It works in Edge or Chrome."
    err = send_keys(*keys)
    return err or msg


def _js(body: str, timeout: float = 3.0):
    res, err = run_js(_PRE + body, timeout)
    if err == "noaddressbar":          # nothing ran (aborted before Enter) → safe to retry once
        time.sleep(0.4)
        res, err = run_js(_PRE + body, timeout)
    if err is None and isinstance(res, dict) and res.get("err") in _ERR:
        return None, res["err"]
    if err is None and isinstance(res, dict) and res.get("err"):
        return None, "script:" + str(res["err"])
    return res, err


# Videos rendered on the current page, in on-screen order. Skips ads, Shorts shelves and
# elements of hidden (cached) pages. No '#' or '%' allowed in here (it becomes a URL).
_PAGE_VIDEOS_JS = (
    "var out=[],seen={};"
    "var sels='ytd-video-renderer, ytd-rich-item-renderer, ytd-grid-video-renderer, ytd-compact-video-renderer, "
    "yt-lockup-view-model, ytd-playlist-video-renderer, ytd-playlist-panel-video-renderer';"
    "document.querySelectorAll(sels).forEach(function(el){"
    "if(el.closest('ytd-ad-slot-renderer, ytd-in-feed-ad-layout-renderer, ytd-reel-shelf-renderer, ytd-rich-shelf-renderer, "
    "ytm-shorts-lockup-view-model, ytd-promoted-sparkles-web-renderer')){return;}"
    "if(el.parentElement&&el.parentElement.closest(sels)){return;}"
    "var a=el.querySelector('a[href*=\"/watch?v=\"]');if(!a){return;}"
    "var h=a.getAttribute('href');var id=h.split('v=')[1];if(!id){return;}id=id.slice(0,11);if(seen[id]){return;}"
    "var r=el.getBoundingClientRect();if(r.width<40||r.height<20){return;}"
    "seen[id]=1;"
    "var t=el.querySelector('[id=video-title], a[title], h3');"
    "var title=t?((t.getAttribute('title')||t.textContent||'').trim()):'';"
    "var ch=el.querySelector('ytd-channel-name a, [id=channel-name] a, .yt-content-metadata-view-model-wiz__metadata-text a, "
    ".yt-content-metadata-view-model__metadata-text a');"
    "var du=el.querySelector('ytd-thumbnail-overlay-time-status-renderer, .badge-shape-wiz__text, .yt-badge-shape__text, "
    "badge-shape');"
    "out.push({id:id,title:title.slice(0,70),channel:ch?ch.textContent.trim().slice(0,30):'',"
    "duration:du?du.textContent.trim():'',y:Math.round(r.top+window.scrollY),x:Math.round(r.left)});});"
    "out.sort(function(p,q){return (Math.abs(p.y-q.y)<30)?(p.x-q.x):(p.y-q.y);});"
    "out=out.slice(0,20).map(function(o){return {id:o.id,title:o.title,channel:o.channel,duration:o.duration.slice(0,9)};});"
    "return {path:location.pathname,search:location.search.slice(0,120),list:out};"
)


def page_videos():
    """
    Read the videos actually shown in the front YouTube tab (what the user sees, including
    YouTube's personalised order). Returns {'path', 'search', 'list': [{id,title,channel,
    duration}]} or None if the page can't be read.
    """
    try:
        com_init()
        res, err = run_js(_PAGE_VIDEOS_JS, 3.5)
        if err in ("noaddressbar", "timeout"):   # read-only, so a retry is safe (page may be loading)
            time.sleep(0.8)
            res, err = run_js(_PAGE_VIDEOS_JS, 4.0)
        if err or not isinstance(res, dict) or res.get("err"):
            return None
        for v in res.get("list") or []:
            for k in ("title", "channel", "duration"):
                v[k] = re.sub(r"\s+", " ", v.get(k) or "").strip()
        return res
    except Exception:
        return None


def open_video(video_id: str) -> bool:
    """Open a video in the front YouTube tab the way a click would (SPA navigation)."""
    vid = re.sub(r"[^A-Za-z0-9_-]", "", video_id or "")[:11]
    if not vid:
        return False
    # The user asked to PLAY it, so make it audible: YouTube keeps a saved "muted" flag.
    # Timers keep running across YouTube's in-page (SPA) navigation after the click.
    unmute = ("var U=function(){var p=document.getElementById('movie_player');"
              "if(p&&p.isMuted&&p.isMuted()){p.unMute();if(p.getVolume()<10){p.setVolume(50);}}};"
              "setTimeout(U,1800);setTimeout(U,3100);setTimeout(U,5100);")
    res, err = run_js(unmute + _MUTED_JS + "var a=document.querySelector('a[href*=\"v=" + vid + "\"]');"
                      "if(a&&a.getBoundingClientRect().width>0){setTimeout(function(){a.click();},600);return {clicked:1};}"
                      "location.assign('/watch?v=" + vid + "');return {assigned:1,muted:M};", 3.0)
    if err == "noaddressbar":
        time.sleep(0.4)
        res, err = run_js("location.assign('/watch?v=" + vid + "');return {assigned:1};", 3.0)
    if err is None and isinstance(res, dict) and res.get("assigned") and res.get("muted"):
        ensure_audible(delay=2.5)            # full page load: timers above were lost
    return err is None


def ensure_audible(delay: float = 0.0) -> bool:
    """Unmute the player (keeps the volume level; raises it only if it's ~0)."""
    if delay:
        time.sleep(delay)
    for _ in range(2):
        res, err = run_js(_PRE + "if(A){if(A.isMuted()){A.unMute();}if(A.getVolume()<10){A.setVolume(50);}}"
                                 "else{v.muted=false;}return {ok:1};", 3.0)
        if err is None and isinstance(res, dict) and not res.get("err"):
            return True
        time.sleep(1.0)
    return False


def current_video_info() -> dict | None:
    """{title, author, t, d, ...} of the video in the front YouTube tab, or None."""
    try:
        com_init()
        st, err = _js("return ST();")
        return st if not err else None
    except Exception:
        return None


def player_action(action: str, amount: float = 0, value: str = "") -> str:
    """
    Precise YouTube player control. Returns a human-readable reply.

    action / amount (seconds) / value:
      status | pause | play | toggle
      forward, rewind (amount s) | seek_to (amount s) | seek_pct (value 0-100) | seek_end
      speed (value e.g. "2", "1.5", "normal") | faster | slower (amount = step, default 0.25)
      volume (value 0-100) | volume_up | volume_down (amount step) | mute | unmute
      captions (value on/off/toggle) | loop (value on/off) | quality (value "1080", "max", "min")
      skip_part | chapter_next | chapter_prev | chapter_goto (value number/name) | chapters
      skip_ad | like | dislike | subscribe | theater | miniplayer | pip | fullscreen | exit_fullscreen
      next | previous
    """
    try:
        com_init()
        a = (action or "").lower().strip().replace(" ", "_").replace("-", "_")
        try:
            amount = float(amount or 0)
        except Exception:
            amount = 0.0
        value = "" if value is None else str(value).strip().lower()

        # ── fullscreen is pure keyboard (the script path itself leaves fullscreen) ──
        if a in ("fullscreen", "full_screen", "exit_fullscreen", "exit_full_screen"):
            wins = youtube_windows()
            if not wins:
                return NO_TAB
            fs = is_fullscreen(wins[0][0])
            want = not a.startswith("exit")
            if fs == want:
                return "It's already full screen, Sir." if want else "It's not in full screen, Sir."
            hwnd = wins[0][0]

            def _now_fs(expect: bool) -> bool:
                end = time.time() + 2.0
                while time.time() < end:
                    if is_fullscreen(hwnd) == expect:
                        return True
                    time.sleep(0.2)
                return False

            if want:
                # 1) YouTube's own fullscreen button via the page; 2) the 'f' key
                res, err = _js("var b=document.querySelector('.ytp-fullscreen-button');"
                               "if(b){b.click();}return {ok:!!b};")
                if not err and _now_fs(True):
                    return "Full screen, Sir."
                err2 = send_keys("f")
                if not err2 and _now_fs(True):
                    return "Full screen, Sir."
                return err2 or "I couldn't switch the video to full screen, Sir. Please try again."
            err = send_keys("escape")
            if not err and _now_fs(False):
                return "Exited full screen, Sir."
            err2 = send_keys("f")
            if not err2 and _now_fs(False):
                return "Exited full screen, Sir."
            return err or err2 or "I couldn't leave full screen, Sir."

        if a == "status":
            st, err = _js("return ST();")
            if err:
                return _fallback(a, amount, value, err)
            left = "" if st.get("live") else f" ({fmt_time(max(st['d'] - st['t'], 0))} left)"
            who = f" by {st['author']}" if st.get("author") else ""
            state = "paused" if st.get("paused") else "playing"
            vol = "muted" if st.get("m") else f"volume {st.get('vol')}"
            ad = " An ad is playing right now." if st.get("ad") else ""
            return (f"You're watching '{st.get('title')}'{who}, {state} at {_pos(st)}{left}, "
                    f"{_rate(st.get('r'))} speed, {vol}.{ad}")

        # ── Pause / play through the tab's Windows media session: exact (knows if it's
        #    already paused), works in fullscreen and when Edge isn't the front window.
        if a in ("pause", "play", "toggle", "resume"):
            wins = youtube_windows()
            if not wins:
                return NO_TAB
            hint = re.split(r" - YouTube", wins[0][1])[0]
            hint = re.sub(r"^\(\d+\)\s*", "", hint)
            r = {"ok": False}
            if is_fullscreen(wins[0][0]) or _user32.GetForegroundWindow() != wins[0][0]:
                try:
                    from app.services.media_sessions import control
                    r = control({"resume": "play"}.get(a, a), app="browser", title_hint=hint)
                except Exception:
                    r = {"ok": False, "reason": "error"}
            # Media-session status lags ~2 s in Edge, so only use this path where the script
            # path would cost more: fullscreen (no leaving it) or Edge not in front.
            if r.get("ok"):
                return "Paused, Sir." if a == "pause" else ("Playing, Sir." if a != "toggle" else "Done, Sir.")
            # no media session yet (video still loading / never played) → script path below

        # ── In video fullscreen use YouTube's own keys (no leaving fullscreen) ──
        wins_fs = youtube_windows()
        in_fs = bool(wins_fs) and is_fullscreen(wins_fs[0][0])
        if in_fs:
            keys, msg = None, None
            if a in ("forward", "rewind"):
                secs = amount or 10
                n10, rem = int(secs // 10), secs - int(secs // 10) * 10
                n5 = int(round(rem / 5.0))
                keys = (["l" if a == "forward" else "j"] * min(n10, 360)
                        + (["right" if a == "forward" else "left"] * n5))
                msg = f"{'Forward' if a == 'forward' else 'Back'} {fmt_span(secs)}, Sir."
            elif a == "seek_pct" and value and float(value) % 10 == 0 and float(value) < 100:
                keys, msg = [str(int(float(value)) // 10)], f"Jumped to {int(float(value))} percent, Sir."
            elif a == "restart" or (a == "seek_to" and not amount):
                keys, msg = ["0"], "Back to the start, Sir."
            elif a == "next":
                keys, msg = [("shift", "n")], "Playing the next video, Sir."
            elif a == "faster":
                keys, msg = [("shift", ".")] * max(1, int(round((amount or 0.25) / 0.25))), "Faster, Sir."
            elif a == "slower":
                keys, msg = [("shift", ",")] * max(1, int(round((amount or 0.25) / 0.25))), "Slower, Sir."
            elif a in ("captions", "subtitles") and value in ("", "toggle"):
                keys, msg = ["c"], "Toggled captions, Sir."
            if keys:
                err = send_keys(*keys)
                return err or msg

        if a in ("pause", "play", "toggle", "resume"):
            body = {
                "pause": "var ps=A?A.getPlayerState():(v.paused?2:1);var w=(ps===2||ps===0);"
                         "if(A){A.pauseVideo();}else{v.pause();}"
                         "if(ps===-1||ps===3||ps===5){var h=function(){v.pause();v.removeEventListener('playing',h);};"
                         "v.addEventListener('playing',h);}"
                         "var s=ST();s.was=w;s.paused=true;return s;",
                "play": "var w=v.paused;if(A){A.playVideo();}else{v.play();}var s=ST();s.was=w;s.paused=false;return s;",
                "resume": "var w=v.paused;if(A){A.playVideo();}else{v.play();}var s=ST();s.was=w;s.paused=false;return s;",
                "toggle": "var w=v.paused;if(w){if(A){A.playVideo();}else{v.play();}}else{if(A){A.pauseVideo();}else{v.pause();}}var s=ST();s.was=w;s.paused=!w;return s;",
            }[a]
            st, err = _js(body)
            if err:
                return _fallback(a, amount, value, err)
            if a == "pause":
                return "It's already paused, Sir." if st.get("was") else "Paused, Sir."
            if a in ("play", "resume") and not st.get("was"):
                return "It's already playing, Sir."
            return "Paused, Sir." if st.get("paused") else "Playing, Sir."

        if a in ("forward", "rewind"):
            secs = amount or 10
            delta = secs if a == "forward" else -secs
            st, err = _js(f"var o=T();var n=SK(o+({delta}));var s=ST();s.from=o;s.t=n;return s;")
            if err:
                return _fallback(a, secs, value, err)
            word = "Forward" if a == "forward" else "Back"
            return f"{word} {fmt_span(secs)}, Sir."

        if a in ("seek_to", "seek_pct", "seek_end", "restart"):
            if a == "seek_pct":
                pct = max(0.0, min(100.0, float(value or 0)))
                expr = f"D()*{pct / 100.0}"
            elif a == "seek_end":
                expr = "D()-(" + str(amount or 10) + ")"
            else:
                expr = str(0 if a == "restart" else amount)
            st, err = _js(f"var n=SK({expr});var s=ST();s.t=n;return s;")
            if err:
                return _fallback("seek_to" if a == "restart" else a, 0 if a == "restart" else amount, value, err)
            if a == "restart" or (a == "seek_to" and not amount):
                return "Back to the start, Sir."
            return f"Jumped to {fmt_time(st['t'])}, Sir."

        if a in ("speed", "faster", "slower", "normal_speed"):
            if a == "normal_speed" or value in ("normal", "default", "regular", "1x"):
                target = "1"
            elif a == "speed":
                try:
                    r = float(value.rstrip("x"))
                except Exception:
                    return f"I didn't catch the speed '{value}', Sir. Try 'speed 1.5x'."
                target = str(max(0.1, min(16.0, r)))
            else:
                step = amount or 0.25
                target = f"Math.max(0.25,Math.min(4,Math.round((v.playbackRate{'+' if a == 'faster' else '-'}{step})*4)/4))"
            st, err = _js(f"var R={target};if(A&&A.setPlaybackRate&&R>=0.25&&R<=2){{A.setPlaybackRate(R);}}"
                          f"v.playbackRate=R;var s=ST();s.r=R;return s;")
            if err:
                if a == "speed" or a == "normal_speed":
                    return _fallback("speed", 0, target if a == "speed" else "1", err)
                return _fallback(a, amount, value, err)
            return f"Speed {_rate(st['r'])}, Sir."

        if a in ("volume", "volume_up", "volume_down", "mute", "unmute"):
            if a == "volume":
                try:
                    n = int(max(0, min(100, float(value.rstrip("%")))))
                except Exception:
                    return f"I didn't catch the volume '{value}', Sir."
                body = f"var N={n};"
            elif a in ("volume_up", "volume_down"):
                step = int(amount or 10)
                sign = "+" if a == "volume_up" else "-"
                body = f"var N=Math.max(0,Math.min(100,(A?A.getVolume():Math.round(v.volume*100)){sign}{step}));"
            if a in ("mute", "unmute"):
                body = ("if(A){A." + ("mute" if a == "mute" else "unMute") + "();}else{v.muted="
                        + ("true" if a == "mute" else "false") + ";}var s=ST();s.m=" + ("true" if a == "mute" else "false") + ";return s;")
            else:
                body += "if(A){A.setVolume(N);if(N>0){A.unMute();}}else{v.volume=N/100;if(N>0){v.muted=false;}}var s=ST();s.vol=N;s.m=(N===0);return s;"
            st, err = _js(body)
            if err:
                return _fallback(a, amount, value, err)
            if a == "mute":
                return "Muted the video, Sir."
            if a == "unmute":
                return "Unmuted, Sir."
            return f"Volume {st.get('vol')}, Sir."

        if a in ("captions", "subtitles"):
            want = {"on": "true", "off": "false"}.get(value, "null")
            st, err = _js("var b=BTN('.ytp-subtitles-button');if(!b){return {nocc:1};}"
                          "var on=b.getAttribute('aria-pressed')==='true';var W=" + want + ";"
                          "if(W===null||W!==on){b.click();on=!on;}return {cc:on};")
            if err:
                return _fallback("captions", amount, value, err)
            if st.get("nocc"):
                return "This video doesn't have captions, Sir."
            return f"Captions {'on' if st.get('cc') else 'off'}, Sir."

        if a == "loop":
            want = "false" if value in ("off", "false", "no") else "true"
            st, err = _js(f"v.loop={want};return {{loop:v.loop}};")
            if err:
                return _fallback(a, amount, value, err)
            return "Looping this video, Sir." if st.get("loop") else "Loop turned off, Sir."

        if a == "quality":
            q = {"max": "highres", "best": "highres", "highest": "highres", "4k": "hd2160",
                 "2160": "hd2160", "1440": "hd1440", "1080": "hd1080", "hd": "hd720", "full hd": "hd1080",
                 "720": "hd720", "480": "large", "360": "medium", "240": "small", "144": "tiny",
                 "min": "tiny", "lowest": "tiny", "auto": "auto"}.get(value.rstrip("p"), "")
            if not q:
                return f"I didn't catch the quality '{value}', Sir. Try '1080p', 'max' or 'lowest'."
            st, err = _js("if(!A||!A.getAvailableQualityLevels){return {noq:1};}var L=A.getAvailableQualityLevels();"
                          f"var Q={_js_str(q)};if(Q==='highres'){{Q=L[0];}}if(Q==='tiny'){{Q=L[L.length-2]||L[0];}}"
                          "if(Q!=='auto'&&L.indexOf(Q)<0){return {levels:L,miss:Q};}"
                          "try{A.setPlaybackQualityRange(Q,Q);}catch(e){}try{A.setPlaybackQuality(Q);}catch(e){}"
                          "return {set:Q,levels:L};")
            if err:
                return _fallback(a, amount, value, err)
            names = {"hd2160": "4K", "hd1440": "1440p", "hd1080": "1080p", "hd720": "720p",
                     "large": "480p", "medium": "360p", "small": "240p", "tiny": "144p", "auto": "auto"}
            if st.get("noq"):
                return "I can't change the quality on this player, Sir."
            if st.get("miss"):
                have = ", ".join(names.get(l, l) for l in st.get("levels", []) if l != "auto")
                return f"This video doesn't offer {names.get(st['miss'], value)}, Sir. Available: {have}."
            return f"Quality set to {names.get(st.get('set'), st.get('set'))}, Sir."

        if a in ("skip_part", "chapter_next"):
            st, err = _js("var c=CH(),t=T(),n=null;for(var i=0;i<c.length;i++){if(c[i].t>t+1){n=c[i];break;}}"
                          "if(n){SK(n.t);var s=ST();s.ch=n;s.t=n.t;return s;}"
                          + ("var q=SK(t+30);var s2=ST();s2.nochap=c.length===0;s2.last=c.length>0;s2.t=q;return s2;"
                             if a == "skip_part" else "var s3=ST();s3.nochap=c.length===0;s3.last=c.length>0;return s3;"))
            if err:
                return _fallback(a, amount, value, err)
            if st.get("ch"):
                name = f" {st['ch']['n']}" if st["ch"].get("n") else ""
                return f"Skipped to{name or ' the next chapter'}, Sir."
            if a == "skip_part":
                why = "This video has no chapters" if st.get("nochap") else "You're in the last chapter"
                return f"{why}, so I skipped 30 seconds, Sir."
            return ("This video has no chapters, Sir." if st.get("nochap")
                    else "You're already in the last chapter, Sir.")

        if a == "chapter_prev":
            st, err = _js("var c=CH(),t=T(),i=-1;for(var k=0;k<c.length;k++){if(c[k].t<=t){i=k;}}"
                          "if(!c.length){return {nochap:1};}"
                          "var g=(i>0&&t-c[i].t<4)?c[i-1]:c[Math.max(i,0)];SK(g.t);var s=ST();s.ch=g;s.t=g.t;return s;")
            if err:
                return _fallback(a, amount, value, err)
            if st.get("nochap"):
                return "This video has no chapters, Sir."
            name = f" {st['ch']['n']}" if st["ch"].get("n") else ""
            return f"Back to{name or ' the previous chapter'}, Sir."

        if a in ("chapters", "chapter_goto", "current_chapter"):
            st, err = _js("var s=ST();s.chs=CH();return s;")
            if err:
                return _fallback(a, amount, value, err)
            chs = st.get("chs") or []
            if not chs:
                return "This video has no chapters, Sir."
            cur_i = max([i for i, c in enumerate(chs) if c["t"] <= st["t"]] or [0])
            if a == "chapters":
                lines = [f"{i + 1}. {c['n'] or 'Chapter'} ({fmt_time(c['t'])})" + ("  ← you're here" if i == cur_i else "")
                         for i, c in enumerate(chs[:15])]
                more = f"\n…and {len(chs) - 15} more." if len(chs) > 15 else ""
                return "Chapters, Sir:\n" + "\n".join(lines) + more + "\nSay 'go to chapter 3' or name one."
            if a == "current_chapter":
                c = chs[cur_i]
                return f"You're in chapter {cur_i + 1}, '{c['n']}', which started at {fmt_time(c['t'])}, Sir."
            # chapter_goto
            target = None
            words = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
                     "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10, "last": len(chs)}
            v = value.strip()
            if re.fullmatch(r"\d{1,3}", v):
                target = int(v)
            elif v in words:
                target = words[v]
            elif v in _WORDNUM and _WORDNUM[v] >= 1:
                target = int(_WORDNUM[v])
            if target is not None:
                if not 1 <= target <= len(chs):
                    return f"This video only has {len(chs)} chapters, Sir."
                c = chs[target - 1]
            else:
                import difflib
                scored = [(difflib.SequenceMatcher(None, v, c["n"].lower()).ratio()
                           + (0.5 if v and v in c["n"].lower() else 0), i) for i, c in enumerate(chs)]
                best = max(scored)
                if best[0] < 0.5:
                    return f"I couldn't find a chapter called '{value}', Sir. " + player_action("chapters")
                c = chs[best[1]]
            _, err = _js(f"SK({c['t']});return 1;")
            if err:
                return _fallback("seek_to", c["t"], "", err)
            return f"Jumped to {c['n'] or 'that chapter'}, Sir."

        if a == "skip_ad":
            st, err = _js("var b=document.querySelector('.ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern');"
                          "var ad=!!document.querySelector('.ad-showing');if(b&&b.offsetParent!==null){b.click();return {skipped:1};}"
                          "return {ad:ad};")
            if err:
                return _fallback(a, amount, value, err)
            if st.get("skipped"):
                return "Skipped the ad, Sir."
            return ("The ad can't be skipped yet, Sir. Ask me again in a few seconds."
                    if st.get("ad") else "There's no ad playing, Sir.")

        if a in ("like", "dislike", "unlike"):
            sel = ("dislike-button-view-model button, [id=segmented-dislike-button] button" if a == "dislike"
                   else "like-button-view-model button, [id=segmented-like-button] button")
            want = "false" if a == "unlike" else "true"
            st, err = _js("if(!document.querySelector('[id=avatar-btn]')){return {signin:1};}"
                          f"var b=document.querySelector({_js_str(sel)});if(!b){{return {{nobtn:1}};}}"
                          f"var on=b.getAttribute('aria-pressed')==='true';if(on!=={want}){{b.click();}}"
                          f"return {{was:on}};")
            if err:
                return _fallback(a, amount, value, err)
            if st.get("signin"):
                return "You need to be signed in to YouTube in this browser for that, Sir."
            if st.get("nobtn"):
                return f"I couldn't find the {a} button, Sir."
            if a == "unlike":
                return "Removed your like, Sir." if st.get("was") else "You hadn't liked it, Sir."
            if st.get("was"):
                return f"You've already {a}d this video, Sir."
            return f"{'Liked' if a == 'like' else 'Disliked'} the video, Sir."

        if a == "subscribe":
            st, err = _js("if(!document.querySelector('[id=avatar-btn]')){return {signin:1};}"
                          "var b=document.querySelector('ytd-watch-metadata [id=subscribe-button] button, [id=subscribe-button] button');"
                          "if(!b){return {nobtn:1};}var txt=(b.innerText||b.getAttribute('aria-label')||'').trim();"
                          "if(/^subscribed/i.test(txt)){return {already:1};}b.click();return {ok:1,author:VD().author||''};")
            if err:
                return _fallback(a, amount, value, err)
            if st.get("signin"):
                return "You need to be signed in to YouTube in this browser to subscribe, Sir."
            if st.get("nobtn"):
                return "I couldn't find the subscribe button, Sir."
            if st.get("already"):
                return "You're already subscribed, Sir."
            return f"Subscribed to {st.get('author') or 'the channel'}, Sir."

        if a in ("theater", "miniplayer"):
            sel = ".ytp-size-button" if a == "theater" else ".ytp-miniplayer-button"
            st, err = _js(f"var b=BTN({_js_str(sel)});if(!b){{return {{nobtn:1}};}}b.click();return {{ok:1}};")
            if err:
                return _fallback(a, amount, value, err)
            if st.get("nobtn"):
                return f"That button isn't available on this page, Sir."
            return "Toggled theater mode, Sir." if a == "theater" else "Switched to the mini player, Sir."

        if a == "pip":
            st, err = _js("if(document.pictureInPictureElement){document.exitPictureInPicture();return {off:1};}"
                          "v.requestPictureInPicture();return {on:1};")
            if err:
                return _fallback(a, amount, value, err)
            return "Picture-in-picture off, Sir." if st.get("off") else "Picture-in-picture on, Sir."

        if a in ("next", "previous"):
            wins = youtube_windows()
            before = wins[0][1] if wins else ""
            # nextVideo() only works inside playlists; on a normal watch page use the player's
            # Next button (it links to YouTube's Up Next), else the first sidebar video.
            body = ("var cur=VD().video_id||'';var nb=document.querySelector('.ytp-next-button');"
                    "var h=nb?(nb.getAttribute('href')||''):'';var L=function(f){setTimeout(f,600);};"
                    "if(h&&h.indexOf('v=')>=0&&h.indexOf(cur)<0){L(function(){nb.click();});return {how:'next-button'};}"
                    "var sb=document.querySelector('ytd-watch-next-secondary-results-renderer a[href*=\"/watch?v=\"], "
                    "ytd-compact-video-renderer a[href*=\"/watch?v=\"]');"
                    "if(sb&&sb.getAttribute('href').indexOf(cur)<0){L(function(){sb.click();});return {how:'sidebar'};}"
                    "if(A&&A.nextVideo){L(function(){A.nextVideo();});return {how:'api'};}return {how:'none'};"
                    if a == "next" else "setTimeout(function(){history.back();},600);return {how:'back'};")
            st, err = _js(body)
            if err:
                return _fallback(a, amount, value, err)
            end = time.time() + 4.0
            now = before
            while time.time() < end:
                time.sleep(0.3)
                wins = youtube_windows()
                now = wins[0][1] if wins else ""
                if now and now != before and "__JV" not in now and "__JV" not in before:
                    break
                if "__JV" in before and now and "__JV" not in now:
                    before = ""          # our own marker was still up at the start
            if isinstance(st, dict) and st.get("how") == "none":
                return "I couldn't find a next video here, Sir."
            if now and now != before and "__JV" not in now:
                return "Playing the next video, Sir." if a == "next" else "Went back, Sir."
            return ("I couldn't find a next video here, Sir." if a == "next"
                    else "There's no previous page, Sir.")

        return f"I don't know the YouTube action '{action}', Sir."
    except Exception as e:
        return f"YouTube player error: {e}"


# ── spoken-command parser ──────────────────────────────────────────────────

def parse_player_command(t: str):
    """
    Map a spoken player command to (action, amount, value), or None.
    `t` should already be lower-cased and stripped of 'jarvis'/punctuation.
    """
    t = t.lower().strip(" .,!?")

    # status / info
    if re.search(r"\b(?:where am i|what(?:'s| is) the (?:current )?(?:time|timestamp|position)|how much (?:time )?(?:is )?(?:left|remaining)|"
                 r"how long is (?:this|the) video|time (?:left|remaining)|what (?:video|song) is this|what(?:'s| is) this video|"
                 r"video (?:info|status)|what(?:'s| is) (?:the )?(?:speed|playback speed|volume))\b", t):
        return ("status", 0, "")

    # chapters
    if re.search(r"\b(?:list|show|tell|read|what are)(?: me)?(?: all)? (?:the )?chapters\b|^chapters$", t):
        return ("chapters", 0, "")
    if re.search(r"\b(?:what|which) chapter\b", t):
        return ("current_chapter", 0, "")
    if re.search(r"\bskip (?:the |this )?ads?\b|\bskip (?:the )?advert", t):
        return ("skip_ad", 0, "")
    if re.search(r"\b(?:skip|jump past|fast[\s-]?forward|move past|get past|go past|skip over)\s+(?:this|the current|current|the)\s+"
                 r"(?:part|section|bit|chapter|segment|portion|intro|sponsor(?:ship)?)\b|\bnext (?:chapter|section|part)\b|"
                 r"^skip (?:this )?(?:part|section|chapter|bit|intro)$", t):
        return ("skip_part", 0, "")
    if re.search(r"\b(?:previous|last) (?:chapter|section|part)\b|\brestart (?:this|the) (?:chapter|section|part)\b|"
                 r"\bback to (?:the )?(?:start of (?:this|the) )(?:chapter|section|part)\b", t):
        return ("chapter_prev", 0, "")
    m = re.search(r"\b(?:go|jump|skip|move|take me)\s+to\s+(?:the\s+)?chapter\s+(.+)$", t) \
        or re.search(r"\b(?:go|jump|skip|move|take me)\s+to\s+(?:the\s+)?(.+?)\s+(?:chapter|section|part)$", t) \
        or re.search(r"^chapter\s+(\w+)$", t)
    if m:
        return ("chapter_goto", 0, m.group(1).strip())

    # restart
    if re.search(r"^(?:restart|start over|replay)(?: (?:it|the video|this video))?$|"
                 r"\b(?:play|start|watch)(?: it| the video| this video)? (?:again )?from the (?:beginning|start|top)\b|"
                 r"\b(?:go|jump|skip|rewind|take me)(?: back)? to the (?:beginning|start|top)\b|^from the (?:beginning|start)$", t):
        return ("restart", 0, "")
    if re.search(r"\b(?:go|jump|skip|move|take me)\s+to\s+the\s+end\b", t):
        return ("seek_end", 10, "")

    # speed
    if re.search(r"\b(?:normal|regular|default|original|usual)\s+speed\b|\bspeed\s+(?:back\s+)?(?:to\s+)?normal\b|\breset (?:the )?speed\b", t):
        return ("speed", 0, "1")
    word_speed = {"double": 2, "twice": 2, "triple": 3, "half": 0.5, "quarter": 0.25}
    m = re.search(r"\b(double|twice|triple|half|quarter)\s+(?:the\s+)?speed\b", t)
    if m:
        return ("speed", 0, str(word_speed[m.group(1)]))
    if re.search(r"\bone and a half\s*(?:x|times)\b|\b1\s*and\s*a\s*half\s*(?:x|times)\b", t):
        return ("speed", 0, "1.5")
    m = re.search(r"\b(?:speed|rate|pace)\b\D{0,20}?(\d+(?:\.\d+)?)\s*(?:x|times)?\b", t) \
        or re.search(r"\b(\d+(?:\.\d+)?)\s*(?:x|times)(?:\s+speed)?\b", t) \
        or re.search(r"\b(?:speed|rate)\b\D{0,20}?\b(one|two|three|four)\b", t) \
        or re.search(r"\b(one|two|three|four)\s*(?:x|times)\s+speed\b", t)
    if m and not re.search(r"\b(?:forward|rewind|back|skip|volume)\b", t):
        return ("speed", 0, str(_num(m.group(1))))
    m = re.search(r"\b(?:speed(?: it)? up|faster|increase (?:the )?speed)\b(?:\s+by\s+(\d+(?:\.\d+)?))?", t)
    if m:
        return ("faster", float(m.group(1) or 0.25), "")
    m = re.search(r"\b(?:slow(?: it)? down|slower|decrease (?:the )?speed|reduce (?:the )?speed)\b(?:\s+by\s+(\d+(?:\.\d+)?))?", t)
    if m:
        return ("slower", float(m.group(1) or 0.25), "")

    # absolute seek: "go to 5:30", "jump to 10 minutes", "skip to the 2 minute mark", "halfway"
    if re.search(r"\b(?:halfway|half way|the middle)\b", t) and re.search(r"\b(?:go|jump|skip|move|take me|seek|to)\b", t):
        return ("seek_pct", 0, "50")
    m = re.search(r"\b(\d{1,3})\s*(?:percent|per cent|%)", t)
    if m and re.search(r"\b(?:go|jump|skip|move|seek|to)\b", t) and "volume" not in t:
        return ("seek_pct", 0, m.group(1))
    abs_m = re.search(r"\b(?:go|jump|skip|seek|move|fast[\s-]?forward|forward|rewind|take me|start(?: it)?|play(?: it)?|resume|set it|put it|continue)"
                      r"(?:\s+(?:it|the video|this video|back|ahead))?\s+(?:to|at|from)\s+(?:the\s+)?(.+)$", t)
    if abs_m:
        rest = abs_m.group(1)
        clock = parse_clock("to " + rest)
        dur = parse_duration(rest)
        if clock is not None:
            return ("seek_to", clock, "")
        if dur is not None:
            return ("seek_to", dur, "")
    clock = parse_clock(t)
    if clock is not None and re.fullmatch(r"(?:at\s+|to\s+)?\d{1,2}:\d{2}(?::\d{2})?", t):
        return ("seek_to", clock, "")

    # relative seek
    fwd = re.search(r"\b(?:fast[\s-]?forward|forward|skip(?: ahead| forward)?|jump(?: ahead| forward)?|go (?:ahead|forward)|move (?:ahead|forward)|ahead|advance)\b", t)
    back = re.search(r"\b(?:rewind|go back|back(?:ward)?s?|reverse|move back|jump back|skip back)\b", t)
    dur = parse_duration(t)
    if dur is not None and (fwd or back) and "volume" not in t:
        if back and (not fwd or back.start() < fwd.start()):
            return ("rewind", dur, "")
        return ("forward", dur, "")
    if re.fullmatch(r"(?:fast[\s-]?forward|skip ahead|jump ahead|go forward|forward)(?: (?:a bit|a little|it))?", t):
        return ("forward", 10, "")
    # bare "go back" = previous page (handled by youtube_control); "go back a bit" = rewind
    if re.fullmatch(r"(?:rewind|skip back|jump back)(?: (?:a bit|a little|it))?|go back (?:a bit|a little)", t):
        return ("rewind", 10, "")

    # YouTube player volume (plain "volume up/down" stays the system volume tool)
    m = re.search(r"\b(?:video |youtube |player )?volume\s+(?:to\s+|at\s+)?(\d{1,3})\s*(?:percent|%)?\b", t) \
        or re.search(r"\bset (?:the )?(?:video |youtube )?volume (?:to )?(\d{1,3})", t)
    if m:
        return ("volume", 0, m.group(1))
    if re.search(r"\b(?:video|youtube|player) volume (?:up|higher)\b|\b(?:increase|raise) (?:the )?(?:video|youtube) volume\b", t):
        return ("volume_up", 10, "")
    if re.search(r"\b(?:video|youtube|player) volume (?:down|lower)\b|\b(?:decrease|lower|reduce) (?:the )?(?:video|youtube) volume\b", t):
        return ("volume_down", 10, "")
    if re.fullmatch(r"unmute(?:\s+(?:it|the video|video|youtube|this))?", t):
        return ("unmute", 0, "")
    if re.fullmatch(r"mute(?:\s+(?:it|the video|video|youtube|this))?", t):
        return ("mute", 0, "")

    # captions
    if re.search(r"\b(?:captions?|subtitles?|cc)\b", t):
        if re.search(r"\b(?:off|disable|hide|remove|stop|no)\b", t):
            return ("captions", 0, "off")
        if re.search(r"\b(?:on|enable|show|turn on|add)\b", t):
            return ("captions", 0, "on")
        return ("captions", 0, "toggle")

    # loop
    if re.search(r"\b(?:stop|turn off|disable|no|cancel)\s+(?:the\s+)?loop(?:ing)?\b|\bunloop\b|\bloop off\b|\bdon'?t (?:loop|repeat)\b", t):
        return ("loop", 0, "off")
    if re.search(r"\bloop\b|\brepeat (?:this|the|it)(?: video)?\b|\bon repeat\b", t):
        return ("loop", 0, "on")

    # quality
    m = re.search(r"\b(144|240|360|480|720|1080|1440|2160)\s*p\b", t) \
        or re.search(r"\b(?:quality|resolution)\b.*?\b(144|240|360|480|720|1080|1440|2160|4k|hd|full hd|max|best|highest|lowest|min|auto)\b", t)
    if m:
        return ("quality", 0, m.group(1))
    if re.search(r"\b(?:max(?:imum)?|best|highest) (?:quality|resolution)\b", t):
        return ("quality", 0, "max")
    if re.search(r"\b(?:lowest|minimum|worst) (?:quality|resolution)\b|\bdata saver\b", t):
        return ("quality", 0, "lowest")

    # view modes
    if re.search(r"\bfull\s*screen\b", t):
        out = re.search(r"\b(?:exit|leave|close|stop|come out|get out|minimi[sz]e|turn off|disable|out of)\b", t)
        return ("exit_fullscreen" if out else "fullscreen", 0, "")
    if re.search(r"\btheat(?:er|re)\s+mode\b|\bcinema mode\b|\bwide mode\b", t):
        return ("theater", 0, "")
    if re.search(r"\bmini ?player\b", t):
        return ("miniplayer", 0, "")
    if re.search(r"\bpicture[\s-]in[\s-]picture\b|\bpip\b|\bpop ?out\b|\bfloating (?:video|window)\b", t):
        return ("pip", 0, "")

    # engagement (not "song" — "like this song" is Spotify)
    if re.search(r"\b(?:un-?like|remove (?:my|the) like)\b", t) and "song" not in t:
        return ("unlike", 0, "")
    if re.search(r"\bdislike (?:this|the|it)\b(?! song)", t):
        return ("dislike", 0, "")
    if re.search(r"\b(?:like (?:this|the) video|like it|give (?:it|this|the video) a (?:like|thumbs up)|hit (?:the )?like|thumbs up)\b", t):
        return ("like", 0, "")
    if re.search(r"^(?:please\s+)?subscribe\b|\bsubscribe to (?:this|the|him|her|them)\b", t):
        return ("subscribe", 0, "")

    # play / pause
    if re.fullmatch(r"(?:pause|stop|hold on|wait|freeze)(?:\s+(?:it|the video|video|this|that|youtube|playback|the youtube video))?(?:\s+(?:please|for a (?:sec|second|moment)))?", t):
        return ("pause", 0, "")
    if re.fullmatch(r"(?:resume|continue|unpause|play)(?:\s+(?:it|the video|video|this|that|youtube|playing|again|the youtube video))?(?:\s+please)?", t):
        return ("play", 0, "")
    return None
