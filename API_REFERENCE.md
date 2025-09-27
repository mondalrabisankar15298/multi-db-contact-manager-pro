# 📒 Contact Book Manager - API Reference

## 🔧 Technical API Documentation

This document provides detailed technical information about all functions, classes, and methods available in the Contact Book Manager application.

## 📁 File Structure

```
contact_book/
│── db.py                    # Database connection management
│── crud.py                  # All CRUD and advanced operations
│── main.py                  # Main application and UI
│── DOCUMENTATION.md         # Complete feature documentation
│── USER_GUIDE.md           # Quick user guide
│── API_REFERENCE.md        # This technical reference
```

## 🗄️ Database Module (`db.py`)

### Functions

#### `get_connection()`
- **Purpose**: Create and return a database connection
- **Returns**: SQLite connection object
- **Usage**: Used by all database operations
- **Example**: `conn = get_connection()`

## 🔧 CRUD Module (`crud.py`)

### Basic CRUD Operations

#### `create_table()`
- **Purpose**: Create the contacts table if it doesn't exist
- **Parameters**: None
- **Returns**: None
- **SQL**: Creates table with id, name, phone, email columns

#### `add_contact(name, phone, email)`
- **Purpose**: Add a new contact to the database
- **Parameters**:
  - `name` (str): Contact name (required)
  - `phone` (str): Phone number (optional)
  - `email` (str): Email address (optional)
- **Returns**: None
- **SQL**: `INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)`

#### `view_contacts()`
- **Purpose**: Retrieve all contacts from the database
- **Parameters**: None
- **Returns**: List of tuples (contact records)
- **SQL**: `SELECT * FROM contacts`

#### `update_contact_name(contact_id, new_name)`
- **Purpose**: Update a contact's name
- **Parameters**:
  - `contact_id` (int): Contact ID
  - `new_name` (str): New name
- **Returns**: None
- **SQL**: `UPDATE contacts SET name = ? WHERE id = ?`

#### `update_contact_phone(contact_id, new_phone)`
- **Purpose**: Update a contact's phone number
- **Parameters**:
  - `contact_id` (int): Contact ID
  - `new_phone` (str): New phone number
- **Returns**: None
- **SQL**: `UPDATE contacts SET phone = ? WHERE id = ?`

#### `update_contact_email(contact_id, new_email)`
- **Purpose**: Update a contact's email address
- **Parameters**:
  - `contact_id` (int): Contact ID
  - `new_email` (str): New email address
- **Returns**: None
- **SQL**: `UPDATE contacts SET email = ? WHERE id = ?`

#### `delete_contact(contact_id)`
- **Purpose**: Delete a contact from the database
- **Parameters**:
  - `contact_id` (int): Contact ID to delete
- **Returns**: None
- **SQL**: `DELETE FROM contacts WHERE id = ?`

#### `get_contact_by_id(contact_id)`
- **Purpose**: Get a specific contact by ID
- **Parameters**:
  - `contact_id` (int): Contact ID
- **Returns**: Tuple (contact record) or None
- **SQL**: `SELECT * FROM contacts WHERE id = ?`

#### `search_contact(search_term)`
- **Purpose**: Search for contacts by name, phone, or email
- **Parameters**:
  - `search_term` (str): Search term
- **Returns**: List of tuples (matching contacts)
- **SQL**: `SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?`

### Advanced Search Functions

#### `advanced_search(filters)`
- **Purpose**: Advanced search with multiple filters
- **Parameters**:
  - `filters` (dict): Dictionary of search criteria
    - `name` (str, optional): Name filter
    - `phone` (str, optional): Phone filter
    - `email` (str, optional): Email filter
    - `min_id` (int, optional): Minimum ID
    - `max_id` (int, optional): Maximum ID
- **Returns**: List of tuples (matching contacts)
- **SQL**: Dynamic query based on filters

#### `search_by_pattern(pattern, field='all')`
- **Purpose**: Search using regex-like patterns
- **Parameters**:
  - `pattern` (str): Search pattern
  - `field` (str): Field to search ('all', 'name', 'phone', 'email')
- **Returns**: List of tuples (matching contacts)
- **SQL**: `SELECT * FROM contacts WHERE {field} LIKE ?`

