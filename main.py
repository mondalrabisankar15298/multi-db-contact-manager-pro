"""
Contact Book Manager - Main Application
A professional contact management system with advanced features.
"""

# Keep imports minimal at module load to remain import-safe
import os
import sys
import builtins

# Import from core operations only; UI/menu imports are deferred inside functions
from core_operations import create_table

def is_interactive() -> bool:
    """Return True if CLI should run (TTY and not explicitly disabled)."""
    if os.environ.get("CONTACT_MANAGER_DISABLE_UI", "0") == "1":
        return False
    try:
        return sys.stdin.isatty()
    except Exception:
        return False

def display_main_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("📒 Contact Book Manager")
    print("="*50)
    print("1. ➕ Add Contact")
    print("2. 👀 View All Contacts")
    print("3. 🔍 Search Contacts")
    print("4. ✏️  Update Contact")
    print("5. 🗑️  Delete Contact")
    print("6. 📊 Advanced Features")
    print("7. ⚙️  Database Management")
    print("8. 🚪 Exit")
    print("0. 🔄 Refresh Menu")
    print("="*50)

def display_advanced_features_menu():
    """Display advanced features submenu."""
    print("\n" + "="*50)
    print("📊 Advanced Features")
    print("="*50)
    print("1. 📈 Contact Analytics")
    print("2. 🔍 Advanced Search")
    print("3. 📤 Export Data")
    print("4. 📥 Import Data")
    print("5. 🔄 Bulk Operations")
    print("6. 🏷️  Categories & Tags")
    print("7. ✅ Data Validation")
    print("8. 🔍 Data Integrity Check")
    print("9. 🔙 Back to Previous Menu")
    print("0. 🚪 Exit Application")
    print("="*50)

def display_database_management_menu():
    """Display database management submenu."""
    print("\n" + "="*50)
    print("⚙️  Database Management")
    print("="*50)
    print("1. 📊 View Database Statistics")
    print("2. 🏗️  View Table Structure")
    print("3. ➕ Add Column")
    print("4. ➖ Remove Column")
    print("5. 💾 Backup Database")
    print("6. 🔄 Restore Database")
    print("7. 🧹 Cleanup Database")
    print("8. 🔙 Back to Previous Menu")
    print("0. 🚪 Exit Application")
    print("="*50)

def handle_advanced_features():
    """Handle advanced features submenu."""
    while True:
        display_advanced_features_menu()
        choice = input("\nEnter your choice (0-9): ").strip()

        if choice == "1":
            from menus import contact_analytics_menu
            contact_analytics_menu()
        elif choice == "2":
            from menus import advanced_search_menu
            advanced_search_menu()
        elif choice == "3":
            from menus import export_data_menu
            export_data_menu()
        elif choice == "4":
            from menus import import_data_menu
            import_data_menu()
        elif choice == "5":
            from menus import bulk_operations_menu
            bulk_operations_menu()
        elif choice == "6":
            from menus import categories_tags_menu
            categories_tags_menu()
        elif choice == "7":
            from menus import data_validation_menu
            data_validation_menu()
        elif choice == "8":
            from menus import data_integrity_menu
            data_integrity_menu()
        elif choice == "9":
            # Back to previous menu
            return "back"
        elif choice == "0":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        else:
            from ui import display_error
            display_error("Invalid choice! Please enter 0-9.")

def handle_database_management():
    """Handle database management submenu."""
    while True:
        display_database_management_menu()
        choice = input("\nEnter your choice (0-8): ").strip()

        if choice == "1":
            from ui import display_database_stats
            display_database_stats()
        elif choice == "2":
            from ui import display_table_structure
            display_table_structure()
        elif choice == "3":
            from menus import add_column_menu
            add_column_menu()
        elif choice == "4":
            from menus import remove_column_menu
            remove_column_menu()
        elif choice == "5":
            from menus import backup_database_menu
            backup_database_menu()
        elif choice == "6":
            from menus import restore_database_menu
            restore_database_menu()
        elif choice == "7":
            from menus import cleanup_database_menu
            cleanup_database_menu()
        elif choice == "8":
            # Back to previous menu
            return "back"
        elif choice == "0":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        else:
            from ui import display_error
            display_error("Invalid choice! Please enter 0-8.")

def initialize_database():
    """Initialize the database."""
    try:
        create_table()
        from ui import display_success
        display_success("Database initialized successfully!")
        return True
    except Exception as e:
        from ui import display_error
        display_error(f"Error initializing database: {e}")
        return False

def main():
    """Main application loop."""

    # Gate UI startup more strictly
    if not _should_run_ui():
        return

    print("🚀 Starting Contact Book Manager...")

    # Initialize database
    if not initialize_database():
        return

    # Main application loop
    main_menu_loop()

def main_menu_loop():
    """Main menu loop with navigation handling."""
    # Import menus lazily to keep module import side-effect free
    from menus import (add_contact_menu, view_contacts_menu, search_contacts_menu,
                       update_contact_menu, delete_contact_menu)
    from ui import display_error

    while True:
        try:
            display_main_menu()
            choice = input("\nEnter your choice (0-8): ").strip()

            if choice == "1":
                add_contact_menu()
            elif choice == "2":
                view_contacts_menu()
            elif choice == "3":
                search_contacts_menu()
            elif choice == "4":
                update_contact_menu()
            elif choice == "5":
                delete_contact_menu()
            elif choice == "6":
                result = handle_advanced_features()
                if result == "back":
                    continue
                elif result == "goto_main":
                    continue
            elif choice == "7":
                result = handle_database_management()
                if result == "back":
                    continue
                elif result == "goto_main":
                    continue
            elif choice == "8":
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                break
            elif choice == "0":
                print("🔄 Refreshing menu...")
                continue
            else:
                display_error("Invalid choice! Please enter 0-8.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except (EOFError, SystemExit):
            # End scripted/non-interactive runs cleanly
            print("\n[Script/UI input ended – exiting]")
            break
        except Exception as e:
            from ui import display_error as _display_error
            _display_error(f"Unexpected error: {e}")

def _should_run_ui() -> bool:
    """Decide whether to run the interactive UI.
    - Do not run when CONTACT_MANAGER_DISABLE_UI=1
    - Run only when interactive TTY
    """
    if os.environ.get("CONTACT_MANAGER_DISABLE_UI", "0") == "1":
        return False
    # Only run in interactive TTY
    return is_interactive()

if __name__ == "__main__":
    # Only run when appropriate to avoid accidental startup in automated contexts
    if _should_run_ui():
        main()