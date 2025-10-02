"""
UI Module - User Interface Functions
Handles all display and formatting functions for the Contact Book Manager.
"""

# Import from core operations to avoid circular dependencies
from ..core.core_operations import (view_contacts, get_contact_by_id, search_contact, 
                            get_contact_analytics, get_database_stats, get_table_info,
                            validate_email, validate_phone, format_phone, check_data_integrity)
from ..core.schema_manager import schema_manager

def display_contacts(contacts, detailed=False):
    """Display contacts in a formatted way.
    
    Args:
        contacts: List of contact tuples
        detailed: If True, shows all fields. If False, shows compact view (ID, Name, Phone, Email)
    """
    if not contacts:
        print("📭 No contacts found!")
        return
    
    if detailed:
        # Detailed view - show all fields
        print("\n📋 Detailed Contact List:")
        print("=" * 120)
        
        for i, contact in enumerate(contacts, 1):
            # Use dynamic schema to map tuple to dict
            try:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                
                print(f"\n📇 Contact #{contact_dict.get('id', 'N/A')}")
                
                # Display all columns dynamically (except id which is already shown)
                columns = schema_manager.get_editable_columns()
                for column in columns:
                    value = contact_dict.get(column, '')
                    display_name = column.replace('_', ' ').title()
                    formatted_value = str(value) if value is not None else '(not provided)'
                    print(f"   {display_name:<12}: {formatted_value}")
                    
            except Exception as e:
                # Fallback to basic display if schema manager fails
                contact_id = str(contact[0]) if contact[0] is not None else 'N/A'
                print(f"\n📇 Contact #{contact_id}")
                print(f"   Raw data: {contact}")
            
            if i < len(contacts):
                print("-" * 120)
    else:
        # Compact view - show main fields dynamically
        try:
            columns = schema_manager.get_display_columns()
            
            print("\n📋 Contact List:")
            
            # Create dynamic header
            header_line = ""
            separator_length = 0
            column_widths = {}
            
            # Calculate column widths and build header
            for column in columns:
                if column == 'id':
                    width = 5
                elif column in ['name']:
                    width = 20
                elif column == 'phone':
                    width = 15
                elif column == 'email':
                    width = 50  # Extra wide for long email addresses
                elif column in ['created_at', 'updated_at']:
                    width = 25  # Enough for "2025-10-02 08:15:30 IST"
                else:
                    width = 12
                
                column_widths[column] = width
                separator_length += width + 1
                header_line += f"{column.title():<{width}} "
            
            print("-" * separator_length)
            print(header_line)
            print("-" * separator_length)
            
            # Display contacts dynamically
            for contact in contacts:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                line = ""
                for column in columns:
                    value = str(contact_dict.get(column, '')) if contact_dict.get(column) is not None else ''
                    width = column_widths[column]
                    line += f"{value:<{width}} "
                print(line)
                
        except Exception as e:
            # Fallback to simple display
            print("\n📋 Contact List:")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact}")

def display_contact_analytics():
    """Display contact analytics."""
    print("\n📈 Contact Analytics")
    print("-" * 30)
    
    try:
        analytics = get_contact_analytics()
        
        print(f"📊 Total Contacts: {analytics['total_contacts']}")
        print(f"📞 Contacts with Phone: {analytics['contacts_with_phone']} ({analytics['phone_percentage']}%)")
        print(f"📧 Contacts with Email: {analytics['contacts_with_email']} ({analytics['email_percentage']}%)")
        print(f"✅ Complete Contacts: {analytics['complete_contacts']} ({analytics['complete_percentage']}%)")
        
        if analytics['top_email_domains']:
            print("\n🌐 Top Email Domains:")
            for domain, count in analytics['top_email_domains']:
                print(f"   {domain}: {count} contacts")
        
    except Exception as e:
        print(f"❌ Error getting analytics: {e}")

def display_database_stats():
    """Display database statistics."""
    print("\n📊 Database Statistics")
    print("-" * 30)
    
    try:
        stats = get_database_stats()
        
        # Handle different key names from different adapters
        record_count = stats.get('record_count', stats.get('contact_count', 0))
        db_size_mb = stats.get('database_size_mb', stats.get('db_size_mb', 0))
        db_type = stats.get('database_type', 'Unknown')
        
        print(f"🗄️  Database Type: {db_type}")
        print(f"📈 Total Contacts: {record_count}")
        print(f"💾 Database Size: {db_size_mb} MB")
        
        # Show database-specific information
        if 'database_name' in stats:
            print(f"📋 Database Name: {stats['database_name']}")
        if 'database_path' in stats:
            print(f"📁 Database Path: {stats['database_path']}")
        if 'database_host' in stats:
            print(f"🌐 Host: {stats['database_host']}:{stats.get('database_port', 'N/A')}")
        
        # Get column info separately if needed
        try:
            from ..core.schema_manager import schema_manager
            columns = schema_manager.get_table_columns()
            print(f"🏗️  Total Columns: {len(columns)}")
            print(f"📋 Columns: {', '.join(columns)}")
        except Exception:
            pass
        
    except Exception as e:
        print(f"❌ Error getting database stats: {e}")