### Export/Import Functions

#### `export_to_csv(filename="contacts_export.csv")`
- **Purpose**: Export contacts to CSV file
- **Parameters**:
  - `filename` (str): Output filename
- **Returns**: String (filename)
- **Features**: UTF-8 encoding, proper CSV formatting

#### `export_to_json(filename="contacts_export.json")`
- **Purpose**: Export contacts to JSON file
- **Parameters**:
  - `filename` (str): Output filename
- **Returns**: String (filename)
- **Features**: Structured JSON, UTF-8 encoding

#### `import_from_csv(filename)`
- **Purpose**: Import contacts from CSV file
- **Parameters**:
  - `filename` (str): Input CSV filename
- **Returns**: Integer (number of imported contacts)
- **Features**: Automatic column mapping, validation

### Bulk Operations

#### `bulk_update(contact_ids, field, new_value)`
- **Purpose**: Update multiple contacts at once
- **Parameters**:
  - `contact_ids` (list): List of contact IDs
  - `field` (str): Field to update
  - `new_value` (str): New value
- **Returns**: Integer (number of updated rows)
- **SQL**: `UPDATE contacts SET {field} = ? WHERE id IN (...)`

#### `bulk_delete(contact_ids)`
- **Purpose**: Delete multiple contacts at once
- **Parameters**:
  - `contact_ids` (list): List of contact IDs to delete
- **Returns**: Integer (number of deleted rows)
- **SQL**: `DELETE FROM contacts WHERE id IN (...)`

### Data Analytics

#### `get_contact_analytics()`
- **Purpose**: Get detailed analytics about contacts
- **Parameters**: None
- **Returns**: Dictionary with analytics data
- **Keys**:
  - `total_contacts`: Total number of contacts
  - `contacts_with_phone`: Contacts with phone numbers
  - `contacts_with_email`: Contacts with email addresses
  - `contacts_complete`: Contacts with both phone and email
  - `phone_percentage`: Percentage with phone numbers
  - `email_percentage`: Percentage with email addresses
  - `complete_percentage`: Percentage with complete data
  - `top_domains`: List of top email domains

#### `get_database_stats()`
- **Purpose**: Get database statistics
- **Parameters**: None
- **Returns**: Dictionary with database statistics
- **Keys**:
  - `contact_count`: Number of contacts
  - `column_count`: Number of columns
  - `columns`: List of column names
  - `db_size_bytes`: Database size in bytes
  - `db_size_mb`: Database size in MB

### Data Validation

#### `validate_email(email)`
- **Purpose**: Validate email format
- **Parameters**:
  - `email` (str): Email address to validate
- **Returns**: Boolean (True if valid)
- **Pattern**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

#### `validate_phone(phone)`
- **Purpose**: Validate phone number format
- **Parameters**:
  - `phone` (str): Phone number to validate
- **Returns**: Boolean (True if valid)
- **Validation**: 7-15 digits after removing non-digit characters

#### `format_phone(phone)`
- **Purpose**: Format phone number consistently
- **Parameters**:
  - `phone` (str): Phone number to format
- **Returns**: String (formatted phone number)
- **Formats**:
  - 10 digits: `(123) 456-7890`
  - 11 digits starting with 1: `+1 (123) 456-7890`
  - Other: Returns original

### Database Management

#### `get_table_info()`
- **Purpose**: Get information about the contacts table structure
- **Parameters**: None
- **Returns**: List of tuples (column information)
- **SQL**: `PRAGMA table_info(contacts)`

#### `add_column(column_name, column_type, default_value=None)`
- **Purpose**: Add a new column to the contacts table
- **Parameters**:
  - `column_name` (str): Name of the new column
  - `column_type` (str): Data type of the new column
  - `default_value` (str, optional): Default value for the column
- **Returns**: Boolean (True if successful)
- **SQL**: `ALTER TABLE contacts ADD COLUMN {column_name} {column_type} DEFAULT '{default_value}'`

#### `remove_column(column_name)`
- **Purpose**: Remove a column from the contacts table
- **Parameters**:
  - `column_name` (str): Name of the column to remove
