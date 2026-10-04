"""
resume_replica — Scene-graph-based resume replication engine.
Import the public API:
    from app.services.resume_replica import build_replica, compile_replica_html
"""
from .orchestrator import build_replica, compile_replica_html
from .schema import SCHEMA_VERSION

__all__ = ["build_replica", "compile_replica_html", "SCHEMA_VERSION"]
