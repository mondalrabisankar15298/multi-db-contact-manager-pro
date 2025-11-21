"""
Advanced Features Menu Handler
Handles advanced features like analytics, export, import, etc.
"""

from ..ui.ui import display_success, display_error, display_warning
from ..ui.input_helpers import get_user_input, get_yes_no_input
from ..ui.dynamic_ui import display_contacts_dynamic
from ..core.core_operations import view_contacts, bulk_update, bulk_delete
from ..core.schema_manager import schema_manager


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
                self.bulk_update_contacts()
            elif choice == "2":
                self.bulk_delete_contacts()
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
    
    def bulk_update_contacts(self) -> None:
        """Handle bulk update of contacts."""
        try:
            print("\n📝 Bulk Update Contacts")
            print("=" * 50)
            
            # Show all contacts first
            contacts = view_contacts()
            if not contacts:
                display_warning("No contacts found!")
                return
            
            print("Current contacts:")
            display_contacts_dynamic(contacts, detailed=False)
            
            # Get contact IDs to update
            print("\n📋 Select contacts to update:")
            print("Enter contact IDs separated by commas (e.g., 1,3,5)")
            print("Or enter 'all' to update all contacts")
            
            ids_input = get_user_input("Contact IDs", required=True)
            if ids_input is None:
                return
            
            # Parse contact IDs
            if ids_input.lower() == 'all':
                contact_ids = [contact[0] for contact in contacts]
            else:
                try:
                    contact_ids = [int(id_str.strip()) for id_str in ids_input.split(',')]
                except ValueError:
                    display_error("Invalid contact IDs format!")
                    return
            
            # Validate contact IDs exist
            valid_ids = [contact[0] for contact in contacts]
            invalid_ids = [cid for cid in contact_ids if cid not in valid_ids]
            if invalid_ids:
                display_error(f"Invalid contact IDs: {invalid_ids}")
                return
            
            # Get field to update
            editable_columns = schema_manager.get_editable_columns()
            print(f"\n🔧 Select field to update:")
            for i, col in enumerate(editable_columns, 1):
                col_display = col.replace('_', ' ').title()
                print(f"{i}. {col_display}")
            
            field_choice = get_user_input(f"Field choice (1-{len(editable_columns)})", input_type="int")
            if field_choice is None or field_choice < 1 or field_choice > len(editable_columns):
                display_error("Invalid field choice!")
                return
            
            field_name = editable_columns[field_choice - 1]
            field_display = field_name.replace('_', ' ').title()
            
            # Get new value
            new_value = get_user_input(f"New {field_display}", required=True)
            if new_value is None:
                return
            
            # Validate field-specific requirements
            if field_name == 'email' and new_value:
                from ..core.core_operations import validate_email
                if not validate_email(new_value):
                    display_error("Invalid email format!")
                    return
            
            if field_name == 'phone' and new_value:
                from ..core.core_operations import validate_phone, format_phone
                if not validate_phone(new_value):
                    display_error("Invalid phone format!")
                    return
                new_value = format_phone(new_value)
            
            # Confirm the operation
            print(f"\n⚠️  Confirmation:")
            print(f"   Field: {field_display}")
            print(f"   New Value: {new_value}")
            print(f"   Contacts: {len(contact_ids)} contact(s) - IDs: {contact_ids}")
            
            if not get_yes_no_input("Proceed with bulk update?"):
                display_warning("Bulk update cancelled.")
                return
            
            # Perform bulk update
            updated_count = bulk_update(contact_ids, field_name, new_value)
            
            if updated_count > 0:
                display_success(f"✅ Successfully updated {updated_count} contact(s)!")
            else:
                display_warning("No contacts were updated.")
                
        except Exception as e:
            display_error(f"Bulk update error: {str(e)}")
    
    def bulk_delete_contacts(self) -> None:
        """Handle bulk delete of contacts with multiple selection options."""
        try:
            print("\n🗑️  Bulk Delete Contacts")
            print("=" * 50)
            
            # Show all contacts first
            contacts = view_contacts()
            if not contacts:
                display_warning("No contacts found!")
                return
            
            print("Current contacts:")
            display_contacts_dynamic(contacts, detailed=False)
            
            # Selection method menu
            print("\n📋 Choose deletion method:")
            print("1. 🎯 Delete by Contact IDs")
            print("2. 🔍 Delete by Search Pattern")
            print("3. 📧 Delete by Email Domain")
            print("4. 📱 Delete by Phone Pattern")
            print("5. 📅 Delete by Date Range")
            print("6. 🧹 Delete ALL Contacts (DANGER!)")
            print("0. 🔙 Cancel")
            
            method_choice = get_user_input("Selection method (0-6)", input_type="int")
            if method_choice is None or method_choice == 0:
                return
            
            contact_ids = []
            
            if method_choice == 1:
                # Delete by IDs (original method)
                contact_ids = self._get_contacts_by_ids(contacts)
            elif method_choice == 2:
                # Delete by search pattern
                contact_ids = self._get_contacts_by_search(contacts)
            elif method_choice == 3:
                # Delete by email domain
                contact_ids = self._get_contacts_by_email_domain(contacts)
            elif method_choice == 4:
                # Delete by phone pattern
                contact_ids = self._get_contacts_by_phone_pattern(contacts)
            elif method_choice == 5:
                # Delete by date range
                contact_ids = self._get_contacts_by_date_range(contacts)
            elif method_choice == 6:
                # Delete ALL contacts
                contact_ids = self._get_all_contacts_with_confirmation(contacts)
            else:
                display_error("Invalid selection method!")
                return
            
            if not contact_ids:
                display_warning("No contacts selected for deletion.")
                return
            
            # Show contacts to be deleted
            contacts_to_delete = [contact for contact in contacts if contact[0] in contact_ids]
            print(f"\n⚠️  Contacts to be DELETED ({len(contacts_to_delete)} total):")
            display_contacts_dynamic(contacts_to_delete, detailed=True)
            
            # Final confirmation with summary
            print(f"\n🚨 FINAL CONFIRMATION:")
            print(f"   You are about to DELETE {len(contact_ids)} contact(s)")
            print(f"   Contact IDs: {contact_ids}")
            print(f"   This action CANNOT be undone!")
            print(f"   Current total contacts: {len(contacts)}")
            print(f"   Remaining after deletion: {len(contacts) - len(contact_ids)}")
            
            if not get_yes_no_input("Are you absolutely sure you want to delete these contacts?"):
                display_warning("Bulk delete cancelled.")
                return
            
            # Second confirmation for safety
            if not get_yes_no_input("Type 'y' again to confirm deletion"):
                display_warning("Bulk delete cancelled.")
                return
            
            # Perform bulk delete
            deleted_count = bulk_delete(contact_ids)
            
            if deleted_count > 0:
                display_success(f"✅ Successfully deleted {deleted_count} contact(s)!")
                print(f"📊 Remaining contacts: {len(contacts) - deleted_count}")
            else:
                display_warning("No contacts were deleted.")
                
        except Exception as e:
            display_error(f"Bulk delete error: {str(e)}")
    
    def _get_contacts_by_ids(self, contacts) -> list:
        """Get contact IDs by manual ID input."""
        print("\n🎯 Delete by Contact IDs")
        print("Enter contact IDs separated by commas (e.g., 1,3,5)")
        print("⚠️  WARNING: This action cannot be undone!")
        
        ids_input = get_user_input("Contact IDs", required=True)
        if ids_input is None:
            return []
        
        try:
            contact_ids = [int(id_str.strip()) for id_str in ids_input.split(',')]
        except ValueError:
            display_error("Invalid contact IDs format!")
            return []
        
        # Validate contact IDs exist
        valid_ids = [contact[0] for contact in contacts]
        invalid_ids = [cid for cid in contact_ids if cid not in valid_ids]
        if invalid_ids:
            display_error(f"Invalid contact IDs: {invalid_ids}")
            return []
        
        return contact_ids
    
    def _get_contacts_by_search(self, contacts) -> list:
        """Get contact IDs by searching name, email, or phone."""
        print("\n🔍 Delete by Search Pattern")
        print("Search in name, email, or phone fields")
        
        search_term = get_user_input("Search term", required=True)
        if not search_term:
            return []
        
        search_term = search_term.lower()
        matching_contacts = []
        
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            name = str(contact_dict.get('name', '')).lower()
            email = str(contact_dict.get('email', '')).lower()
            phone = str(contact_dict.get('phone', '')).lower()
            
            if (search_term in name or search_term in email or search_term in phone):
                matching_contacts.append(contact[0])
        
        if matching_contacts:
            print(f"Found {len(matching_contacts)} matching contacts")
            return matching_contacts
        else:
            display_warning(f"No contacts found matching '{search_term}'")
            return []
    
    def _get_contacts_by_email_domain(self, contacts) -> list:
        """Get contact IDs by email domain."""
        print("\n📧 Delete by Email Domain")
        print("Enter email domain (e.g., gmail.com, company.com)")
        
        domain = get_user_input("Email domain", required=True)
        if not domain:
            return []
        
        domain = domain.lower().strip()
        if not domain.startswith('@'):
            domain = '@' + domain
        
        matching_contacts = []
        
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            email = str(contact_dict.get('email', '')).lower()
            
            if email.endswith(domain):
                matching_contacts.append(contact[0])
        
        if matching_contacts:
            print(f"Found {len(matching_contacts)} contacts with domain '{domain}'")
            return matching_contacts
        else:
            display_warning(f"No contacts found with domain '{domain}'")
            return []
    
    def _get_contacts_by_phone_pattern(self, contacts) -> list:
        """Get contact IDs by phone pattern."""
        print("\n📱 Delete by Phone Pattern")
        print("Enter phone pattern (e.g., +1, 555, (424))")
        
        pattern = get_user_input("Phone pattern", required=True)
        if not pattern:
            return []
        
        pattern = pattern.lower().strip()
        matching_contacts = []
        
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            phone = str(contact_dict.get('phone', '')).lower()
            
            if pattern in phone:
                matching_contacts.append(contact[0])
        
        if matching_contacts:
            print(f"Found {len(matching_contacts)} contacts with phone pattern '{pattern}'")
            return matching_contacts
        else:
            display_warning(f"No contacts found with phone pattern '{pattern}'")
            return []
    
    def _get_contacts_by_date_range(self, contacts) -> list:
        """Get contact IDs by creation date range."""
        print("\n📅 Delete by Date Range")
        print("Delete contacts created within a date range")
        print("Date format: YYYY-MM-DD (e.g., 2025-01-01)")
        
        start_date = get_user_input("Start date (YYYY-MM-DD)", required=False)
        end_date = get_user_input("End date (YYYY-MM-DD)", required=False)
        
        if not start_date and not end_date:
            display_warning("At least one date must be provided")
            return []
        
        matching_contacts = []
        
        for contact in contacts:
            contact_dict = schema_manager.get_contact_as_dict(contact)
            created_at = str(contact_dict.get('created_at', ''))
            
            # Extract date part (first 10 characters: YYYY-MM-DD)
            if len(created_at) >= 10:
                contact_date = created_at[:10]
                
                include_contact = True
                
                if start_date and contact_date < start_date:
                    include_contact = False
                if end_date and contact_date > end_date:
                    include_contact = False
                
                if include_contact:
                    matching_contacts.append(contact[0])
        
        if matching_contacts:
            date_range = f"{start_date or 'beginning'} to {end_date or 'now'}"
            print(f"Found {len(matching_contacts)} contacts created between {date_range}")
            return matching_contacts
        else:
            display_warning("No contacts found in the specified date range")
            return []
    
    def _get_all_contacts_with_confirmation(self, contacts) -> list:
        """Get all contact IDs with extra confirmation."""
        print("\n🧹 Delete ALL Contacts")
        print("⚠️  DANGER: This will delete ALL contacts in the database!")
        print(f"   Total contacts to delete: {len(contacts)}")
        print("   This action CANNOT be undone!")
        
        if not get_yes_no_input("Are you sure you want to delete ALL contacts?"):
            return []
        
        # Extra confirmation for delete all
        confirm_text = get_user_input("Type 'DELETE ALL' to confirm", required=True)
        if confirm_text != "DELETE ALL":
            display_warning("Confirmation text incorrect. Operation cancelled.")
            return []
        
        return [contact[0] for contact in contacts]
    
