"""
Jarvis Tool Registry — All callable actions Jarvis can perform.
Includes agentic tools for multi-step automation (PDF, Word, window mgmt, Copilot).
"""
from datetime import datetime
import webbrowser
import threading
import urllib.parse
import tkinter as tk
import subprocess
import os
import sys
import re
import pyperclip
import pyautogui
import psutil

from app.services.whatsapp import open_whatsapp, send_whatsapp_message

pyautogui.FAILSAFE = False


# ─── Web & Information ──────────────────────────────────────────────────────

def _extract_location(query: str) -> str:
    """Pulls a clean location name out of a weather query."""
    # Remove filler words
    for word in ['current', 'weather', 'temperature', 'temp', 'forecast',
                 'tell me', 'what is', 'what\'s', 'the', 'whats', 'today',
                 'in', 'of', 'at', 'right now', 'now', 'india']:
        query = re.sub(rf'\b{re.escape(word)}\b', ' ', query, flags=re.IGNORECASE)
    return query.strip(' ,.-') or "Delhi"


def get_weather(location: str) -> str:
    """Get current weather using wttr.in — returns a clean spoken string."""
    try:
        import requests
        # Detailed JSON weather
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            feels_c = current['FeelsLikeC']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            area = data['nearest_area'][0]['areaName'][0]['value']
            region = data['nearest_area'][0]['region'][0]['value']
            return (f"{desc}, {temp_c}°C (feels like {feels_c}°C), "
                    f"humidity {humidity}% in {area}, {region}.")
    except Exception:
        pass
    # Fallback: simple format string
    try:
        import requests
        resp = requests.get(f"https://wttr.in/{urllib.parse.quote(location)}?format=3", timeout=5)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception:
        pass
    return f"Couldn't fetch weather for {location}."


def get_info(query: str) -> str:
    """
    Smart information lookup:
    - Weather queries → wttr.in (reliable, real-time)
    - Everything else → DuckDuckGo text search
    Does NOT open any browser.
    """
    lower = query.lower()

    # Route weather queries to the dedicated weather API
    weather_kw = ['weather', 'temperature', 'temp', 'rain', 'forecast', 'humidity', 'mausam', 'barish']
    if any(kw in lower for kw in weather_kw):
        location = _extract_location(query)
        return get_weather(location)

    # General knowledge — Google Search (via googlesearch-python)
    try:
        from googlesearch import search
        import requests
        from bs4 import BeautifulSoup
        
        urls = list(search(query, num_results=3, lang="en"))
        if not urls:
            return f"No results found for: {query}"
        
        snippets = []
        for url in urls[:2]:
            try:
                resp = requests.get(url, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    text = " ".join(p.text for p in soup.find_all('p'))
                    snippets.append(text[:300])
            except Exception:
                continue
                
        if not snippets:
            return f"Found results but couldn't extract text. URLs: {', '.join(urls)}"
            
        return " | ".join(snippets)[:1000]
    except Exception as e:
        return f"Search failed: {e}"


SITE_SHORTCUTS = {
    # Global
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org",
    "twitter": "https://www.twitter.com",
    "x": "https://www.x.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
    "amazon": "https://www.amazon.in",
    "whatsapp": "whatsapp:",
    "chatgpt": "https://chat.openai.com",
    "gemini": "https://gemini.google.com",
    # Indian streaming
    "hotstar": "https://www.hotstar.com",
    "disney": "https://www.hotstar.com",
    "disney hotstar": "https://www.hotstar.com",
    "jiocinema": "https://www.jiocinema.com",
    "jio cinema": "https://www.jiocinema.com",
    "jio": "https://www.jiocinema.com",
    "zee5": "https://www.zee5.com",
    "sonyliv": "https://www.sonyliv.com",
    "sony liv": "https://www.sonyliv.com",
    "prime": "https://www.primevideo.com",
    "prime video": "https://www.primevideo.com",
    "amazon prime": "https://www.primevideo.com",
    "mxplayer": "https://www.mxplayer.in",
    # Social & productivity
    "facebook": "https://www.facebook.com",
    "telegram": "https://web.telegram.org",
    "notion": "https://www.notion.so",
    "figma": "https://www.figma.com",
    "canva": "https://www.canva.com",
    "stackoverflow": "https://www.stackoverflow.com",
    "stack overflow": "https://www.stackoverflow.com",
    "flipkart": "https://www.flipkart.com",
    "swiggy": "https://www.swiggy.com",
    "zomato": "https://www.zomato.com",
}

def open_safe_website(url: str, browser: str = None) -> str:
    """Opens a specific website in the browser."""
    url_lower = url.lower().strip()
    if url_lower in SITE_SHORTCUTS:
        final_url = SITE_SHORTCUTS[url_lower]
    elif url.startswith("http"):
        final_url = url
    else:
        final_url = f"https://www.{url_lower.replace(' ', '')}.com"
        
    if browser and "chrome" in browser.lower():
        subprocess.Popen(f'start chrome "{final_url}"', shell=True)
        return f"Opened {final_url} in Chrome"
    elif browser and "edge" in browser.lower():
        subprocess.Popen(f'start msedge "{final_url}"', shell=True)
        return f"Opened {final_url} in Edge"
        
    webbrowser.open(final_url)
    return f"Opened: {final_url}"

def open_google_search_in_browser(query: str) -> str:
    """Opens Google search in browser for user to see results."""
    encoded = urllib.parse.quote_plus(query)
    webbrowser.open(f"https://www.google.com/search?q={encoded}")
    return f"Searched Google for: {query}"

def youtube_search(query: str, autoplay: bool = False) -> str:
    """Search YouTube and either play the first video or show results."""
    encoded = urllib.parse.quote_plus(query)
    if autoplay:
        try:
            from urllib.request import urlopen
            html = urlopen(f"https://www.youtube.com/results?search_query={encoded}").read().decode()
            video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html)
            if video_ids:
                first_vid = video_ids[0]
                webbrowser.open(f"https://www.youtube.com/watch?v={first_vid}")
                return f"Playing first YouTube result for: {query}"
        except Exception as e:
            pass
    
    # Fallback or if autoplay is False
    webbrowser.open(f"https://www.youtube.com/results?search_query={encoded}")
    return f"Searching YouTube for: {query}"


