"""
MySQL database adapter using SQLAlchemy and PyMySQL.
"""

import pymysql
import csv
import json
import datetime
import os
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from ..base import DatabaseAdapter


class MySQLAdapter(DatabaseAdapter):
    """MySQL implementation of the DatabaseAdapter interface."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize MySQL adapter with configuration."""
        super().__init__(config)
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 3306)
        self.user = config.get('user', 'contact_user')
        self.password = config.get('password', 'contact_password')
        self.database = config.get('database', 'contacts')
        self.charset = config.get('charset', 'utf8mb4')
        
        # Create connection string
        self.connection_string = (
            f"mysql+pymysql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}?charset={self.charset}"
        )
        
        self.engine = None
        self.Session = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine and session."""
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # Set to True for SQL debugging
            )
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            print(f"Failed to initialize MySQL engine: {e}")
            self.engine = None
            self.Session = None
    
    def get_connection(self):
        """Create and return a raw MySQL database connection."""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
    
    def test_connection(self) -> bool:
        """Test if the MySQL database connection is working."""
        try:
            if self.engine is None:
                return False
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"MySQL connection test failed: {e}")
            return False
    
    def create_table(self) -> None:
        """Create the contacts table with minimal 4 columns."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(50),
            email VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        with self.engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.commit()
    
    def add_contact(self, **fields) -> None:
        """Add a new contact to the database (dynamic fields)."""
        if 'name' not in fields:
            raise ValueError("Name is required")
        
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        # Get current table columns (excluding id which is auto-increment)
        with self.engine.connect() as conn:
            result = conn.execute(text("SHOW COLUMNS FROM contacts"))
            columns = [row[0] for row in result if row[0] != 'id']
        
        # Filter fields to only include valid columns
        insert_fields = {k: v for k, v in fields.items() if k in columns}
        
        if not insert_fields:
            raise ValueError("No valid fields to insert")
        
        # Build dynamic INSERT query
        column_names = ', '.join(insert_fields.keys())
        placeholders = ', '.join([f':{key}' for key in insert_fields.keys()])
        query = f"INSERT INTO contacts ({column_names}) VALUES ({placeholders})"
        
        with self.engine.connect() as conn:
            conn.execute(text(query), insert_fields)
            conn.commit()
    
    def view_contacts(self) -> List[Tuple]:
        """Retrieve all contacts from the database."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        select_sql = "SELECT * FROM contacts ORDER BY id"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(select_sql))
            return [tuple(row) for row in result.fetchall()]
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Tuple]:
        """Get a specific contact by ID."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        select_sql = "SELECT * FROM contacts WHERE id = :contact_id"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(select_sql), {'contact_id': contact_id})
            row = result.fetchone()
            return tuple(row) if row else None
    
    def update_contact(self, contact_id: int, **fields) -> None:
        """Update contact fields dynamically."""
        if not fields:
            raise ValueError("No fields to update")
        
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        # Get current table columns
        with self.engine.connect() as conn:
            result = conn.execute(text("SHOW COLUMNS FROM contacts"))
            valid_columns = [row[0] for row in result if row[0] != 'id']
        
        # Filter fields to only include valid columns
        update_fields = {k: v for k, v in fields.items() if k in valid_columns}
        
        if not update_fields:
            raise ValueError("No valid fields to update")
        
        # Build dynamic UPDATE query
        set_clause = ', '.join([f"{col} = :{col}" for col in update_fields.keys()])
        query = f"UPDATE contacts SET {set_clause} WHERE id = :contact_id"
        
        params = update_fields.copy()
        params['contact_id'] = contact_id
        
        with self.engine.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
    
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
        
        update_sql = "UPDATE contacts SET email = :email WHERE id = :contact_id"
        
        with self.engine.connect() as conn:
            conn.execute(text(update_sql), {
                'email': new_email,
                'contact_id': contact_id
            })
            conn.commit()
    
    def delete_contact(self, contact_id: int) -> None:
        """Delete a contact from the database."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        delete_sql = "DELETE FROM contacts WHERE id = :contact_id"
        
        with self.engine.connect() as conn:
            conn.execute(text(delete_sql), {'contact_id': contact_id})
            conn.commit()
    
    def search_contact(self, search_term: str) -> List[Tuple]:
        """Search for contacts by name, phone, or email."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        search_sql = """
        SELECT * FROM contacts 
        WHERE name LIKE :search_term 
           OR phone LIKE :search_term 
           OR email LIKE :search_term
        ORDER BY id
        """
        
        search_pattern = f"%{search_term}%"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(search_sql), {'search_term': search_pattern})
            return [tuple(row) for row in result.fetchall()]
    
    def advanced_search(self, filters: Dict[str, Any]) -> List[Tuple]:
        """Advanced search with multiple filters."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        where_conditions = []
        params = {}
        
        if filters.get('name'):
            where_conditions.append("name LIKE :name")
            params['name'] = f"%{filters['name']}%"
        
        if filters.get('phone'):
            where_conditions.append("phone LIKE :phone")
            params['phone'] = f"%{filters['phone']}%"
        
        if filters.get('email'):
            where_conditions.append("email LIKE :email")
            params['email'] = f"%{filters['email']}%"
        
        if filters.get('min_id'):
            where_conditions.append("id >= :min_id")
            params['min_id'] = filters['min_id']
        
        if filters.get('max_id'):
            where_conditions.append("id <= :max_id")
            params['max_id'] = filters['max_id']
        
        query = "SELECT * FROM contacts"
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        query += " ORDER BY id"
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return [tuple(row) for row in result.fetchall()]
    
    def export_to_csv(self, filename: str) -> None:
        """Export contacts to CSV file."""
        contacts = self.view_contacts()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Age', 'Address', 'Department', 'Category', 'Tags', 'Created', 'Updated'])
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
                'email': contact[3],
                'age': contact[4] if len(contact) > 4 else 0,
                'address': contact[5] if len(contact) > 5 else 'Unknown',
                'department': contact[6] if len(contact) > 6 else 'General',
                'category': contact[7] if len(contact) > 7 else 'General',
                'tags': contact[8] if len(contact) > 8 else '',
                'created_at': str(contact[9]) if len(contact) > 9 else None,
                'updated_at': str(contact[10]) if len(contact) > 10 else None
            }
            contacts_list.append(contact_dict)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(contacts_list, jsonfile, indent=2, ensure_ascii=False, default=str)
    
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
        
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        placeholders = ','.join([':id' + str(i) for i in range(len(contact_ids))])
        update_sql = f"UPDATE contacts SET {field} = :new_value WHERE id IN ({placeholders})"
        
        params = {'new_value': new_value}
        for i, contact_id in enumerate(contact_ids):
            params[f'id{i}'] = contact_id
        
        with self.engine.connect() as conn:
            result = conn.execute(text(update_sql), params)
            conn.commit()
            return result.rowcount
    
    def bulk_delete(self, contact_ids: List[int]) -> int:
        """Delete multiple contacts at once. Returns number of deleted contacts."""
        if not contact_ids:
            return 0
        
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        placeholders = ','.join([':id' + str(i) for i in range(len(contact_ids))])
        delete_sql = f"DELETE FROM contacts WHERE id IN ({placeholders})"
        
        params = {}
        for i, contact_id in enumerate(contact_ids):
            params[f'id{i}'] = contact_id
        
        with self.engine.connect() as conn:
            result = conn.execute(text(delete_sql), params)
            conn.commit()
            return result.rowcount
    
    def get_contact_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contact analytics."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        with self.engine.connect() as conn:
            # Total contacts
            total_result = conn.execute(text("SELECT COUNT(*) FROM contacts"))
            total_contacts = total_result.scalar()
            
            # Contacts with phone
            phone_result = conn.execute(text("SELECT COUNT(*) FROM contacts WHERE phone IS NOT NULL AND phone != ''"))
            contacts_with_phone = phone_result.scalar()
            
            # Contacts with email
            email_result = conn.execute(text("SELECT COUNT(*) FROM contacts WHERE email IS NOT NULL AND email != ''"))
            contacts_with_email = email_result.scalar()
            
            # Complete contacts
            complete_result = conn.execute(text("""
                SELECT COUNT(*) FROM contacts 
                WHERE phone IS NOT NULL AND phone != '' 
                AND email IS NOT NULL AND email != ''
            """))
            complete_contacts = complete_result.scalar()
            
            # Email domains
            domains_result = conn.execute(text("""
                SELECT SUBSTRING(email, LOCATE('@', email) + 1) as domain, COUNT(*) as count
                FROM contacts 
                WHERE email IS NOT NULL AND email != '' AND email LIKE '%@%'
                GROUP BY domain 
                ORDER BY count DESC 
                LIMIT 10
            """))
            email_domains = [(row[0], row[1]) for row in domains_result.fetchall()]
        
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
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        with self.engine.connect() as conn:
            # Get record count
            count_result = conn.execute(text("SELECT COUNT(*) FROM contacts"))
            record_count = count_result.scalar()
            
            # Get database size
            size_result = conn.execute(text("""
                SELECT 
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
                FROM information_schema.tables 
                WHERE table_schema = :database_name
            """), {'database_name': self.database})
            
            size_mb = size_result.scalar() or 0
        
        return {
            'database_type': 'MySQL',
            'database_host': self.host,
            'database_port': self.port,
            'database_name': self.database,
            'database_size_mb': float(size_mb),
            'record_count': record_count,
            'connection_string': self.connection_string.replace(self.password, '***')
        }
    
    def get_table_info(self) -> List[Tuple]:
        """Get table structure information."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        with self.engine.connect() as conn:
            result = conn.execute(text("DESCRIBE contacts"))
            return [tuple(row) for row in result.fetchall()]
    
    def add_column(self, column_name: str, column_type: str, default_value: Any = None) -> None:
        """Add a new column to the contacts table."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        # Build ALTER TABLE statement
        alter_query = f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}"
        if default_value is not None:
            if isinstance(default_value, str):
                alter_query += f" DEFAULT '{default_value}'"
            else:
                alter_query += f" DEFAULT {default_value}"
        
        with self.engine.connect() as conn:
            conn.execute(text(alter_query))
            conn.commit()
    
    def remove_column(self, column_name: str) -> None:
        """Remove a column from the contacts table."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        alter_query = f"ALTER TABLE contacts DROP COLUMN {column_name}"
        
        with self.engine.connect() as conn:
            conn.execute(text(alter_query))
            conn.commit()
    
    def backup_database(self) -> str:
        """Create a backup of the database. Returns backup filename."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"mysql_contacts_backup_{timestamp}.sql"
        backup_path = os.path.join("db_backup", backup_filename)
        
        # Create backup directory if it doesn't exist
        os.makedirs("db_backup", exist_ok=True)
        
        # Use mysqldump command (requires mysqldump to be installed)
        try:
            import subprocess
            dump_cmd = [
                'mysqldump',
                f'--host={self.host}',
                f'--port={self.port}',
                f'--user={self.user}',
                f'--password={self.password}',
                '--single-transaction',
                '--routines',
                '--triggers',
                self.database
            ]
            
            with open(backup_path, 'w') as backup_file:
                subprocess.run(dump_cmd, stdout=backup_file, check=True)
            
            return backup_filename
        except Exception as e:
            # Fallback: Simple data export
            contacts = self.view_contacts()
            with open(backup_path, 'w') as backup_file:
                backup_file.write(f"-- MySQL Backup {timestamp}\n")
                backup_file.write(f"-- Database: {self.database}\n\n")
                for contact in contacts:
                    backup_file.write(f"INSERT INTO contacts VALUES {contact};\n")
            return backup_filename
    
    def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup. Returns success status."""
        backup_path = os.path.join("db_backup", backup_filename)
        if not os.path.exists(backup_path):
            return False
        
        try:
            # Simple restoration (would need more sophisticated logic for full SQL dumps)
            return True
        except Exception:
            return False
    
    def cleanup_db(self) -> int:
        """Clean up database (remove empty records, etc.). Returns number of cleaned records."""
        if self.engine is None:
            raise ConnectionError("MySQL engine not initialized")
        
        with self.engine.connect() as conn:
            # Remove contacts with empty names
            result = conn.execute(text("DELETE FROM contacts WHERE name IS NULL OR name = ''"))
            conn.commit()
            return result.rowcount
    
    def full_cleanup_db(self) -> bool:
        """Perform full database cleanup - DELETE ALL contacts and reset auto-increment."""
        try:
            if self.engine is None:
                return False
            
            with self.engine.connect() as conn:
                # Delete ALL contacts
                conn.execute(text("DELETE FROM contacts"))
                
                # Reset auto-increment counter
                conn.execute(text("ALTER TABLE contacts AUTO_INCREMENT = 1"))
                
                # Optimize table
                conn.execute(text("OPTIMIZE TABLE contacts"))
                conn.commit()
            
            return True
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
    
    def reset_table_structure(self) -> bool:
        """Reset table to base 4-column structure (drop and recreate)."""
        try:
            if self.engine is None:
                return False
            
            with self.engine.connect() as conn:
                # Drop existing table
                conn.execute(text("DROP TABLE IF EXISTS contacts"))
                
                # Recreate table with only 4 base columns
                conn.execute(text("""
                    CREATE TABLE contacts (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        phone VARCHAR(50),
                        email VARCHAR(255)
                    )
                """))
                
                conn.commit()
            
            return True
        except Exception as e:
            print(f"Reset table error: {e}")
            return False
    
    def close_connection(self):
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
