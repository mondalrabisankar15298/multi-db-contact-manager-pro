"""
Database configuration settings for all supported database types.
"""

import os
from typing import Dict, Any

# Load environment variables
def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default value."""
    return os.environ.get(key, default)

# Database configurations for all supported types
DATABASE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "sqlite": {
        "path": get_env("SQLITE_PATH", "contacts.db"),
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
        "port": int(get_env("POSTGRES_PORT", "5432")),
        "user": get_env("POSTGRES_USER", "contact_user"),
        "password": get_env("POSTGRES_PASSWORD", "contact_password"),
        "database": get_env("POSTGRES_DATABASE", "contacts"),
        "description": "PostgreSQL (Advanced relational database)"
    },
    
    "mongodb": {
        "host": get_env("MONGO_HOST", "localhost"),
        "port": int(get_env("MONGO_PORT", "27017")),
        "database": get_env("MONGO_DATABASE", "contacts"),
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
