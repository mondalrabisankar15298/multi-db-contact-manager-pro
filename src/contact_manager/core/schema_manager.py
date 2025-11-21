"""
Schema Manager - Dynamic Database Schema Management
Handles dynamic column introspection and schema modifications across all database types.
"""

from typing import List, Dict, Any, Tuple


class SchemaManager:
    """Manages dynamic database schema operations."""
    
    # Minimum required columns (cannot be removed)
    REQUIRED_COLUMNS = ['id', 'name', 'phone', 'email', 'created_at', 'updated_at']
    
    @staticmethod
    def get_table_columns() -> List[str]:
        """Get list of all column names in the contacts table."""
        from ..database.manager import db_manager
        table_info = db_manager.current_adapter.get_table_info()
        
        # Handle different return formats from different databases
        if not table_info:
            return SchemaManager.REQUIRED_COLUMNS.copy()
        
        columns = []
        for col_info in table_info:
            # Different databases return different tuple structures
            # SQLite: (cid, name, type, notnull, dflt_value, pk)
            # PostgreSQL: (name, type, nullable, default)
            # MongoDB: (name, type, nullable, default)
            if isinstance(col_info, (list, tuple)):
                # Different databases return different tuple structures
                # SQLite: (cid, name, type, notnull, dflt_value, pk) - name at index 1
                # MySQL/PostgreSQL/MongoDB: (name, type, ...) - name at index 0
                if len(col_info) > 1 and isinstance(col_info[0], int):
                    # SQLite format: column name is at index 1
                    col_name = col_info[1]
                else:
                    # MySQL/PostgreSQL/MongoDB format: column name is at index 0
                    col_name = col_info[0]
                columns.append(str(col_name))
        
        return columns if columns else SchemaManager.REQUIRED_COLUMNS.copy()
    
    @staticmethod
    def get_display_columns() -> List[str]:
        """Get columns in proper display order with timestamps last."""
        columns = SchemaManager.get_table_columns()
        
        # Separate timestamp columns from others
        timestamp_cols = ['created_at', 'updated_at']
        other_cols = [col for col in columns if col not in timestamp_cols]
        present_timestamp_cols = [col for col in timestamp_cols if col in columns]
        
        # Return other columns first, then timestamp columns
        return other_cols + present_timestamp_cols
    
    @staticmethod
    def get_column_info() -> List[Dict[str, Any]]:
        """Get detailed information about all columns."""
        from ..database.manager import db_manager
        table_info = db_manager.current_adapter.get_table_info()
        columns_info = []
        
        for col_info in table_info:
            if isinstance(col_info, (list, tuple)):
                # Parse based on database type
                db_type = db_manager.current_db_type
                
                if db_type == 'sqlite':
                    # (cid, name, type, notnull, dflt_value, pk)
                    if len(col_info) >= 6:
                        columns_info.append({
                            'name': col_info[1],
                            'type': col_info[2],
                            'nullable': col_info[3] == 0,
                            'default': col_info[4],
                            'primary_key': col_info[5] == 1
                        })
                elif db_type in ['postgres', 'postgresql']:
                    # (name, type, nullable, default)
                    if len(col_info) >= 4:
                        columns_info.append({
                            'name': col_info[0],
                            'type': col_info[1],
                            'nullable': col_info[2] == 'YES',
                            'default': col_info[3],
                            'primary_key': col_info[0] == 'id'
                        })
                elif db_type in ['mongodb', 'mongo']:
                    # MongoDB schemaless - return expected fields
                    if len(col_info) >= 4:
                        columns_info.append({
                            'name': col_info[0],
                            'type': col_info[1],
                            'nullable': col_info[2] == 'YES',
                            'default': col_info[3],
                            'primary_key': col_info[0] == 'id'
                        })
                else:  # MySQL
                    # Try to parse generically
                    columns_info.append({
                        'name': col_info[0] if isinstance(col_info[0], str) else col_info[1],
                        'type': col_info[1] if len(col_info) > 1 else 'TEXT',
                        'nullable': True,
                        'default': None,
                        'primary_key': False
                    })
        
        return columns_info
    
    @staticmethod
    def get_editable_columns() -> List[str]:
        """Get list of columns that can be edited (excludes id and timestamps)."""
        columns = SchemaManager.get_table_columns()
        return [col for col in columns if col not in ['id', 'created_at', 'updated_at']]
    
    @staticmethod
    def get_optional_columns() -> List[str]:
        """Get columns that are not required (can be added/removed)."""
        columns = SchemaManager.get_table_columns()
        return [col for col in columns if col not in SchemaManager.REQUIRED_COLUMNS]
    
    @staticmethod
    def can_remove_column(column_name: str) -> bool:
        """Check if a column can be removed."""
        return column_name not in SchemaManager.REQUIRED_COLUMNS
    
    @staticmethod
    def add_column(column_name: str, column_type: str = 'TEXT', default_value: Any = None) -> bool:
        """Add a new column to the contacts table."""
        try:
            # Check if column already exists
            existing_columns = SchemaManager.get_table_columns()
            if column_name in existing_columns:
                return False
            
            # Validate column name
            if not column_name.isidentifier():
                return False
            
            # Add column using adapter
            from ..database.manager import db_manager
            db_manager.current_adapter.add_column(column_name, column_type, default_value)
            return True
        except Exception as e:
            print(f"Error adding column: {e}")
            return False
    
    @staticmethod
    def remove_column(column_name: str) -> bool:
        """Remove a column from the contacts table."""
        try:
            # Check if column can be removed
            if not SchemaManager.can_remove_column(column_name):
                return False
            
            # Check if column exists
            existing_columns = SchemaManager.get_table_columns()
            if column_name not in existing_columns:
                return False
            
            # Remove column using adapter
            from ..database.manager import db_manager
            if hasattr(db_manager.current_adapter, 'remove_column'):
                db_manager.current_adapter.remove_column(column_name)
                return True
            else:
                print("Current database adapter doesn't support column removal")
                return False
        except Exception as e:
            print(f"Error removing column: {e}")
            return False
    
    @staticmethod
    def get_contact_as_dict(contact_tuple: Tuple) -> Dict[str, Any]:
        """Convert contact tuple to dictionary based on current schema."""
        columns = SchemaManager.get_table_columns()
        contact_dict = {}
        
        for i, column in enumerate(columns):
            if i < len(contact_tuple):
                value = contact_tuple[i]
                # Format timestamp columns for display
                if column in ['created_at', 'updated_at'] and value is not None:
                    try:
                        from ..utils.timezone_utils import format_timestamp_for_display
                        contact_dict[column] = format_timestamp_for_display(value)
                    except ImportError:
                        # Fallback if timezone utils not available
                        contact_dict[column] = value
                else:
                    contact_dict[column] = value
            else:
                contact_dict[column] = None
        
        return contact_dict
    
    @staticmethod
    def get_contact_as_dict_raw(contact_tuple: Tuple) -> Dict[str, Any]:
        """Convert contact tuple to dictionary with raw database values (no formatting)."""
        columns = SchemaManager.get_table_columns()
        contact_dict = {}
        
        for i, column in enumerate(columns):
            if i < len(contact_tuple):
                contact_dict[column] = contact_tuple[i]
            else:
                contact_dict[column] = None
        
        return contact_dict
    
    @staticmethod
    def build_contact_tuple(contact_dict: Dict[str, Any]) -> Tuple:
        """Build contact tuple from dictionary based on current schema."""
        columns = SchemaManager.get_table_columns()
        values = []
        
        for column in columns:
            values.append(contact_dict.get(column))
        
        return tuple(values)


# Global instance
schema_manager = SchemaManager()

