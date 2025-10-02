"""
Dynamic UI Module - Generates UI elements based on current database schema
"""

from typing import List, Dict, Any
from ..core.schema_manager import schema_manager
from ..core.core_operations import validate_email, validate_phone, format_phone


def display_contacts_dynamic(contacts: List[tuple], detailed: bool = False):
    """Display contacts dynamically based on current schema."""
    if not contacts:
        print("📭 No contacts found!")
        return
    
    columns = schema_manager.get_display_columns()
    
    if not columns:
        print("❌ Unable to determine table structure")
        return
    
    if detailed:
        # Detailed view - one contact per block
        print("\n📋 Detailed Contact List:")
        print("=" * 80)
        
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            
            # Display ID prominently
            contact_id = contact_dict.get('id', 'N/A')
            print(f"\n📇 Contact #{contact_id}")
            
            # Display all other fields
            for col in columns:
                if col != 'id':  # Skip ID since we already showed it
                    value = contact_dict.get(col, '')
                    display_value = value if value not in [None, ''] else '(not provided)'
                    # Capitalize column name for display
                    col_display = col.replace('_', ' ').title()
                    print(f"   {col_display:<15} {display_value}")
            
            print("-" * 80)
    else:
        # Compact view - show all columns (up to 6)
        display_cols = columns
        
        # Calculate column widths dynamically
        col_widths = {}
        for col in display_cols:
            if col == 'id':
                col_widths[col] = 5
            elif col == 'name':
                col_widths[col] = 20
            elif col == 'phone':
                col_widths[col] = 15
            elif col == 'email':
                col_widths[col] = 50  # Extra wide for long email addresses
            elif col in ['created_at', 'updated_at']:
                col_widths[col] = 25  # Enough for "2025-10-02 08:15:30 IST"
            else:
                col_widths[col] = 15
        
        # Print header
        print("\n📋 Contact List:")
        total_width = sum(col_widths.values()) + len(display_cols) - 1
        print("-" * total_width)
        
        header = ' '.join([col.upper()[:col_widths[col]].ljust(col_widths[col]) 
                          for col in display_cols])
        print(header)
        print("-" * total_width)
        
        # Print contacts
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            row = []
            for col in display_cols:
                value = str(contact_dict.get(col, ''))
                if not value or value == 'None':
                    value = ''
                row.append(value[:col_widths[col]].ljust(col_widths[col]))
            print(' '.join(row))
        
        # Note: Now showing all columns in compact view


def get_contact_input_dynamic() -> Dict[str, Any]:
    """Get contact input dynamically based on current schema."""
    columns = schema_manager.get_table_columns()
    editable_columns = [col for col in columns if col != 'id']
    
    contact_data = {}
    
    print("\n📝 Enter Contact Information:")
    print("=" * 50)
    print("(Type '0' to cancel, or '111' to exit at any time)")
    
    for col in editable_columns:
        # Format prompt
        col_display = col.replace('_', ' ').title()
        is_required = (col == 'name')
        prompt = f"{col_display}{'*' if is_required else ''}: "
        
        while True:
            value_raw = input(prompt).strip()
            
            # Allow cancellation or exit
            if value_raw.lower() in ('q', 'quit', 'cancel', 'abort', 'back') or value_raw == '0':
                print("ℹ️  Add contact aborted.")
                return None
            if value_raw == '111':
                print("\n👋 Thank you for using Contact Book Manager!")
                print("Goodbye! 👋")
                raise SystemExit(0)
            
            value = value_raw
            
            # Handle required fields
            if is_required and not value:
                print(f"❌ {col_display} is required!")
                continue
            
            # Empty value for optional fields
            if not value and not is_required:
                break
            
            # Field-specific validation
            if col == 'email' and value:
                if not validate_email(value):
                    print("❌ Invalid email format. Please enter a valid email (e.g., user@example.com).")
                    continue
            
            if col == 'phone' and value:
                if not validate_phone(value):
                    print("❌ Invalid phone number. Enter 7-15 digits; separators are allowed.")
                    continue
                # Format phone consistently
                value = format_phone(value)
            
            # Store the value
            contact_data[col] = value
            break
    
    return contact_data


def get_update_field_choice() -> str:
    """Get which field to update based on current schema."""
    editable_columns = schema_manager.get_editable_columns()
    
    print("\n✏️  Which field would you like to update?")
    print("=" * 50)
    print("0. 🔙 Back to Previous Menu")
    print("111. 🚪 Exit Application")
    
    for i, col in enumerate(editable_columns, 1):
        col_display = col.replace('_', ' ').title()
        print(f"{i}. {col_display}")
    
    while True:
        choice = input(f"\nEnter choice (0-{len(editable_columns)}, 111): ").strip()
        if choice == '0':
            return None
        if choice == '111':
            print("\n👋 Thank you for using Contact Book Manager!")
            print("Goodbye! 👋")
            raise SystemExit(0)
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(editable_columns):
                return editable_columns[choice_num - 1]
            else:
                print(f"❌ Please enter a number between 0 and {len(editable_columns)} or 111")
        except ValueError:
            print("❌ Please enter a valid number")


def display_schema_info():
    """Display current database schema information."""
    print("\n🗄️  Current Database Schema")
    print("=" * 80)
    
    columns_info = schema_manager.get_column_info()
    
    print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Default':<15}")
    print("-" * 80)
    
    for col_info in columns_info:
        col_name = col_info.get('name', 'N/A')
        col_type = col_info.get('type', 'N/A')
        nullable = 'YES' if col_info.get('nullable', True) else 'NO'
        default = str(col_info.get('default', 'NULL'))
        
        # Mark primary key and required fields
        if col_info.get('primary_key'):
            col_name += ' (PK)'
        elif col_name in schema_manager.REQUIRED_COLUMNS:
            col_name += ' *'
        
        print(f"{col_name:<20} {col_type:<15} {nullable:<10} {default:<15}")
    
    print("\n* = Required field, cannot be removed")
    print(f"\nTotal columns: {len(columns_info)}")


def display_column_management_menu():
    """Display column management menu."""
    print("\n🛠️  Column Management")
    print("=" * 50)
    print("1. View current schema")
    print("2. Add new column")
    print("3. Remove column")
    print("0. 🔙 Back to Previous Menu")
    print("=" * 50)

