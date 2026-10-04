# storage

> 16 nodes · cohesion 0.18

## Key Concepts

- **storage.py** (12 connections) — `app/services/resume_replica/storage.py`
- **get_document_path()** (6 connections) — `app/services/resume_replica/storage.py`
- **save_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **_ensure_dir()** (5 connections) — `app/services/resume_replica/storage.py`
- **has_replica_document()** (5 connections) — `app/services/resume_replica/storage.py`
- **delete_replica_document()** (4 connections) — `app/services/resume_replica/storage.py`
- **prune_old_documents()** (4 connections) — `app/services/resume_replica/storage.py`
- **list_replica_documents()** (3 connections) — `app/services/resume_replica/storage.py`
- **storage.py — Persisting and retrieving replica documents. Replica documents are…** (1 connections) — `app/services/resume_replica/storage.py`
- **Returns a list of all stored document IDs (filenames without extension). The…** (1 connections) — `app/services/resume_replica/storage.py`
- **Deletes old replica documents, keeping only the `keep_last` most recently…** (1 connections) — `app/services/resume_replica/storage.py`
- **Creates the replica_docs directory if it does not already exist.** (1 connections) — `app/services/resume_replica/storage.py`
- **Returns the file path for a replica document.** (1 connections) — `app/services/resume_replica/storage.py`
- **Saves the replica document to disk as a pretty-printed JSON file. Returns the…** (1 connections) — `app/services/resume_replica/storage.py`
- **Returns True if a replica document with this ID exists on disk.** (1 connections) — `app/services/resume_replica/storage.py`
- **Deletes the replica document JSON file. Returns True if the file existed and…** (1 connections) — `app/services/resume_replica/storage.py`

## Relationships

- [orchestrator + renderer](orchestrator_+_renderer.md) (6 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/storage.py`

## Audit Trail

- EXTRACTED: 31 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*