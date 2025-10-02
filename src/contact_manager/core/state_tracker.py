"""
Local state tracker using SQLite to persist:
- last used database type
- per-database health status

This file is intentionally lightweight and self-contained so it can be
imported early in the application lifecycle without pulling in heavy
dependencies or causing circular imports.
"""

import os
import sqlite3
from typing import Dict, Optional


def _get_db_path() -> str:
    """Resolve the tracker database path, defaulting to data/app_state.db."""
    default_path = os.path.join("data", "app_state.db")
    return os.environ.get("APP_STATE_DB_PATH", default_path)


def _ensure_parent_dir(path: str) -> None:
    parent_dir = os.path.dirname(os.path.abspath(path))
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)


def _connect() -> sqlite3.Connection:
    db_path = _get_db_path()
    _ensure_parent_dir(db_path)
    conn = sqlite3.connect(db_path)
    return conn


def ensure_schema() -> None:
    """Create required tables if they do not exist."""
    conn = _connect()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS db_health (
                db_type TEXT PRIMARY KEY,
                is_healthy INTEGER NOT NULL,
                details TEXT,
                checked_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def set_last_db_type(db_type: str) -> None:
    """Persist the last-used database type."""
    ensure_schema()
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO app_state(key, value, updated_at) VALUES('last_db_type', ?, datetime('now'))",
            (db_type,),
        )
        conn.commit()
    finally:
        conn.close()


def get_last_db_type() -> Optional[str]:
    """Return the last-used database type, if any."""
    ensure_schema()
    conn = _connect()
    try:
        cur = conn.execute("SELECT value FROM app_state WHERE key='last_db_type' LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def set_db_health(db_type: str, is_healthy: bool, details: str = "ok") -> None:
    """Upsert a health record for a given database type."""
    ensure_schema()
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT OR REPLACE INTO db_health(db_type, is_healthy, details, checked_at)
            VALUES(?, ?, ?, datetime('now'))
            """,
            (db_type, 1 if is_healthy else 0, details),
        )
        conn.commit()
    finally:
        conn.close()


def get_db_health_map() -> Dict[str, int]:
    """Return a mapping of db_type -> is_healthy (1/0)."""
    ensure_schema()
    conn = _connect()
    try:
        cur = conn.execute("SELECT db_type, is_healthy FROM db_health")
        rows = cur.fetchall()
        return {db_type: int(is_healthy) for db_type, is_healthy in rows}
    finally:
        conn.close()


def get_db_health_details() -> Dict[str, str]:
    """Return a mapping of db_type -> details string."""
    ensure_schema()
    conn = _connect()
    try:
        cur = conn.execute("SELECT db_type, details FROM db_health")
        rows = cur.fetchall()
        return {db_type: (details or "") for db_type, details in rows}
    finally:
        conn.close()




