"""
Database abstraction layer for multi-database support.
Provides unified interface for SQLite, MySQL, PostgreSQL, and MongoDB.
"""

from .base import DatabaseAdapter
from .factory import DatabaseFactory
from .manager import DatabaseManager

__all__ = ['DatabaseAdapter', 'DatabaseFactory', 'DatabaseManager']
