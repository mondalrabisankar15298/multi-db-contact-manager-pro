import sqlite3

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect("contacts.db")
    return conn
