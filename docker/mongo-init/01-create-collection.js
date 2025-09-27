// MongoDB initialization script for contacts collection

// Switch to contacts database
db = db.getSiblingDB('contacts');

// Create contacts collection with sample document
db.contacts.insertOne({
    name: "Sample Contact",
    phone: "+1-555-0123",
    email: "sample@example.com",
    age: 0,
    address: "Unknown",
    department: "General",
    category: "General",
    tags: "",
    created_at: new Date(),
    updated_at: new Date()
});

// Create indexes for better performance
db.contacts.createIndex({ "name": 1 });
db.contacts.createIndex({ "email": 1 });
db.contacts.createIndex({ "phone": 1 });

print("MongoDB contacts collection initialized successfully!");
