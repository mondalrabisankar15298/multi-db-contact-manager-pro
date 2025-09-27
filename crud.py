from db import get_connection

def create_table():
    """Create the contacts table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_contact(name, phone, email):
    """Add a new contact to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                   (name, phone, email))
    conn.commit()
    conn.close()

def view_contacts():
    """Retrieve all contacts from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_contact_phone(contact_id, new_phone):
    """Update a contact's phone number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?",
                   (new_phone, contact_id))
    conn.commit()
    conn.close()

def update_contact_name(contact_id, new_name):
    """Update a contact's name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name = ? WHERE id = ?",
                   (new_name, contact_id))
    conn.commit()
    conn.close()

def update_contact_email(contact_id, new_email):
    """Update a contact's email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET email = ? WHERE id = ?",
                   (new_email, contact_id))
    conn.commit()
    conn.close()

def update_contact(contact_id, new_phone):
    """Update a contact's phone number. (Legacy function for backward compatibility)"""
    update_contact_phone(contact_id, new_phone)

def delete_contact(contact_id):
    """Delete a contact from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

def search_contact(search_term):
    """Search for contacts by name, phone, or email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts 
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_contact_by_id(contact_id):
    """Get a specific contact by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def cleanup_db():
    """Delete all contacts from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()

def reset_auto_increment():
    """Reset the auto-increment counter for the contacts table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='contacts'")
    conn.commit()
    conn.close()

def full_cleanup_db():
    """Complete database cleanup - removes all contacts and resets auto-increment."""
    cleanup_db()
    reset_auto_increment()

def get_table_info():
    """Get information about the contacts table structure."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(contacts)")
    columns = cursor.fetchall()
    conn.close()
    return columns

def add_column(column_name, column_type, default_value=None):
    """Add a new column to the contacts table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if default_value is not None:
            cursor.execute(f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type} DEFAULT '{default_value}'")
        else:
            cursor.execute(f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e

def remove_column(column_name):
    """Remove a column from the contacts table (SQLite limitation - requires table recreation)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get current table structure
        cursor.execute("PRAGMA table_info(contacts)")
        columns = cursor.fetchall()
        
        # Create new table without the specified column
        remaining_columns = []
        for col in columns:
            if col[1] != column_name:  # col[1] is column name
                remaining_columns.append(f"{col[1]} {col[2]}")
        
        # Create new table
        new_table_sql = f"""
        CREATE TABLE contacts_new (
            {', '.join(remaining_columns)}
        )
        """
        cursor.execute(new_table_sql)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO contacts_new 
            SELECT {columns} FROM contacts
        """.format(columns=', '.join([col[1] for col in columns if col[1] != column_name])))
        
        # Drop old table and rename new table
        cursor.execute("DROP TABLE contacts")
        cursor.execute("ALTER TABLE contacts_new RENAME TO contacts")
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e

def backup_database():
    """Create a backup of the current database."""
    import shutil
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"contacts_backup_{timestamp}.db"
    
    try:
        shutil.copy2("contacts.db", backup_filename)
        return backup_filename
    except Exception as e:
        raise e

def restore_database(backup_filename):
    """Restore database from backup."""
    import shutil
    
    try:
        shutil.copy2(backup_filename, "contacts.db")
        return True
    except Exception as e:
        raise e

def get_database_stats():
    """Get database statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get contact count
    cursor.execute("SELECT COUNT(*) FROM contacts")
    contact_count = cursor.fetchone()[0]
    
    # Get table info
    cursor.execute("PRAGMA table_info(contacts)")
    columns = cursor.fetchall()
    
    # Get database file size
    import os
    db_size = os.path.getsize("contacts.db") if os.path.exists("contacts.db") else 0
    
    conn.close()
    
    return {
        'contact_count': contact_count,
        'column_count': len(columns),
        'columns': [col[1] for col in columns],
        'db_size_bytes': db_size,
        'db_size_mb': round(db_size / (1024 * 1024), 2)
    }

# Advanced Export/Import Functions
def export_to_csv(filename="contacts_export.csv"):
    """Export contacts to CSV file."""
    import csv
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)
    
    conn.close()
    return filename

def export_to_json(filename="contacts_export.json"):
    """Export contacts to JSON file."""
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Convert to list of dictionaries
    contacts = []
    for row in rows:
        contact = {}
        for i, col in enumerate(columns):
            contact[col] = row[i]
        contacts.append(contact)
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(contacts, jsonfile, indent=2, ensure_ascii=False)
    
    conn.close()
    return filename

def import_from_csv(filename):
    """Import contacts from CSV file."""
    import csv
    conn = get_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract values, handling missing columns
            name = row.get('name', '')
            phone = row.get('phone', '')
            email = row.get('email', '')
            
            if name:  # Only import if name is provided
                cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                             (name, phone, email))
                imported_count += 1
    
    conn.commit()
    conn.close()
    return imported_count

