"""
Column Management Menu - Allows users to dynamically add/remove columns
"""

from ..core.schema_manager import schema_manager
from ..ui.dynamic_ui import display_schema_info, display_column_management_menu


def column_management_menu():
    """Main column management menu."""
    while True:
        display_column_management_menu()
        choice = input("\nEnter your choice (0-3): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            view_schema_menu()
        elif choice == '2':
            add_column_menu()
        elif choice == '3':
            remove_column_menu()
        else:
            print("❌ Invalid choice! Please enter 0-3.")


def view_schema_menu():
    """View current database schema."""
    display_schema_info()
    input("\nPress Enter to continue...")


def add_column_menu():
    """Add a new column to the database."""
    print("\n➕ Add New Column")
    print("=" * 50)
    
    # Get column name
    while True:
        col_name = input("Enter column name (or '0' to cancel): ").strip().lower()
        
        if col_name == '0':
            print("❌ Operation cancelled")
            return
        
        if not col_name:
            print("❌ Column name cannot be empty!")
            continue
        
        if not col_name.isidentifier():
            print("❌ Invalid column name! Use only letters, numbers, and underscores.")
            continue
        
        # Check if already exists
        existing_columns = schema_manager.get_table_columns()
        if col_name in existing_columns:
            print(f"❌ Column '{col_name}' already exists!")
            continue
        
        break
    
    # Get column type
    print("\nSelect data type:")
    print("1. TEXT (for strings)")
    print("2. INTEGER (for whole numbers)")
    print("3. REAL (for decimal numbers)")
    print("4. BOOLEAN (for true/false)")
    
    type_map = {
        '1': 'TEXT',
        '2': 'INTEGER',
        '3': 'REAL',
        '4': 'BOOLEAN'
    }
    
    while True:
        type_choice = input("Enter choice (1-4): ").strip()
        if type_choice in type_map:
            col_type = type_map[type_choice]
            break
        print("❌ Invalid choice!")
    
    # Get default value
    default_val = input(f"Enter default value (press Enter for NULL): ").strip()
    if not default_val:
        default_val = None
    elif col_type == 'INTEGER':
        try:
            default_val = int(default_val)
        except ValueError:
            print("⚠️  Invalid integer, using NULL")
            default_val = None
    elif col_type == 'REAL':
        try:
            default_val = float(default_val)
        except ValueError:
            print("⚠️  Invalid number, using NULL")
            default_val = None
    
    # Confirm
    print(f"\n📋 Column to be added:")
    print(f"   Name: {col_name}")
    print(f"   Type: {col_type}")
    print(f"   Default: {default_val if default_val is not None else 'NULL'}")
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return
    
    # Add the column
    try:
        if schema_manager.add_column(col_name, col_type, default_val):
            print(f"✅ Column '{col_name}' added successfully!")
            print("ℹ️  All existing contacts now have this field with the default value.")
        else:
            print(f"❌ Failed to add column '{col_name}'")
    except Exception as e:
        print(f"❌ Error adding column: {e}")
    
    input("\nPress Enter to continue...")


def remove_column_menu():
    """Remove a column from the database."""
    print("\n🗑️  Remove Column")
    print("=" * 50)
    
    # Get removable columns
    optional_columns = schema_manager.get_optional_columns()
    
    if not optional_columns:
        print("ℹ️  No removable columns available.")
        print("   The required columns (id, name, phone, email, created_at, updated_at) cannot be removed.")
        input("\nPress Enter to continue...")
        return
    
    print("Removable columns:")
    for i, col in enumerate(optional_columns, 1):
        col_display = col.replace('_', ' ').title()
        print(f"{i}. {col_display}")
    
    print(f"0. Cancel")
    
    while True:
        choice = input(f"\nEnter choice (0-{len(optional_columns)}): ").strip()
        try:
            choice_num = int(choice)
            if choice_num == 0:
                print("❌ Operation cancelled")
                return
            if 1 <= choice_num <= len(optional_columns):
                col_to_remove = optional_columns[choice_num - 1]
                break
            print(f"❌ Please enter a number between 0 and {len(optional_columns)}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Confirm
    print(f"\n⚠️  WARNING: This will permanently remove the '{col_to_remove}' column")
    print("   and all data in it from all contacts!")
    confirm = input("\nAre you sure? Type 'DELETE' to confirm: ").strip()
    
    if confirm != 'DELETE':
        print("❌ Operation cancelled")
        input("\nPress Enter to continue...")
        return
    
    # Remove the column
    try:
        if schema_manager.remove_column(col_to_remove):
            print(f"✅ Column '{col_to_remove}' removed successfully!")
        else:
            print(f"❌ Failed to remove column '{col_to_remove}'")
    except Exception as e:
        print(f"❌ Error removing column: {e}")
    
    input("\nPress Enter to continue...")

