"""
Abstract base class for database adapters.
Defines the interface that all database implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple


class DatabaseAdapter(ABC):
    """Abstract base class for database operations."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the database adapter with configuration."""
        self.config = config
    
    # Connection Management
    @abstractmethod
    def get_connection(self):
        """Create and return a database connection."""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test if the database connection is working."""
        pass
    
    # Schema Management
    @abstractmethod
    def create_table(self) -> None:
        """Create the contacts table if it doesn't exist."""
        pass
    
    # Basic CRUD Operations
    @abstractmethod
    def add_contact(self, **fields) -> None:
        """Add a new contact to the database with dynamic fields."""
        pass
    
    def update_contact(self, contact_id: int, **fields) -> None:
        """Update contact fields dynamically (optional, adapter-specific)."""
        raise NotImplementedError("Update contact not implemented for this adapter")
    
    @abstractmethod
    def view_contacts(self) -> List[Tuple]:
        """Retrieve all contacts from the database."""
        pass
    
    @abstractmethod
    def get_contact_by_id(self, contact_id: int) -> Optional[Tuple]:
        """Get a specific contact by ID."""
        pass
    
    @abstractmethod
    def update_contact_name(self, contact_id: int, new_name: str) -> None:
        """Update a contact's name."""
        pass
    
    @abstractmethod
    def update_contact_phone(self, contact_id: int, new_phone: str) -> None:
        """Update a contact's phone number."""
        pass
    
    @abstractmethod
    def update_contact_email(self, contact_id: int, new_email: str) -> None:
        """Update a contact's email."""
        pass
    
    @abstractmethod
    def delete_contact(self, contact_id: int) -> None:
        """Delete a contact from the database."""
        pass
    
    # Search Operations
    @abstractmethod
    def search_contact(self, search_term: str) -> List[Tuple]:
        """Search for contacts by name, phone, or email."""
        pass
    
    @abstractmethod
    def advanced_search(self, filters: Dict[str, Any]) -> List[Tuple]:
        """Advanced search with multiple filters."""
        pass
    
    # Data Import/Export Operations
    @abstractmethod
    def export_to_csv(self, filename: str) -> None:
        """Export contacts to CSV file."""
        pass
    
    @abstractmethod
    def export_to_json(self, filename: str) -> None:
        """Export contacts to JSON file."""
        pass
    
    @abstractmethod
    def import_from_csv(self, filename: str) -> int:
        """Import contacts from CSV file. Returns number of imported contacts."""
        pass
    
    # Bulk Operations
    @abstractmethod
    def bulk_update(self, contact_ids: List[int], field: str, new_value: str) -> int:
        """Update multiple contacts at once. Returns number of updated contacts."""
        pass
    
    @abstractmethod
    def bulk_delete(self, contact_ids: List[int]) -> int:
        """Delete multiple contacts at once. Returns number of deleted contacts."""
        pass
    
    # Analytics and Statistics
    @abstractmethod
    def get_contact_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contact analytics."""
        pass
    
    @abstractmethod
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        pass
    
    @abstractmethod
    def get_table_info(self) -> List[Tuple]:
        """Get table structure information."""
        pass
    
    # Database Management
    @abstractmethod
    def add_column(self, column_name: str, column_type: str, default_value: Any = None) -> None:
        """Add a new column to the contacts table."""
        pass
    
    @abstractmethod
    def backup_database(self) -> str:
        """Create a backup of the database. Returns backup filename."""
        pass
    
    @abstractmethod
    def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup. Returns success status."""
        pass
    
    @abstractmethod
    def cleanup_db(self) -> int:
        """Clean up database (remove empty records, etc.). Returns number of cleaned records."""
        pass
    
    @abstractmethod
    def full_cleanup_db(self) -> bool:
        """Perform full database cleanup. Returns success status."""
        pass
    
    def reset_table_structure(self) -> bool:
        """Reset table to base 4-column structure (drop and recreate). Returns success status."""
        pass
    
    # Utility Methods
    def get_db_type(self) -> str:
        """Get the database type identifier."""
        return self.__class__.__name__.replace('Adapter', '').lower()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information for display purposes."""
        return {
            'type': self.get_db_type(),
            'config': {k: v for k, v in self.config.items() if 'password' not in k.lower()}
        }
