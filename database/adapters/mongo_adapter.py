"""
MongoDB database adapter using pymongo.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import csv
import json
import datetime
import os
from typing import List, Dict, Any, Optional, Tuple

from ..base import DatabaseAdapter


class MongoDBAdapter(DatabaseAdapter):
    """MongoDB implementation of the DatabaseAdapter interface."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize MongoDB adapter with configuration."""
        super().__init__(config)
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 27017)
        self.user = config.get('user', '')
        self.password = config.get('password', '')
        self.database = config.get('database', 'contacts')
        self.auth_database = config.get('auth_database', 'admin')
        
        self.client = None
        self.db = None
        self.collection = None
        self._counter = 0
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize MongoDB connection."""
        try:
            # Build connection string based on whether auth is configured
            if self.user and self.password:
                connection_string = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.auth_database}"
            else:
                # No authentication (default Docker setup)
                connection_string = f"mongodb://{self.host}:{self.port}/"
            
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database]
            self.collection = self.db['contacts']
        except Exception as e:
            print(f"Failed to initialize MongoDB connection: {e}")
            self.client = None
            self.db = None
            self.collection = None
    
    def get_connection(self):
        """Return the MongoDB client."""
        if self.client is None:
            self._initialize_connection()
        return self.client
    
    def test_connection(self) -> bool:
        """Test if the MongoDB database connection is working."""
        try:
            if self.client is None:
                return False
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"MongoDB connection test failed: {e}")
            return False
    
    def create_table(self) -> None:
        """Create indexes for the contacts collection."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        # MongoDB creates collections automatically, but we can create indexes
        self.collection.create_index("id", unique=True)
        self.collection.create_index("name")
        self.collection.create_index("email")
        self.collection.create_index("phone")
        
        # Initialize counter if not exists
        counters = self.db['counters']
        if counters.find_one({'_id': 'contact_id'}) is None:
            counters.insert_one({'_id': 'contact_id', 'sequence_value': 0})
    
    def _get_next_id(self) -> int:
        """Get next auto-increment ID for contacts."""
        counters = self.db['counters']
        result = counters.find_one_and_update(
            {'_id': 'contact_id'},
            {'$inc': {'sequence_value': 1}},
            return_document=True,
            upsert=True
        )
        return result['sequence_value']
    
    def _doc_to_tuple(self, doc: Dict) -> Tuple:
        """Convert MongoDB document to tuple format for compatibility.
        Order aligns with get_table_info() column order.
        """
        if doc is None:
            return None
        
        # Derive current visible columns (exclude internal fields)
        columns_info = self.get_table_info()
        column_names = [c[0] for c in columns_info]
        
        values: List[Any] = []
        for col in column_names:
            values.append(doc.get(col))
        return tuple(values)
    
    def add_contact(self, **fields) -> None:
        """Add a new contact to the database (dynamic fields)."""
        if 'name' not in fields:
            raise ValueError("Name is required")
        
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        contact_id = self._get_next_id()
        
        # Build contact document with provided fields
        contact = {
            'id': contact_id,
            # Keep internal timestamps but don't expose as columns
            'created_at': datetime.datetime.utcnow(),
            'updated_at': datetime.datetime.utcnow()
        }
        
        # Add all provided fields
        contact.update(fields)
        
        self.collection.insert_one(contact)
    
    def view_contacts(self) -> List[Tuple]:
        """Retrieve all contacts from the database."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        docs = self.collection.find({}).sort('id', 1)
        return [self._doc_to_tuple(doc) for doc in docs]
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Tuple]:
        """Get a specific contact by ID."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        doc = self.collection.find_one({'id': contact_id})
        return self._doc_to_tuple(doc)
    
    def update_contact(self, contact_id: int, **fields) -> None:
        """Update contact fields dynamically."""
        if not fields:
            raise ValueError("No fields to update")
        
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        # Add updated_at timestamp
        update_fields = fields.copy()
        update_fields['updated_at'] = datetime.datetime.utcnow()
        
        self.collection.update_one(
            {'id': contact_id},
            {'$set': update_fields}
        )
    
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
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        self.collection.delete_one({'id': contact_id})
    
    def search_contact(self, search_term: str) -> List[Tuple]:
        """Search for contacts by name, phone, or email."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        regex_pattern = {'$regex': search_term, '$options': 'i'}
        query = {
            '$or': [
                {'name': regex_pattern},
                {'phone': regex_pattern},
                {'email': regex_pattern}
            ]
        }
        docs = self.collection.find(query).sort('id', 1)
        return [self._doc_to_tuple(doc) for doc in docs]
    
    def advanced_search(self, filters: Dict[str, Any]) -> List[Tuple]:
        """Advanced search with multiple filters."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        query = {}
        
        if filters.get('name'):
            query['name'] = {'$regex': filters['name'], '$options': 'i'}
        
        if filters.get('phone'):
            query['phone'] = {'$regex': filters['phone'], '$options': 'i'}
        
        if filters.get('email'):
            query['email'] = {'$regex': filters['email'], '$options': 'i'}
        
        if filters.get('min_id'):
            query['id'] = query.get('id', {})
            query['id']['$gte'] = filters['min_id']
        
        if filters.get('max_id'):
            query['id'] = query.get('id', {})
            query['id']['$lte'] = filters['max_id']
        
        docs = self.collection.find(query).sort('id', 1)
        return [self._doc_to_tuple(doc) for doc in docs]
    
    def export_to_csv(self, filename: str) -> None:
        """Export contacts to CSV file."""
        contacts = self.view_contacts()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Age', 'Address', 
                           'Department', 'Category', 'Tags'])
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
                'tags': contact[8] if len(contact) > 8 else ''
            }
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
                    continue
        return imported_count
    
    def bulk_update(self, contact_ids: List[int], field: str, new_value: str) -> int:
        """Update multiple contacts at once. Returns number of updated contacts."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        if not contact_ids or field not in ['name', 'phone', 'email']:
            return 0
        
        result = self.collection.update_many(
            {'id': {'$in': contact_ids}},
            {'$set': {field: new_value, 'updated_at': datetime.datetime.utcnow()}}
        )
        return result.modified_count
    
    def bulk_delete(self, contact_ids: List[int]) -> int:
        """Delete multiple contacts at once. Returns number of deleted contacts."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        if not contact_ids:
            return 0
        
        result = self.collection.delete_many({'id': {'$in': contact_ids}})
        return result.deleted_count
    
    def get_contact_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contact analytics."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        # Total contacts
        total_contacts = self.collection.count_documents({})
        
        # Contacts with phone
        contacts_with_phone = self.collection.count_documents({
            'phone': {'$exists': True, '$ne': '', '$ne': None}
        })
        
        # Contacts with email
        contacts_with_email = self.collection.count_documents({
            'email': {'$exists': True, '$ne': '', '$ne': None}
        })
        
        # Complete contacts
        complete_contacts = self.collection.count_documents({
            'phone': {'$exists': True, '$ne': '', '$ne': None},
            'email': {'$exists': True, '$ne': '', '$ne': None}
        })
        
        # Top email domains
        pipeline = [
            {'$match': {'email': {'$regex': '@', '$ne': '', '$ne': None}}},
            {'$project': {
                'domain': {
                    '$arrayElemAt': [
                        {'$split': ['$email', '@']},
                        1
                    ]
                }
            }},
            {'$group': {'_id': '$domain', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        email_domains = list(self.collection.aggregate(pipeline))
        top_domains = [(d['_id'], d['count']) for d in email_domains]
        
        return {
            'total_contacts': total_contacts,
            'contacts_with_phone': contacts_with_phone,
            'contacts_with_email': contacts_with_email,
            'complete_contacts': complete_contacts,
            'phone_percentage': (contacts_with_phone / total_contacts * 100) if total_contacts > 0 else 0,
            'email_percentage': (contacts_with_email / total_contacts * 100) if total_contacts > 0 else 0,
            'complete_percentage': (complete_contacts / total_contacts * 100) if total_contacts > 0 else 0,
            'top_email_domains': top_domains
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        record_count = self.collection.count_documents({})
        
        # Get collection stats
        stats = self.db.command('collstats', 'contacts')
        
        return {
            'database_type': 'MongoDB',
            'database_name': self.database,
            'database_size_bytes': stats.get('size', 0),
            'database_size_mb': round(stats.get('size', 0) / (1024 * 1024), 2),
            'record_count': record_count
        }
    
    def get_table_info(self) -> List[Tuple]:
        """Get collection schema information.
        Returns only the 4 base columns by default, plus any user-added fields
        discovered from an example document. Internal fields are hidden.
        """
        # Base fields (visible)
        fields: List[Tuple[str, str, str, Any]] = [
            ('id', 'Integer', 'NO', 'auto-increment'),
            ('name', 'String', 'NO', None),
            ('phone', 'String', 'YES', None),
            ('email', 'String', 'YES', None),
        ]
        
        # Attempt to discover user-added fields from a sample document
        try:
            if self.collection is not None:
                sample = self.collection.find_one()
            else:
                sample = None
            if sample:
                reserved = {'_id', 'id', 'name', 'phone', 'email', 'created_at', 'updated_at'}
                for key in sample.keys():
                    if key in reserved:
                        continue
                    # Avoid duplicates if already listed
                    if not any(col[0] == key for col in fields):
                        fields.append((key, 'String', 'YES', None))
        except Exception:
            # Non-fatal; fall back to base fields only
            pass
        
        return fields
    
    def add_column(self, column_name: str, column_type: str, default_value: Any = None) -> None:
        """Add a new field to all documents (MongoDB is schemaless)."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        # Update all existing documents to have the new field with default value
        self.collection.update_many(
            {column_name: {'$exists': False}},
            {'$set': {column_name: default_value}}
        )
    
    def remove_column(self, column_name: str) -> None:
        """Remove a field from all documents (MongoDB is schemaless)."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        # Remove the field from all documents
        self.collection.update_many(
            {},
            {'$unset': {column_name: ""}}
        )
    
    def backup_database(self) -> str:
        """Create a backup of the database. Returns backup filename."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"contacts_backup_{timestamp}.json"
        backup_path = os.path.join("db_backup", backup_filename)
        
        os.makedirs("db_backup", exist_ok=True)
        
        # Export all documents to JSON
        docs = list(self.collection.find({}))
        
        # Convert ObjectId to string for JSON serialization
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc:
                doc['created_at'] = doc['created_at'].isoformat()
            if 'updated_at' in doc:
                doc['updated_at'] = doc['updated_at'].isoformat()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)
        
        return backup_filename
    
    def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup. Returns success status."""
        backup_path = os.path.join("db_backup", backup_filename)
        if not os.path.exists(backup_path):
            return False
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                docs = json.load(f)
            
            # Clear existing collection
            self.collection.delete_many({})
            
            # Convert string dates back to datetime
            for doc in docs:
                if '_id' in doc and isinstance(doc['_id'], str):
                    doc['_id'] = ObjectId(doc['_id'])
                if 'created_at' in doc and isinstance(doc['created_at'], str):
                    doc['created_at'] = datetime.datetime.fromisoformat(doc['created_at'])
                if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                    doc['updated_at'] = datetime.datetime.fromisoformat(doc['updated_at'])
            
            # Insert documents
            if docs:
                self.collection.insert_many(docs)
            
            return True
        except Exception:
            return False
    
    def cleanup_db(self) -> int:
        """Clean up database (remove empty records). Returns number of cleaned records."""
        if self.collection is None:
            raise ConnectionError("MongoDB not initialized")
        
        result = self.collection.delete_many({
            '$or': [
                {'name': {'$exists': False}},
                {'name': ''},
                {'name': None}
            ]
        })
        return result.deleted_count
    
    def full_cleanup_db(self) -> bool:
        """Perform full database cleanup - DELETE ALL contacts and reset counter."""
        try:
            if self.collection is None:
                return False
            
            # Delete ALL contacts
            self.collection.delete_many({})
            
            # Reset the counter to 0 (next ID will be 1)
            counters = self.db['counters']
            counters.update_one(
                {'_id': 'contact_id'},
                {'$set': {'sequence_value': 0}},
                upsert=True
            )
            
            return True
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
    
    def reset_table_structure(self) -> bool:
        """Reset collection to base structure (drop and recreate)."""
        try:
            if self.collection is None:
                return False
            
            # Drop the collection entirely
            self.collection.drop()
            
            # Recreate the collection (MongoDB creates it automatically on first insert)
            self.collection = self.db['contacts']
            
            # Reset the counter to 0 (next ID will be 1)
            counters = self.db['counters']
            counters.delete_one({'_id': 'contact_id'})  # Delete old counter
            counters.insert_one({'_id': 'contact_id', 'sequence_value': 0})
            
            return True
        except Exception as e:
            print(f"Reset collection error: {e}")
            return False

