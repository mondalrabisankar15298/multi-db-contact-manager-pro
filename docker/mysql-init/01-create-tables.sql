-- MySQL initialization script for contacts table
USE contacts;

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    age INT DEFAULT 0,
    address TEXT DEFAULT 'Unknown',
    department VARCHAR(100) DEFAULT 'General',
    category VARCHAR(100) DEFAULT 'General',
    tags TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data (optional)
INSERT INTO contacts (name, phone, email) VALUES 
('Sample Contact', '+1-555-0123', 'sample@example.com')
ON DUPLICATE KEY UPDATE name=name;
