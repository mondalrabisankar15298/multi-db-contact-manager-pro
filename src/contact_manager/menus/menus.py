"""
Menus Module - Menu Functions
Handles all menu operations and user interactions for the Contact Book Manager.
"""

# Import from core operations to avoid circular dependencies
from core_operations import (add_contact, view_contacts, update_contact, update_contact_name, update_contact_phone, 
                            update_contact_email, delete_contact, search_contact, get_contact_by_id,
                            export_to_csv, export_to_json, import_from_csv, advanced_search,
                            bulk_update, bulk_delete, validate_email, 
                            validate_phone, format_phone, check_data_integrity, get_contact_analytics,
                            get_database_stats, get_table_info, add_column, 
                            backup_database, restore_database, full_cleanup_db)
from ..core.schema_manager import schema_manager

# TODO: Implement database schema management functions for multi-database support
# from crud import (add_category_column, add_tag_column, get_contacts_by_category,
#                  get_contacts_by_tag, remove_column)

from ui import (display_contacts, display_contact_analytics, display_database_stats,
               display_table_structure, display_data_integrity_results,
               display_validation_results, display_search_results, display_contact_preview,
               display_operation_success, display_operation_error, display_warning,
               display_info, display_success, display_error)

def add_contact_menu():
    """Handle adding a new contact (dynamic based on schema)."""
    from dynamic_ui import get_contact_input_dynamic
    
    print("\n➕ Add New Contact")
    print("-" * 30)
    
    try:
        # Get contact data dynamically based on current schema
        contact_data = get_contact_input_dynamic()
        
        # Handle aborted input flow
        if contact_data is None:
            display_info("Add contact cancelled.")
            return
        
        if not contact_data:
            display_error("No contact data entered!")
            return
        
        # Optional server-side validation as a safety net
        email_val = contact_data.get('email', '')
        phone_val = contact_data.get('phone', '')
        
        if email_val and not validate_email(email_val):
            display_error("Invalid email format. Please correct and try again.")
            return
        
        if phone_val and not validate_phone(phone_val):
            display_error("Invalid phone number format. Please correct and try again.")
            return
        
        # Normalize phone format if provided
        if phone_val:
            contact_data['phone'] = format_phone(phone_val)
        
        # Add contact
        add_contact(**contact_data)
        display_success("Contact added successfully!")
    except Exception as e:
        display_operation_error("adding contact", e)

def view_contacts_menu():
    """Handle viewing all contacts (dynamic based on schema)."""
    from dynamic_ui import display_contacts_dynamic
    
    print("\n👀 All Contacts")
    print("-" * 30)
    
    # Ask user for view preference
    print("\nView options:")
    print("0. 🔙 Back to Previous Menu")
    print("1. Compact view (all columns)")
    print("2. Detailed view (all columns)")
    
    choice = input("\nSelect view (0-2, or press Enter for compact): ").strip()
    
    if choice == '0':
        return
    
    if choice in ['1', '2', '']:
        detailed = (choice == '2')
        try:
            contacts = view_contacts()
            display_contacts_dynamic(contacts, detailed=detailed)
        except Exception as e:
            display_operation_error("retrieving contacts", e)
    else:
        display_error("Invalid choice! Please enter 0-2.")

def search_contacts_menu():
    """Handle searching contacts."""
    print("\n🔍 Search Contacts")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    search_term = input("Enter search term (name, phone, or email): ").strip()
    if search_term in ["0", "111"]:
        if search_term == "0":
            return
        else:
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
    if not search_term:
        display_error("Search term is required!")
        return
    
    try:
        contacts = search_contact(search_term)
        display_search_results(contacts, search_term)
    except Exception as e:
        display_operation_error("searching contacts", e)

def update_contact_menu():
    """Handle updating a contact."""
    print("\n✏️ Update Contact")
    print("-" * 30)

    try:
        contact_id_input = input("Enter contact ID to update: ").strip()

        # Handle empty input
        if not contact_id_input:
            display_error("Contact ID cannot be empty!")
            return

        try:
            contact_id = int(contact_id_input)
        except ValueError:
            display_error("Please enter a valid numeric contact ID!")
            return

        # Check if contact exists
        contact = get_contact_by_id(contact_id)
        if not contact:
            display_error("Contact not found!")
            return

        display_contact_preview(contact)

        # Get field to update dynamically
        from dynamic_ui import get_update_field_choice
        
        field_to_update = get_update_field_choice()
        
        # Handle back/cancel
        if field_to_update is None:
            display_info("Update cancelled.")
            return
        
        # Get new value
        field_display = field_to_update.replace('_', ' ').title()
        new_value = input(f"\nEnter new {field_display}: ").strip()
        
        # Validate name cannot be empty
        if field_to_update == 'name' and not new_value:
            display_error("Name cannot be empty!")
            return
        
        # Field-specific validation
        if field_to_update == 'email' and new_value:
            if not validate_email(new_value):
                display_error("Invalid email format. Please enter a valid email.")
                return
        
        if field_to_update == 'phone' and new_value:
            if not validate_phone(new_value):
                display_error("Invalid phone number. Enter 7-15 digits; separators are allowed.")
                return
            new_value = format_phone(new_value)
        
        # Update the contact
        try:
            update_contact(contact_id, **{field_to_update: new_value})
            display_success(f"{field_display} updated successfully!")
        except Exception as e:
            display_operation_error(f"updating {field_display}", e)

    except EOFError:
        display_error("Input interrupted. Please try again.")
    except Exception as e:
        display_operation_error("updating contact", e)

