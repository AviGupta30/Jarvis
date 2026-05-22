"""
Jarvis Arc Reactor Overlay
--------------------------
A floating, always-on-top, draggable window that shows the arc reactor image
and pulses/glows based on Jarvis's current state.

States (read from temp JSON file):
  idle       → dim slow pulse
  listening  → medium cyan pulse
  processing → fast purple pulse
  speaking   → rapid bright white-cyan flash
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFilter
import math, time, os, json, sys


# ── Shared state file (written by voice_agent.py, read here) ───────────────
STATE_FILE = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'jarvis_ui_state.json')


def read_state() -> str:
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f).get('state', 'idle')
    except Exception:
        return 'idle'


# ── Programmatic arc reactor fallback ──────────────────────────────────────
def generate_arc_reactor(size: int = 220) -> Image.Image:
    """Draws a beautiful arc reactor using PIL when no icon file is found."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Base dark circle
    draw.ellipse([0, 0, size - 1, size - 1], fill=(8, 12, 22, 255))

    # Outer metallic rings
    for offset, col, w in [(3, (0, 90, 130, 200), 1),
                           (6, (0, 130, 180, 220), 2),
                           (10, (0, 170, 220, 255), 3)]:
        r = size // 2 - offset
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)

    # 12 segments
    n, seg_in, seg_out = 12, int(size * 0.31), int(size * 0.44)
    gap = 5
    for i in range(n):
        a1 = math.radians(i * 30 + gap / 2)
        a2 = math.radians((i + 1) * 30 - gap / 2)
        pts = []
        for step in range(10):
            t = step / 9
            a = a1 + (a2 - a1) * t
            pts.append((cx + seg_out * math.cos(a), cy + seg_out * math.sin(a)))
        for step in range(9, -1, -1):
            t = step / 9
            a = a1 + (a2 - a1) * t
            pts.append((cx + seg_in * math.cos(a), cy + seg_in * math.sin(a)))
        bright = 150 + (i % 3) * 35
        draw.polygon(pts, fill=(0, bright, int(bright * 1.35), 210))
        draw.polygon(pts, outline=(0, 200, 255, 140), width=1)

    # Inner concentric rings
    for r, col, w in [(int(size * 0.27), (0, 185, 235, 255), 2),
                      (int(size * 0.20), (20, 205, 248, 255), 2),
                      (int(size * 0.13), (60, 220, 255, 255), 3)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)

    # Center glow layers
    for r, col in [(int(size * 0.11), (0, 155, 225, 170)),
                   (int(size * 0.08), (45, 185, 245, 215)),
                   (int(size * 0.05), (110, 225, 255, 240)),
                   (int(size * 0.03), (210, 245, 255, 255))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # Soft glow blur blend
    blurred = img.filter(ImageFilter.GaussianBlur(2))
    return Image.blend(blurred, img, 0.65)


# ── Overlay window ──────────────────────────────────────────────────────────
class JarvisOverlay:
    W = H = 220  # canvas size

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis")
        self.root.overrideredirect(True)           # no title bar
        self.root.attributes('-topmost', True)     # always on top
        self.root.wm_attributes('-transparentcolor', '#010203')
        self.root.configure(bg='#010203')

        # Initial position: bottom-right corner
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f'{self.W}x{self.H + 30}+{sw - self.W - 24}+{sh - self.H - 80}')

        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H + 30,
                                bg='#010203', highlightthickness=0)
        self.canvas.pack()

        # Load image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'jarvis_icon.png')
        if os.path.exists(icon_path):
            self.base = Image.open(icon_path).convert('RGBA').resize((self.W, self.H), Image.LANCZOS)
            print(f"[Overlay] Loaded icon from {icon_path}")
        else:
            self.base = generate_arc_reactor(self.W)
            print("[Overlay] Using generated arc reactor (place jarvis_icon.png to use your image)")

        cx = self.W // 2
        self.img_item    = self.canvas.create_image(cx, self.H // 2, anchor='center')
        self.status_item = self.canvas.create_text(cx, self.H + 16,
                                                   text="● JARVIS  READY",
                                                   fill="#005599",
                                                   font=("Consolas", 9, "bold"))

        # Drag bindings
        self.canvas.bind('<Button-1>', self._drag_start)
        self.canvas.bind('<B1-Motion>', self._drag_move)
        self._dx = self._dy = 0

        # Double-click to toggle minimize/restore
        self.canvas.bind('<Double-Button-1>', self._toggle_minimize)
        self._minimized = False

        self._t = 0.0
        self._photo = None
        self._last_state = 'idle'
        self.animate()

    # ── Drag ──────────────────────────────────────────────────────────────
    def _drag_start(self, e):
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        self.root.geometry(f'+{e.x_root - self._dx}+{e.y_root - self._dy}')

    def _toggle_minimize(self, e):
        if self._minimized:
            self.root.deiconify()
            self._minimized = False
        else:
            self.root.withdraw()
            self._minimized = True

    # ── Animation ─────────────────────────────────────────────────────────
    def animate(self):
        self._t += 0.12
        state = read_state()

        if state == 'speaking':
            b     = 0.85 + 0.85 * abs(math.sin(self._t * 5.5))
            text  = "◉  SPEAKING..."
            color = "#00ffff"
        elif state == 'working':
            b     = 0.60 + 0.70 * abs(math.sin(self._t * 4.0))
            text  = f"◗  WORKING{'.' * (1 + int(self._t * 1.5) % 3)}"
            color = "#ffaa00"
        elif state == 'listening':
            b     = 0.55 + 0.45 * abs(math.sin(self._t * 2.2))
            text  = "◎  LISTENING..."
            color = "#00bbff"
        elif state == 'processing':
            b     = 0.50 + 0.60 * abs(math.sin(self._t * 3.8))
            text  = "◈  THINKING..."
            color = "#bb88ff"
        else:   # idle
            b     = 0.25 + 0.10 * abs(math.sin(self._t * 0.9))
            text  = "●  JARVIS  READY"
            color = "#004488"

        enhanced = ImageEnhance.Brightness(self.base).enhance(b)
        self._photo = ImageTk.PhotoImage(enhanced)
        self.canvas.itemconfig(self.img_item, image=self._photo)
        self.canvas.itemconfig(self.status_item, text=text, fill=color)
        self.root.after(70, self.animate)   # ~14 fps

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    JarvisOverlay().run()
