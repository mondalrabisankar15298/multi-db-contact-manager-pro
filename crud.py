# Import from core operations module to avoid circular dependencies
from core_operations import *

# This file is kept for backward compatibility
# All actual implementations are now in core_operations.py

# Legacy function for backward compatibility
def update_contact(contact_id, new_phone):
    """Update a contact's phone number. (Legacy function for backward compatibility)"""
    update_contact_phone(contact_id, new_phone)

def search_by_pattern(pattern, field='all'):
    """Search using regex-like patterns."""
    from core_operations import default_db
    conn = default_db.get_connection()
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

def remove_column(column_name):
    """Remove a column from the contacts table (SQLite limitation - requires table recreation)."""
    from core_operations import default_db
    conn = default_db.get_connection()
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
    from core_operations import default_db
    conn = default_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_contacts_by_tag(tag):
    """Get contacts containing a specific tag."""
    from core_operations import default_db
    conn = default_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE tags LIKE ?", (f"%{tag}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows
