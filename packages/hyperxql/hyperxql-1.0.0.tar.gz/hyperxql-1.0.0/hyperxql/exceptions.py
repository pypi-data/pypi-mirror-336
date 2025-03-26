"""
Custom exceptions for HyperXQL.
"""

class HyperXQLException(Exception):
    """Base exception for HyperXQL."""
    pass

class ConfigurationError(HyperXQLException):
    """Exception raised for configuration errors."""
    pass

class LLMAPIError(HyperXQLException):
    """Exception raised for LLM API errors."""
    pass

class DatabaseError(HyperXQLException):
    """Exception raised for database errors."""
    pass

class SQLGenerationError(HyperXQLException):
    """Exception raised for SQL generation errors."""
    pass
