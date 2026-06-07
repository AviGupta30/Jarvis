"""
prompt_overlay.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jarvis Step 2: Floating Prompt Enhancer Overlay

Hotkey: Ctrl+Space
- Press Ctrl+Space anywhere on Windows
- A sleek dark popup appears
- Type your raw prompt → click Enhance
- Groq API (via Jarvis /chat backend) refines it
- Copy to clipboard or inject back into the active app

Run with:
    python -m app.services.prompt_overlay

Rule #4 compliant: calls /chat backend, imports nothing else from Jarvis.
"""

import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import threading
import requests
import keyboard
import pyautogui
import pyperclip
import time
import sys

# ── Config ────────────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000/chat"
HOTKEY      = "ctrl+space"

# ── Dark Theme Palette ────────────────────────────────────────────────────────
BG_DARK       = "#0d0d0f"
BG_CARD       = "#131318"
BG_INPUT      = "#1a1a24"
BG_RESULT     = "#111118"
ACCENT        = "#7c3aed"          # violet
ACCENT_HOVER  = "#6d28d9"
ACCENT_2      = "#06b6d4"          # cyan
TEXT_PRIMARY  = "#f0f0f8"
TEXT_MUTED    = "#6b6b80"
BORDER        = "#2a2a3a"
SUCCESS       = "#10b981"
FONT_FAMILY   = "Segoe UI"