# ─── Date & Time ────────────────────────────────────────────────────────────

def get_system_time() -> str:
    """Returns current date and time naturally."""
    return datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")


# ─── System Information ─────────────────────────────────────────────────────

def get_system_info() -> str:
    """Returns CPU usage, RAM usage, and battery status."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_used = ram.used // (1024**3)
    ram_total = ram.total // (1024**3)
    info = f"CPU: {cpu}% | RAM: {ram_used}GB of {ram_total}GB used"
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "charging" if battery.power_plugged else "on battery"
            info += f" | Battery: {int(battery.percent)}% ({status})"
    except Exception:
        pass
    return info


# ─── Screen & Window Control ────────────────────────────────────────────────

def take_screenshot(filename: str = None) -> str:
    """Takes a full screenshot and saves to Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    fname = filename or f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
    save_path = os.path.join(desktop, fname)
    pyautogui.screenshot().save(save_path)
    return "Screenshot saved to Desktop."

def snap_windows(left_app: str, right_app: str) -> str:
    """Snaps left_app to left half and right_app to right half with fuzzy name matching."""
    import pygetwindow as gw
    import re

    screen_width, screen_height = pyautogui.size()
    half_width = screen_width // 2

    def _normalize(s: str) -> str:
        return re.sub(r'[^a-z0-9]', '', s.lower())

    def _find_win(app_name):
        target = _normalize(app_name)
        all_wins = [w for w in gw.getAllWindows() if w.title]
        # Exact contains
        for w in all_wins:
            if target in _normalize(w.title):
                return w
        # Partial word overlap fallback
        target_words = [t for t in target.split() if len(t) > 3]
        for w in all_wins:
            norm = _normalize(w.title)
            if any(word in norm for word in target_words):
                return w
        return None

    l_win = _find_win(left_app)
    r_win = _find_win(right_app)

    if not l_win:
        return f"Could not find a window for '{left_app}'. Make sure the app is open."
    if not r_win:
        return f"Could not find a window for '{right_app}'. Make sure the app is open."

    try:
        import time
        # Snap Left
        if l_win.isMinimized: l_win.restore()
        l_win.activate()
        time.sleep(0.3)
        pyautogui.hotkey('win', 'left')
        
        # Snap Right
        if r_win.isMinimized: r_win.restore()
        r_win.activate()
        time.sleep(0.3)
        pyautogui.hotkey('win', 'right')
        
        return f"Done! '{l_win.title[:25]}' on the left and '{r_win.title[:25]}' on the right."
    except Exception as e:
        return f"Error arranging windows: {e}"


