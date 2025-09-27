"""
SQLite database adapter.
Wraps the existing ContactDatabase class to implement the DatabaseAdapter interface.
"""

import sqlite3
import csv
import json
import re
import shutil
import datetime
import os
from typing import List, Dict, Any, Optional, Tuple

from ..base import DatabaseAdapter


class SQLiteAdapter(DatabaseAdapter):
    """SQLite implementation of the DatabaseAdapter interface."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize SQLite adapter with configuration."""
        super().__init__(config)
        self.db_path = config.get('path', 'contacts.db')
    
    def get_connection(self):
        """Create and return a SQLite database connection."""
        return sqlite3.connect(self.db_path)
    
    def test_connection(self) -> bool:
        """Test if the SQLite database connection is working."""
        try:
            conn = self.get_connection()
            conn.execute("SELECT 1")
            conn.close()
            return True
        except Exception:
            return False
    
    def create_table(self) -> None:
        """Create the contacts table if it doesn't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            age INTEGER DEFAULT 0,
            address TEXT DEFAULT 'Unknown',
            department TEXT DEFAULT 'General',
            category TEXT DEFAULT 'General',
            tags TEXT DEFAULT ''
        )
        """)
        conn.commit()
        conn.close()
    
    def add_contact(self, name: str, phone: str, email: str) -> None:
        """Add a new contact to the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                       (name, phone, email))
        conn.commit()
        conn.close()
    
    def view_contacts(self) -> List[Tuple]:
        """Retrieve all contacts from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Tuple]:
        """Get a specific contact by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def update_contact_name(self, contact_id: int, new_name: str) -> None:
        """Update a contact's name."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET name = ? WHERE id = ?",
                       (new_name, contact_id))
        conn.commit()
        conn.close()
    
    def update_contact_phone(self, contact_id: int, new_phone: str) -> None:
        """Update a contact's phone number."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?",
                       (new_phone, contact_id))
        conn.commit()
        conn.close()
    
    def update_contact_email(self, contact_id: int, new_email: str) -> None:
        """Update a contact's email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET email = ? WHERE id = ?",
                       (new_email, contact_id))
        conn.commit()
        conn.close()
    
    def delete_contact(self, contact_id: int) -> None:
        """Delete a contact from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
    
    def search_contact(self, search_term: str) -> List[Tuple]:
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
    
    def advanced_search(self, filters: Dict[str, Any]) -> List[Tuple]:
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
            query += " WHERE " + " AND ".join(where_conditions)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def export_to_csv(self, filename: str) -> None:
        """Export contacts to CSV file."""
        contacts = self.view_contacts()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Age', 'Address', 'Department', 'Category', 'Tags'])
            # Write contacts
            for contact in contacts:
                writer.writerow(contact)
    
    def export_to_json(self, filename: str) -> None:
        """Export contacts to JSON file."""
        contacts = self.view_contacts()
        contacts_list = []
        for contact in contacts:
            contact_dict = {
                'id': contact[0],
                'name': contact[1],
                'phone': contact[2],
                'email': contact[3]
            }
            # Add additional fields if they exist
            if len(contact) > 4:
                contact_dict.update({
                    'age': contact[4] if len(contact) > 4 else 0,
                    'address': contact[5] if len(contact) > 5 else 'Unknown',
                    'department': contact[6] if len(contact) > 6 else 'General',
                    'category': contact[7] if len(contact) > 7 else 'General',
                    'tags': contact[8] if len(contact) > 8 else ''
                })
            contacts_list.append(contact_dict)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(contacts_list, jsonfile, indent=2, ensure_ascii=False)
    
    def import_from_csv(self, filename: str) -> int:
        """Import contacts from CSV file. Returns number of imported contacts."""
        imported_count = 0
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    self.add_contact(
                        name=row.get('Name', ''),
                        phone=row.get('Phone', ''),
                        email=row.get('Email', '')
                    )
                    imported_count += 1
                except Exception:
                    continue  # Skip invalid rows
        return imported_count
    
    def bulk_update(self, contact_ids: List[int], field: str, new_value: str) -> int:
        """Update multiple contacts at once. Returns number of updated contacts."""
        if not contact_ids or field not in ['name', 'phone', 'email']:
            return 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        query = f"UPDATE contacts SET {field} = ? WHERE id IN ({placeholders})"
        
        cursor.execute(query, [new_value] + contact_ids)
        updated_count = cursor.rowcount
        conn.commit()
        conn.close()
        return updated_count
    
    def bulk_delete(self, contact_ids: List[int]) -> int:
        """Delete multiple contacts at once. Returns number of deleted contacts."""
        if not contact_ids:
            return 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in contact_ids])
        query = f"DELETE FROM contacts WHERE id IN ({placeholders})"
        
        cursor.execute(query, contact_ids)
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count
    
    def get_contact_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contact analytics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total contacts
        cursor.execute("SELECT COUNT(*) FROM contacts")
        total_contacts = cursor.fetchone()[0]
        
        # Contacts with phone
        cursor.execute("SELECT COUNT(*) FROM contacts WHERE phone IS NOT NULL AND phone != ''")
        contacts_with_phone = cursor.fetchone()[0]
        
        # Contacts with email
        cursor.execute("SELECT COUNT(*) FROM contacts WHERE email IS NOT NULL AND email != ''")
        contacts_with_email = cursor.fetchone()[0]
        
        # Complete contacts (have both phone and email)
        cursor.execute("""
            SELECT COUNT(*) FROM contacts 
            WHERE phone IS NOT NULL AND phone != '' 
            AND email IS NOT NULL AND email != ''
        """)
        complete_contacts = cursor.fetchone()[0]
        
        # Email domains
        cursor.execute("""
            SELECT SUBSTR(email, INSTR(email, '@') + 1) as domain, COUNT(*) as count
            FROM contacts 
            WHERE email IS NOT NULL AND email != '' AND email LIKE '%@%'
            GROUP BY domain 
            ORDER BY count DESC 
            LIMIT 10
        """)
        email_domains = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_contacts': total_contacts,
            'contacts_with_phone': contacts_with_phone,
            'contacts_with_email': contacts_with_email,
            'complete_contacts': complete_contacts,
            'phone_percentage': (contacts_with_phone / total_contacts * 100) if total_contacts > 0 else 0,
            'email_percentage': (contacts_with_email / total_contacts * 100) if total_contacts > 0 else 0,
            'complete_percentage': (complete_contacts / total_contacts * 100) if total_contacts > 0 else 0,
            'top_email_domains': email_domains
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get database file size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        
        # Get table count
        cursor.execute("SELECT COUNT(*) FROM contacts")
        record_count = cursor.fetchone()[0]
        
        # Get database info
        cursor.execute("PRAGMA database_list")
        db_info = cursor.fetchall()
        
        conn.close()
        
        return {
            'database_type': 'SQLite',
            'database_path': self.db_path,
            'database_size_bytes': db_size,
            'database_size_mb': round(db_size / (1024 * 1024), 2),
            'record_count': record_count,
            'database_info': db_info
        }
    
    def get_table_info(self) -> List[Tuple]:
        """Get table structure information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(contacts)")
        table_info = cursor.fetchall()
        conn.close()
        return table_info
    
    def add_column(self, column_name: str, column_type: str, default_value: Any = None) -> None:
        """Add a new column to the contacts table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build ALTER TABLE statement
        alter_query = f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}"
        if default_value is not None:
            if isinstance(default_value, str):
                alter_query += f" DEFAULT '{default_value}'"
            else:
                alter_query += f" DEFAULT {default_value}"
        
        cursor.execute(alter_query)
        conn.commit()
        conn.close()
    
    def backup_database(self) -> str:
        """Create a backup of the database. Returns backup filename."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"contacts_backup_{timestamp}.db"
        backup_path = os.path.join("db_backup", backup_filename)
        
        # Create backup directory if it doesn't exist
        os.makedirs("db_backup", exist_ok=True)
        
        # Copy database file
        shutil.copy2(self.db_path, backup_path)
        return backup_filename
    
    def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup. Returns success status."""
        backup_path = os.path.join("db_backup", backup_filename)
        if not os.path.exists(backup_path):
            return False
        
        try:
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception:
            return False
    
    def cleanup_db(self) -> int:
        """Clean up database (remove empty records, etc.). Returns number of cleaned records."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Remove contacts with empty names
        cursor.execute("DELETE FROM contacts WHERE name IS NULL OR name = ''")
        cleaned_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        return cleaned_count
    
    def full_cleanup_db(self) -> bool:
        """Perform full database cleanup. Returns success status."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Remove duplicate contacts (same name, phone, and email)
            cursor.execute("""
                DELETE FROM contacts WHERE id NOT IN (
                    SELECT MIN(id) FROM contacts 
                    GROUP BY name, phone, email
                )
            """)
            
            # Vacuum database to reclaim space
            cursor.execute("VACUUM")
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