# ── Overlay Window ─────────────────────────────────────────────────────────────
class PromptOverlay:
    def __init__(self):
        self.root = None
        self.visible = False
        self._prev_hwnd = None        # window that was active before popup
        self._enhancing = False

    # ── Build the Tk window ────────────────────────────────────────────────────
    def _build_window(self):
        self.root = tk.Tk()
        self.root.withdraw()          # start hidden
        self.root.title("Jarvis Prompt Enhancer")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)
        self.root.overrideredirect(True)   # borderless
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.97)

        # ── Drag support ──────────────────────────────────────────────────────
        self._drag_x = 0
        self._drag_y = 0

        # ── Outer frame (border glow) ─────────────────────────────────────────
        outer = tk.Frame(self.root, bg=ACCENT, padx=1, pady=1)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg=BG_CARD, padx=24, pady=20)
        card.pack(fill="both", expand=True)

        # Drag bindings on card
        card.bind("<ButtonPress-1>", self._drag_start)
        card.bind("<B1-Motion>",     self._drag_motion)

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(card, bg=BG_CARD)
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header, text="⚡  Prompt Enhancer", bg=BG_CARD,
            fg=TEXT_PRIMARY, font=(FONT_FAMILY, 14, "bold")
        ).pack(side="left")

        close_btn = tk.Label(
            header, text="✕", bg=BG_CARD, fg=TEXT_MUTED,
            font=(FONT_FAMILY, 13), cursor="hand2"
        )
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.hide())
        close_btn.bind("<Enter>",    lambda e: close_btn.config(fg=TEXT_PRIMARY))
        close_btn.bind("<Leave>",    lambda e: close_btn.config(fg=TEXT_MUTED))

        # ── Raw prompt label ──────────────────────────────────────────────────
        tk.Label(
            card, text="Raw Prompt", bg=BG_CARD,
            fg=TEXT_MUTED, font=(FONT_FAMILY, 9)
        ).pack(anchor="w", pady=(0, 4))

        # ── Input textarea ────────────────────────────────────────────────────
        self.input_box = tk.Text(
            card, height=4, width=62, wrap="word",
            bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief="flat", font=(FONT_FAMILY, 11),
            padx=10, pady=8,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        self.input_box.pack(fill="x", pady=(0, 12))
        self.input_box.bind("<Return>",       self._on_enter)
        self.input_box.bind("<Escape>",       lambda e: self.hide())
        self.input_box.bind("<Shift-Return>", lambda e: "break")  # allow newlines w/ shift

        # ── Enhance button ────────────────────────────────────────────────────
        self.enhance_btn = tk.Button(
            card, text="✦  Enhance", command=self._start_enhance,
            bg=ACCENT, fg="white", font=(FONT_FAMILY, 10, "bold"),
            relief="flat", padx=16, pady=7, cursor="hand2",
            activebackground=ACCENT_HOVER, activeforeground="white",
            bd=0
        )
        self.enhance_btn.pack(anchor="w", pady=(0, 16))
        self.enhance_btn.bind("<Enter>", lambda e: self.enhance_btn.config(bg=ACCENT_HOVER))
        self.enhance_btn.bind("<Leave>", lambda e: self.enhance_btn.config(bg=ACCENT))

        # ── Status label ──────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="")
        self.status_lbl = tk.Label(
            card, textvariable=self.status_var, bg=BG_CARD,
            fg=ACCENT_2, font=(FONT_FAMILY, 9)
        )
        self.status_lbl.pack(anchor="w", pady=(0, 4))

        # ── Result label ──────────────────────────────────────────────────────
        tk.Label(
            card, text="Enhanced Prompt", bg=BG_CARD,
            fg=TEXT_MUTED, font=(FONT_FAMILY, 9)
        ).pack(anchor="w", pady=(0, 4))

        # ── Result textarea ───────────────────────────────────────────────────
        self.result_box = tk.Text(
            card, height=8, width=62, wrap="word",
            bg=BG_RESULT, fg=TEXT_PRIMARY,
            relief="flat", font=(FONT_FAMILY, 11),
            padx=10, pady=8, state="disabled",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        self.result_box.pack(fill="x", pady=(0, 14))

        # ── Action buttons ─────────────────────────────────────────────────────
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x")

        self.copy_btn = tk.Button(
            btn_row, text="⎘  Copy", command=self._copy_result,
            bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_FAMILY, 10),
            relief="flat", padx=14, pady=6, cursor="hand2",
            activebackground=BORDER, activeforeground=TEXT_PRIMARY, bd=0
        )
        self.copy_btn.pack(side="left", padx=(0, 8))

        self.inject_btn = tk.Button(
            btn_row, text="↩  Inject into App", command=self._inject_result,
            bg=SUCCESS, fg="white", font=(FONT_FAMILY, 10, "bold"),
            relief="flat", padx=14, pady=6, cursor="hand2",
            activebackground="#059669", activeforeground="white", bd=0
        )
        self.inject_btn.pack(side="left")

        tk.Label(
            btn_row, text="Esc to close", bg=BG_CARD,
            fg=TEXT_MUTED, font=(FONT_FAMILY, 8)
        ).pack(side="right")

        # ── Set window size + center ──────────────────────────────────────────
        self.root.update_idletasks()
        w, h = 620, 520
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2 - 40
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.root.bind("<Escape>", lambda e: self.hide())

    # ── Drag callbacks ─────────────────────────────────────────────────────────
    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_motion(self, e):
        x = e.x_root - self._drag_x
        y = e.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    # ── Show / Hide ────────────────────────────────────────────────────────────
    def show(self):
        # Capture the previously focused window handle before we steal focus
        try:
            import ctypes
            self._prev_hwnd = ctypes.windll.user32.GetForegroundWindow()
        except Exception:
            self._prev_hwnd = None

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.input_box.focus_set()
        self.visible = True
        self._set_result("")
        self.status_var.set("")

    def hide(self):
        self.root.withdraw()
        self.visible = False

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    # ── Enter key in input → enhance ─────────────────────────────────────────
    def _on_enter(self, event):
        if not event.state & 0x1:    # Shift not held
            self._start_enhance()
            return "break"

    # ── Enhance pipeline ───────────────────────────────────────────────────────
    def _start_enhance(self):
        if self._enhancing:
            return
        raw = self.input_box.get("1.0", "end").strip()
        if not raw:
            self.status_var.set("⚠  Type a prompt first.")
            return
        self._enhancing = True
        self.enhance_btn.config(state="disabled", text="Enhancing…")
        self.status_var.set("⚙  Calling Groq via Jarvis backend…")
        self._set_result("")
        threading.Thread(target=self._call_backend, args=(raw,), daemon=True).start()

    def _call_backend(self, raw_prompt: str):
        try:
            resp = requests.post(
                BACKEND_URL,
                json={"prompt": f"enhance this prompt \"{raw_prompt}\""},
                stream=True,
                timeout=30
            )
            result_chunks = []
            for chunk in resp.iter_content(chunk_size=None):
                if chunk:
                    text = chunk.decode("utf-8", errors="ignore")
                    result_chunks.append(text)
                    self.root.after(0, self._append_result, text)
            self.root.after(0, self._enhance_done, "".join(result_chunks))
        except requests.exceptions.ConnectionError:
            self.root.after(0, self._enhance_error,
                "❌  Cannot reach Jarvis backend.\n"
                "Make sure uvicorn is running on http://127.0.0.1:8000"
            )
        except Exception as ex:
            self.root.after(0, self._enhance_error, f"❌  Error: {ex}")

    def _append_result(self, text: str):
        self.result_box.config(state="normal")
        self.result_box.insert("end", text)
        self.result_box.see("end")
        self.result_box.config(state="disabled")

    def _set_result(self, text: str):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        if text:
            self.result_box.insert("1.0", text)
        self.result_box.config(state="disabled")

    def _enhance_done(self, full_text: str):
        self._enhancing = False
        self.enhance_btn.config(state="normal", text="✦  Enhance")
        self.status_var.set("✓  Done. Click Copy or Inject.")
        # Auto-copy to clipboard
        clean = self._extract_prompt(full_text)
        pyperclip.copy(clean)

    def _enhance_error(self, msg: str):
        self._enhancing = False
        self.enhance_btn.config(state="normal", text="✦  Enhance")
        self.status_var.set(msg)

    def _extract_prompt(self, raw_output: str) -> str:
        """Strip the **ENHANCED PROMPT (CODING):** header if present."""
        lines = raw_output.strip().split("\n")
        # Remove the header line
        if lines and lines[0].strip().startswith("**ENHANCED PROMPT"):
            lines = lines[1:]
        return "\n".join(lines).strip()

    # ── Copy button ────────────────────────────────────────────────────────────
    def _copy_result(self):
        raw_out = self.result_box.get("1.0", "end").strip()
        clean   = self._extract_prompt(raw_out)
        pyperclip.copy(clean)
        orig = self.copy_btn["text"]
        self.copy_btn.config(text="✓  Copied!", bg=SUCCESS)
        self.root.after(1500, lambda: self.copy_btn.config(text=orig, bg=BG_INPUT))

    # ── Inject button ──────────────────────────────────────────────────────────
    def _inject_result(self):
        raw_out = self.result_box.get("1.0", "end").strip()
        if not raw_out:
            self.status_var.set("⚠  Nothing to inject yet.")
            return
        clean = self._extract_prompt(raw_out)
        pyperclip.copy(clean)

        self.hide()
        time.sleep(0.25)   # let the window close and focus return

        # Re-focus the previous window then paste
        try:
            if self._prev_hwnd:
                import ctypes
                ctypes.windll.user32.SetForegroundWindow(self._prev_hwnd)
                time.sleep(0.15)
        except Exception:
            pass

        pyautogui.hotkey("ctrl", "v")

    # ── Main loop ──────────────────────────────────────────────────────────────
    def run(self):
        self._build_window()

        def _hotkey_thread():
            keyboard.add_hotkey(HOTKEY, lambda: self.root.after(0, self.toggle))
            keyboard.wait()   # blocks forever — keeps listener alive

        t = threading.Thread(target=_hotkey_thread, daemon=True)
        t.start()

        print(f"[Jarvis Overlay] Running. Press {HOTKEY.upper()} to open.")
        self.root.mainloop()


# ── Entry point ─────────────────────────────────────────────────────────────────
def main():
    overlay = PromptOverlay()
    overlay.run()


if __name__ == "__main__":
    main()
