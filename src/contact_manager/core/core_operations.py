"""
Core Operations Module - Pure Business Logic
Contains all database operations and business logic without UI dependencies.
This module can be imported safely without triggering the UI.
"""

import sqlite3
import csv
import json
import re
import shutil
import datetime
import os

class ContactDatabase:
    """Core database operations for contact management."""
    
    def __init__(self, db_path="contacts.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_path)
    
    def create_table(self):
        """Create the contacts table if it doesn't exist."""
        conn = self.get_connection()
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
    
    # CRUD Operations
    def add_contact(self, name, phone, email):
        """Add a new contact to the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                       (name, phone, email))
        conn.commit()
        conn.close()
    
    def view_contacts(self):
        """Retrieve all contacts from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_contact_by_id(self, contact_id):
        """Get a specific contact by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def update_contact_name(self, contact_id, new_name):
        """Update a contact's name."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET name = ? WHERE id = ?",
                       (new_name, contact_id))
        conn.commit()
        conn.close()
    
    def update_contact_phone(self, contact_id, new_phone):
        """Update a contact's phone number."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?",
                       (new_phone, contact_id))
        conn.commit()
        conn.close()
    
    def update_contact_email(self, contact_id, new_email):
        """Update a contact's email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET email = ? WHERE id = ?",
                       (new_email, contact_id))
        conn.commit()
        conn.close()
    
    def delete_contact(self, contact_id):
        """Delete a contact from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
    
    # Search Operations
    def search_contact(self, search_term):
        """Search for contacts by name, phone, or email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM contacts 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def advanced_search(self, filters):
        """Advanced search with multiple filters."""
        conn = self.get_connection()
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
            query += " WHERE " + " OR ".join(where_conditions)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    # Export/Import Operations
    def export_to_csv(self, filename="contacts_export.csv"):
        """Export contacts to CSV file."""
        conn = self.get_connection()
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
    
    def export_to_json(self, filename="contacts_export.json"):
        """Export contacts to JSON file."""
        conn = self.get_connection()
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
    
    def import_from_csv(self, filename):
        """Import contacts from CSV file."""
        conn = self.get_connection()
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
    
    # Bulk Operations
    def bulk_update(self, contact_ids, field, new_value):
        """Update multiple contacts at once."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        cursor.execute(f"UPDATE contacts SET {field} = ? WHERE id IN ({placeholders})",
                       [new_value] + contact_ids)
        
        conn.commit()
        updated_count = cursor.rowcount
        conn.close()
        return updated_count
    
    def bulk_delete(self, contact_ids):
        """Delete multiple contacts at once."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        cursor.execute(f"DELETE FROM contacts WHERE id IN ({placeholders})", contact_ids)
        
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        return deleted_count
    
    # Analytics
    def get_contact_analytics(self):
        """Get detailed analytics about contacts."""
        conn = self.get_connection()
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
    
    # Database Management
    def get_database_stats(self):
        """Get database statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get contact count
        cursor.execute("SELECT COUNT(*) FROM contacts")
        contact_count = cursor.fetchone()[0]
        
        # Get table info
        cursor.execute("PRAGMA table_info(contacts)")
        columns = cursor.fetchall()
        
        # Get database file size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        
        conn.close()
        
        return {
            'contact_count': contact_count,
            'column_count': len(columns),
            'columns': [col[1] for col in columns],
            'db_size_bytes': db_size,
            'db_size_mb': round(db_size / (1024 * 1024), 2)
        }
    
    def get_table_info(self):
        """Get information about the contacts table structure."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(contacts)")
        columns = cursor.fetchall()
        conn.close()
        return columns
    
    def add_column(self, column_name, column_type, default_value=None):
        """Add a new column to the contacts table."""
        conn = self.get_connection()
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
    
    def backup_database(self):
        """Create a backup of the current database."""
        import os

        # Create db_backup directory if it doesn't exist
        backup_dir = "db_backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(backup_dir, f"contacts_backup_{timestamp}.db")

        try:
            shutil.copy2(self.db_path, backup_filename)
            return backup_filename
        except Exception as e:
            raise e
    
    def restore_database(self, backup_filename):
        """Restore database from backup."""
        try:
            shutil.copy2(backup_filename, self.db_path)
            return True
        except Exception as e:
            raise e
    
    def cleanup_db(self):
        """Delete all contacts from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts")
        conn.commit()
        conn.close()
    
    def reset_auto_increment(self):
        """Reset the auto-increment counter for the contacts table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='contacts'")
        conn.commit()
        conn.close()
    
    def full_cleanup_db(self):
        """Complete database cleanup - removes all contacts and resets auto-increment."""
        self.cleanup_db()
        self.reset_auto_increment()


