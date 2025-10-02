#!/usr/bin/env python3
"""
Contact Book Manager - Entry Point
A professional contact management system with multi-database support.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from contact_manager.app import main

if __name__ == "__main__":
    main()
