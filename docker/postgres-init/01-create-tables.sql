-- PostgreSQL initialization script for contacts table

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    age INTEGER DEFAULT 0,
    address TEXT DEFAULT 'Unknown',
    department VARCHAR(100) DEFAULT 'General',
    category VARCHAR(100) DEFAULT 'General',
    tags TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data (optional)
INSERT INTO contacts (name, phone, email) VALUES 
('Sample Contact', '+1-555-0123', 'sample@example.com')
ON CONFLICT DO NOTHING;
