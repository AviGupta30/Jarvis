"""
storage.py — Persisting and retrieving replica documents.

Replica documents are stored at:
  app/memory/replica_docs/{document_id}.json

The document_id is derived from the SHA-1 hash of the reference image
(same key used by the legacy design cache).
"""

import os
import json
import time

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Resolve the project root: storage.py lives at
#   <root>/app/services/resume_replica/storage.py
# So we go up four levels: resume_replica -> services -> app -> root
_BASE_DIR = os.path.dirname(  # root
    os.path.dirname(           # app
        os.path.dirname(       # services
            os.path.dirname(   # resume_replica
                os.path.abspath(__file__)
            )
        )
    )
)
_REPLICA_DIR = os.path.join(_BASE_DIR, "app", "memory", "replica_docs")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _ensure_dir() -> None:
    """Creates the replica_docs directory if it does not already exist."""
    os.makedirs(_REPLICA_DIR, exist_ok=True)


def get_document_path(doc_id: str) -> str:
    """Returns the file path for a replica document."""
    return os.path.join(_REPLICA_DIR, f"{doc_id}.json")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def save_replica_document(doc: dict) -> str:
    """
    Saves the replica document to disk as a pretty-printed JSON file.
    Returns the absolute path where the document was saved.
    Raises ValueError if the doc is missing the required 'id' field.
    """
    doc_id = doc.get("id")
    if not doc_id:
        raise ValueError("Replica document must have a non-empty 'id' field.")

    _ensure_dir()
    path = get_document_path(doc_id)

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)

    return path


def load_replica_document(doc_id: str):
    """
    Loads a replica document by ID.
    Returns the parsed dict, or None if the file does not exist.
    """
    path = get_document_path(doc_id)
    if not os.path.isfile(path):
        return None

    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def has_replica_document(doc_id: str) -> bool:
    """Returns True if a replica document with this ID exists on disk."""
    return os.path.isfile(get_document_path(doc_id))


def delete_replica_document(doc_id: str) -> bool:
    """
    Deletes the replica document JSON file.
    Returns True if the file existed and was deleted, False otherwise.
    """
    path = get_document_path(doc_id)
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False


def list_replica_documents() -> list:
    """
    Returns a list of all stored document IDs (filenames without extension).
    The directory is created if it doesn't exist yet.
    """
    _ensure_dir()
    doc_ids = []
    for filename in os.listdir(_REPLICA_DIR):
        if filename.endswith(".json"):
            doc_ids.append(filename[:-5])  # strip ".json"
    return doc_ids


def prune_old_documents(keep_last: int = 20) -> list:
    """
    Deletes old replica documents, keeping only the `keep_last` most recently
    modified ones. Returns the list of document IDs that were deleted.
    """
    _ensure_dir()

    # Collect (mtime, doc_id) pairs for all existing documents
    entries = []
    for filename in os.listdir(_REPLICA_DIR):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(_REPLICA_DIR, filename)
        mtime = os.path.getmtime(path)
        doc_id = filename[:-5]
        entries.append((mtime, doc_id))

    if len(entries) <= keep_last:
        return []

    # Sort ascending by mtime so oldest are first
    entries.sort(key=lambda t: t[0])

    to_delete = entries[: len(entries) - keep_last]
    deleted_ids = []
    for _mtime, doc_id in to_delete:
        if delete_replica_document(doc_id):
            deleted_ids.append(doc_id)

    return deleted_ids
