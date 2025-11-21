"""
PostgreSQL database adapter using psycopg2.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import json
import datetime
import os
from typing import List, Dict, Any, Optional, Tuple

from ..base import DatabaseAdapter
from ...core.schema_manager import schema_manager


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL implementation of the DatabaseAdapter interface."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize PostgreSQL adapter with configuration."""
        super().__init__(config)
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 5432)
        self.user = config.get('user', 'contact_user')
        self.password = config.get('password', 'contact_password')
        self.database = config.get('database', 'contacts')
    
    def get_connection(self):
        """Create and return a PostgreSQL database connection with UTC timezone."""
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database
        )
        # Set timezone to UTC for this connection
        with conn.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'UTC'")
        conn.commit()
        return conn
    
    def test_connection(self) -> bool:
        """Test if the PostgreSQL database connection is working."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"PostgreSQL connection test failed: {e}")
            return False
    
    def create_table(self) -> None:
        """Create the contacts table with 6 columns including timestamps."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create table with timestamps
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(50),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
        )
        """)
        
        # Create function for updating updated_at column
        cursor.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = (NOW() AT TIME ZONE 'UTC');
            RETURN NEW;
        END;
        $$ language 'plpgsql'
        """)
        
        # Create trigger to automatically update updated_at column
        cursor.execute("""
        DROP TRIGGER IF EXISTS update_contacts_updated_at ON contacts
        """)
        cursor.execute("""
        CREATE TRIGGER update_contacts_updated_at 
            BEFORE UPDATE ON contacts 
            FOR EACH ROW 
            EXECUTE FUNCTION update_updated_at_column()
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def add_contact(self, **fields) -> None:
        """Add a new contact to the database (dynamic fields)."""
        if 'name' not in fields:
            raise ValueError("Name is required")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'contacts' AND column_name != 'id'
        """)
        valid_columns = [row[0] for row in cursor.fetchall()]
        
        # Filter fields to only include valid columns
        insert_fields = {k: v for k, v in fields.items() if k in valid_columns}
        
        # Don't manually set timestamps - PostgreSQL handles them automatically with DEFAULT CURRENT_TIMESTAMP
        # Remove timestamp fields if they were passed in (let PostgreSQL handle them)
        insert_fields.pop('created_at', None)
        insert_fields.pop('updated_at', None)
        
        if not insert_fields:
            cursor.close()
            conn.close()
            raise ValueError("No valid fields to insert")
        
        # Build dynamic INSERT query
        columns = ', '.join(insert_fields.keys())
        placeholders = ', '.join(['%s' for _ in insert_fields])
        query = f"INSERT INTO contacts ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(insert_fields.values()))
        conn.commit()
        cursor.close()
        conn.close()
    
    def view_contacts(self) -> List[Tuple]:
        """Retrieve all contacts from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Tuple]:
        """Get a specific contact by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    
    def update_contact(self, contact_id: int, **fields) -> None:
        """Update contact fields dynamically."""
        if not fields:
            raise ValueError("No fields to update")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'contacts' AND column_name != 'id'
        """)
        valid_columns = [row[0] for row in cursor.fetchall()]
        
        # Filter fields to only include valid columns
        update_fields = {k: v for k, v in fields.items() if k in valid_columns}
        
        # Don't manually set timestamps - PostgreSQL handles updated_at automatically with trigger
        # Remove timestamp fields if they were passed in (let PostgreSQL handle them)
        update_fields.pop('created_at', None)  # Never update created_at
        update_fields.pop('updated_at', None)  # Let PostgreSQL trigger handle updated_at automatically
        
        if not update_fields:
            cursor.close()
            conn.close()
            raise ValueError("No valid fields to update")
        
        # Build dynamic UPDATE query
        set_clause = ', '.join([f"{col} = %s" for col in update_fields.keys()])
        query = f"UPDATE contacts SET {set_clause} WHERE id = %s"
        
        values = list(update_fields.values()) + [contact_id]
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
    
    # Backward compatibility methods
    def update_contact_name(self, contact_id: int, new_name: str) -> None:
        """Update a contact's name."""
        self.update_contact(contact_id, name=new_name)
    
    def update_contact_phone(self, contact_id: int, new_phone: str) -> None:
        """Update a contact's phone number."""
        self.update_contact(contact_id, phone=new_phone)
    
    def update_contact_email(self, contact_id: int, new_email: str) -> None:
        """Update a contact's email."""
        self.update_contact(contact_id, email=new_email)
    
    def delete_contact(self, contact_id: int) -> None:
        """Delete a contact from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def search_contact(self, search_term: str) -> List[Tuple]:
        """Search for contacts by name, phone, or email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute("""
            SELECT * FROM contacts 
            WHERE name ILIKE %s OR phone ILIKE %s OR email ILIKE %s
            ORDER BY id
        """, (search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    def advanced_search(self, filters: Dict[str, Any]) -> List[Tuple]:
        """Advanced search with multiple filters."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_conditions = []
        params = []
        
        if filters.get('name'):
            where_conditions.append("name ILIKE %s")
            params.append(f"%{filters['name']}%")
        
        if filters.get('phone'):
            where_conditions.append("phone ILIKE %s")
            params.append(f"%{filters['phone']}%")
        
        if filters.get('email'):
            where_conditions.append("email ILIKE %s")
            params.append(f"%{filters['email']}%")
        
        if filters.get('min_id'):
            where_conditions.append("id >= %s")
            params.append(filters['min_id'])
        
        if filters.get('max_id'):
            where_conditions.append("id <= %s")
            params.append(filters['max_id'])
        
        query = "SELECT * FROM contacts"
        if where_conditions:
            query += " WHERE " + " OR ".join(where_conditions)
        query += " ORDER BY id"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    def export_to_csv(self, filename: str) -> str:
        """Export contacts to CSV file."""
        contacts = self.view_contacts()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Get dynamic column headers
            columns = schema_manager.get_display_columns()
            header = [col.title() for col in columns]
            writer.writerow(header)
            
            for contact in contacts:
                writer.writerow(contact)
        
        return filename
    
    def export_to_json(self, filename: str) -> str:
        """Export contacts to JSON file."""
        contacts = self.view_contacts()
        contacts_list = []
        
        # Use dynamic schema for JSON export (raw data, no formatting)
        from ...core.schema_manager import schema_manager
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict_raw(contact)
            contacts_list.append(contact_dict)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(contacts_list, jsonfile, indent=2, ensure_ascii=False, default=str)
        
        return filename
    
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
                    continue
        return imported_count
    
    def bulk_update(self, contact_ids: List[int], field: str, new_value: str) -> int:
        """Update multiple contacts at once. Returns number of updated contacts."""
        if not contact_ids:
            return 0
        
        # Get valid columns dynamically
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'contacts' AND column_name NOT IN ('id', 'created_at', 'updated_at')
        """)
        valid_columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        if field not in valid_columns:
            conn.close()
            return 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['%s' for _ in contact_ids])
        query = f"UPDATE contacts SET {field} = %s, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})"
        
        cursor.execute(query, [new_value] + contact_ids)
        updated_count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return updated_count
    
    def bulk_delete(self, contact_ids: List[int]) -> int:
        """Delete multiple contacts at once. Returns number of deleted contacts."""
        if not contact_ids:
            return 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['%s' for _ in contact_ids])
        query = f"DELETE FROM contacts WHERE id IN ({placeholders})"
        
        cursor.execute(query, contact_ids)
        deleted_count = cursor.rowcount
        conn.commit()
        cursor.close()
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
        
        # Complete contacts
        cursor.execute("""
            SELECT COUNT(*) FROM contacts 
            WHERE phone IS NOT NULL AND phone != '' 
            AND email IS NOT NULL AND email != ''
        """)
        complete_contacts = cursor.fetchone()[0]
        
        # Email domains
        cursor.execute("""
            SELECT SUBSTRING(email FROM POSITION('@' IN email) + 1) as domain, COUNT(*) as count
            FROM contacts 
            WHERE email IS NOT NULL AND email != '' AND email LIKE '%@%'
            GROUP BY domain 
            ORDER BY count DESC 
            LIMIT 10
        """)
        email_domains = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'total_contacts': total_contacts,
            'contacts_with_phone': contacts_with_phone,
            'contacts_with_email': contacts_with_email,
            'complete_contacts': complete_contacts,
            'phone_percentage': round((contacts_with_phone / total_contacts * 100) if total_contacts > 0 else 0, 1),
            'email_percentage': round((contacts_with_email / total_contacts * 100) if total_contacts > 0 else 0, 1),
            'complete_percentage': round((complete_contacts / total_contacts * 100) if total_contacts > 0 else 0, 1),
            'top_email_domains': email_domains
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM contacts")
        record_count = cursor.fetchone()[0]
        
        # Get database size
        cursor.execute("""
            SELECT pg_database_size(current_database()) as db_size
        """)
        db_size = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            'database_type': 'PostgreSQL',
            'database_name': self.database,
            'database_size_bytes': db_size,
            'database_size_mb': round(db_size / (1024 * 1024), 2),
            'record_count': record_count
        }
    
    def get_table_info(self) -> List[Tuple]:
        """Get table structure information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                column_name, 
                data_type, 
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_name = 'contacts'
            ORDER BY ordinal_position
        """)
        table_info = cursor.fetchall()
        cursor.close()
        conn.close()
        return table_info
    
    def add_column(self, column_name: str, column_type: str, default_value: Any = None) -> None:
        """Add a new column to the contacts table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        alter_query = f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}"
        if default_value is not None:
            if isinstance(default_value, str):
                alter_query += f" DEFAULT '{default_value}'"
            else:
                alter_query += f" DEFAULT {default_value}"
        
        cursor.execute(alter_query)
        conn.commit()
        cursor.close()
        conn.close()
    
    def remove_column(self, column_name: str) -> None:
        """Remove a column from the contacts table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        alter_query = f"ALTER TABLE contacts DROP COLUMN {column_name}"
        
        cursor.execute(alter_query)
        conn.commit()
        cursor.close()
        conn.close()
    
    def backup_database(self) -> str:
        """Create a backup of the database. Returns backup filename."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"contacts_backup_{timestamp}.sql"
        backup_path = os.path.join("db_backup", backup_filename)
        
        os.makedirs("db_backup", exist_ok=True)
        
        # Use pg_dump command
        import subprocess
        cmd = [
            'pg_dump',
            '-h', self.host,
            '-p', str(self.port),
            '-U', self.user,
            '-d', self.database,
            '-f', backup_path
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password
        
        try:
            subprocess.run(cmd, env=env, check=True)
            return backup_filename
        except subprocess.CalledProcessError:
            raise Exception("Backup failed. Make sure pg_dump is installed.")
    
    def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup. Returns success status."""
        backup_path = os.path.join("db_backup", backup_filename)
        if not os.path.exists(backup_path):
            return False
        
        import subprocess
        cmd = [
            'psql',
            '-h', self.host,
            '-p', str(self.port),
            '-U', self.user,
            '-d', self.database,
            '-f', backup_path
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password
        
        try:
            subprocess.run(cmd, env=env, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def cleanup_db(self) -> int:
        """Clean up database (remove empty records). Returns number of cleaned records."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM contacts WHERE name IS NULL OR name = ''")
        cleaned_count = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        return cleaned_count
    
    def full_cleanup_db(self) -> bool:
        """Perform full database cleanup - DELETE ALL contacts and reset auto-increment."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Delete ALL contacts
            cursor.execute("DELETE FROM contacts")
            
            # Reset auto-increment sequence
            cursor.execute("ALTER SEQUENCE contacts_id_seq RESTART WITH 1")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Vacuum needs to be in autocommit mode
            conn = self.get_connection()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("VACUUM ANALYZE contacts")
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
    
    def reset_table_structure(self) -> bool:
        """Reset table to base 6-column structure (drop and recreate)."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Drop existing table (CASCADE drops the sequence too)
            cursor.execute("DROP TABLE IF EXISTS contacts CASCADE")
            
            # Recreate table with 6 base columns including timestamps
            cursor.execute("""
                CREATE TABLE contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC'),
                    updated_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
                )
            """)
            
            # Create function for updating updated_at column
            cursor.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = (NOW() AT TIME ZONE 'UTC');
                RETURN NEW;
            END;
            $$ language 'plpgsql'
            """)
            
            # Create trigger to automatically update updated_at column
            cursor.execute("""
            CREATE TRIGGER update_contacts_updated_at 
                BEFORE UPDATE ON contacts 
                FOR EACH ROW 
                EXECUTE FUNCTION update_updated_at_column()
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Vacuum to reclaim space
            conn = self.get_connection()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("VACUUM ANALYZE contacts")
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Reset table error: {e}")
            return False