# Advanced Search Functions
def advanced_search(filters):
    """Advanced search with multiple filters."""
    conn = get_connection()
    cursor = conn.cursor()
    
    where_conditions = []
    params = []
    
    if filters.get('name'):
        where_conditions.append("name LIKE ?")
        params.append(f"%{filters['name']}%")
    
    if filters.get('phone'):
        where_conditions.append("phone LIKE ?")
        params.append(f"%{filters['phone']}%")
    
    if filters.get('email'):
        where_conditions.append("email LIKE ?")
        params.append(f"%{filters['email']}%")
    
    if filters.get('min_id'):
        where_conditions.append("id >= ?")
        params.append(filters['min_id'])
    
    if filters.get('max_id'):
        where_conditions.append("id <= ?")
        params.append(filters['max_id'])
    
    query = "SELECT * FROM contacts"
    if where_conditions:
        query += " WHERE " + " AND ".join(where_conditions)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_by_pattern(pattern, field='all'):
    """Search using regex-like patterns."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if field == 'all':
        cursor.execute("""
            SELECT * FROM contacts 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
    else:
        cursor.execute(f"SELECT * FROM contacts WHERE {field} LIKE ?", (f"%{pattern}%",))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

# Bulk Operations
def bulk_update(contact_ids, field, new_value):
    """Update multiple contacts at once."""
    conn = get_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join(['?' for _ in contact_ids])
    cursor.execute(f"UPDATE contacts SET {field} = ? WHERE id IN ({placeholders})",
                   [new_value] + contact_ids)
    
    conn.commit()
    conn.close()
    return cursor.rowcount

def bulk_delete(contact_ids):
    """Delete multiple contacts at once."""
    conn = get_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join(['?' for _ in contact_ids])
    cursor.execute(f"DELETE FROM contacts WHERE id IN ({placeholders})", contact_ids)
    
    conn.commit()
    conn.close()
    return cursor.rowcount

# Data Analytics
def get_contact_analytics():
    """Get detailed analytics about contacts."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total contacts
    cursor.execute("SELECT COUNT(*) FROM contacts")
    total_contacts = cursor.fetchone()[0]
    
    # Contacts with phone numbers
    cursor.execute("SELECT COUNT(*) FROM contacts WHERE phone IS NOT NULL AND phone != ''")
    contacts_with_phone = cursor.fetchone()[0]
    
    # Contacts with email
    cursor.execute("SELECT COUNT(*) FROM contacts WHERE email IS NOT NULL AND email != ''")
    contacts_with_email = cursor.fetchone()[0]
    
    # Contacts with both phone and email
    cursor.execute("SELECT COUNT(*) FROM contacts WHERE phone IS NOT NULL AND phone != '' AND email IS NOT NULL AND email != ''")
    contacts_complete = cursor.fetchone()[0]
    
    # Most common email domains
    cursor.execute("""
        SELECT SUBSTR(email, INSTR(email, '@') + 1) as domain, COUNT(*) as count 
        FROM contacts 
        WHERE email IS NOT NULL AND email != '' AND email LIKE '%@%'
        GROUP BY domain 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_domains = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_contacts': total_contacts,
        'contacts_with_phone': contacts_with_phone,
        'contacts_with_email': contacts_with_email,
        'contacts_complete': contacts_complete,
        'phone_percentage': round((contacts_with_phone / total_contacts * 100) if total_contacts > 0 else 0, 1),
        'email_percentage': round((contacts_with_email / total_contacts * 100) if total_contacts > 0 else 0, 1),
        'complete_percentage': round((contacts_complete / total_contacts * 100) if total_contacts > 0 else 0, 1),
        'top_domains': top_domains
    }

# Data Validation
def validate_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format."""
    import re
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Check if it has 7-15 digits
    return 7 <= len(digits) <= 15

def format_phone(phone):
    """Format phone number consistently."""
    import re
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

# Contact Categories and Tags
def add_category_column():
    """Add category column to contacts table."""
    try:
        add_column('category', 'TEXT', 'General')
        return True
    except:
        return False

def add_tag_column():
    """Add tags column to contacts table."""
    try:
        add_column('tags', 'TEXT', '')
        return True
    except:
        return False

def get_contacts_by_category(category):
    """Get contacts by category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_contacts_by_tag(tag):
    """Get contacts containing a specific tag."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE tags LIKE ?", (f"%{tag}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Data Integrity
def check_data_integrity():
    """Check for data integrity issues."""
    conn = get_connection()
    cursor = conn.cursor()
    
    issues = []
    
    # Check for duplicate names
    cursor.execute("SELECT name, COUNT(*) FROM contacts GROUP BY name HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    if duplicates:
        issues.append(f"Duplicate names found: {[name for name, count in duplicates]}")
    
    # Check for invalid emails
    cursor.execute("SELECT id, email FROM contacts WHERE email IS NOT NULL AND email != ''")
    contacts_with_email = cursor.fetchall()
    invalid_emails = []
    for contact_id, email in contacts_with_email:
        if not validate_email(email):
            invalid_emails.append((contact_id, email))
    
    if invalid_emails:
        issues.append(f"Invalid email formats found: {invalid_emails}")
    
    # Check for empty names
    cursor.execute("SELECT id FROM contacts WHERE name IS NULL OR name = ''")
    empty_names = cursor.fetchall()
    if empty_names:
        issues.append(f"Empty names found: {[id for id, in empty_names]}")
    
    conn.close()
    return issues