class DataValidator:
    """Data validation utilities."""
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Check if it has 7-15 digits
        return 7 <= len(digits) <= 15
    
    @staticmethod
    def format_phone(phone):
        """Format phone number consistently."""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return phone  # Return original if can't format


class DataIntegrity:
    """Data integrity checking utilities."""
    
    def __init__(self, db):
        self.db = db
    
    def check_data_integrity(self):
        """Check for data integrity issues."""
        conn = self.db.get_connection()
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
            if not DataValidator.validate_email(email):
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


# Import database manager for multi-database support
from ..database.manager import db_manager

# Create a default instance for backward compatibility
# Now uses the database manager which handles database switching
default_db = db_manager.current_adapter
validator = DataValidator()

# Export functions for backward compatibility with existing code
# These functions now use the current database adapter from db_manager
def create_table():
    return db_manager.current_adapter.create_table()

def add_contact(**fields):
    """Add contact with dynamic fields."""
    return db_manager.current_adapter.add_contact(**fields)

def update_contact(contact_id, **fields):
    """Update contact with dynamic fields."""
    return db_manager.current_adapter.update_contact(contact_id, **fields)

def view_contacts():
    return db_manager.current_adapter.view_contacts()

def get_contact_by_id(contact_id):
    return db_manager.current_adapter.get_contact_by_id(contact_id)

def update_contact_name(contact_id, new_name):
    return db_manager.current_adapter.update_contact_name(contact_id, new_name)

def update_contact_phone(contact_id, new_phone):
    return db_manager.current_adapter.update_contact_phone(contact_id, new_phone)

def update_contact_email(contact_id, new_email):
    return db_manager.current_adapter.update_contact_email(contact_id, new_email)

def delete_contact(contact_id):
    return db_manager.current_adapter.delete_contact(contact_id)

def search_contact(search_term):
    return db_manager.current_adapter.search_contact(search_term)

def advanced_search(filters):
    return db_manager.current_adapter.advanced_search(filters)

def export_to_csv(filename=None):
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"contacts_export_{timestamp}.csv"
    return db_manager.current_adapter.export_to_csv(filename)

def export_to_json(filename=None):
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"contacts_export_{timestamp}.json"
    return db_manager.current_adapter.export_to_json(filename)

def import_from_csv(filename):
    return db_manager.current_adapter.import_from_csv(filename)

def bulk_update(contact_ids, field, new_value):
    return db_manager.current_adapter.bulk_update(contact_ids, field, new_value)

def bulk_delete(contact_ids):
    return db_manager.current_adapter.bulk_delete(contact_ids)

def get_contact_analytics():
    return db_manager.current_adapter.get_contact_analytics()

def get_database_stats():
    return db_manager.current_adapter.get_database_stats()

def get_table_info():
    return db_manager.current_adapter.get_table_info()

def add_column(column_name, column_type, default_value=None):
    return db_manager.current_adapter.add_column(column_name, column_type, default_value)

def backup_database():
    return db_manager.current_adapter.backup_database()

def restore_database(backup_filename):
    return db_manager.current_adapter.restore_database(backup_filename)

def cleanup_db():
    return db_manager.current_adapter.cleanup_db()

def full_cleanup_db():
    return db_manager.current_adapter.full_cleanup_db()

def reset_table_structure():
    """Reset table to base 4-column structure (deletes table and recreates)."""
    return db_manager.current_adapter.reset_table_structure()

def validate_email(email):
    return validator.validate_email(email)

def validate_phone(phone):
    return validator.validate_phone(phone)

def format_phone(phone):
    return validator.format_phone(phone)

def check_data_integrity():
    integrity_checker = DataIntegrity(db_manager.current_adapter)
    return integrity_checker.check_data_integrity()

# Additional helper functions for database management
def get_current_database_type():
    """Get the current database type."""
    return db_manager.current_db_type

def get_current_database_info():
    """Get information about the current database connection."""
    return db_manager.get_connection_info()

def switch_database(db_type, config=None):
    """Switch to a different database."""
    return db_manager.switch_database(db_type, config)

def get_available_databases():
    """Get list of available database types."""
    return db_manager.get_available_databases()

def test_database_connection():
    """Test the current database connection."""
    return db_manager.test_current_connection()
