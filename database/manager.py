"""
Database manager for handling database switching and global state.
"""

from typing import Optional, Dict, Any
from .base import DatabaseAdapter
from .factory import DatabaseFactory
from config.settings import settings
from state_tracker import set_last_db_type


class DatabaseManager:
    """
    Singleton manager for database operations and switching.
    Handles the current active database connection and switching between databases.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _current_adapter: Optional[DatabaseAdapter] = None
    _current_db_type: str = "sqlite"
    
    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database manager."""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._current_db_type = settings.get_default_database_type()
            self._current_adapter = None
    
    @property
    def current_adapter(self) -> DatabaseAdapter:
        """Get the current database adapter, creating it if necessary."""
        if self._current_adapter is None:
            self._current_adapter = DatabaseFactory.create_adapter(self._current_db_type)
        return self._current_adapter
    
    @property
    def current_db_type(self) -> str:
        """Get the current database type."""
        return self._current_db_type
    
    def switch_database(self, db_type: str, config: Dict[str, Any] = None) -> bool:
        """
        Switch to a different database.
        
        Args:
            db_type: Target database type
            config: Optional custom configuration
            
        Returns:
            True if switch was successful, False otherwise
        """
        try:
            # Test the new connection first
            new_adapter = DatabaseFactory.create_with_test(db_type, config)
            
            # If test successful, switch to new adapter
            old_adapter = self._current_adapter
            self._current_adapter = new_adapter
            self._current_db_type = db_type
            
            # Update global settings
            settings.set_default_database_type(db_type)
            # Persist as last used for future sessions
            try:
                set_last_db_type(db_type)
            except Exception:
                pass
            
            # Close old connection if it exists
            if old_adapter and hasattr(old_adapter, 'close_connection'):
                try:
                    old_adapter.close_connection()
                except:
                    pass  # Ignore errors when closing old connection
            
            return True
            
        except Exception as e:
            print(f"Failed to switch to {db_type}: {e}")
            return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get information about the current database connection."""
        if self._current_adapter:
            return self._current_adapter.get_connection_info()
        return {
            'type': self._current_db_type,
            'status': 'not_connected'
        }
    
    def test_current_connection(self) -> bool:
        """Test the current database connection."""
        try:
            return self.current_adapter.test_connection()
        except Exception:
            return False
    
    def get_available_databases(self) -> list:
        """Get list of available database types."""
        return DatabaseFactory.get_available_types()
    
    def is_database_available(self, db_type: str) -> bool:
        """Check if a database type is available."""
        return DatabaseFactory.is_supported(db_type)
    
    def reset_to_default(self) -> bool:
        """Reset to the default database (SQLite)."""
        return self.switch_database('sqlite')
    
    def force_reconnect(self) -> bool:
        """Force reconnection to the current database."""
        current_type = self._current_db_type
        self._current_adapter = None
        try:
            # This will create a new adapter
            self.current_adapter.test_connection()
            return True
        except Exception:
            return False


# Global database manager instance
db_manager = DatabaseManager()
