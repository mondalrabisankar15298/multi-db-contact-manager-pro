// MongoDB initialization script for contacts collection

// Switch to contacts database
db = db.getSiblingDB('contacts');

// Create contacts collection (will be created automatically when first document is inserted)

// Create indexes for better performance
db.contacts.createIndex({ "name": 1 });
db.contacts.createIndex({ "email": 1 });
db.contacts.createIndex({ "phone": 1 });
db.contacts.createIndex({ "created_at": 1 });
db.contacts.createIndex({ "updated_at": 1 });

print("MongoDB contacts collection initialized successfully!");
