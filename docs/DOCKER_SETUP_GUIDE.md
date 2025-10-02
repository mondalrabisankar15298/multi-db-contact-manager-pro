# 🚀 Multi-Database Contact Manager - Docker Setup Guide

> **Complete Docker Setup for Multi-Database Contact Manager with SQLite, MySQL, PostgreSQL & MongoDB**

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Detailed Setup Steps](#detailed-setup-steps)
- [Project Structure](#project-structure)
- [Configuration Files](#configuration-files)
- [Database Services](#database-services)
- [Running the Application](#running-the-application)
- [Accessing Services](#accessing-services)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

---

## 📋 Prerequisites

### Required Software
- **Docker** (version 24.0+ recommended)
- **Docker Compose** (version 2.20+ recommended)
- **Git** (for cloning repositories)

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Disk Space**: 5GB+ free space
- **OS**: Linux, macOS, or Windows with WSL2

### Installation Commands

#### Ubuntu/Debian
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (optional)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

#### macOS
```bash
# Install Docker Desktop
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

#### Windows
```bash
# Install Docker Desktop for Windows
# Download from: https://www.docker.com/products/docker-desktop
```

---

## 🎯 Project Overview

This project provides a **complete multi-database contact management system** with:

- ✅ **SQLite** - Local file-based database
- ✅ **MySQL** - Relational database
- ✅ **PostgreSQL** - Advanced relational database
- ✅ **MongoDB** - NoSQL document database
- ✅ **Adminer** - Web-based database administration
- ✅ **Runtime database switching** - Change databases without restarting
- ✅ **Docker containerization** - Complete isolation and portability

---

## ⚡ Quick Start

### One-Line Setup (Recommended)
```bash
# Clone and run
git clone <your-repo-url>
cd multi-db-contact-manager-pro
./start-docker-app.sh
```

### Manual Setup
```bash
# Clone repository
git clone <your-repo-url>
cd multi-db-contact-manager-pro

# Start all services
docker compose --profile full up --build
```

---

## 📝 Detailed Setup Steps

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd multi-db-contact-manager-pro
```

### Step 2: Verify Docker Installation
```bash
# Check Docker version
docker --version
docker compose version

# Verify Docker is running
docker info
```

### Step 3: Review Project Files
Ensure you have all required files:
```bash
ls -la
# Should see: docker-compose.yml, Dockerfile, requirements.txt, etc.
```

### Step 4: Configure Environment (Optional)
Edit `docker.env` if you need custom database credentials:
```bash
# Edit database credentials if needed
nano docker.env
```

### Step 5: Start the Application
```bash
# Option 1: Quick start (recommended)
./start-docker-app.sh

# Option 2: Manual start
docker compose --profile full up --build

# Option 3: Background mode
docker compose --profile full up -d --build
```

### Step 6: Verify Services are Running
```bash
# Check all containers
docker compose ps

# Check logs
docker compose logs
```

---

## 📁 Project Structure

```
multi-db-contact-manager-pro/
├── 📁 config/                    # Database configuration
│   ├── database_config.py        # Database connection settings
│   └── settings.py               # Application settings
├── 📁 database/                  # Multi-database architecture
│   ├── base.py                   # Abstract database adapter
│   ├── factory.py                # Database factory
│   ├── manager.py                # Database manager (singleton)
│   └── 📁 adapters/              # Concrete database adapters
│       ├── sqlite_adapter.py     # SQLite implementation
│       └── mysql_adapter.py      # MySQL implementation
├── 📁 docker/                    # Database initialization scripts
│   ├── mysql-init/
│   │   └── 01-create-tables.sql
│   ├── postgres-init/
│   │   └── 01-create-tables.sql
│   └── mongo-init/
│       └── 01-create-collection.js
├── 🐳 docker-compose.yml         # Multi-service orchestration
├── 🐳 Dockerfile                 # Application container
├── 🐳 docker.env                 # Environment variables
├── 🐍 main.py                    # Main application entry point
├── 🐍 core_operations.py         # Core business logic
├── 🐍 ui.py                      # User interface components
├── 🐍 menus.py                   # Menu system
├── 🐍 input_helpers.py           # Input validation
├── 🐍 navigation.py              # Navigation logic
├── 📚 requirements.txt           # Python dependencies
├── 🔧 start-docker-app.sh        # Quick start script
├── 🔧 start-databases-only.sh    # Database-only script
├── 🔧 run-docker.sh              # Advanced management script
├── 📚 DOCKER_SETUP_GUIDE.md      # This guide
├── 📚 README.md                  # Main documentation
└── 📚 USER_GUIDE.md              # User manual
```

---

## ⚙️ Configuration Files

### docker-compose.yml
Main orchestration file with 5 services:
- **contact-manager**: Python application
- **mysql**: MySQL database
- **postgres**: PostgreSQL database
- **mongodb**: MongoDB database
- **adminer**: Database administration tool

### Dockerfile
Python application container with:
- Python 3.11 slim base image
- Database drivers (PyMySQL, psycopg2, pymongo)
- SQLAlchemy ORM
- Tabulate for table formatting

### docker.env
Environment variables:
```env
# Database Configuration
DB_TYPE=sqlite
SQLITE_PATH=contacts.db

MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=contact_user
MYSQL_PASSWORD=contact_password
MYSQL_DATABASE=contacts

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=contact_user
POSTGRES_PASSWORD=contact_password
POSTGRES_DATABASE=contacts

MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_DATABASE=contacts
```

---

## 🗄️ Database Services

### Port Mappings
| Service | Host Port | Container Port | Access URL |
|---------|-----------|----------------|------------|
| **Adminer** | 8050 | 8050 | http://localhost:8050 |
| **PostgreSQL** | 5433 | 5433 | localhost:5433 |
| **MySQL** | 3306 | 3306 | localhost:3306 |
| **MongoDB** | 27017 | 27017 | localhost:27017 |

### 🔐 Database Credentials

#### **MySQL Database**
- **Host**: `localhost:3306` (external access from your machine)
- **Server**: `mysql` (Docker service name for internal connections)
- **Username**: `contact_user`
- **Password**: `contact_password`
- **Database**: `contacts`
- **Root Password**: `rootpassword` (for admin access)

#### **PostgreSQL Database**
- **Host**: `localhost:5433` (external access from your machine)
- **Server**: `postgres` (Docker service name for internal connections)
- **Username**: `contact_user`
- **Password**: `contact_password`
- **Database**: `contacts`

#### **MongoDB Database**
- **Host**: `localhost:27017` (external access from your machine)
- **Server**: `mongodb` (Docker service name for internal connections)
- **Database**: `contacts`
- **Username**: *(none required)*
- **Password**: *(none required)*
- **Authentication**: Disabled (development mode)

#### **SQLite Database** (Local File)
- **File Path**: `contacts.db` (in project root)
- **No credentials required**
- **Automatic initialization**

### 🔧 Adminer Login Credentials

Adminer (http://localhost:8050) supports all databases:

| Database Type | System | Server | Username | Password | Database |
|---------------|--------|--------|----------|----------|----------|
| **MySQL** | `MySQL` | `mysql` | `contact_user` | `contact_password` | `contacts` |
| **PostgreSQL** | `PostgreSQL` | `postgres` | `contact_user` | `contact_password` | `contacts` |
| **MongoDB** | `MongoDB` | `mongodb` | *(leave empty)* | *(leave empty)* | `contacts` |
| **SQLite** | `SQLite 3` | `/app/contacts.db` | *(leave empty)* | *(leave empty)* | *(leave empty)* |


### 📝 Connection Examples

#### Direct Database Connections

**MySQL:**
```bash
# From host machine (use localhost/127.0.0.1)
mysql -h localhost -P 3306 -u contact_user -pcontact_password contacts

# From inside container (use service name 'mysql')
docker exec -it contact-mysql mysql -h mysql -u contact_user -pcontact_password contacts
```

**PostgreSQL:**
```bash
# From host machine (use localhost/127.0.0.1)
psql -h localhost -p 5433 -U contact_user -d contacts

# From inside container (use service name 'postgres')
docker exec -it contact-postgres psql -h postgres -U contact_user -d contacts
```

**MongoDB:**
```bash
# From host machine (use localhost/127.0.0.1)
mongosh mongodb://localhost:27017/contacts

# From inside container (use service name 'mongodb')
docker exec -it contact-mongodb mongosh mongodb://mongodb:27017/contacts
```

**Note**: Inside Docker containers, use the **Server names** (mysql, postgres, mongodb) to connect between containers. From your host machine, use **localhost** or **127.0.0.1**.

### 🔑 Default Credentials Summary
| Database | Username | Password | Database |
|----------|----------|----------|----------|
| **MySQL** | contact_user | contact_password | contacts |
| **PostgreSQL** | contact_user | contact_password | contacts |
| **MongoDB** | *(none)* | *(none)* | contacts |

### Database Features
- **Automatic initialization** on first startup
- **Persistent data** using Docker named volumes
- **Health checks** to ensure services are ready
- **Sample data** inserted automatically

---

## 🚀 Running the Application

### Start Options

#### Option 1: Full Application (Recommended)
```bash
./start-docker-app.sh
```
- Starts all services + application
- Shows interactive menu immediately
- Press Ctrl+C to stop everything

#### Option 2: Databases Only
```bash
./start-databases-only.sh
```
- Starts only database services
- Run Python app locally: `python main.py`

#### Option 3: Manual Control
```bash
# Start everything
docker compose --profile full up --build

# Start in background
docker compose --profile full up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Application Features
- ✅ **Add/View/Update/Delete** contacts
- ✅ **Search** by name, phone, email
- ✅ **Advanced search** with filters
- ✅ **Database switching** at runtime
- ✅ **Import/Export** (CSV, JSON)
- ✅ **Analytics** and statistics

---

## 🌐 Accessing Services

### Contact Manager Application
```bash
# If running in Docker (recommended)
docker attach contact-manager-app

# Or if running locally
python main.py
```

### Database Administration (Adminer)
- **URL**: http://localhost:8050
- **Login**: Select database type, enter credentials above

### Direct Database Access
```bash
# MySQL
docker exec -it contact-mysql mysql -u contact_user -pcontact_password contacts

# PostgreSQL
docker exec -it contact-postgres psql -U contact_user -d contacts

# MongoDB
docker exec -it contact-mongodb mongosh contacts
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using ports
lsof -i :8050
lsof -i :5433

# Change ports in docker-compose.yml
ports:
  - "8051:8050"  # Change host port
```

#### 2. Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

#### 3. Database Connection Failed
```bash
# Check database health
docker compose ps

# View database logs
docker compose logs mysql
docker compose logs postgres
docker compose logs mongodb
```

#### 4. Application Won't Start
```bash
# Check application logs
docker compose logs contact-manager

# Rebuild container
docker compose build --no-cache contact-manager
```

#### 5. Out of Disk Space
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Health Checks
```bash
# Check all services health
docker compose ps

# Test database connections
docker exec contact-mysql mysqladmin ping -u contact_user -pcontact_password
docker exec contact-postgres pg_isready -U contact_user
docker exec contact-mongodb mongosh --eval "db.adminCommand('ping')"
```

---

## 🔄 Development Workflow

### Making Code Changes
```bash
# 1. Edit Python files
nano main.py

# 2. Rebuild and restart
docker compose build contact-manager
docker compose up -d contact-manager

# 3. Check logs
docker compose logs -f contact-manager
```

### Adding New Dependencies
```bash
# 1. Edit requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# 2. Rebuild container
docker compose build contact-manager
docker compose up -d contact-manager
```

### Database Schema Changes
```bash
# Edit initialization scripts
nano docker/mysql-init/01-create-tables.sql

# Restart to apply changes
docker compose down
docker compose up --build
```

### Backup and Restore
```bash
# Backup databases
docker exec contact-mysql mysqldump -u contact_user -p contacts > backup.sql
docker exec contact-postgres pg_dump -U contact_user contacts > backup.sql

# Restore databases
docker exec -i contact-mysql mysql -u contact_user -p contacts < backup.sql
docker exec -i contact-postgres psql -U contact_user contacts < backup.sql
```

---

## 📊 Monitoring and Management

### View Resource Usage
```bash
# Container resource usage
docker stats

# Disk usage
docker system df -v
```

### Management Commands
```bash
# Stop all services
docker compose down

# Stop and remove data (CAUTION!)
docker compose down -v

# Restart specific service
docker compose restart contact-manager

# Scale services (if needed)
docker compose up -d --scale contact-manager=2
```

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Start everything
./start-docker-app.sh

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Clean restart
docker compose down && docker compose up --build
```

### 🔑 Database Credentials

| Database | Server | Host:Port | Username | Password | Database |
|----------|--------|-----------|----------|----------|----------|
| **MySQL** | mysql | localhost:3306 | contact_user | contact_password | contacts |
| **PostgreSQL** | postgres | localhost:5433 | contact_user | contact_password | contacts |
| **MongoDB** | mongodb | localhost:27017 | *(none)* | *(none)* | contacts |
| **Adminer** | - | localhost:8050 | [Web UI](http://localhost:8050) | - | - |

### Port Reference
```bash
Adminer:    http://localhost:8050
PostgreSQL: localhost:5433
MySQL:      localhost:3306
MongoDB:    localhost:27017
```

### Database Credentials
```bash
Username: contact_user
Password: contact_password
Database: contacts
```

---

## 🎉 Success Checklist

- [ ] Docker installed and running
- [ ] Repository cloned
- [ ] `./start-docker-app.sh` executed
- [ ] All containers show "healthy" status
- [ ] Contact Manager menu appears
- [ ] Adminer accessible at http://localhost:8050
- [ ] Database switching works
- [ ] Can add/view/edit contacts

---

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review container logs: `docker compose logs`
3. Verify port availability: `docker compose ps`
4. Check system resources: `docker system df`

**Happy coding with your multi-database contact manager!** 🚀✨
