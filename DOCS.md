# 📒 Multi-Database Contact Manager Pro

A professional contact management system supporting SQLite, MySQL, PostgreSQL, and MongoDB with dynamic schema management and advanced features.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)

### Choose Your Deployment Method

#### Option A: Full Docker (Recommended)
Everything runs in containers:
```bash
# Clone the repository
git clone <repository-url>
cd multi-db-contact-manager-pro

# Copy environment configuration
cp docker.env.example docker.env

# Start everything in Docker
docker compose --profile full up --build

# In another terminal, connect to the app
docker compose exec contact-manager python main.py
```

#### Option B: Local Development
Databases in Docker, app locally:
```bash
# Clone the repository
git clone <repository-url>
cd multi-db-contact-manager-pro

# Install Python dependencies
pip install -r requirements.txt

# Copy environment configuration
cp docker.env.example docker.env

# Start database containers
docker compose up -d mysql postgres mongodb

# Run the application locally
python main.py
```

#### Option C: Use Quick Start Scripts
```bash
# For full Docker deployment
./start-docker-app.sh

# OR for databases only (run app locally)
./start-databases-only.sh
python main.py
```

## 🗄️ Multi-Database Support

### Supported Databases
- **SQLite** - File-based, no server required
- **MySQL** - Popular relational database
- **PostgreSQL** - Advanced relational database  
- **MongoDB** - Document-based NoSQL

### Database Switching
The application automatically tests all databases and selects the healthiest one. You can switch databases through the menu:
```
Main Menu → 8. Switch Database
```

### Configuration
Database settings are configured in `docker.env`:
```bash
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=contact_user
MYSQL_PASSWORD=contact_password

# PostgreSQL  
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_USER=contact_user
POSTGRES_PASSWORD=contact_password

# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=contacts
```

## 🏗️ Dynamic Schema Management

### Core Schema
All databases maintain a consistent 4-column base schema:
- `id` - Auto-increment primary key
- `name` - Contact name (required)
- `phone` - Phone number (optional)
- `email` - Email address (optional)

### Dynamic Columns
Add custom fields dynamically:
```
Database Management → Column Management → Add Column
```

Supported column types:
- TEXT - String data
- INTEGER - Numeric data
- REAL - Decimal numbers
- Custom types (database-specific)

## 📋 Features

### Core Operations
- ➕ **Add Contact** - Create new contacts with validation
- 👀 **View Contacts** - Display all contacts in formatted tables
- 🔍 **Search** - Find contacts by name, phone, or email
- ✏️ **Update** - Modify contact information
- 🗑️ **Delete** - Remove contacts with confirmation

### Advanced Features
- 📊 **Analytics** - Contact statistics and reporting
- 🔍 **Advanced Search** - Multi-criteria filtering
- 📤 **Export** - CSV and JSON export
- 📥 **Import** - CSV import with validation
- 🔄 **Bulk Operations** - Update/delete multiple contacts
- ✅ **Data Validation** - Email and phone validation

### Database Management
- 📊 **Statistics** - Database size and performance metrics
- 🏗️ **Schema** - View and modify table structure
- ➕ **Add Columns** - Dynamic schema expansion
- 💾 **Backup** - Automated database backups
- 🔄 **Restore** - Restore from backup files
- 🧹 **Cleanup** - Database maintenance tools

## 🐳 Docker Deployment

### Option 1: Development (Databases Only)
Run databases in Docker, app locally in venv:
```bash
# Start database containers
docker compose up -d mysql postgres mongodb

# Install dependencies locally
pip install -r requirements.txt

# Run app locally
python main.py
```

### Option 2: Full Docker Deployment
Run everything (app + databases) in Docker:
```bash
# Build and start all services
docker compose --profile full up --build

# Or run in background
docker compose --profile full up --build -d

# Connect to running app container
docker compose exec contact-manager python main.py
```

### Option 3: Quick Start Scripts
Use provided convenience scripts:

**For databases only:**
```bash
./start-databases-only.sh
```

**For full Docker deployment:**
```bash
./start-docker-app.sh
```

### Docker Services

**Database Services (always available):**
- `mysql` - MySQL 8.0 on port 3306
- `postgres` - PostgreSQL 15 on port 5433  
- `mongodb` - MongoDB 7.0 on port 27017
- `adminer` - Database admin tool on port 8050

**Application Service (with `--profile full`):**
- `contact-manager` - Python app container

### Environment Configuration
- **Local Development**: Uses `localhost` hostnames in `docker.env`
- **Docker Containers**: `docker-compose.yml` overrides to container hostnames
- **Automatic Override**: No manual configuration needed

### Docker Commands

**Start databases only:**
```bash
docker compose up -d mysql postgres mongodb
```

**Start everything:**
```bash
docker compose --profile full up --build
```

