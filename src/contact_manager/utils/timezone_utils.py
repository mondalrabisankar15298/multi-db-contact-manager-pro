"""
Timezone utilities for displaying timestamps in the configured timezone.
"""

import os
from datetime import datetime
from typing import Optional, Union
import pytz


def get_display_timezone() -> pytz.BaseTzInfo:
    """Get the configured display timezone."""
    timezone_name = os.getenv('DISPLAY_TIMEZONE', 'Asia/Kolkata')
    try:
        return pytz.timezone(timezone_name)
    except pytz.UnknownTimeZoneError:
        # Fallback to Asia/Kolkata if invalid timezone
        return pytz.timezone('Asia/Kolkata')


def format_timestamp_for_display(timestamp: Union[str, datetime, None]) -> str:
    """
    Format a timestamp for display in the configured timezone.
    
    Args:
        timestamp: The timestamp to format (string, datetime, or None)
        
    Returns:
        Formatted timestamp string in the display timezone
    """
    if timestamp is None:
        return '(not set)'
    
    if isinstance(timestamp, str):
        if not timestamp or timestamp.lower() in ['none', 'null', '']:
            return '(not set)'
        
        # Try to parse the string timestamp
        try:
            # Handle different timestamp formats
            if 'T' in timestamp:
                # ISO format: 2025-10-02T08:15:30
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            elif ' ' in timestamp:
                # MySQL/PostgreSQL format: 2025-10-02 08:15:30
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            else:
                # Other formats
                dt = datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            # If parsing fails, return the original string
            return str(timestamp)
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        return str(timestamp)
    
    # Get the display timezone
    display_tz = get_display_timezone()
    
    # If datetime is naive (no timezone info), assume it's UTC
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    
    # Convert to display timezone
    local_dt = dt.astimezone(display_tz)
    
    # Format for display
    return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')


def get_current_timestamp_for_display() -> str:
    """Get current timestamp formatted for display."""
    return format_timestamp_for_display(datetime.utcnow())


def get_timezone_info() -> dict:
    """Get information about the current timezone configuration."""
    display_tz = get_display_timezone()
    now = datetime.now(display_tz)
    
    return {
        'timezone_name': str(display_tz),
        'timezone_abbreviation': now.strftime('%Z'),
        'utc_offset': now.strftime('%z'),
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S %Z')
    }
