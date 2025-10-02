"""
Contact Menu Handler
Handles all contact-related operations (CRUD).
"""

from ..core.core_operations import (
    add_contact, view_contacts, search_contact, 
    update_contact, delete_contact
)
from ..ui.dynamic_ui import get_contact_input_dynamic, display_contacts_dynamic
from ..ui.ui import display_success, display_error, display_warning
from ..ui.input_helpers import get_user_input, get_yes_no_input
from ..core.schema_manager import schema_manager


class ContactMenuHandler:
    """Handles contact-related menu operations."""
    
    def add_contact(self) -> None:
        """Handle adding a new contact."""
        try:
            print("\n📝 Add New Contact")
            print("="*30)
            
            contact_data = get_contact_input_dynamic()
            
            if contact_data is None:
                display_warning("Add contact cancelled.")
                return
            
            # Validate uniqueness
            from ..validation.validation_utils import ContactValidator
            validation = ContactValidator.validate_contact_uniqueness(
                contact_data.get('email', ''),
                contact_data.get('phone', '')
            )
            
            if not validation['is_valid']:
                display_error("Cannot add contact:")
                for error in validation['errors']:
                    print(f"   • {error}")
                return
            
            contact_id = add_contact(contact_data)
            if contact_id:
                display_success(f"Contact added successfully! ID: {contact_id}")
            else:
                display_error("Failed to add contact.")
                
        except Exception as e:
            display_error(f"Error adding contact: {str(e)}")
    
    def view_contacts(self) -> None:
        """Handle viewing all contacts."""
        try:
            print("\n👀 All Contacts")
            print("-"*30)
            print("\nView options:")
            print("0. 🔙 Back to Previous Menu")
            print("1. Compact view (all columns)")
            print("2. Detailed view (all columns)")
            
            choice = input("\nSelect view (0-2, or press Enter for compact): ").strip()
            
            if choice == "0":
                return
            elif choice == "111":
                print("\n👋 Thank you for using Contact Book Manager!")
                exit()
            
            contacts = view_contacts()
            
            if choice == "2":
                display_contacts_dynamic(contacts, detailed=True)
            else:
                display_contacts_dynamic(contacts, detailed=False)
                
        except Exception as e:
            display_error(f"Error viewing contacts: {str(e)}")
    
    def search_contacts(self) -> None:
        """Handle searching contacts."""
        try:
            from .search_menu import SearchMenuHandler
            search_handler = SearchMenuHandler()
            search_handler.show_search_menu()
        except Exception as e:
            display_error(f"Error in search: {str(e)}")
    
    def update_contact(self) -> None:
        """Handle updating a contact."""
        try:
            print("\n✏️  Update Contact")
            print("="*30)
            
            contact_id = get_user_input("Enter contact ID to update", input_type="int")
            if contact_id is None:
                return
            
            # Check if contact exists
            contacts = view_contacts()
            contact_exists = any(contact[0] == contact_id for contact in contacts)
            
            if not contact_exists:
                display_error(f"Contact with ID {contact_id} not found.")
                return
            
            # Get updated data
            print(f"\nUpdating contact ID {contact_id}:")
            print("(Leave fields empty to keep current values)")
            
            contact_data = get_contact_input_dynamic()
            if contact_data is None:
                display_warning("Update cancelled.")
                return
            
            # Validate uniqueness (excluding current contact)
            from ..validation.validation_utils import ContactValidator
            validation = ContactValidator.validate_contact_uniqueness(
                contact_data.get('email', ''),
                contact_data.get('phone', ''),
                exclude_id=contact_id
            )
            
            if not validation['is_valid']:
                display_error("Cannot update contact:")
                for error in validation['errors']:
                    print(f"   • {error}")
                return
            
            success = update_contact(contact_id, contact_data)
            if success:
                display_success(f"Contact {contact_id} updated successfully!")
            else:
                display_error("Failed to update contact.")
                
        except Exception as e:
            display_error(f"Error updating contact: {str(e)}")
    
    def delete_contact(self) -> None:
        """Handle deleting a contact."""
        try:
            print("\n🗑️  Delete Contact")
            print("="*30)
            
            contact_id = get_user_input("Enter contact ID to delete", input_type="int")
            if contact_id is None:
                return
            
            # Check if contact exists and show details
            contacts = view_contacts()
            target_contact = None
            for contact in contacts:
                if contact[0] == contact_id:
                    target_contact = contact
                    break
            
            if not target_contact:
                display_error(f"Contact with ID {contact_id} not found.")
                return
            
            # Show contact details
            contact_dict = schema_manager.get_contact_as_dict(target_contact)
            print(f"\nContact to delete:")
            print(f"   ID: {contact_dict.get('id')}")
            print(f"   Name: {contact_dict.get('name')}")
            print(f"   Phone: {contact_dict.get('phone', 'N/A')}")
            print(f"   Email: {contact_dict.get('email', 'N/A')}")
            
            # Confirm deletion
            if get_yes_no_input(f"\nAre you sure you want to delete this contact?"):
                success = delete_contact(contact_id)
                if success:
                    display_success(f"Contact {contact_id} deleted successfully!")
                else:
                    display_error("Failed to delete contact.")
            else:
                display_warning("Delete cancelled.")
                
        except Exception as e:
            display_error(f"Error deleting contact: {str(e)}")
