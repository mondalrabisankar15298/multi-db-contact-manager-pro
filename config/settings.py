"""
Application settings and configuration management.
"""

import os
from typing import Optional

class Settings:
    """Application settings manager."""
    
    def __init__(self):
        self.load_environment()
    
    def load_environment(self):
        """Load settings from environment variables."""
        # Default database type
        self.default_db_type = os.environ.get('DB_TYPE', 'sqlite')
        
        # Application settings
        self.disable_ui = os.environ.get('CONTACT_MANAGER_DISABLE_UI', '0') == '1'
        
        # Debug settings
        self.debug_mode = os.environ.get('DEBUG', '0') == '1'
        
        # Backup settings
        self.auto_backup = os.environ.get('AUTO_BACKUP', '1') == '1'
        self.backup_interval_hours = int(os.environ.get('BACKUP_INTERVAL_HOURS', '24'))
    
    def get_default_database_type(self) -> str:
        """Get the default database type."""
        return self.default_db_type
    
    def set_default_database_type(self, db_type: str) -> None:
        """Set the default database type."""
        self.default_db_type = db_type
        os.environ['DB_TYPE'] = db_type
    
    def is_ui_disabled(self) -> bool:
        """Check if UI is disabled."""
        return self.disable_ui
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug_mode
    
    def should_auto_backup(self) -> bool:
        """Check if auto backup is enabled."""
        return self.auto_backup
    
    def get_backup_interval_hours(self) -> int:
        """Get backup interval in hours."""
        return self.backup_interval_hours

# Global settings instance
settings = Settings()