**View logs:**
```bash
docker compose logs -f contact-manager
```

**Stop services:**
```bash
docker compose down
```

**Rebuild and restart:**
```bash
docker compose --profile full up --build --force-recreate
```

## 🔧 Architecture

### Project Structure
```
multi-db-contact-manager-pro/
├── main.py                 # Application entry point
├── core_operations.py      # Business logic layer
├── menus.py               # User interface menus
├── ui.py                  # Display utilities
├── dynamic_ui.py          # Dynamic schema UI
├── preflight.py           # Database health checks
├── state_tracker.py       # Application state management
├── schema_manager.py      # Dynamic schema management
├── database/              # Database abstraction layer
│   ├── base.py           # Database adapter interface
│   ├── factory.py        # Adapter factory
│   ├── manager.py        # Database manager
│   └── adapters/         # Database-specific implementations
├── config/               # Configuration management
├── docker/              # Docker initialization scripts
└── data/               # SQLite databases and app state
```

### Database Abstraction
All database operations go through a unified adapter interface:
```python
# Same code works with any database
from core_operations import add_contact, view_contacts, switch_database

# Add contact (works with any database)
add_contact(name="John Doe", phone="555-0123", email="john@example.com")

# Switch database
switch_database('postgres')

# Same operations work immediately
contacts = view_contacts()
```

## 🛡️ Data Validation & Safety

### Input Validation
- **Email**: RFC-compliant email format validation
- **Phone**: International phone number validation (7-15 digits)
- **Required Fields**: Name is required, others optional

### Safety Features
- **Confirmation Prompts**: Multiple confirmations for destructive operations
- **Automatic Backups**: Before major operations
- **Data Integrity Checks**: Detect duplicates and invalid data
- **Error Handling**: Comprehensive error management

## 📊 Analytics & Reporting

### Contact Analytics
- Total contact count
- Phone/email completion rates
- Top email domains
- Data quality metrics

### Database Statistics
- Record counts
- Database size
- Column information
- Performance metrics

## 🔍 Search Capabilities

### Basic Search
- Search across name, phone, email
- Case-insensitive matching
- Partial string matching

### Advanced Search
- Multi-field filtering
- ID range searches
- Complex query combinations

## 📤 Import/Export

### Export Formats
- **CSV**: Spreadsheet-compatible format
- **JSON**: Structured data format
- **UTF-8**: Full Unicode support

### Import Features
- CSV import with automatic column mapping
- Data validation during import
- Import statistics and error reporting

## 🔄 Bulk Operations

### Bulk Update
- Update multiple contacts simultaneously
- Field-specific updates
- Safety confirmations

### Bulk Delete
- Delete multiple contacts at once
- ID-based selection
- Multiple confirmation prompts

## 🏷️ Organization

### Categories & Tags
- Organize contacts by categories
- Flexible tagging system
- Filter by categories/tags
- Dynamic category management

## 💾 Backup & Recovery

### Automatic Backups
- Timestamped backup files
- Before destructive operations
- Configurable backup intervals

### Restore Options
- Select from available backups
- Safe restoration process
- Data verification after restore

## 🚀 Performance

### Optimizations
- Efficient database queries
- Batch processing for bulk operations
- Memory-optimized operations
- Fast search algorithms

### Scalability
- Handle thousands of contacts
- Optimized for large datasets
- Efficient memory usage

## 🔧 Development

### Adding New Database Support
1. Create adapter in `database/adapters/`
2. Implement `DatabaseAdapter` interface
3. Register in `DatabaseFactory`
4. Add configuration in `database_config.py`

### Testing
```bash
# Test all databases
python test_all_databases.py

# Test specific database
MYSQL_HOST=localhost python test_all_databases.py
```

## 📞 Troubleshooting

### Common Issues

**Database Connection Failed**
- Ensure Docker containers are running
- Check host configuration in `docker.env`
- Verify ports are not in use

**Import Errors**
- Check CSV format and headers
- Ensure proper encoding (UTF-8)
- Validate data before import

**Performance Issues**
- Use bulk operations for large datasets
- Regular database cleanup
- Monitor database size

### Health Checks
The application runs automatic health checks on startup and stores results in `data/app_state.db`. Unhealthy databases are marked as unavailable in the switch menu.

## 🎯 Best Practices

### Data Management
- Regular backups before major changes
- Use data validation features
- Keep contact information current
- Organize with categories/tags

### Performance
- Use bulk operations for efficiency
- Regular database maintenance
- Monitor database growth
- Clean up unused data

### Security
- Change default passwords in production
- Use strong database credentials
- Regular security updates
- Limit database permissions

---

**Version**: 3.0 - Multi-Database Contact Manager Pro  
**License**: Open Source  
**Support**: See troubleshooting section above
