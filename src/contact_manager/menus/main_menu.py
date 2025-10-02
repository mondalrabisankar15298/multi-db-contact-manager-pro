"""
Main Menu Handler for Contact Manager
Handles the primary menu system and navigation.
"""

from typing import Dict, Callable
from ..core.core_operations import get_current_database_type, get_current_database_info
from ..ui.ui import display_error, display_success
from .contact_menu import ContactMenuHandler
from .advanced_menu import AdvancedMenuHandler
from .database_menu import DatabaseMenuHandler


class MainMenuHandler:
    """Handles the main menu system and navigation."""
    
    def __init__(self):
        self.contact_handler = ContactMenuHandler()
        self.advanced_handler = AdvancedMenuHandler()
        self.database_handler = DatabaseMenuHandler()
        self.running = True
    
    def display_main_menu(self) -> None:
        """Display the main menu."""
        current_db = get_current_database_type().upper()
        
        print("\n" + "="*50)
        print("📒 Contact Book Manager")
        print("="*50)
        print(f"🗄️  Current Database: {current_db}")
        print("="*50)
        print("1. ➕ Add Contact")
        print("2. 👀 View All Contacts")
        print("3. 🔍 Search Contacts")
        print("4. ✏️  Update Contact")
        print("5. 🗑️  Delete Contact")
        print("6. 📊 Advanced Features")
        print("7. ⚙️  Database Management")
        print("8. 🗄️  Switch Database")
        print("0. 🔙 Back to Previous Menu")
        print("111. 🚪 Exit Application")
        print("="*50)
    
    def get_menu_actions(self) -> Dict[str, Callable]:
        """Get the mapping of menu choices to actions."""
        return {
            "1": self.contact_handler.add_contact,
            "2": self.contact_handler.view_contacts,
            "3": self.contact_handler.search_contacts,
            "4": self.contact_handler.update_contact,
            "5": self.contact_handler.delete_contact,
            "6": self.advanced_handler.show_advanced_menu,
            "7": self.database_handler.show_database_menu,
            "8": self.database_handler.switch_database,
            "0": self.go_back,
            "111": self.exit_application
        }
    
    def show_main_menu(self) -> None:
        """Show the main menu and handle user input."""
        while self.running:
            try:
                self.display_main_menu()
                choice = input("\nEnter your choice (0-8, 111): ").strip()
                
                actions = self.get_menu_actions()
                
                if choice in actions:
                    actions[choice]()
                else:
                    display_error("Invalid choice! Please enter 0-8 or 111.")
                    
            except KeyboardInterrupt:
                self.exit_application()
            except Exception as e:
                display_error(f"Menu error: {str(e)}")
    
    def go_back(self) -> None:
        """Handle going back (in main menu, this exits)."""
        self.exit_application()
    
    def exit_application(self) -> None:
        """Exit the application gracefully."""
        print("\n👋 Thank you for using Contact Book Manager!")
        self.running = False
