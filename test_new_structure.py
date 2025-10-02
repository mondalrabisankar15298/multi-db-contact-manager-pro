#!/usr/bin/env python3
"""
Test script for the new project structure
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if key imports work with new structure."""
    try:
        print("🧪 Testing new project structure...")
        
        # Test core imports
        print("📦 Testing core imports...")
        from contact_manager.database.manager import db_manager
        from contact_manager.core.schema_manager import schema_manager
        from contact_manager.config.settings import settings
        print("✅ Core imports successful")
        
        # Test database connection
        print("🔌 Testing database connection...")
        db_manager.switch_database('sqlite')  # Use SQLite for testing
        print("✅ Database connection successful")
        
        # Test basic operations
        print("🔧 Testing basic operations...")
        from contact_manager.core.core_operations import view_contacts
        contacts = view_contacts()
        print(f"✅ Found {len(contacts)} contacts in database")
        
        print("\n🎉 New project structure is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