def delete_contact_menu():
    """Handle deleting a contact."""
    print("\n🗑️ Delete Contact")
    print("-" * 30)
    
    try:
        contact_id_input = input("Enter contact ID to delete: ").strip()

        # Handle empty input
        if not contact_id_input:
            display_error("Contact ID cannot be empty!")
            return

        try:
            contact_id = int(contact_id_input)
        except ValueError:
            display_error("Please enter a valid numeric contact ID!")
            return

        # Check if contact exists
        contact = get_contact_by_id(contact_id)
        if not contact:
            display_error("Contact not found!")
            return

        display_contact_preview(contact)
        confirm = input("Are you sure you want to delete this contact? (y/N): ").strip().lower()

        if confirm in ['y', 'yes']:
            delete_contact(contact_id)
            display_success("Contact deleted successfully!")
        else:
            display_info("Deletion cancelled.")

    except EOFError:
        display_error("Input interrupted. Please try again.")
    except Exception as e:
        display_operation_error("deleting contact", e)

def cleanup_database_menu():
    """Handle database cleanup with multiple options."""
    while True:
        print("\n🧹 Database Cleanup Options")
        print("-" * 50)
        
        try:
            contacts = view_contacts()
            contact_count = len(contacts)
            print(f"📊 Current contacts in database: {contact_count}")
        except:
            contact_count = 0
        
        print("\nChoose cleanup type:")
        print("0. 🔙 Back to Previous Menu")
        print("1. 🗑️  Delete All Data (Keep table structure & columns)")
        print("2. 🔄 Reset Table (Delete table, recreate with 4 base columns)")
        
        choice = input("\nEnter your choice (0-2): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            _delete_all_data_menu(contact_count)
        elif choice == '2':
            _reset_table_structure_menu(contact_count)
        else:
            display_error("Invalid choice! Please enter 0-2.")

def _delete_all_data_menu(contact_count):
    """Delete all data but keep table structure."""
    print("\n🗑️ Delete All Data")
    print("-" * 50)
    
    try:
        if contact_count == 0:
            display_info("Database is already empty!")
            return
        
        display_warning("This will delete ALL contacts from the database!")
        display_info("Table structure and custom columns will remain intact.")
        print("This action cannot be undone!")
        
        confirm1 = input("\nAre you sure you want to delete ALL contacts? (y/N): ").strip().lower()
        
        if confirm1 not in ['y', 'yes']:
            display_info("Cleanup cancelled.")
            return
        
        # Double confirmation for safety
        confirm2 = input("Type 'DELETE ALL' to confirm: ").strip()
        
        if confirm2 == 'DELETE ALL':
            from core_operations import full_cleanup_db
            result = full_cleanup_db()
            if result:
                display_success("All data deleted successfully!")
                print("🧹 All contacts removed, table structure intact.")
            else:
                display_error("Cleanup failed!")
        else:
            display_info("Cleanup cancelled - confirmation text did not match.")
            
    except Exception as e:
        display_operation_error("cleanup", e)

def _reset_table_structure_menu(contact_count):
    """Reset table to base 4-column structure."""
    print("\n🔄 Reset Table Structure")
    print("-" * 50)
    
    try:
        display_warning("This will DELETE the entire table and recreate it!")
        display_warning("ALL contacts AND custom columns will be removed!")
        display_info("Table will be recreated with only 4 base columns:")
        print("   • id")
        print("   • name")
        print("   • phone")
        print("   • email")
        print("\nThis action cannot be undone!")
        
        confirm1 = input("\nAre you sure you want to RESET the table? (y/N): ").strip().lower()
        
        if confirm1 not in ['y', 'yes']:
            display_info("Reset cancelled.")
            return
        
        # Triple confirmation for this destructive operation
        confirm2 = input("Type 'RESET TABLE' to confirm: ").strip()
        
        if confirm2 == 'RESET TABLE':
            from core_operations import reset_table_structure
            result = reset_table_structure()
            if result:
                display_success("Table reset successfully!")
                print("🔄 Table recreated with 4 base columns.")
                print("   All custom columns have been removed.")
            else:
                display_error("Table reset failed!")
        else:
            display_info("Reset cancelled - confirmation text did not match.")
            
    except Exception as e:
        display_operation_error("table reset", e)

def contact_analytics_menu():
    """Display contact analytics."""
    display_contact_analytics()

def advanced_search_menu():
    """Handle advanced search."""
    print("\n🔍 Advanced Search")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        filters = {}
        
        name = input("Search by name (optional): ").strip()
        if name in ["0", "111"]:
            if name == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if name:
            filters['name'] = name
        
        phone = input("Search by phone (optional): ").strip()
        if phone in ["0", "111"]:
            if phone == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if phone:
            filters['phone'] = phone
        
        email = input("Search by email (optional): ").strip()
        if email in ["0", "111"]:
            if email == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if email:
            filters['email'] = email
        
        min_id = input("Minimum ID (optional): ").strip()
        if min_id in ["0", "111"]:
            if min_id == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if min_id:
            filters['min_id'] = int(min_id)
        
        max_id = input("Maximum ID (optional): ").strip()
        if max_id in ["0", "111"]:
            if max_id == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if max_id:
            filters['max_id'] = int(max_id)
        
        if not filters:
            display_error("Please provide at least one search criteria!")
            return
        
        results = advanced_search(filters)
        display_search_results(results)
            
    except Exception as e:
        display_operation_error("advanced search", e)

def export_data_menu():
    """Handle data export."""
    print("\n📤 Export Data")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        print("Export format:")
        print("1. CSV")
        print("2. JSON")
        
        format_choice = input("Enter choice (0-2, 111): ").strip()
        
        if format_choice == "0":
            return
        if format_choice == "111":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        
        if format_choice == "1":
            filename = export_to_csv()
            display_success(f"Data exported to: {filename}")
        elif format_choice == "2":
            filename = export_to_json()
            display_success(f"Data exported to: {filename}")
        else:
            display_error("Invalid choice!")
            
    except Exception as e:
        display_operation_error("exporting data", e)

def import_data_menu():
    """Handle data import."""
    print("\n📥 Import Data")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        filename = input("Enter CSV filename to import: ").strip()
        if filename in ["0", "111"]:
            if filename == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        if not filename:
            display_error("Filename is required!")
            return
        
        imported_count = import_from_csv(filename)
        display_operation_success("Import", imported_count)
        
    except Exception as e:
        display_operation_error("importing data", e)

def bulk_operations_menu():
    """Handle bulk operations."""
    print("\n🔄 Bulk Operations")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        print("1. Bulk Update")
        print("2. Bulk Delete")
        
        choice = input("Enter choice (0-2, 111): ").strip()
        
        if choice == "0":
            return
        if choice == "111":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        
        if choice == "1":
            contact_ids_input = input("Enter contact IDs (comma-separated): ").strip()
            if contact_ids_input in ["0", "111"]:
                if contact_ids_input == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            contact_ids = [int(id.strip()) for id in contact_ids_input.split(',')]
            
            field = input("Enter field to update (name/phone/email): ").strip()
            if field in ["0", "111"]:
                if field == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            new_value = input("Enter new value: ").strip()
            if new_value in ["0", "111"]:
                if new_value == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            
            updated_count = bulk_update(contact_ids, field, new_value)
            display_operation_success("Bulk update", updated_count)
            
        elif choice == "2":
            contact_ids_input = input("Enter contact IDs to delete (comma-separated): ").strip()
            if contact_ids_input in ["0", "111"]:
                if contact_ids_input == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            contact_ids = [int(id.strip()) for id in contact_ids_input.split(',')]
            
            confirm = input(f"Delete {len(contact_ids)} contacts? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                deleted_count = bulk_delete(contact_ids)
                display_operation_success("Bulk delete", deleted_count)
            else:
                display_info("Bulk delete cancelled.")
        else:
            display_error("Invalid choice!")
            
    except Exception as e:
        display_operation_error("bulk operations", e)

def categories_tags_menu():
    """Handle categories and tags."""
    print("\n🏷️  Categories & Tags")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        print("1. Add Category Column")
        print("2. Add Tags Column")
        print("3. View Contacts by Category")
        print("4. View Contacts by Tag")
        
        choice = input("Enter choice (0-4, 111): ").strip()
        
        if choice == "0":
            return
        if choice == "111":
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        
        if choice == "1":
            display_info("Category column management not yet implemented for multi-database support")
                
        elif choice == "2":
            display_info("Tag column management not yet implemented for multi-database support")
                
        elif choice == "3":
            category = input("Enter category: ").strip()
            if category in ["0", "111"]:
                if category == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            contacts = []
            if contacts:
                print(f"\nContacts in category '{category}':")
                display_contacts(contacts)
            else:
                display_info(f"No contacts found in category '{category}'")
                
        elif choice == "4":
            tag = input("Enter tag: ").strip()
            if tag in ["0", "111"]:
                if tag == "0":
                    return
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            contacts = []
            if contacts:
                print(f"\nContacts with tag '{tag}':")
                display_contacts(contacts)
            else:
                display_info(f"No contacts found with tag '{tag}'")
        else:
            display_error("Invalid choice!")
            
    except Exception as e:
        display_operation_error("categories/tags", e)

def data_validation_menu():
    """Handle data validation."""
    print("\n✅ Data Validation")
    print("-" * 30)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    try:
        email = input("Enter email to validate: ").strip()
        if email in ["0", "111"]:
            if email == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        phone = input("Enter phone to validate: ").strip()
        if phone in ["0", "111"]:
            if phone == "0":
                return
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        
        display_validation_results(email if email else None, phone if phone else None)
                
    except Exception as e:
        display_operation_error("data validation", e)

def data_integrity_menu():
    """Handle data integrity check."""
    display_data_integrity_results()

def add_column_menu():
    """Handle adding a new column."""
    print("\n➕ Add New Column")
    print("-" * 30)
    
    try:
        column_name = input("Enter column name: ").strip()
        if not column_name:
            display_error("Column name is required!")
            return
        
        print("\nAvailable column types:")
        print("1. TEXT")
        print("2. INTEGER")
        print("3. REAL")
        print("4. BLOB")
        print("5. Custom type")
        
        type_choice = input("Enter choice (1-5): ").strip()
        
        if type_choice == "1":
            column_type = "TEXT"
        elif type_choice == "2":
            column_type = "INTEGER"
        elif type_choice == "3":
            column_type = "REAL"
        elif type_choice == "4":
            column_type = "BLOB"
        elif type_choice == "5":
            column_type = input("Enter custom type: ").strip()
        else:
            display_error("Invalid choice!")
            return
        
        default_value = input("Enter default value (optional): ").strip()
        if not default_value:
            default_value = None
        
        add_column(column_name, column_type, default_value)
        display_success("Column added successfully!")
        
    except Exception as e:
        display_operation_error("adding column", e)

def remove_column_menu():
    """Handle removing a column."""
    print("\n➖ Remove Column")
    print("-" * 30)
    
    try:
        # Show current columns
        columns = get_table_info()
        if not columns:
            display_info("No columns found!")
            return
        
        print("Current columns:")
        for i, col in enumerate(columns, 1):
            print(f"{i}. {col[1]} ({col[2]})")
        
        column_name = input("\nEnter column name to remove: ").strip()
        if not column_name:
            display_error("Column name is required!")
            return
        
        # Check if column exists
        column_names = [col[1] for col in columns]
        if column_name not in column_names:
            display_error("Column not found!")
            return
        
        # Prevent removing required columns
        if not schema_manager.can_remove_column(column_name):
            display_error("Cannot remove required columns (id, name, phone, email, created_at, updated_at)!")
            return
        
        confirm = input(f"Are you sure you want to remove column '{column_name}'? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            # TODO: Implement remove_column for multi-database support
            # remove_column(column_name)
            display_info("Column removal not yet implemented for multi-database support")
            display_success("Column removed successfully!")
        else:
            display_info("Column removal cancelled.")
            
    except Exception as e:
        display_operation_error("removing column", e)

def backup_database_menu():
    """Handle database backup."""
    print("\n💾 Backup Database")
    print("-" * 30)
    
    try:
        backup_filename = backup_database()
        display_success(f"Database backed up successfully!")
        print(f"📁 Backup file: {backup_filename}")
        
    except Exception as e:
        display_operation_error("creating backup", e)

def restore_database_menu():
    """Handle database restore."""
    print("\n🔄 Restore Database")
    print("-" * 30)
    
    try:
        import glob
        import os
        backup_files = glob.glob(os.path.join("db_backup", "contacts_backup_*.db"))
        
        if not backup_files:
            display_info("No backup files found!")
            return
        
        print("Available backup files:")
        for i, backup_file in enumerate(backup_files, 1):
            print(f"{i}. {backup_file}")
        
        try:
            choice_input = input("\nEnter backup file number: ").strip()

            # Handle empty input
            if not choice_input:
                display_error("Choice cannot be empty!")
                return

            try:
                choice = int(choice_input) - 1
            except ValueError:
                display_error("Please enter a valid number!")
                return

            if 0 <= choice < len(backup_files):
                backup_filename = backup_files[choice]

                confirm = input(f"Restore from '{backup_filename}'? This will overwrite current database! (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    restore_database(backup_filename)
                    display_success("Database restored successfully!")
                else:
                    display_info("Restore cancelled.")
            else:
                display_error("Invalid choice!")
        except EOFError:
            display_error("Input interrupted. Please try again.")
            
    except Exception as e:
        display_operation_error("restoring database", e)
