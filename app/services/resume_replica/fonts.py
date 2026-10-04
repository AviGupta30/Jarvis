"""
fonts.py — Local font library + font identification for exact resume replication.

Library: the most popular Google Fonts families (latin subset, every weight 300-900 they have) are downloaded
once into data/fonts/gf/ (index.json), plus the Windows system fonts that are installed. Drop extra .ttf/.otf/.woff2
files into data/fonts/user/ (file name = family name, optional "-700" weight suffix) to make a paid font exact.

Identification lives in fontmatch.py.
"""
from __future__ import annotations

import json
import os
import re
import threading

import numpy as np

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FONT_DIR = os.path.join(_BASE, "data", "fonts")
GF_DIR = os.path.join(FONT_DIR, "gf")
USER_DIR = os.path.join(FONT_DIR, "user")
INDEX = os.path.join(GF_DIR, "index.json")
FONT_ORIGIN = "https://rfonts.local/"          # served from disk via Playwright routing (no CORS issues)

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
       "Chrome/124.0 Safari/537.36")
_WEIGHTS = (300, 400, 500, 600, 700, 800, 900)
TOP_N = 450                                      # most popular families
# Always included (common in resume templates even when not in the top N)
_FAVOURITES = [
    "Montserrat", "Poppins", "Open Sans", "Lato", "Roboto", "Raleway", "Inter", "Nunito", "Nunito Sans",
    "Source Sans 3", "Work Sans", "Rubik", "Manrope", "DM Sans", "Josefin Sans", "Quicksand", "Ubuntu", "Oswald",
    "Bebas Neue", "Anton", "League Spartan", "Archivo", "Barlow", "Cabin", "Fira Sans", "Heebo", "Hind", "IBM Plex Sans",
    "Karla", "Kanit", "Libre Franklin", "Mukta", "Mulish", "Noto Sans", "PT Sans", "Questrial", "Red Hat Display",
    "Sora", "Space Grotesk", "Titillium Web", "Varela Round", "Lexend", "Outfit", "Plus Jakarta Sans", "Urbanist",
    "Figtree", "Jost", "Saira", "Comfortaa", "Didact Gothic", "Tenor Sans", "Glacial Indifference", "League Gothic",
    "Merriweather", "Playfair Display", "Lora", "Cormorant Garamond", "Cormorant", "EB Garamond", "PT Serif",
    "Libre Baskerville", "Crimson Text", "Noto Serif", "Source Serif 4", "Roboto Slab", "Arvo", "Bitter", "Alegreya",
    "Cinzel", "Abril Fatface", "DM Serif Display", "Prata", "Spectral", "Gilda Display", "Marcellus", "Alice",
    "Josefin Slab", "Zilla Slab", "Archivo Black", "Righteous", "Dancing Script", "Great Vibes", "Pacifico", "Allura",
    "Parisienne", "Sacramento", "Alex Brush", "Pinyon Script", "JetBrains Mono", "Roboto Mono", "Space Mono",
    "Courier Prime", "Source Code Pro", "Arimo", "Tinos", "Cousine", "Carlito", "Caladea", "Gelasio", "Open Sans Condensed",
    "Roboto Condensed", "Barlow Condensed", "Fjalla One", "Teko", "Yanone Kaffeesatz", "Exo 2", "Orbitron",
    "Abel", "Assistant", "Catamaran", "Encode Sans", "Maven Pro", "Oxygen", "Prompt", "Signika", "Play", "Asap",
]
# Installed Windows fonts worth testing (only kept if actually installed — checked in the browser)
SYSTEM_FONTS = [
    "Arial", "Arial Narrow", "Arial Black", "Calibri", "Calibri Light", "Cambria", "Candara", "Century Gothic",
    "Consolas", "Constantia", "Corbel", "Franklin Gothic Medium", "Garamond", "Georgia", "Gill Sans MT",
    "Segoe UI", "Segoe UI Light", "Segoe UI Semibold", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana",
    "Book Antiqua", "Palatino Linotype", "Bahnschrift", "Lucida Sans Unicode", "Aptos", "Aptos Display",
    "Century Schoolbook", "Bookman Old Style", "Rockwell", "Tw Cen MT", "Gadugi", "Leelawadee UI", "Ebrima",
    "Sitka Text", "Sitka Heading", "Microsoft Sans Serif", "Courier New", "Lucida Console",
]

_lock = threading.Lock()


# ── Library ────────────────────────────────────────────────────────────────────────────────────────

