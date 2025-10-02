"""
Advanced Features Menu Handler
Handles advanced features like analytics, export, import, etc.
"""

from ..ui.ui import display_success, display_error, display_warning


class AdvancedMenuHandler:
    """Handles advanced features menu operations."""
    
    def show_advanced_menu(self) -> None:
        """Show the advanced features menu."""
        while True:
            try:
                print("\n📊 Advanced Features")
                print("="*50)
                print("1. 📈 Contact Analytics")
                print("2. 🔍 Advanced Search")
                print("3. 📤 Export Data")
                print("4. 📥 Import Data")
                print("5. 🔄 Bulk Operations")
                print("6. 🏷️  Categories & Tags")
                print("7. ✅ Data Validation")
                print("8. 🔍 Data Integrity Check")
                print("9. 🎲 Insert Dummy Data")
                print("10. 🔒 Check Duplicates")
                print("0. 🔙 Back to Previous Menu")
                print("111. 🚪 Exit Application")
                print("="*50)
                
                choice = input("\nEnter your choice (0-10, 111): ").strip()
                
                if choice == "0":
                    break
                elif choice == "111":
                    print("\n👋 Thank you for using Contact Book Manager!")
                    exit()
                elif choice == "1":
                    self.show_analytics()
                elif choice == "2":
                    self.show_advanced_search()
                elif choice == "3":
                    self.show_export_menu()
                elif choice == "4":
                    self.show_import_menu()
                elif choice == "5":
                    self.show_bulk_operations()
                elif choice == "6":
                    self.show_categories_tags()
                elif choice == "7":
                    self.show_data_validation()
                elif choice == "8":
                    self.show_data_integrity()
                elif choice == "9":
                    self.handle_dummy_data()
                elif choice == "10":
                    self.handle_duplicate_check()
                else:
                    display_error("Invalid choice! Please enter 0-10 or 111.")
                    
            except Exception as e:
                display_error(f"Advanced menu error: {str(e)}")
    
    def show_analytics(self) -> None:
        """Show contact analytics."""
        try:
            from ..ui.ui import display_contact_analytics
            display_contact_analytics()
            input("\nPress Enter to continue...")
        except Exception as e:
            display_error(f"Analytics error: {str(e)}")
    
    def show_advanced_search(self) -> None:
        """Show advanced search."""
        try:
            from .search_menu import SearchMenuHandler
            search_handler = SearchMenuHandler()
            search_handler.advanced_search()
        except Exception as e:
            display_error(f"Search error: {str(e)}")
    
    def show_export_menu(self) -> None:
        """Show export menu."""
        try:
            print("\n📤 Export Data")
            print("-"*30)
            print("1. CSV Format")
            print("2. JSON Format")
            print("0. Back")
            
            choice = input("\nEnter choice (0-2): ").strip()
            
            if choice == "1":
                from ..core.core_operations import export_to_csv
                filename = export_to_csv()
                display_success(f"Data exported to: {filename}")
            elif choice == "2":
                from ..core.core_operations import export_to_json
                filename = export_to_json()
                display_success(f"Data exported to: {filename}")
            elif choice != "0":
                display_error("Invalid choice!")
                
        except Exception as e:
            display_error(f"Export error: {str(e)}")
    
    def handle_dummy_data(self) -> None:
        """Handle dummy data insertion with sub-menu options."""
        while True:
            print("\n🎲 Insert Dummy Data")
            print("="*50)
            
            try:
                from ..database.manager import db_manager
                current_db = db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper()
                print(f"🗄️  Current Database: {current_db}")
                
                # Show current contact count
                from ..core.core_operations import view_contacts
                existing_contacts = view_contacts()
                print(f"📊 Current contacts: {len(existing_contacts)}")
                
            except Exception as e:
                print(f"⚠️  Could not get database info: {str(e)}")
            
            print("\nDummy Data Options:")
            print("0. 🔙 Back to Previous Menu")
            print("1. ⚡ Quick Insert (10 contacts)")
            print("2. 🎯 Custom Insert (choose amount)")
            print("3. 👁️  Preview Sample Data")
            print("="*50)
            
            choice = input("\nEnter your choice (0-3): ").strip()
            
            if choice == '0':
                return
            elif choice == '1':
                self._quick_insert_dummy_data()
            elif choice == '2':
                self._custom_insert_dummy_data()
            elif choice == '3':
                self._preview_dummy_data()
            else:
                display_error("Invalid choice! Please enter 0-3.")
    
    def _quick_insert_dummy_data(self) -> None:
        """Quick insert 10 dummy contacts."""
        try:
            from ..data_management.dummy_data_generator import DummyDataGenerator
            
            print("\n⚡ Quick Insert - 10 Contacts")
            print("-" * 40)
            
            confirm = input("Insert 10 realistic dummy contacts? (Y/n): ").strip().lower()
            if confirm in ['', 'y', 'yes']:
                print("\n🎲 Generating 10 dummy contacts...")
                result = DummyDataGenerator.insert_dummy_data(10, show_progress=True)
                
                if result['success']:
                    display_success(f"✅ Successfully inserted {result['inserted_count']} contacts!")
                    if result.get('existing_emails_found', 0) > 0 or result.get('existing_phones_found', 0) > 0:
                        print(f"📊 Avoided {result.get('existing_emails_found', 0)} duplicate emails and {result.get('existing_phones_found', 0)} duplicate phones")
                else:
                    display_error(f"❌ Failed to insert dummy data: {result.get('error', 'Unknown error')}")
            else:
                display_warning("Cancelled.")
                
        except Exception as e:
            display_error(f"Quick insert error: {str(e)}")
    
    def _custom_insert_dummy_data(self) -> None:
        """Custom insert with user-specified count."""
        try:
            from ..data_management.dummy_data_generator import DummyDataGenerator
            
            print("\n🎯 Custom Insert")
            print("-" * 40)
            
            while True:
                count_str = input("Enter number of contacts to generate (1-1000): ").strip()
                
                if not count_str.isdigit():
                    display_error("Please enter a valid number!")
                    continue
                
                count = int(count_str)
                if count < 1 or count > 1000:
                    display_error("Please enter a number between 1 and 1000!")
                    continue
                
                break
            
            # Show warning for large numbers
            if count > 100:
                print(f"⚠️  Generating {count} contacts may take some time...")
                confirm = input("Continue? (y/N): ").strip().lower()
                if confirm != 'y':
                    display_warning("Cancelled.")
                    return
            elif count > 10:
                confirm = input(f"Generate {count} realistic dummy contacts? (Y/n): ").strip().lower()
                if confirm not in ['', 'y', 'yes']:
                    display_warning("Cancelled.")
                    return
            
            print(f"\n🎲 Generating {count} dummy contacts...")
            result = DummyDataGenerator.insert_dummy_data(count, show_progress=True)
            
            if result['success']:
                display_success(f"✅ Successfully inserted {result['inserted_count']} contacts!")
                if result.get('existing_emails_found', 0) > 0 or result.get('existing_phones_found', 0) > 0:
                    print(f"📊 Avoided {result.get('existing_emails_found', 0)} duplicate emails and {result.get('existing_phones_found', 0)} duplicate phones")
                
                # Show generation stats
                print(f"\n📈 Generation Statistics:")
                print(f"   Requested: {result.get('requested_count', count)}")
                print(f"   Generated: {result.get('generated_count', 0)}")
                print(f"   Inserted: {result.get('inserted_count', 0)}")
                print(f"   Database: {result.get('database_type', 'Unknown')}")
                print(f"   Uniqueness Check: {result.get('uniqueness_check', 'Unknown')}")
            else:
                display_error(f"❌ Failed to insert dummy data: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            display_error(f"Custom insert error: {str(e)}")
    
    def _preview_dummy_data(self) -> None:
        """Preview sample dummy data without inserting."""
        try:
            from ..data_management.dummy_data_generator import DummyDataGenerator
            
            print("\n👁️  Preview Sample Data")
            print("-" * 40)
            
            # Generate 5 sample contacts for preview
            print("🔍 Generating sample data...")
            sample_contacts = DummyDataGenerator.generate_contacts(5)
            
            if sample_contacts:
                print(f"\n📋 Sample of {len(sample_contacts)} realistic contacts:")
                print("-" * 60)
                
                for i, contact in enumerate(sample_contacts, 1):
                    print(f"{i}. Name: {contact['name']}")
                    print(f"   Phone: {contact['phone']}")
                    print(f"   Email: {contact['email']}")
                    print()
                
                print("💡 These are examples of the realistic data that will be generated.")
                print("   Each contact has unique email and phone numbers.")
                print("   Names are randomly combined from realistic first/last names.")
                print("   Phone numbers follow various realistic formats.")
                print("   Email addresses use common domains and patterns.")
                
                choice = input("\nWould you like to insert dummy data now? (y/N): ").strip().lower()
                if choice == 'y':
                    self._custom_insert_dummy_data()
            else:
                display_error("Could not generate sample data.")
                
        except Exception as e:
            display_error(f"Preview error: {str(e)}")
    
    def handle_duplicate_check(self) -> None:
        """Handle duplicate checking."""
        try:
            from ..validation.validation_utils import ContactValidator
            
            print("\n🔒 Duplicate Checker")
            print("="*30)
            print("🔍 Scanning for duplicates...")
            
            stats = ContactValidator.get_duplicate_statistics()
            
            if 'error' in stats:
                display_error(f"Error: {stats['error']}")
                return
            
            print(f"\n📊 Results:")
            print(f"   📋 Total Contacts: {stats['total_contacts']}")
            print(f"   📧 Unique Emails: {stats['unique_emails']}")
            print(f"   📞 Unique Phones: {stats['unique_phones']}")
            
            if stats['database_clean']:
                print(f"\n✅ DATABASE IS CLEAN!")
                print(f"🎉 No duplicate emails or phone numbers found.")
            else:
                print(f"\n⚠️  DUPLICATES FOUND:")
                print(f"   🔴 Duplicate Emails: {stats['duplicate_emails']}")
                print(f"   🔴 Duplicate Phones: {stats['duplicate_phones']}")
                
                if stats['duplicate_email_details']:
                    print(f"\n📧 Email Duplicates:")
                    for email, ids in list(stats['duplicate_email_details'].items())[:3]:
                        print(f"   • {email} → contacts {', '.join(map(str, ids))}")
                
                if stats['duplicate_phone_details']:
                    print(f"\n📞 Phone Duplicates:")
                    for phone, ids in list(stats['duplicate_phone_details'].items())[:3]:
                        print(f"   • {phone} → contacts {', '.join(map(str, ids))}")
            
            print(f"\n🔒 Protection: All new data is validated for uniqueness")
            input("\nPress Enter to continue...")
            
        except Exception as e:
            display_error(f"Duplicate check error: {str(e)}")
    
    def show_import_menu(self) -> None:
        """Handle data import."""
        print("\n📥 Import Data")
        print("-" * 30)
        print("0. 🔙 Back to Previous Menu")
        
        try:
            filename = input("Enter CSV filename to import: ").strip()
            if filename == "0":
                return
            
            if not filename:
                display_error("Filename cannot be empty!")
                return
            
            # Import functionality would be implemented here
            display_error("Import functionality not yet implemented in new structure.")
            
        except Exception as e:
            display_error(f"Import error: {str(e)}")
    
    def show_bulk_operations(self) -> None:
        """Handle bulk operations."""
        print("\n🔄 Bulk Operations")
        print("-" * 30)
        print("1. Bulk Update")
        print("2. Bulk Delete")
        print("0. 🔙 Back to Previous Menu")
        
        try:
            choice = input("\nEnter choice (0-2): ").strip()
            
            if choice == "0":
                return
            elif choice == "1":
                display_error("Bulk update not yet implemented in new structure.")
            elif choice == "2":
                display_error("Bulk delete not yet implemented in new structure.")
            else:
                display_error("Invalid choice!")
                
        except Exception as e:
            display_error(f"Bulk operations error: {str(e)}")
    
    def show_categories_tags(self) -> None:
        """Handle categories and tags."""
        print("\n🏷️  Categories & Tags")
        print("-" * 30)
        print("1. Add Category Column")
        print("2. Add Tags Column")
        print("3. View Contacts by Category")
        print("4. View Contacts by Tag")
        print("0. 🔙 Back to Previous Menu")
        
        try:
            choice = input("\nEnter choice (0-4): ").strip()
            
            if choice == "0":
                return
            elif choice in ["1", "2", "3", "4"]:
                display_error("Categories & Tags functionality not yet implemented in new structure.")
            else:
                display_error("Invalid choice!")
                
        except Exception as e:
            display_error(f"Categories & Tags error: {str(e)}")
    
    def show_data_validation(self) -> None:
        """Handle data validation."""
        print("\n✅ Data Validation")
        print("-" * 30)
        print("0. 🔙 Back to Previous Menu")
        
        try:
            email = input("Enter email to validate: ").strip()
            if email == "0":
                return
            
            if not email:
                display_error("Email cannot be empty!")
                return
            
            from ..core.core_operations import validate_email
            if validate_email(email):
                display_success(f"✅ '{email}' is a valid email address!")
            else:
                display_error(f"❌ '{email}' is not a valid email address!")
                
        except Exception as e:
            display_error(f"Data validation error: {str(e)}")
    
    def show_data_integrity(self) -> None:
        """Handle data integrity check."""
        print("\n🔍 Data Integrity Check")
        print("-" * 30)
        
        try:
            from ..core.core_operations import check_data_integrity
            from ..ui.ui import display_data_integrity_results
            
            print("🔍 Checking data integrity...")
            results = check_data_integrity()
            display_data_integrity_results(results)
            
        except Exception as e:
            display_error(f"Data integrity check error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
