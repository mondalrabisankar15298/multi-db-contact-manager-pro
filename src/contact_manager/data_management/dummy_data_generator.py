"""
Dummy Data Generator Module
Generates realistic contact data for testing and demonstration purposes.
"""

import random
from typing import List, Dict, Any
from ..database.manager import db_manager
from ..core.schema_manager import schema_manager

class DummyDataGenerator:
    """Generate realistic dummy contact data."""
    
    # Realistic first names
    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
        "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
        "Kenneth", "Laura", "Kevin", "Sarah", "Brian", "Kimberly", "George", "Deborah",
        "Edward", "Dorothy", "Ronald", "Lisa", "Timothy", "Nancy", "Jason", "Karen",
        "Jeffrey", "Betty", "Ryan", "Helen", "Jacob", "Sandra", "Gary", "Donna",
        "Nicholas", "Carol", "Eric", "Ruth", "Jonathan", "Sharon", "Stephen", "Michelle",
        "Larry", "Laura", "Justin", "Sarah", "Scott", "Kimberly", "Brandon", "Deborah",
        "Benjamin", "Dorothy", "Samuel", "Amy", "Gregory", "Angela", "Alexander", "Ashley",
        "Patrick", "Brenda", "Frank", "Emma", "Raymond", "Olivia", "Jack", "Cynthia"
    ]
    
    # Realistic last names
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
        "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
        "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
        "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
        "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
        "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza"
    ]
    
    # Email domains for realistic emails
    EMAIL_DOMAINS = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
        "aol.com", "protonmail.com", "zoho.com", "mail.com", "yandex.com",
        "fastmail.com", "tutanota.com", "gmx.com", "live.com", "msn.com"
    ]
    
    # Area codes for realistic phone numbers
    AREA_CODES = [
        "212", "213", "214", "215", "216", "217", "218", "219", "224", "225",
        "301", "302", "303", "304", "305", "307", "308", "309", "310", "312",
        "313", "314", "315", "316", "317", "318", "319", "320", "321", "323",
        "401", "402", "403", "404", "405", "406", "407", "408", "409", "410",
        "412", "413", "414", "415", "416", "417", "418", "419", "423", "424",
        "501", "502", "503", "504", "505", "507", "508", "509", "510", "512",
        "513", "515", "516", "517", "518", "520", "530", "540", "541", "559",
        "601", "602", "603", "605", "606", "607", "608", "609", "610", "612",
        "614", "615", "616", "617", "618", "619", "620", "623", "626", "630"
    ]
    
    @staticmethod
    def generate_name() -> str:
        """Generate a realistic full name."""
        first_name = random.choice(DummyDataGenerator.FIRST_NAMES)
        last_name = random.choice(DummyDataGenerator.LAST_NAMES)
        return f"{first_name} {last_name}"
    
    @staticmethod
    def generate_email(name: str) -> str:
        """Generate a realistic email based on the name."""
        # Clean the name and create email variations
        clean_name = name.lower().replace(" ", "")
        first_name, last_name = name.lower().split(" ", 1)
        
        # Different email patterns
        patterns = [
            f"{first_name}.{last_name}",
            f"{first_name}{last_name}",
            f"{first_name}_{last_name}",
            f"{first_name}{last_name[0]}",
            f"{first_name[0]}{last_name}",
            f"{clean_name}{random.randint(1, 999)}"
        ]
        
        email_pattern = random.choice(patterns)
        domain = random.choice(DummyDataGenerator.EMAIL_DOMAINS)
        return f"{email_pattern}@{domain}"
    
    @staticmethod
    def generate_phone() -> str:
        """Generate a realistic phone number."""
        area_code = random.choice(DummyDataGenerator.AREA_CODES)
        exchange = random.randint(200, 999)  # Avoid 0xx and 1xx exchanges
        number = random.randint(1000, 9999)
        
        # Different phone formats
        formats = [
            f"+1-{area_code}-{exchange}-{number}",
            f"({area_code}) {exchange}-{number}",
            f"{area_code}.{exchange}.{number}",
            f"{area_code}-{exchange}-{number}",
            f"+1 {area_code} {exchange} {number}"
        ]
        
        return random.choice(formats)
    
    @staticmethod
    def generate_contact() -> Dict[str, str]:
        """Generate a single realistic contact."""
        name = DummyDataGenerator.generate_name()
        email = DummyDataGenerator.generate_email(name)
        phone = DummyDataGenerator.generate_phone()
        
        return {
            "name": name,
            "email": email,
            "phone": phone
        }
    
    @staticmethod
    def generate_contacts(count: int = 10, existing_emails: set = None, existing_phones: set = None) -> List[Dict[str, str]]:
        """Generate multiple realistic contacts ensuring uniqueness against existing data."""
        contacts = []
        used_emails = existing_emails.copy() if existing_emails else set()
        used_phones = existing_phones.copy() if existing_phones else set()
        
        max_attempts = count * 10  # Prevent infinite loops
        attempts = 0
        
        while len(contacts) < count and attempts < max_attempts:
            attempts += 1
            contact = DummyDataGenerator.generate_contact()
            
            # Ensure unique emails and phones (both within this batch and against existing data)
            if contact["email"] not in used_emails and contact["phone"] not in used_phones:
                contacts.append(contact)
                used_emails.add(contact["email"])
                used_phones.add(contact["phone"])
        
        if len(contacts) < count:
            print(f"⚠️  Warning: Could only generate {len(contacts)} unique contacts out of {count} requested")
            print("   This may happen with very large datasets due to limited name/phone combinations")
        
        return contacts
    
    @staticmethod
    def get_existing_emails_and_phones():
        """Get existing emails and phones from the current database."""
        try:
            existing_contacts = db_manager.current_adapter.view_contacts()
            existing_emails = set()
            existing_phones = set()
            
            for contact in existing_contacts:
                contact_dict = schema_manager.get_contact_as_dict(contact)
                email = contact_dict.get('email')
                phone = contact_dict.get('phone')
                
                if email and email.strip():
                    existing_emails.add(email.strip().lower())
                if phone and phone.strip():
                    existing_phones.add(phone.strip())
            
            return existing_emails, existing_phones
        except Exception as e:
            print(f"⚠️  Warning: Could not fetch existing contacts: {str(e)}")
            return set(), set()
    
    @staticmethod
    def insert_dummy_data(count: int = 10, show_progress: bool = True) -> Dict[str, Any]:
        """Insert dummy data into the current database with optional progress tracking and uniqueness checking."""
        try:
            # Get existing emails and phones to avoid duplicates
            if show_progress and count > 5:
                print("🔍 Checking existing contacts for uniqueness...")
            
            existing_emails, existing_phones = DummyDataGenerator.get_existing_emails_and_phones()
            
            if show_progress and count > 5:
                print(f"📊 Found {len(existing_emails)} existing emails and {len(existing_phones)} existing phones")
            
            # Generate realistic contacts avoiding duplicates
            if show_progress and count > 20:
                print(f"📊 Generating {count} unique contacts...")
            
            contacts = DummyDataGenerator.generate_contacts(count, existing_emails, existing_phones)
            
            if len(contacts) < count:
                print(f"⚠️  Generated {len(contacts)} contacts instead of {count} due to uniqueness constraints")
            
            # Insert contacts into the current database
            inserted_count = 0
            errors = []
            progress_interval = max(1, len(contacts) // 10)  # Show progress every 10%
            
            if show_progress and len(contacts) > 20:
                print("📝 Inserting contacts into database...")
            
            for i, contact in enumerate(contacts, 1):
                try:
                    db_manager.current_adapter.add_contact(
                        name=contact["name"],
                        phone=contact["phone"],
                        email=contact["email"]
                    )
                    inserted_count += 1
                    
                    # Show progress for large datasets
                    if show_progress and len(contacts) > 50 and i % progress_interval == 0:
                        percentage = (i / len(contacts)) * 100
                        print(f"   ⏳ Progress: {i}/{len(contacts)} ({percentage:.0f}%)")
                        
                except Exception as e:
                    errors.append(f"Failed to insert {contact['name']}: {str(e)}")
            
            return {
                "success": True,
                "inserted_count": inserted_count,
                "requested_count": count,
                "generated_count": len(contacts),
                "existing_emails_found": len(existing_emails),
                "existing_phones_found": len(existing_phones),
                "errors": errors,
                "database_type": db_manager.current_adapter.__class__.__name__.replace("Adapter", "").upper(),
                "uniqueness_check": "Enabled"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "inserted_count": 0,
                "requested_count": count
            }
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """Get statistics about the dummy data generator capabilities."""
        return {
            "total_first_names": len(DummyDataGenerator.FIRST_NAMES),
            "total_last_names": len(DummyDataGenerator.LAST_NAMES),
            "total_email_domains": len(DummyDataGenerator.EMAIL_DOMAINS),
            "total_area_codes": len(DummyDataGenerator.AREA_CODES),
            "possible_combinations": len(DummyDataGenerator.FIRST_NAMES) * len(DummyDataGenerator.LAST_NAMES),
            "recommended_max": 1000,
            "phone_formats": 5,
            "email_patterns": 6
        }