def display_table_structure():
    """Display table structure."""
    print("\n🏗️  Table Structure")
    print("-" * 30)
    
    try:
        columns = get_table_info()
        
        if not columns:
            print("📭 No table structure found!")
            return
        
        print(f"{'Column':<15} {'Type':<15} {'Nullable':<10} {'Default':<15}")
        print("-" * 60)
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            nullable = "YES" if col[3] == 0 else "NO"
            default = str(col[4]) if col[4] is not None else "None"
            
            print(f"{col_name:<15} {col_type:<15} {nullable:<10} {default:<15}")
            
    except Exception as e:
        print(f"❌ Error getting table structure: {e}")

def display_data_integrity_results():
    """Display data integrity check results."""
    print("\n🔍 Data Integrity Check")
    print("-" * 30)
    
    try:
        issues = check_data_integrity()
        
        if not issues:
            print("✅ No data integrity issues found!")
        else:
            print("⚠️  Data integrity issues found:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
                
    except Exception as e:
        print(f"❌ Error checking data integrity: {e}")

def display_validation_results(email=None, phone=None):
    """Display data validation results."""
    print("\n✅ Data Validation")
    print("-" * 30)
    
    try:
        if email:
            if validate_email(email):
                print(f"✅ Email '{email}' is valid!")
            else:
                print(f"❌ Email '{email}' is invalid!")
        
        if phone:
            if validate_phone(phone):
                formatted = format_phone(phone)
                print(f"✅ Phone '{phone}' is valid! Formatted: {formatted}")
            else:
                print(f"❌ Phone '{phone}' is invalid!")
                
    except Exception as e:
        print(f"❌ Error in data validation: {e}")

def display_search_results(results, search_term=""):
    """Display search results."""
    if not results:
        if search_term:
            print(f"📭 No contacts found matching '{search_term}'")
        else:
            print("📭 No contacts found!")
        return
    
    if search_term:
        print(f"\n🔍 Found {len(results)} contact(s) matching '{search_term}':")
    else:
        print(f"\n🔍 Found {len(results)} contact(s):")
    
    display_contacts(results)

def display_contact_preview(contact):
    """Display a contact preview for confirmation using dynamic schema."""
    if not contact:
        print("❌ Contact not found!")
        return

    # Use dynamic schema to map tuple to dict
    try:
        columns = schema_manager.get_table_columns()
        contact_dict = {}
        for i, col in enumerate(columns):
            contact_dict[col] = contact[i] if i < len(contact) else None
    except Exception:
        # Fallback: minimal mapping
        columns = ['id', 'name', 'phone', 'email']
        contact_dict = {
            'id': contact[0] if len(contact) > 0 else 'N/A',
            'name': contact[1] if len(contact) > 1 else 'N/A',
            'phone': contact[2] if len(contact) > 2 else '',
            'email': contact[3] if len(contact) > 3 else ''
        }

    print(f"\n📇 Contact Details:")
    for col in columns:
        # Display ID first
        if col == 'id':
            print(f"   ID:         {contact_dict.get('id', 'N/A')}")
            continue
        
        value = contact_dict.get(col)
        display_value = value if value not in [None, ''] else '(not provided)'
        col_display = col.replace('_', ' ').title()
        print(f"   {col_display}: {display_value}")

def display_operation_success(operation, count=None):
    """Display operation success message."""
    if count is not None:
        print(f"✅ {operation} successful! ({count} items affected)")
    else:
        print(f"✅ {operation} successful!")

def display_operation_error(operation, error):
    """Display operation error message."""
    print(f"❌ Error in {operation}: {error}")

def display_warning(message):
    """Display warning message."""
    print(f"⚠️  {message}")

def display_info(message):
    """Display info message."""
    print(f"ℹ️  {message}")

def display_success(message):
    """Display success message."""
    print(f"✅ {message}")

def display_error(message):
    """Display error message."""
    print(f"❌ {message}")
