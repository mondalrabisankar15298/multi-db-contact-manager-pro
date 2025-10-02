"""
Database factory for creating database adapter instances.
"""

from typing import Dict, Any
from .base import DatabaseAdapter
from .adapters.sqlite_adapter import SQLiteAdapter
from .adapters.mysql_adapter import MySQLAdapter
from .adapters.postgres_adapter import PostgreSQLAdapter
from .adapters.mongo_adapter import MongoDBAdapter
from ..config.database_config import get_database_config


class DatabaseFactory:
    """Factory class for creating database adapter instances."""
    
    # Registry of available database adapters
    _adapters = {
        'sqlite': SQLiteAdapter,
        'mysql': MySQLAdapter,
        'postgres': PostgreSQLAdapter,
        'postgresql': PostgreSQLAdapter,  # Alias (internal use only)
        'mongodb': MongoDBAdapter,
        'mongo': MongoDBAdapter,  # Alias (internal use only)
    }
    
    # Primary database types to show in menu (excludes aliases)
    _primary_types = ['sqlite', 'mysql', 'postgres', 'mongodb']
    
    @classmethod
    def create_adapter(cls, db_type: str, config: Dict[str, Any] = None) -> DatabaseAdapter:
        """
        Create a database adapter instance.
        
        Args:
            db_type: Type of database ('sqlite', 'mysql', 'postgres', 'mongodb')
            config: Optional configuration dict. If None, uses default config.
            
        Returns:
            DatabaseAdapter instance
            
        Raises:
            ValueError: If database type is not supported
        """
        if db_type not in cls._adapters:
            available = ', '.join(cls._adapters.keys())
            raise ValueError(f"Unsupported database type: {db_type}. Available: {available}")
        
        # Use provided config or get default config
        if config is None:
            config = get_database_config(db_type)
        
        # Create and return adapter instance
        adapter_class = cls._adapters[db_type]
        return adapter_class(config)
    
    @classmethod
    def get_available_types(cls) -> list:
        """Get list of available database types (primary only, no aliases)."""
        return cls._primary_types
    
    @classmethod
    def register_adapter(cls, db_type: str, adapter_class: type) -> None:
        """
        Register a new database adapter.
        
        Args:
            db_type: Database type identifier
            adapter_class: Adapter class that inherits from DatabaseAdapter
        """
        if not issubclass(adapter_class, DatabaseAdapter):
            raise ValueError("Adapter class must inherit from DatabaseAdapter")
        
        cls._adapters[db_type] = adapter_class
    
    @classmethod
    def is_supported(cls, db_type: str) -> bool:
        """Check if a database type is supported."""
        return db_type in cls._adapters
    
    @classmethod
    def create_with_test(cls, db_type: str, config: Dict[str, Any] = None) -> DatabaseAdapter:
        """
        Create adapter and test connection.
        
        Args:
            db_type: Type of database
            config: Optional configuration dict
            
        Returns:
            DatabaseAdapter instance with tested connection
            
        Raises:
            ConnectionError: If connection test fails
            ValueError: If database type is not supported
        """
        adapter = cls.create_adapter(db_type, config)
        
        if not adapter.test_connection():
            raise ConnectionError(f"Failed to connect to {db_type} database")
        
        return adapter