- **Returns**: Boolean (True if successful)
- **Process**: Creates new table, copies data, drops old table

#### `backup_database()`
- **Purpose**: Create a backup of the current database
- **Parameters**: None
- **Returns**: String (backup filename)
- **Format**: `contacts_backup_YYYYMMDD_HHMMSS.db`

#### `restore_database(backup_filename)`
- **Purpose**: Restore database from backup
- **Parameters**:
  - `backup_filename` (str): Backup filename to restore
- **Returns**: Boolean (True if successful)

#### `cleanup_db()`
- **Purpose**: Delete all contacts from the database
- **Parameters**: None
- **Returns**: None
- **SQL**: `DELETE FROM contacts`

#### `reset_auto_increment()`
- **Purpose**: Reset the auto-increment counter
- **Parameters**: None
- **Returns**: None
- **SQL**: `DELETE FROM sqlite_sequence WHERE name='contacts'`

#### `full_cleanup_db()`
- **Purpose**: Complete database cleanup
- **Parameters**: None
- **Returns**: None
- **Process**: Calls `cleanup_db()` and `reset_auto_increment()`

### Categories and Tags

#### `add_category_column()`
- **Purpose**: Add category column to contacts table
- **Parameters**: None
- **Returns**: Boolean (True if successful)
- **Default**: 'General'

#### `add_tag_column()`
- **Purpose**: Add tags column to contacts table
- **Parameters**: None
- **Returns**: Boolean (True if successful)
- **Default**: Empty string

#### `get_contacts_by_category(category)`
- **Purpose**: Get contacts by category
- **Parameters**:
  - `category` (str): Category name
- **Returns**: List of tuples (matching contacts)
- **SQL**: `SELECT * FROM contacts WHERE category = ?`

#### `get_contacts_by_tag(tag)`
- **Purpose**: Get contacts containing a specific tag
- **Parameters**:
  - `tag` (str): Tag to search for
- **Returns**: List of tuples (matching contacts)
- **SQL**: `SELECT * FROM contacts WHERE tags LIKE ?`

### Data Integrity

#### `check_data_integrity()`
- **Purpose**: Check for data integrity issues
- **Parameters**: None
- **Returns**: List of strings (issues found)
- **Checks**:
  - Duplicate names
  - Invalid email formats
  - Empty names
- **Returns**: List of issue descriptions

## 🎮 Main Application Module (`main.py`)

### Menu Functions

#### `menu()`
- **Purpose**: Display the main menu
- **Parameters**: None
- **Returns**: None
- **Output**: Formatted menu display

#### `display_contacts(contacts)`
- **Purpose**: Display contacts in a formatted table
- **Parameters**:
  - `contacts` (list): List of contact tuples
- **Returns**: None
- **Format**: ID, Name, Phone, Email columns

### Menu Handlers

#### `add_contact_menu()`
- **Purpose**: Handle adding a new contact
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for input, validates, adds contact

#### `view_contacts_menu()`
- **Purpose**: Handle viewing all contacts
- **Parameters**: None
- **Returns**: None
- **Process**: Retrieves and displays all contacts

#### `search_contacts_menu()`
- **Purpose**: Handle searching contacts
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for search term, displays results

#### `update_contact_menu()`
- **Purpose**: Handle updating contacts
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for ID, field, and new value

#### `delete_contact_menu()`
- **Purpose**: Handle deleting contacts
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for ID, shows contact, confirms deletion

#### `cleanup_database_menu()`
- **Purpose**: Handle database cleanup
- **Parameters**: None
- **Returns**: None
- **Process**: Shows statistics, requires double confirmation

### Advanced Features Menu

#### `advanced_features_menu()`
- **Purpose**: Handle advanced features submenu
- **Parameters**: None
- **Returns**: None
- **Options**: 9 advanced feature options

#### `contact_analytics_menu()`
- **Purpose**: Display contact analytics
- **Parameters**: None
- **Returns**: None
- **Process**: Retrieves and displays analytics data

#### `advanced_search_menu()`
- **Purpose**: Handle advanced search
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for multiple search criteria

#### `export_data_menu()`
- **Purpose**: Handle data export
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for format, exports data

