"""
Validation Utilities Module
Provides validation functions for contact data including uniqueness checks.
"""

from typing import Dict, Any, Optional, Tuple
from ..database.manager import db_manager
from ..core.schema_manager import schema_manager

class ContactValidator:
    """Validates contact data for uniqueness and format."""
    
    @staticmethod
    def check_email_uniqueness(email: str, exclude_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Check if email is unique in the database.
        
        Args:
            email: Email to check
            exclude_id: Contact ID to exclude from check (for updates)
            
        Returns:
            Tuple of (is_unique, message)
        """
        if not email or not email.strip():
            return True, "Email is empty"
        
        email = email.strip().lower()
        
        try:
            existing_contacts = db_manager.current_adapter.view_contacts()
            
            for contact in existing_contacts:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                contact_id = contact_dict.get('id')
                contact_email = contact_dict.get('email')
                
                # Skip if this is the same contact (for updates)
                if exclude_id and contact_id == exclude_id:
                    continue
                
                if contact_email and contact_email.strip().lower() == email:
                    return False, f"Email '{email}' is already used by contact ID {contact_id}"
            
            return True, "Email is unique"
            
        except Exception as e:
            return False, f"Error checking email uniqueness: {str(e)}"
    
    @staticmethod
    def check_phone_uniqueness(phone: str, exclude_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Check if phone number is unique in the database.
        
        Args:
            phone: Phone number to check
            exclude_id: Contact ID to exclude from check (for updates)
            
        Returns:
            Tuple of (is_unique, message)
        """
        if not phone or not phone.strip():
            return True, "Phone is empty"
        
        phone = phone.strip()
        
        try:
            existing_contacts = db_manager.current_adapter.view_contacts()
            
            for contact in existing_contacts:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                contact_id = contact_dict.get('id')
                contact_phone = contact_dict.get('phone')
                
                # Skip if this is the same contact (for updates)
                if exclude_id and contact_id == exclude_id:
                    continue
                
                if contact_phone and contact_phone.strip() == phone:
                    return False, f"Phone '{phone}' is already used by contact ID {contact_id}"
            
            return True, "Phone is unique"
            
        except Exception as e:
            return False, f"Error checking phone uniqueness: {str(e)}"
    
    @staticmethod
    def validate_contact_uniqueness(email: str = None, phone: str = None, exclude_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Validate both email and phone uniqueness.
        
        Args:
            email: Email to check (optional)
            phone: Phone to check (optional)
            exclude_id: Contact ID to exclude from check (for updates)
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check email uniqueness
        if email and email.strip():
            email_unique, email_msg = ContactValidator.check_email_uniqueness(email, exclude_id)
            if not email_unique:
                results["valid"] = False
                results["errors"].append(f"Email: {email_msg}")
        
        # Check phone uniqueness
        if phone and phone.strip():
            phone_unique, phone_msg = ContactValidator.check_phone_uniqueness(phone, exclude_id)
            if not phone_unique:
                results["valid"] = False
                results["errors"].append(f"Phone: {phone_msg}")
        
        return results
    
    @staticmethod
    def get_duplicate_statistics() -> Dict[str, Any]:
        """Get statistics about duplicate emails and phones in the database."""
        try:
            existing_contacts = db_manager.current_adapter.view_contacts()
            
            emails = {}
            phones = {}
            total_contacts = len(existing_contacts)
            
            for contact in existing_contacts:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                contact_id = contact_dict.get('id')
                email = contact_dict.get('email')
                phone = contact_dict.get('phone')
                
                # Track emails
                if email and email.strip():
                    email_key = email.strip().lower()
                    if email_key not in emails:
                        emails[email_key] = []
                    emails[email_key].append(contact_id)
                
                # Track phones
                if phone and phone.strip():
                    phone_key = phone.strip()
                    if phone_key not in phones:
                        phones[phone_key] = []
                    phones[phone_key].append(contact_id)
            
            # Find duplicates
            duplicate_emails = {email: ids for email, ids in emails.items() if len(ids) > 1}
            duplicate_phones = {phone: ids for phone, ids in phones.items() if len(ids) > 1}
            
            return {
                "total_contacts": total_contacts,
                "unique_emails": len(emails),
                "unique_phones": len(phones),
                "duplicate_emails": len(duplicate_emails),
                "duplicate_phones": len(duplicate_phones),
                "duplicate_email_details": duplicate_emails,
                "duplicate_phone_details": duplicate_phones,
                "database_clean": len(duplicate_emails) == 0 and len(duplicate_phones) == 0
            }
            
        except Exception as e:
            return {
                "error": f"Could not analyze duplicates: {str(e)}",
                "total_contacts": 0,
                "database_clean": False
            }
