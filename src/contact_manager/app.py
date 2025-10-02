"""
Contact Book Manager - Application Controller
Handles the main application flow and menu coordination.
"""

import os
import sys
from typing import Optional

from .cli.preflight import run_preflight_and_choose_db
from .core.core_operations import create_table
from .config.settings import settings
from .database.manager import db_manager
from .menus.main_menu import MainMenuHandler
from .ui.ui import display_success, display_error


class ContactManagerApp:
    """Main application controller for the Contact Manager."""
    
    def __init__(self):
        self.menu_handler = MainMenuHandler()
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the application with preflight checks."""
        try:
            # Run preflight checks
            verbose = os.environ.get("DEBUG", "0") == "1"
            run_preflight_and_choose_db(verbose=verbose)
            
            # Ensure database manager aligns with settings
            default_db = settings.get_default_database_type()
            if db_manager.current_db_type != default_db:
                db_manager.switch_database(default_db)
            
            # Create table if needed
            create_table()
            
            self._initialized = True
            return True
            
        except Exception as e:
            display_error(f"Failed to initialize application: {str(e)}")
            return False
    
    def is_interactive(self) -> bool:
        """Check if the application should run in interactive mode."""
        if os.environ.get("CONTACT_MANAGER_DISABLE_UI", "0") == "1":
            return False
        try:
            return sys.stdin.isatty()
        except Exception:
            return False
    
    def run(self) -> None:
        """Run the main application loop."""
        if not self._initialized:
            if not self.initialize():
                sys.exit(1)
        
        if not self.is_interactive():
            print("Contact Manager: Non-interactive mode detected. Exiting.")
            return
        
        try:
            self.menu_handler.show_main_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Contact Book Manager!")
        except Exception as e:
            display_error(f"Application error: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point for the application."""
    app = ContactManagerApp()
    app.run()


if __name__ == "__main__":
    main()
