# Import from core operations for consistency
from core_operations import default_db

def get_connection():
    """Create and return a database connection."""
    return default_db.get_connection()