def _slug(family: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", family.lower()).strip("_")


def load_index() -> dict:
    """{family: {"category": str, "weights": {weight: relative file}}} (Google + user fonts)."""
    idx = {}
    try:
        with open(INDEX, encoding="utf-8") as f:
            idx = json.load(f)
    except Exception:
        idx = {}
    if os.path.isdir(USER_DIR):
        for fn in os.listdir(USER_DIR):
            m = re.match(r"(.+?)(?:-(\d{3}))?\.(ttf|otf|woff2?|TTF|OTF)$", fn)
            if not m:
                continue
            fam = m.group(1).replace("_", " ").strip()
            w = m.group(2) or "400"
            idx.setdefault(fam, {"category": "user", "weights": {}, "user": True})["weights"][w] = "../user/" + fn
    return idx


def ensure_library(top_n: int = TOP_N, log=print) -> dict:
    """Downloads (once) the latin woff2 files of the popular families. Safe to call repeatedly; only missing
    families are fetched. Returns the index."""
    import requests
    with _lock:
        os.makedirs(GF_DIR, exist_ok=True)
        os.makedirs(USER_DIR, exist_ok=True)
        try:
            with open(INDEX, encoding="utf-8") as f:
                idx = json.load(f)
        except Exception:
            idx = {}
        try:
            r = requests.get("https://fonts.google.com/metadata/fonts", timeout=40)
            txt = r.text[r.text.index("{"):]
            meta = json.loads(txt)["familyMetadataList"]
        except Exception as e:
            log(f"[fonts] metadata unavailable ({e}); using {len(idx)} cached families")
            return load_index()
        latin = [m for m in meta if "latin" in (m.get("subsets") or [])
                 and not re.search(r"icons|symbols|emoji", m["family"], re.I)]
        latin.sort(key=lambda m: m.get("popularity") or 99999)
        wanted = [m for m in latin[:top_n]]
        names = {m["family"] for m in wanted}
        wanted += [m for m in latin if m["family"] in _FAVOURITES and m["family"] not in names]
        todo = [m for m in wanted if m["family"] not in idx]
        log(f"[fonts] {len(wanted)} families wanted, {len(todo)} to download")
        sess = requests.Session()
        sess.headers["User-Agent"] = _UA
        for i, m in enumerate(todo):
            fam = m["family"]
            weights = sorted({int(k) for k in (m.get("fonts") or {}) if k.isdigit() and int(k) in _WEIGHTS})
            if not weights:
                continue
            spec = fam.replace(" ", "+") + (":wght@" + ";".join(map(str, weights)) if weights != [400] else "")
            try:
                css = sess.get(f"https://fonts.googleapis.com/css2?family={spec}&display=swap", timeout=20).text
                files = {}
                for block in re.finditer(r"/\*\s*latin\s*\*/\s*@font-face\s*{([^}]*)}", css):
                    body = block.group(1)
                    if "font-style: normal" not in body:
                        continue
                    w = re.search(r"font-weight:\s*(\d+)", body).group(1)
                    url = re.search(r"url\((https://[^)]+)\)", body).group(1)
                    fn = f"{_slug(fam)}_{w}.woff2"
                    path = os.path.join(GF_DIR, fn)
                    if not os.path.exists(path):
                        data = sess.get(url, timeout=20).content
                        with open(path, "wb") as f:
                            f.write(data)
                    files[w] = fn
                if files:
                    idx[fam] = {"category": m.get("category", ""), "weights": files,
                                "popularity": m.get("popularity")}
            except Exception as e:
                log(f"[fonts] {fam}: {e}")
            if i % 25 == 24:
                with open(INDEX, "w", encoding="utf-8") as f:
                    json.dump(idx, f)
                log(f"[fonts] {i + 1}/{len(todo)}")
        with open(INDEX, "w", encoding="utf-8") as f:
            json.dump(idx, f)
        return load_index()


def font_face_css(families: dict | None = None, origin: str = FONT_ORIGIN) -> str:
    """@font-face rules for the given {family: [weights]} (default: the whole library) served from `origin`."""
    idx = load_index()
    out = []
    for fam, info in idx.items():
        if families is not None and fam not in families:
            continue
        for w, fn in info["weights"].items():
            if families is not None and families[fam] and int(w) not in families[fam]:
                continue
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                       f"src:url('{origin}{fn}')}}")
    return "\n".join(out)


def embed_css(families: dict) -> str:
    """@font-face rules with the font files inlined (base64) — for the final resume HTML/PDF (works offline)."""
    import base64
    idx = load_index()
    out = []
    for fam, weights in families.items():
        info = idx.get(fam)
        if not info:
            continue                                     # system font: nothing to embed
        avail = sorted(int(w) for w in info["weights"])
        for w in sorted(set(weights or avail)):
            ww = min(avail, key=lambda a: abs(a - w))
            path = os.path.normpath(os.path.join(GF_DIR, info["weights"][str(ww)]))
            try:
                with open(path, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
            except Exception:
                continue
            ext = os.path.splitext(path)[1].lower()
            fmt = {".woff2": "woff2", ".woff": "woff", ".otf": "opentype"}.get(ext, "truetype")
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                       f"src:url(data:font/{fmt};base64,{data}) format('{fmt}')}}")
    return "\n".join(out)


def route_fonts(page) -> None:
    """Serve the font library at FONT_ORIGIN for this Playwright page."""
    def handler(route):
        name = route.request.url[len(FONT_ORIGIN):].split("?")[0]
        path = os.path.normpath(os.path.join(GF_DIR, name))
        if not path.startswith(os.path.normpath(FONT_DIR)) or not os.path.exists(path):
            return route.fulfill(status=404, body="")
        ext = os.path.splitext(path)[1].lower()
        ctype = {".woff2": "font/woff2", ".woff": "font/woff", ".otf": "font/otf"}.get(ext, "font/ttf")
        with open(path, "rb") as f:
            route.fulfill(status=200, body=f.read(), headers={"Content-Type": ctype,
                                                              "Access-Control-Allow-Origin": "*"})
    page.route(FONT_ORIGIN + "**", handler)


if __name__ == "__main__":
    ensure_library()
