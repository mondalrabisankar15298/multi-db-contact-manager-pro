"""
Database Menu Handler
Handles database management and switching operations.
"""

import os
from ..database.manager import db_manager
from ..ui.ui import display_success, display_error, display_warning
from ..core.core_operations import view_contacts


class DatabaseMenuHandler:
    """Handles database-related menu operations."""
    
    def show_database_menu(self) -> None:
        """Show the database management menu."""
        while True:
            try:
                print("\n⚙️  Database Management")
                print("="*50)
                print("1. 📊 Database Statistics")
                print("2. 🔧 Table Structure")
                print("3. 🧹 Clean Database")
                print("4. 💾 Backup Database")
                print("5. 📥 Restore Database")
                print("6. 🔄 Reset Database")
                print("7. 🌍 Timezone Configuration")
                print("8. 🏗️  Column Management")
                print("0. 🔙 Back to Previous Menu")
                print("111. 🚪 Exit Application")
                print("="*50)
                
                choice = input("\nEnter your choice (0-8, 111): ").strip()
                
                if choice == "0":
                    break
                elif choice == "111":
                    print("\n👋 Thank you for using Contact Book Manager!")
                    exit()
                elif choice == "1":
                    self.show_database_stats()
                elif choice == "2":
                    self.show_table_structure()
                elif choice == "3":
                    self.handle_clean_database()
                elif choice == "4":
                    self.handle_backup_database()
                elif choice == "5":
                    self.handle_restore_database()
                elif choice == "6":
                    self.handle_reset_database()
                elif choice == "7":
                    self.show_timezone_info()
                elif choice == "8":
                    self.show_column_management()
                else:
                    display_error("Invalid choice! Please enter 0-8 or 111.")
                    
            except Exception as e:
                display_error(f"Database menu error: {str(e)}")
    
    def show_database_stats(self) -> None:
        """Show database statistics."""
        try:
            from ..ui.ui import display_database_stats
            display_database_stats()
            input("\nPress Enter to continue...")
        except Exception as e:
            display_error(f"Database stats error: {str(e)}")
    
    def show_table_structure(self) -> None:
        """Show table structure."""
        try:
            from ..ui.ui import display_table_structure
            display_table_structure()
            input("\nPress Enter to continue...")
        except Exception as e:
            display_error(f"Table structure error: {str(e)}")
    
    def show_timezone_info(self) -> None:
        """Show timezone configuration."""
        try:
            import os
            current_tz_setting = os.getenv('DISPLAY_TIMEZONE', 'Asia/Kolkata')
            
            print(f"\n🌍 Timezone Configuration")
            print("="*40)
            print(f"Current Setting: {current_tz_setting}")
            print(f"\n💡 To change timezone, update DISPLAY_TIMEZONE in docker.env")
            print(f"   Examples: America/New_York, Europe/London, UTC")
            
            try:
                from ..utils.timezone_utils import get_timezone_info
                tz_info = get_timezone_info()
                print(f"\n📊 Current Timezone Info:")
                print(f"   Name: {tz_info['timezone_name']}")
                print(f"   Abbreviation: {tz_info['timezone_abbreviation']}")
                print(f"   UTC Offset: {tz_info['utc_offset']}")
                print(f"   Current Time: {tz_info['current_time']}")
            except Exception:
                pass
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            display_error(f"Timezone info error: {str(e)}")
    
    def switch_database(self) -> None:
        """Handle database switching with connection status display."""
        try:
            # Get current database and health status
            current_db = db_manager.current_db_type
            
            # Get health status for all databases
            try:
                from ..core.state_tracker import get_db_health_map, get_db_health_details
                health_map = get_db_health_map()
                health_details = get_db_health_details()
            except Exception:
                health_map = {}
                health_details = {}
            
            # Database display information
            db_info = {
                "sqlite": {"emoji": "💾", "name": "SQLite", "subtitle": "Local file database"},
                "mysql": {"emoji": "🐬", "name": "MySQL", "subtitle": "Popular relational database"},
                "postgres": {"emoji": "🐘", "name": "PostgreSQL", "subtitle": "Advanced relational database"},
                "mongodb": {"emoji": "🍃", "name": "MongoDB", "subtitle": "Document-based NoSQL"}
            }
            
            print("\nDatabase Options:")
            
            db_map = {
                "1": "sqlite",
                "2": "mysql", 
                "3": "postgres",
                "4": "mongodb"
            }
            
            for choice, db_type in db_map.items():
                info = db_info.get(db_type, {"emoji": "🗄️", "name": db_type.title(), "subtitle": "Database"})
                
                # Determine status indicators
                if db_type == current_db:
                    current_marker = "➤"
                    current_text = " (current)"
                else:
                    current_marker = " "
                    current_text = ""
                
                # Check health status
                is_healthy = health_map.get(db_type, 0) == 1
                status_icon = "[ONLINE]" if is_healthy else "[OFFLINE]"
                
                print(f"{current_marker} {choice}. {info['name']}{current_text} {status_icon}")
            
            print("  0. Cancel")
            
            choice = input("\nSelect database (0-4): ").strip()
            
            if choice == "0":
                return
            elif choice in db_map:
                db_type = db_map[choice]
                
                if db_type == current_db:
                    display_warning(f"Already connected to {db_type.upper()}!")
                    return
                
                print(f"\n🔄 Switching to {db_type.upper()}...")
                
                success = db_manager.switch_database(db_type)
                if success:
                    display_success(f"✅ Successfully switched to {db_type.upper()}!")
                    
                    # Update health status after successful switch
                    try:
                        from ..core.state_tracker import set_db_health
                        set_db_health(db_type, True, "Connected successfully")
                    except Exception:
                        pass
                else:
                    display_error(f"❌ Failed to switch to {db_type.upper()}. Check connection settings.")
                    
                    # Update health status after failed switch
                    try:
                        from ..core.state_tracker import set_db_health
                        set_db_health(db_type, False, "Connection failed during switch")
                    except Exception:
                        pass
            else:
                display_error("Invalid choice! Please enter 0-4.")
                
        except Exception as e:
            display_error(f"Database switch error: {str(e)}")
    
    def handle_clean_database(self) -> None:
        """Handle database cleanup with multiple options."""
        while True:
            print("\n🧹 Database Cleanup Options")
            print("="*50)
            
            try:
                contacts = view_contacts()
                contact_count = len(contacts)
                current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
                print(f"🗄️  Current Database: {current_db}")
                print(f"📊 Current contacts in database: {contact_count}")
            except Exception:
                contact_count = 0
                print("📊 Current contacts in database: Unknown")
            
            print("\nChoose cleanup type:")
            print("0. 🔙 Back to Previous Menu")
            print("1. 🧽 Light Cleanup (Remove empty/invalid records)")
            print("2. 🗑️  Delete All Data (Keep table structure & columns)")
            print("3. 🔄 Reset Table Structure (Reset to 6 base columns)")
            print("="*50)
            
            choice = input("\nEnter your choice (0-3): ").strip()
            
            if choice == '0':
                return
            elif choice == '1':
                self._light_cleanup_menu(contact_count)
            elif choice == '2':
                self._delete_all_data_menu(contact_count)
            elif choice == '3':
                self._reset_table_structure_menu(contact_count)
            else:
                display_error("Invalid choice! Please enter 0-3.")
    
    def _light_cleanup_menu(self, contact_count: int) -> None:
        """Perform light cleanup - remove empty/invalid records."""
        print("\n🧽 Light Cleanup")
        print("-" * 40)
        
        try:
            if contact_count == 0:
                print("ℹ️  Database is already empty!")
                input("\nPress Enter to continue...")
                return
            
            print("This will remove contacts with:")
            print("• Empty or null names")
            print("• Other invalid data patterns")
            print("\n💡 This is a safe operation that preserves valid data.")
            
            confirm = input("\nProceed with light cleanup? (Y/n): ").strip().lower()
            
            if confirm in ['', 'y', 'yes']:
                print("\n🧽 Performing light cleanup...")
                cleaned_count = db_manager.current_adapter.cleanup_db()
                
                if cleaned_count > 0:
                    display_success(f"✅ Light cleanup completed! Removed {cleaned_count} invalid records.")
                else:
                    print("ℹ️  No invalid records found. Database is clean!")
            else:
                print("ℹ️  Light cleanup cancelled.")
                
        except Exception as e:
            display_error(f"Light cleanup error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _delete_all_data_menu(self, contact_count: int) -> None:
        """Delete all data but keep table structure."""
        print("\n🗑️ Delete All Data")
        print("-" * 40)
        
        try:
            if contact_count == 0:
                print("ℹ️  Database is already empty!")
                input("\nPress Enter to continue...")
                return
            
            display_warning("⚠️  This will delete ALL contacts from the database!")
            print("ℹ️  Table structure and custom columns will remain intact.")
            print("❌ This action cannot be undone!")
            
            confirm1 = input("\nAre you sure you want to delete ALL contacts? (y/N): ").strip().lower()
            
            if confirm1 not in ['y', 'yes']:
                print("ℹ️  Cleanup cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Double confirmation for safety
            print("\n🔒 Final confirmation required:")
            confirm2 = input("Type 'DELETE ALL' to confirm: ").strip()
            
            if confirm2 == 'DELETE ALL':
                print("\n🗑️  Deleting all contacts...")
                result = db_manager.current_adapter.full_cleanup_db()
                
                if result:
                    display_success("✅ All data deleted successfully!")
                    print("🧹 All contacts removed, table structure intact.")
                else:
                    display_error("❌ Cleanup failed!")
            else:
                print("ℹ️  Cleanup cancelled - confirmation text did not match.")
                
        except Exception as e:
            display_error(f"Delete all data error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _reset_table_structure_menu(self, contact_count: int) -> None:
        """Reset table to base 6-column structure."""
        print("\n🔄 Reset Table Structure")
        print("-" * 40)
        
        try:
            current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
            print(f"🗄️  Current Database: {current_db}")
            print(f"📊 Current contacts: {contact_count}")
            
            # Show current table structure
            try:
                from ..core.schema_manager import schema_manager
                columns = schema_manager.get_table_columns()
                print(f"\n📋 Current table has {len(columns)} columns:")
                for i, col in enumerate(columns, 1):
                    print(f"   {i}. {col}")
            except Exception:
                print("\n📋 Current table structure: Unable to retrieve")
            
            display_warning("\n⚠️  WARNING: This will:")
            print("❌ Delete ALL contacts and data")
            print("❌ Remove ALL custom columns")
            print("✅ Reset table to 6 base columns: id, name, phone, email, created_at, updated_at")
            print("❌ This action cannot be undone!")
            
            confirm1 = input("\nAre you sure you want to reset the table structure? (y/N): ").strip().lower()
            
            if confirm1 not in ['y', 'yes']:
                print("ℹ️  Table reset cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Double confirmation for safety
            print("\n🔒 Final confirmation required:")
            print("This will permanently destroy all data and custom columns!")
            confirm2 = input("Type 'RESET TABLE' to confirm: ").strip()
            
            if confirm2 == 'RESET TABLE':
                print("\n🔄 Resetting table structure...")
                result = db_manager.current_adapter.reset_table_structure()
                
                if result:
                    display_success("✅ Table structure reset successfully!")
                    print("🔄 Table now has 6 base columns with no data.")
                else:
                    display_error("❌ Table reset failed!")
            else:
                print("ℹ️  Table reset cancelled - confirmation text did not match.")
                
        except Exception as e:
            display_error(f"Reset table structure error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def handle_backup_database(self) -> None:
        """Handle database backup creation."""
        print("\n💾 Backup Database")
        print("="*40)
        
        try:
            current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
            print(f"🗄️  Current Database: {current_db}")
            
            # Show current contact count
            try:
                contacts = view_contacts()
                contact_count = len(contacts)
                print(f"📊 Contacts to backup: {contact_count}")
            except Exception:
                print("📊 Contacts to backup: Unknown")
            
            # Create backup directory if it doesn't exist
            backup_dir = "db_backup"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                print(f"📁 Created backup directory: {backup_dir}/")
            
            print(f"\n💾 Backup will be saved to: {backup_dir}/")
            print("💡 Backup filename will include timestamp for uniqueness.")
            
            confirm = input("\nProceed with database backup? (Y/n): ").strip().lower()
            
            if confirm in ['', 'y', 'yes']:
                print(f"\n💾 Creating {current_db} database backup...")
                
                try:
                    backup_filename = db_manager.current_adapter.backup_database()
                    
                    if backup_filename:
                        display_success(f"✅ Backup created successfully!")
                        print(f"📁 Backup file: {backup_filename}")
                        
                        # Show file size if possible
                        try:
                            if os.path.exists(backup_filename):
                                file_size = os.path.getsize(backup_filename)
                                if file_size < 1024:
                                    size_str = f"{file_size} bytes"
                                elif file_size < 1024 * 1024:
                                    size_str = f"{file_size / 1024:.1f} KB"
                                else:
                                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                                print(f"📊 File size: {size_str}")
                        except Exception:
                            pass
                        
                        print("\n💡 You can restore this backup using the 'Restore Database' option.")
                    else:
                        display_error("❌ Backup creation failed!")
                        
                except Exception as e:
                    display_error(f"❌ Backup error: {str(e)}")
                    
                    # Provide database-specific troubleshooting
                    if current_db == "POSTGRESQL":
                        print("\n💡 PostgreSQL backup troubleshooting:")
                        print("   • Ensure pg_dump is installed and in PATH")
                        print("   • Check database connection settings")
                    elif current_db == "MYSQL":
                        print("\n💡 MySQL backup troubleshooting:")
                        print("   • Ensure mysqldump is installed and in PATH")
                        print("   • Check database connection settings")
            else:
                print("ℹ️  Backup cancelled.")
                
        except Exception as e:
            display_error(f"Backup handler error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def handle_restore_database(self) -> None:
        """Handle database restore from backup."""
        print("\n📥 Restore Database")
        print("="*40)
        
        try:
            current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
            print(f"🗄️  Current Database: {current_db}")
            
            # Show current contact count
            try:
                contacts = view_contacts()
                contact_count = len(contacts)
                print(f"📊 Current contacts: {contact_count}")
            except Exception:
                print("📊 Current contacts: Unknown")
            
            # List available backup files
            backup_dir = "db_backup"
            if not os.path.exists(backup_dir):
                print(f"\n❌ Backup directory '{backup_dir}' does not exist!")
                print("💡 Create a backup first using the 'Backup Database' option.")
                input("\nPress Enter to continue...")
                return
            
            backup_files = []
            try:
                for filename in os.listdir(backup_dir):
                    if filename.endswith(('.db', '.sql', '.json', '.bson')):
                        filepath = os.path.join(backup_dir, filename)
                        if os.path.isfile(filepath):
                            backup_files.append(filename)
            except Exception as e:
                display_error(f"Error reading backup directory: {str(e)}")
                input("\nPress Enter to continue...")
                return
            
            if not backup_files:
                print(f"\n❌ No backup files found in '{backup_dir}' directory!")
                print("💡 Create a backup first using the 'Backup Database' option.")
                input("\nPress Enter to continue...")
                return
            
            # Sort backup files by modification time (newest first)
            backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)), reverse=True)
            
            print(f"\n📁 Available backup files ({len(backup_files)} found):")
            print("-" * 60)
            
            for i, filename in enumerate(backup_files, 1):
                filepath = os.path.join(backup_dir, filename)
                try:
                    file_size = os.path.getsize(filepath)
                    if file_size < 1024:
                        size_str = f"{file_size} bytes"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f} KB"
                    else:
                        size_str = f"{file_size / (1024 * 1024):.1f} MB"
                    
                    # Get file modification time
                    import time
                    mod_time = time.ctime(os.path.getmtime(filepath))
                    
                    print(f"{i:2d}. {filename}")
                    print(f"    📊 Size: {size_str} | 📅 Modified: {mod_time}")
                except Exception:
                    print(f"{i:2d}. {filename}")
                    print(f"    📊 Size: Unknown | 📅 Modified: Unknown")
            
            print("0. 🔙 Cancel restore")
            
            # Get user selection
            while True:
                try:
                    choice = input(f"\nSelect backup file to restore (0-{len(backup_files)}): ").strip()
                    
                    if choice == '0':
                        print("ℹ️  Restore cancelled.")
                        input("\nPress Enter to continue...")
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(backup_files):
                        selected_file = backup_files[choice_idx]
                        break
                    else:
                        print(f"❌ Invalid choice! Please enter 0-{len(backup_files)}.")
                except ValueError:
                    print("❌ Invalid input! Please enter a number.")
            
            # Confirm restore operation
            display_warning(f"\n⚠️  WARNING: Restoring from backup will:")
            print("❌ Replace ALL current data")
            print("❌ This action cannot be undone!")
            print(f"📁 Backup file: {selected_file}")
            
            confirm1 = input("\nAre you sure you want to restore from this backup? (y/N): ").strip().lower()
            
            if confirm1 not in ['y', 'yes']:
                print("ℹ️  Restore cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Double confirmation for safety
            print("\n🔒 Final confirmation required:")
            confirm2 = input("Type 'RESTORE' to confirm: ").strip()
            
            if confirm2 == 'RESTORE':
                print(f"\n📥 Restoring {current_db} database from backup...")
                
                try:
                    result = db_manager.current_adapter.restore_database(selected_file)
                    
                    if result:
                        display_success("✅ Database restored successfully!")
                        print(f"📁 Restored from: {selected_file}")
                        print("💡 You may need to refresh your view to see the restored data.")
                    else:
                        display_error("❌ Database restore failed!")
                        
                        # Provide database-specific troubleshooting
                        if current_db == "POSTGRESQL":
                            print("\n💡 PostgreSQL restore troubleshooting:")
                            print("   • Ensure psql is installed and in PATH")
                            print("   • Check backup file format and integrity")
                        elif current_db == "MYSQL":
                            print("\n💡 MySQL restore troubleshooting:")
                            print("   • Ensure mysql client is installed and in PATH")
                            print("   • Check backup file format and integrity")
                        
                except Exception as e:
                    display_error(f"❌ Restore error: {str(e)}")
            else:
                print("ℹ️  Restore cancelled - confirmation text did not match.")
                
        except Exception as e:
            display_error(f"Restore handler error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def handle_reset_database(self) -> None:
        """Handle complete database reset."""
        print("\n🔄 Reset Database")
        print("="*40)
        
        try:
            current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
            print(f"🗄️  Current Database: {current_db}")
            
            # Show current contact count
            try:
                contacts = view_contacts()
                contact_count = len(contacts)
                print(f"📊 Current contacts: {contact_count}")
            except Exception:
                contact_count = 0
                print("📊 Current contacts: Unknown")
            
            # Show current table structure
            try:
                from ..core.schema_manager import schema_manager
                columns = schema_manager.get_table_columns()
                print(f"\n📋 Current table has {len(columns)} columns:")
                for i, col in enumerate(columns, 1):
                    print(f"   {i}. {col}")
            except Exception:
                print("\n📋 Current table structure: Unable to retrieve")
            
            display_warning("\n⚠️  DANGER: Complete Database Reset")
            print("="*50)
            print("This operation will:")
            print("❌ DELETE ALL contacts and data permanently")
            print("❌ REMOVE ALL custom columns")
            print("❌ DROP and RECREATE the entire table")
            print("✅ Reset to clean 6-column structure:")
            print("   • id (Primary Key)")
            print("   • name (Required)")
            print("   • phone")
            print("   • email")
            print("   • created_at (Timestamp)")
            print("   • updated_at (Timestamp)")
            print("❌ This action CANNOT be undone!")
            print("="*50)
            
            if contact_count > 0:
                print(f"\n📊 You will lose {contact_count} contacts!")
            
            print("\n💡 Consider creating a backup first if you want to preserve data.")
            
            confirm1 = input("\nAre you absolutely sure you want to reset the database? (y/N): ").strip().lower()
            
            if confirm1 not in ['y', 'yes']:
                print("ℹ️  Database reset cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Second confirmation
            print(f"\n🔒 Second confirmation:")
            print(f"You are about to PERMANENTLY DESTROY all data in {current_db}!")
            confirm2 = input("Are you really sure? (y/N): ").strip().lower()
            
            if confirm2 not in ['y', 'yes']:
                print("ℹ️  Database reset cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Final confirmation with exact text
            print("\n🔒 FINAL CONFIRMATION:")
            print("This is your last chance to cancel!")
            print("Type exactly 'RESET DATABASE' to proceed:")
            confirm3 = input("Confirmation: ").strip()
            
            if confirm3 == 'RESET DATABASE':
                print(f"\n🔄 Resetting {current_db} database...")
                print("⚠️  This may take a moment...")
                
                try:
                    # First try the reset_table_structure method
                    if hasattr(db_manager.current_adapter, 'reset_table_structure'):
                        result = db_manager.current_adapter.reset_table_structure()
                        
                        if result:
                            display_success("✅ Database reset completed successfully!")
                            print("🔄 Database now has a clean 6-column structure with no data.")
                            print("💡 You can now start adding contacts to the fresh database.")
                        else:
                            display_error("❌ Database reset failed!")
                            print("💡 The database may be in an inconsistent state.")
                    else:
                        # Fallback to full cleanup if reset_table_structure is not available
                        print("ℹ️  Using fallback cleanup method...")
                        result = db_manager.current_adapter.full_cleanup_db()
                        
                        if result:
                            display_success("✅ Database cleanup completed!")
                            print("🧹 All data removed. Table structure may still have custom columns.")
                            print("💡 Consider using table structure management to remove custom columns.")
                        else:
                            display_error("❌ Database cleanup failed!")
                    
                except Exception as e:
                    display_error(f"❌ Database reset error: {str(e)}")
                    print("💡 The database may be in an inconsistent state.")
                    print("💡 You may need to manually recreate the database.")
                    
                    # Provide database-specific troubleshooting
                    if current_db == "POSTGRESQL":
                        print("\n💡 PostgreSQL troubleshooting:")
                        print("   • Check database connection and permissions")
                        print("   • Ensure the database user has DROP/CREATE privileges")
                    elif current_db == "MYSQL":
                        print("\n💡 MySQL troubleshooting:")
                        print("   • Check database connection and permissions")
                        print("   • Ensure the database user has DROP/CREATE privileges")
                    elif current_db == "MONGODB":
                        print("\n💡 MongoDB troubleshooting:")
                        print("   • Check database connection")
                        print("   • Ensure the user has write permissions")
            else:
                print("ℹ️  Database reset cancelled - confirmation text did not match.")
                
        except Exception as e:
            display_error(f"Reset database handler error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def show_column_management(self) -> None:
        """Handle column management."""
        try:
            from ..menus.column_management_menu import column_management_menu
            column_management_menu()
        except Exception as e:
            display_error(f"Column management error: {str(e)}")
