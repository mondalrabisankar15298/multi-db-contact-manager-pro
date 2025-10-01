"""
Application startup preflight:
- Tests connectivity for all supported databases
- Writes health results to local tracker (data/app_state.db)
- Chooses a database to use for this session
- Exports DB_TYPE in os.environ so downstream modules pick it up
"""

import os
from typing import Dict, List, Tuple

from database.factory import DatabaseFactory
from state_tracker import (
    ensure_schema,
    get_last_db_type,
    set_last_db_type,
    set_db_health,
    get_db_health_map,
)
from config.settings import settings


def _test_db(db_type: str) -> Tuple[bool, str]:
    """Return (is_healthy, details)."""
    try:
        # Leverage adapter's own connection test for accuracy
        DatabaseFactory.create_with_test(db_type)
        return True, "ok"
    except Exception as exc:  # Broad by design; we need to record any failure
        return False, str(exc)


def _choose_db(available: List[str], health: Dict[str, int]) -> str:
    """Choose a database for this session based on priority rules.
    Priority:
    1) DB_TYPE env (if healthy)
    2) Last used from tracker (if healthy)
    3) 'sqlite'
    """
    explicit = os.environ.get("DB_TYPE", "").strip()
    if explicit and health.get(explicit) == 1:
        return explicit

    last = get_last_db_type()
    if last and health.get(last) == 1:
        return last

    return "sqlite"


def run_preflight_and_choose_db(verbose: bool = False) -> Tuple[str, Dict[str, int]]:
    """Run preflight checks, persist results, choose DB, and export DB_TYPE.

    Returns:
        (chosen_db_type, health_map)
    """
    ensure_schema()

    available = list(DatabaseFactory.get_available_types())

    for db_type in available:
        ok, details = _test_db(db_type)
        set_db_health(db_type, ok, details)
        if verbose:
            status = "healthy" if ok else "unhealthy"
            print(f"[preflight] {db_type}: {status} ({details if not ok else 'ok'})")

    health_map = get_db_health_map()
    chosen = _choose_db(available, health_map)

    # Export for this process and persist as last used
    os.environ["DB_TYPE"] = chosen
    # Also update live settings in case it was already imported elsewhere
    try:
        settings.set_default_database_type(chosen)
    except Exception:
        pass
    set_last_db_type(chosen)

    # Ensure the global database manager reflects the selection immediately
    try:
        from database.manager import db_manager
        # Only switch if different to avoid unnecessary reconnect
        if getattr(db_manager, 'current_db_type', None) != chosen:
            db_manager.switch_database(chosen)
    except Exception:
        # Best-effort; the manager may be imported later
        pass

    if verbose:
        print(f"[preflight] chosen DB_TYPE: {chosen}")

    return chosen, health_map


