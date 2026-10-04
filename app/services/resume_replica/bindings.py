"""
bindings.py — Content binding resolution and editor path mapping.

Binding paths use dot notation:
  'name'                       -> content['name']
  'title'                      -> content['title']
  'contact.email'              -> content['contact']['email']
  'section_titles.experience'  -> content['section_titles']['experience']
  'experience'                 -> content['experience'] (full list)
  'experience.0.role'          -> content['experience'][0]['role']
  'skills'                     -> content['skills'] (full list)
"""

from .schema import SECTION_KEYS, NODE_TEXT, NODE_REPEAT, NODE_CHART, walk_nodes

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_TITLES = {
    "profile":        "Profile",
    "highlights":     "Career Highlights",
    "contact":        "Contact",
    "skills":         "Skills",
    "competencies":   "Core Competencies",
    "experience":     "Work Experience",
    "education":      "Education",
    "achievements":   "Achievements",
    "certifications": "Certifications",
    "languages":      "Languages",
    "interests":      "Interests",
    "projects":       "Projects",
    "references":     "References",
}

# Keys whose top-level value is expected to be a list of items
_LIST_SECTION_KEYS = {
    "experience", "education", "skills", "projects",
    "languages", "achievements", "certifications",
    "highlights", "interests", "references", "competencies",
}

# ---------------------------------------------------------------------------
# Core binding resolution
# ---------------------------------------------------------------------------

def resolve_binding(content: dict, path: str):
    """
    Resolves a binding path against content dict.
    Returns the value at that path, or empty string / empty list as appropriate.

    For list paths (e.g. 'experience'), returns the full list.
    For scalar paths, returns the raw value (str, int, etc.) or ''.
    """
    if not path or not isinstance(content, dict):
        return ""

    parts = path.split(".")
    current = content

    for part in parts:
        if current is None:
            break
        if isinstance(current, list):
            try:
                idx = int(part)
                current = current[idx] if 0 <= idx < len(current) else None
            except ValueError:
                current = None
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            current = None

    if current is None:
        # Return an appropriate empty value depending on top-level key
        top_key = parts[0] if parts else ""
        if top_key in _LIST_SECTION_KEYS and len(parts) == 1:
            return []
        return ""

    return current


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_binding_value(value, content: dict, path: str) -> str:
    """
    Converts a resolved binding value to a display string.

    - None / empty string / empty list -> ''
    - list -> not applicable, caller handles lists separately; returns ''
    - Other -> str(value)
    """
    if value is None:
        return ""
    if isinstance(value, list):
        # Lists are rendered by REPEAT nodes, not as a flat string.
        return ""
    if isinstance(value, str):
        return value
    return str(value)


# ---------------------------------------------------------------------------
# Editor path map
# ---------------------------------------------------------------------------

def build_editor_path_map(scene_graph: dict) -> dict:
    """
    Walks the scene graph and builds a map from binding path -> list of node IDs
    that reference that path. Used by the editor to know which nodes to update
    when a field is edited.

    Returns: {"name": ["header_name_text"], "experience": ["experience_repeat"], ...}
    """
    path_map: dict = {}

    def _visitor(node, parent, depth):
        binding = node.get("binding")
        if not binding:
            return
        node_id = node.get("id", "")
        if not node_id:
            return
        if binding not in path_map:
            path_map[binding] = []
        if node_id not in path_map[binding]:
            path_map[binding].append(node_id)

    walk_nodes(scene_graph, _visitor)
    return path_map


# ---------------------------------------------------------------------------
# Repeat iteration
# ---------------------------------------------------------------------------

def iter_content_items(content: dict, binding: str):
    """
    Iterator for repeat bindings. Yields (index, item) for each item in the
    list at content[binding].

    Handles: experience, education, skills, projects, languages, achievements,
    certifications, highlights, interests, references, competencies.
    """
    items = content.get(binding)
    if not isinstance(items, list):
        return
    for idx, item in enumerate(items):
        yield idx, item


# ---------------------------------------------------------------------------
# Section title helper
# ---------------------------------------------------------------------------

def section_title(content: dict, key: str) -> str:
    """
    Returns the display title for a section, checking content['section_titles']
    first, then falling back to DEFAULT_TITLES.
    """
    section_titles = content.get("section_titles")
    if isinstance(section_titles, dict):
        title = section_titles.get(key)
        if title:
            return str(title)
    return DEFAULT_TITLES.get(key, key.replace("_", " ").title())
