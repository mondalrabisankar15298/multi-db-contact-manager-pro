"""
Navigation Module - Menu Navigation System
Handles navigation stack and menu history for the Contact Book Manager.
"""

class NavigationStack:
    """Navigation stack to track menu history."""
    
    def __init__(self):
        self.stack = []
        self.current_menu = None
    
    def push_menu(self, menu_name, menu_function):
        """Push a menu onto the navigation stack."""
        self.stack.append((menu_name, menu_function))
        self.current_menu = menu_name
    
    def pop_menu(self):
        """Pop the current menu from the stack."""
        if len(self.stack) > 0:
            return self.stack.pop()
        return None
    
    def get_previous_menu(self):
        """Get the previous menu without removing it."""
        if len(self.stack) > 1:
            return self.stack[-2]
        return None
    
    def get_current_menu(self):
        """Get the current menu."""
        if len(self.stack) > 0:
            return self.stack[-1]
        return None
    
    def clear_stack(self):
        """Clear the navigation stack."""
        self.stack = []
        self.current_menu = None
    
    def get_stack_depth(self):
        """Get the current stack depth."""
        return len(self.stack)
    
    def can_go_back(self):
        """Check if we can go back to a previous menu."""
        return len(self.stack) > 1
    
    def get_menu_history(self):
        """Get the menu history as a list."""
        return [menu[0] for menu in self.stack]

# Global navigation stack instance
nav_stack = NavigationStack()

def navigate_to_menu(menu_name, menu_function):
    """Navigate to a specific menu."""
    nav_stack.push_menu(menu_name, menu_function)
    return menu_function()

def go_back():
    """Go back to the previous menu."""
    if nav_stack.can_go_back():
        # Remove current menu
        nav_stack.pop_menu()
        # Get previous menu
        previous_menu = nav_stack.get_previous_menu()
        if previous_menu:
            menu_name, menu_function = previous_menu
            return menu_function()
    return None

def get_navigation_options():
    """Get navigation options based on current stack depth."""
    options = []
    
    if nav_stack.can_go_back():
        options.append("🔙 Back to Previous Menu")
    
    if nav_stack.get_stack_depth() > 0:
        options.append("🏠 Back to Main Menu")
    
    options.append("🚪 Exit Application")
    
    return options

def display_navigation_options():
    """Display available navigation options."""
    options = get_navigation_options()
    if options:
        print("\n" + "="*30)
        print("🧭 Navigation Options")
        print("="*30)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("="*30)
        return len(options)
    return 0

def handle_navigation_choice(choice, max_options):
    """Handle navigation choice."""
    if choice == "1" and nav_stack.can_go_back():
        return go_back()
    elif choice == "2" and nav_stack.get_stack_depth() > 0:
        # Go to main menu
        nav_stack.clear_stack()
        from main import main_menu_loop
        return main_menu_loop()
    elif choice == "3" or (choice == "1" and not nav_stack.can_go_back()):
        # Exit application
        print("\n👋 Thank you for using Contact Book Manager!")
        print("Goodbye! 👋")
        exit()
    
    return None

def add_navigation_to_menu(menu_function):
    """Decorator to add navigation options to any menu."""
    def wrapper():
        while True:
            result = menu_function()
            if result is None:
                break
            
            # Show navigation options
            max_options = display_navigation_options()
            if max_options > 0:
                choice = input(f"\nEnter your choice (1-{max_options}): ").strip()
                nav_result = handle_navigation_choice(choice, max_options)
                if nav_result is not None:
                    return nav_result
            else:
                break
        return None
    return wrapper