# ─── File Operations ────────────────────────────────────────────────────────
def create_folder(folder_name: str) -> str:
    """Creates a new folder on the Desktop."""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        path = os.path.join(desktop, folder_name)
        os.makedirs(path, exist_ok=True)
        return f"Successfully created folder '{folder_name}' on Desktop."
    except Exception as e:
        return f"Failed to create folder: {str(e)}"

def create_file(filepath: str, content: str) -> str:
    """Creates a new file with the given content."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully created file: {filepath}"
    except Exception as e:
        return f"Failed to create file: {str(e)}"

def append_to_file(filepath: str, content: str) -> str:
    """Appends content to an existing file."""
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write("\n" + content)
        return f"Successfully appended to file: {filepath}"
    except Exception as e:
        return f"Failed to edit file: {str(e)}"

def close_tab() -> str:
    """Closes the current browser tab using Ctrl+W."""
    pyautogui.hotkey('ctrl', 'w')
    return "Closed the current tab."

def close_window() -> str:
    """Closes the current active window using Alt+F4."""
    pyautogui.hotkey('alt', 'f4')
    return "Closed the active window."

def _find_window_fuzzy(app_name: str):
    """Find a window by fuzzy name matching — strips hyphens/spaces for comparison."""
    import pygetwindow as gw
    import re
    def _norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
    target = _norm(app_name)
    all_wins = [w for w in gw.getAllWindows() if w.title]
    for w in all_wins:
        if target in _norm(w.title): return w
    # Word overlap fallback
    words = [t for t in target.split() if len(t) > 2]
    for w in all_wins:
        norm = _norm(w.title)
        if any(word in norm for word in words): return w
    return None

def close_specific_window(app_name: str) -> str:
    """Closes a specific window/app by name."""
    import time
    win = _find_window_fuzzy(app_name)
    if not win:
        return f"Could not find an open window for '{app_name}'."
    try:
        win.activate()
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'f4')
        return f"Closed '{win.title[:40]}'."
    except Exception as e:
        return f"Failed to close '{app_name}': {e}"

def minimize_window(app_name: str) -> str:
    """Minimizes a specific window by name."""
    win = _find_window_fuzzy(app_name)
    if not win:
        return f"Could not find an open window for '{app_name}'."
    try:
        win.minimize()
        return f"Minimized '{win.title[:40]}'."
    except Exception as e:
        return f"Failed to minimize '{app_name}': {e}"

def maximize_window(app_name: str) -> str:
    """Maximizes/restores a specific window by name."""
    win = _find_window_fuzzy(app_name)
    if not win:
        return f"Could not find an open window for '{app_name}'."
    try:
        win.maximize()
        return f"Maximized '{win.title[:40]}'."
    except Exception as e:
        return f"Failed to maximize '{app_name}': {e}"



def minimize_all_windows() -> str:
    """Minimizes all open windows to show the desktop."""
    pyautogui.hotkey('win', 'd')
    return "All windows minimized."

def lock_screen() -> str:
    """Locks the Windows screen."""
    pyautogui.hotkey('win', 'l')
    return "Screen locked."


# ─── Volume & Media Control ─────────────────────────────────────────────────

def volume_up(steps: int = 5) -> str:
    """Increases system volume."""
    for _ in range(steps):
        pyautogui.press('volumeup')
    return f"Volume increased."

def volume_down(steps: int = 5) -> str:
    """Decreases system volume."""
    for _ in range(steps):
        pyautogui.press('volumedown')
    return f"Volume decreased."

def mute_volume() -> str:
    """Toggles mute on the system."""
    pyautogui.press('volumemute')
    return "Volume toggled mute."

def media_play_pause() -> str:
    """Plays or pauses media (Spotify, YouTube, etc.)."""
    pyautogui.press('playpause')
    return "Media play/pause toggled."

def media_next() -> str:
    """Skips to next track."""
    pyautogui.press('nexttrack')
    return "Skipped to next track."

def media_previous() -> str:
    """Goes to previous track."""
    pyautogui.press('prevtrack')
    return "Went to previous track."

def play_music(song: str) -> str:
    """Play a song on Spotify by searching and using Tab/Enter."""
    import time
    def _do_play():
        subprocess.Popen(f'start "" "spotify:search:{song}"', shell=True)
        time.sleep(3.5)
        try:
            import pygetwindow as gw
            wins = [w for w in gw.getAllWindows() if w.title and 'spotify' in w.title.lower()]
            if wins:
                win = wins[0]
                win.restore()
                win.activate()
                time.sleep(1.0)
                # Fallback: Tab from search bar to Best Result, then Enter
                pyautogui.press('tab')
                time.sleep(0.3)
                pyautogui.press('enter')
        except Exception as e:
            pass

    threading.Thread(target=_do_play, daemon=True).start()
    return f"Playing '{song}' on Spotify."


# ─── Clipboard & Typing ─────────────────────────────────────────────────────

def read_clipboard() -> str:
    """Reads and returns the current clipboard content."""
    content = pyperclip.paste()
    return f"Clipboard contains: {content[:500]}" if content else "Clipboard is empty."

def write_clipboard(text: str) -> str:
    """Copies text to the clipboard."""
    pyperclip.copy(text)
    return f"Copied to clipboard: '{text}'"

def type_text(text: str) -> str:
    """Types the given text into the currently focused window."""
    import time
    time.sleep(0.5)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    return f"Typed: '{text}'"


# ─── App Launcher ────────────────────────────────────────────────────────────

def open_app(app_name: str) -> str:
    """Opens a Windows application by name."""
    apps = {
        "notepad": "notepad.exe", "calculator": "calc.exe", "paint": "mspaint.exe",
        "file explorer": "explorer.exe", "explorer": "explorer.exe",
        "task manager": "taskmgr.exe", "cmd": "cmd.exe", "command prompt": "cmd.exe",
        "terminal": "wt.exe", "vs code": "code", "vscode": "code",
        "word": "winword.exe", "excel": "excel.exe", "powerpoint": "powerpnt.exe",
        "chrome": "chrome.exe", "edge": "msedge.exe",
        "spotify": "spotify.exe", "discord": "discord.exe", "zoom": "zoom.exe",
        "settings": "ms-settings:", "control panel": "control.exe",
        "snipping tool": "snippingtool.exe",
    }
    exe = apps.get(app_name.lower().strip(), app_name)
    try:
        subprocess.Popen(exe, shell=True)
        return f"Opened {app_name}."
    except Exception as e:
        return f"Could not open {app_name}: {e}"


# ─── Sticky Notes ────────────────────────────────────────────────────────────

def _spawn_sticky(content: str):
    root = tk.Tk()
    root.title("📌 Jarvis Note")
    screen_w = root.winfo_screenwidth()
    root.geometry(f"300x200+{screen_w - 320}+40")
    root.configure(bg="#FFEF9F")
    root.attributes("-topmost", True)
    header = tk.Frame(root, bg="#F5C518", height=28)
    header.pack(fill=tk.X)
    tk.Label(header, text="📌 Jarvis Note", bg="#F5C518",
             font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=8, pady=4)
    tk.Button(header, text="✕", bg="#F5C518", relief=tk.FLAT,
              command=root.destroy).pack(side=tk.RIGHT, padx=6, pady=2)
    tk.Text(root, bg="#FFEF9F", fg="#1a1a1a", font=("Segoe UI", 11),
            wrap=tk.WORD, relief=tk.FLAT, bd=8).pack(fill=tk.BOTH, expand=True)
    root.nametowidget(root.winfo_children()[-1]).insert(tk.END, content)
    root.mainloop()

def create_sticky_note(content: str) -> str:
    """Creates a floating sticky note on screen."""
    threading.Thread(target=_spawn_sticky, args=(content,), daemon=True).start()
    return f"Sticky note created."

def close_sticky_notes() -> str:
    """Closes all active sticky notes created by Jarvis."""
    try:
        import pygetwindow as gw
        closed = 0
        for w in gw.getAllWindows():
            if w.title and "📌 Jarvis Note" in w.title:
                w.close()
                closed += 1
        if closed > 0:
            return f"Closed {closed} sticky note(s)."
        return "No sticky notes found."
    except Exception as e:
        return f"Failed to close sticky notes: {e}"


# ─── Math & Calculations ─────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    """Safely evaluates a math expression and returns the result."""
    try:
        # Only allow safe math characters
        safe = re.sub(r'[^0-9+\-*/.() %]', '', expression)
        result = eval(safe)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Could not calculate: {expression} ({e})"


# ─── Reminders ───────────────────────────────────────────────────────────────

def set_reminder(message: str, seconds: int = 60) -> str:
    """Sets a reminder that Jarvis will speak after a given number of seconds."""
    def _remind():
        import time
        time.sleep(seconds)
        # Import here to avoid circular import
        import asyncio
        from app.services.voice import speak_text as _speak
        asyncio.run(_speak(f"Reminder: {message}"))

    threading.Thread(target=_remind, daemon=True).start()
    minutes = seconds // 60
    return f"Reminder set for {minutes} minute{'s' if minutes != 1 else ''}: '{message}'"




# ─── Memory Tools ─────────────────────────────────────────────────────────────

def remember_preference(key: str, value: str) -> str:
    """Save a user preference to long-term memory."""
    try:
        from app.memory import save_preference
        save_preference(key.strip(), value.strip())
        return f"Got it! I'll remember that your {key} preference is: {value}."
    except Exception as e:
        return f"Couldn't save preference: {e}"


def list_learned_skills() -> str:
    """Return all dynamic skills Jarvis has learned."""
    try:
        from app.memory import list_skills
        skills = list_skills()
        if not skills:
            return "I haven't learned any custom skills yet. Give me tasks to figure out and I'll remember them!"
        lines = "\n".join(f"• {s}" for s in skills[:20])
        return f"I've learned {len(skills)} custom skill(s):\n{lines}"
    except Exception as e:
        return f"Couldn't retrieve skills: {e}"


# ─── Agentic / Multi-Step Tools ───────────────────────────────────────────────

def read_pdf_text(path: str = None, filename: str = None) -> str:
    """Extract all text from a PDF file. Accepts full path or filename to search on Desktop."""
    import time
    # Resolve path if only filename given
    if not path and filename:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        docs = os.path.join(os.path.expanduser("~"), "Documents")
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        for folder in [desktop, docs, downloads]:
            candidate = os.path.join(folder, filename)
            if os.path.exists(candidate):
                path = candidate
                break
        if not path:
            # Try case-insensitive search
            for folder in [desktop, docs, downloads]:
                try:
                    for f in os.listdir(folder):
                        if f.lower() == filename.lower():
                            path = os.path.join(folder, f)
                            break
                except Exception:
                    pass
                if path:
                    break
    if not path or not os.path.exists(path):
        return f"PDF file not found: {filename or path}"
    # Try pdfplumber first (best for text PDFs)
    try:
        import pdfplumber
        text_pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_pages.append(t)
        text = "\n\n".join(text_pages)
        if text.strip():
            return text[:8000]  # cap at 8000 chars
    except ImportError:
        pass
    except Exception as e:
        pass
    # Try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(path)
        text = "\n\n".join(page.get_text() for page in doc)
        if text.strip():
            return text[:8000]
    except ImportError:
        pass
    except Exception:
        pass
    # Fallback: install pdfplumber and retry
    try:
        subprocess.run([sys.executable if 'sys' in dir() else 'python', '-m', 'pip', 'install', 'pdfplumber', '-q'], timeout=30)
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            text = "\n\n".join(p.extract_text() or "" for p in pdf.pages)
        return text[:8000] if text.strip() else "Could not extract text from PDF."
    except Exception as e:
        return f"Failed to read PDF: {e}"


def find_file(name: str, location: str = "all") -> str:
    """Find a file by name (or partial name) on Desktop, Documents, Downloads."""
    search_dirs = {
        "desktop": [os.path.join(os.path.expanduser("~"), "Desktop")],
        "documents": [os.path.join(os.path.expanduser("~"), "Documents")],
        "downloads": [os.path.join(os.path.expanduser("~"), "Downloads")],
        "all": [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
        ]
    }
    dirs = search_dirs.get(location.lower(), search_dirs["all"])
    name_lower = name.lower()
    found = []
    for d in dirs:
        try:
            for f in os.listdir(d):
                if name_lower in f.lower():
                    found.append(os.path.join(d, f))
        except Exception:
            pass
    if not found:
        return f"No file matching '{name}' found in {location}."
    return "\n".join(found[:5])


def open_file(path: str) -> str:
    """Open any file with its default application."""
    try:
        os.startfile(path)
        return f"Opened: {os.path.basename(path)}"
    except Exception as e:
        try:
            subprocess.Popen(['cmd', '/c', 'start', '', path], shell=False)
            return f"Opened: {os.path.basename(path)}"
        except Exception as e2:
            return f"Failed to open file: {e2}"


def focus_window(name: str, timeout: float = 5.0) -> str:
    """Bring a window to the foreground by partial name match."""
    import time
    try:
        import pygetwindow as gw
        deadline = time.time() + timeout
        while time.time() < deadline:
            for w in gw.getAllWindows():
                if w.title and name.lower() in w.title.lower():
                    if w.isMinimized:
                        w.restore()
                    w.activate()
                    time.sleep(0.4)
                    return f"Focused window: {w.title[:50]}"
            time.sleep(0.3)
        return f"Window '{name}' not found after {timeout}s."
    except Exception as e:
        return f"focus_window error: {e}"


def wait_for_window(name: str, timeout: float = 15.0) -> str:
    """Block until a window with the given name appears, then focus it."""
    import time
    try:
        import pygetwindow as gw
        deadline = time.time() + timeout
        while time.time() < deadline:
            for w in gw.getAllWindows():
                if w.title and name.lower() in w.title.lower():
                    if w.isMinimized:
                        w.restore()
                    w.activate()
                    time.sleep(0.4)
                    return f"Window appeared and focused: {w.title[:50]}"
            time.sleep(0.5)
        return f"Timed out waiting for window '{name}' after {timeout}s."
    except Exception as e:
        return f"wait_for_window error: {e}"


def type_and_submit(text: str, delay: float = 0.3) -> str:
    """Type text into the focused field, then press Enter."""
    import time
    time.sleep(delay)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.press('enter')
    return f"Typed and submitted: '{text[:60]}'"


def copy_selected_text() -> str:
    """Select all text in the focused element and copy to clipboard, then return it."""
    import time
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    content = pyperclip.paste()
    return content[:5000] if content else "(clipboard empty after copy)"


def create_word_doc(filename: str, content: str, save_path: str = None) -> str:
    """Create a .docx Word document with the given content.
    content can be a list of (heading, body) tuples formatted as 'Q: ...\nA: ...' blocks.
    """
    if not save_path:
        save_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
    if not save_path.endswith('.docx'):
        save_path += '.docx'
    try:
        try:
            from docx import Document
        except ImportError:
            subprocess.run([sys.executable if 'sys' in dir() else 'python', '-m', 'pip', 'install', 'python-docx', '-q'], timeout=60)
            from docx import Document
        doc = Document()
        doc.add_heading(os.path.splitext(os.path.basename(save_path))[0], 0)
        # Parse Q&A blocks if present
        blocks = content.split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            for line in lines:
                if line.startswith('Q:') or line.startswith('Question:'):
                    doc.add_heading(line, level=2)
                elif line.startswith('A:') or line.startswith('Answer:'):
                    doc.add_paragraph(line)
                else:
                    doc.add_paragraph(line)
        doc.save(save_path)
        return f"Word document saved: {save_path}"
    except Exception as e:
        # Fallback: save as plain text .txt
        txt_path = save_path.replace('.docx', '.txt')
        try:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Saved as text file (python-docx unavailable): {txt_path}"
        except Exception as e2:
            return f"Failed to create document: {e} | txt fallback: {e2}"


def read_active_window_text() -> str:
    """Get all readable text from the currently active window."""
    try:
        from app.services.ui_inspector import get_active_window_info
        return get_active_window_info()
    except Exception as e:
        return f"Could not read active window: {e}"


def open_windows_copilot() -> str:
    """Open Windows Copilot sidebar using Win+C hotkey."""
    import time
    pyautogui.hotkey('win', 'c')
    time.sleep(2.5)  # Wait for Copilot panel to animate open
    return "Windows Copilot opened."


def send_to_copilot(question: str, wait_seconds: float = 8.0) -> str:
    """Type a question into the Windows Copilot sidebar and retrieve the response.
    Assumes Copilot is already open and focused.
    """
    import time
    # Click Copilot input area — it's usually at the bottom of the panel
    # Use the UI inspector to find the text box
    try:
        from app.services.ui_inspector import click_ui_element
        clicked = click_ui_element("Ask me anything")
        if not clicked:
            clicked = click_ui_element("Message Copilot")
        if not clicked:
            # Try clicking in the lower-right area where Copilot input usually sits
            screen_w, screen_h = pyautogui.size()
            pyautogui.click(screen_w - 200, screen_h - 80)
        time.sleep(0.5)
    except Exception:
        pass
    # Type the question
    pyperclip.copy(question)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.4)
    pyautogui.press('enter')
    # Wait for Copilot to respond
    time.sleep(wait_seconds)
    # Try to copy response — Copilot has a copy button after each response
    try:
        from app.services.ui_inspector import click_ui_element
        click_ui_element("Copy")
        time.sleep(0.5)
        response = pyperclip.paste()
        if response and response != question:
            return response[:3000]
    except Exception:
        pass
    # Fallback: select all text in panel and copy
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    response = pyperclip.paste()
    return response[:3000] if response else "(Could not retrieve Copilot response)"


TOOL_REGISTRY = {
    # Information & Web
    "get_info": get_info,
    "get_system_time": get_system_time,
    "get_system_info": get_system_info,
    "open_website": open_safe_website,
    "open_google_search_in_browser": open_google_search_in_browser,
    "youtube_search": youtube_search,
    "take_screenshot": take_screenshot,
    "snap_windows": snap_windows,
    # File Operations
    "create_folder": create_folder,
    "create_file": create_file,
    "append_to_file": append_to_file,
    # Browser controls
    "close_tab": close_tab,
    "close_window": close_window,
    "close_specific_window": close_specific_window,
    "minimize_window": minimize_window,
    "maximize_window": maximize_window,
    "minimize_all_windows": minimize_all_windows,
    "lock_screen": lock_screen,
    # Volume / Media
    "volume_up": volume_up,
    "volume_down": volume_down,
    "mute_volume": mute_volume,
    "play_music": play_music,
    "media_play_pause": media_play_pause,
    "media_next": media_next,
    "media_previous": media_previous,
    # Clipboard & Typing
    "read_clipboard": read_clipboard,
    "write_clipboard": write_clipboard,
    "type_text": type_text,
    # Apps
    "open_app": open_app,
    # Notes & Reminders
    "create_sticky_note": create_sticky_note,
    "close_sticky_notes": close_sticky_notes,
    "set_reminder": set_reminder,
    # Math
    "calculate": calculate,
    # WhatsApp
    "open_whatsapp": open_whatsapp,
    "send_whatsapp_message": send_whatsapp_message,
    # Memory
    "remember_preference": remember_preference,
    "list_learned_skills": list_learned_skills,
    # ── Agentic / Multi-Step Tools ──
    "read_pdf_text": read_pdf_text,
    "find_file": find_file,
    "open_file": open_file,
    "focus_window": focus_window,
    "wait_for_window": wait_for_window,
    "type_and_submit": type_and_submit,
    "copy_selected_text": copy_selected_text,
    "create_word_doc": create_word_doc,
    "read_active_window_text": read_active_window_text,
    "open_windows_copilot": open_windows_copilot,
    "send_to_copilot": send_to_copilot,
}