#### `import_data_menu()`
- **Purpose**: Handle data import
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for filename, imports data

#### `bulk_operations_menu()`
- **Purpose**: Handle bulk operations
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for operation type and parameters

#### `categories_tags_menu()`
- **Purpose**: Handle categories and tags
- **Parameters**: None
- **Returns**: None
- **Process**: Manages categories and tags

#### `data_validation_menu()`
- **Purpose**: Handle data validation
- **Parameters**: None
- **Returns**: None
- **Process**: Validates email and phone formats

#### `data_integrity_menu()`
- **Purpose**: Handle data integrity check
- **Parameters**: None
- **Returns**: None
- **Process**: Checks for data integrity issues

### Database Management Menu

#### `database_management_menu()`
- **Purpose**: Handle database management submenu
- **Parameters**: None
- **Returns**: None
- **Options**: 8 database management options

#### `view_database_stats()`
- **Purpose**: Display database statistics
- **Parameters**: None
- **Returns**: None
- **Process**: Retrieves and displays database statistics

#### `view_table_structure()`
- **Purpose**: Display table structure
- **Parameters**: None
- **Returns**: None
- **Process**: Retrieves and displays table schema

#### `add_column_menu()`
- **Purpose**: Handle adding columns
- **Parameters**: None
- **Returns**: None
- **Process**: Prompts for column details, adds column

#### `remove_column_menu()`
- **Purpose**: Handle removing columns
- **Parameters**: None
- **Returns**: None
- **Process**: Shows columns, prompts for removal, confirms

#### `backup_database_menu()`
- **Purpose**: Handle database backup
- **Parameters**: None
- **Returns**: None
- **Process**: Creates backup, displays filename

#### `restore_database_menu()`
- **Purpose**: Handle database restore
- **Parameters**: None
- **Returns**: None
- **Process**: Lists backups, prompts for selection, restores

### Main Application

#### `main()`
- **Purpose**: Main application loop
- **Parameters**: None
- **Returns**: None
- **Process**: Initializes database, runs main menu loop

## 🗄️ Database Schema

### Contacts Table
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    age INTEGER DEFAULT 0,
    address TEXT DEFAULT 'Unknown',
    department TEXT DEFAULT 'General',
    category TEXT DEFAULT 'General',
    tags TEXT DEFAULT ''
);
```

### Column Types
- **id**: INTEGER PRIMARY KEY AUTOINCREMENT
- **name**: TEXT NOT NULL
- **phone**: TEXT (optional)
- **email**: TEXT (optional)
- **age**: INTEGER (optional, default 0)
- **address**: TEXT (optional, default 'Unknown')
- **department**: TEXT (optional, default 'General')
- **category**: TEXT (optional, default 'General')
- **tags**: TEXT (optional, default '')

## 🔧 Error Handling

### Common Exceptions
- **sqlite3.OperationalError**: Database operation errors
- **ValueError**: Invalid input values
- **FileNotFoundError**: Missing files
- **PermissionError**: File access issues

### Error Recovery
- **Database Connection**: Automatic reconnection
- **File Operations**: Graceful error handling
- **User Input**: Input validation and error messages
- **Data Integrity**: Automatic data validation

## 📊 Performance Considerations

### Database Operations
- **Indexing**: Primary key on id column
- **Query Optimization**: Efficient SQL queries
- **Connection Management**: Proper connection handling
- **Memory Usage**: Efficient data structures

### File Operations
- **CSV Processing**: Efficient CSV reading/writing
- **JSON Processing**: Optimized JSON serialization
- **Backup Operations**: Efficient file copying
- **Import/Export**: Streamlined data processing

## 🛡️ Security Features

### Data Protection
- **Input Validation**: All user input validated
- **SQL Injection Prevention**: Parameterized queries
- **File Access Control**: Proper file permissions
- **Data Integrity**: Comprehensive data validation

### Backup Security
- **Automatic Backups**: Before destructive operations
- **Backup Verification**: Integrity checking
- **Recovery Options**: Multiple recovery methods
- **Data Encryption**: File system level security

---

**Version**: 2.0  
**Last Updated**: 2024  
**Technical Level**: Advanced  
**Compatibility**: Python 3.6+
