import re

with open('app/api/chat.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = '''        if pos or w_pct or h_pct:
            args = {"position": pos, "width_percent": w_pct, "height_percent": h_pct}
            # Clean up the extracted app name (strip filler words like "the", "my", "current")
            clean_app = None
            if raw_app:
                filler = {'the', 'my', 'current', 'a', 'an', 'this', 'that', 'tab', 'window', 'screen'}
                clean_app = ' '.join(w for w in raw_app.lower().split() if w not in filler).strip()
                if clean_app in ('', 'it'):
                    clean_app = None
            if clean_app:
                args["app_name"] = clean_app
            return {"tool_name": "adjust_active_window", "arguments": args}'''

good = '''        # Must have found EITHER a position or a percentage
        if not pos and not (w_pct or h_pct):
            return None

        # ── Step 5: Extract app name ──────────────────────────────────────
        # Remove all words that are NOT the app name
        _STRIP_WORDS = {
            # Layout verbs
            'adjust', 'move', 'set', 'resize', 'snap', 'put', 'place', 'pin',
            'tile', 'shift', 'tune', 'bring', 'send', 'dock', 'push', 'slide',
            'position', 'in', 'into',
            # Articles / pronouns
            'the', 'my', 'a', 'an', 'this', 'that', 'it', 'its',
            # Layout nouns
            'screen', 'tab', 'window', 'current', 'active',
            # Connectors
            'of', 'to', 'at', 'for', 'from', 'on', 'with', 'and', 'or', 'is', 'be',
            # Direction words
            'upper', 'lower', 'top', 'bottom', 'left', 'right',
            'center', 'centre', 'middle',
            # Filler
            'please', 'jarvis', 'ok', 'okay', 'now', 'just',
            # Orientation helpers
            'horizontally', 'horizontal', 'vertically', 'vertical',
            'width', 'height', 'percent', 'percentage',
        }

        # Remove percentage tokens from text first
        clean = re.sub(r'\\d+\\s*%', '', t)
        # Tokenise and filter
        tokens = re.split(r'[\\s,\\.!?]+', clean)
        app_tokens = []
        for tok in tokens:
            tok_clean = tok.strip().lower()
            if not tok_clean:
                continue
            # Skip pure position phrases already captured
            if tok_clean in _STRIP_WORDS:
                continue
            # Skip numeric-only tokens
            if re.match(r'^\\d+$', tok_clean):
                continue
            app_tokens.append(tok)

        app_name = ' '.join(app_tokens).strip()
        # Reject very short or clearly non-app leftovers
        if len(app_name) <= 1 or app_name.lower() in ('', 'it', 'i', 'up', 'out'):
            app_name = None

        result = {"position": pos, "width_percent": w_pct, "height_percent": h_pct}
        if app_name:
            result["app_name"] = app_name
        return result

    _adj = _semantic_window_adjust(lower)
    if _adj is not None:
        return {"tool_name": "adjust_active_window", "arguments": _adj}'''

if bad in text:
    text = text.replace(bad, good)
    with open('app/api/chat.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Could not find bad block!")
