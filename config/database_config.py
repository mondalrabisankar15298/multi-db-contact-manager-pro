"""
Database configuration settings for all supported database types.
"""

import os
from typing import Dict, Any

# Load environment variables from env files when running locally (outside Docker)
try:
    from dotenv import load_dotenv  # type: ignore
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _DOCKER_ENV_PATH = os.path.join(_PROJECT_ROOT, 'docker.env')
    _DOTENV_PATH = os.path.join(_PROJECT_ROOT, '.env')
    # Load docker.env first, then .env (later files do not override earlier by default)
    if os.path.exists(_DOCKER_ENV_PATH):
        load_dotenv(_DOCKER_ENV_PATH)
    if os.path.exists(_DOTENV_PATH):
        load_dotenv(_DOTENV_PATH)
except Exception:
    # Safe fallback if python-dotenv is not available or any error occurs
    pass

# Load environment variables
def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default value."""
    return os.environ.get(key, default)

# Database configurations for all supported types
DATABASE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "sqlite": {
        "path": get_env("SQLITE_PATH", "data/contacts.db"),
        "description": "SQLite (File-based, No server required)"
    },
    
    "mysql": {
        "host": get_env("MYSQL_HOST", "localhost"),
        "port": int(get_env("MYSQL_PORT", "3306")),
        "user": get_env("MYSQL_USER", "contact_user"),
        "password": get_env("MYSQL_PASSWORD", "contact_password"),
        "database": get_env("MYSQL_DATABASE", "contacts"),
        "charset": "utf8mb4",
        "description": "MySQL (Relational database)"
    },
    
    "postgres": {
        "host": get_env("POSTGRES_HOST", "localhost"),
        "port": int(get_env("POSTGRES_PORT", "5433")),  # Fixed: Docker uses 5433
        "user": get_env("POSTGRES_USER", "contact_user"),
        "password": get_env("POSTGRES_PASSWORD", "contact_password"),
        "database": get_env("POSTGRES_DATABASE", "contacts"),
        "description": "PostgreSQL (Advanced relational database)"
    },
    
    "mongodb": {
        "host": get_env("MONGO_HOST", "localhost"),
        "port": int(get_env("MONGO_PORT", "27017")),
        "user": get_env("MONGO_USER", ""),  # No auth by default in Docker
        "password": get_env("MONGO_PASSWORD", ""),  # No auth by default in Docker
        "database": get_env("MONGO_DATABASE", "contacts"),
        "auth_database": get_env("MONGO_AUTH_DATABASE", "admin"),
        "collection": "contacts",
        "description": "MongoDB (Document-based NoSQL)"
    }
}

# Database display information for menus
DATABASE_MENU_INFO = {
    "sqlite": {
        "emoji": "💾",
        "name": "SQLite",
        "subtitle": "Local file database"
    },
    "mysql": {
        "emoji": "🐬",
        "name": "MySQL",
        "subtitle": "Popular relational database"
    },
    "postgres": {
        "emoji": "🐘",
        "name": "PostgreSQL",
        "subtitle": "Advanced relational database"
    },
    "mongodb": {
        "emoji": "🍃",
        "name": "MongoDB",
        "subtitle": "Document-based NoSQL"
    }
}

def get_database_config(db_type: str) -> Dict[str, Any]:
    """Get configuration for a specific database type."""
    if db_type not in DATABASE_CONFIGS:
        raise ValueError(f"Unsupported database type: {db_type}")
    return DATABASE_CONFIGS[db_type].copy()

def get_available_databases() -> list:
    """Get list of available database types."""
    return list(DATABASE_CONFIGS.keys())

def get_database_display_info(db_type: str) -> Dict[str, str]:
    """Get display information for a database type."""
    if db_type not in DATABASE_MENU_INFO:
        return {"emoji": "🗄️", "name": db_type.upper(), "subtitle": "Database"}
    return DATABASE_MENU_INFO[db_type].copy()
