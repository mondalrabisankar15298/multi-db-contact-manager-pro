"""
Contact Book Manager - Main Application
A professional contact management system with advanced features.
"""

from crud import create_table
from menus import (add_contact_menu, view_contacts_menu, search_contacts_menu,
                  update_contact_menu, delete_contact_menu, cleanup_database_menu,
                  contact_analytics_menu, advanced_search_menu, export_data_menu,
                  import_data_menu, bulk_operations_menu, categories_tags_menu,
                  data_validation_menu, data_integrity_menu, add_column_menu,
                  remove_column_menu, backup_database_menu, restore_database_menu)
from ui import display_error, display_success
from navigation import navigate_to_menu, nav_stack

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
            contact_analytics_menu()
        elif choice == "2":
            advanced_search_menu()
        elif choice == "3":
            export_data_menu()
        elif choice == "4":
            import_data_menu()
        elif choice == "5":
            bulk_operations_menu()
        elif choice == "6":
            categories_tags_menu()
        elif choice == "7":
            data_validation_menu()
        elif choice == "8":
            data_integrity_menu()
        elif choice == "9":
            # Back to previous menu
            return "back"
        elif choice == "0":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            exit()
        else:
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
            add_column_menu()
        elif choice == "4":
            remove_column_menu()
        elif choice == "5":
            backup_database_menu()
        elif choice == "6":
            restore_database_menu()
        elif choice == "7":
            cleanup_database_menu()
        elif choice == "8":
            # Back to previous menu
            return "back"
        elif choice == "0":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            exit()
        else:
            display_error("Invalid choice! Please enter 0-8.")

def initialize_database():
    """Initialize the database."""
    try:
        create_table()
        display_success("Database initialized successfully!")
        return True
    except Exception as e:
        display_error(f"Error initializing database: {e}")
        return False

def main():
    """Main application loop."""
    print("🚀 Starting Contact Book Manager...")
    
    # Initialize database
    if not initialize_database():
        return
    
    # Main application loop
    main_menu_loop()

def main_menu_loop():
    """Main menu loop with navigation handling."""
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
            elif choice == "7":
                result = handle_database_management()
                if result == "back":
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
        except Exception as e:
            display_error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()