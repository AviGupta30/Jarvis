import re

with open(r'c:\Users\avi40\Desktop\Jarvis\app\services\ppt_chart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

# _render_bar
code = re.sub(
    r'def _render_bar\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, ax = plt\.subplots\(figsize=\(7, max\(3\.2, n \* 0\.7\)\)\)',
    r'def _render_bar(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else 7\n    fig_h = h if h else max(3.2, n * 0.7)\n    fig, ax = plt.subplots(figsize=(fig_w, fig_h))',
    code
)

# _render_pie
code = re.sub(
    r'def _render_pie\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, ax = plt\.subplots\(figsize=\(6, 5\)\)',
    r'def _render_pie(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else 6\n    fig_h = h if h else 5\n    fig, ax = plt.subplots(figsize=(fig_w, fig_h))',
    code
)

# _render_line
code = re.sub(
    r'def _render_line\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, ax = plt\.subplots\(figsize=\(7, 4\)\)',
    r'def _render_line(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else 7\n    fig_h = h if h else 4\n    fig, ax = plt.subplots(figsize=(fig_w, fig_h))',
    code
)

# _render_comparison
code = re.sub(
    r'def _render_comparison\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, ax = plt\.subplots\(figsize=\(11, max\(3\.0, n \* 0\.65\)\)\)',
    r'def _render_comparison(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else 11\n    fig_h = h if h else max(3.0, n * 0.65)\n    fig, ax = plt.subplots(figsize=(fig_w, fig_h))',
    code
)

# _render_metrics_dashboard
code = re.sub(
    r'def _render_metrics_dashboard\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, axes = plt\.subplots\(rows, cols, figsize=\(cols \* 2\.8, rows \* 2\.2\)\)',
    r'def _render_metrics_dashboard(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else (cols * 2.8)\n    fig_h = h if h else (rows * 2.2)\n    fig, axes = plt.subplots(rows, cols, figsize=(fig_w, fig_h))',
    code
)

# _render_timeline
code = re.sub(
    r'def _render_timeline\(data: dict, palette: dict\) -> bytes:\n([\s\S]*?)fig, ax = plt\.subplots\(figsize=\(max\(8, n \* 1\.8\), 3\.5\)\)',
    r'def _render_timeline(data: dict, palette: dict, w: float=None, h: float=None) -> bytes:\n\1fig_w = w if w else max(8, n * 1.8)\n    fig_h = h if h else 3.5\n    fig, ax = plt.subplots(figsize=(fig_w, fig_h))',
    code
)

# _RENDERERS
code = re.sub(
    r'"vertical_bar":\s*lambda d, p: _render_bar\(\{\*\*d, "orientation": "vertical"\}, p\),',
    r'"vertical_bar":   lambda d, p, w=None, h=None: _render_bar({**d, "orientation": "vertical"}, p, w, h),',
    code
)

# ChartEngine.render signature
code = re.sub(
    r'def render\(chart_data: dict, palette: dict\) -> Optional\[bytes\]:',
    r'def render(chart_data: dict, palette: dict, w: float=None, h: float=None) -> Optional[bytes]:',
    code
)

# renderer call
code = re.sub(
    r'result = renderer\(chart_data, palette\)',
    r'result = renderer(chart_data, palette, w, h)',
    code
)

with open(r'c:\Users\avi40\Desktop\Jarvis\app\services\ppt_chart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched ppt_chart_engine.py")
