"""
Utility functions for HyperXQL.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from .config import Config
from .exceptions import DatabaseError

logger = logging.getLogger(__name__)

# Cache for database info
_db_info_cache = None

def get_current_db_info(config: Config, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get current database information, with caching.
    
    Args:
        config: Config object
        force_refresh: Whether to force refresh the cache
        
    Returns:
        Dictionary with database information or None if not available
    """
    global _db_info_cache
    
    # Return cached info if available and refresh not forced
    if _db_info_cache is not None and not force_refresh:
        return _db_info_cache
    
    try:
        # Import here to avoid circular imports
        from .db_manager import DatabaseManager
        
        db_manager = DatabaseManager(config)
        db_info = db_manager.get_database_info()
        
        # Cache the result
        _db_info_cache = db_info
        
        return db_info
    except DatabaseError as e:
        logger.warning(f"Could not get database info: {str(e)}")
        return None
    except Exception as e:
        logger.exception("Unexpected error getting database info")
        return None

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.2f} s"

def is_interactive_terminal() -> bool:
    """
    Check if the current terminal is interactive.
    
    Returns:
        True if interactive, False otherwise
    """
    return sys.stdout.isatty()

def get_terminal_width() -> int:
    """
    Get the width of the terminal.
    
    Returns:
        Terminal width in characters
    """
    try:
        return os.get_terminal_size().columns
    except (AttributeError, OSError):
        return 80  # Default width

def truncate_string(text: str, max_length: int = 80) -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def ensure_db_path(db_path_str):
    """
    Ensure database path exists and is valid.
    
    Args:
        db_path_str: String representation of database path
        
    Returns:
        Path object for the validated database path
    """
    # Convert to Path object
    db_path = Path(db_path_str).expanduser().resolve()
    
    # Ensure parent directory exists
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Database directory created/verified: {db_path.parent}")
    except Exception as e:
        logger.error(f"Error creating database directory: {e}")
        # Fallback to home directory
        fallback_path = Path.home() / ".hyperxql" / "hyperxql.db"
        fallback_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Using fallback database path: {fallback_path}")
        return fallback_path
    
    return db_path
