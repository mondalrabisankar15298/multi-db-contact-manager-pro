"""
UI Module - User Interface Functions
Handles all display and formatting functions for the Contact Book Manager.
"""

# Import from core operations to avoid circular dependencies
from core_operations import (view_contacts, get_contact_by_id, search_contact, 
                            get_contact_analytics, get_database_stats, get_table_info,
                            validate_email, validate_phone, format_phone, check_data_integrity)

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
            contact_id = str(contact[0]) if contact[0] is not None else 'N/A'
            name = str(contact[1]) if len(contact) > 1 and contact[1] is not None else 'N/A'
            phone = str(contact[2]) if len(contact) > 2 and contact[2] is not None else ''
            email = str(contact[3]) if len(contact) > 3 and contact[3] is not None else ''
            age = str(contact[4]) if len(contact) > 4 and contact[4] is not None else '0'
            address = str(contact[5]) if len(contact) > 5 and contact[5] is not None else 'Unknown'
            department = str(contact[6]) if len(contact) > 6 and contact[6] is not None else 'General'
            category = str(contact[7]) if len(contact) > 7 and contact[7] is not None else 'General'
            tags = str(contact[8]) if len(contact) > 8 and contact[8] is not None else ''
            
            print(f"\n📇 Contact #{contact_id}")
            print(f"   Name:       {name}")
            print(f"   Phone:      {phone or '(not provided)'}")
            print(f"   Email:      {email or '(not provided)'}")
            print(f"   Age:        {age}")
            print(f"   Address:    {address}")
            print(f"   Department: {department}")
            print(f"   Category:   {category}")
            print(f"   Tags:       {tags or '(no tags)'}")
            
            if i < len(contacts):
                print("-" * 120)
    else:
        # Compact view - show only main fields
        print("\n📋 Contact List:")
        print("-" * 60)
        print(f"{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<20}")
        print("-" * 60)
        
        for contact in contacts:
            contact_id = str(contact[0]) if contact[0] is not None else 'N/A'
            name = str(contact[1]) if contact[1] is not None else 'N/A'
            phone = str(contact[2]) if len(contact) > 2 and contact[2] is not None else ''
            email = str(contact[3]) if len(contact) > 3 and contact[3] is not None else ''
            print(f"{contact_id:<5} {name:<20} {phone:<15} {email:<20}")

def display_contact_analytics():
    """Display contact analytics."""
    print("\n📈 Contact Analytics")
    print("-" * 30)
    
    try:
        analytics = get_contact_analytics()
        
        print(f"📊 Total Contacts: {analytics['total_contacts']}")
        print(f"📞 Contacts with Phone: {analytics['contacts_with_phone']} ({analytics['phone_percentage']}%)")
        print(f"📧 Contacts with Email: {analytics['contacts_with_email']} ({analytics['email_percentage']}%)")
        print(f"✅ Complete Contacts: {analytics['contacts_complete']} ({analytics['complete_percentage']}%)")
        
        if analytics['top_domains']:
            print("\n🌐 Top Email Domains:")
            for domain, count in analytics['top_domains']:
                print(f"   {domain}: {count} contacts")
        
    except Exception as e:
        print(f"❌ Error getting analytics: {e}")

def display_database_stats():
    """Display database statistics."""
    print("\n📊 Database Statistics")
    print("-" * 30)
    
    try:
        stats = get_database_stats()
        
        print(f"📈 Total Contacts: {stats['contact_count']}")
        print(f"🏗️  Total Columns: {stats['column_count']}")
        print(f"💾 Database Size: {stats['db_size_mb']} MB")
        print(f"📋 Columns: {', '.join(stats['columns'])}")
        
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
        from schema_manager import schema_manager
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
