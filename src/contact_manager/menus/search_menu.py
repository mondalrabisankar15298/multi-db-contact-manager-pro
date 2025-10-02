"""
Search Menu Handler
Handles search operations and advanced search functionality.
"""

from ..core.core_operations import search_contact, advanced_search
from ..ui.dynamic_ui import display_contacts_dynamic
from ..ui.ui import display_success, display_error, display_warning
from ..ui.input_helpers import get_user_input


class SearchMenuHandler:
    """Handles search-related menu operations."""
    
    def show_search_menu(self) -> None:
        """Show the search menu and handle user input."""
        while True:
            try:
                print("\n🔍 Search Contacts")
                print("="*30)
                print("1. Simple Search")
                print("2. Advanced Search")
                print("0. Back to Main Menu")
                
                choice = input("\nEnter your choice (0-2): ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    self.simple_search()
                elif choice == "2":
                    self.advanced_search()
                else:
                    display_error("Invalid choice! Please enter 0-2.")
                    
            except Exception as e:
                display_error(f"Search menu error: {str(e)}")
    
    def simple_search(self) -> None:
        """Handle simple search."""
        try:
            search_term = get_user_input("Enter search term (name, phone, or email)")
            if not search_term:
                return
            
            results = search_contact(search_term)
            
            if results:
                print(f"\n📋 Found {len(results)} contacts:")
                display_contacts_dynamic(results, detailed=False)
            else:
                display_warning("No contacts found matching your search.")
                
        except Exception as e:
            display_error(f"Search error: {str(e)}")
    
    def advanced_search(self) -> None:
        """Handle advanced search with multiple criteria."""
        try:
            print("\n🔍 Advanced Search")
            print("-"*30)
            print("Enter search criteria (leave empty to skip):")
            
            filters = {}
            
            name = get_user_input("Search by name (optional)", required=False)
            if name:
                filters['name'] = name
            
            phone = get_user_input("Search by phone (optional)", required=False)
            if phone:
                filters['phone'] = phone
            
            email = get_user_input("Search by email (optional)", required=False)
            if email:
                filters['email'] = email
            
            min_id = get_user_input("Minimum ID (optional)", input_type="int", required=False)
            if min_id is not None:
                filters['min_id'] = min_id
            
            max_id = get_user_input("Maximum ID (optional)", input_type="int", required=False)
            if max_id is not None:
                filters['max_id'] = max_id
            
            if not filters:
                display_warning("No search criteria provided.")
                return
            
            results = advanced_search(filters)
            
            if results:
                print(f"\n📋 Found {len(results)} contacts:")
                display_contacts_dynamic(results, detailed=False)
            else:
                display_warning("No contacts found matching your criteria.")
                
        except Exception as e:
            display_error(f"Advanced search error: {str(e)}")
